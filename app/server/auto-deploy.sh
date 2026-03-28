#!/bin/bash
# Auto-deploy: pulls latest code and restarts service if app/server changed
# Runs via cron every minute

REPO_DIR=/home/rathpisey/ITC-OS-2026
LOG=/home/rathpisey/deploy.log
LOCKFILE=/tmp/auto-deploy.lock

# Prevent concurrent runs
if [ -f "$LOCKFILE" ]; then
    exit 0
fi
trap "rm -f $LOCKFILE" EXIT
touch "$LOCKFILE"

cd "$REPO_DIR" || exit 1

# Fetch latest from remote
git fetch origin main --quiet 2>/dev/null

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

# Nothing new
if [ "$LOCAL" = "$REMOTE" ]; then
    exit 0
fi

echo "[$(date)] New commits detected ($LOCAL -> $REMOTE). Deploying..." >> "$LOG"

# Pull latest
git pull origin main --quiet >> "$LOG" 2>&1

# Check if server files changed
CHANGED=$(git diff "$LOCAL" "$REMOTE" --name-only -- app/server/)
if [ -z "$CHANGED" ]; then
    echo "[$(date)] No server changes, skipping restart." >> "$LOG"
    exit 0
fi

echo "[$(date)] Server files changed: $CHANGED" >> "$LOG"

# Restart the systemd service
sudo systemctl restart itc-os-presence >> "$LOG" 2>&1

echo "[$(date)] Deploy complete." >> "$LOG"
