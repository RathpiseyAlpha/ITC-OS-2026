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
import os
import re
import secrets
import subprocess
import time
import warnings
from datetime import datetime, timezone, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

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

# ── Student Roster ─────────────────────────────────────────────
# Maps student ID → { "name": display name, "user": Linux username }
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

# Reverse lookup: Linux username → student ID
_USER_TO_SID = {v["user"]: k for k, v in STUDENTS.items()}

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

def _parse_last_date(raw):
    """Try to extract a datetime from a `last -F` info string.

    The string looks like: 'pts/0 192.168.71.1 Fri Mar 27 17:25:33 2026'
    We scan for the date portion 'Fri Mar 27 17:25:33 2026'.
    """
    import re
    # Match pattern: Day Mon DD HH:MM:SS YYYY
    m = re.search(
        r'[A-Z][a-z]{2}\s+[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\d{4}', raw
    )
    if m:
        try:
            dt = datetime.strptime(m.group(), "%a %b %d %H:%M:%S %Y")
            # Attach server's local timezone
            local_tz = datetime.now().astimezone().tzinfo
            return dt.replace(tzinfo=local_tz)
        except ValueError:
            pass
    return None


def get_user_stats():
    """Parse `last` for per-user login statistics, include all non-system users."""
    stats = {}

    # Get all real (non-system) users from /etc/passwd (UID >= 1000, valid shell)
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
                if uid < 1000 or shell in ("/usr/sbin/nologin", "/bin/false", "/sbin/nologin"):
                    continue
                stats[username] = {
                    "username": username,
                    "loginCount": 0,
                    "lastLogin": "",
                    "totalSeconds": 0,
                }
    except OSError:
        pass

    # Enrich with login data from `last -F` (full timestamps)
    try:
        result = subprocess.run(
            ["last", "-n", "500", "-F", "-w"],
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
                # Extract date from full line — find pattern like "Mon Mar 27 17:06:09 2026"
                info = " ".join(parts[2:])
                for sep in (" - ", " still logged in"):
                    idx = info.find(sep)
                    if idx > 0:
                        info = info[:idx]
                # Try to parse the date portion (after terminal/host)
                raw = info.strip()
                parsed_dt = _parse_last_date(raw)
                if parsed_dt:
                    # Convert server local time to Phnom Penh and store as ISO
                    stats[username]["lastLogin"] = parsed_dt.astimezone(_PPH).isoformat()
                else:
                    stats[username]["lastLogin"] = raw
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


# ── Lab Grading Engine ─────────────────────────────────────────

# Required deliverables per lab.  Each entry:
#   "files"  – list of relative paths (from labN/ root)
#   "dirs"   – list of required directories
#   Points: each item is worth (total_points / total_items).
#   Case mismatch: -1 from the item's score (minimum 0).
#   Screenshots (images/*) are skipped for auto-grading.

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
        "dirs": [
            "task2_files",
            "images",
        ],
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
        "dirs": [
            "images",
            "redirect_lab",
        ],
    },
}


# ── Class Activity Specs ───────────────────────────────────────
# Dynamically parsed from lectures/class-activity/class-activity*.md
# so they stay in sync with the markdown submission folder structures.

_ACTIVITY_MD_DIR = Path(__file__).resolve().parent.parent.parent / "lectures" / "class-activity"
_SKIP_CONTENT_DIRS = frozenset(("screenshots", "images"))


def _parse_activity_spec(md_path, activity_name):
    """Parse a class-activity markdown file and build a grading spec.

    Locates the Submission Folder Structure tree code block, walks the
    tree to collect expected files and directories, and reads
    ``total_points`` from the Grading Criteria table.

    Returns ``{"total_points": int, "files": [...], "dirs": [...]}``
    or ``None`` on parse failure.
    """
    try:
        text = Path(md_path).read_text(encoding="utf-8")
    except OSError:
        return None

    # ── 1. Find the tree code block containing activityN/ ──────
    tree_block = None
    in_code = False
    buf = []
    for line in text.splitlines():
        if line.strip().startswith("```"):
            if in_code:
                block = "\n".join(buf)
                if f"{activity_name}/" in block and ("├" in block or "└" in block):
                    tree_block = block
                    break
                buf = []
            in_code = not in_code
            continue
        if in_code:
            buf.append(line)

    if not tree_block:
        return None

    # ── 2. Walk the tree and collect files / dirs ──────────────
    files, dirs = [], []
    root_found = False
    base_indent = None
    stack = []  # dir names forming path context

    for raw in tree_block.splitlines():
        m = re.search(r"([├└])── (.+)", raw)
        if not m:
            continue

        marker_pos = raw.index(m.group(1))
        entry_raw = m.group(2)

        # Locate root node (e.g. "activity1/")
        if not root_found:
            if entry_raw.strip().rstrip("/") == activity_name:
                root_found = True
            continue

        if base_indent is None:
            base_indent = marker_pos
        depth = (marker_pos - base_indent) // 4
        if depth < 0:
            break  # exited the root subtree

        # Clean display name: strip  # comments  and  ← annotations
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
            # Skip items marked optional or bonus in the original comment
            cm = re.search(r"\s{2,}#\s*(.+)$", entry_raw)
            if cm and re.search(r"optional|bonus", cm.group(1), re.I):
                continue

            # Skip individual files under screenshots/ or images/
            if stack and stack[0] in _SKIP_CONTENT_DIRS:
                continue

            rel = "/".join(stack + [name]) if stack else name
            files.append(rel)

    if not root_found or (not files and not dirs):
        return None

    # ── 3. Extract total_points from Grading Criteria table ────
    total = 100
    for line in text.splitlines():
        if "total" in line.lower() and "|" in line:
            pts = re.search(r"\*\*(\d+)(?:\s*\(\+\d+[^)]*\))?\*\*", line)
            if pts:
                total = int(pts.group(1))
                break

    return {"total_points": total, "files": files, "dirs": dirs}


def _build_activity_specs():
    """Build ACTIVITY_SPECS by parsing class-activity markdown files."""
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

# Override activity1 — the markdown was revised after students submitted.
# Students followed the eb3f441 version (commit "Class Activity 1") which had:
#   task1/ = file_creator + file_reader (combined)
#   task2/ = dir_list
#   task3_strace & task4_os_structure created by mkdir but no specific files
#     were listed in the tree, so only grade the explicitly listed deliverables.
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
    "dirs": [
        "screenshots",
        "task1",
        "task2",
        "task3_strace",
    ],
}

# Flexible keyword matching for task4 screenshot files.
# When exact match fails, match any file under screenshots/ whose basename
# (extension-stripped) contains ALL listed keywords.  Extension is ignored.
_SCREENSHOT_KEYWORDS = {
    "screenshots/task4_system_info.png": [["system", "info"], ["cpuinfo"], ["meminfo"], ["cpu"], ["mem"]],
    "screenshots/task4_process_info.png": [["process", "info"], ["process"], ["proc"]],
    "screenshots/task4_modules.png": [["mod"]],
    "screenshots/task4_os_layers_diagram.png": [["layer"]],
}


def _find_lab_root(username, lab_name):
    """Find a student's lab directory under their home.

    Expected: /home/<user>/os-se-*/os-lab-*/labN/
    Also supports repos cloned directly as os-lab-*/labN/ or labN/ in home.
    """
    home = Path(f"/home/{username}")
    if not home.is_dir():
        return None

    try:
        # Pattern 1: os-se-*/os-lab-*/labN/
        for d in home.iterdir():
            if d.is_dir() and d.name.lower().startswith("os-se-"):
                for sub in d.iterdir():
                    if sub.is_dir() and sub.name.lower().startswith("os-lab-"):
                        lab_dir = sub / lab_name
                        if lab_dir.is_dir():
                            return lab_dir

        # Pattern 2: os-lab-*/labN/
        for d in home.iterdir():
            if d.is_dir() and d.name.lower().startswith("os-lab-"):
                lab_dir = d / lab_name
                if lab_dir.is_dir():
                    return lab_dir

        # Pattern 3: direct labN/ in home
        lab_dir = home / lab_name
        if lab_dir.is_dir():
            return lab_dir
    except PermissionError:
        return None

    return None


def _find_activity_root(username, activity_name):
    """Find a student's class activity directory under their home.

    Expected: /home/<user>/os-se-*/os-class-activities-*/activityN/
    Also supports os-class-activities-*/activityN/ or direct activityN/ in home.
    """
    home = Path(f"/home/{username}")
    if not home.is_dir():
        return None

    try:
        # Pattern 1: os-se-*/os-class-activities-*/activityN/
        for d in home.iterdir():
            if d.is_dir() and d.name.lower().startswith("os-se-"):
                for sub in d.iterdir():
                    if sub.is_dir() and sub.name.lower().startswith("os-class-activit"):
                        act_dir = sub / activity_name
                        if act_dir.is_dir():
                            return act_dir

        # Pattern 2: os-class-activities-*/activityN/
        for d in home.iterdir():
            if d.is_dir() and d.name.lower().startswith("os-class-activit"):
                act_dir = d / activity_name
                if act_dir.is_dir():
                    return act_dir

        # Pattern 3: direct activityN/ in home
        act_dir = home / activity_name
        if act_dir.is_dir():
            return act_dir
    except PermissionError:
        return None

    return None


def _get_submission_date(root):
    """Get the submission date for a directory using git log.

    Uses `git log --diff-filter=A --format=%aI` to find when files were first
    added (committed).  This is NOT affected by `git pull` — git preserves
    the original author date of each commit.

    Returns ISO date string of the latest first-commit among files, or None.
    """
    if not root or not Path(root).is_dir():
        return None
    try:
        # Get the most recent author-date of the first commit that added any file
        result = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%aI", "--", "."],
            capture_output=True, text=True, timeout=10,
            cwd=str(root)
        )
        if result.returncode != 0 or not result.stdout.strip():
            return None
        # Lines are newest-first; the first line is the latest "add" commit
        dates = result.stdout.strip().splitlines()
        if dates:
            return dates[0]  # most recent add-commit's author date
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def _list_recursive(root):
    """Return a set of all relative paths (files and dirs) under root, lowercase."""
    result = {}  # lowercase_rel_path -> actual_rel_path
    root = Path(root)
    try:
        for item in root.rglob("*"):
            rel = str(item.relative_to(root)).replace("\\", "/")
            result[rel.lower()] = rel
    except PermissionError:
        pass
    return result


def grade_student_lab(username, lab_name):
    """Grade a single student's lab submission.

    Returns dict with: score, total, percentage, items (details), feedback.
    """
    spec = LAB_SPECS.get(lab_name)
    if not spec:
        return {"error": f"Unknown lab: {lab_name}"}

    lab_root = _find_lab_root(username, lab_name)
    if not lab_root:
        return {
            "username": username,
            "lab": lab_name,
            "score": 0,
            "total": spec["total_points"],
            "percentage": 0,
            "found": False,
            "labPath": None,
            "items": [],
            "feedback": [f"Lab directory not found. Expected ~/os-se-<ID>/os-lab-<ID>/{lab_name}/"],
        }

    all_items = spec.get("files", []) + spec.get("dirs", [])
    total_items = len(all_items)
    if total_items == 0:
        return {"error": "No items defined for this lab."}

    points_per_item = spec["total_points"] / total_items
    existing = _list_recursive(lab_root)  # lowercase -> actual

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
            # Verify type
            type_ok = full_path.is_dir() if is_dir else full_path.is_file()
            if not type_ok:
                items.append({
                    "expected": expected,
                    "status": "wrong_type",
                    "points": 0,
                    "maxPoints": round(points_per_item, 2),
                    "type": item_type,
                })
                feedback.append(f"'{expected}' exists but is {'a file' if is_dir else 'a directory'} (expected {item_type}).")
                continue

            # Check case convention
            if actual_path != expected:
                # Case mismatch — partial credit
                penalty = min(1.0, points_per_item)
                earned = max(0, points_per_item - penalty)
                score += earned
                items.append({
                    "expected": expected,
                    "actual": actual_path,
                    "status": "case_mismatch",
                    "points": round(earned, 2),
                    "maxPoints": round(points_per_item, 2),
                    "type": item_type,
                })
                feedback.append(f"'{actual_path}' should be '{expected}' (naming convention: all lowercase with underscores). -1 point.")
            else:
                score += points_per_item
                items.append({
                    "expected": expected,
                    "status": "ok",
                    "points": round(points_per_item, 2),
                    "maxPoints": round(points_per_item, 2),
                    "type": item_type,
                })
        else:
            items.append({
                "expected": expected,
                "status": "missing",
                "points": 0,
                "maxPoints": round(points_per_item, 2),
                "type": item_type,
            })
            feedback.append(f"Missing {item_type}: '{expected}'")

    score = round(min(score, spec["total_points"]), 2)
    sub_date = _get_submission_date(lab_root)
    return {
        "username": username,
        "lab": lab_name,
        "score": score,
        "total": spec["total_points"],
        "percentage": round(score / spec["total_points"] * 100, 1),
        "found": True,
        "labPath": str(lab_root),
        "submissionDate": sub_date,
        "items": items,
        "feedback": feedback,
    }


def grade_all_students(lab_name=None):
    """Grade all students from STUDENTS roster, optionally filtered by lab."""
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
                    "username": linux_user,
                    "id": sid,
                    "name": info["name"],
                    "lab": lab,
                    "score": 0,
                    "total": LAB_SPECS.get(lab, {}).get("total_points", 0),
                    "percentage": 0,
                    "found": False,
                    "labPath": None,
                    "items": [],
                    "feedback": ["Permission denied: cannot access home directory."],
                })
    return results


def grade_student_activity(username, activity_name):
    """Grade a single student's class activity submission.

    Reuses the same grading logic as labs: check files/dirs, case matching.
    """
    spec = ACTIVITY_SPECS.get(activity_name)
    if not spec:
        return {"error": f"Unknown activity: {activity_name}"}

    act_root = _find_activity_root(username, activity_name)
    if not act_root:
        return {
            "username": username,
            "activity": activity_name,
            "score": 0,
            "total": spec["total_points"],
            "percentage": 0,
            "found": False,
            "activityPath": None,
            "items": [],
            "feedback": [f"Activity directory not found. Expected ~/os-se-<ID>/os-class-activities-<ID>/{activity_name}/"],
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
            type_ok = full_path.is_dir() if is_dir else full_path.is_file()
            if not type_ok:
                items.append({
                    "expected": expected, "status": "wrong_type",
                    "points": 0, "maxPoints": round(points_per_item, 2), "type": item_type,
                })
                feedback.append(f"'{expected}' exists but is {'a file' if is_dir else 'a directory'} (expected {item_type}).")
                continue

            if actual_path != expected:
                penalty = min(1.0, points_per_item)
                earned = max(0, points_per_item - penalty)
                score += earned
                items.append({
                    "expected": expected, "actual": actual_path,
                    "status": "case_mismatch",
                    "points": round(earned, 2), "maxPoints": round(points_per_item, 2), "type": item_type,
                })
                feedback.append(f"'{actual_path}' should be '{expected}' (naming convention). -1 point.")
            else:
                score += points_per_item
                items.append({
                    "expected": expected, "status": "ok",
                    "points": round(points_per_item, 2), "maxPoints": round(points_per_item, 2), "type": item_type,
                })
        else:
            # Fallback: keyword-based matching for screenshot files
            matched_path = None
            if expected in _SCREENSHOT_KEYWORDS:
                keyword_groups = _SCREENSHOT_KEYWORDS[expected]
                for ex_lower, ex_actual in existing.items():
                    if not ex_lower.startswith("screenshots/"):
                        continue
                    base = ex_lower.rsplit("/", 1)[-1]
                    base = base.rsplit(".", 1)[0] if "." in base else base
                    if any(all(kw in base for kw in grp) for grp in keyword_groups):
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
                    "maxPoints": round(points_per_item, 2), "type": "file",
                })
            else:
                items.append({
                    "expected": expected, "status": "missing",
                    "points": 0, "maxPoints": round(points_per_item, 2), "type": item_type,
                })
                feedback.append(f"Missing {item_type}: '{expected}'")

    score = round(min(score, spec["total_points"]), 2)
    sub_date = _get_submission_date(act_root)
    return {
        "username": username,
        "activity": activity_name,
        "score": score,
        "total": spec["total_points"],
        "percentage": round(score / spec["total_points"] * 100, 1),
        "found": True,
        "activityPath": str(act_root),
        "submissionDate": sub_date,
        "items": items,
        "feedback": feedback,
    }


def grade_all_activities(activity_name=None):
    """Grade all students' class activities."""
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
                    "username": linux_user, "id": sid, "name": info["name"],
                    "activity": act, "score": 0,
                    "total": ACTIVITY_SPECS.get(act, {}).get("total_points", 0),
                    "percentage": 0, "found": False, "activityPath": None,
                    "items": [], "feedback": ["Permission denied: cannot access home directory."],
                })
    return results


def get_leaderboard():
    """Compute leaderboard: total score across all labs + activities per student."""
    all_grades = grade_all_students()
    all_acts = grade_all_activities()
    per_student = {}

    for g in all_grades:
        sid = g.get("id", g["username"])
        if sid not in per_student:
            per_student[sid] = {"id": sid, "username": g["username"], "name": g.get("name", sid), "labs": {}, "activities": {}, "totalScore": 0, "totalPossible": 0}
        per_student[sid]["labs"][g["lab"]] = {
            "score": g["score"],
            "total": g["total"],
            "percentage": g["percentage"],
            "found": g.get("found", False),
        }
        per_student[sid]["totalScore"] += g["score"]
        per_student[sid]["totalPossible"] += g["total"]

    for g in all_acts:
        sid = g.get("id", g["username"])
        if sid not in per_student:
            per_student[sid] = {"id": sid, "username": g["username"], "name": g.get("name", sid), "labs": {}, "activities": {}, "totalScore": 0, "totalPossible": 0}
        per_student[sid]["activities"][g["activity"]] = {
            "score": g["score"],
            "total": g["total"],
            "percentage": g["percentage"],
            "found": g.get("found", False),
        }
        per_student[sid]["totalScore"] += g["score"]
        per_student[sid]["totalPossible"] += g["total"]

    board = []
    for s in per_student.values():
        s["totalPercentage"] = round(s["totalScore"] / s["totalPossible"] * 100, 1) if s["totalPossible"] > 0 else 0
        board.append(s)

    board.sort(key=lambda x: x["totalScore"], reverse=True)
    # Add rank
    for i, entry in enumerate(board):
        entry["rank"] = i + 1
    return board


def get_student_tree(username, lab_name):
    """Get the file tree for a student's lab directory."""
    lab_root = _find_lab_root(username, lab_name)
    if not lab_root:
        return None

    def build_tree(path, depth=0, max_depth=5):
        if depth > max_depth:
            return []
        items = []
        try:
            entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
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
        "username": username,
        "lab": lab_name,
        "path": str(lab_root),
        "tree": build_tree(lab_root),
    }


def get_student_activity_tree(username, activity_name):
    """Get the file tree for a student's class activity directory."""
    act_root = _find_activity_root(username, activity_name)
    if not act_root:
        return None

    def build_tree(path, depth=0, max_depth=5):
        if depth > max_depth:
            return []
        items = []
        try:
            entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except PermissionError:
            return items
        for entry in entries:
            if entry.name.startswith("."):
                continue
            node = {"name": entry.name, "type": "dir" if entry.is_dir() else "file"}
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
        "username": username,
        "activity": activity_name,
        "path": str(act_root),
        "tree": build_tree(act_root),
    }


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

        elif path == "/api/admin/deadlines":
            token = self._get_token()
            session = validate_token(token)
            if not session or session["role"] != "admin":
                self._json_response({"error": "Unauthorized"}, 403)
                return
            # body: { "lab1": { "due": "2026-03-22T23:59:00", "penalty": 5 }, ... }
            deadlines = body if isinstance(body, dict) else {}
            # Validate entries
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
            self._json_response({"ok": True, "deadlines": clean})

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
        elif path == "/api/admin/grades":
            token = self._get_token()
            session = validate_token(token)
            if not session or session["role"] != "admin":
                self._json_response({"error": "Unauthorized"}, 403)
                return
            qs = parse_qs(parsed.query)
            lab = qs.get("lab", [None])[0]
            user = qs.get("user", [None])[0]
            if user and lab:
                result = grade_student_lab(user, lab)
                self._json_response(result)
            else:
                results = grade_all_students(lab)
                self._json_response({"grades": results, "labs": list(LAB_SPECS.keys())})
        elif path == "/api/admin/leaderboard":
            token = self._get_token()
            session = validate_token(token)
            if not session or session["role"] != "admin":
                self._json_response({"error": "Unauthorized"}, 403)
                return
            self._json_response({"leaderboard": get_leaderboard(), "labs": list(LAB_SPECS.keys()), "activities": list(ACTIVITY_SPECS.keys())})
        elif path == "/api/admin/tree":
            token = self._get_token()
            session = validate_token(token)
            if not session or session["role"] != "admin":
                self._json_response({"error": "Unauthorized"}, 403)
                return
            qs = parse_qs(parsed.query)
            user = qs.get("user", [None])[0]
            lab = qs.get("lab", [None])[0]
            if not user or not lab:
                self._json_response({"error": "user and lab params required"}, 400)
                return
            tree = get_student_tree(user, lab)
            if tree is None:
                self._json_response({"error": "Lab directory not found"}, 404)
                return
            self._json_response(tree)
        # ── Deadlines (any authenticated user can read) ──
        elif path == "/api/deadlines":
            token = self._get_token()
            session = validate_token(token)
            if not session:
                self._json_response({"error": "Unauthorized"}, 403)
                return
            self._json_response({"deadlines": _load_deadlines()})
        # ── Student-facing endpoints (any authenticated user) ──
        elif path == "/api/my/grades":
            token = self._get_token()
            session = validate_token(token)
            if not session:
                self._json_response({"error": "Unauthorized"}, 403)
                return
            username = session["username"]
            sid = _USER_TO_SID.get(username)
            info = STUDENTS.get(sid) if sid else None
            if not info:
                self._json_response({"error": "Student not found in roster"}, 404)
                return
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
                        "lab": lab, "score": 0,
                        "total": LAB_SPECS[lab]["total_points"],
                        "percentage": 0, "found": False, "labPath": None,
                        "items": [], "feedback": ["Cannot access lab directory."],
                    })
            self._json_response({"grades": grades, "labs": labs})
        elif path == "/api/my/tree":
            token = self._get_token()
            session = validate_token(token)
            if not session:
                self._json_response({"error": "Unauthorized"}, 403)
                return
            username = session["username"]
            sid = _USER_TO_SID.get(username)
            info = STUDENTS.get(sid) if sid else None
            if not info:
                self._json_response({"error": "Student not found in roster"}, 404)
                return
            qs = parse_qs(parsed.query)
            lab = qs.get("lab", [None])[0]
            if not lab:
                self._json_response({"error": "lab param required"}, 400)
                return
            tree = get_student_tree(info["user"], lab)
            if tree is None:
                self._json_response({"error": "Lab directory not found"}, 404)
                return
            self._json_response(tree)
        elif path == "/api/my/leaderboard":
            token = self._get_token()
            session = validate_token(token)
            if not session:
                self._json_response({"error": "Unauthorized"}, 403)
                return
            self._json_response({"leaderboard": get_leaderboard(), "labs": list(LAB_SPECS.keys()), "activities": list(ACTIVITY_SPECS.keys())})
        elif path == "/api/my/activities":
            token = self._get_token()
            session = validate_token(token)
            if not session:
                self._json_response({"error": "Unauthorized"}, 403)
                return
            username = session["username"]
            sid = _USER_TO_SID.get(username)
            info = STUDENTS.get(sid) if sid else None
            if not info:
                self._json_response({"error": "Student not found in roster"}, 404)
                return
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
                        "username": linux_user, "id": sid or "", "name": info["name"],
                        "activity": act, "score": 0,
                        "total": ACTIVITY_SPECS[act]["total_points"],
                        "percentage": 0, "found": False, "activityPath": None,
                        "items": [], "feedback": ["Cannot access activity directory."],
                    })
            self._json_response({"grades": grades, "activities": acts})
        elif path == "/api/my/activity-tree":
            token = self._get_token()
            session = validate_token(token)
            if not session:
                self._json_response({"error": "Unauthorized"}, 403)
                return
            username = session["username"]
            sid = _USER_TO_SID.get(username)
            info = STUDENTS.get(sid) if sid else None
            if not info:
                self._json_response({"error": "Student not found in roster"}, 404)
                return
            qs = parse_qs(parsed.query)
            activity = qs.get("activity", [None])[0]
            if not activity:
                self._json_response({"error": "activity param required"}, 400)
                return
            tree = get_student_activity_tree(info["user"], activity)
            if tree is None:
                self._json_response({"error": "Activity directory not found"}, 404)
                return
            self._json_response(tree)
        elif path == "/api/admin/activities":
            token = self._get_token()
            session = validate_token(token)
            if not session or session["role"] != "admin":
                self._json_response({"error": "Unauthorized"}, 403)
                return
            qs = parse_qs(parsed.query)
            activity = qs.get("activity", [None])[0]
            user = qs.get("user", [None])[0]
            if user and activity:
                result = grade_student_activity(user, activity)
                self._json_response(result)
            else:
                grades = grade_all_activities(activity)
                self._json_response({"grades": grades, "activities": list(ACTIVITY_SPECS.keys())})
        elif path == "/api/admin/activity-tree":
            token = self._get_token()
            session = validate_token(token)
            if not session or session["role"] != "admin":
                self._json_response({"error": "Unauthorized"}, 403)
                return
            qs = parse_qs(parsed.query)
            user = qs.get("user", [None])[0]
            activity = qs.get("activity", [None])[0]
            if not user or not activity:
                self._json_response({"error": "user and activity params required"}, 400)
                return
            tree = get_student_activity_tree(user, activity)
            if tree is None:
                self._json_response({"error": "Activity directory not found"}, 404)
                return
            self._json_response(tree)
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
    print(f"    GET  /api/admin/grades  — lab grading (admin only)")
    print(f"    GET  /api/admin/leaderboard — student leaderboard (admin)")
    print(f"    GET  /api/admin/tree    — student file tree (admin only)")
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
