#!/usr/bin/env python3
"""
ITC-OS 2026 — Presence Server
Tracks Linux users currently logged into the server via `who` and `last`.
Exposes a REST API for the frontend to poll.

Usage:
    python3 app.py                    # runs on 0.0.0.0:5000
    python3 app.py --port 8080        # custom port
    python3 app.py --host 127.0.0.1   # localhost only
"""

import argparse
import json
import subprocess
import time
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# ── Configuration ──────────────────────────────────────────────

CORS_ORIGIN = "*"  # Restrict in production, e.g. "https://rathpiseyalpha.github.io"
POLL_CACHE_SEC = 5  # Cache `who` output for this many seconds
WEB_STALE_SEC = 20  # Prune web visitors after 20s without heartbeat

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
        # CORS headers for all responses
        self.send_header("Access-Control-Allow-Origin", CORS_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

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

        if path == "/api/web/login":
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
    print(f"    GET  /api/users       — currently logged-in Linux users")
    print(f"    GET  /api/web/users   — web visitors")
    print(f"    POST /api/web/login   — register web visitor")
    print(f"    POST /api/web/heartbeat — keep web session alive")
    print(f"    POST /api/web/logout  — unregister web visitor")
    print(f"    GET  /api/who         — raw `who` output")
    print(f"    GET  /api/last        — recent login history")
    print(f"    GET  /api/health      — server health check")
    print(f"  Static files served from: {Path(__file__).resolve().parent.parent}")
    print(f"  Press Ctrl+C to stop.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Presence Server] Stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
