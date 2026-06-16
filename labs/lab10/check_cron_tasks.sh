#!/bin/bash
# check_cron_tasks.sh - Verify the two GRADED Lab 10 cron tasks ran successfully.
#
# It inspects the output files written by the scheduled jobs and reports
# PASS/FAIL for each task plus an overall result.
#
# Usage:
#   ./check_cron_tasks.sh [BASE_DIR]
#
#   BASE_DIR is the student's automation folder.
#   Defaults to "$HOME/os-lab-automation" (run it inside a student account),
#   or pass another path to grade someone else, e.g.:
#       ./check_cron_tasks.sh /home/<StudentUser>/os-lab-automation
#
# Exit status: 0 if BOTH tasks passed, 1 otherwise.

set -u

base="${1:-$HOME/os-lab-automation}"
outdir="$base/cron_tasks"

pass=0
fail=0

check_one() {
    local label="$1" file="$2" marker="$3"
    echo "----------------------------------------"
    echo "Task   : $label"
    echo "Output : $file"
    if [ ! -f "$file" ]; then
        echo "Result : FAIL (output file not found - job never ran)"
        fail=$((fail + 1)); return
    fi
    if [ ! -s "$file" ]; then
        echo "Result : FAIL (output file is empty)"
        fail=$((fail + 1)); return
    fi
    if ! grep -q "$marker" "$file"; then
        echo "Result : FAIL (success marker '$marker' not found)"
        fail=$((fail + 1)); return
    fi
    local runs last
    runs=$(grep -c "$marker" "$file")
    last=$(grep "$marker" "$file" | tail -n 1)
    echo "Runs   : $runs"
    echo "Last   : $last"
    echo "Result : PASS"
    pass=$((pass + 1))
}

echo "========================================"
echo " Lab 10 - Graded Cron Task Checker"
echo " Base directory : $base"
echo " Checked at     : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

check_one "Lab session job (2:30 PM, lab day)" "$outdir/session_job.out"  "SESSION_JOB_OK"
check_one "Deadline job (before deadline)"     "$outdir/deadline_job.out" "DEADLINE_JOB_OK"

echo "========================================"
echo " Summary: $pass passed, $fail failed"
echo "========================================"

if [ "$fail" -eq 0 ] && [ "$pass" -eq 2 ]; then
    echo "OVERALL: PASS - both cron tasks ran successfully."
    exit 0
else
    echo "OVERALL: FAIL - see details above."
    exit 1
fi
