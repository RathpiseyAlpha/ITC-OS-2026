# OS Lab 2 — Linux Navigation & File Management (Hands-on)

| | |
|---|---|
| **Course** | Operating Systems |
| **Lab Title** | Mastering Linux Navigation & File Management |
| **Chapter** | Linux Essentials — Navigation |
| **Duration** | 2 Hours |
| **Lab Type** | Individual |

---

## Lab Objectives

After completing this lab, students will be able to:

1. Use basic navigation commands (`cd`, `pwd`, `ls`) to move around the filesystem.
2. Navigate the Linux filesystem using both absolute and relative paths.
3. Explain the role of key system directories (`/`, `/etc`, `/var`, `/home`, `/tmp`).
4. Use the `..` (parent) and `.` (current directory) shortcuts to navigate efficiently.
5. Build complex, multi-level directory structures with `mkdir -p`.
6. Move, copy, rename, and remove files across different directories.
7. Use advanced `ls` options (`-R`, `-lS`, `-lt`, `-lh`, `-r`) to list and sort directory contents.
8. Apply previously learned commands to solve new, unfamiliar problems independently.

> **Scenario:** You are **Alex**, a newly hired junior system administrator at **TechCorp Inc.** Your first assignment is to set up and organize the company's shared file server. Each task below represents a real responsibility you would face on your first day.

---

## Lab Setup

Navigate into your existing lab submission repository and create the `lab2` directory:

```bash
cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>
mkdir lab2
cd lab2
```

### Documenting Your Work (Taking Screenshots)

Follow the same process as Lab 1:

1. **Take Screenshots:** As you complete each task, capture your terminal using your host machine's screenshot tool.
2. **Save Temporarily:** Save images to a folder on your host machine. Name them clearly (e.g., `task1.png`, `task2.png`).
3. **Document Later:** You will add these images to a `README.md` file after finishing all terminal tasks.

### Lab Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         WSL / Linux Terminal                            │
│                                                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │
│  │ Task 1  │  │ Task 2  │  │ Task 3  │  │ Task 4  │  │ Task 5  │      │
│  │ Basic   │─▶│ Explore │─▶│ Build   │─▶│Navigate │─▶│Organize │      │
│  │ Nav     │  │ FileSys │  │ DirTree │  │ Paths   │  │ Files   │      │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └────┬────┘      │
│                                                             │           │
│                                           ┌─────────┐      │           │
│                                           │ Task 6  │      │           │
│                                           │Advanced │◀─────┘           │
│                                           │ Listing │                   │
│                                           └────┬────┘                   │
│                                                │                        │
│                                                ▼                        │
│                                         ┌───────────┐                   │
│                                         │ git push  │                   │
│                                         │ to GitHub │                   │
│                                         └─────┬─────┘                   │
└───────────────────────────────────────────────┼─────────────────────────┘
                                                │
                                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Host OS (Windows / Mac)                          │
│                                                                         │
│   ┌──────────────┐   ┌───────────────┐   ┌─────────────────────┐       │
│   │ Clone/Pull   │──▶│ Add Images &  │──▶│ Final git push      │       │
│   │ in VS Code   │   │ Write README  │   │ to GitHub           │       │
│   └──────────────┘   └───────────────┘   └──────────┬──────────┘       │
└─────────────────────────────────────────────────────┼──────────────────┘
                                                      │
                                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        Local Lab Server (SSH)                           │
│                                                                         │
│   ┌───────────────────┐   ┌─────────────────────────────────────┐      │
│   │ SSH into server   │──▶│ git clone / git pull repo           │      │
│   │ with credentials  │   │ into home directory (~/)            │      │
│   └───────────────────┘   └─────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────┘
```

### Quick Reference: Path Concepts

Before you begin, review these essential concepts:

| Concept | Symbol | Meaning |
|---|---|---|
| Root directory | `/` | The top-most directory in the filesystem |
| Home directory | `~` | Shorthand for `/home/<username>` |
| Current directory | `.` | The directory you are currently in |
| Parent directory | `..` | One level above the current directory |
| Previous directory | `cd -` | Return to the last directory you were in |
| Absolute path | Starts with `/` | Full path from root (e.g., `/home/alex/docs`) |
| Relative path | Does **not** start with `/` | Path relative to current location (e.g., `docs/report`) |

---

## Task 1 — Basic Navigation Warm-Up

**Scenario:** It's your very first time opening a terminal on the TechCorp server. Before doing anything else, your senior colleague says: *"Let me see you move around the filesystem. Show me where you are, what's in this directory, and that you can go to a few places and come back."*

**Purpose:** Get comfortable with the three most fundamental navigation commands: `cd`, `pwd`, and `ls`.

**Commands Used:**

- `pwd` — print working directory (shows where you are)
- `ls` — list what is in the current directory
- `cd` — change to a different directory

**Instructions:**

1. Check where you currently are:

   ```bash
   pwd
   ```

2. List the contents of your current directory:

   ```bash
   ls
   ```

3. Go to your home directory and confirm:

   ```bash
   cd ~
   pwd > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task1_basic_navigation.txt
   ```

4. List the files and folders in your home directory (including hidden files):

   ```bash
   ls -la >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task1_basic_navigation.txt
   ```

5. Go to the root directory and list its contents:

   ```bash
   cd /
   echo "--- Root directory (/) ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task1_basic_navigation.txt
   pwd >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task1_basic_navigation.txt
   ls >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task1_basic_navigation.txt
   ```

6. Go back to your home directory using `~`, then verify:

   ```bash
   cd ~
   echo "--- Back to home ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task1_basic_navigation.txt
   pwd >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task1_basic_navigation.txt
   ```

7. Return to your lab2 working directory:

   ```bash
   cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2
   ```

**Output File:** `task1_basic_navigation.txt`

---

## Task 2 — Exploring the File System

**Scenario:** Now that you know the basics, your manager asks: *"Before we set anything up, explore the key directories on this server and document what you find. I want you to understand the Linux directory layout."*

**Purpose:** Understand the Linux directory hierarchy by navigating to and inspecting key system directories.

**Commands Used:**

- `cd` — change directory (with absolute paths)
- `pwd` — print working directory
- `ls -la` — list all files including hidden ones, in long format
- `~` — home directory shortcut

**Instructions:**

1. Start from the **root** of the filesystem and list its contents:

   ```bash
   cd /
   pwd > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task2_filesystem_exploration.txt
   ls -la >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task2_filesystem_exploration.txt
   ```

2. Navigate to the `/etc` directory (system configuration files) and record its contents:

   ```bash
   cd /etc
   echo "--- /etc ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task2_filesystem_exploration.txt
   pwd >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task2_filesystem_exploration.txt
   ls >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task2_filesystem_exploration.txt
   ```

3. Navigate to the `/var` directory (variable data — logs, caches) and record:

   ```bash
   cd /var
   echo "--- /var ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task2_filesystem_exploration.txt
   pwd >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task2_filesystem_exploration.txt
   ls >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task2_filesystem_exploration.txt
   ```

4. Navigate to the `/home` directory and record all user directories:

   ```bash
   cd /home
   echo "--- /home ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task2_filesystem_exploration.txt
   pwd >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task2_filesystem_exploration.txt
   ls -la >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task2_filesystem_exploration.txt
   ```

5. Navigate to the `/tmp` directory (temporary files) and record:

   ```bash
   cd /tmp
   echo "--- /tmp ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task2_filesystem_exploration.txt
   pwd >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task2_filesystem_exploration.txt
   ls -la >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task2_filesystem_exploration.txt
   ```

6. Return to your home directory and back to the lab2 folder:

   ```bash
   cd ~
   echo "--- Home (~) ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task2_filesystem_exploration.txt
   pwd >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task2_filesystem_exploration.txt
   cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2
   ```

**Output File:** `task2_filesystem_exploration.txt`

---

## Task 3 — Building the Company Directory Structure

**Scenario:** Your manager hands you a plan for TechCorp's shared file server. You need to create the entire directory structure for three departments — **HR**, **Engineering**, and **Marketing** — each with their own subdirectories and placeholder files.

**Purpose:** Practice creating multi-level directory trees using `mkdir -p`, and populating them with files using `touch` and `echo`.

**Commands Used:**

- `mkdir -p` — create nested directories in one command
- `touch` — create empty files
- `echo` — write text into files (with `>` redirection)
- `tree` or `ls -R` — verify the complete structure

**Instructions:**

1. Create the entire directory tree in a single command:

   ```bash
   mkdir -p techcorp/{hr/{policies,onboarding},engineering/{frontend,backend,devops},marketing/{campaigns,assets}}
   ```

2. Navigate into the HR department and create policy documents:

   ```bash
   cd techcorp/hr/policies
   echo "TechCorp Leave Policy - Effective 2026" > leave_policy.txt
   echo "TechCorp Remote Work Guidelines" > remote_work.txt
   ```

3. Move to onboarding and create a welcome file:

   ```bash
   cd ../onboarding
   echo "Welcome to TechCorp! Please review all HR policies." > welcome_guide.txt
   touch checklist.txt
   ```

4. Navigate to the Engineering department and create project files:

   ```bash
   cd ../../engineering/frontend
   echo "React App - Version 3.2.1" > app_config.txt
   touch index.html styles.css

   cd ../backend
   echo "API Server - Node.js v20 LTS" > server_config.txt
   touch app.js database.sql

   cd ../devops
   echo "CI/CD Pipeline Configuration" > pipeline.txt
   touch Dockerfile docker-compose.yml
   ```

5. Navigate to the Marketing department and create campaign files:

   ```bash
   cd ../../marketing/campaigns
   echo "Q1 2026 Product Launch Campaign" > q1_launch.txt
   echo "Social Media Strategy - March 2026" > social_media.txt

   cd ../assets
   touch logo.png banner.jpg brochure.pdf
   ```

6. Return to the lab2 directory and record the entire structure:

   ```bash
   cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2
   tree techcorp > task3_directory_structure.txt
   ```

   > If `tree` is not installed, use `ls -R techcorp` instead, or install it with `sudo apt-get install tree -y`.

**Output File:** `task3_directory_structure.txt`

---

## Task 4 — Navigating with Absolute and Relative Paths

**Scenario:** You need to quickly navigate between departments to check on files. Your manager challenges you: *"Can you get to any folder on this server using both absolute and relative paths? Show me."*

**Purpose:** Demonstrate mastery of absolute paths, relative paths, `..` (parent), `.` (current), and `cd -` (previous directory).

**Commands Used:**

- `cd` — change directory (absolute and relative)
- `pwd` — confirm current location
- `..` — parent directory shortcut
- `cd -` — return to previous directory

**Instructions:**

1. Start from your lab2 directory and set up the output file:

   ```bash
   cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2
   echo "=== Task 4: Navigation with Paths ===" > task4_navigation_paths.txt
   ```

2. **Navigate using an absolute path** to the HR policies folder:

   ```bash
   cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/techcorp/hr/policies
   echo "--- Absolute path to HR/policies ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   pwd >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   ls >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   ```

3. **Use `..` to go up** to the `hr` directory, then **use a relative path** to move to `onboarding`:

   ```bash
   cd ..
   echo "--- Up to hr/ ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   pwd >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt

   cd onboarding
   echo "--- Relative path to onboarding/ ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   pwd >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   ls >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   ```

4. **Navigate sideways** from `onboarding` to `engineering/frontend` using `..`:

   ```bash
   cd ../../engineering/frontend
   echo "--- Sideways to engineering/frontend/ ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   pwd >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   ls >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   ```

5. **Go up two levels** to the `techcorp` root:

   ```bash
   cd ../..
   echo "--- Up two levels to techcorp/ ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   pwd >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   ```

6. **Use an absolute path** to jump to `marketing/campaigns`:

   ```bash
   cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/techcorp/marketing/campaigns
   echo "--- Absolute path to marketing/campaigns/ ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   pwd >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   ls >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   ```

7. **Use `cd -`** to return to the previous directory (`techcorp`):

   ```bash
   cd -
   echo "--- cd - (back to previous directory) ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   pwd >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task4_navigation_paths.txt
   ```

8. Return to the lab2 directory:

   ```bash
   cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2
   ```

### 🧩 Challenge — Navigate on Your Own

The steps below tell you **what to achieve**, but not the exact commands. Figure out the right `cd` command for each one. Record your `pwd` after each navigation.

> **Tip:** Think about whether you need an absolute path, a relative path, or a shortcut like `..` or `cd -`.

```bash
echo "--- Challenge Navigation ---" >> task4_navigation_paths.txt
```

**Starting position:** You are in your `lab2` directory.

8a. Navigate to `techcorp/engineering/backend` using a **relative path**. Record `pwd`.

8b. From `backend`, navigate to `techcorp/marketing/assets` using **only `..` shortcuts** (no absolute paths). Record `pwd`.

8c. From `assets`, jump to `/usr/bin` using an **absolute path**. Record `pwd`.

8d. From `/usr/bin`, return to the directory you were in before (hint: one of the shortcuts from the Quick Reference table). Record `pwd`.

8e. From wherever you are now, navigate to `techcorp/hr/onboarding` using **any method you choose**. Record `pwd` and list the files.

> Append all your results to `task4_navigation_paths.txt`.

**Output File:** `task4_navigation_paths.txt`

---

## Task 5 — Organizing Files Across Directories

**Scenario:** After an intern's first day, several files ended up in the wrong folders. Your job is to fix the mess by copying, moving, and removing files across the TechCorp directory tree — all without leaving the terminal.

**Purpose:** Practice using `cp`, `mv`, and `rm` with relative paths that cross directory boundaries.

**Commands Used:**

- `cp` — copy files
- `mv` — move or rename files
- `rm` — remove files
- `cat` — display file contents
- `ls` — list directory contents

**Instructions:**

1. Start from the lab2 directory and set up the output file:

   ```bash
   cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2
   echo "=== Task 5: File Organization ===" > task5_file_organization.txt
   ```

2. **Simulate misplaced files:** Create some files in the wrong locations:

   ```bash
   echo "URGENT: Server maintenance scheduled for Friday" > techcorp/marketing/server_notice.txt
   echo "New Logo Design Brief" > techcorp/engineering/backend/logo_brief.txt
   touch techcorp/hr/policies/temp_debug.log
   echo "Employee Handbook v2.0" > techcorp/engineering/devops/handbook.txt
   ```

3. **Fix #1 — Move** the server notice from Marketing to DevOps (where it belongs):

   ```bash
   cd techcorp/marketing
   mv server_notice.txt ../engineering/devops/
   echo "--- Moved server_notice.txt to devops/ ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task5_file_organization.txt
   ls ../engineering/devops/ >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task5_file_organization.txt
   ```

4. **Fix #2 — Move** the logo brief from Backend to Marketing Assets:

   ```bash
   mv ../engineering/backend/logo_brief.txt assets/
   echo "--- Moved logo_brief.txt to marketing/assets/ ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task5_file_organization.txt
   ls assets/ >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task5_file_organization.txt
   ```

5. **Fix #3 — Remove** the debug log that doesn't belong in HR Policies:

   ```bash
   rm ../hr/policies/temp_debug.log
   echo "--- Removed temp_debug.log from policies/ ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task5_file_organization.txt
   ls ../hr/policies/ >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task5_file_organization.txt
   ```

6. **Fix #4 — Move** the employee handbook from DevOps to HR Onboarding:

   ```bash
   mv ../engineering/devops/handbook.txt ../hr/onboarding/
   echo "--- Moved handbook.txt to hr/onboarding/ ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task5_file_organization.txt
   ls ../hr/onboarding/ >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task5_file_organization.txt
   ```

7. **Copy** the leave policy to the onboarding folder so new hires can see it too:

   ```bash
   cp ../hr/policies/leave_policy.txt ../hr/onboarding/
   echo "--- Copied leave_policy.txt to onboarding/ ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task5_file_organization.txt
   ls ../hr/onboarding/ >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task5_file_organization.txt
   ```

8. **Rename** the Q1 campaign file to include the year:

   ```bash
   mv campaigns/q1_launch.txt campaigns/q1_2026_launch.txt
   echo "--- Renamed q1_launch.txt to q1_2026_launch.txt ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task5_file_organization.txt
   ls campaigns/ >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2/task5_file_organization.txt
   ```

9. Return to the lab2 directory and record the final structure:

   ```bash
   cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2
   echo "--- Final Structure ---" >> task5_file_organization.txt
   tree techcorp >> task5_file_organization.txt
   ```

### 🧩 Challenge — Fix It Yourself

Your manager discovers **more misplaced files**. This time you get only a description of the problem — no commands. Figure out the right commands yourself.

> **Tip:** You already know `cp`, `mv`, `rm`, and how to use relative paths with `../`. Apply what you learned above.

```bash
echo "--- Challenge File Organization ---" >> task5_file_organization.txt
```

**Starting position:** You are in your `lab2` directory.

9a. **A new file appeared in the wrong place.** Create a file called `security_audit.txt` with the content `"Annual Security Audit Report 2026"` inside `techcorp/hr/policies/`. Then **move** it to `techcorp/engineering/devops/` where it actually belongs. Record the contents of `devops/` to prove it's there.

9b. **Duplicate for backup.** Make a **copy** of `techcorp/engineering/devops/pipeline.txt` and place the copy in `techcorp/engineering/backend/` with the name `pipeline_backup.txt`. Record the contents of `backend/`.

9c. **Cleanup.** Someone created three junk files. Create them first, then delete them:
   - Create `techcorp/marketing/campaigns/draft1.tmp`
   - Create `techcorp/marketing/campaigns/draft2.tmp`
   - Create `techcorp/marketing/campaigns/old_notes.tmp`
   - Remove **all three `.tmp` files** in a single command. Record the contents of `campaigns/` to prove they're gone.

9d. **Rename for consistency.** Rename `techcorp/engineering/frontend/app_config.txt` to `frontend_config.txt` (keeping it in the same directory). Record the contents of `frontend/`.

> Append all your results to `task5_file_organization.txt`. Then record the final structure:
> ```bash
> echo "--- Final Challenge Structure ---" >> task5_file_organization.txt
> tree techcorp >> task5_file_organization.txt
> ```

**Output File:** `task5_file_organization.txt`

---

## Task 6 — Advanced Listing & Directory Audit

**Scenario:** Your manager says: *"We need a full audit of the file server before the IT review next week. I want to know the full tree, the largest files, the newest files, and I want the sizes in a readable format."*

**Purpose:** Use advanced `ls` flags to list, sort, and analyze directory contents.

**Commands Used:**

- `ls -R` — recursive listing (list all contents of all subdirectories)
- `ls -lS` — long listing sorted by file size (largest first)
- `ls -lt` — long listing sorted by modification time (newest first)
- `ls -lh` — long listing with human-readable file sizes
- `ls -rlS` — reverse sort by size (smallest first)
- `ls -rlt` — reverse sort by time (oldest first)

**Instructions:**

1. Start from the lab2 directory:

   ```bash
   cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab2
   echo "=== Task 6: Advanced Listing & Directory Audit ===" > task6_advanced_listing.txt
   ```

2. **Recursive listing** — show the complete contents of the `techcorp` tree:

   ```bash
   echo "--- Recursive Listing (ls -R) ---" >> task6_advanced_listing.txt
   ls -R techcorp >> task6_advanced_listing.txt
   ```

3. **Sort by file size** — find the largest files in the Engineering department:

   ```bash
   echo "" >> task6_advanced_listing.txt
   echo "--- Sort by Size: engineering/ (ls -lS) ---" >> task6_advanced_listing.txt
   ls -lS techcorp/engineering/frontend/ >> task6_advanced_listing.txt
   ls -lS techcorp/engineering/backend/ >> task6_advanced_listing.txt
   ls -lS techcorp/engineering/devops/ >> task6_advanced_listing.txt
   ```

4. **Sort by modification time** — see which files were changed most recently:

   ```bash
   echo "" >> task6_advanced_listing.txt
   echo "--- Sort by Time: techcorp/ (ls -lt) ---" >> task6_advanced_listing.txt
   ls -lt techcorp/hr/policies/ >> task6_advanced_listing.txt
   ls -lt techcorp/hr/onboarding/ >> task6_advanced_listing.txt
   ls -lt techcorp/marketing/campaigns/ >> task6_advanced_listing.txt
   ```

5. **Human-readable sizes** — display file sizes in KB, MB, and GB:

   ```bash
   echo "" >> task6_advanced_listing.txt
   echo "--- Human-Readable (ls -lh) ---" >> task6_advanced_listing.txt
   ls -lh techcorp/marketing/assets/ >> task6_advanced_listing.txt
   ls -lh techcorp/engineering/devops/ >> task6_advanced_listing.txt
   ```

6. **Reverse sort** — show smallest files first and oldest files first:

   ```bash
   echo "" >> task6_advanced_listing.txt
   echo "--- Reverse Sort by Size (ls -rlS) ---" >> task6_advanced_listing.txt
   ls -rlS techcorp/engineering/backend/ >> task6_advanced_listing.txt

   echo "" >> task6_advanced_listing.txt
   echo "--- Reverse Sort by Time (ls -rlt) ---" >> task6_advanced_listing.txt
   ls -rlt techcorp/hr/onboarding/ >> task6_advanced_listing.txt
   ```

7. **Combined flags** — recursive, human-readable, sorted by size:

   ```bash
   echo "" >> task6_advanced_listing.txt
   echo "--- Combined: Recursive + Human-Readable + Sort by Size (ls -lhRS) ---" >> task6_advanced_listing.txt
   ls -lhRS techcorp/ >> task6_advanced_listing.txt
   ```

### 🧩 Challenge — Investigate on Your Own

Your manager gives you a few more investigative questions. Only the goal is provided — **you** decide which `ls` options to use.

> **Hint:** Review the commands table at the top of this task. You may need to combine flags you haven't tried together yet.

```bash
echo "" >> task6_advanced_listing.txt
echo "--- Challenge Investigation ---" >> task6_advanced_listing.txt
```

6a. **Question:** *"Which file in `techcorp/hr/onboarding/` was modified most recently?"*
— Use the right `ls` options to show files sorted by modification time (newest first) with detailed info. Record the output.

6b. **Question:** *"Show me every single file inside `techcorp/marketing/`, including files in subdirectories, with their sizes in human-readable format."*
— Figure out which combination of flags for `ls` gives a recursive, long-format, human-readable listing. Record the output.

6c. **Question:** *"I want to see all files in `techcorp/engineering/devops/`, but I want the smallest files at the top."*
— Use the right flags to get a long listing sorted by size in reverse order. Record the output.

6d. **Question:** *"List all hidden files (files starting with `.`) in your home directory, sorted by size (largest first), with human-readable sizes."*
— Navigate to your home directory and figure out the `ls` command that shows hidden files, sorted by size, in human-readable format. Record the output.

> Append all your results to `task6_advanced_listing.txt`.

**Output File:** `task6_advanced_listing.txt`

---

## Final Submission: GitHub and VS Code Documentation

You have finished the terminal work. Now push your folder to GitHub and document it.

### Phase 1: Push Your Terminal Work to GitHub (From WSL)

1. Verify your folder structure with `tree`:

   ```bash
   cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>
   tree lab2
   ```

2. Commit and push your work:

   ```bash
   cd ~/os-se-<YourStudentID>
   git add .
   git commit -m "Completed Lab 2 — Navigation & File Management"
   git push
   ```

### Phase 2: Clone & Document in VS Code (From Host OS)

1. **Pull the latest code** to your host machine:

   ```bash
   cd OS-SE-<YourStudentID>
   git pull
   ```

2. **Open in VS Code** and navigate to the `lab2` folder.

3. **Add Images:** Inside the `lab2` folder, create a new folder called `images`. Drag and drop all screenshots into this `images` folder.

4. **Create README:** Inside the `lab2` folder, create a `README.md` file. Use the Lab 2 README template provided by your instructor. You can preview the file in VS Code by pressing <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>V</kbd>.

5. **Final Push:**

   ```bash
   git add .
   git commit -m "Added Lab 2 README report and screenshots"
   git push
   ```

### Phase 3: Pull Your Work to the Lab Server

1. **Connect to the server** using SSH:

   ```bash
   ssh <YourUsername>@<server-address>
   ```

2. **Pull latest changes:**

   ```bash
   cd ~/OS-SE-<YourStudentID>
   git pull
   ```

3. **Verify:**

   ```bash
   tree ~/OS-SE-<YourStudentID>/os-lab-<YourStudentID>/lab2
   ```

4. **Log out:**

   ```bash
   exit
   ```

**Submission:** Submit the link to your GitHub repository's `lab2` folder to your instructor via the course portal.

---

## Expected Folder Structure

After completing all tasks and documentation, your `lab2` folder should look like this:

```
os-lab-<YourStudentID>/
└── lab2/
    ├── README.md
    ├── images/
    │   ├── task1.png
    │   ├── task2.png
    │   ├── task3.png
    │   ├── task4.png
    │   ├── task5.png
    │   └── task6.png
    ├── task1_basic_navigation.txt
    ├── task2_filesystem_exploration.txt
    ├── task3_directory_structure.txt
    ├── task4_navigation_paths.txt
    ├── task5_file_organization.txt
    ├── task6_advanced_listing.txt
    └── techcorp/
        ├── hr/
        │   ├── policies/
        │   │   ├── leave_policy.txt
        │   │   └── remote_work.txt
        │   └── onboarding/
        │       ├── checklist.txt
        │       ├── handbook.txt
        │       ├── leave_policy.txt
        │       └── welcome_guide.txt
        ├── engineering/
        │   ├── frontend/
        │   │   ├── frontend_config.txt
        │   │   ├── index.html
        │   │   └── styles.css
        │   ├── backend/
        │   │   ├── server_config.txt
        │   │   ├── pipeline_backup.txt
        │   │   ├── app.js
        │   │   └── database.sql
        │   └── devops/
        │       ├── pipeline.txt
        │       ├── server_notice.txt
        │       ├── security_audit.txt
        │       ├── Dockerfile
        │       └── docker-compose.yml
        └── marketing/
            ├── campaigns/
            │   ├── q1_2026_launch.txt
            │   └── social_media.txt
            └── assets/
                ├── logo.png
                ├── banner.jpg
                ├── brochure.pdf
                └── logo_brief.txt
```

> **Tip:** Run `tree lab2` from your `os-lab-<YourStudentID>` directory to verify your structure matches the one above before submitting.
