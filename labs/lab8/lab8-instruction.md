# OS Lab 8 - Secure Bash Scripting, Race Conditions & File Locking (Hands-on)

| | |
|---|---|
| **Course** | Operating Systems |
| **Lab Title** | The Quantum Widget Exploit |
| **Chapter** | Secure Bash Scripting, Critical Sections, Permissions |
| **Duration** | 3 Hours |
| **Lab Type** | Individual, with peer red-team testing |

---

**Source reference:** This canonical lab instruction was adapted from the original Quantum Widget brief.

---

> **IMPORTANT - READ EVERYTHING FIRST**
>
> Before you type a single command, read this document from top to bottom. This lab starts with a basic Bash warm-up, then moves into a vulnerable Bash program that you will exploit and patch. If you skip the observation steps, you will miss the main OS lesson.
>
> **Document structure:**
> 1. **Lab Objectives** - What you will learn
> 2. **Mission Briefing** - Incident response scenario
> 3. **Task Overview** - Summary of all levels
> 4. **Lab Setup** - Repository, server, and naming rules
> 5. **Quick Reference** - Bash, permissions, and `flock`
> 6. **Levels 0-7 (Required)** - Bash warm-up, validation, logging, TOC-TOU exploit, mutex patch, permissions, drop zone, cleanup
> 7. **Deliverables & Submission** - Folder structure, README template, git push
> 8. **Screenshot Checklist** - Every screenshot you need, in one place

---

## Lab Objectives

After completing this lab, students will be able to:

1. Use Bash variables, positional parameters (`$1`, `$2`), exit status (`$?`), conditionals, and loops.
2. Write secure Bash scripts using functions and strict input validation.
3. Explain a Time-of-Check to Time-of-Use (TOC-TOU) vulnerability caused by concurrent OS processes.
4. Demonstrate how process scheduling can produce inconsistent results in a shared file update.
5. Patch a race condition using OS-level mutual exclusion with `flock`.
6. Configure cross-user execution permissions without using `sudo`.
7. Apply the principle of least privilege using a shared sticky-bit drop zone.
8. Automate log cleanup by sorting files according to extension.

> **Scenario:** You are a DevSecOps engineer at **QuantumTech**. The company is launching a limited-edition **Quantum Widget** with only **100 units** in stock. A botnet is trying to abuse concurrent purchases to drain the inventory. Your job is to build the backend script, observe the exploit, patch the critical section, and secure the shared environment.

---

## Task Overview

| Level | Title | Key Commands / Concepts | Screenshots Required |
|:---:|-------|-------------------------|:-------------------:|
| **0** | Bash Warm-Up Scripts | arguments, parameters, `$0`, `$1`, `$2`, `$#`, `$?`, `if`, `for` | yes |
| **1** | Input Validation | arguments, integer checks, `chmod +x` | optional evidence |
| **2** | Audit Trails | functions, file I/O, `sales.log` | yes |
| **3** | The Exploit | background jobs, `wait`, TOC-TOU | observations file |
| **4** | The Patch | mutex, `flock`, critical section | yes |
| **5** | Red Team vs. Blue Team | absolute paths, cross-user permissions | yes |
| **6** | Secure Drop Zone | least privilege, sticky bit | yes |
| **7** | Forensic Cleanup | loops, extensions, `mv`, `tree` / `ls -R` | yes |

---

## Lab Setup

Navigate into your existing lab submission repository and create the `lab8` directory:

```bash
cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>
mkdir lab8
cd lab8
mkdir images scripts
```

### Working Location

Your active scripts should live in a personal executable directory that is already on your `PATH`:

```bash
~/bin/
```

Your submission files and screenshots must be saved in:

```bash
~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab8/
```

### Rules for This Lab

1. Use the shared Linux server with your assigned student account.
2. Do not use `sudo`. All security controls must work with standard user privileges.
3. Script names must be lowercase, snake_case, and have no file extension.
4. Use your real student ID in audit log lines.
5. Work with at least one classmate for Level 5 and Level 6.

---

## Quick Reference

### Bash Basics

| Syntax | Purpose |
|--------|---------|
| `$#` | Number of command-line arguments |
| `$1`, `$2` | First and second command-line arguments |
| `$?` | Exit status of the most recent command (`0` means success) |
| `name="Ada"` | Assign a variable; no spaces around `=` |
| `echo "$name"` | Read a variable safely with quotes |
| `[[ "$x" =~ regex ]]` | Bash regular-expression test |
| `if condition; then ... fi` | Run code only when a condition is true |
| `for i in {1..50}; do ... done` | Loop 50 times |
| `command &` | Run command in the background |
| `wait` | Wait for background jobs to finish |

### Permissions

| Command | Purpose |
|---------|---------|
| `chmod +x script` | Make a script executable |
| `chmod o+x "$HOME"` | Let others traverse your home directory |
| `chmod o+rx buy_widget` | Let others read and run a script |
| `chmod o+rw file` | Let others read and write a file |
| `chmod +t directory` | Apply sticky bit to a shared directory |

### File Locking

| Pattern | Purpose |
|---------|---------|
| `flock -x 200` | Acquire an exclusive lock on file descriptor 200 |
| `) 200> inventory.lock` | Attach file descriptor 200 to the lock file |
| critical section | The code region where shared data must not be modified concurrently |

---

## Level 0 - Bash Warm-Up Scripts

**Scenario:** *"Before touching the live Quantum Widget store, prove you understand how a Bash script receives words from the command line. These warm-ups are intentionally simple so you can explain every line before moving on to the exploit."*

1. Create your script workspace:
   ```bash
   mkdir -p ~/bin
   cd ~/bin
   ```

### Part A - Argument Viewer

Create a very short script named `arg_viewer`. This script should help you explain the difference between the command you run, the arguments you pass, and the special variables Bash fills in.

```bash
nano arg_viewer
```

Use this script:

```bash
#!/bin/bash

echo "Script name (\$0): $0"
echo "First argument (\$1): $1"
echo "Second argument (\$2): $2"
echo "Number of arguments (\$#): $#"

test -n "$1"
echo "Exit status of 'test -n \$1' (\$?): $?"
```

Make it executable:

```bash
chmod +x arg_viewer
```

Run it twice:

```bash
arg_viewer Alice 3
arg_viewer
```

What to understand:

- `arg_viewer Alice 3` is the command you typed.
- `Alice` and `3` are arguments.
- Inside the script, those arguments become parameters: `$1` is `Alice`, `$2` is `3`.
- `$#` is the number of arguments.
- `$?` is the exit status of the most recent command.

### Part B - Operator Console

Create a script named `quantum_probe`:
   ```bash
   nano quantum_probe
   ```

Your script must use:
   - normal variables, such as `operator="$1"` and `cycles="$2"`
   - special variables `$1` and `$2` for command-line input
   - `$#` to check the number of arguments
   - `$?` to inspect whether a command succeeded
   - at least one `if` condition
   - at least one loop

Required behavior:
   - accept exactly two arguments: operator name and number of diagnostic cycles
   - print `Usage: quantum_probe <operator> <cycles>` when the argument count is wrong
   - reject non-positive or non-integer cycle counts
   - create a folder named `probe_logs`
   - store the exit status of `mkdir -p probe_logs` in a variable and print it
   - loop from `1` to the requested cycle count and print one status line per cycle
   - exit with status `0` for success and nonzero for invalid input

Example structure:
   ```bash
   #!/bin/bash

   operator="$1"
   cycles="$2"

   if [ "$#" -ne 2 ]; then
       echo "Usage: quantum_probe <operator> <cycles>"
       exit 1
   fi

   if ! [[ "$cycles" =~ ^[1-9][0-9]*$ ]]; then
       echo "Error: cycles must be a positive integer."
       exit 2
   fi

   mkdir -p probe_logs
   mkdir_status=$?
   echo "mkdir exit status: $mkdir_status"

   if [ "$mkdir_status" -ne 0 ]; then
       echo "Could not prepare probe_logs."
       exit 3
   fi

   echo "Operator: $operator"
   echo "Cycles requested: $cycles"

   for i in $(seq 1 "$cycles"); do
       echo "Cycle $i: quantum widget console online"
   done

   exit 0
   ```

Make it executable:
   ```bash
   chmod +x quantum_probe
   ```

Save evidence for both warm-up scripts:
   ```bash
   {
       cd ~/bin
       echo "=== argument viewer with arguments ==="
       arg_viewer Alice 3
       echo "=== argument viewer with no arguments ==="
       arg_viewer
       echo "=== successful probe ==="
       quantum_probe Alice 3
       echo "exit status after success: $?"
       echo "=== invalid probe ==="
       quantum_probe Bob not_a_number
       echo "exit status after invalid input: $?"
       echo "=== loop/log directory evidence ==="
       ls -ld ~/bin/probe_logs
   } > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab8/task0_warmup.txt
   cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab8/task0_warmup.txt
   ```

> **Required Screenshot 1:** Save as `images/level0_warmup.png` and embed it in `README.md`.

---

## Level 1 - Input Validation: Building the Engine

**Scenario:** *"Before we defend the store, we need a purchase script that refuses bad input."*

1. Create your script workspace:
   ```bash
   mkdir -p ~/bin
   cd ~/bin
   ```

2. Create the inventory file:
   ```bash
   echo 100 > inventory.txt
   ```

3. Create a script named `buy_widget`:
   ```bash
   nano buy_widget
   ```

4. Your script must:
   - accept exactly two arguments: `username` and `purchase_quantity`
   - print `Usage: buy_widget <username> <quantity>` if the argument count is wrong
   - reject any quantity that is not a positive integer
   - reject negative numbers, zero, decimals, letters, and blank values

5. Make it executable:
   ```bash
   chmod +x buy_widget
   ```

6. Save evidence:
   ```bash
   {
       echo "=== missing argument test ==="
       buy_widget Alice
       echo "=== invalid quantity test ==="
       buy_widget Eve -3
       echo "=== script permissions ==="
       ls -l ~/bin/buy_widget
   } > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab8/task1_validation.txt
   cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab8/task1_validation.txt
   ```

---

## Level 2 - Audit Trails: Functions & File I/O

**Scenario:** *"In incident response, if it is not logged, it did not happen."*

Modify `buy_widget` so it includes the actual purchase logic.

### Requirements

1. Create a function named `log_transaction`.
2. Append successful transactions to `sales.log`.
3. Each successful log entry must include your actual student ID:
   ```text
   [YourStudentID] [SUCCESS] <username> bought <quantity> widgets.
   ```
4. Read the current inventory from `inventory.txt`.
5. If enough widgets are available, subtract the requested quantity and overwrite `inventory.txt`.
6. If not enough widgets are available, print:
   ```text
   Transaction Failed: Not enough inventory!
   ```

### Observation Checkpoint 1

Run these commands exactly in order:

```bash
buy_widget Alice 5
buy_widget Hacker_Bob 200
buy_widget Eve -3
```

Save evidence:

```bash
{
    echo 100 > ~/bin/inventory.txt
    rm -f ~/bin/sales.log
    echo "=== transaction tests ==="
    buy_widget Alice 5
    buy_widget Hacker_Bob 200
    buy_widget Eve -3
    echo "=== inventory ==="
    cat ~/bin/inventory.txt
    echo "=== sales.log ==="
    cat ~/bin/sales.log
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab8/task2_audit.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab8/task2_audit.txt
```

> **Required Screenshot 2:** Save as `images/level2_audit.png` and embed it in `README.md`.

---

## Level 3 - The Exploit: TOC-TOU Vulnerability

**Scenario:** *"Your script works for one buyer. Now simulate 50 buyers arriving at the same instant."*

1. Reset your inventory and log:
   ```bash
   echo 100 > ~/bin/inventory.txt
   rm -f ~/bin/sales.log
   ```

2. Create a new script named `bot_swarm`:
   ```bash
   nano ~/bin/bot_swarm
   ```

3. Inside `bot_swarm`, run 50 concurrent purchases:
   ```bash
   #!/bin/bash

   for i in {1..50}; do
       buy_widget "Bot_$i" 2 &
   done

   wait
   ```

4. Make it executable and run it:
   ```bash
   chmod +x ~/bin/bot_swarm
   bot_swarm
   cat ~/bin/inventory.txt
   ```

### Observation Checkpoint 2

Reset inventory to `100`, clear the log, and run `bot_swarm` five separate times.

Create `observations.txt` in your `lab8` folder. Record:

1. final inventory after each of the five runs
2. whether each result was expected or suspicious
3. a 2-3 sentence explanation of why the value changes based on OS process scheduling

Example format:

```text
Run 1 final inventory: __
Run 2 final inventory: __
Run 3 final inventory: __
Run 4 final inventory: __
Run 5 final inventory: __

Explanation:
...
```

---

## Level 4 - The Patch: Mutex / File Locking

**Scenario:** *"Patch the shared inventory update so only one process can touch it at a time."*

Modify `buy_widget` to wrap the inventory read, inventory calculation, inventory write, and log append inside an exclusive `flock` block:

```bash
(
    flock -x 200

    # critical section starts here
    # read inventory
    # validate availability
    # write new inventory
    # append sales log
    # critical section ends here
) 200> inventory.lock
```

Before the critical section, anchor file paths to the directory where the script lives. This keeps Level 5 correct when a classmate runs your script by absolute path from a different working directory:

```bash
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
inventory_file="$script_dir/inventory.txt"
sales_log="$script_dir/sales.log"
lock_file="$script_dir/inventory.lock"
```

Then use those variables inside the lock:

```bash
(
    flock -x 200
    # read and write "$inventory_file"
    # append to "$sales_log"
) 200> "$lock_file"
```

### Observation Checkpoint 3

1. Reset inventory and log:
   ```bash
   echo 100 > ~/bin/inventory.txt
   rm -f ~/bin/sales.log
   ```

2. Run the swarm again:
   ```bash
   bot_swarm
   ```

3. Verify inventory is exactly `0`:
   ```bash
   cat ~/bin/inventory.txt
   tail -5 ~/bin/sales.log
   ```

4. Save evidence:
   ```bash
   {
       echo "=== final inventory ==="
       cat ~/bin/inventory.txt
       echo "=== last 5 sales ==="
       tail -5 ~/bin/sales.log
   } > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab8/task4_mutex.txt
   cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab8/task4_mutex.txt
   ```

> **Required Screenshot 3:** Save as `images/level4_mutex.png` and embed it in `README.md`.

---

## Level 5 - Red Team vs. Blue Team: Cross-User Permissions

**Scenario:** *"Your mutex works against your own bots. Now expose the API to a classmate without exposing your whole account."*

Pair up with a classmate. Decide who is Player A and Player B.

### Blue Team Setup

1. Create a public API folder:
   ```bash
   mkdir -p ~/public_api
   ```

2. Move or copy your protected files into it:
   ```bash
   cp ~/bin/buy_widget ~/public_api/
   cp ~/bin/inventory.txt ~/public_api/
   cp ~/bin/sales.log ~/public_api/ 2>/dev/null || touch ~/public_api/sales.log
   touch ~/public_api/inventory.lock
   ```

3. Configure permissions:
   ```bash
   chmod o+x "$HOME"
   chmod 755 ~/public_api
   chmod o+rx ~/public_api/buy_widget
   chmod o+rw ~/public_api/inventory.txt ~/public_api/sales.log ~/public_api/inventory.lock
   ```

4. Confirm:
   ```bash
   ls -ld "$HOME" ~/public_api
   ls -l ~/public_api
   ```

### Red Team Attack

Modify your own `bot_swarm` so it targets your partner's absolute script path:

```bash
#!/bin/bash

target="/home/<PartnerUsername>/public_api/buy_widget"

for i in {1..50}; do
    "$target" "RedTeam_${USER}_$i" 2 &
done

wait
```

Both partners should run their swarms against each other at nearly the same time.

### Observation Checkpoint 4

Check your own `~/public_api/sales.log`. Your partner should appear in the log, and your inventory should still be protected by the lock.

Save evidence:

```bash
{
    echo "=== public api permissions ==="
    ls -ld "$HOME" ~/public_api
    ls -l ~/public_api
    echo "=== inventory ==="
    cat ~/public_api/inventory.txt
    echo "=== red team sales evidence ==="
    tail -10 ~/public_api/sales.log
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab8/task5_red_blue.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab8/task5_red_blue.txt
```

> **Required Screenshot 4:** Save as `images/level5_red_blue.png` and embed it in `README.md`.

---

## Level 6 - Principle of Least Privilege: Secure Drop Zone

**Scenario:** *"External vendors need to upload reports, but they must not delete files owned by you."*

Create a script named `create_dropzone`.

### Requirements

1. Prompt the operator for a folder name:
   ```bash
   read -r -p "Drop zone folder name: " folder
   ```

2. Create the folder in your home directory.
3. Allow others to write and enter the directory.
4. Apply the sticky bit.
5. Print the final permissions using `ls -ld`.

Recommended permission pattern:

```bash
chmod o+wx "$HOME/$folder"
chmod +t "$HOME/$folder"
```

### Observation Checkpoint 5

1. Run `create_dropzone` and create a folder such as `vendor_reports`.
2. Create your protected file:
   ```bash
   echo "Only I should delete this." > ~/vendor_reports/my_rules.txt
   ```

3. Ask your partner to create:
   ```bash
   echo "Partner report" > /home/<YourUsername>/vendor_reports/partner_report.txt
   ```

4. Ask your partner to try deleting your file:
   ```bash
   rm /home/<YourUsername>/vendor_reports/my_rules.txt
   ```

5. Save evidence:
   ```bash
   {
       echo "=== drop zone permissions ==="
       ls -ld ~/vendor_reports
       echo "=== drop zone files ==="
       ls -l ~/vendor_reports
       echo "=== partner deletion result ==="
       echo "Paste or summarize the Permission denied result here."
   } > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab8/task6_dropzone.txt
   cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab8/task6_dropzone.txt
   ```

> **Required Screenshot 5:** Save as `images/level6_dropzone.png` and embed it in `README.md`.

---

## Level 7 - Forensic Cleanup: Log Management

**Scenario:** *"The attack generated many files. A SOC analyst needs them sorted by extension."*

Create a script named `cleanup`.

### Requirements

1. Create three dummy files in a test directory:
   ```bash
   mkdir -p ~/forensic_cleanup
   cd ~/forensic_cleanup
   touch test.log data.csv error.tmp
   ```

2. Write `cleanup` so it:
   - loops through files in the current directory
   - detects each file extension
   - creates a folder named after the extension if needed
   - moves the file into the matching folder
   - ignores files without extensions
   - does not move itself while it is running

3. Run it and verify:
   ```bash
   cleanup
   tree . 2>/dev/null || ls -R .
   ```

4. Save evidence:
   ```bash
   { tree . 2>/dev/null || ls -R .; } > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab8/task7_cleanup.txt
   cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab8/task7_cleanup.txt
   ```

> **Required Screenshot 6:** Save as `images/level7_cleanup.png` and embed it in `README.md`.

---

## Copy Scripts for Submission

Before submitting, copy your scripts into your lab folder:

```bash
cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab8
mkdir -p scripts
cp ~/bin/arg_viewer scripts/
cp ~/bin/quantum_probe scripts/
cp ~/bin/buy_widget scripts/
cp ~/bin/bot_swarm scripts/
cp ~/bin/create_dropzone scripts/
cp ~/bin/cleanup scripts/
```

If your final Level 5 version of `buy_widget` lives in `~/public_api`, copy that final patched version instead:

```bash
cp ~/public_api/buy_widget scripts/buy_widget
```

---

## Lab Questions

Answer these in your `README.md`:

1. What does TOC-TOU mean, and where did it appear in the vulnerable `buy_widget` script?
2. Why did `bot_swarm` sometimes leave inventory values other than `0` before the patch?
3. What part of the script is the critical section, and why must it be protected?
4. How does `flock -x` enforce mutual exclusion between concurrent processes?
5. Which permissions did you use to let a classmate run your API without giving full access to your home directory?
6. Why does the sticky bit protect files in a shared drop zone?
7. What defensive scripting practice from this lab would you use in a real production script?

---

## Screenshot Checklist

Before submitting, verify you have all required screenshots:

| # | File Name | Level | What It Shows |
|:-:|-----------|:----:|---------------|
| 1 | `level0_warmup.png` | Level 0 | `arg_viewer` special variables and `quantum_probe` condition/loop output |
| 2 | `level2_audit.png` | Level 2 | Input validation, successful sale, failed sale, inventory, and log |
| 3 | `level4_mutex.png` | Level 4 | Patched swarm result with inventory exactly `0` and last 5 sales |
| 4 | `level5_red_blue.png` | Level 5 | Partner execution evidence in `public_api/sales.log` |
| 5 | `level6_dropzone.png` | Level 6 | Sticky-bit directory permissions and deletion-denied evidence |
| 6 | `level7_cleanup.png` | Level 7 | Files sorted into extension folders |

---

## Final Submission

### Required Folder Structure

```text
os-se-<YourStudentID>/
`-- os-lab-<YourStudentID>/
    `-- lab8/
        |-- README.md
        |-- observations.txt
        |-- task0_warmup.txt
        |-- task1_validation.txt
        |-- task2_audit.txt
        |-- task4_mutex.txt
        |-- task5_red_blue.txt
        |-- task6_dropzone.txt
        |-- task7_cleanup.txt
        |-- scripts/
        |   |-- arg_viewer
        |   |-- quantum_probe
        |   |-- buy_widget
        |   |-- bot_swarm
        |   |-- create_dropzone
        |   `-- cleanup
        `-- images/
            |-- level0_warmup.png
            |-- level2_audit.png
            |-- level4_mutex.png
            |-- level5_red_blue.png
            |-- level6_dropzone.png
            `-- level7_cleanup.png
```

### Git Push

```bash
cd ~/os-se-<YourStudentID>
git add .
git commit -m "Lab 8: Secure Bash scripting and TOC-TOU mutex"
git push origin main
```

---

## Grading Criteria

| Criteria | Points | Description |
|----------|--------|-------------|
| **Level 0: Bash warm-up scripts** | 10 | `arg_viewer` explains special variables, and `quantum_probe` demonstrates variables, `$1`, `$2`, `$?`, conditionals, and loops. |
| **Levels 1-2: Validation and audit logging** | 15 | `buy_widget` validates input, updates inventory correctly, and logs successful transactions with student ID. |
| **Level 3: Race-condition experiment** | 15 | `bot_swarm` demonstrates concurrent execution and `observations.txt` explains the TOC-TOU behavior clearly. |
| **Level 4: Mutex patch** | 20 | `flock` protects the critical section and the swarm reliably ends with inventory `0`. |
| **Level 5: Cross-user permission test** | 15 | Partner can execute the public API while inventory locking still works. |
| **Level 6: Secure drop zone** | 10 | Sticky-bit drop zone allows uploads while preventing deletion of another user's file. |
| **Level 7: Forensic cleanup** | 5 | `cleanup` sorts files safely by extension. |
| **README, screenshots, and organization** | 10 | Submission is complete, screenshots are embedded, and answers show understanding. |
| **Total** | **100** | |

---

## Tips

- Keep one final patched version of `buy_widget`; do not submit only the vulnerable version.
- If the swarm still produces inconsistent results after the patch, check that every inventory read/write happens inside the same `flock` block.
- If a partner cannot execute your API, check traversal permission on your home directory and execute permission on `public_api`.
- If a partner can delete your file in the drop zone, check for the `t` bit in `ls -ld`.
- Avoid `chmod 777` on your whole home directory. That solves one problem by creating several larger ones.
