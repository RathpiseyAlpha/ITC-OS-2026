#!/usr/bin/env python3
"""
ITC-OS 2026 — Presence Server (Flask)
Tracks Linux users currently logged into the server via `who` and `last`.
Exposes a REST API for the frontend to poll.
Provides authentication against Linux user accounts and admin statistics.

Usage:
    python3 app.py                    # runs on 0.0.0.0:5000
    python3 app.py --port 8080        # custom port
    python3 app.py --host 127.0.0.1   # localhost only
"""

import argparse
import crypt as _crypt  # type: ignore[deprecated]
import json
import math
import os
import re
import secrets
import subprocess
import threading
import time
import warnings
from datetime import datetime, timedelta, timezone
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

warnings.filterwarnings("ignore", category=DeprecationWarning, module="crypt")

# Phnom Penh is UTC+7
_PPH = timezone(timedelta(hours=7))

# ── Configuration ──────────────────────────────────────────────

CORS_ORIGIN = "*"
POLL_CACHE_SEC = 5
WEB_STALE_SEC = 20
ADMIN_USERS = ["rathpisey"]
MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SEC = 60
SESSION_TIMEOUT_SEC = 3600  # 1 hour

# ── Deadline Storage ───────────────────────────────────────────

_DEADLINES_FILE = Path(__file__).resolve().parent / "deadlines.json"


def _load_deadlines():
    """Load deadlines from JSON file."""
    if _DEADLINES_FILE.exists():
        try:
            with open(_DEADLINES_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_deadlines(data):
    """Save deadlines to JSON file."""
    with open(_DEADLINES_FILE, "w") as f:
        json.dump(data, f, indent=2)


# In-memory cache refreshed from disk on every read
_deadlines = _load_deadlines()


def _debug_enabled():
    return os.environ.get("ITC_OS_DEBUG", "").strip().lower() in (
        "1", "true", "yes", "on",
    )


def _debug_log(*parts):
    if not _debug_enabled():
        return
    ts = datetime.now().isoformat(timespec="seconds")
    print("[DEBUG " + ts + "]", *parts, flush=True)


# ── Student Roster ─────────────────────────────────────────────

STUDENTS = {
    "p20240032": {"name": "CHEA SEAVHONG", "user": "se-chea-seavhong"},
    "p20240007": {"name": "CHHENG KIMTER", "user": "se-chheng-kimter"},
    "p20240044": {"name": "CHHENG SOKUNTHEARY", "user": "se-chheng-sokuntheary"},
    "p20240050": {"name": "CHHI LAYHORNG", "user": "se-chhi-layhorng"},
    "p20240024": {"name": "CHIN MENGHONG", "user": "se-chin-menghong"},
    "p20240019": {"name": "CHIV INTHERA", "user": "se-chiv-inthera"},
    "p20240067": {"name": "CHUM KIMCHHUN", "user": "se-chum-kimchhun"},
    "p20250002": {"name": "DARA PANHASETH", "user": "se-dara-panhaseth"},
    "p20240009": {"name": "EANG MENGLY", "user": "se-eang-mengly"},
    "p20240002": {"name": "HAI MONYOUDOM", "user": "se-hai-monyoudom"},
    "p20230043": {"name": "HEN CHHORDAVATTEY", "user": "se-hen-chhordavattey"},
    "p20240001": {"name": "KIV SOVANNLYDA", "user": "se-kiv-sovannlyda"},
    "p20240063": {"name": "KONG SOPHANHA", "user": "se-kong-sophanha"},
    "p20240034": {"name": "LOR HENGRITH", "user": "se-lor-hengrith"},
    "p20240013": {"name": "MI SORAKMONY", "user": "se-mi-sorakmony"},
    "p20240058": {"name": "NHEM PHADA", "user": "se-nhem-phada"},
    "p20240033": {"name": "OUK PUTHIRITH", "user": "se-ouk-puthirith"},
    "p20240047": {"name": "PAV RATANA", "user": "se-pav-ratana"},
    "p20240045": {"name": "PI SEREYVATHANAK", "user": "se-pi-sereyvathanak"},
    "p20240004": {"name": "PICH CHANVATANAK", "user": "se-pich-chanvatanak"},
    "p20240041": {"name": "PONG MENGHEANG", "user": "se-pong-mengheang"},
    "p20240043": {"name": "RASMEY RITHYSAK", "user": "se-rasmey-rithysak"},
    "p20240038": {"name": "RITH CHANKOLBOTH", "user": "se-rith-chankolboth"},
    "p20240003": {"name": "SAO DALI INACO", "user": "se-sao-dali-inaco"},
    "p20240012": {"name": "SATHYA POCH", "user": "se-sathya-poch"},
    "p20240046": {"name": "SONG PHENGROTH", "user": "se-song-phengroth"},
    "p20240023": {"name": "SUON CARO", "user": "se-suon-caro"},
    "p20240057": {"name": "TEK RITHIREACH", "user": "se-tek-rithireach"},
    "p20240055": {"name": "THAI MONIKA", "user": "se-thai-monika"},
    "p20240035": {"name": "THENG VAN HENG", "user": "se-theng-van-heng"},
    "p20240017": {"name": "THO PAGNASAKAL", "user": "se-tho-pagnasakal"},
}

_USER_TO_SID = {v["user"]: k for k, v in STUDENTS.items()}

# ── Cache ──────────────────────────────────────────────────────

_cache = {"data": None, "ts": 0}

# ── Web Presence (in-memory) ───────────────────────────────────

_web_users = {}


def _prune_web_users():
    now = time.time()
    stale = [k for k, v in _web_users.items()
             if now - v.get("lastSeen", 0) > WEB_STALE_SEC]
    for k in stale:
        del _web_users[k]


# ── Authentication ─────────────────────────────────────────────

_sessions = {}
_login_attempts = {}
_session_lock = threading.Lock()
_SESSIONS_FILE = Path(__file__).resolve().parent / "sessions.json"
_SESSION_SAVE_INTERVAL = 30  # persist at most every 30s during activity
_last_session_save = 0.0


def _load_sessions():
    """Load sessions from disk (survives server restarts)."""
    global _sessions
    if _SESSIONS_FILE.exists():
        try:
            with open(_SESSIONS_FILE, "r") as f:
                data = json.load(f)
            now = time.time()
            # Only restore sessions that haven't expired
            _sessions = {
                t: s for t, s in data.items()
                if now - s.get("last_active", s.get("created", 0)) < SESSION_TIMEOUT_SEC
            }
        except (json.JSONDecodeError, OSError, TypeError):
            _sessions = {}


def _save_sessions():
    """Persist sessions to disk. Must be called with _session_lock held."""
    try:
        with open(_SESSIONS_FILE, "w") as f:
            json.dump(_sessions, f)
    except OSError:
        pass


# Load sessions from previous run on startup
_load_sessions()


def _rate_limited(ip):
    now = time.time()
    attempts = [t for t in _login_attempts.get(ip, [])
                if now - t < LOGIN_WINDOW_SEC]
    _login_attempts[ip] = attempts
    return len(attempts) >= MAX_LOGIN_ATTEMPTS


def _record_attempt(ip):
    _login_attempts.setdefault(ip, []).append(time.time())


def _prune_sessions():
    """Remove expired sessions. Must be called with _session_lock held."""
    now = time.time()
    expired = [t for t, s in _sessions.items()
               if now - s.get("last_active", s.get("created", 0)) > SESSION_TIMEOUT_SEC]
    for t in expired:
        _sessions.pop(t, None)
    if expired:
        _save_sessions()


def verify_password(username, password):
    try:
        result = subprocess.run(
            ["getent", "shadow", username],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode != 0:
            return False
        fields = result.stdout.strip().split(":")
        if len(fields) < 2:
            return False
        stored = fields[1]
        if stored in ("!", "*", "!!", "", "x"):
            return False
        return secrets.compare_digest(
            _crypt.crypt(password, stored), stored  # type: ignore
        )
    except Exception:
        return False


def create_session(username):
    with _session_lock:
        _prune_sessions()
        token = secrets.token_urlsafe(32)
        role = "admin" if username in ADMIN_USERS else "user"
        now = time.time()
        _sessions[token] = {
            "username": username, "role": role,
            "created": now, "last_active": now,
        }
        _save_sessions()
    return token, role


def validate_token(token):
    global _last_session_save
    with _session_lock:
        _prune_sessions()
        s = _sessions.get(token)
        if s and time.time() - s.get("last_active", s["created"]) < SESSION_TIMEOUT_SEC:
            now = time.time()
            s["last_active"] = now
            # Throttle disk writes — persist activity updates periodically
            if now - _last_session_save > _SESSION_SAVE_INTERVAL:
                _save_sessions()
                _last_session_save = now
            return s
    return None


# ── Flask Helpers ──────────────────────────────────────────────

def _get_token():
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:]
    return None


def _get_client_ip():
    forwarded = (request.headers.get("CF-Connecting-IP")
                 or request.headers.get("X-Forwarded-For"))
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr


# ── Auth Decorators ────────────────────────────────────────────

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _get_token()
        session = validate_token(token)
        if not session:
            return jsonify({"error": "Unauthorized"}), 403
        request._session = session # type: ignore
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _get_token()
        session = validate_token(token)
        if not session or session["role"] != "admin":
            return jsonify({"error": "Unauthorized"}), 403
        request._session = session # type: ignore
        return f(*args, **kwargs)
    return decorated


# ── Admin Statistics ───────────────────────────────────────────

def _parse_last_date(raw):
    m = re.search(
        r'[A-Z][a-z]{2}\s+[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\d{4}',
        raw,
    )
    if m:
        try:
            dt = datetime.strptime(m.group(), "%a %b %d %H:%M:%S %Y")
            local_tz = datetime.now().astimezone().tzinfo
            return dt.replace(tzinfo=local_tz)
        except ValueError:
            pass
    return None


def get_user_stats():
    stats = {}

    try:
        with open("/etc/passwd", "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) < 7:
                    continue
                username, uid_str, shell = parts[0], parts[2], parts[6]
                try:
                    uid = int(uid_str)
                except ValueError:
                    continue
                if uid < 1000 or shell in (
                    "/usr/sbin/nologin", "/bin/false", "/sbin/nologin",
                ):
                    continue
                stats[username] = {
                    "username": username,
                    "loginCount": 0,
                    "lastLogin": "",
                    "totalSeconds": 0,
                }
    except OSError:
        pass

    try:
        result = subprocess.run(
            ["last", "-n", "500", "-F", "-w"],
            capture_output=True, text=True, timeout=10,
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
            if not stats[username]["lastLogin"]:
                info = " ".join(parts[2:])
                for sep in (" - ", " still logged in"):
                    idx = info.find(sep)
                    if idx > 0:
                        info = info[:idx]
                raw = info.strip()
                parsed_dt = _parse_last_date(raw)
                if parsed_dt:
                    stats[username]["lastLogin"] = parsed_dt.astimezone(
                        _PPH
                    ).isoformat()
                else:
                    stats[username]["lastLogin"] = raw
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
                    stats[username]["totalSeconds"] += (
                        days * 86400 + hours * 3600 + minutes * 60
                    )
                except (ValueError, IndexError):
                    pass
    except Exception:
        pass

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
    now = time.time()
    if _cache["data"] is not None and (now - _cache["ts"]) < POLL_CACHE_SEC:
        return _cache["data"]

    users = []
    seen = set()
    try:
        result = subprocess.run(
            ["who"], capture_output=True, text=True, timeout=5,
        )
        for line in result.stdout.strip().splitlines():
            parts = line.split()
            if len(parts) < 3:
                continue
            username = parts[0]
            terminal = parts[1]
            login_time = (
                " ".join(parts[2:4]) if len(parts) >= 4 else parts[2]
            )
            host = ""
            if "(" in line and ")" in line:
                host = line[line.rindex("(") + 1 : line.rindex(")")]
            key = f"{username}@{terminal}"
            if key not in seen:
                seen.add(key)
                users.append({
                    "username": username,
                    "terminal": terminal,
                    "loginTime": login_time,
                    "host": host,
                })
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        users = []

    users.sort(key=lambda u: u["username"])
    _cache["data"] = users
    _cache["ts"] = now
    return users


def get_recent_logins(count=20):
    entries = []
    try:
        result = subprocess.run(
            ["last", "-n", str(count), "-w"],
            capture_output=True, text=True, timeout=5,
        )
        for line in result.stdout.strip().splitlines():
            line = line.strip()
            if (
                not line
                or line.startswith("wtmp")
                or line.startswith("reboot")
            ):
                continue
            parts = line.split()
            if len(parts) < 4:
                continue
            entries.append({
                "username": parts[0],
                "terminal": parts[1],
                "info": " ".join(parts[2:]),
            })
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        entries = []
    return entries


# ── Lab Grading Engine ─────────────────────────────────────────

LAB_SPECS = {
    "lab1": {
        "total_points": 100,
        "files": [
            "README.md",
            "task1_os_info.txt",
            "task2_file_commands.txt",
            "task3_apt_update.txt",
            "task3_apt_install.txt",
            "task3_verify_install.txt",
            "task3_apt_remove.txt",
            "task3_config_after_remove.txt",
            "task3_apt_purge.txt",
            "task3_config_after_purge.txt",
            "task4_process_list.txt",
            "task5_app_verify.txt",
            "task5_multitasking.txt",
            "task6_virtualization_check.txt",
        ],
        "dirs": ["task2_files", "images"],
    },
    "lab2": {
        "total_points": 100,
        "files": [
            "README.md",
            "task1_basic_navigation.txt",
            "task2_filesystem_exploration.txt",
            "task3_directory_structure.txt",
            "task4_navigation_paths.txt",
            "task5_file_organization.txt",
            "task6_advanced_listing.txt",
        ],
        "dirs": [
            "images",
            "techcorp",
            "techcorp/hr",
            "techcorp/hr/policies",
            "techcorp/hr/onboarding",
            "techcorp/engineering",
            "techcorp/engineering/frontend",
            "techcorp/engineering/backend",
            "techcorp/engineering/devops",
            "techcorp/marketing",
            "techcorp/marketing/campaigns",
            "techcorp/marketing/assets",
        ],
    },
    "lab3": {
        "total_points": 100,
        "files": [
            "README.md",
            "task1_wildcards.txt",
            "task2_links.txt",
            "task3_grub.txt",
            "task4_shared_objects.txt",
            "task5_shared_library.txt",
            "task_history.txt",
        ],
        "dirs": [
            "images",
            "wildcard_lab",
            "csv_archive",
            "links_lab",
            "shared_lib_lab",
        ],
    },
    "lab4": {
        "total_points": 100,
        "files": [
            "README.md",
            "task1_redirection.txt",
            "task2_pipelines.txt",
            "task3_analysis.txt",
            "task4_processes.txt",
            "task5_orphan_zombie.txt",
            "orphan.c",
            "zombie.c",
            "access.log",
        ],
        "dirs": ["images", "redirect_lab"],
    },
    "lab5": {
        "total_points": 100,
        "files": [
            "README.md",
            "thread_lab/process_test.c",
            "thread_lab/thread_test.c",
            "thread_lab/multi_thread.c",
            "thread_lab/sleeper_threads.c",
            "thread_lab/signal_handler.c",
            "thread_lab/challenge.c",
            "images/process_vs_thread_1.png",
            "images/process_vs_thread_2.png",
            "images/thread_interaction.png",
            "images/user_kernel_mapping.png",
            "images/htop_kernel_threads.png",
            "images/signal_sigint.png",
            "images/challenge_shutdown.png",
        ],
        "dirs": ["images", "thread_lab"],
    },
    "lab6": {
        "total_points": 100,
        "files": [
            "README.md",
            "task1_users.txt",
            "task2_groups.txt",
            "task3_permissions.txt",
            "task3_stat_output.txt",
            "task4_special_bits.txt",
            "task5_acl.txt",
            "security_lab/whoami_suid.c",
            "images/task1_user_creation.png",
            "images/task1_user_modify.png",
            "images/task2_group_setup.png",
            "images/task2_multi_group.png",
            "images/task3_dir_permissions.png",
            "images/task3_access_denied.png",
            "images/task4_setgid.png",
            "images/task4_sticky_bit.png",
            "images/task4_setuid.png",
            "images/task5_acl_dir.png",
            "images/task5_acl_test.png",
            "images/task5_acl_output.png",
        ],
        "dirs": ["images", "security_lab"],
    },
    "lab7": {
        "total_points": 100,
        "files": [
            "README.md",
            "task1_warmup.txt",
            "task2_path.txt",
            "task3_doorstep.txt",
            "task4_inbox.txt",
            "task5_broadcaster.txt",
            "task6_guestbook.txt",
            "harvest_report.txt",
            "task8_mailman.txt",
            "sign_book.c",
            "scripts/warmup",
            "scripts/broadcaster",
            "scripts/harvester",
            "scripts/mailman",
            "scripts/sign_book_binary",
            "images/task1_warmup.png",
            "images/task2_path.png",
            "images/task3_doorstep.png",
            "images/task4_inbox.png",
            "images/task5_broadcaster.png",
            "images/task6_guestbook.png",
            "images/task7_harvester.png",
            "images/task8_mailman.png",
        ],
        "dirs": ["images", "scripts"],
    },
    "lab8": {
        "total_points": 100,
        "files": [
            "README.md",
            "observations.txt",
            "task0_warmup.txt",
            "task1_validation.txt",
            "task2_audit.txt",
            "task4_mutex.txt",
            "task5_red_blue.txt",
            "task6_dropzone.txt",
            "task7_cleanup.txt",
            "scripts/arg_viewer",
            "scripts/quantum_probe",
            "scripts/buy_widget",
            "scripts/bot_swarm",
            "scripts/create_dropzone",
            "scripts/cleanup",
            "images/level0_warmup.png",
            "images/level2_audit.png",
            "images/level4_mutex.png",
            "images/level5_red_blue.png",
            "images/level6_dropzone.png",
            "images/level7_cleanup.png",
        ],
        "dirs": ["images", "scripts"],
    },
    "lab9": {
        "total_points": 100,
        "files": [
            "README.md",
            "task1_vaults.txt",
            "task2_sync_scripts.txt",
            "task3_local_deadlock.txt",
            "task4_cross_deadlock.txt",
            "task5_ordering_patch.txt",
            "task6_timeout_recovery.txt",
            "task7_teardown.txt",
            "scripts/sync_up",
            "scripts/sync_down",
            "scripts/sync_timeout",
            "scripts/teardown",
            "images/level1_vaults.png",
            "images/level3_local_deadlock.png",
            "images/level4_cross_deadlock.png",
            "images/level5_ordering_patch.png",
            "images/level6_timeout_recovery.png",
            "images/level7_teardown.png",
        ],
        "dirs": ["images", "scripts"],
    },
}

# ── Class Activity Specs ───────────────────────────────────────

_ACTIVITY_MD_DIR = (
    Path(__file__).resolve().parent.parent.parent
    / "lectures"
    / "class-activity"
)
_SKIP_CONTENT_DIRS = frozenset(("screenshots", "images"))


def _parse_activity_spec(md_path, activity_name):
    try:
        text = Path(md_path).read_text(encoding="utf-8")
    except OSError:
        return None

    tree_block = None
    in_code = False
    buf = []
    for line in text.splitlines():
        if line.strip().startswith("```"):
            if in_code:
                block = "\n".join(buf)
                if (
                    f"{activity_name}/" in block
                    and ("├" in block or "└" in block)
                ):
                    tree_block = block
                    break
                buf = []
            in_code = not in_code
            continue
        if in_code:
            buf.append(line)

    if not tree_block:
        return None

    files, dirs = [], []
    root_found = False
    base_indent = None
    stack = []

    for raw in tree_block.splitlines():
        m = re.search(r"([├└])── (.+)", raw)
        if not m:
            continue
        marker_pos = raw.index(m.group(1))
        entry_raw = m.group(2)

        if not root_found:
            if entry_raw.strip().rstrip("/") == activity_name:
                root_found = True
            continue

        if base_indent is None:
            base_indent = marker_pos
        depth = (marker_pos - base_indent) // 4
        if depth < 0:
            break

        entry = re.sub(r"\s{2,}#.*$", "", entry_raw).strip()
        entry = re.sub(r"\s+←.*$", "", entry).strip()
        if not entry or "..." in entry:
            continue

        is_dir = entry.endswith("/")
        name = entry.rstrip("/")
        stack = stack[:depth]

        if is_dir:
            rel = "/".join(stack + [name]) if stack else name
            dirs.append(rel)
            stack.append(name)
        else:
            cm = re.search(r"\s{2,}#\s*(.+)$", entry_raw)
            if cm and re.search(r"optional|bonus", cm.group(1), re.I):
                continue
            if stack and stack[0] in _SKIP_CONTENT_DIRS:
                continue
            rel = "/".join(stack + [name]) if stack else name
            files.append(rel)

    if not root_found or (not files and not dirs):
        return None

    total = 100
    for line in text.splitlines():
        if "total" in line.lower() and "|" in line:
            pts = re.search(r"\*\*(\d+)(?:\s*\(\+\d+[^)]*\))?\*\*", line)
            if pts:
                total = int(pts.group(1))
                break

    return {"total_points": total, "files": files, "dirs": dirs}


def _build_activity_specs():
    specs = {}
    for i in range(1, 100):
        md = _ACTIVITY_MD_DIR / f"class-activity{i}.md"
        if not md.exists():
            break
        spec = _parse_activity_spec(md, f"activity{i}")
        if spec:
            specs[f"activity{i}"] = spec
    return specs


ACTIVITY_SPECS = _build_activity_specs()

# Hard-coded override for activity1 (its markdown tree is complex)
ACTIVITY_SPECS["activity1"] = {
    "total_points": 100,
    "files": [
        "README.md",
        "task1/file_creator_lib.c",
        "task1/file_creator_sys.c",
        "task1/file_reader_lib.c",
        "task1/file_reader_sys.c",
        "task2/dir_list_lib.c",
        "task2/dir_list_sys.c",
        "task3_strace/strace_lib_task1.txt",
        "task3_strace/strace_sys_task1.txt",
        "task3_strace/strace_lib_reader.txt",
        "task3_strace/strace_sys_reader.txt",
        "task3_strace/strace_summary_lib.txt",
        "task3_strace/strace_summary_sys.txt",
        "screenshots/task4_system_info.png",
        "screenshots/task4_process_info.png",
        "screenshots/task4_modules.png",
        "screenshots/task4_os_layers_diagram.png",
    ],
    "dirs": ["screenshots", "task1", "task2", "task3_strace"],
}

# Activity 5 permits any programming language, so source filenames vary.
ACTIVITY_SPECS["activity5"] = {
    "total_points": 100,
    "files": [
        "README.md",
        "screenshots/task1_before_semaphore.png",
        "screenshots/task1_after_semaphore.png",
        "screenshots/task2_before_semaphore.png",
        "screenshots/task2_after_semaphore.png",
    ],
    "dirs": ["screenshots", "task1_particles", "task2_hello"],
}

# Activity 6 permits any programming language, so source filenames vary.
ACTIVITY_SPECS["activity6"] = {
    "total_points": 100,
    "files": [
        "README.md",
        "screenshots/task1_deadlock.png",
        "screenshots/task2_prevention.png",
    ],
    "dirs": ["screenshots", "task1_deadlock", "task2_prevention"],
}

_SCREENSHOT_KEYWORDS = {
    "screenshots/task4_system_info.png": [
        ["system", "info"], ["cpuinfo"], ["meminfo"], ["cpu"], ["mem"],
    ],
    "screenshots/task4_process_info.png": [
        ["process", "info"], ["process"], ["proc"],
    ],
    "screenshots/task4_modules.png": [["mod"]],
    "screenshots/task4_os_layers_diagram.png": [["layer"]],
}

_DIR_ALIASES = {"task3_strace": ["task3"]}


def _try_alias(expected_lower, existing):
    for spec_dir, alts in _DIR_ALIASES.items():
        sd = spec_dir.lower()
        if expected_lower == sd or expected_lower.startswith(sd + "/"):
            for alt in alts:
                p = alt + expected_lower[len(sd):]
                if p in existing:
                    return existing[p]
        for alt in alts:
            al = alt.lower()
            if expected_lower == al or expected_lower.startswith(al + "/"):
                p = sd + expected_lower[len(al):]
                if p in existing:
                    return existing[p]
    return None


# ── File-System Helpers ────────────────────────────────────────


def _find_lab_root(username, lab_name):
    home = Path(f"/home/{username}")
    if not home.is_dir():
        return None
    try:
        for d in home.iterdir():
            if d.is_dir() and d.name.lower().startswith("os-se-"):
                for sub in d.iterdir():
                    if sub.is_dir() and sub.name.lower().startswith("os-lab-"):
                        lab_dir = sub / lab_name
                        if lab_dir.is_dir():
                            return lab_dir
        for d in home.iterdir():
            if d.is_dir() and d.name.lower().startswith("os-lab-"):
                lab_dir = d / lab_name
                if lab_dir.is_dir():
                    return lab_dir
        lab_dir = home / lab_name
        if lab_dir.is_dir():
            return lab_dir
    except PermissionError:
        return None
    return None


def _find_activity_root(username, activity_name):
    home = Path(f"/home/{username}")
    if not home.is_dir():
        return None
    try:
        for d in home.iterdir():
            if d.is_dir() and d.name.lower().startswith("os-se-"):
                for sub in d.iterdir():
                    if sub.is_dir() and sub.name.lower().startswith(
                        "os-class-activit"
                    ):
                        act_dir = sub / activity_name
                        if act_dir.is_dir():
                            return act_dir
        for d in home.iterdir():
            if d.is_dir() and d.name.lower().startswith("os-class-activit"):
                act_dir = d / activity_name
                if act_dir.is_dir():
                    return act_dir
        act_dir = home / activity_name
        if act_dir.is_dir():
            return act_dir
    except PermissionError:
        return None
    return None


def _get_file_submission_dates(root):
    if not root or not Path(root).is_dir():
        _debug_log("git-dates: skipped; invalid root:", root)
        return {}
    try:
        repo_prefix = ""
        prefix_result = subprocess.run(
            ["git", "rev-parse", "--show-prefix"],
            capture_output=True, text=True, timeout=5,
            cwd=str(root),
        )
        if prefix_result.returncode == 0:
            repo_prefix = (prefix_result.stdout or "").strip().replace(
                "\\", "/"
            )
            if repo_prefix and not repo_prefix.endswith("/"):
                repo_prefix += "/"
        _debug_log(
            "git-dates: repo prefix", repr(repo_prefix), "for", str(root)
        )

        _debug_log("git-dates: running git log in", str(root))
        result = subprocess.run(
            [
                "git", "log", "--diff-filter=A", "--format=DATE:%aI",
                "--name-only", "--", ".",
            ],
            capture_output=True, text=True, timeout=10,
            cwd=str(root),
        )
        if result.returncode != 0 or not result.stdout.strip():
            _debug_log(
                "git-dates: empty or failed",
                "cwd=" + str(root),
                "returncode=" + str(result.returncode),
                "stderr=" + repr((result.stderr or "").strip()[:400]),
                "stdout=" + repr((result.stdout or "").strip()[:400]),
                "service_user=" + os.environ.get("USER", "?"),
                "path=" + os.environ.get("PATH", ""),
            )
            return {}

        file_dates = {}
        current_date = None
        for line in result.stdout.strip().splitlines():
            if line.startswith("DATE:"):
                current_date = line[5:]
            elif line.strip() and current_date:
                fname = line.strip().replace("\\", "/")
                if repo_prefix and fname.startswith(repo_prefix):
                    fname = fname[len(repo_prefix):]
                if fname.startswith("./"):
                    fname = fname[2:]
                if not fname:
                    continue
                file_dates[fname] = current_date
        _debug_log(
            "git-dates: parsed", len(file_dates), "entries from", str(root),
        )
        return file_dates
    except subprocess.TimeoutExpired as exc:
        _debug_log(
            "git-dates: timeout",
            "cwd=" + str(root),
            "timeout=" + str(exc.timeout),
        )
        return {}
    except FileNotFoundError as exc:
        _debug_log("git-dates: git not found", "cwd=" + str(root), repr(exc))
        return {}
    except OSError as exc:
        _debug_log("git-dates: os error", "cwd=" + str(root), repr(exc))
        return {}


def _calc_late_penalty(file_dates, deadline_iso, penalty_per_day):
    if not file_dates or not deadline_iso:
        return None
    try:
        deadline_dt = datetime.fromisoformat(deadline_iso)
        if deadline_dt.tzinfo is None:
            deadline_dt = deadline_dt.replace(tzinfo=_PPH)
    except (ValueError, TypeError):
        return None

    total_files = len(file_dates)
    late_files = 0
    max_days_late = 0

    for _fname, date_iso in file_dates.items():
        try:
            fdt = datetime.fromisoformat(date_iso)
            if fdt.tzinfo is None:
                fdt = fdt.replace(tzinfo=_PPH)
            if fdt > deadline_dt:
                late_files += 1
                days = math.ceil(
                    (fdt - deadline_dt).total_seconds() / 86400
                )
                if days > max_days_late:
                    max_days_late = days
        except (ValueError, TypeError):
            continue

    if late_files == 0:
        return {
            "late": False, "lateFiles": 0, "totalFiles": total_files,
            "weight": 0, "daysLate": 0, "penalty": 0,
        }

    weight = round(late_files / total_files, 4)
    penalty = round(weight * max_days_late * penalty_per_day, 2)
    return {
        "late": True,
        "lateFiles": late_files,
        "totalFiles": total_files,
        "weight": weight,
        "daysLate": max_days_late,
        "penalty": penalty,
    }


def _list_recursive(root):
    result = {}
    root = Path(root)
    try:
        for item in root.rglob("*"):
            rel = str(item.relative_to(root)).replace("\\", "/")
            result[rel.lower()] = rel
    except PermissionError:
        pass
    return result


# ── Grading Functions ──────────────────────────────────────────


def grade_student_lab(username, lab_name):
    spec = LAB_SPECS.get(lab_name)
    if not spec:
        return {"error": f"Unknown lab: {lab_name}"}

    lab_root = _find_lab_root(username, lab_name)
    if not lab_root:
        return {
            "username": username, "lab": lab_name, "score": 0,
            "finalScore": 0, "total": spec["total_points"],
            "percentage": 0, "finalPercentage": 0,
            "found": False, "labPath": None, "items": [],
            "feedback": [
                f"Lab directory not found. Expected "
                f"~/os-se-<ID>/os-lab-<ID>/{lab_name}/"
            ],
        }

    all_items = spec.get("files", []) + spec.get("dirs", [])
    total_items = len(all_items)
    if total_items == 0:
        return {"error": "No items defined for this lab."}

    points_per_item = spec["total_points"] / total_items
    existing = _list_recursive(lab_root)

    score = 0.0
    items = []
    feedback = []

    for expected in all_items:
        expected_lower = expected.lower()
        is_dir = expected in spec.get("dirs", [])
        item_type = "dir" if is_dir else "file"

        if expected_lower in existing:
            actual_path = existing[expected_lower]
            full_path = lab_root / actual_path
            type_ok = (
                full_path.is_dir() if is_dir else full_path.is_file()
            )
            if not type_ok:
                items.append({
                    "expected": expected, "status": "wrong_type",
                    "points": 0, "maxPoints": round(points_per_item, 2),
                    "type": item_type,
                })
                feedback.append(
                    f"'{expected}' exists but is "
                    f"{'a file' if is_dir else 'a directory'} "
                    f"(expected {item_type})."
                )
                continue

            if actual_path != expected:
                penalty = min(1.0, points_per_item)
                earned = max(0, points_per_item - penalty)
                score += earned
                items.append({
                    "expected": expected, "actual": actual_path,
                    "status": "case_mismatch",
                    "points": round(earned, 2),
                    "maxPoints": round(points_per_item, 2),
                    "type": item_type,
                })
                feedback.append(
                    f"'{actual_path}' should be '{expected}' "
                    f"(naming convention: all lowercase with underscores). "
                    f"-1 point."
                )
            else:
                score += points_per_item
                items.append({
                    "expected": expected, "status": "ok",
                    "points": round(points_per_item, 2),
                    "maxPoints": round(points_per_item, 2),
                    "type": item_type,
                })
        else:
            items.append({
                "expected": expected, "status": "missing",
                "points": 0, "maxPoints": round(points_per_item, 2),
                "type": item_type,
            })
            feedback.append(f"Missing {item_type}: '{expected}'")

    score = round(min(score, spec["total_points"]), 2)
    file_dates = _get_file_submission_dates(lab_root)
    sub_date = max(file_dates.values()) if file_dates else None

    dl = _deadlines.get(lab_name, {})
    late_info = _calc_late_penalty(
        file_dates, dl.get("due"), dl.get("penalty", 5),
    )
    final_score = score
    if late_info and late_info["late"]:
        final_score = round(max(0, score - late_info["penalty"]), 2)
        feedback.append(
            f"Late penalty: {late_info['lateFiles']}/{late_info['totalFiles']}"
            f" files submitted late (max {late_info['daysLate']}d) — "
            f"-{late_info['penalty']} pts "
            f"(weight {late_info['weight']:.0%})"
        )

    return {
        "username": username, "lab": lab_name,
        "score": score, "finalScore": final_score,
        "total": spec["total_points"],
        "percentage": round(score / spec["total_points"] * 100, 1),
        "finalPercentage": round(final_score / spec["total_points"] * 100, 1),
        "found": True, "labPath": str(lab_root),
        "submissionDate": sub_date, "lateInfo": late_info,
        "fileDates": file_dates,
        "deadline": dl if dl else None,
        "items": items, "feedback": feedback,
    }


def grade_all_students(lab_name=None):
    labs = [lab_name] if lab_name else list(LAB_SPECS.keys())
    results = []
    for sid in sorted(STUDENTS.keys()):
        info = STUDENTS[sid]
        linux_user = info["user"]
        for lab in labs:
            try:
                g = grade_student_lab(linux_user, lab)
                g["id"] = sid
                g["name"] = info["name"]
                results.append(g)
            except (PermissionError, OSError):
                results.append({
                    "username": linux_user, "id": sid,
                    "name": info["name"], "lab": lab, "score": 0,
                    "finalScore": 0,
                    "total": LAB_SPECS.get(lab, {}).get("total_points", 0),
                    "percentage": 0, "finalPercentage": 0,
                    "found": False, "labPath": None,
                    "items": [],
                    "feedback": [
                        "Permission denied: cannot access home directory."
                    ],
                })
    return results


def grade_student_activity(username, activity_name):
    spec = ACTIVITY_SPECS.get(activity_name)
    if not spec:
        return {"error": f"Unknown activity: {activity_name}"}

    act_root = _find_activity_root(username, activity_name)
    if not act_root:
        return {
            "username": username, "activity": activity_name,
            "score": 0, "finalScore": 0, "total": spec["total_points"],
            "percentage": 0, "finalPercentage": 0,
            "found": False, "activityPath": None,
            "items": [],
            "feedback": [
                f"Activity directory not found. Expected "
                f"~/os-se-<ID>/os-class-activities-<ID>/{activity_name}/"
            ],
        }

    all_items = spec.get("files", []) + spec.get("dirs", [])
    total_items = len(all_items)
    if total_items == 0:
        return {"error": "No items defined for this activity."}

    points_per_item = spec["total_points"] / total_items
    existing = _list_recursive(act_root)

    score = 0.0
    items = []
    feedback = []

    for expected in all_items:
        expected_lower = expected.lower()
        is_dir = expected in spec.get("dirs", [])
        item_type = "dir" if is_dir else "file"

        if expected_lower in existing:
            actual_path = existing[expected_lower]
            full_path = act_root / actual_path
            type_ok = (
                full_path.is_dir() if is_dir else full_path.is_file()
            )
            if not type_ok:
                items.append({
                    "expected": expected, "status": "wrong_type",
                    "points": 0, "maxPoints": round(points_per_item, 2),
                    "type": item_type,
                })
                feedback.append(
                    f"'{expected}' exists but is "
                    f"{'a file' if is_dir else 'a directory'} "
                    f"(expected {item_type})."
                )
                continue

            if actual_path != expected:
                penalty = min(1.0, points_per_item)
                earned = max(0, points_per_item - penalty)
                score += earned
                items.append({
                    "expected": expected, "actual": actual_path,
                    "status": "case_mismatch",
                    "points": round(earned, 2),
                    "maxPoints": round(points_per_item, 2),
                    "type": item_type,
                })
                feedback.append(
                    f"'{actual_path}' should be '{expected}' "
                    f"(naming convention). -1 point."
                )
            else:
                score += points_per_item
                items.append({
                    "expected": expected, "status": "ok",
                    "points": round(points_per_item, 2),
                    "maxPoints": round(points_per_item, 2),
                    "type": item_type,
                })
        elif (
            alias_path := _try_alias(expected_lower, existing)
        ) is not None:
            actual_path = alias_path
            full_path = act_root / actual_path
            type_ok = (
                full_path.is_dir() if is_dir else full_path.is_file()
            )
            if not type_ok:
                items.append({
                    "expected": expected, "status": "wrong_type",
                    "points": 0, "maxPoints": round(points_per_item, 2),
                    "type": item_type,
                })
                feedback.append(
                    f"'{expected}' exists but is "
                    f"{'a file' if is_dir else 'a directory'} "
                    f"(expected {item_type})."
                )
                continue
            score += points_per_item
            items.append({
                "expected": expected, "actual": actual_path,
                "status": "ok",
                "points": round(points_per_item, 2),
                "maxPoints": round(points_per_item, 2),
                "type": item_type,
            })
        else:
            # Screenshot keyword matching for activity1
            matched_path = None
            if expected in _SCREENSHOT_KEYWORDS:
                keyword_groups = _SCREENSHOT_KEYWORDS[expected]
                for ex_lower, ex_actual in existing.items():
                    if not ex_lower.startswith("screenshots/"):
                        continue
                    base = ex_lower.rsplit("/", 1)[-1]
                    base = base.rsplit(".", 1)[0] if "." in base else base
                    if any(
                        all(kw in base for kw in grp)
                        for grp in keyword_groups
                    ):
                        full = act_root / ex_actual
                        if full.is_file():
                            matched_path = ex_actual
                            break

            if matched_path is not None:
                score += points_per_item
                items.append({
                    "expected": expected, "actual": matched_path,
                    "status": "ok",
                    "points": round(points_per_item, 2),
                    "maxPoints": round(points_per_item, 2),
                    "type": "file",
                })
            else:
                items.append({
                    "expected": expected, "status": "missing",
                    "points": 0, "maxPoints": round(points_per_item, 2),
                    "type": item_type,
                })
                feedback.append(f"Missing {item_type}: '{expected}'")

    score = round(min(score, spec["total_points"]), 2)
    file_dates = _get_file_submission_dates(act_root)
    sub_date = max(file_dates.values()) if file_dates else None

    dl = _deadlines.get(activity_name, {})
    late_info = _calc_late_penalty(
        file_dates, dl.get("due"), dl.get("penalty", 5),
    )
    final_score = score
    if late_info and late_info["late"]:
        final_score = round(max(0, score - late_info["penalty"]), 2)
        feedback.append(
            f"Late penalty: {late_info['lateFiles']}/{late_info['totalFiles']}"
            f" files submitted late (max {late_info['daysLate']}d) — "
            f"-{late_info['penalty']} pts "
            f"(weight {late_info['weight']:.0%})"
        )

    return {
        "username": username, "activity": activity_name,
        "score": score, "finalScore": final_score,
        "total": spec["total_points"],
        "percentage": round(score / spec["total_points"] * 100, 1),
        "finalPercentage": round(final_score / spec["total_points"] * 100, 1),
        "found": True, "activityPath": str(act_root),
        "submissionDate": sub_date, "lateInfo": late_info,
        "fileDates": file_dates,
        "deadline": dl if dl else None,
        "items": items, "feedback": feedback,
    }


def grade_all_activities(activity_name=None):
    acts = [activity_name] if activity_name else list(ACTIVITY_SPECS.keys())
    results = []
    for sid in sorted(STUDENTS.keys()):
        info = STUDENTS[sid]
        linux_user = info["user"]
        for act in acts:
            try:
                g = grade_student_activity(linux_user, act)
                g["id"] = sid
                g["name"] = info["name"]
                results.append(g)
            except (PermissionError, OSError):
                results.append({
                    "username": linux_user, "id": sid,
                    "name": info["name"], "activity": act, "score": 0,
                    "finalScore": 0,
                    "total": ACTIVITY_SPECS.get(act, {}).get(
                        "total_points", 0
                    ),
                    "percentage": 0, "finalPercentage": 0,
                    "found": False, "activityPath": None,
                    "items": [],
                    "feedback": [
                        "Permission denied: cannot access home directory."
                    ],
                })
    return results


def get_leaderboard():
    all_grades = grade_all_students()
    all_acts = grade_all_activities()
    per_student = {}

    def add_grade(target, category, key, grade):
        score = grade.get("score", 0) or 0
        final_score = grade.get("finalScore", score)
        total = grade.get("total", 0) or 0
        late_info = grade.get("lateInfo") or {}
        is_late = bool(late_info.get("late"))
        penalty = round(max(0, score - final_score), 2)
        percentage = round(final_score / total * 100, 1) if total else 0

        target[category][key] = {
            "score": final_score,
            "rawScore": score,
            "finalScore": final_score,
            "total": total,
            "percentage": percentage,
            "rawPercentage": grade.get("percentage", percentage),
            "finalPercentage": percentage,
            "found": grade.get("found", False),
            "late": is_late,
            "lateInfo": late_info if late_info else None,
            "penalty": penalty,
        }
        target["totalRawScore"] += score
        target["totalScore"] += final_score
        target["totalPossible"] += total
        if is_late:
            target["lateCount"] += 1
            target["totalPenalty"] = round(target["totalPenalty"] + penalty, 2)

    for g in all_grades:
        sid = g.get("id", g["username"])
        if sid not in per_student:
            per_student[sid] = {
                "id": sid, "username": g["username"],
                "name": g.get("name", sid),
                "labs": {}, "activities": {},
                "totalRawScore": 0, "totalScore": 0,
                "totalPossible": 0, "lateCount": 0,
                "totalPenalty": 0,
            }
        add_grade(per_student[sid], "labs", g["lab"], g)

    for g in all_acts:
        sid = g.get("id", g["username"])
        if sid not in per_student:
            per_student[sid] = {
                "id": sid, "username": g["username"],
                "name": g.get("name", sid),
                "labs": {}, "activities": {},
                "totalRawScore": 0, "totalScore": 0,
                "totalPossible": 0, "lateCount": 0,
                "totalPenalty": 0,
            }
        add_grade(per_student[sid], "activities", g["activity"], g)

    board = []
    for s in per_student.values():
        s["totalPercentage"] = (
            round(s["totalScore"] / s["totalPossible"] * 100, 1)
            if s["totalPossible"] > 0
            else 0
        )
        s["totalRawPercentage"] = (
            round(s["totalRawScore"] / s["totalPossible"] * 100, 1)
            if s["totalPossible"] > 0
            else 0
        )
        board.append(s)

    board.sort(key=lambda x: x["totalScore"], reverse=True)
    for i, entry in enumerate(board):
        entry["rank"] = i + 1
    return board


def get_student_tree(username, lab_name):
    lab_root = _find_lab_root(username, lab_name)
    if not lab_root:
        return None

    def build_tree(path, depth=0, max_depth=5):
        if depth > max_depth:
            return []
        items = []
        try:
            entries = sorted(
                path.iterdir(),
                key=lambda p: (not p.is_dir(), p.name.lower()),
            )
        except PermissionError:
            return items
        for entry in entries:
            if entry.name.startswith("."):
                continue
            node = {
                "name": entry.name,
                "type": "dir" if entry.is_dir() else "file",
            }
            if entry.is_dir():
                node["children"] = build_tree(entry, depth + 1, max_depth)
            else:
                try:
                    node["size"] = entry.stat().st_size
                except OSError:
                    node["size"] = 0
            items.append(node)
        return items

    return {
        "username": username, "lab": lab_name,
        "path": str(lab_root), "tree": build_tree(lab_root),
    }


def get_student_activity_tree(username, activity_name):
    act_root = _find_activity_root(username, activity_name)
    if not act_root:
        return None

    def build_tree(path, depth=0, max_depth=5):
        if depth > max_depth:
            return []
        items = []
        try:
            entries = sorted(
                path.iterdir(),
                key=lambda p: (not p.is_dir(), p.name.lower()),
            )
        except PermissionError:
            return items
        for entry in entries:
            if entry.name.startswith("."):
                continue
            node = {
                "name": entry.name,
                "type": "dir" if entry.is_dir() else "file",
            }
            if entry.is_dir():
                node["children"] = build_tree(entry, depth + 1, max_depth)
            else:
                try:
                    node["size"] = entry.stat().st_size
                except OSError:
                    node["size"] = 0
            items.append(node)
        return items

    return {
        "username": username, "activity": activity_name,
        "path": str(act_root), "tree": build_tree(act_root),
    }


# ══════════════════════════════════════════════════════════════
#  Final Exam — config, completion grading, status & controls
# ══════════════════════════════════════════════════════════════

EXAM_HOME_BASE = os.environ.get("EXAM_HOME_BASE", "/home")
EXAM_SRV_BASE = os.environ.get("EXAM_SRV_BASE", "/srv/exam")
EXAM_PAPER_DIR = os.environ.get("EXAM_PAPER_DIR", "exam-paper")
# Where paper_access / curveball_access live (run via sudo for open/seal controls,
# since this service runs as a normal user, not root).
EXAM_TOOLS_DIR = os.environ.get("EXAM_TOOLS_DIR", "/home/rathpisey/exam-final")
# Admin-editable schedule override (written from the dashboard). Takes precedence
# over EXAM_DATE / *_HHMM env vars, so the timetable can be changed live without a
# service restart.
EXAM_SCHEDULE_FILE = os.environ.get(
    "EXAM_SCHEDULE_FILE", os.path.join(EXAM_TOOLS_DIR, "schedule.json"))

# Expected deliverables in ~/os-se-<id>/final-exam/  (an item ending in "buy_" is
# matched by prefix, since that script name varies per student).
FINAL_EXAM_ITEMS = {
    "Docs": ["README.md", "commands.md", "live_mods.md"],
    "A": [
        "partA_threads/thread_demo.c", "partA_threads/signal_demo.c",
        "partA_threads/thread_map.txt",
        "partA_threads/images/a1_thread_run.png",
        "partA_threads/images/live_a.png",
    ],
    "B": [
        "partB_security/perm_report.txt",
        "partB_security/setuid_demo.c",
        "partB_security/images/b1_special_bits.png",
    ],
    "C": [
        "partC_scripting/scripts/greeter", "partC_scripting/scripts/collector",
        "partC_scripting/path_report.txt",
        "partC_scripting/images/c1_collector_run.png",
    ],
    "D": [
        "partD_secure/scripts/buy_", "partD_secure/scripts/swarm",
        "partD_secure/observations.txt",
        "partD_secure/images/d2_patched.png",
        "partD_secure/images/live_d.png",
    ],
    "E": [
        "partE_automation/scripts/backup_project",
        "partE_automation/scripts/timed_job",
        "partE_automation/cron_report.txt",
        "partE_automation/images/e1_backup_retention.png",
        "partE_automation/images/live_e.png",
    ],
}


def _exam_hhmm_ms(hhmm, d):
    h, m = (int(x) for x in hhmm.split(":"))
    return int(datetime(d.year, d.month, d.day, h, m,
                        tzinfo=_PPH).timestamp() * 1000)


def _valid_hhmm(s):
    h, m = (int(x) for x in str(s).split(":"))
    if not (0 <= h < 24 and 0 <= m < 60):
        raise ValueError("time out of range")
    return "%02d:%02d" % (h, m)


def _read_schedule_override():
    """Schedule written by the admin dashboard, if any. {} when absent/invalid."""
    try:
        with open(EXAM_SCHEDULE_FILE, encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def exam_schedule():
    ov = _read_schedule_override()
    date_s = ov.get("date") or os.environ.get("EXAM_DATE")
    if date_s:
        y, mo, da = (int(x) for x in str(date_s).split("-"))
        d = datetime(y, mo, da).date()
    else:
        d = datetime.now(_PPH).date()
    start = ov.get("start") or os.environ.get("EXAM_START_HHMM", "13:00")
    cb_open = ov.get("cbOpen") or os.environ.get("CB_OPEN_HHMM", "14:30")
    cb_seal = ov.get("cbSeal") or os.environ.get("CB_SEAL_HHMM", "14:45")
    try:
        dur = int(ov.get("durationMin") or os.environ.get("EXAM_DURATION_MIN", "120"))
    except (TypeError, ValueError):
        dur = 120
    if dur <= 0:
        dur = 120
    start_ms = _exam_hhmm_ms(start, d)
    finish = start_ms + dur * 60000
    return {
        "start": start_ms,
        # Exam ends at start + duration (the separate End field was removed).
        "finish": finish,
        "end": finish,
        "cbOpen": _exam_hhmm_ms(cb_open, d),
        "cbSeal": _exam_hhmm_ms(cb_seal, d),
        "durationMin": dur,
        # Raw values so the admin form can prefill, plus where they came from.
        "date": d.isoformat(),
        "startHHMM": start,
        "cbOpenHHMM": cb_open, "cbSealHHMM": cb_seal,
        "source": "file" if ov else (
            "env" if os.environ.get("EXAM_DATE") else "default"),
    }


def exam_set_schedule(date_s, start, cb_open, cb_seal, duration_min=120):
    """Persist an admin-supplied timetable; returns the recomputed schedule.
    Raises ValueError on malformed input (caller maps to HTTP 400)."""
    datetime.strptime(date_s, "%Y-%m-%d")  # validates the date
    try:
        dur = int(duration_min)
    except (TypeError, ValueError):
        raise ValueError("duration must be an integer")
    if not (1 <= dur <= 24 * 60):
        raise ValueError("duration out of range (1..1440 min)")
    data = {
        "date": date_s,
        "start": _valid_hhmm(start),
        "cbOpen": _valid_hhmm(cb_open),
        "cbSeal": _valid_hhmm(cb_seal),
        "durationMin": dur,
    }
    os.makedirs(os.path.dirname(EXAM_SCHEDULE_FILE), exist_ok=True)
    tmp = EXAM_SCHEDULE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f)
    os.replace(tmp, EXAM_SCHEDULE_FILE)
    return exam_schedule()


def _find_final_root(username):
    home = Path(f"{EXAM_HOME_BASE}/{username}")
    if not home.is_dir():
        return None
    try:
        for de in home.iterdir():
            if de.is_dir() and de.name.lower().startswith("os-se-"):
                fe = de / "final-exam"
                if fe.is_dir():
                    return fe
    except (PermissionError, OSError):
        return None
    return None


def _exam_present(item, found):
    il = item.lower()
    if il.endswith("buy_"):
        return any(k.startswith(il) for k in found)
    return il in found


def exam_completion(username):
    root = _find_final_root(username)
    found = set(_list_recursive(root).keys()) if root else set()
    parts, tp, tt = {}, 0, 0
    for g, items in FINAL_EXAM_ITEMS.items():
        present = sum(1 for x in items if _exam_present(x, found))
        parts[g] = {"p": present, "t": len(items)}
        tp += present
        tt += len(items)
    return {
        "found": root is not None, "present": tp, "total": tt,
        "pct": round(tp / tt * 100) if tt else 0, "parts": parts,
    }


def exam_paper_status(username):
    d = Path(EXAM_HOME_BASE) / username / EXAM_PAPER_DIR
    try:
        st = d.stat()
    except FileNotFoundError:
        return "missing"
    except (PermissionError, OSError):
        return "unknown"
    # Note: when sealed (0700 root:root) a non-root service cannot stat files
    # inside, so we judge by the directory's own mode (deployed => dir exists).
    return "open" if (st.st_mode & 0o001) else "sealed"


def exam_curveball_status(username):
    p = Path(EXAM_SRV_BASE) / username / "curveball.md"
    try:
        st = p.stat()
    except FileNotFoundError:
        return "missing"
    except (PermissionError, OSError):
        return "unknown"
    return "open" if (st.st_mode & 0o040) else "sealed"


def exam_set_access(target, action):
    """Open/seal papers or curveballs by invoking the root-owned access scripts via
    sudo (this service runs as a normal user; the exam account has passwordless sudo
    for the exam window). Returns {ok, output}."""
    script = "paper_access" if target == "paper" else "curveball_access"
    path = os.path.join(EXAM_TOOLS_DIR, script)
    try:
        r = subprocess.run(
            ["sudo", "-n", "bash", path, action],
            capture_output=True, text=True, timeout=30,
        )
        out = (r.stdout or "") + (r.stderr or "")
        return {"ok": r.returncode == 0, "output": out.strip()[:300]}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "output": str(exc)}


def _exam_blocked_shells():
    """Users whose login shell is nologin/false (i.e. SSH-blocked)."""
    blocked = set()
    try:
        with open("/etc/passwd", encoding="utf-8", errors="replace") as f:
            for line in f:
                parts = line.split(":")
                if len(parts) >= 7:
                    shell = parts[6].strip()
                    if shell.endswith("nologin") or shell.endswith("false"):
                        blocked.add(parts[0])
    except OSError:
        pass
    return blocked


def _exam_active_users():
    """Usernames with an active login session (per `who`)."""
    try:
        r = subprocess.run(["who"], capture_output=True, text=True, timeout=10)
        return {ln.split()[0] for ln in r.stdout.splitlines() if ln.split()}
    except Exception:  # noqa: BLE001
        return set()


def exam_ssh_state(user, blocked, active):
    if user in blocked:
        return "blocked"
    if user in active:
        return "connected"
    return "idle"


def exam_set_ssh(action):
    """Block/unblock SSH for all student accounts via the root-owned ssh_access
    script (nologin shell + session kill on block; shell restore on unblock)."""
    users = [STUDENTS[s]["user"] for s in sorted(STUDENTS.keys())]
    path = os.path.join(EXAM_TOOLS_DIR, "ssh_access")
    try:
        r = subprocess.run(
            ["sudo", "-n", "bash", path, action] + users,
            capture_output=True, text=True, timeout=90,
        )
        out = (r.stdout or "") + (r.stderr or "")
        return {"ok": r.returncode == 0, "output": out.strip()[-300:]}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "output": str(exc)}


def exam_admin_state():
    blocked, active = _exam_blocked_shells(), _exam_active_users()
    students = []
    for sid in sorted(STUDENTS.keys()):
        info = STUDENTS[sid]
        u = info["user"]
        c = exam_completion(u)
        students.append({
            "id": sid, "name": info["name"], "user": u,
            "found": c["found"], "pct": c["pct"], "parts": c["parts"],
            "paper": exam_paper_status(u), "cb": exam_curveball_status(u),
            "ssh": exam_ssh_state(u, blocked, active),
        })
    students.sort(key=lambda s: (-s["pct"], s["name"]))
    cb = {"open": 0, "sealed": 0, "missing": 0, "unknown": 0}
    paper = {"open": 0, "sealed": 0, "missing": 0, "unknown": 0}
    ssh = {"connected": 0, "blocked": 0, "idle": 0}
    for s in students:
        cb[s["cb"]] = cb.get(s["cb"], 0) + 1
        paper[s["paper"]] = paper.get(s["paper"], 0) + 1
        ssh[s["ssh"]] = ssh.get(s["ssh"], 0) + 1
    return {
        "serverNow": int(datetime.now(timezone.utc).timestamp() * 1000),
        "schedule": exam_schedule(),
        "env": {"homeBase": EXAM_HOME_BASE, "srvBase": EXAM_SRV_BASE,
                "paperDir": EXAM_PAPER_DIR},
        "students": students,
        "overall": {
            "totalStudents": len(students),
            "foundCount": sum(1 for s in students if s["found"]),
            "curveball": cb, "paper": paper, "ssh": ssh,
        },
    }


# Auto-block: once the exam-finish moment (start + duration) passes, block all
# student SSH access. Server-clock driven; latches so a manual unblock isn't
# immediately undone, and re-arms if the schedule is moved back to the future.
_ssh_auto_blocked = False


def _exam_autoblock_loop():
    global _ssh_auto_blocked
    while True:
        try:
            sch = exam_schedule()
            now = int(datetime.now(timezone.utc).timestamp() * 1000)
            fin = sch.get("finish")
            if fin:
                if now >= fin and not _ssh_auto_blocked:
                    exam_set_ssh("block")
                    _ssh_auto_blocked = True
                elif now < fin:
                    _ssh_auto_blocked = False
        except Exception:  # noqa: BLE001
            pass
        time.sleep(20)


# ══════════════════════════════════════════════════════════════
#  Flask Application & Routes
# ══════════════════════════════════════════════════════════════

app = Flask(__name__, static_folder=None)
CORS(app)


# ── Auth Routes ────────────────────────────────────────────────


@app.route("/api/auth/login", methods=["POST"])
def route_auth_login():
    body = request.get_json(silent=True) or {}
    ip = _get_client_ip()
    if _rate_limited(ip):
        return jsonify({"error": "Too many attempts. Try again later."}), 429
    username = str(body.get("username", "")).strip()[:32]
    password = body.get("password", "")
    if not username or not password:
        return jsonify({"error": "Username and password required."}), 400
    _record_attempt(ip)
    if not verify_password(username, password):
        return jsonify({"error": "Invalid credentials."}), 401
    token, role = create_session(username)
    return jsonify({
        "ok": True, "token": token, "user": username, "role": role,
    })


@app.route("/api/auth/verify", methods=["POST"])
def route_auth_verify():
    body = request.get_json(silent=True) or {}
    token = _get_token() or str(body.get("token", ""))
    session = validate_token(token)
    if session:
        return jsonify({
            "valid": True, "user": session["username"],
            "role": session["role"],
        })
    return jsonify({"valid": False}), 401


@app.route("/api/auth/logout", methods=["POST"])
def route_auth_logout():
    body = request.get_json(silent=True) or {}
    token = _get_token() or str(body.get("token", ""))
    with _session_lock:
        _sessions.pop(token, None)
        _save_sessions()
    return jsonify({"ok": True})


# ── Web Presence Routes ────────────────────────────────────────


@app.route("/api/web/login", methods=["POST"])
def route_web_login():
    body = request.get_json(silent=True) or {}
    name = str(body.get("name", "")).strip()[:50]
    sid = str(body.get("sessionId", "")).strip()[:64]
    if not name or not sid:
        return jsonify({"error": "name and sessionId required"}), 400
    _prune_web_users()
    _web_users[sid] = {
        "name": name, "loginTime": time.time(), "lastSeen": time.time(),
    }
    return jsonify({"ok": True, "count": len(_web_users)})


@app.route("/api/web/heartbeat", methods=["POST"])
def route_web_heartbeat():
    body = request.get_json(silent=True) or {}
    sid = str(body.get("sessionId", "")).strip()[:64]
    if sid in _web_users:
        _web_users[sid]["lastSeen"] = time.time()
    _prune_web_users()
    return jsonify({"ok": True, "count": len(_web_users)})


@app.route("/api/web/logout", methods=["POST"])
def route_web_logout():
    body = request.get_json(silent=True) or {}
    sid = str(body.get("sessionId", "")).strip()[:64]
    _web_users.pop(sid, None)
    _prune_web_users()
    return jsonify({"ok": True, "count": len(_web_users)})


@app.route("/api/web/users")
@auth_required
def route_web_users():
    _prune_web_users()
    users = [
        {"name": v["name"], "loginTime": v["loginTime"], "sessionId": k}
        for k, v in _web_users.items()
    ]
    users.sort(key=lambda u: u["loginTime"])
    return jsonify({
        "users": users, "count": len(users),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    })


# ── Server Presence Routes ─────────────────────────────────────


@app.route("/api/users")
@auth_required
def route_api_users():
    users = get_logged_in_users()
    return jsonify({
        "users": users, "count": len(users),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    })


@app.route("/api/who")
def route_api_who():
    try:
        result = subprocess.run(
            ["who"], capture_output=True, text=True, timeout=5,
        )
        return jsonify({
            "output": result.stdout,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        })
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return jsonify({"output": "", "error": "who command not available"})


@app.route("/api/last")
def route_api_last():
    count = request.args.get("n", 20, type=int)
    count = max(1, min(count, 100))
    return jsonify({
        "entries": get_recent_logins(count),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    })


@app.route("/api/health")
def route_api_health():
    return jsonify({
        "status": "ok",
        "time": datetime.utcnow().isoformat() + "Z",
    })


# ── Admin Routes ───────────────────────────────────────────────


@app.route("/api/admin/stats")
@admin_required
def route_admin_stats():
    return jsonify({
        "users": get_user_stats(),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    })


@app.route("/api/admin/grades")
@admin_required
def route_admin_grades():
    lab = request.args.get("lab")
    user = request.args.get("user")
    if user and lab:
        return jsonify(grade_student_lab(user, lab))
    results = grade_all_students(lab)
    return jsonify({"grades": results, "labs": list(LAB_SPECS.keys())})


@app.route("/api/admin/leaderboard")
@admin_required
def route_admin_leaderboard():
    return jsonify({
        "leaderboard": get_leaderboard(),
        "labs": list(LAB_SPECS.keys()),
        "activities": list(ACTIVITY_SPECS.keys()),
    })


@app.route("/api/admin/tree")
@admin_required
def route_admin_tree():
    user = request.args.get("user")
    lab = request.args.get("lab")
    if not user or not lab:
        return jsonify({"error": "user and lab params required"}), 400
    tree = get_student_tree(user, lab)
    if tree is None:
        return jsonify({"error": "Lab directory not found"}), 404
    return jsonify(tree)


@app.route("/api/admin/deadlines", methods=["POST"])
@admin_required
def route_admin_deadlines_post():
    body = request.get_json(silent=True) or {}
    deadlines = body if isinstance(body, dict) else {}
    clean = {}
    for lab_key, val in deadlines.items():
        lab_key = str(lab_key).strip()[:20]
        if not lab_key or not isinstance(val, dict):
            continue
        due = str(val.get("due", "")).strip()[:30]
        penalty = val.get("penalty", 5)
        if isinstance(penalty, (int, float)):
            penalty = max(0, min(100, int(penalty)))
        else:
            penalty = 5
        if due:
            clean[lab_key] = {"due": due, "penalty": penalty}
    global _deadlines
    _deadlines = clean
    _save_deadlines(clean)
    return jsonify({"ok": True, "deadlines": clean})


@app.route("/api/admin/activities")
@admin_required
def route_admin_activities():
    activity = request.args.get("activity")
    user = request.args.get("user")
    if user and activity:
        return jsonify(grade_student_activity(user, activity))
    grades = grade_all_activities(activity)
    return jsonify({
        "grades": grades, "activities": list(ACTIVITY_SPECS.keys()),
    })


@app.route("/api/admin/activity-tree")
@admin_required
def route_admin_activity_tree():
    user = request.args.get("user")
    activity = request.args.get("activity")
    if not user or not activity:
        return jsonify({"error": "user and activity params required"}), 400
    tree = get_student_activity_tree(user, activity)
    if tree is None:
        return jsonify({"error": "Activity directory not found"}), 404
    return jsonify(tree)


# ── Deadlines (any authenticated user) ────────────────────────


@app.route("/api/deadlines")
@auth_required
def route_api_deadlines():
    return jsonify({"deadlines": _load_deadlines()})


# ── Student Self-Service Routes ────────────────────────────────


def _get_student_info():
    """Look up student from current session. Returns (sid, info)."""
    username = request._session["username"] # type: ignore
    sid = _USER_TO_SID.get(username)
    info = STUDENTS.get(sid) if sid else None
    return sid, info


@app.route("/api/my/grades")
@auth_required
def route_my_grades():
    sid, info = _get_student_info()
    if not info:
        return jsonify({"error": "Student not found in roster"}), 404
    linux_user = info["user"]
    labs = list(LAB_SPECS.keys())
    grades = []
    for lab in labs:
        try:
            g = grade_student_lab(linux_user, lab)
            g["id"] = sid or ""
            g["name"] = info["name"]
            grades.append(g)
        except (PermissionError, OSError):
            grades.append({
                "username": linux_user, "id": sid, "name": info["name"],
                "lab": lab, "score": 0, "finalScore": 0,
                "total": LAB_SPECS[lab]["total_points"],
                "percentage": 0, "finalPercentage": 0,
                "found": False, "labPath": None,
                "items": [],
                "feedback": ["Cannot access lab directory."],
            })
    return jsonify({"grades": grades, "labs": labs})


@app.route("/api/my/tree")
@auth_required
def route_my_tree():
    sid, info = _get_student_info()
    if not info:
        return jsonify({"error": "Student not found in roster"}), 404
    lab = request.args.get("lab")
    if not lab:
        return jsonify({"error": "lab param required"}), 400
    tree = get_student_tree(info["user"], lab)
    if tree is None:
        return jsonify({"error": "Lab directory not found"}), 404
    return jsonify(tree)


@app.route("/api/my/leaderboard")
@auth_required
def route_my_leaderboard():
    return jsonify({
        "leaderboard": get_leaderboard(),
        "labs": list(LAB_SPECS.keys()),
        "activities": list(ACTIVITY_SPECS.keys()),
    })


@app.route("/api/my/activities")
@auth_required
def route_my_activities():
    sid, info = _get_student_info()
    if not info:
        return jsonify({"error": "Student not found in roster"}), 404
    linux_user = info["user"]
    acts = list(ACTIVITY_SPECS.keys())
    grades = []
    for act in acts:
        try:
            g = grade_student_activity(linux_user, act)
            g["id"] = sid or ""
            g["name"] = info["name"]
            grades.append(g)
        except (PermissionError, OSError):
            grades.append({
                "username": linux_user, "id": sid or "",
                "name": info["name"], "activity": act, "score": 0,
                "finalScore": 0,
                "total": ACTIVITY_SPECS[act]["total_points"],
                "percentage": 0, "finalPercentage": 0,
                "found": False, "activityPath": None,
                "items": [],
                "feedback": ["Cannot access activity directory."],
            })
    return jsonify({"grades": grades, "activities": acts})


@app.route("/api/my/activity-tree")
@auth_required
def route_my_activity_tree():
    sid, info = _get_student_info()
    if not info:
        return jsonify({"error": "Student not found in roster"}), 404
    activity = request.args.get("activity")
    if not activity:
        return jsonify({"error": "activity param required"}), 400
    tree = get_student_activity_tree(info["user"], activity)
    if tree is None:
        return jsonify({"error": "Activity directory not found"}), 404
    return jsonify(tree)


EXAM_PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OS Final — Exam Monitor</title>
<style>
 :root{--bg:#0e1116;--card:#171c24;--line:#262d39;--ink:#e6edf3;--mut:#8b949e}
 *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--ink);
   font:14px/1.45 system-ui,Segoe UI,Roboto,sans-serif}
 header{padding:14px 20px;border-bottom:1px solid var(--line);display:flex;
   justify-content:space-between;align-items:center}
 h1{font-size:17px;margin:0} .mut{color:var(--mut);font-size:12px}
 .wrap{padding:16px 20px;max-width:1200px;margin:0 auto}
 .timers{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin-bottom:14px}
 .t{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
 .t .lab{font-size:11px;color:var(--mut);text-transform:uppercase;letter-spacing:.06em}
 .t .big{font-size:26px;font-weight:700;font-variant-numeric:tabular-nums;margin-top:4px}
 .pill{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px;font-weight:600}
 .pill.wait{background:#1f2937;color:#9ca3af}.pill.live{background:#0f3d2e;color:#3fb37f}
 .pill.done{background:#3a1d1d;color:#e5736f}
 .card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin-bottom:14px}
 .bar{position:relative;height:18px;background:#0b0e13;border-radius:6px;overflow:hidden;min-width:120px}
 .bar>i{position:absolute;inset:0 auto 0 0;border-radius:6px}
 .bar>span{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600}
 .parts{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
 .pc{font-size:12px;font-weight:600;border-radius:6px;padding:4px 8px;color:#06120c}
 table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}
 th,td{padding:7px 9px;border-bottom:1px solid var(--line);text-align:left;font-size:13px}
 th{font-size:11px;color:var(--mut);text-transform:uppercase}
 .cell{text-align:center;font-size:12px;font-weight:600;border-radius:5px;padding:3px 0;color:#06120c}
 .ctrl button{background:#1f2937;color:var(--ink);border:1px solid var(--line);border-radius:8px;
   padding:7px 12px;font-size:13px;cursor:pointer;margin-right:8px}
 .ctrl button:hover{border-color:#3fb37f}
 input{background:#0b0e13;border:1px solid var(--line);color:var(--ink);border-radius:8px;padding:9px 11px;font-size:14px}
 #login{max-width:340px;margin:60px auto;display:flex;flex-direction:column;gap:10px}
 .miss{color:#6b7280;font-style:italic} .hide{display:none}
 .env{color:var(--mut);font-size:12px;margin:2px 0 12px;display:flex;gap:14px;flex-wrap:wrap}
</style></head>
<body>
<header><h1>OS Practical Final — Monitor</h1>
  <div class="mut" id="who"></div></header>

<div id="login" class="wrap">
  <div class="mut">Log in with your server account to see your exam status.</div>
  <input id="u" placeholder="username" autocomplete="username">
  <input id="p" type="password" placeholder="password" autocomplete="current-password">
  <button class="ctrl" onclick="doLogin()" style="background:#0f3d2e;color:#3fb37f;border:1px solid #3fb37f;border-radius:8px;padding:9px">Log in</button>
  <div class="mut" id="loginErr" style="color:#e5736f"></div>
</div>

<div id="app" class="wrap hide">
  <section class="timers">
    <div class="t"><div class="lab">Exam</div><div class="big" id="exam">--:--</div><div id="examSt"></div></div>
    <div class="t"><div class="lab">Curveball release</div><div class="big" id="cbo">--:--</div><div id="cboSt"></div></div>
    <div class="t"><div class="lab">Curveball closes</div><div class="big" id="cbs">--:--</div><div id="cbsSt"></div></div>
  </section>

  <div id="meCard" class="card hide"></div>

  <div id="adminWrap" class="hide">
    <div class="env" id="env"></div>
    <div class="card ctrl">
      <b>Manual control</b><br><br>
      Papers:
      <button onclick="ctl('paper','open')">Open papers</button>
      <button onclick="ctl('paper','seal')">Seal papers</button>
      &nbsp;&nbsp; Curveballs:
      <button onclick="ctl('curveball','open')">Release curveballs</button>
      <button onclick="ctl('curveball','seal')">Seal curveballs</button>
      <div class="mut" id="ctlMsg" style="margin-top:8px"></div>
    </div>
    <table><thead><tr><th>#</th><th>Student</th><th>Paper</th><th>Curveball</th>
      <th>Overall</th><th>Docs</th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th></tr></thead>
      <tbody id="rows"></tbody></table>
  </div>
</div>

<script>
let TOK=localStorage.getItem('exam_tok')||'', ROLE=localStorage.getItem('exam_role')||'';
let sched=null, skew=0;
const $=id=>document.getElementById(id);
function af(url,opts){opts=opts||{};opts.headers=Object.assign({'Authorization':'Bearer '+TOK,'Content-Type':'application/json'},opts.headers||{});return fetch(url,opts);}
function clr(f){return `hsl(${Math.round(f*125)},65%,42%)`;}
function fmt(ms){if(ms<=0)return'00:00';let s=Math.floor(ms/1000),h=Math.floor(s/3600);s-=h*3600;let m=Math.floor(s/60);s-=m*60;const p=n=>String(n).padStart(2,'0');return(h>0?p(h)+':':'')+p(m)+':'+p(s);}
const PILL={open:['live','OPEN'],sealed:['wait','sealed'],missing:['done','MISSING'],unknown:['wait','?']};
function pill(x){const c=PILL[x]||PILL.unknown;return `<span class="pill ${c[0]}">${c[1]}</span>`;}

async function doLogin(){
  $('loginErr').textContent='';
  const r=await fetch('/api/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({username:$('u').value.trim(),password:$('p').value})});
  const d=await r.json();
  if(!r.ok){$('loginErr').textContent=d.error||'login failed';return;}
  TOK=d.token;ROLE=d.role;localStorage.setItem('exam_tok',TOK);localStorage.setItem('exam_role',ROLE);
  start();
}
function logout(){localStorage.removeItem('exam_tok');localStorage.removeItem('exam_role');location.reload();}

function tick(){
  if(!sched)return;const now=Date.now()+skew;
  const e=$('exam'),es=$('examSt');
  if(now<sched.start){e.textContent=fmt(sched.start-now);es.innerHTML='<span class="pill wait">starts in</span>';}
  else if(now<sched.end){e.textContent=fmt(sched.end-now);es.innerHTML='<span class="pill live">ends in</span>';}
  else{e.textContent='00:00';es.innerHTML='<span class="pill done">ENDED</span>';}
  [['cbo','cboSt'],['cbs','cbsSt']].forEach(([a,b])=>{
    const el=$(a),st=$(b);
    if(now<sched.cbOpen){el.textContent=fmt(sched.cbOpen-now);st.innerHTML='<span class="pill wait">opens in</span>';}
    else if(now<sched.cbSeal){el.textContent=fmt(sched.cbSeal-now);st.innerHTML='<span class="pill live">RELEASED · closes in</span>';}
    else{el.textContent='00:00';st.innerHTML='<span class="pill done">CLOSED</span>';}
  });
}
function partsHtml(parts){return ['Docs','A','B','C','D','E'].map(p=>{const x=parts[p]||{p:0,t:0};const f=x.t?x.p/x.t:0;
  return `<span class="pc" style="background:${clr(f)}">${p} ${x.p}/${x.t}</span>`;}).join('');}

async function pollMe(){
  const r=await af('/api/exam/status'); if(r.status===403){logout();return;}
  const d=await r.json(); sched=d.schedule; skew=d.serverNow-Date.now();
  $('who').innerHTML=`signed in${d.role==='admin'?' as <b>admin</b>':''} · <a href="#" onclick="logout();return false" style="color:#8b949e">log out</a>`;
  if(d.me){const m=d.me;$('meCard').classList.remove('hide');
    $('meCard').innerHTML=`<b>${m.name}</b> <span class="mut">${m.user}</span> · paper ${pill(m.paper)} · curveball ${pill(m.cb)}`+
      `<div style="margin-top:10px"><div class="bar" style="max-width:320px"><i style="width:${m.pct}%;background:${clr(m.pct/100)}"></i><span>${m.pct}% complete</span></div></div>`+
      `<div class="parts">${partsHtml(m.parts)}</div>`+
      (m.found?'':`<div class="miss" style="margin-top:8px">No final-exam folder pushed yet.</div>`);
  } else {$('meCard').classList.remove('hide');$('meCard').innerHTML='<span class="mut">You are signed in but not in the exam roster.</span>';}
}
async function pollAdmin(){
  if(ROLE!=='admin')return; const r=await af('/api/admin/exam'); if(!r.ok)return;
  const d=await r.json(); const o=d.overall,e=d.env,c=o.curveball,pp=o.paper,N=o.totalStudents;
  $('adminWrap').classList.remove('hide');
  $('env').innerHTML=`<span>homes <b>${e.homeBase}</b> · srv <b>${e.srvBase}</b> · paper <b>${e.paperDir}</b></span>`+
    `<span>papers <b>${pp.open+pp.sealed}/${N}</b> · ${pp.sealed} sealed · <b style="color:#3fb37f">${pp.open} open</b></span>`+
    `<span>curveballs <b>${c.open+c.sealed}/${N}</b> · ${c.sealed} sealed · <b style="color:#3fb37f">${c.open} open</b></span>`+
    `<span>started <b>${o.foundCount}/${N}</b></span>`;
  $('rows').innerHTML=d.students.map((s,i)=>{
    const cells=['Docs','A','B','C','D','E'].map(p=>{const x=s.parts[p]||{p:0,t:0};const f=x.t?x.p/x.t:0;
      return `<td><div class="cell" style="background:${clr(f)}">${x.p}/${x.t}</div></td>`;}).join('');
    const nm=s.found?s.name:`<span class="miss">${s.name}</span>`;
    return `<tr><td>${i+1}</td><td>${nm}<br><span class="mut">${s.user}</span></td>`+
      `<td>${pill(s.paper)}</td><td>${pill(s.cb)}</td>`+
      `<td><div class="bar"><i style="width:${s.pct}%;background:${clr(s.pct/100)}"></i><span>${s.pct}%</span></div></td>`+cells+`</tr>`;
  }).join('');
}
async function ctl(target,action){
  if(!confirm(`${action} ${target} for ALL students?`))return;
  const r=await af('/api/admin/exam/control',{method:'POST',body:JSON.stringify({target,action})});
  const d=await r.json();
  $('ctlMsg').textContent=(r.ok&&d.ok)?`${action} ${target} — ${d.output}`:(d.output||d.error||'failed');
  pollAdmin();
}
function start(){$('login').classList.add('hide');$('app').classList.remove('hide');
  pollMe();pollAdmin();setInterval(()=>{pollMe();pollAdmin();},7000);setInterval(tick,250);}
if(TOK){start();}
</script>
</body></html>"""


# ── Final Exam Routes ──────────────────────────────────────────


@app.route("/api/exam/status")
@auth_required
def route_exam_status():
    username = request._session["username"]  # type: ignore
    sid = _USER_TO_SID.get(username)
    info = STUDENTS.get(sid) if sid else None
    me = None
    if info:
        u = info["user"]
        c = exam_completion(u)
        me = {
            "id": sid, "name": info["name"], "user": u,
            "found": c["found"], "pct": c["pct"], "parts": c["parts"],
            "paper": exam_paper_status(u),
            "cb": exam_curveball_status(u),
            "ssh": exam_ssh_state(u, _exam_blocked_shells(), _exam_active_users()),
        }
    return jsonify({
        "serverNow": int(datetime.now(timezone.utc).timestamp() * 1000),
        "schedule": exam_schedule(),
        "role": request._session["role"],  # type: ignore
        "me": me,
    })


@app.route("/api/admin/exam")
@admin_required
def route_admin_exam():
    return jsonify(exam_admin_state())


@app.route("/api/admin/exam/control", methods=["POST"])
@admin_required
def route_admin_exam_control():
    body = request.get_json(silent=True) or {}
    target = str(body.get("target", ""))
    action = str(body.get("action", ""))
    if target == "ssh":
        if action not in ("block", "unblock"):
            return jsonify({"error": "action=block|unblock for ssh"}), 400
        res = exam_set_ssh(action)
        return jsonify({"ok": res["ok"], "target": target, "action": action,
                        "output": res["output"]})
    if target not in ("paper", "curveball") or action not in ("open", "seal"):
        return jsonify({"error": "target=paper|curveball, action=open|seal"}), 400
    res = exam_set_access(target, action)
    return jsonify({"ok": res["ok"], "target": target, "action": action,
                    "output": res["output"]})


@app.route("/api/admin/exam/schedule", methods=["POST"])
@admin_required
def route_admin_exam_schedule():
    body = request.get_json(silent=True) or {}
    try:
        sched = exam_set_schedule(
            str(body.get("date", "")).strip(),
            str(body.get("start", "")).strip(),
            str(body.get("cbOpen", "")).strip(),
            str(body.get("cbSeal", "")).strip(),
            body.get("durationMin", 120),
        )
    except (ValueError, KeyError) as exc:
        return jsonify({"error": "invalid schedule: %s" % exc}), 400
    return jsonify({"ok": True, "schedule": sched})


@app.route("/exam")
def route_exam_page():
    return EXAM_PAGE, 200, {"Content-Type": "text/html; charset=utf-8"}


# ── Main ───────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="ITC-OS Presence Server")
    parser.add_argument(
        "--host", default="0.0.0.0", help="Bind address (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port", type=int, default=5000, help="Port (default: 5000)",
    )
    args = parser.parse_args()

    print(f"[Presence Server] http://{args.host}:{args.port}")
    print(f"  API endpoints:")
    print(f"    GET  /api/users              — logged-in Linux users")
    print(f"    GET  /api/web/users          — web visitors")
    print(f"    POST /api/web/login          — register web visitor")
    print(f"    POST /api/web/heartbeat      — keep web session alive")
    print(f"    POST /api/web/logout         — unregister web visitor")
    print(f"    POST /api/auth/login         — authenticate Linux user")
    print(f"    POST /api/auth/verify        — validate session token")
    print(f"    POST /api/auth/logout        — end session")
    print(f"    GET  /api/admin/stats        — user statistics (admin)")
    print(f"    GET  /api/admin/grades       — lab grading (admin)")
    print(f"    GET  /api/admin/leaderboard  — leaderboard (admin)")
    print(f"    GET  /api/admin/tree         — student file tree (admin)")
    print(f"    GET  /api/admin/activities   — activity grading (admin)")
    print(f"    GET  /api/admin/activity-tree — activity tree (admin)")
    print(f"    POST /api/admin/deadlines    — set deadlines (admin)")
    print(f"    GET  /api/deadlines          — read deadlines")
    print(f"    GET  /api/my/*               — student self-service")
    print(f"    GET  /api/who                — raw `who` output")
    print(f"    GET  /api/last               — recent login history")
    print(f"    GET  /api/health             — health check")
    print(f"  Press Ctrl+C to stop.\n")

    threading.Thread(target=_exam_autoblock_loop, daemon=True).start()
    app.run(host=args.host, port=args.port, threaded=True)


if __name__ == "__main__":
    main()
