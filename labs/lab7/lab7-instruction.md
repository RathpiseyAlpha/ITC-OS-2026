# OS Lab 7 — Bash Scripting, Permissions & Server Automation (Hands-on)

| | |
|---|---|
| **Course** | Operating Systems |
| **Lab Title** | Bash Scripting, Permissions & Server Automation |
| **Chapter** | Shell Scripting, Linux Permissions, Automation |
| **Duration** | 3 Hours |
| **Lab Type** | Individual, with peer interaction |

---

> ⚠️ **IMPORTANT — READ EVERYTHING FIRST**
>
> **Before you type a single command, read through this ENTIRE document from top to bottom.** This lab has several scripts that depend on files and permissions created in earlier tasks. If you skip ahead, later tasks may fail in confusing ways.
>
> **Document structure:**
> 1. **Lab Objectives** — What you'll learn
> 2. **Task Overview** — Summary of all tasks
> 3. **Lab Setup** — Repository and folder preparation
> 4. **Quick Reference** — Bash and permission reminders
> 5. **Tasks 1–8 (Required)** — Scripting, PATH, permissions, SUID, harvesting, mailbox automation
> 6. **Deliverables & Submission** — Folder structure, README template, git push
> 7. **Screenshot Checklist** — Every screenshot you need, in one place

---

## Lab Objectives

After completing this lab, students will be able to:

1. Write executable Bash scripts using a shebang.
2. Add a personal `~/bin` directory to the shell `PATH`.
3. Customize login behavior using `.bashrc`.
4. Configure Linux permissions for public read-only and write-only directories.
5. Use Bash variables, arrays, loops, command substitution, and redirection.
6. Demonstrate SUID behavior with a compiled C helper program.
7. Write scripts that safely inspect peer directories on a shared Linux server.
8. Automate cross-user feedback by writing messages into peer drop-boxes.

> **Scenario:** You are building a small "server neighborhood" inside `/home`. Each student has a house, an inbox, an outbox, and a few automation bots. Your goal is to make your own space useful while also interacting safely with classmates' spaces.

---

## Task Overview

| Task | Title | Key Commands / Concepts | Screenshots Required |
|:---:|-------|-------------------------|:-------------------:|
| **1** | Warm-Up Script | shebang, `chmod +x`, `./script` | ✅ |
| **2** | Custom Command Center | `PATH`, `.bashrc`, `source` | ✅ |
| **3** | Doorstep Login Message | variables, arrays, command substitution | ✅ |
| **4** | Secure Mailbox | `chmod 733`, write-only drop-box | ✅ |
| **5** | Broadcaster Script | redirection, timestamps, public outbox | ✅ |
| **6** | VIP Guestbook | C wrapper, SUID, restricted file writes | ✅ |
| **7** | Data Harvester | loops, `/home/*`, readable-file checks | ✅ |
| **8** | Mailman Bot | `while read`, parsing, cross-user writing | ✅ |

---

## Lab Setup

Navigate into your existing lab submission repository and create the `lab7` directory:

```bash
$ cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>
$ mkdir lab7
$ cd lab7
$ mkdir images
```

### Working Location

Most scripts in this lab must live in your Linux home directory:

```bash
~/bin/
```

Your submission files and screenshots must be saved in:

```bash
~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/
```

### Documenting Your Work

1. Save all screenshots in `lab7/images/`.
2. Save required command outputs into `.txt` files in `lab7/`.
3. Keep your scripts in `~/bin/`, but also copy them into `lab7/scripts/` before submission.
4. Work with at least one classmate for the mailbox, guestbook, harvester, and mailman tests.

---

## Quick Reference

### Bash Script Basics

| Syntax | Purpose |
|--------|---------|
| `#!/bin/bash` | Shebang: tells Linux to run the file with Bash |
| `chmod +x scriptname` | Makes a script executable |
| `./scriptname` | Runs a script from the current directory |
| `echo "text"` | Prints text |
| `pwd` | Prints current working directory |
| `date +"%Y-%m-%d %H:%M:%S"` | Prints a formatted timestamp |

### PATH and Configuration

| Command | Purpose |
|---------|---------|
| `echo $PATH` | Shows executable search paths |
| `export PATH="$HOME/bin:$PATH"` | Adds `~/bin` to the front of `PATH` |
| `source ~/.bashrc` | Reloads `.bashrc` without logging out |
| `which commandname` | Shows which executable will run |

### Permissions

| Permission | Meaning |
|------------|---------|
| `chmod 755 dir` | Owner can write; everyone can read/enter |
| `chmod 733 dir` | Owner full access; others can write/enter but cannot list |
| `chmod 600 file` | Owner read/write only |
| `chmod u+s file` | Sets SUID bit on an executable |

### Bash Logic

| Syntax | Purpose |
|--------|---------|
| `value=$(command)` | Stores command output in a variable |
| `for item in /home/*; do ... done` | Loops through matching paths |
| `[ -f "$file" ]` | Tests whether a regular file exists |
| `[ -r "$file" ]` | Tests whether a file is readable |
| `while read -r line; do ... done < file` | Reads a file line by line |

---

## Task 1 — Warm-Up Script: Permissions & Execution

**Scenario:** *"Before automating the server, prove that you understand how Linux executes script files."*

**Instructions:**

1. Create your personal script directory:
   ```bash
   $ mkdir -p ~/bin
   $ chmod 755 ~/bin
   $ cd ~/bin
   ```

2. Create a file named `warmup` with no `.sh` extension:
   ```bash
   $ nano warmup
   ```

3. Add this content:
   ```bash
   #!/bin/bash
   echo "Hello from my first script! My current directory is:"
   pwd
   ```

4. Try to run it by name:
   ```bash
   $ warmup
   ```
   > Expected: `command not found` if `~/bin` is not in your `PATH` yet.

5. Try to run it from the current directory:
   ```bash
   $ ./warmup
   ```
   > Expected: `Permission denied` because the file is not executable yet.

6. Make it executable and run it successfully:
   ```bash
   $ chmod +x warmup
   $ ./warmup
   ```

7. Save evidence:
   ```bash
   $ {
   > echo "=== warmup permissions ==="
   > ls -l ~/bin/warmup
   > echo "=== warmup output ==="
   > ~/bin/warmup
   > } > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/task1_warmup.txt
   $ cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/task1_warmup.txt
   ```

   > 📸 **Required Screenshot 1:** Save as `images/task1_warmup.png`.

---

## Task 2 — Custom Command Center: Setting Up `PATH`

**Scenario:** *"System administrators do not type `./` every time. Make your personal scripts run like normal commands."*

**Instructions:**

1. Open your `.bashrc`:
   ```bash
   $ nano ~/.bashrc
   ```

2. Add this line near the bottom:
   ```bash
   export PATH="$HOME/bin:$PATH"
   ```

3. Reload your configuration:
   ```bash
   $ source ~/.bashrc
   ```

4. Test from your home directory:
   ```bash
   $ cd ~
   $ warmup
   ```

5. Save evidence:
   ```bash
   $ {
   > echo "=== PATH ==="
   > echo "$PATH"
   > echo "=== warmup location ==="
   > which warmup
   > echo "=== warmup command output ==="
   > warmup
   > } > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/task2_path.txt
   $ cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/task2_path.txt
   ```

   > 📸 **Required Screenshot 2:** Save as `images/task2_path.png`.

---

## Task 3 — Doorstep: Dynamic Login Message

**Scenario:** *"When you log in, your shell should greet you and show a small server status snapshot."*

**Instructions:**

1. Open `.bashrc`:
   ```bash
   $ nano ~/.bashrc
   ```

2. Add this block near the bottom:
   ```bash
   # Lab 7 doorstep message
   users_online=$(who | wc -l)
   uptime_info=$(uptime -p)
   jokes=("Keep calm and check the logs." "There is no place like 127.0.0.1." "Automate the boring stuff.")
   joke=${jokes[$RANDOM % ${#jokes[@]}]}

   echo "========================================"
   echo "Welcome, $USER"
   echo "Users currently logged in: $users_online"
   echo "Server uptime: $uptime_info"
   echo "Random tech quote: $joke"
   echo "========================================"
   ```

3. Test it:
   ```bash
   $ source ~/.bashrc
   ```

4. Save evidence:
   ```bash
   $ source ~/.bashrc > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/task3_doorstep.txt
   $ cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/task3_doorstep.txt
   ```

   > 📸 **Required Screenshot 3:** Save as `images/task3_doorstep.png`.

---

## Task 4 — Secure Mailbox: Write-Only Drop-Box

**Scenario:** *"Classmates should be able to drop files into your inbox, but they should not be able to list or read other people's messages."*

**Instructions:**

1. Create your inbox:
   ```bash
   $ mkdir -p ~/public_inbox
   $ chmod 733 ~/public_inbox
   ```

2. Check permissions:
   ```bash
   $ ls -ld ~/public_inbox
   ```

3. Ask a classmate to test from their account:
   ```bash
   $ ls /home/<YourUsername>/public_inbox
   $ touch /home/<YourUsername>/public_inbox/test_from_<ClassmateUsername>.txt
   ```

   Expected:
   - `ls` should fail with `Permission denied`.
   - `touch` should succeed.

4. Save evidence:
   ```bash
   $ {
   > echo "=== inbox permissions ==="
   > ls -ld ~/public_inbox
   > echo "=== inbox files as owner ==="
   > ls -l ~/public_inbox
   > } > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/task4_inbox.txt
   $ cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/task4_inbox.txt
   ```

   > 📸 **Required Screenshot 4:** Save as `images/task4_inbox.png`.

---

## Task 5 — Broadcaster: Public Outbox Automation

**Scenario:** *"Create data for the server neighborhood. Your classmates' bots will try to find it."*

**Instructions:**

1. Create a public outbox:
   ```bash
   $ mkdir -p ~/public_outbox
   $ chmod 755 ~/public_outbox
   ```

2. Create `~/bin/broadcaster`:
   ```bash
   $ nano ~/bin/broadcaster
   ```

3. Add this content:
   ```bash
   #!/bin/bash

   secrets=("kernel" "mutex" "scheduler" "filesystem" "semaphore")
   secret=${secrets[$RANDOM % ${#secrets[@]}]}
   current_time=$(date +"%Y-%m-%d %H:%M:%S")

   echo "$secret - $current_time" > "$HOME/public_outbox/secret.txt"
   chmod 644 "$HOME/public_outbox/secret.txt"
   echo "Broadcast complete: $HOME/public_outbox/secret.txt"
   ```

4. Make it executable and run it:
   ```bash
   $ chmod +x ~/bin/broadcaster
   $ broadcaster
   $ cat ~/public_outbox/secret.txt
   ```

5. Save evidence:
   ```bash
   $ {
   > echo "=== broadcaster script ==="
   > ls -l ~/bin/broadcaster
   > echo "=== outbox permissions ==="
   > ls -ld ~/public_outbox
   > echo "=== secret.txt ==="
   > cat ~/public_outbox/secret.txt
   > } > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/task5_broadcaster.txt
   $ cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/task5_broadcaster.txt
   ```

   > 📸 **Required Screenshot 5:** Save as `images/task5_broadcaster.png`.

---

## Task 6 — VIP Guestbook: SUID Helper Program

**Scenario:** *"Classmates should be able to sign your guestbook, but they should not receive direct read/write access to the guestbook file."*

> Note: Modern Linux ignores SUID on Bash scripts for security reasons. To demonstrate SUID, you will use a compiled C program.

**Instructions:**

1. Create and lock down your guestbook:
   ```bash
   $ touch ~/guestbook.txt
   $ chmod 600 ~/guestbook.txt
   ```

2. Create `sign_book.c` in your `lab7` folder:
   ```bash
   $ cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7
   $ nano sign_book.c
   ```

3. Paste this code. Replace `YOUR_USERNAME` with your real Linux username:
   ```c
   #include <stdio.h>

   int main(int argc, char *argv[]) {
       if (argc != 2) {
           printf("Usage: sign_book 'Your Name'\n");
           return 1;
       }

       FILE *file = fopen("/home/YOUR_USERNAME/guestbook.txt", "a");
       if (file == NULL) {
           printf("Error opening guestbook.\n");
           return 1;
       }

       fprintf(file, "Visitor signed: %s\n", argv[1]);
       fclose(file);
       printf("Successfully signed the VIP guestbook!\n");
       return 0;
   }
   ```

4. Compile it into `~/bin`:
   ```bash
   $ gcc sign_book.c -o ~/bin/sign_book
   $ chmod 4755 ~/bin/sign_book
   ```

5. If classmates cannot reach your `~/bin` directory, allow execute-only traversal of your home directory:
   ```bash
   $ chmod 711 "$HOME"
   ```

6. Ask a classmate to run:
   ```bash
   $ /home/<YourUsername>/bin/sign_book "Hello from <ClassmateUsername>"
   ```

7. Verify your guestbook:
   ```bash
   $ cat ~/guestbook.txt
   $ ls -l ~/guestbook.txt ~/bin/sign_book
   ```

8. Save evidence:
   ```bash
   $ {
   > echo "=== guestbook permissions ==="
   > ls -l ~/guestbook.txt
   > echo "=== sign_book permissions ==="
   > ls -l ~/bin/sign_book
   > echo "=== guestbook contents ==="
   > cat ~/guestbook.txt
   > } > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/task6_guestbook.txt
   $ cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/task6_guestbook.txt
   ```

   > 📸 **Required Screenshot 6:** Save as `images/task6_guestbook.png`.

---

## Task 7 — Data Harvester: Cross-User Scripting

**Scenario:** *"Write a bot that scans the server neighborhood and collects readable secrets."*

**Instructions:**

1. Create `~/bin/harvester`:
   ```bash
   $ nano ~/bin/harvester
   ```

2. Add this content:
   ```bash
   #!/bin/bash

   report="$HOME/harvest_report.txt"
   > "$report"

   for user_dir in /home/*; do
       username=$(basename "$user_dir")
       target_file="$user_dir/public_outbox/secret.txt"

       if [ -f "$target_file" ] && [ -r "$target_file" ]; then
           secret_data=$(cat "$target_file")
           echo "${username}'s secret is: $secret_data" >> "$report"
       fi
   done

   echo "Harvest complete. Report saved to $report"
   ```

3. Make it executable and run it:
   ```bash
   $ chmod +x ~/bin/harvester
   $ harvester
   $ cat ~/harvest_report.txt
   ```

4. If a classmate's secret is missing, ask them to check:
   ```bash
   $ ls -ld ~/public_outbox
   $ ls -l ~/public_outbox/secret.txt
   ```

5. Save evidence:
   ```bash
   $ cp ~/harvest_report.txt ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/harvest_report.txt
   $ cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/harvest_report.txt
   ```

   > 📸 **Required Screenshot 7:** Save as `images/task7_harvester.png`.

---

## Task 8 — Mailman Bot: Automated Feedback

**Scenario:** *"Now prove that your harvester worked by dropping automated messages into classmates' secure inboxes."*

**Instructions:**

1. Create `~/bin/mailman`:
   ```bash
   $ nano ~/bin/mailman
   ```

2. Add this content:
   ```bash
   #!/bin/bash

   report="$HOME/harvest_report.txt"
   sent_count=0

   if [ ! -f "$report" ]; then
       echo "Missing $report. Run harvester first."
       exit 1
   fi

   while read -r line; do
       classmate=$(echo "$line" | awk -F"'" '{print $1}')
       secret=$(echo "$line" | awk -F"is: " '{print $2}' | awk -F" - " '{print $1}')
       inbox="/home/$classmate/public_inbox"
       message="$inbox/message_from_$USER.txt"

       if [ -d "$inbox" ]; then
           echo "Hello $classmate, I am an automated bot written by $USER. I successfully read your secret word: $secret." > "$message" 2>/dev/null
           if [ $? -eq 0 ]; then
               echo "Sent message to $classmate"
               sent_count=$((sent_count + 1))
           else
               echo "Could not write to $classmate's inbox"
           fi
       fi

       if [ "$sent_count" -ge 3 ]; then
           break
       fi
   done < "$report"

   echo "Messages sent: $sent_count"
   ```

3. Make it executable and run it:
   ```bash
   $ chmod +x ~/bin/mailman
   $ mailman
   ```

4. Check your own inbox:
   ```bash
   $ ls -l ~/public_inbox
   $ cat ~/public_inbox/message_from_*.txt 2>/dev/null
   ```

5. Save evidence:
   ```bash
   $ {
   > echo "=== mailman output ==="
   > mailman
   > echo "=== my inbox ==="
   > ls -l ~/public_inbox
   > echo "=== messages I received ==="
   > cat ~/public_inbox/message_from_*.txt 2>/dev/null
   > } > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/task8_mailman.txt
   $ cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7/task8_mailman.txt
   ```

   > 📸 **Required Screenshot 8:** Save as `images/task8_mailman.png`.

---

## Copy Scripts for Submission

Before submitting, copy your scripts into your lab folder:

```bash
$ cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab7
$ mkdir -p scripts
$ cp ~/bin/warmup scripts/
$ cp ~/bin/broadcaster scripts/
$ cp ~/bin/harvester scripts/
$ cp ~/bin/mailman scripts/
$ cp ~/bin/sign_book scripts/sign_book_binary
```

---

## Lab Questions

Answer these in your `README.md`:

1. Why did `warmup` fail before you added execute permission?
2. What does adding `~/bin` to `PATH` allow you to do?
3. Why does `chmod 733 public_inbox` allow classmates to drop files but not list the inbox?
4. Why does Linux ignore SUID on shell scripts, and why did we use a compiled C program instead?
5. What is the difference between `>` and `>>` in Bash redirection?
6. How did your `harvester` avoid reading files that were missing or not readable?
7. What permission problems did you or your classmates need to fix during the lab?

---

## Screenshot Checklist

Before submitting, verify you have all required screenshots:

| # | File Name | Task | What It Shows |
|:-:|-----------|:----:|---------------|
| 1 | `task1_warmup.png` | Task 1 | `warmup` permissions and successful output |
| 2 | `task2_path.png` | Task 2 | `PATH`, `which warmup`, and running `warmup` by name |
| 3 | `task3_doorstep.png` | Task 3 | Dynamic login/status message from `.bashrc` |
| 4 | `task4_inbox.png` | Task 4 | `public_inbox` permissions and received test file |
| 5 | `task5_broadcaster.png` | Task 5 | `public_outbox` and generated `secret.txt` |
| 6 | `task6_guestbook.png` | Task 6 | SUID binary permissions and guestbook contents |
| 7 | `task7_harvester.png` | Task 7 | `harvest_report.txt` with classmates' secrets |
| 8 | `task8_mailman.png` | Task 8 | Mailman output and inbox messages |

---

## Final Submission

### Required Folder Structure

```
os-se-<YourStudentID>/
└── os-lab-<YourStudentID>/
    └── lab7/
        ├── README.md
        ├── task1_warmup.txt
        ├── task2_path.txt
        ├── task3_doorstep.txt
        ├── task4_inbox.txt
        ├── task5_broadcaster.txt
        ├── task6_guestbook.txt
        ├── harvest_report.txt
        ├── task8_mailman.txt
        ├── sign_book.c
        ├── scripts/
        │   ├── warmup
        │   ├── broadcaster
        │   ├── harvester
        │   ├── mailman
        │   └── sign_book_binary
        └── images/
            ├── task1_warmup.png
            ├── task2_path.png
            ├── task3_doorstep.png
            ├── task4_inbox.png
            ├── task5_broadcaster.png
            ├── task6_guestbook.png
            ├── task7_harvester.png
            └── task8_mailman.png
```

### Git Push

```bash
$ cd ~/os-se-<YourStudentID>
$ git add .
$ git commit -m "Lab 7: Bash scripting and server automation"
$ git push origin main
```

---

## Grading Criteria

| Criteria | Points | Description |
|----------|--------|-------------|
| **Tasks 1–2: Script execution and PATH** | 15 | `warmup` works, permissions are correct, and `PATH` is configured. |
| **Task 3: Doorstep message** | 10 | `.bashrc` shows dynamic username, logged-in users, uptime, and random quote. |
| **Task 4: Secure mailbox** | 10 | `public_inbox` uses correct write-only drop-box permissions and is tested with a classmate. |
| **Task 5: Broadcaster** | 10 | `broadcaster` creates readable `secret.txt` with a secret and timestamp. |
| **Task 6: VIP guestbook** | 15 | SUID C helper is compiled, permissioned, tested, and documented. |
| **Task 7: Harvester** | 15 | Script loops through `/home`, checks readable secrets, and builds `harvest_report.txt`. |
| **Task 8: Mailman** | 10 | Script reads the harvest report and sends automated messages to at least three classmates. |
| **README, screenshots, and answers** | 15 | README is complete, screenshots are embedded, outputs are present, and questions are answered clearly. |
| **Total** | **100** | |

---

## Tips

- Do not add `.sh` extensions to the required command scripts.
- If a command works with `./script` but not by name, check `PATH`.
- If classmates cannot write into your inbox, check `chmod 733 ~/public_inbox`.
- If classmates cannot read your outbox secret, check `chmod 755 ~/public_outbox` and `chmod 644 ~/public_outbox/secret.txt`.
- If SUID does not work, check that `~/bin/sign_book` is owned by you and has `-rwsr-xr-x` style permissions.
- If your harvester finds no secrets, ask classmates whether they ran `broadcaster`.
