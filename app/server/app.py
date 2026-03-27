#!/usr/bin/env python3
"""
ITC-OS 2026 — Presence Server
Tracks Linux users currently logged into the server via `who` and `last`.
Exposes a REST API for the frontend to poll.
Provides authentication against Linux user accounts and admin statistics.

Usage:
    python3 app.py                    # runs on 0.0.0.0:5000
    python3 app.py --port 8080        # custom port
    python3 app.py --host 127.0.0.1   # localhost only
"""

import argparse
import crypt as _crypt
import json
import secrets
import subprocess
import time
import warnings
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

warnings.filterwarnings("ignore", category=DeprecationWarning, module="crypt")

# ── Configuration ──────────────────────────────────────────────

CORS_ORIGIN = "*"
POLL_CACHE_SEC = 5
WEB_STALE_SEC = 20
ADMIN_USERS = ["rathpisey"]
MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SEC = 60
SESSION_TIMEOUT_SEC = 3600  # 1 hour

# ── Cache ──────────────────────────────────────────────────────

_cache = {"data": None, "ts": 0}

# ── Web Presence (in-memory) ───────────────────────────────────
# { session_id: { "name": str, "loginTime": float, "lastSeen": float } }
_web_users = {}


def _prune_web_users():
    """Remove stale web sessions."""
    now = time.time()
    stale = [k for k, v in _web_users.items() if now - v.get("lastSeen", 0) > WEB_STALE_SEC]
    for k in stale:
        del _web_users[k]


# ── Authentication ─────────────────────────────────────────────

_sessions = {}        # token -> {username, role, created}
_login_attempts = {}  # ip -> [timestamp, ...]


def _rate_limited(ip):
    """Return True if IP has exceeded login attempt limit."""
    now = time.time()
    attempts = [t for t in _login_attempts.get(ip, []) if now - t < LOGIN_WINDOW_SEC]
    _login_attempts[ip] = attempts
    return len(attempts) >= MAX_LOGIN_ATTEMPTS


def _record_attempt(ip):
    _login_attempts.setdefault(ip, []).append(time.time())


def _prune_sessions():
    now = time.time()
    expired = [t for t, s in _sessions.items() if now - s["created"] > SESSION_TIMEOUT_SEC]
    for t in expired:
        del _sessions[t]


def verify_password(username, password):
    """Verify a Linux user password via getent shadow + crypt."""
    try:
        result = subprocess.run(
            ["getent", "shadow", username],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode != 0:
            return False
        fields = result.stdout.strip().split(":")
        if len(fields) < 2:
            return False
        stored = fields[1]
        if stored in ("!", "*", "!!", "", "x"):
            return False
        return secrets.compare_digest(_crypt.crypt(password, stored), stored)
    except Exception:
        return False


def create_session(username):
    """Create auth session, return (token, role)."""
    _prune_sessions()
    token = secrets.token_urlsafe(32)
    role = "admin" if username in ADMIN_USERS else "user"
    _sessions[token] = {"username": username, "role": role, "created": time.time()}
    return token, role


def validate_token(token):
    """Return session dict if valid, else None."""
    _prune_sessions()
    s = _sessions.get(token)
    if s and time.time() - s["created"] < SESSION_TIMEOUT_SEC:
        return s
    return None


# ── Admin Statistics ───────────────────────────────────────────

def get_user_stats():
    """Parse `last` for per-user login statistics."""
    stats = {}
    try:
        result = subprocess.run(
            ["last", "-n", "500", "-w"],
            capture_output=True, text=True, timeout=10
        )
        for line in result.stdout.strip().splitlines():
            line = line.strip()
            if not line or "wtmp begins" in line.lower():
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            username = parts[0]
            if username in ("reboot", "shutdown"):
                continue
            if username not in stats:
                stats[username] = {
                    "username": username,
                    "loginCount": 0,
                    "lastLogin": "",
                    "totalSeconds": 0,
                }
            stats[username]["loginCount"] += 1
            # Capture latest login (first occurrence per user is most recent)
            if not stats[username]["lastLogin"]:
                # parts[2:] has host/date info — take what's before " - " or "still logged in"
                info = " ".join(parts[2:])
                # Remove duration and logout info for cleaner display
                for sep in (" - ", " still logged in"):
                    idx = info.find(sep)
                    if idx > 0:
                        info = info[:idx]
                stats[username]["lastLogin"] = info.strip()
            # Duration in parentheses at end of line
            if "(" in line and ")" in line:
                dur_str = line[line.rindex("(") + 1 : line.rindex(")")]
                try:
                    if "+" in dur_str:
                        day_part, time_part = dur_str.split("+", 1)
                        days = int(day_part)
                    else:
                        days = 0
                        time_part = dur_str
                    hm = time_part.split(":")
                    hours = int(hm[0])
                    minutes = int(hm[1]) if len(hm) > 1 else 0
                    stats[username]["totalSeconds"] += days * 86400 + hours * 3600 + minutes * 60
                except (ValueError, IndexError):
                    pass
    except Exception:
        pass

    # Determine who's currently online
    current = get_logged_in_users()
    online = {u["username"] for u in current}
    result_list = []
    for u in sorted(stats.values(), key=lambda x: x["loginCount"], reverse=True):
        secs = u["totalSeconds"]
        h, rem = divmod(secs, 3600)
        m = rem // 60
        u["totalDuration"] = f"{h}h {m}m"
        u["isOnline"] = u["username"] in online
        result_list.append(u)
    return result_list


def get_logged_in_users():
    """Parse `who` to get currently logged-in Linux users."""
    now = time.time()
    if _cache["data"] is not None and (now - _cache["ts"]) < POLL_CACHE_SEC:
        return _cache["data"]

    users = []
    seen = set()
    try:
        result = subprocess.run(
            ["who"], capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.strip().splitlines():
            parts = line.split()
            if len(parts) < 3:
                continue
            username = parts[0]
            terminal = parts[1]
            # `who` date format varies; grab what's there
            login_time = " ".join(parts[2:4]) if len(parts) >= 4 else parts[2]
            host = ""
            # Host is usually in parentheses at the end
            if "(" in line and ")" in line:
                host = line[line.rindex("(") + 1 : line.rindex(")")]

            key = f"{username}@{terminal}"
            if key not in seen:
                seen.add(key)
                users.append(
                    {
                        "username": username,
                        "terminal": terminal,
                        "loginTime": login_time,
                        "host": host,
                    }
                )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as exc:
        # `who` not available (e.g., testing on Windows)
        users = []

    users.sort(key=lambda u: u["username"])
    _cache["data"] = users
    _cache["ts"] = now
    return users


def get_recent_logins(count=20):
    """Parse `last` to get recent login history."""
    entries = []
    try:
        result = subprocess.run(
            ["last", "-n", str(count), "-w"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        for line in result.stdout.strip().splitlines():
            line = line.strip()
            if not line or line.startswith("wtmp") or line.startswith("reboot"):
                continue
            parts = line.split()
            if len(parts) < 4:
                continue
            entries.append(
                {
                    "username": parts[0],
                    "terminal": parts[1],
                    "info": " ".join(parts[2:]),
                }
            )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        entries = []
    return entries


# ── HTTP Handler ───────────────────────────────────────────────

class PresenceHandler(SimpleHTTPRequestHandler):
    """Serves API routes under /api/ and static files from project root."""

    # Serve static files from the project root (parent of server/)
    def translate_path(self, path):
        # Strip query params
        path = urlparse(path).path
        root = Path(__file__).resolve().parent.parent
        return str(root / path.lstrip("/"))

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", CORS_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def _get_client_ip(self):
        """Get client IP, respecting X-Forwarded-For from Cloudflare."""
        forwarded = self.headers.get("CF-Connecting-IP") or self.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return self.client_address[0]

    def _get_token(self):
        """Extract bearer token from Authorization header."""
        auth = self.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            return auth[7:]
        return None

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        # Read JSON body
        length = int(self.headers.get("Content-Length", 0))
        body = {}
        if length > 0:
            raw = self.rfile.read(min(length, 4096))
            try:
                body = json.loads(raw)
            except (json.JSONDecodeError, ValueError):
                pass

        if path == "/api/auth/login":
            ip = self._get_client_ip()
            if _rate_limited(ip):
                self._json_response({"error": "Too many attempts. Try again later."}, 429)
                return
            username = str(body.get("username", "")).strip()[:32]
            password = body.get("password", "")
            if not username or not password:
                self._json_response({"error": "Username and password required."}, 400)
                return
            _record_attempt(ip)
            if not verify_password(username, password):
                # Generic message — don't reveal if user exists
                self._json_response({"error": "Invalid credentials."}, 401)
                return
            token, role = create_session(username)
            self._json_response({"ok": True, "token": token, "user": username, "role": role})

        elif path == "/api/auth/verify":
            token = self._get_token() or str(body.get("token", ""))
            session = validate_token(token)
            if session:
                self._json_response({"valid": True, "user": session["username"], "role": session["role"]})
            else:
                self._json_response({"valid": False}, 401)

        elif path == "/api/auth/logout":
            token = self._get_token() or str(body.get("token", ""))
            _sessions.pop(token, None)
            self._json_response({"ok": True})

        elif path == "/api/web/login":
            name = str(body.get("name", "")).strip()[:50]
            sid = str(body.get("sessionId", "")).strip()[:64]
            if not name or not sid:
                self._json_response({"error": "name and sessionId required"}, 400)
                return
            _prune_web_users()
            _web_users[sid] = {"name": name, "loginTime": time.time(), "lastSeen": time.time()}
            self._json_response({"ok": True, "count": len(_web_users)})

        elif path == "/api/web/heartbeat":
            sid = str(body.get("sessionId", "")).strip()[:64]
            if sid in _web_users:
                _web_users[sid]["lastSeen"] = time.time()
            _prune_web_users()
            self._json_response({"ok": True, "count": len(_web_users)})

        elif path == "/api/web/logout":
            sid = str(body.get("sessionId", "")).strip()[:64]
            _web_users.pop(sid, None)
            _prune_web_users()
            self._json_response({"ok": True, "count": len(_web_users)})

        else:
            self._json_response({"error": "not found"}, 404)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/api/users":
            self._json_response(self._api_users())
        elif path == "/api/web/users":
            _prune_web_users()
            users = [{"name": v["name"], "loginTime": v["loginTime"], "sessionId": k}
                     for k, v in _web_users.items()]
            users.sort(key=lambda u: u["loginTime"])
            self._json_response({"users": users, "count": len(users),
                                 "timestamp": datetime.utcnow().isoformat() + "Z"})
        elif path == "/api/admin/stats":
            token = self._get_token()
            session = validate_token(token)
            if not session or session["role"] != "admin":
                self._json_response({"error": "Unauthorized"}, 403)
                return
            self._json_response({
                "users": get_user_stats(),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            })
        elif path == "/api/who":
            self._json_response(self._api_who())
        elif path == "/api/last":
            self._json_response(self._api_last(parsed))
        elif path == "/api/health":
            self._json_response({"status": "ok", "time": datetime.utcnow().isoformat() + "Z"})
        else:
            # Serve static files
            super().do_GET()

    def _json_response(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _api_users(self):
        users = get_logged_in_users()
        return {
            "users": users,
            "count": len(users),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    def _api_who(self):
        """Raw `who` output for terminal display."""
        try:
            result = subprocess.run(
                ["who"], capture_output=True, text=True, timeout=5
            )
            return {"output": result.stdout, "timestamp": datetime.utcnow().isoformat() + "Z"}
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return {"output": "", "error": "who command not available"}

    def _api_last(self, parsed):
        qs = parse_qs(parsed.query)
        count = 20
        try:
            count = int(qs.get("n", [20])[0])
            count = max(1, min(count, 100))
        except (ValueError, IndexError):
            pass
        return {
            "entries": get_recent_logins(count),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    # Suppress request logs for static files; keep API logs
    def log_message(self, format, *args):
        if self.path.startswith("/api/"):
            super().log_message(format, *args)


# ── Main ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="ITC-OS Presence Server")
    parser.add_argument("--host", default="0.0.0.0", help="Bind address (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=5000, help="Port (default: 5000)")
    args = parser.parse_args()

    server = HTTPServer((args.host, args.port), PresenceHandler)
    print(f"[Presence Server] http://{args.host}:{args.port}")
    print(f"  API endpoints:")
    print(f"    GET  /api/users         — currently logged-in Linux users")
    print(f"    GET  /api/web/users     — web visitors")
    print(f"    POST /api/web/login     — register web visitor")
    print(f"    POST /api/web/heartbeat — keep web session alive")
    print(f"    POST /api/web/logout    — unregister web visitor")
    print(f"    POST /api/auth/login    — authenticate Linux user")
    print(f"    POST /api/auth/verify   — validate session token")
    print(f"    POST /api/auth/logout   — end session")
    print(f"    GET  /api/admin/stats   — user statistics (admin only)")
    print(f"    GET  /api/who           — raw `who` output")
    print(f"    GET  /api/last          — recent login history")
    print(f"    GET  /api/health        — server health check")
    print(f"  Static files served from: {Path(__file__).resolve().parent.parent}")
    print(f"  Press Ctrl+C to stop.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Presence Server] Stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
