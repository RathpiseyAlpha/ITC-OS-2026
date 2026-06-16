# OS Lab 10 - Backups, Archiving, Scheduling & cron Automation (Hands-on)

| | |
|---|---|
| **Course** | Operating Systems |
| **Lab Title** | The QuantumTech Automation Pipeline |
| **Chapter** | Process Scheduling, Shell Automation, Backups |
| **Duration** | 3 Hours |
| **Lab Type** | Individual |

---

**Source reference:** This canonical lab instruction continues the QuantumTech series from Labs 7-9. It runs entirely with a normal user account using `tar`, `gzip`, and the per-user `crontab`, so no `sudo`, no system cron files, and no special permissions are required.

---

> **IMPORTANT - READ EVERYTHING FIRST**
>
> This lab uses files and folders in two places:
>
> 1. Your **submission folder** inside `~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10`
> 2. Your **working folders** outside the repo: `~/bin` and `~/os-lab-automation`
>
> The working folders are required because cron must execute your scripts by absolute path, and the backup jobs must read and write real files on disk. Before submitting, copy your scripts and evidence back into your `lab10` folder.
>
> **A note on timing:** cron runs jobs on the clock, and its smallest unit is **one minute**. Several levels ask you to schedule a job for `*/1` or `*/2` minutes, then **wait** for it to fire. Be patient and watch the log files. Do not assume a job failed just because nothing happened in the first few seconds.
>
> **⏰ TIME-SENSITIVE - LEVEL 4:** Level 4 contains two **graded, date-specific** cron jobs. The first must fire **at 2:30 PM during this lab session**, so you must install it **before 2:30 PM**. Level 4 comes right after the cron basics for this reason - set up **both** timed jobs as soon as you reach it, then continue with the later levels and return at 2:30 PM to verify.
>
> **Document structure:**
> 1. **Lab Objectives** - What you will learn
> 2. **Mission Briefing** - Automation scenario
> 3. **Task Overview** - Summary of all levels
> 4. **Lab Setup** - Repository, working folders, and naming rules
> 5. **Quick Reference** - Archiving, compression, cron, Bash idioms
> 6. **Levels 0-8 (Required)** - Warm-up, archiving, file backup, cron, timed graded jobs, scheduling, maintenance, design-your-own job, teardown
> 7. **Deliverables & Submission** - Complete tree structure, README template, git push
> 8. **Screenshot Checklist** - Every screenshot you need, in one place

---

## Lab Objectives

After completing this lab, students will be able to:

1. Write robust, idempotent Bash automation scripts using functions, logging, and exit codes.
2. Archive multiple files and folders into a single file with `tar`, and compress them with `gzip`.
3. Distinguish **archiving** (combining files) from **compression** (shrinking bytes) and measure the size difference.
4. Build a file/folder backup script that produces timestamped archives and enforces a retention policy.
5. Read and write the per-user `crontab`, interpret the five time fields, and use special strings such as `@daily`.
6. Diagnose the classic "works in my shell but not in cron" failure and redirect job output to log files.
7. Schedule one-time cron jobs that fire on a specific future date and time, and verify their output with a checker script.
8. Independently design a Bash automation script and write its crontab schedule from scratch, without a template.
9. Automate routine maintenance and cleanly inventory and remove scheduled jobs during teardown without disturbing jobs that must still run.

> **Scenario:** You are an **SRE / DevOps engineer** at **QuantumTech**. The team keeps a small source project on a shared server, and routine chores - backups, scheduled jobs, log cleanup, and health checks - were being done by hand and were sometimes missed. Management mandates an automated pipeline. Your job is to package each chore as a reliable Bash script, schedule it with `cron`, prove the scheduled jobs run unattended, then cleanly decommission the jobs at the end of the drill.

---

## Task Overview

| Level | Title | Key Commands / Concepts | Screenshots Required |
|:---:|-------|-------------------------|:-------------------:|
| **0** | Automation Warm-Up | functions, `date`, logging, `$?`, `set -euo pipefail` | yes |
| **1** | Archiving & Compression | `tar -cf`, `tar -czf`, `gzip`, size comparison, extract | yes |
| **2** | File & Folder Backup Script | timestamps, retention pruning, `ls -t` | yes |
| **3** | Cron Fundamentals | `crontab -l/-e/-r`, five fields, `*/n`, `@daily` | yes |
| **4** | Timed Graded Cron Tasks | dated cron fields, one-time future jobs, checker script | yes |
| **5** | Scheduling the Backup | cron environment, absolute paths, `>> log 2>&1` | yes |
| **6** | Maintenance Automation | log rotation, `df`, `uptime`, threshold alert | yes |
| **7** | Design Your Own Scheduled Job | student-authored script + self-written crontab line | yes |
| **8** | Teardown and Reset | selective `crontab -e`, preserve graded jobs | yes |

---

## Lab Setup

Navigate into your existing lab submission repository and create the `lab10` directory:

```bash
cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>
mkdir -p lab10
cd lab10
mkdir -p images scripts
```

Create the working folders used by the running scripts:

```bash
mkdir -p ~/bin
mkdir -p ~/os-lab-automation
mkdir -p ~/os-lab-automation/logs
mkdir -p ~/os-lab-automation/backups
mkdir -p ~/os-lab-automation/cron_tasks
```

### Required Working Locations

| Path | Holds |
|------|-------|
| `~/bin/` | Your executable scripts |
| `~/os-lab-automation/project/` | Sample files and folders to back up |
| `~/os-lab-automation/backups/` | File/folder archives |
| `~/os-lab-automation/logs/` | Logs written by every script and cron job |
| `~/os-lab-automation/cron_tasks/` | Output of the two graded timed cron jobs (Level 4) |
| `~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/` | Submission files and screenshots |

### Make `~/bin` Runnable (if it is not already)

```bash
export PATH="$HOME/bin:$PATH"
```

> **Note:** This `export` only affects your current shell. As you will learn in Level 5, **cron does not read it**, which is exactly why cron jobs must call scripts by their **absolute path**.

### Rules for This Lab

1. Use the shared Linux server with your assigned student account.
2. Do not use `sudo`. Use only your **per-user** crontab (`crontab -e`).
3. Do not edit `/etc/crontab` or files under `/etc/cron.*`.
4. Script names must be lowercase, snake_case, and have no file extension.
5. Every scheduled job must write to a log file so its activity is visible.
6. Use short intervals (`*/1` or `*/2` minutes) only for testing; remove them in Level 8.
7. Copy your final scripts from `~/bin` into `lab10/scripts` before submitting.

---

## Quick Reference

### Archiving and Compression

| Command | Purpose |
|---------|---------|
| `tar -cf out.tar dir` | **Archive** a folder into one uncompressed `.tar` file |
| `tar -czf out.tar.gz dir` | Archive **and** gzip-compress into `.tar.gz` |
| `tar -tzf out.tar.gz` | List the contents of a compressed archive |
| `tar -xzf out.tar.gz -C dest` | Extract a compressed archive into `dest` |
| `gzip file` / `gunzip file.gz` | Compress / decompress a single file |
| `gzip -k file` | Compress but **keep** the original |
| `gunzip -c file.gz > out` | Decompress to stdout without deleting the `.gz` |
| `du -h file` / `ls -lh` | Show human-readable file sizes |

> **Archiving vs compression:** `tar` *combines* many files into one (it does not shrink them). `gzip` *shrinks* bytes. `tar -czf` does both in one step.

### crontab Commands and Time Fields

| Command | Purpose |
|---------|---------|
| `crontab -l` | List your current cron jobs |
| `crontab -e` | Edit your cron jobs |
| `crontab -r` | Remove **all** your cron jobs (be careful) |

```text
 ┌───────────── minute        (0 - 59)
 │ ┌─────────── hour          (0 - 23)
 │ │ ┌───────── day of month  (1 - 31)
 │ │ │ ┌─────── month         (1 - 12)
 │ │ │ │ ┌───── day of week    (0 - 6, Sunday = 0)
 │ │ │ │ │
 * * * * *  command-to-run
```

| Example | Meaning | | Special | Equivalent |
|---------|---------|---|---------|------------|
| `*/2 * * * *` | Every 2 minutes | | `@hourly` | `0 * * * *` |
| `30 2 * * *` | Daily at 02:30 | | `@daily` | `0 0 * * *` |
| `0 9 * * 1` | Mondays at 09:00 | | `@weekly` | `0 0 * * 0` |

> **One-time dated jobs:** filling in the day-of-month and month fields pins a job to a date. `30 14 16 6 *` means **14:30 on 16 June** (any year), so it effectively fires once for a given month. This is exactly how the two graded jobs in Level 4 work.

### Bash Automation Idioms

| Idiom | Purpose |
|-------|---------|
| `#!/bin/bash` | Shebang: run the script with Bash |
| `set -euo pipefail` | Exit on error, undefined var, or failed pipe |
| `ts=$(date +%Y%m%d_%H%M%S)` | Timestamp safe for file names |
| `command >> file.log 2>&1` | Append both stdout and stderr to a log |
| `ls -1t dir \| tail -n +4` | List all but the 3 newest files |

---

## Level 0 - Automation Warm-Up

**Scenario:** *"Before automating anything, build one small, well-behaved script. A good automation script announces what it is doing, logs it, and returns a meaningful exit status."*

1. Create `automation_demo`:

```bash
nano ~/bin/automation_demo
```

2. Use this script:

```bash
#!/bin/bash
set -euo pipefail

base="$HOME/os-lab-automation"
logfile="$base/logs/automation_demo.log"

log() {
    local message="$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $message" | tee -a "$logfile"
}

main() {
    log "automation_demo started by user $(whoami)"
    log "working directory is $(pwd)"
    log "home directory is $HOME"
    log "automation_demo finished successfully"
}

main
exit 0
```

3. Make it executable and run it twice:

```bash
chmod +x ~/bin/automation_demo
automation_demo
automation_demo
echo "exit status: $?"
```

4. Confirm the log grew on the second run (append-only, idempotent logging):

```bash
cat ~/os-lab-automation/logs/automation_demo.log
```

5. Save evidence:

```bash
{
    echo "=== script permissions ==="
    ls -l ~/bin/automation_demo
    echo "=== log contents ==="
    cat ~/os-lab-automation/logs/automation_demo.log
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task0_warmup.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task0_warmup.txt
```

> **Required Screenshot 1:** Save as `images/level0_warmup.png` and embed it in `README.md`.

---

## Level 1 - Archiving & Compression

**Scenario:** *"A backup is just an archive you can trust. First learn the two skills every backup depends on: bundling many files and folders into one archive, and compressing that archive to save space."*

1. Create a sample project with several files and folders to archive:

```bash
mkdir -p ~/os-lab-automation/project/src ~/os-lab-automation/project/docs
echo "print('Quantum Widget v1')" > ~/os-lab-automation/project/src/widget.py
echo "# QuantumTech Project" > ~/os-lab-automation/project/README.md
seq 1 500 > ~/os-lab-automation/project/docs/changelog.txt
seq 1 500 > ~/os-lab-automation/project/docs/notes.txt
```

2. Move into the working folder:

```bash
cd ~/os-lab-automation
```

3. Create an **uncompressed archive** (bundle only), then a **compressed archive** (bundle + shrink):

```bash
tar -cf project_plain.tar project
tar -czf project_compressed.tar.gz project
```

4. Compare the sizes. The `.tar.gz` should be much smaller because the text files compress well:

```bash
ls -lh project_plain.tar project_compressed.tar.gz
```

5. List what is inside the compressed archive **without extracting it**:

```bash
tar -tzf project_compressed.tar.gz
```

6. Prove you can **restore** by extracting into a separate folder and comparing:

```bash
mkdir -p ~/os-lab-automation/restore_demo
tar -xzf project_compressed.tar.gz -C ~/os-lab-automation/restore_demo
diff -r ~/os-lab-automation/project ~/os-lab-automation/restore_demo/project && echo "RESTORE OK: archive matches original"
```

7. Save evidence:

```bash
{
    echo "=== archive sizes (plain vs compressed) ==="
    ls -lh ~/os-lab-automation/project_plain.tar ~/os-lab-automation/project_compressed.tar.gz
    echo "=== contents of compressed archive ==="
    tar -tzf ~/os-lab-automation/project_compressed.tar.gz
    echo "=== restore verification ==="
    diff -r ~/os-lab-automation/project ~/os-lab-automation/restore_demo/project && echo "RESTORE OK: archive matches original"
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task1_archive.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task1_archive.txt
```

> **Required Screenshot 2:** Save as `images/level1_archive.png` and embed it in `README.md`. Make sure the size difference between the `.tar` and the `.tar.gz` is visible.

---

## Level 2 - File & Folder Backup Script

**Scenario:** *"Now wrap the archiving skill in a repeatable script. Every run snapshots the project into a timestamped, compressed archive, and keeps only the three most recent so the disk does not fill up."*

1. Create `backup_project`:

```bash
nano ~/bin/backup_project
```

2. Use this script:

```bash
#!/bin/bash
set -euo pipefail

base="$HOME/os-lab-automation"
source_dir="$base/project"
backup_dir="$base/backups"
logfile="$base/logs/backup_project.log"
keep=3

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') | $1" >> "$logfile"; }

mkdir -p "$backup_dir"

ts=$(date +%Y%m%d_%H%M%S)
archive="$backup_dir/project_$ts.tar.gz"

log "starting backup of $source_dir"
tar -czf "$archive" -C "$base" project
log "created archive $archive"

# Retention: keep only the newest $keep archives, delete the rest.
old=$(ls -1t "$backup_dir"/project_*.tar.gz 2>/dev/null | tail -n +$((keep + 1)) || true)
if [ -n "$old" ]; then
    echo "$old" | while read -r f; do
        rm -f "$f"
        log "pruned old archive $f"
    done
else
    log "no old archives to prune"
fi

log "backup finished successfully"
```

3. Make it executable, then run it **four times** so retention has something to prune:

```bash
chmod +x ~/bin/backup_project
backup_project; sleep 1
backup_project; sleep 1
backup_project; sleep 1
backup_project
```

4. Confirm only three archives remain:

```bash
ls -1t ~/os-lab-automation/backups/project_*.tar.gz
```

5. Save evidence:

```bash
{
    echo "=== backup script permissions ==="
    ls -l ~/bin/backup_project
    echo "=== archives kept (should be 3) ==="
    ls -1t ~/os-lab-automation/backups/project_*.tar.gz
    echo "=== backup log ==="
    cat ~/os-lab-automation/logs/backup_project.log
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task2_backup.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task2_backup.txt
```

> **Required Screenshot 3:** Save as `images/level2_backup.png` and embed it in `README.md`.

---

## Level 3 - Cron Fundamentals

**Scenario:** *"Running backups by hand defeats the purpose. Learn the per-user crontab by scheduling one trivial 'heartbeat' job, watching it fire, then reading it back."*

1. Set your editor and open your crontab:

```bash
export EDITOR=nano
crontab -e
```

2. Add this single line, then save and exit. It writes one timestamped line every minute:

```cron
# Lab10 heartbeat - runs every minute
* * * * * date '+\%Y-\%m-\%d \%H:\%M:\%S heartbeat' >> $HOME/os-lab-automation/logs/heartbeat.log 2>&1
```

> **Important:** Inside a crontab the `%` character has a special meaning and **must be escaped as `\%`**. This is one of the most common cron mistakes.

3. Confirm the job is installed, then **wait up to 2 minutes** and watch it fire:

```bash
crontab -l
cat ~/os-lab-automation/logs/heartbeat.log
```

You should see one new line per minute. (Use `tail -f` to watch live; `Ctrl+C` to stop.)

4. Save evidence:

```bash
{
    echo "=== installed cron jobs ==="
    crontab -l
    echo "=== heartbeat log (one line per minute) ==="
    cat ~/os-lab-automation/logs/heartbeat.log
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task3_cron_basics.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task3_cron_basics.txt
```

> **Required Screenshot 4:** Save as `images/level3_cron_basics.png` and embed it in `README.md`.

---

## Level 4 - Timed Graded Cron Tasks

**Scenario:** *"Real maintenance windows happen on the calendar, not 'every two minutes.' You must prove you can schedule a job to run at one exact moment in the future. Two jobs are graded: one fires live during this lab session, the second fires before the submission deadline."*

> **⏰ DO THIS NOW.** You have just learned the crontab, so set these two graded jobs up immediately. The session job must fire **at 2:30 PM today, during the lab**. If you install it after 2:30 PM it will not fire and that task is lost. Install both jobs now, then continue with Level 5 and beyond, and return here at 2:30 PM to verify.

| Graded task | Must run at | Cron schedule |
|-------------|-------------|---------------|
| **Session job** | **2:30 PM on 2026-06-16** (lab session, 1-3 PM) | `30 14 16 6 *` |
| **Deadline job** | **2:30 PM on 2026-06-22** (before the 2026-06-23 deadline) | `30 14 22 6 *` |

> **Read the schedule:** `30 14 16 6 *` = minute 30, hour 14, day 16, month 6, any weekday → 14:30 on 16 June. Change the day field to `22` for the deadline job.

### Step 1 - Create the two job scripts

Create `lab_session_job`:

```bash
nano ~/bin/lab_session_job
```

```bash
#!/bin/bash
set -euo pipefail

base="$HOME/os-lab-automation"
outdir="$base/cron_tasks"
mkdir -p "$outdir"

echo "SESSION_JOB_OK | $(date '+%Y-%m-%d %H:%M:%S') | user=$(whoami) | host=$(hostname)" >> "$outdir/session_job.out"
```

Create `deadline_job`:

```bash
nano ~/bin/deadline_job
```

```bash
#!/bin/bash
set -euo pipefail

base="$HOME/os-lab-automation"
outdir="$base/cron_tasks"
mkdir -p "$outdir"

echo "DEADLINE_JOB_OK | $(date '+%Y-%m-%d %H:%M:%S') | user=$(whoami) | host=$(hostname)" >> "$outdir/deadline_job.out"
```

Make both executable and test them by hand once (this proves the script works before you trust cron):

```bash
chmod +x ~/bin/lab_session_job ~/bin/deadline_job
lab_session_job
deadline_job
cat ~/os-lab-automation/cron_tasks/session_job.out
cat ~/os-lab-automation/cron_tasks/deadline_job.out
```

### Step 2 - Schedule both graded jobs

```bash
whoami        # note your username
crontab -e
```

Add these two lines (replace `<YourUsername>` with the output of `whoami`). Note there is **no** `TEST interval` comment - that keyword is how teardown tells graded jobs apart from practice jobs:

```cron
# Lab10 GRADED session job - fires once at 2:30 PM on 2026-06-16 (lab session)
30 14 16 6 * /home/<YourUsername>/bin/lab_session_job >> /home/<YourUsername>/os-lab-automation/logs/cron_session_job.log 2>&1

# Lab10 GRADED deadline job - fires once at 2:30 PM on 2026-06-22 (before deadline)
30 14 22 6 * /home/<YourUsername>/bin/deadline_job >> /home/<YourUsername>/os-lab-automation/logs/cron_deadline_job.log 2>&1
```

Confirm both are installed:

```bash
crontab -l
```

### Step 3 - Create the checker script

Create `check_cron_tasks` in `~/bin`. It inspects `~/os-lab-automation/cron_tasks/` and prints `PASS`/`FAIL` for each graded task, with an overall result:

```bash
nano ~/bin/check_cron_tasks
```

```bash
#!/bin/bash
# Verify the two graded Lab 10 cron tasks ran successfully.
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
echo " Checked at : $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

check_one "Lab session job (2:30 PM, lab day)" "$outdir/session_job.out"  "SESSION_JOB_OK"
check_one "Deadline job (before deadline)"     "$outdir/deadline_job.out" "DEADLINE_JOB_OK"

echo "========================================"
if [ "$fail" -eq 0 ] && [ "$pass" -eq 2 ]; then
    echo "OVERALL: PASS - both cron tasks ran successfully."
    exit 0
else
    echo "OVERALL: FAIL ($pass passed, $fail failed) - see details above."
    exit 1
fi
```

Make it executable:

```bash
chmod +x ~/bin/check_cron_tasks
```

### Step 4 - Verify the session job (during the lab)

Continue with the rest of the lab. At or shortly after **2:30 PM**, come back and run the checker:

```bash
check_cron_tasks
```

The **session job** should report `PASS`. The **deadline job** will still report `FAIL` - that is expected, because it does not fire until 2026-06-22. You will run the checker again then.

### Step 5 - Save evidence

```bash
{
    echo "=== graded job scripts ==="
    ls -l ~/bin/lab_session_job ~/bin/deadline_job
    echo "=== graded cron jobs installed ==="
    crontab -l | grep GRADED
    echo "=== session job output (filled at 2:30 PM) ==="
    cat ~/os-lab-automation/cron_tasks/session_job.out 2>/dev/null || echo "(not fired yet)"
    echo "=== checker result ==="
    check_cron_tasks || true
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task4_timed_tasks.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task4_timed_tasks.txt
```

> **Required Screenshot 5:** Save as `images/level4_session_job.png` and embed it in `README.md`. Take it after 2:30 PM today; it must show the session job's output line and the checker reporting the session task as `PASS`.
>
> **Required Screenshot 6:** Save as `images/level4_deadline_job.png` and embed it in `README.md`. Take this **after 2026-06-22 14:30 but before the deadline**; it must show `check_cron_tasks` reporting **both** tasks as `PASS`.

---

## Level 5 - Scheduling the Backup (and the Environment Trap)

**Scenario:** *"You schedule the backup script with cron, but a naive attempt silently does nothing. This is the most famous cron bug: cron runs with a stripped-down environment, so your `PATH` and `~` shortcut are not available."*

### Why the naive attempt fails

If you scheduled `backup_project` by bare name, cron would not find it: cron's `PATH` is minimal (often only `/usr/bin:/bin`) and does **not** include `~/bin`. Always use the **absolute path** and always **redirect output to a log**.

### Schedule the backup correctly

1. Find your username, then edit the crontab:

```bash
whoami
crontab -e
```

2. Add this line **below** the heartbeat line (replace `<YourUsername>` with the output of `whoami`). It runs the backup every 2 minutes (for testing) and captures all output:

```cron
# Lab10 file backup - every 2 minutes (TEST interval)
*/2 * * * * /home/<YourUsername>/bin/backup_project >> /home/<YourUsername>/os-lab-automation/logs/cron_backup.log 2>&1
```

> Cron does **not** reliably expand `~`, so spell out the full path to both the script and the log.

3. Save and exit, confirm, then **wait up to 4 minutes** and check that cron produced new backups unattended:

```bash
crontab -l
ls -1t ~/os-lab-automation/backups/project_*.tar.gz
cat ~/os-lab-automation/logs/backup_project.log
cat ~/os-lab-automation/logs/cron_backup.log
```

An empty `cron_backup.log` with new archives and a growing `backup_project.log` means the job ran cleanly.

4. Save evidence:

```bash
{
    echo "=== my username ==="
    whoami
    echo "=== installed cron jobs ==="
    crontab -l
    echo "=== archives produced by cron ==="
    ls -1t ~/os-lab-automation/backups/project_*.tar.gz
    echo "=== backup log (note the new timestamps from cron) ==="
    cat ~/os-lab-automation/logs/backup_project.log
    echo "=== captured cron output (empty = clean) ==="
    cat ~/os-lab-automation/logs/cron_backup.log 2>/dev/null || echo "(empty)"
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task5_schedule.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task5_schedule.txt
```

> **Required Screenshot 7:** Save as `images/level5_schedule.png` and embed it in `README.md`.

---

## Level 6 - Maintenance Automation: Log Rotation & Health Check

**Scenario:** *"Two recurring chores remain: old log files pile up, and nobody notices when the disk fills. Build one maintenance script that rotates aged logs and writes a health report with a threshold alert, then schedule it."*

1. Create `maintenance`:

```bash
nano ~/bin/maintenance
```

2. Use this script:

```bash
#!/bin/bash
set -euo pipefail

base="$HOME/os-lab-automation"
logdir="$base/logs"
archive_dir="$logdir/archive"
report="$base/logs/health_report.log"
threshold=90   # percent disk usage that triggers an alert

mkdir -p "$archive_dir"
stamp() { date '+%Y-%m-%d %H:%M:%S'; }

# Part 1: rotate logs older than 1 day into an archive folder.
rotated=0
while IFS= read -r f; do
    mv "$f" "$archive_dir/"
    rotated=$((rotated + 1))
done < <(find "$logdir" -maxdepth 1 -type f -name '*.log' -mtime +1)

# Part 2: health snapshot.
usage=$(df -P "$HOME" | awk 'NR==2 {gsub("%",""); print $5}')
procs=$(ps -u "$(whoami)" --no-headers | wc -l)

{
    echo "----- health check at $(stamp) -----"
    echo "disk usage of home : ${usage}%"
    echo "my processes       : ${procs}"
    echo "load / uptime      : $(uptime)"
    echo "logs rotated       : ${rotated}"
    if [ "$usage" -ge "$threshold" ]; then
        echo "ALERT: disk usage ${usage}% has reached the ${threshold}% threshold!"
    else
        echo "status             : OK (below ${threshold}% threshold)"
    fi
} >> "$report"
```

3. Make it executable and run it once by hand:

```bash
chmod +x ~/bin/maintenance
maintenance
cat ~/os-lab-automation/logs/health_report.log
```

4. Schedule it every 2 minutes (replace `<YourUsername>`):

```bash
crontab -e
```

```cron
# Lab10 maintenance - log rotation + health check, every 2 minutes (TEST interval)
*/2 * * * * /home/<YourUsername>/bin/maintenance >> /home/<YourUsername>/os-lab-automation/logs/cron_maintenance.log 2>&1
```

5. **Wait up to 4 minutes**, then confirm the report grew on its own:

```bash
cat ~/os-lab-automation/logs/health_report.log
```

6. Save evidence:

```bash
{
    echo "=== maintenance script permissions ==="
    ls -l ~/bin/maintenance
    echo "=== installed cron jobs ==="
    crontab -l
    echo "=== health report (multiple entries = cron ran it) ==="
    cat ~/os-lab-automation/logs/health_report.log
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task6_maintenance.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task6_maintenance.txt
```

> **Note on rotation:** In a single session your `.log` files are unlikely to be older than one day, so `logs rotated` will usually be `0`. That is expected. To *prove* the rotation logic works, artificially age a throwaway file: `touch -d '2 days ago' ~/os-lab-automation/logs/old_demo.log` then run `maintenance` again.

> **Required Screenshot 8:** Save as `images/level6_maintenance.png` and embed it in `README.md`.

---

## Level 7 - Design Your Own Scheduled Job (Capstone)

**Scenario:** *"You have copied working examples all lab. Now prove you actually understand cron by building one entirely yourself - you choose the task, write the Bash script, and write the crontab line on your own."*

> This is the only level with **no finished script handed to you**. You design it. Do not reuse `backup_project` or `maintenance` - write something new.

### Step 1 - Choose an automation task

Pick one small, useful job (or invent your own):

| Idea | What the script does |
|------|----------------------|
| Disk watcher | Append free disk space (`df -h $HOME`) to a log |
| File counter | Count the files in your project and log the number |
| Login recorder | Record who is logged in (`who`) with a timestamp |
| Folder snapshot | Make a small timestamped `tar.gz` of one folder |
| Uptime logger | Append the system `uptime` to a log |

### Step 2 - Write your script

Create `my_automation` in `~/bin`. It **must**:

- start with the `#!/bin/bash` shebang
- write **timestamped** output to its own log in `~/os-lab-automation/logs/`
- be made executable with `chmod +x`

Use this skeleton and replace the marked line with your chosen task:

```bash
nano ~/bin/my_automation
```

```bash
#!/bin/bash
set -euo pipefail

base="$HOME/os-lab-automation"
logfile="$base/logs/my_automation.log"

# TODO: replace the line below with YOUR own automation task.
echo "$(date '+%Y-%m-%d %H:%M:%S') | free space: $(df -h "$HOME" | awk 'NR==2 {print $4}')" >> "$logfile"
```

Test it by hand first - never schedule a script you have not run once:

```bash
chmod +x ~/bin/my_automation
my_automation
cat ~/os-lab-automation/logs/my_automation.log
```

### Step 3 - Write your own crontab line

Open your crontab and add **your own** line. You decide the schedule - use a short interval (every 1-2 minutes) so you can watch it fire during the lab. Add a clear comment describing it; this is a practice job, so Level 8 teardown will remove it. Remember the absolute path and the output redirect.

```bash
crontab -e
```

Fill in the schedule and your username yourself:

```cron
# Lab10 my own job - <describe what it does> (TEST interval)
<your schedule> /home/<YourUsername>/bin/my_automation >> /home/<YourUsername>/os-lab-automation/logs/cron_my_automation.log 2>&1
```

Wait for it to fire, then confirm it ran on schedule:

```bash
crontab -l
cat ~/os-lab-automation/logs/my_automation.log
```

### Step 4 - Save evidence

```bash
{
    echo "=== my automation script ==="
    cat ~/bin/my_automation
    echo "=== my cron line ==="
    crontab -l | grep my_automation
    echo "=== output produced on schedule ==="
    cat ~/os-lab-automation/logs/my_automation.log
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task7_own_job.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task7_own_job.txt
```

In your `README.md`, explain **in your own words**: what your script does, the schedule you chose and why, and what each of the five fields in your cron line means.

> **Required Screenshot 9:** Save as `images/level7_own_job.png` and embed it in `README.md`. It must show your script, your crontab line, and the log it produced on schedule.

---

## Level 8 - Teardown and Reset

**Scenario:** *"The lab session is over. Remove only the short practice intervals so they stop spamming your logs - but you must NOT remove the graded deadline job, which still has to fire on 2026-06-22."*

> **Do NOT run `crontab -r` here.** That would delete the graded deadline job and you would fail that task. Remove only the practice jobs.

1. Record your current crontab **before** changing anything:

```bash
crontab -l > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/crontab_before_teardown.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/crontab_before_teardown.txt
```

2. Remove the practice jobs. The only jobs you must keep are the two graded ones, which call `lab_session_job` and `deadline_job`. This pipeline keeps exactly those four lines (the two `GRADED` comments and their job lines) and drops everything else - the heartbeat, the backup, the maintenance job, and the job you wrote in Level 7:

```bash
crontab -l | grep -E 'GRADED|lab_session_job|deadline_job' | crontab -
```

> **Prefer to do it by hand?** Run `crontab -e` and delete the heartbeat, backup, maintenance, and your Level 7 lines, leaving only the two `GRADED` blocks. (A plain `grep -v 'TEST interval'` is **not** enough - it only removes the comment lines and leaves the practice jobs scheduled.)

3. Verify the practice `*/1` and `*/2` jobs are gone and **only the two GRADED jobs remain**:

```bash
crontab -l
```

You should see the session and deadline `GRADED` lines and nothing else. Confirm the practice logs stop growing:

```bash
date
tail -n 3 ~/os-lab-automation/logs/heartbeat.log
```

4. Save evidence:

```bash
{
    echo "=== crontab BEFORE teardown ==="
    cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/crontab_before_teardown.txt
    echo "=== crontab AFTER teardown (only GRADED jobs should remain) ==="
    crontab -l 2>&1 || echo "no crontab for $(whoami)"
    echo "=== final automation tree ==="
    find ~/os-lab-automation -maxdepth 2 | sort
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task8_teardown.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10/task8_teardown.txt
```

> **Required Screenshot 10:** Save as `images/level8_teardown.png` and embed it in `README.md`.

### After the deadline (final cleanup)

Once you have taken Screenshot 6 (deadline job verified) and submitted, you may remove the remaining graded jobs:

```bash
crontab -r
crontab -l 2>&1 || echo "no crontab for $(whoami)"
```

---

## Copy Scripts for Submission

```bash
cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab10
mkdir -p scripts
cp ~/bin/automation_demo  scripts/
cp ~/bin/backup_project   scripts/
cp ~/bin/maintenance      scripts/
cp ~/bin/lab_session_job  scripts/
cp ~/bin/deadline_job     scripts/
cp ~/bin/my_automation    scripts/
cp ~/bin/check_cron_tasks scripts/check_cron_tasks.sh
```

Also save a small operational README in the working folder:

```bash
cat > ~/os-lab-automation/README.md <<'EOF'
QuantumTech Automation Pipeline working folder

Student ID: <YourStudentID>

This folder contains the sample project, file/folder archives,
scheduled-job logs, and the output of the timed graded cron jobs
used by Lab 10. Scripts live in ~/bin and were scheduled with the
per-user crontab (no sudo).
EOF
```

---

## Lab Questions

Answer these in your `README.md`:

1. What is the difference between **archiving** (`tar`) and **compression** (`gzip`)? Which one shrinks bytes?
2. From Level 1, roughly how much smaller was your `.tar.gz` than your `.tar`, and why?
3. Why did your cron jobs need an **absolute path** to the script and the log instead of `~/bin/...`?
4. Why must the `%` sign be escaped as `\%` inside a crontab entry, and what does `>> logfile 2>&1` accomplish?
5. How does your `backup_project` retention logic decide which archives to delete, and why does keeping only N backups matter?
6. Write the cron line that runs `/home/me/bin/deadline_job` once at 2:30 PM on 22 June. Which fields did you have to fill in, and which stayed `*`?
7. In Level 8 teardown, why did you use a filtered `crontab -` pipeline instead of `crontab -r`? What would `crontab -r` have broken?
8. Why is a scheduled health check with a threshold alert useful in real software engineering / operations?
9. Describe the job you wrote in Level 7: what it does, the schedule you chose, and what each of the five fields in your cron line means.

---

## Screenshot Checklist

| # | File Name | Level | What It Shows |
|:-:|-----------|:----:|---------------|
| 1 | `level0_warmup.png` | 0 | `automation_demo` running and its append-only log |
| 2 | `level1_archive.png` | 1 | `.tar` vs `.tar.gz` size difference and successful extract |
| 3 | `level2_backup.png` | 2 | Exactly three retained archives and the backup log |
| 4 | `level3_cron_basics.png` | 3 | `crontab -l` and the per-minute heartbeat log |
| 5 | `level4_session_job.png` | 4 | Session job output + checker showing session task `PASS` (after 2:30 PM lab day) |
| 6 | `level4_deadline_job.png` | 4 | Checker showing **both** tasks `PASS` (after 2026-06-22, before deadline) |
| 7 | `level5_schedule.png` | 5 | Backup archives created by cron, unattended |
| 8 | `level6_maintenance.png` | 6 | Health report with multiple scheduled entries |
| 9 | `level7_own_job.png` | 7 | Your own script, your crontab line, and the log it produced |
| 10 | `level8_teardown.png` | 8 | Practice jobs removed, only GRADED jobs remain, final tree |

---

## Final Submission

> **README template:** A starter `README-template.md` is provided with this lab. Copy it into your `lab10/` folder as `README.md`, fill in every section, embed your screenshots, and answer the Lab Questions.

### Required Working Tree Outside the Repo

```text
~/
|-- bin/
|   |-- automation_demo
|   |-- backup_project
|   |-- maintenance
|   |-- lab_session_job
|   |-- deadline_job
|   |-- my_automation
|   `-- check_cron_tasks
`-- os-lab-automation/
    |-- README.md
    |-- project/
    |   |-- README.md
    |   |-- src/widget.py
    |   `-- docs/{changelog.txt,notes.txt}
    |-- backups/
    |   `-- project_<timestamp>.tar.gz   (3 kept)
    |-- cron_tasks/
    |   |-- session_job.out
    |   `-- deadline_job.out
    `-- logs/
        |-- automation_demo.log
        |-- backup_project.log
        |-- heartbeat.log
        |-- cron_backup.log
        |-- cron_maintenance.log
        |-- cron_session_job.log
        |-- cron_deadline_job.log
        |-- my_automation.log
        |-- cron_my_automation.log
        |-- health_report.log
        `-- archive/
```

### Required Submission Tree

```text
os-se-<YourStudentID>/
`-- os-lab-<YourStudentID>/
    `-- lab10/
        |-- README.md
        |-- task0_warmup.txt
        |-- task1_archive.txt
        |-- task2_backup.txt
        |-- task3_cron_basics.txt
        |-- task4_timed_tasks.txt
        |-- task5_schedule.txt
        |-- task6_maintenance.txt
        |-- task7_own_job.txt
        |-- task8_teardown.txt
        |-- crontab_before_teardown.txt
        |-- scripts/
        |   |-- automation_demo
        |   |-- backup_project
        |   |-- maintenance
        |   |-- lab_session_job
        |   |-- deadline_job
        |   |-- my_automation
        |   `-- check_cron_tasks.sh
        `-- images/
            |-- level0_warmup.png
            |-- level1_archive.png
            |-- level2_backup.png
            |-- level3_cron_basics.png
            |-- level4_session_job.png
            |-- level4_deadline_job.png
            |-- level5_schedule.png
            |-- level6_maintenance.png
            |-- level7_own_job.png
            `-- level8_teardown.png
```

### Git Push

```bash
cd ~/os-se-<YourStudentID>
git add .
git commit -m "Lab 10: backups, archiving, and cron automation"
git push origin main
```

---

## Grading Criteria

| Criteria | Points | Description |
|----------|--------|-------------|
| **Level 0: Automation warm-up** | 6 | `automation_demo` uses functions, timestamped logging, and a clean exit status. |
| **Level 1: Archiving & compression** | 12 | Creates `.tar` and `.tar.gz`, shows the size difference, and verifies an extract. |
| **Level 2: File & folder backup script** | 12 | `backup_project` produces timestamped archives and keeps only the 3 newest. |
| **Level 3: Cron fundamentals** | 8 | Installs a per-minute heartbeat job and reads it back with `crontab -l`. |
| **Level 4: Timed graded cron tasks** | 16 | Session job fires at 2:30 PM live (8) and deadline job fires before the deadline (8); both verified by the checker. |
| **Level 5: Scheduling the backup** | 12 | Schedules the backup with an absolute path and redirected output; proves cron ran it. |
| **Level 6: Maintenance automation** | 8 | `maintenance` rotates logs and writes a threshold health report on a schedule. |
| **Level 7: Design your own scheduled job** | 12 | Student-authored script and a self-written crontab line that runs on schedule, explained in the README. |
| **Level 8: Teardown and reset** | 2 | Selectively removes practice jobs while preserving the graded deadline job. |
| **README, screenshots, and answers** | 12 | Submission tree complete, screenshots embedded, answers show understanding. |
| **Total** | **100** | |

---

## Tips

- If a scheduled job "does nothing," check three things: absolute path to the script, the script is executable (`chmod +x`), and the `%` signs are escaped as `\%`.
- Always redirect output with `>> logfile 2>&1`. A job with no log is a job you cannot debug.
- `tar` archives, `gzip` compresses; `tar -czf` does both. Use `tar -tzf` to peek inside before extracting.
- cron's smallest interval is one minute. Use `*/1` or `*/2` for testing, then switch to realistic times (`@daily`, `30 2 * * *`) in production.
- **Install the Level 4 timed jobs as soon as you reach that level.** The 2:30 PM session job cannot be earned if it is scheduled after 2:30 PM.
- Use `check_cron_tasks` to confirm a job actually ran. A `FAIL` for the deadline job before 2026-06-22 is expected, not a mistake.
- In Level 8, never use `crontab -r` while the graded deadline job is still pending - filter the practice lines out instead, or you will delete the job you still need.
- Remember to run Level 8 teardown. Leaving `*/2` test jobs running will keep writing to logs forever.
- Do not use `sudo` and do not edit `/etc/crontab`. This lab runs entirely from your personal account.
