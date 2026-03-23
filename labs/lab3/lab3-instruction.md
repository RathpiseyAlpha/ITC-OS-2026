# OS Lab 3 — Wildcards, Links, GRUB & Shared Libraries (Hands-on)

| | |
|---|---|
| **Course** | Operating Systems |
| **Lab Title** | Wildcards, Links, Boot Loader Exploration & Shared Libraries |
| **Chapter** | OS Structures & Bootstrap Process |
| **Duration** | 3 Hours |
| **Lab Type** | Individual + Pair (Task 5) |

---

> ⚠️ **IMPORTANT — READ EVERYTHING FIRST**
>
> **Before you type a single command, read through this ENTIRE document from top to bottom.** Scan every section — the tasks, the challenges, the deliverables, the folder structure, and the README template. Understand the full scope of what is expected **before** you start working. Students who skip ahead often miss requirements and waste time redoing work.
>
> **Document structure:**
> 1. **Lab Objectives** — What you'll learn
> 2. **Task Overview** — Summary of all tasks at a glance
> 3. **Lab Setup** — Repository and folder preparation
> 4. **Quick Reference Tables** — Command cheat sheets for each topic
> 5. **Tasks 1–4 (Required, Individual)** — Wildcards, Links, GRUB (exploration + customization + boot recovery), Shared objects
> 6. **Task 5 (Required, Pair)** — Create and register a custom shared library collaboratively
> 7. **Deliverables & Submission** — Folder structure, README template, git push
> 8. **Screenshot Checklist** — Every screenshot you need, in one place

---

## Quick Navigation

| Section | Jump To |
|---------|---------|
| Lab Objectives | [▶ Lab Objectives](#lab-objectives) |
| Task Overview | [▶ Task Overview](#task-overview) |
| Lab Setup | [▶ Lab Setup](#lab-setup) |
| Quick Reference | [▶ Quick Reference](#quick-reference-wildcards) |
| Task 1: Wildcards | [▶ Task 1](#task-1--mastering-wildcards) |
| Task 2: Links | [▶ Task 2](#task-2--hard-links-and-symbolic-links) |
| Task 3: GRUB (Explore + Customize + Recovery) | [▶ Task 3](#task-3--grub-exploration-customization--boot-recovery) |
| Task 4: Shared Objects | [▶ Task 4](#task-4--shared-objects-dynamic-libraries-exploration) |
| Task 5: Build a Shared Library (Pair) | [▶ Task 5](#task-5--build--register-a-shared-library-pair-task) |
| Submission | [▶ Submission](#final-submission-github-and-vs-code-documentation) |
| Screenshot Checklist | [▶ Screenshot Checklist](#screenshot-checklist) |

---

## Lab Objectives

After completing this lab, students will be able to:

1. Use wildcard characters (`*`, `?`, `[]`, `{}`) to match and manipulate groups of files efficiently.
2. Explain the difference between hard links and symbolic (soft) links.
3. Create, inspect, and manage both hard links and symbolic links.
4. Explore the GRUB bootloader configuration and understand the Linux boot sequence.
5. Customize the GRUB menu with a custom title, timeout, and background image.
6. Identify shared libraries (`.so` files) used by common Linux programs using `ldd` and `ldconfig`.
7. Understand how the dynamic linker resolves shared objects at runtime.
8. Create a custom shared library, compile it, install it, and register it with `ldconfig`.
9. Simulate a safe boot "break," enter rescue mode, and restore normal boot on a virtual machine.
10. Apply previously learned commands to solve new, unfamiliar problems independently.

> **Scenario:** You are **Alex**, now a few weeks into the junior sysadmin role at **TechCorp Inc.** Your manager says: *"Today I need you to do three things: clean up our server files efficiently using wildcards and links, audit our boot configuration, and verify that our critical applications have all their shared libraries intact. Also — we have a training VM I want you to practice emergency boot recovery on, in case a real server ever fails to start. And one more — you'll pair up with a teammate to write and install a custom shared library for our monitoring tools."*

---

## Task Overview

| Task | Title | Type | Environment | Key Commands | Output Files |
|:---:|-------|:----:|:-----------:|-------------|:------------:|
| **1** | Mastering Wildcards | Individual | WSL / Server | `*`, `?`, `[]`, `{}`, `ls`, `cp`, `rm` | `task1_wildcards.txt` |
| **2** | Hard Links & Symbolic Links | Individual | WSL / Server | `ln`, `ln -s`, `ls -li`, `stat`, `readlink` | `task2_links.txt` |
| **3** | GRUB: Explore, Customize & Recover | Individual | WSL + **VM** | `cat`, `dmesg`, `/etc/default/grub`, `update-grub`, GRUB CLI | `task3_grub.txt` + screenshots |
| **4** | Shared Objects Exploration | Individual | WSL / Server | `ldd`, `ldconfig -p`, `file`, `readelf` | `task4_shared_objects.txt` |
| **5** | Build a Shared Library | **Pair** | WSL / Server | `gcc -shared -fPIC`, `ldconfig`, `ldd` | `task5_shared_library.txt` |

---

## Lab Setup

Navigate into your existing lab submission repository and create the `lab3` directory:

```bash
cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>
mkdir lab3
cd lab3
```

### Documenting Your Work (Taking Screenshots)

Each task in this lab redirects its output into `.txt` files, which serve as your **primary proof of work** for the guided portions. You also need screenshots for challenges, VM tasks, and the pair task:

1. **Output Files (No Screenshots Needed for Guided Steps):** The guided steps in each task automatically save results to `.txt` files (e.g., `task1_wildcards.txt`). These files will be committed to your repository as proof of completion.
2. **Challenge Screenshots:** When you reach the 🧩 **Challenge** sections in Tasks 1, 2, 3, and 4, take a screenshot of your terminal showing the commands you used and their output.
3. **VM Screenshots (Task 3 Parts B & C):** GRUB customization and boot recovery involve the VM console/display, so they must be documented with screenshots.
4. **Pair Task Screenshot (Task 5):** Take screenshots showing the API design session and the integration test with both partners' work.
5. **Full History Screenshot:** After finishing all tasks, run `history | tail -n 100` and take a screenshot.
6. **Save All Images:** Save all screenshots to a folder on your host machine. You will add them to an `images/` folder in your `README.md` later.

> **See the [Screenshot Checklist](#screenshot-checklist) at the end of this document for the complete list of every screenshot you need.**

### Lab Workflow Overview

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          WSL / Linux Terminal                                │
│                                                                              │
│  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Task 1  │  │ Task 2  │  │ Task 3A  │  │ Task 4   │  │ Task 5   │        │
│  │Wildcards│─▶│  Links  │─▶│  GRUB    │─▶│ Shared   │─▶│ Build .so│        │
│  │         │  │         │  │ Explore  │  │ Objects  │  │  (Pair)  │        │
│  └─────────┘  └─────────┘  └─────┬────┘  └──────────┘  └────┬─────┘        │
│                                   │                           │              │
│                                   ▼                           ▼              │
│                            ┌─────────────┐             ┌───────────┐         │
│                            │ Continue to │             │ git push  │         │
│                            │ VM (3B, 3C) │             │ to GitHub │         │
│                            └──────┬──────┘             └─────┬─────┘         │
└───────────────────────────────────┼──────────────────────────┼───────────────┘
                                    │                          │
┌───────────────────────────────────┼──────────────────────────┘
│                                   ▼
│  ┌──────────────────────────────────────────────────────────────────────────┐
│  │                          VM (VirtualBox / VMware)                        │
│  │                                                                          │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐                             │
│  │  │ Task 3B  │──▶│ Task 3C  │──▶│ Challenge│                             │
│  │  │   GRUB   │   │Boot Break│   │  (GRUB)  │                             │
│  │  │Customize │   │& Recovery│   │          │                             │
│  │  └──────────┘   └──────────┘   └──────────┘                             │
│  └──────────────────────────────────────────────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         Host OS (Windows / Mac)                              │
│                                                                              │
│   ┌──────────────┐   ┌───────────────┐   ┌─────────────────────┐            │
│   │ Clone/Pull   │──▶│ Add Images &  │──▶│ Final git push      │            │
│   │ in VS Code   │   │ Write README  │   │ to GitHub           │            │
│   └──────────────┘   └───────────────┘   └──────────┬──────────┘            │
└──────────────────────────────────────────────────────┼───────────────────────┘
                                                       │
                                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         Local Lab Server (SSH)                               │
│                                                                              │
│   ┌───────────────────┐   ┌─────────────────────────────────────┐           │
│   │ SSH into server   │──▶│ git clone / git pull repo           │           │
│   │ with credentials  │   │ into home directory (~/)            │           │
│   └───────────────────┘   └─────────────────────────────────────┘           │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference: Wildcards

| Pattern | Symbol | Meaning | Example |
|---|---|---|---|
| Match any characters | `*` | Zero or more characters | `*.txt` → all `.txt` files |
| Match single character | `?` | Exactly one character | `file?.txt` → `file1.txt`, `fileA.txt` |
| Match character set | `[abc]` | One character from the set | `file[123].txt` → `file1.txt`, `file2.txt` |
| Match character range | `[a-z]` | One character in the range | `[A-Z]*.txt` → files starting A–Z |
| Negate set | `[!abc]` | Any character NOT in the set | `file[!0-9].txt` → `fileA.txt`, not `file1.txt` |
| Brace expansion | `{a,b,c}` | Generate multiple strings | `file.{txt,log}` → `file.txt file.log` |

## Quick Reference: Links

| Concept | Command | Meaning |
|---|---|---|
| Hard link | `ln <target> <link>` | Creates another name for the same inode (same data on disk) |
| Symbolic link | `ln -s <target> <link>` | Creates a pointer file that stores the target path |
| Show inodes | `ls -li` | Displays inode numbers alongside file listings |
| File info | `stat <file>` | Shows inode, link count, permissions, timestamps |
| Read link target | `readlink <link>` | Shows where a symbolic link points |
| Follow full chain | `readlink -f <link>` | Resolves all symlinks to the final real path |

## Quick Reference: GRUB & Boot

| Concept | Command / File | Meaning |
|---|---|---|
| Current kernel | `uname -r` | Print the running kernel version |
| Boot messages | `dmesg` | Display kernel ring buffer (boot log) |
| GRUB config (auto) | `/boot/grub/grub.cfg` | Auto-generated — **never edit directly** |
| GRUB defaults | `/etc/default/grub` | The file admins edit to change boot behavior |
| Regenerate GRUB | `sudo update-grub` | Rebuilds `grub.cfg` from scripts + defaults |
| GRUB scripts | `/etc/grub.d/` | Individual scripts that generate menu entries |
| Kernel image | `/boot/vmlinuz-*` | The compressed Linux kernel |
| Initial ramdisk | `/boot/initrd.img-*` | Temporary root FS loaded before real root |

## Quick Reference: Shared Libraries

| Concept | Command | Meaning |
|---|---|---|
| List dependencies | `ldd <binary>` | Show shared libraries a program needs |
| Library cache | `ldconfig -p` | List all cached shared libraries |
| Refresh cache | `sudo ldconfig` | Rebuild `/etc/ld.so.cache` after adding libraries |
| Linker config | `/etc/ld.so.conf` | Main config for library search paths |
| Extra paths | `/etc/ld.so.conf.d/` | Drop-in configs for additional library paths |
| File type | `file <path>` | Identify whether a file is ELF, shared object, etc. |
| ELF headers | `readelf -h <binary>` | Examine ELF binary headers |
| Memory maps | `cat /proc/$$/maps` | Show memory-mapped files for current process |
| Compile shared lib | `gcc -shared -fPIC` | Build a `.so` shared object from C source |

---

## Task 1 — Mastering Wildcards

**Scenario:** The TechCorp server has accumulated hundreds of files across departments. Your manager says: *"We need you to search, list, copy, and clean up files efficiently. Typing each filename one by one is NOT acceptable. Use wildcards."*

**Purpose:** Learn to use shell wildcard patterns (`*`, `?`, `[]`, `{}`) to select and manipulate groups of files with a single command.

**Commands Used:**

- `*` — matches zero or more characters
- `?` — matches exactly one character
- `[...]` — matches one character from a set or range
- `{...}` — brace expansion to generate multiple patterns
- `ls`, `cp`, `mv`, `rm` — file operations with wildcards

**Instructions:**

1. Create a playground directory with a variety of files:

   ```bash
   mkdir -p wildcard_lab
   cd wildcard_lab

   # Create files with different extensions
   touch report01.txt report02.txt report03.txt report10.txt
   touch summary.txt notes.txt readme.txt
   touch data01.csv data02.csv data03.csv
   touch image1.png image2.png image3.jpg image4.jpg
   touch log_jan.log log_feb.log log_mar.log log_apr.log
   touch config.yaml config.yml settings.json
   touch backup1.tar.gz backup2.tar.gz
   touch temp1.tmp temp2.tmp temp3.tmp
   echo "=== Task 1: Wildcards ===" > ../task1_wildcards.txt
   ```

2. **Star wildcard (`*`)** — match any number of characters:

   ```bash
   echo "--- All .txt files ---" >> ../task1_wildcards.txt
   ls *.txt >> ../task1_wildcards.txt

   echo "--- All files starting with 'report' ---" >> ../task1_wildcards.txt
   ls report* >> ../task1_wildcards.txt

   echo "--- All files starting with 'log_' ---" >> ../task1_wildcards.txt
   ls log_* >> ../task1_wildcards.txt
   ```

3. **Question mark (`?`)** — match exactly one character:

   ```bash
   echo "--- Files matching 'data0?.csv' (single digit) ---" >> ../task1_wildcards.txt
   ls data0?.csv >> ../task1_wildcards.txt

   echo "--- Files matching 'image?.png' ---" >> ../task1_wildcards.txt
   ls image?.png >> ../task1_wildcards.txt

   echo "--- Files matching 'temp?.tmp' ---" >> ../task1_wildcards.txt
   ls temp?.tmp >> ../task1_wildcards.txt
   ```

4. **Square brackets (`[]`)** — match a set or range of characters:

   ```bash
   echo "--- Files matching 'report0[1-3].txt' (reports 01 to 03 only) ---" >> ../task1_wildcards.txt
   ls report0[1-3].txt >> ../task1_wildcards.txt

   echo "--- Files matching 'image[1-2].*' ---" >> ../task1_wildcards.txt
   ls image[1-2].* >> ../task1_wildcards.txt

   echo "--- Files matching 'log_[jfm]*.log' (months starting with j, f, or m) ---" >> ../task1_wildcards.txt
   ls log_[jfm]*.log >> ../task1_wildcards.txt
   ```

5. **Negated set (`[!...]`)** — match anything NOT in the set:

   ```bash
   echo "--- .log files NOT starting with 'log_j' (not January) ---" >> ../task1_wildcards.txt
   ls log_[!j]*.log >> ../task1_wildcards.txt
   ```

6. **Brace expansion (`{}`)** — generate multiple patterns:

   ```bash
   echo "--- List both .yaml and .yml files using braces ---" >> ../task1_wildcards.txt
   ls config.{yaml,yml} >> ../task1_wildcards.txt

   echo "--- List all image files (.png and .jpg) using braces ---" >> ../task1_wildcards.txt
   ls *.{png,jpg} >> ../task1_wildcards.txt
   ```

7. **Wildcards with commands** — copy and clean up using patterns:

   ```bash
   # Copy all CSV files to a new directory
   mkdir -p ../csv_archive
   cp *.csv ../csv_archive/
   echo "--- Copied CSV files to csv_archive/ ---" >> ../task1_wildcards.txt
   ls ../csv_archive/ >> ../task1_wildcards.txt

   # Remove all .tmp files in one command
   rm *.tmp
   echo "--- After removing all .tmp files ---" >> ../task1_wildcards.txt
   ls >> ../task1_wildcards.txt
   ```

8. Return to the lab3 directory:

   ```bash
   cd ..
   ```

### 🧩 Challenge — Wildcards on Your Own

Your manager gives you additional file management tasks. Only the goal is described — you decide the commands.

```bash
echo "--- Challenge Wildcards ---" >> task1_wildcards.txt
```

**Starting position:** You are in your `lab3` directory.

1a. **List all `.txt` files inside `wildcard_lab/` whose names start with `r`** (e.g., `report01.txt`, `readme.txt`). Record the output.

1b. **List only files in `wildcard_lab/` that have exactly a single character between `image` and the file extension** (i.e., `image1.png`, `image2.png`, `image3.jpg`, `image4.jpg` — but NOT a file like `image10.png` if it existed). Record the output.

1c. **Create 5 new files in one command** using brace expansion: `memo_{mon,tue,wed,thu,fri}.txt` inside `wildcard_lab/`. Then list only the `memo_*.txt` files to confirm. Record the output.

1d. **Remove all `.log` files from `wildcard_lab/`** in a single command. List the remaining files to prove they are gone. Record the output.

> Append all your results to `task1_wildcards.txt`.

**Output File:** `task1_wildcards.txt`

---

## Task 2 — Hard Links and Symbolic Links

**Scenario:** Your manager explains: *"We have configuration files that multiple departments need to access. Instead of making copies everywhere (which get out of sync), we use links. I need you to understand the difference between hard links and symbolic links — this is critical for server administration."*

**Purpose:** Understand and practice creating hard links and symbolic links, and observe how they differ in behavior when the original file is modified, moved, or deleted.

**Commands Used:**

- `ln <target> <link_name>` — create a hard link
- `ln -s <target> <link_name>` — create a symbolic (soft) link
- `ls -li` — list files with inode numbers
- `readlink` — display the target of a symbolic link
- `stat` — display detailed file information (inode, link count, etc.)
- `find -inum` — find files by inode number

> **Key Concept — Inodes:**
> Every file on a Linux filesystem is identified by an **inode** (index node) — a unique number that stores the file's metadata (permissions, owner, size, disk location). The filename is just a label (directory entry) pointing to the inode.
>
> - A **hard link** is an additional directory entry pointing to the **same inode**. The file's data exists once, but it has multiple names. Deleting one name does not remove the data — it persists until *all* hard links are removed.
> - A **symbolic link** is a separate file (with its own inode) that stores the **path** to the target file. If the original file is moved or deleted, the symbolic link **breaks** (becomes a "dangling" link).

**Instructions:**

1. Create a workspace with an original file:

   ```bash
   mkdir -p links_lab
   cd links_lab
   echo "=== Task 2: Hard Links and Symbolic Links ===" > ../task2_links.txt

   echo "TechCorp Global Configuration v3.1" > config_original.txt
   echo "--- Original file ---" >> ../task2_links.txt
   ls -li config_original.txt >> ../task2_links.txt
   cat config_original.txt >> ../task2_links.txt
   ```

2. **Create a hard link** to the original file:

   ```bash
   ln config_original.txt config_hardlink.txt
   echo "" >> ../task2_links.txt
   echo "--- After creating hard link ---" >> ../task2_links.txt
   ls -li config_original.txt config_hardlink.txt >> ../task2_links.txt
   ```

   > **Observe:** Both files share the **same inode number** and the link count is now **2**.

3. **Create a symbolic link** to the original file:

   ```bash
   ln -s config_original.txt config_symlink.txt
   echo "" >> ../task2_links.txt
   echo "--- After creating symbolic link ---" >> ../task2_links.txt
   ls -li config_original.txt config_hardlink.txt config_symlink.txt >> ../task2_links.txt
   ```

   > **Observe:** The symbolic link has a **different inode number** and shows `->` pointing to the original file.

4. **Verify both links read the same content:**

   ```bash
   echo "" >> ../task2_links.txt
   echo "--- Content via hard link ---" >> ../task2_links.txt
   cat config_hardlink.txt >> ../task2_links.txt
   echo "--- Content via symbolic link ---" >> ../task2_links.txt
   cat config_symlink.txt >> ../task2_links.txt
   ```

5. **Modify the original file and check both links:**

   ```bash
   echo "Updated: New security patch applied." >> config_original.txt
   echo "" >> ../task2_links.txt
   echo "--- After modifying original ---" >> ../task2_links.txt
   echo "Hard link content:" >> ../task2_links.txt
   cat config_hardlink.txt >> ../task2_links.txt
   echo "Symlink content:" >> ../task2_links.txt
   cat config_symlink.txt >> ../task2_links.txt
   ```

   > **Observe:** Both links reflect the change because (a) the hard link shares the same inode data, and (b) the symlink follows the path to the same file.

6. **Delete the original file and observe the difference:**

   ```bash
   rm config_original.txt
   echo "" >> ../task2_links.txt
   echo "--- After deleting original file ---" >> ../task2_links.txt
   echo "Hard link still works:" >> ../task2_links.txt
   cat config_hardlink.txt >> ../task2_links.txt
   echo "Symlink is broken:" >> ../task2_links.txt
   cat config_symlink.txt >> ../task2_links.txt 2>&1
   ls -li config_hardlink.txt config_symlink.txt >> ../task2_links.txt 2>&1
   ```

   > **Observe:** The hard link **still works** because the data persists as long as at least one link to the inode exists. The symbolic link is now **broken** — it points to a path that no longer exists.

7. **Inspect link details with `stat`:**

   ```bash
   echo "" >> ../task2_links.txt
   echo "--- stat on hard link ---" >> ../task2_links.txt
   stat config_hardlink.txt >> ../task2_links.txt
   echo "--- readlink on symlink ---" >> ../task2_links.txt
   readlink config_symlink.txt >> ../task2_links.txt
   ```

8. **Symbolic links to directories:**

   ```bash
   mkdir -p projects/frontend
   echo "index.html placeholder" > projects/frontend/index.html
   ln -s projects/frontend web_shortcut
   echo "" >> ../task2_links.txt
   echo "--- Symlink to directory ---" >> ../task2_links.txt
   ls -ld web_shortcut >> ../task2_links.txt
   ls web_shortcut/ >> ../task2_links.txt
   ```

9. **Explore real-world symlinks on the system:**

   ```bash
   echo "" >> ../task2_links.txt
   echo "--- Real-world symlinks in /usr/bin ---" >> ../task2_links.txt
   ls -la /usr/bin/python* >> ../task2_links.txt 2>&1
   ls -la /usr/bin/editor >> ../task2_links.txt 2>&1
   echo "--- Symlinks in /etc/alternatives ---" >> ../task2_links.txt
   ls -la /etc/alternatives/ | head -20 >> ../task2_links.txt
   ```

10. Return to the lab3 directory:

    ```bash
    cd ..
    ```

### 🧩 Challenge — Links on Your Own

```bash
echo "--- Challenge Links ---" >> task2_links.txt
```

**Starting position:** You are in your `lab3` directory.

2a. **Create a file** called `shared_data.txt` inside `links_lab/` with the content `"Shared resource across departments"`. Create **two hard links** to it: `hr_data.txt` and `eng_data.txt` (inside the same directory). Use `ls -li` to show that all three files share the same inode. Record the output.

2b. **Create a symbolic link** called `quick_access` in your `lab3/` directory that points to `links_lab/projects/frontend/`. Verify you can `ls quick_access/` and see `index.html`. Record the output.

2c. **Test your understanding.** Delete `shared_data.txt` (the original). Can you still read `hr_data.txt`? Can you still read `eng_data.txt`? Try both and record whether they still work. What does `ls -li` show for the link count now?

> Append all your results to `task2_links.txt`.

**Output File:** `task2_links.txt`

---

## Task 3 — GRUB: Exploration, Customization & Boot Recovery

**Scenario:** A senior engineer tells you: *"Every sysadmin needs to understand how Linux boots. If a server can't boot, nothing else matters. I need you to first read and understand our GRUB configuration, then customize the boot menu on our training VM so it's branded for TechCorp, and finally practice emergency boot recovery — because if a production server can't start, you need to know how to fix it WITHOUT reinstalling the OS."*

**Purpose:** Explore the GRUB (GRand Unified Bootloader) configuration, customize the boot menu, and practice emergency recovery. This task covers the full lifecycle of bootloader administration — from reading and understanding, to modifying, to breaking and fixing. It connects directly to the **Bootstrap Process** concept from Week 1 lectures.

> **Background — The Linux Boot Sequence:**
>
> ```
>  ┌──────────┐    ┌─────────┐    ┌──────────┐    ┌─────────┐    ┌──────────┐
>  │  BIOS /  │───▶│  GRUB   │───▶│  Kernel  │───▶│  init / │───▶│  Login   │
>  │  UEFI    │    │ Stage 1 │    │  Loads   │    │ systemd │    │  Prompt  │
>  │ (POST)   │    │ & 2     │    │          │    │         │    │          │
>  └──────────┘    └─────────┘    └──────────┘    └─────────┘    └──────────┘
>       │               │               │               │               │
>   Hardware        Boot loader      Kernel init     System services  User space
>   self-test       loads kernel     & mount root    start up         ready
> ```
>
> 1. **BIOS/UEFI** performs a Power-On Self Test (POST) and finds the boot device.
> 2. **GRUB** (the bootloader) loads from the boot device, presents a menu, and loads the selected kernel into memory.
> 3. **The kernel** initializes hardware, mounts the root filesystem, and starts the first process.
> 4. **init/systemd** starts all system services in the correct order.
> 5. The **login prompt** appears — the system is ready for use.

**Commands Used:**

- `cat` / `less` — view file contents
- `ls` — list directory contents
- `uname -r` — display current kernel version
- `dmesg` — display kernel boot messages
- `vi` or `nano` — text editor
- `/etc/default/grub` — main GRUB defaults file
- `/etc/grub.d/` — custom menu scripts directory
- `sudo update-grub` — regenerate `grub.cfg`
- VM snapshot tools (VirtualBox: `Snapshots` panel)
- GRUB command line (`grub>`) — manual boot commands
- `mount`, `chroot` — repair commands in rescue mode
- `grub-install`, `update-grub` — reinstall/reconfigure GRUB

---

### Part A — Bootloader Exploration (WSL / Server)

**Instructions:**

1. Start the output file and identify the currently running kernel:

   ```bash
   echo "=== Task 3: GRUB Bootloader Exploration ===" > task3_grub.txt
   echo "--- Current kernel version ---" >> task3_grub.txt
   uname -r >> task3_grub.txt
   ```

2. **Examine the GRUB configuration directory:**

   ```bash
   echo "" >> task3_grub.txt
   echo "--- GRUB directory listing ---" >> task3_grub.txt
   ls -la /boot/grub/ >> task3_grub.txt 2>&1
   ```

3. **Read the main GRUB configuration file:**

   ```bash
   echo "" >> task3_grub.txt
   echo "--- GRUB config (/boot/grub/grub.cfg) - first 60 lines ---" >> task3_grub.txt
   head -60 /boot/grub/grub.cfg >> task3_grub.txt 2>&1
   ```

   > **Note:** `grub.cfg` is auto-generated. You should **never** edit it directly. Changes are made via `/etc/default/grub`.

4. **Read the GRUB defaults file** (the file administrators actually edit):

   ```bash
   echo "" >> task3_grub.txt
   echo "--- GRUB defaults (/etc/default/grub) ---" >> task3_grub.txt
   cat /etc/default/grub >> task3_grub.txt 2>&1
   ```

   > **Key settings to understand:**
   >
   > | Setting | Meaning |
   > |---|---|
   > | `GRUB_DEFAULT` | Which menu entry to boot by default (0 = first) |
   > | `GRUB_TIMEOUT` | Seconds to wait at GRUB menu before auto-booting |
   > | `GRUB_CMDLINE_LINUX_DEFAULT` | Kernel parameters for normal boot (e.g., `quiet splash`) |
   > | `GRUB_CMDLINE_LINUX` | Kernel parameters applied to ALL boot entries |

5. **List installed kernels on the system:**

   ```bash
   echo "" >> task3_grub.txt
   echo "--- Installed kernels in /boot ---" >> task3_grub.txt
   ls -lh /boot/vmlinuz* >> task3_grub.txt 2>&1
   ls -lh /boot/initrd* >> task3_grub.txt 2>&1
   ```

   > **Concepts:**
   > - `vmlinuz` — the compressed Linux kernel image
   > - `initrd` / `initramfs` — the initial RAM disk, a temporary root filesystem loaded into memory to help the kernel boot before the real root filesystem is available

6. **Examine early boot messages with `dmesg`:**

   ```bash
   echo "" >> task3_grub.txt
   echo "--- Early kernel boot messages (first 40 lines) ---" >> task3_grub.txt
   dmesg | head -40 >> task3_grub.txt 2>&1
   ```

7. **Examine the boot scripts directory:**

   ```bash
   echo "" >> task3_grub.txt
   echo "--- GRUB scripts in /etc/grub.d/ ---" >> task3_grub.txt
   ls -la /etc/grub.d/ >> task3_grub.txt 2>&1
   ```

   > These scripts are run by `grub-mkconfig` to build the final `grub.cfg`. Each script handles a different part of the menu (e.g., `10_linux` adds Linux entries, `30_os-prober` detects other operating systems).

---

### Part B — GRUB Customization (VM Only)

> ⚠️ **This part and Part C must be performed only on a virtual machine** (VirtualBox, VMware, or a cloud VM). **Never** perform these steps on a physical machine or your primary development system.

#### Step 1 — Take a VM Snapshot (Safety Net)

Before making any changes to the VM, create a snapshot so you can always restore it:

- **VirtualBox:** Machine → Take Snapshot → Name it `"Before Boot Lab"`
- **VMware:** VM → Snapshot → Take Snapshot

> 📸 **Screenshot `task3_snapshot.png`:** Take a screenshot showing your snapshot has been created.

#### Step 2 — Change the GRUB Timeout

1. Open the GRUB defaults file:

   ```bash
   sudo nano /etc/default/grub
   ```

2. Find the `GRUB_TIMEOUT` line and change it to show the menu for **10 seconds**:

   ```
   GRUB_TIMEOUT=10
   ```

3. Also find `GRUB_CMDLINE_LINUX_DEFAULT` — remove `quiet splash` temporarily so you can see boot messages:

   ```
   GRUB_CMDLINE_LINUX_DEFAULT=""
   ```

4. Save the file and regenerate the GRUB configuration:

   ```bash
   sudo update-grub
   ```

5. Record what you changed:

   ```bash
   echo "" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task3_grub.txt
   echo "=== Part B: GRUB Customization ===" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task3_grub.txt
   echo "--- Modified /etc/default/grub ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task3_grub.txt
   cat /etc/default/grub >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task3_grub.txt
   ```

> 📸 **Screenshot `task3_timeout.png`:** Take a screenshot showing the modified `/etc/default/grub`.

#### Step 3 — Add a Custom GRUB Menu Entry

Custom menu entries are added by creating a script in `/etc/grub.d/`. Scripts are numbered (e.g., `10_linux`, `30_os-prober`) and executed in order when `update-grub` runs.

1. Create a custom entry script:

   ```bash
   sudo nano /etc/grub.d/40_custom_techcorp
   ```

2. Add the following content:

   ```bash
   #!/bin/sh
   exec tail -n +3 $0
   # Custom GRUB menu entry for TechCorp Training VM

   menuentry "TechCorp Training VM — Boot Standard" {
       set root=(hd0,msdos1)
       linux /boot/vmlinuz-$(uname -r) root=/dev/sda1
       initrd /boot/initrd.img-$(uname -r)
   }
   ```

   > **Note:** Adjust `(hd0,msdos1)` and `/dev/sda1` to match your VM's partition layout — you will discover the correct values in Part C, Step 5. Replace `$(uname -r)` with the actual kernel version string if the script does not expand it correctly.

3. Make the script executable and regenerate GRUB:

   ```bash
   sudo chmod +x /etc/grub.d/40_custom_techcorp
   sudo update-grub
   ```

4. Record the new menu:

   ```bash
   echo "" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task3_grub.txt
   echo "--- Custom script /etc/grub.d/40_custom_techcorp ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task3_grub.txt
   cat /etc/grub.d/40_custom_techcorp >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task3_grub.txt
   ```

5. Reboot and verify the new entry appears in the GRUB menu:

   ```bash
   sudo reboot
   ```

> 📸 **Screenshot `task3_custom_entry.png`:** Take a screenshot of the GRUB menu showing your custom "TechCorp Training VM" entry.

#### Step 4 — Add a GRUB Background Image

GRUB supports custom background images in `png`, `tga`, or `jpg` format. The image should ideally be **640×480** for the best compatibility. Here is how to set one:

1. After booting, install the GRUB splash tool (if not already installed):

   ```bash
   sudo apt install grub2-splashimages 2>/dev/null || echo "Package not available — using custom image"
   ```

2. **Option A — Use a pre-installed splash image (if available):**

   ```bash
   ls /usr/share/images/grub/ 2>/dev/null
   ```

   If images exist, copy one:

   ```bash
   sudo cp /usr/share/images/grub/<image_name>.tga /boot/grub/splash.tga
   ```

   **Option B — Create a simple custom image with ImageMagick:**

   ```bash
   sudo apt install imagemagick -y 2>/dev/null
   convert -size 640x480 xc:'#1a1a2e' \
     -fill white -gravity center -pointsize 36 \
     -annotate +0+0 'TechCorp Server' \
     /tmp/grub_bg.png
   sudo cp /tmp/grub_bg.png /boot/grub/grub_bg.png
   ```

   **Option C — Use any `.png` image you have** (transfer it to your VM via shared folders or `scp`). Resize it to 640×480 if it's larger.

3. Tell GRUB to use a background image by editing the defaults:

   ```bash
   sudo nano /etc/default/grub
   ```

   Add or modify the following line (use the correct filename from above):

   ```
   GRUB_BACKGROUND="/boot/grub/grub_bg.png"
   ```

4. Regenerate and reboot:

   ```bash
   sudo update-grub
   sudo reboot
   ```

5. Record the final configuration:

   ```bash
   echo "" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task3_grub.txt
   echo "--- Final /etc/default/grub (with background) ---" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task3_grub.txt
   cat /etc/default/grub >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task3_grub.txt
   ```

> 📸 **Screenshot `task3_background.png`:** Take a screenshot of the GRUB menu showing the custom background image.

---

### Part C — Boot Break & Recovery (VM Only)

> **Background — Linux Recovery Modes:**
>
> | Mode | How to Enter | What It Does |
> |---|---|---|
> | **Recovery Mode** | Select from GRUB menu → "Advanced options" → "(recovery mode)" | Boots into single-user mode with limited services; root shell access |
> | **GRUB Command Line** | Press `c` at the GRUB menu | Manual boot commands when GRUB menu entries are broken |
> | **Live USB Rescue** | Boot from external USB/ISO | Full rescue environment when GRUB itself is destroyed |

#### Step 5 — Explore the GRUB Menu

1. Reboot your VM:

   ```bash
   sudo reboot
   ```

2. During startup, **hold `Shift`** (BIOS systems) or press **`Esc`** (UEFI systems) to access the GRUB menu.

3. You should see a menu with entries like:
   - `Ubuntu`
   - `Advanced options for Ubuntu`
   - `TechCorp Training VM — Boot Standard` (from Part B)

4. Select **`Advanced options for Ubuntu`** and observe the available kernel entries and recovery mode options. **Do not select anything yet** — just take note of what you see.

> 📸 **Screenshot `task3_recovery.png`:** Take a screenshot showing the GRUB advanced options and then boot into recovery mode → select `root` → run `whoami`, `mount | grep "on / "`, and `uname -r`. Capture the recovery shell output.

#### Step 6 — Boot into Recovery Mode

1. From the **Advanced options** menu, select the entry ending in **`(recovery mode)`**.

2. The system will boot into a **Recovery Menu** with options like:
   - `resume` — Resume normal boot
   - `clean` — Try to free up disk space
   - `fsck` — Check all file systems
   - `root` — Drop to root shell prompt
   - `grub` — Update GRUB bootloader

3. Select **`root`** to drop into a root shell.

4. In the root shell, verify the system status:

   ```bash
   whoami
   mount | grep "on / "
   uname -r
   ```

5. Resume normal boot:

   ```bash
   reboot
   ```

#### Step 7 — Simulate a GRUB Configuration Break

After rebooting back to normal mode:

1. **Back up** the current GRUB configuration:

   ```bash
   cp /boot/grub/grub.cfg /boot/grub/grub.cfg.bak
   ```

2. **"Break" GRUB** by renaming the configuration file:

   ```bash
   mv /boot/grub/grub.cfg /boot/grub/grub.cfg.broken
   ```

3. **Reboot** to see the effect:

   ```bash
   reboot
   ```

4. After reboot, instead of the normal GRUB menu, you should see the **GRUB command line prompt** (`grub>`), because GRUB can no longer find its configuration.

> 📸 **Screenshot `task3_break.png`:** Take a screenshot showing the `grub>` prompt.

#### Step 8 — Manual Boot from GRUB Command Line

At the `grub>` prompt, you will manually boot the system:

1. **Find available partitions:**

   ```
   ls
   ```

   > This will show something like `(hd0) (hd0,msdos1)` or `(hd0,gpt2)`.

2. **Identify the root partition** (try each one until you find the one with Linux files):

   ```
   ls (hd0,msdos1)/
   ```

   > Look for directories like `boot/`, `etc/`, `home/`, `usr/`. That is your root partition.

3. **Set the root and boot the kernel manually:**

   ```
   set root=(hd0,msdos1)
   linux /boot/vmlinuz-<kernel-version> root=/dev/sda1
   initrd /boot/initrd.img-<kernel-version>
   boot
   ```

   > Replace `<kernel-version>` with the actual kernel version you noted earlier (e.g., `5.15.0-91-generic`). Replace `(hd0,msdos1)` and `/dev/sda1` with the correct values for your VM.

> 📸 **Screenshot `task3_manual_boot.png`:** Take a screenshot showing the manual GRUB commands and the system starting to boot.

#### Step 9 — Restore the GRUB Configuration

Once the system boots (you may need to log in):

1. **Restore the backed-up configuration:**

   ```bash
   sudo mv /boot/grub/grub.cfg.broken /boot/grub/grub.cfg
   ```

   Or, regenerate it completely:

   ```bash
   sudo update-grub
   ```

2. **Verify the configuration is back and reboot:**

   ```bash
   ls -la /boot/grub/grub.cfg
   head -5 /boot/grub/grub.cfg
   sudo reboot
   ```

3. After normal boot, record the result:

   ```bash
   echo "" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task3_grub.txt
   echo "=== Part C: Boot Recovery ===" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task3_grub.txt
   echo "Boot recovery successful on $(date)" >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task3_grub.txt
   uname -r >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task3_grub.txt
   uptime >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task3_grub.txt
   ```

> 📸 **Screenshot `task3_restored.png`:** Take a screenshot showing the restored configuration (`ls -la`, `head`) and the system booted normally with `uname -r` and `uptime`.

---

### 🧩 Challenge — GRUB on Your Own

```bash
echo "--- Challenge GRUB ---" >> task3_grub.txt
```

**You are still on your VM.** Only the goal is described — you decide the commands.

3a. **Change the default boot entry.** Modify `GRUB_DEFAULT` in `/etc/default/grub` so that the **second menu entry** (index `1`) boots by default instead of the first. Run `update-grub`, reboot, and observe which entry is highlighted. Record what you changed and what happened.

3b. **Customize the GRUB color scheme.** Add the following settings to `/etc/default/grub` and choose your own color values (options: `black`, `blue`, `green`, `cyan`, `red`, `magenta`, `brown`, `light-gray`, `dark-gray`, `light-blue`, `light-green`, `light-cyan`, `light-red`, `light-magenta`, `yellow`, `white`):

   ```
   GRUB_COLOR_NORMAL="light-gray/black"
   GRUB_COLOR_HIGHLIGHT="yellow/blue"
   ```

   Run `update-grub`, reboot, and capture the new color scheme.

3c. **Find the root partition UUID.** Search inside `/boot/grub/grub.cfg` for the UUID of your root partition using `grep`. Record the UUID and explain how GRUB uses it to find the root filesystem.

> Append all your results to `task3_grub.txt`.

> 📸 **Screenshot `task3_challenge.png`:** Take a screenshot showing the GRUB menu with your custom color scheme and the `grep` output for the UUID.

**Output File:** `task3_grub.txt` and screenshots `task3_snapshot.png` through `task3_challenge.png`

---

## Task 4 — Shared Objects (Dynamic Libraries) Exploration

**Scenario:** A developer reports that an application is crashing with the error `error while loading shared libraries: libXYZ.so: cannot open shared object file`. Your manager says: *"You need to understand how Linux handles shared libraries. Investigate our system's shared objects so you can troubleshoot issues like this."*

**Purpose:** Understand how Linux programs use shared libraries (`.so` files) at runtime, and learn to inspect and troubleshoot library dependencies. This connects to the **OS Structures** concepts from Week 2 — the system call interface and how programs interact with the OS.

**Commands Used:**

- `ldd` — list shared library dependencies of a program
- `ldconfig -p` — display the shared library cache
- `file` — identify file type
- `readelf` — examine ELF (Executable and Linkable Format) binary headers
- `ls` — list shared library directories
- `objdump` — display information about object files

> **Background — Static vs. Dynamic Linking:**
>
> | Aspect | Static Linking | Dynamic Linking |
> |---|---|---|
> | When linked | At **compile time** | At **runtime** (when program starts) |
> | Library code | **Embedded** in the executable | Loaded from **shared `.so` files** |
> | Executable size | Larger (includes all library code) | Smaller (references external `.so`) |
> | Memory usage | Each program has its own copy | Multiple programs **share** one copy in memory |
> | Updates | Must recompile to update library | Update `.so` file — all programs benefit |
> | File extension | `.a` (archive) | `.so` (shared object) |

**Instructions:**

1. Start the output file:

   ```bash
   echo "=== Task 4: Shared Objects Exploration ===" > task4_shared_objects.txt
   ```

2. **Inspect shared library dependencies of common programs:**

   ```bash
   echo "--- Shared libraries used by /bin/ls ---" >> task4_shared_objects.txt
   ldd /bin/ls >> task4_shared_objects.txt

   echo "" >> task4_shared_objects.txt
   echo "--- Shared libraries used by /bin/bash ---" >> task4_shared_objects.txt
   ldd /bin/bash >> task4_shared_objects.txt

   echo "" >> task4_shared_objects.txt
   echo "--- Shared libraries used by /usr/bin/grep ---" >> task4_shared_objects.txt
   ldd /usr/bin/grep >> task4_shared_objects.txt
   ```

   > **Reading `ldd` output:** Each line shows a library name, `=>`, and the path where it is found in the filesystem, followed by the memory address where it will be loaded.

3. **Identify the type of a shared library file:**

   ```bash
   echo "" >> task4_shared_objects.txt
   echo "--- File type of libc ---" >> task4_shared_objects.txt
   file /lib/x86_64-linux-gnu/libc.so.* >> task4_shared_objects.txt 2>&1
   ```

4. **Explore the shared library directories:**

   ```bash
   echo "" >> task4_shared_objects.txt
   echo "--- Contents of /lib/x86_64-linux-gnu/ (first 30 lines) ---" >> task4_shared_objects.txt
   ls /lib/x86_64-linux-gnu/*.so* | head -30 >> task4_shared_objects.txt

   echo "" >> task4_shared_objects.txt
   echo "--- Contents of /usr/lib/ (first 20 lines) ---" >> task4_shared_objects.txt
   ls /usr/lib/*.so* 2>/dev/null | head -20 >> task4_shared_objects.txt
   ```

5. **Search the shared library cache:**

   ```bash
   echo "" >> task4_shared_objects.txt
   echo "--- Shared library cache: searching for 'libc' ---" >> task4_shared_objects.txt
   ldconfig -p | grep libc >> task4_shared_objects.txt

   echo "" >> task4_shared_objects.txt
   echo "--- Shared library cache: searching for 'libpthread' ---" >> task4_shared_objects.txt
   ldconfig -p | grep libpthread >> task4_shared_objects.txt

   echo "" >> task4_shared_objects.txt
   echo "--- Total number of cached shared libraries ---" >> task4_shared_objects.txt
   ldconfig -p | wc -l >> task4_shared_objects.txt
   ```

6. **Examine the dynamic linker configuration:**

   ```bash
   echo "" >> task4_shared_objects.txt
   echo "--- Dynamic linker config (/etc/ld.so.conf) ---" >> task4_shared_objects.txt
   cat /etc/ld.so.conf >> task4_shared_objects.txt
   echo "" >> task4_shared_objects.txt
   echo "--- Include files in /etc/ld.so.conf.d/ ---" >> task4_shared_objects.txt
   ls /etc/ld.so.conf.d/ >> task4_shared_objects.txt
   cat /etc/ld.so.conf.d/*.conf >> task4_shared_objects.txt 2>&1
   ```

   > **How the dynamic linker works:**
   > 1. When you run a program, the kernel loads it into memory.
   > 2. If the program uses shared libraries, the kernel launches the **dynamic linker** (`ld-linux-x86-64.so.2`).
   > 3. The dynamic linker reads the program's headers to find required `.so` files.
   > 4. It searches for them using: `LD_LIBRARY_PATH` → `/etc/ld.so.cache` → default paths (`/lib`, `/usr/lib`).
   > 5. It maps the shared libraries into the program's address space.

7. **Compare a statically linked vs dynamically linked binary:**

   ```bash
   echo "" >> task4_shared_objects.txt
   echo "--- Checking if /bin/ls is dynamically linked ---" >> task4_shared_objects.txt
   file /bin/ls >> task4_shared_objects.txt

   echo "" >> task4_shared_objects.txt
   echo "--- ELF header of /bin/ls ---" >> task4_shared_objects.txt
   readelf -h /bin/ls 2>/dev/null | head -20 >> task4_shared_objects.txt
   ```

8. **Examine which shared libraries are currently loaded in memory:**

   ```bash
   echo "" >> task4_shared_objects.txt
   echo "--- Shared libraries loaded by current shell (from /proc) ---" >> task4_shared_objects.txt
   cat /proc/$$/maps | grep '\.so' | awk '{print $6}' | sort -u >> task4_shared_objects.txt
   ```

   > **Explanation:** `/proc/$$/maps` shows the memory mapping of the current process (`$$` is the PID of the current shell). Filtering for `.so` shows all loaded shared libraries.

### 🧩 Challenge — Investigate on Your Own

```bash
echo "--- Challenge Shared Objects ---" >> task4_shared_objects.txt
```

4a. **Find all shared libraries used by `/usr/bin/ssh`** (or `/usr/bin/curl` if ssh is not installed). Record the output. How many shared libraries does it depend on?

4b. **Use wildcards** to list all shared object files in `/lib/x86_64-linux-gnu/` that start with `libm` (math-related libraries). Record the output.

4c. **Find the actual file** behind the `libc.so.6` symlink. Use `readlink -f` or `ls -la` to follow the chain. Record what you find — is `libc.so.6` a symlink itself?

4d. **Simulate a missing library error.** Create a simple C program or use an existing binary. Use `LD_LIBRARY_PATH` to demonstrate how the system searches for libraries:

   ```bash
   echo 'int main() { return 0; }' > /tmp/test_link.c
   gcc /tmp/test_link.c -o /tmp/test_link 2>/dev/null
   ldd /tmp/test_link >> task4_shared_objects.txt 2>&1
   ```

   Record the shared libraries of the compiled program.

> Append all your results to `task4_shared_objects.txt`.

**Output File:** `task4_shared_objects.txt`

---

## Task 5 — Build & Register a Shared Library (Pair Task)

**Scenario:** A senior developer approaches you and your partner: *"We're building a set of monitoring utilities for TechCorp servers. I need you two to design a shared library API together, then split up — one of you implements the library while the other writes the test program. Neither of you can succeed alone: the library author needs the tester to verify it works, and the tester needs the library to compile against. This is how real teams develop shared components."*

**Purpose:** Apply what you learned about shared objects in Task 4 by collaboratively designing, implementing, testing, and installing a custom `.so` shared library. This task requires genuine coordination — partners depend on each other's work and cannot complete the task independently.

> 👥 **Pair Task:** Work **side by side** with your partner (or on a call). You will coordinate throughout. Decide who starts as **Role A** (Library Author) and **Role B** (Test Author). You will **swap roles** in Phase 4.

**Commands Used:**

- `gcc -shared -fPIC` — compile a position-independent shared object
- `sudo cp` — install the library to a system directory
- `sudo ldconfig` — refresh the shared library cache
- `ldd` — verify library linking
- `gcc -L -l` — compile a program linking against a custom library

**Instructions:**

### Phase 1 — Design the API Together (Both Partners)

Sit together and **agree on the library's API**. Discuss what each function should do, its name, parameters, and return type. Then **both partners** create the same header file on their own system:

```bash
mkdir -p shared_lib_lab
cd shared_lib_lab
echo "=== Task 5: Build and Register a Shared Library ===" > ../task5_shared_library.txt
```

Create the **header file** — this is the contract both partners must follow:

```bash
cat > techcorp_sysinfo.h << 'EOF'
#ifndef TECHCORP_SYSINFO_H
#define TECHCORP_SYSINFO_H

// Returns the hostname of the machine
const char* tc_get_hostname(void);

// Returns the current uptime in a human-readable string
const char* tc_get_uptime(void);

// Returns the number of CPU cores
int tc_get_cpu_count(void);

#endif
EOF
```

Record the API design:

```bash
echo "--- API Design (header file) ---" >> ../task5_shared_library.txt
cat techcorp_sysinfo.h >> ../task5_shared_library.txt
```

> 📸 **Screenshot `task5_pair_design.png`:** Take a screenshot showing **both partners' screens** with the same header file open. This proves you designed the API together.

---

### Phase 2 — Divide & Build (Work Separately)

**From this point, partners work on their own systems WITHOUT showing each other their code.** Partner A writes the implementation; Partner B writes the test. Neither sees the other's work until Phase 3.

#### Partner A — Implement the Library

Create the **library implementation** that fulfills the API contract:

```bash
cat > techcorp_sysinfo.c << 'EOF'
#include "techcorp_sysinfo.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static char hostname_buf[256];
static char uptime_buf[128];

const char* tc_get_hostname(void) {
    if (gethostname(hostname_buf, sizeof(hostname_buf)) == 0)
        return hostname_buf;
    return "unknown";
}

const char* tc_get_uptime(void) {
    FILE *fp = fopen("/proc/uptime", "r");
    if (fp) {
        double up_seconds;
        if (fscanf(fp, "%lf", &up_seconds) == 1) {
            int hours = (int)(up_seconds / 3600);
            int minutes = ((int)up_seconds % 3600) / 60;
            snprintf(uptime_buf, sizeof(uptime_buf),
                     "%d hours, %d minutes", hours, minutes);
        }
        fclose(fp);
        return uptime_buf;
    }
    return "unknown";
}

int tc_get_cpu_count(void) {
    return (int)sysconf(_SC_NPROCESSORS_ONLN);
}
EOF
```

Compile the shared library:

```bash
gcc -fPIC -c techcorp_sysinfo.c -o techcorp_sysinfo.o
gcc -shared -o libtechcorp_sysinfo.so techcorp_sysinfo.o

echo "" >> ../task5_shared_library.txt
echo "--- Partner A: Compiled shared library ---" >> ../task5_shared_library.txt
file libtechcorp_sysinfo.so >> ../task5_shared_library.txt
ls -l libtechcorp_sysinfo.so >> ../task5_shared_library.txt
```

> **Explanation:**
> - `-fPIC` means **Position-Independent Code** — required for shared libraries so the code can be loaded at any memory address.
> - `-shared` tells `gcc` to produce a `.so` file instead of a regular executable.

**Partner A: STOP here. Do not write a test program. Wait for Partner B.**

#### Partner B — Write the Test Program

Using **only the header file** (you have NOT seen Partner A's `.c` implementation), write a test program that exercises every function in the API:

```bash
cat > sysinfo_test.c << 'EOF'
#include <stdio.h>
#include "techcorp_sysinfo.h"

int main(void) {
    printf("=== TechCorp System Info Report ===\n");
    printf("Hostname : %s\n", tc_get_hostname());
    printf("Uptime   : %s\n", tc_get_uptime());
    printf("CPU Cores: %d\n", tc_get_cpu_count());
    printf("===================================\n");
    return 0;
}
EOF

echo "" >> ../task5_shared_library.txt
echo "--- Partner B: Test program written ---" >> ../task5_shared_library.txt
cat sysinfo_test.c >> ../task5_shared_library.txt
```

**Partner B: STOP here. You cannot compile yet — you need Partner A's `.so` file.**

---

### Phase 3 — Integrate & Debug (Both Partners Together)

Now come back together. Partner A shares their compiled `.so` file with Partner B (e.g., copy it to Partner B's `shared_lib_lab/` directory via `scp`, USB, or shared folder). Partner B also shares their `sysinfo_test.c` with Partner A.

**On Partner B's system** (or whichever machine has both files):

```bash
# Compile the test program linking against the shared library
gcc sysinfo_test.c -L. -ltechcorp_sysinfo -o sysinfo_test

echo "" >> ../task5_shared_library.txt
echo "--- Integration: ldd on test program (before install) ---" >> ../task5_shared_library.txt
ldd ./sysinfo_test >> ../task5_shared_library.txt 2>&1

# Run with LD_LIBRARY_PATH pointing to the current directory
echo "" >> ../task5_shared_library.txt
echo "--- Integration: Test run (using LD_LIBRARY_PATH) ---" >> ../task5_shared_library.txt
LD_LIBRARY_PATH=. ./sysinfo_test >> ../task5_shared_library.txt
```

> **If the test fails or gives unexpected output:** Debug together. Check that the header file matches on both systems, that the `.so` compiled cleanly, and that the test calls the functions correctly. This debugging is a key part of the pair experience.

---

### Phase 4 — Swap Roles: Extend the Library

Now **swap roles**: Partner B adds a new function to the library, and Partner A writes a test for it.

#### Partner B — Add a New Function

1. First, **both partners** update the header file to add a new function:

   ```bash
   cat > techcorp_sysinfo.h << 'EOF'
   #ifndef TECHCORP_SYSINFO_H
   #define TECHCORP_SYSINFO_H

   const char* tc_get_hostname(void);
   const char* tc_get_uptime(void);
   int tc_get_cpu_count(void);

   // NEW — Returns total memory in MB
   long tc_get_memory_mb(void);

   #endif
   EOF
   ```

2. **Partner B** implements the new function in a separate file:

   ```bash
   cat > techcorp_memory.c << 'EOF'
   #include "techcorp_sysinfo.h"
   #include <stdio.h>

   long tc_get_memory_mb(void) {
       FILE *fp = fopen("/proc/meminfo", "r");
       if (fp) {
           long mem_kb = 0;
           if (fscanf(fp, "MemTotal: %ld kB", &mem_kb) == 1) {
               fclose(fp);
               return mem_kb / 1024;
           }
           fclose(fp);
       }
       return -1;
   }
   EOF
   ```

3. **Partner B** recompiles the full library (combining both `.c` files):

   ```bash
   gcc -fPIC -c techcorp_sysinfo.c -o techcorp_sysinfo.o
   gcc -fPIC -c techcorp_memory.c -o techcorp_memory.o
   gcc -shared -o libtechcorp_sysinfo.so techcorp_sysinfo.o techcorp_memory.o

   echo "" >> ../task5_shared_library.txt
   echo "--- Phase 4: Partner B recompiled library with new function ---" >> ../task5_shared_library.txt
   file libtechcorp_sysinfo.so >> ../task5_shared_library.txt
   ```

#### Partner A — Write a Test for the New Function

Using only the updated header file, **Partner A** writes a new test:

```bash
cat > sysinfo_test_v2.c << 'EOF'
#include <stdio.h>
#include "techcorp_sysinfo.h"

int main(void) {
    printf("=== TechCorp System Info Report v2 ===\n");
    printf("Hostname : %s\n", tc_get_hostname());
    printf("Uptime   : %s\n", tc_get_uptime());
    printf("CPU Cores: %d\n", tc_get_cpu_count());
    printf("Memory   : %ld MB\n", tc_get_memory_mb());
    printf("======================================\n");
    return 0;
}
EOF

echo "" >> ../task5_shared_library.txt
echo "--- Phase 4: Partner A wrote v2 test ---" >> ../task5_shared_library.txt
cat sysinfo_test_v2.c >> ../task5_shared_library.txt
```

**Integrate again** — compile and test on the same system:

```bash
gcc sysinfo_test_v2.c -L. -ltechcorp_sysinfo -o sysinfo_test_v2

echo "" >> ../task5_shared_library.txt
echo "--- Phase 4: v2 test run ---" >> ../task5_shared_library.txt
LD_LIBRARY_PATH=. ./sysinfo_test_v2 >> ../task5_shared_library.txt
```

---

### Phase 5 — Install System-Wide (Both Partners)

Install the final library so any program on the system can use it:

```bash
# Copy the library to the system library directory
sudo cp libtechcorp_sysinfo.so /usr/local/lib/

# Refresh the shared library cache
sudo ldconfig

# Verify it is registered
echo "" >> ../task5_shared_library.txt
echo "--- System-wide install: ldconfig cache ---" >> ../task5_shared_library.txt
ldconfig -p | grep techcorp >> ../task5_shared_library.txt

# Re-test WITHOUT LD_LIBRARY_PATH
echo "" >> ../task5_shared_library.txt
echo "--- System-wide test (no LD_LIBRARY_PATH) ---" >> ../task5_shared_library.txt
ldd ./sysinfo_test_v2 >> ../task5_shared_library.txt 2>&1
./sysinfo_test_v2 >> ../task5_shared_library.txt
```

### Clean Up (Optional)

If you want to remove the system-wide library after the lab:

```bash
sudo rm /usr/local/lib/libtechcorp_sysinfo.so
sudo ldconfig
```

### Document Your Partner

```bash
echo "" >> ../task5_shared_library.txt
echo "--- Pair Information ---" >> ../task5_shared_library.txt
echo "Role A (Library Author → v2 Tester): <Partner A Name> - <Student ID>" >> ../task5_shared_library.txt
echo "Role B (Test Author → v2 Library Extender): <Partner B Name> - <Student ID>" >> ../task5_shared_library.txt
```

Return to the lab3 directory:

```bash
cd ..
```

> 📸 **Screenshot `task5_pair_integration.png`:** Take a screenshot showing the final integration test — `ldconfig -p | grep techcorp`, `ldd ./sysinfo_test_v2`, and the test program running with all four fields (hostname, uptime, CPU cores, memory). Both partners should have this screenshot.

**Output File:** `task5_shared_library.txt` and screenshots `task5_pair_design.png`, `task5_pair_integration.png`

---

## Final Submission: GitHub and VS Code Documentation

You have finished all terminal work. Now push your folder to GitHub and document it.

### Phase 1: Push Your Terminal Work to GitHub (From WSL)

1. Capture your terminal history:

   ```bash
   echo "=== Full Command History ===" > task_history.txt
   history | tail -n 100 >> task_history.txt
   ```

2. Verify your folder structure with `tree`:

   ```bash
   cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>
   tree lab3
   ```

3. Commit and push your work:

   ```bash
   cd ~/os-se-<YourStudentID>
   git add .
   git commit -m "Completed Lab 3 — Wildcards, Links, GRUB & Shared Libraries"
   git push
   ```

### Phase 2: Clone & Document in VS Code (From Host OS)

1. **Pull the latest code** to your host machine:

   ```bash
   cd OS-SE-<YourStudentID>
   git pull
   ```

2. **Open in VS Code** and navigate to the `lab3` folder.

3. **Add Images:** Inside the `lab3` folder, create a new folder called `images`. Drag and drop all screenshots into this `images` folder.

4. **Create README:** Inside the `lab3` folder, create a `README.md` file. Use the Lab 3 README template provided by your instructor (see `README.md` in the lab3 folder). You can preview the file in VS Code by pressing <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>V</kbd>.

5. **Final Push:**

   ```bash
   git add .
   git commit -m "Added Lab 3 README report and screenshots"
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
   tree ~/OS-SE-<YourStudentID>/os-lab-<YourStudentID>/lab3
   ```

4. **Log out:**

   ```bash
   exit
   ```

**Submission:** Submit the link to your GitHub repository's `lab3` folder to your instructor via the course portal.

---

## Screenshot Checklist

Use this checklist to make sure you have every required screenshot before moving to the documentation phase. Save all screenshots to your `lab3/images/` folder.

| # | Filename | Task | What to Capture |
|:-:|----------|:----:|-----------------|
| 1 | `task1_challenge.png` | 1 | Terminal showing your challenge wildcard commands (1a–1d) and output |
| 2 | `task2_challenge.png` | 2 | Terminal showing your challenge link commands (2a–2c) and output |
| 3 | `task3_snapshot.png` | 3B | VM snapshot creation confirmation before any VM changes |
| 4 | `task3_timeout.png` | 3B | Modified `/etc/default/grub` with `GRUB_TIMEOUT=10` |
| 5 | `task3_custom_entry.png` | 3B | GRUB menu showing custom "TechCorp Training VM" entry |
| 6 | `task3_background.png` | 3B | GRUB menu with custom background image |
| 7 | `task3_recovery.png` | 3C | GRUB advanced options + recovery shell with `whoami`, `mount`, `uname -r` |
| 8 | `task3_break.png` | 3C | The `grub>` prompt after breaking GRUB |
| 9 | `task3_manual_boot.png` | 3C | Manual GRUB commands and system starting to boot |
| 10 | `task3_restored.png` | 3C | Restored config + normal boot with `uname -r` and `uptime` |
| 11 | `task3_challenge.png` | 3 | GRUB menu with custom colors + `grep` UUID output |
| 12 | `task4_challenge.png` | 4 | Terminal showing your challenge shared objects commands (4a–4d) and output |
| 13 | `task5_pair_design.png` | 5 | Both partners' screens showing the agreed header file (API design) |
| 14 | `task5_pair_integration.png` | 5 | Final integration: `ldconfig`, `ldd`, and v2 test program output |
| 15 | `full_history.png` | All | Output of `history \| tail -n 100` at the end of the lab |

**Total screenshots: 15**

---

## Expected Folder Structure

After completing all tasks and documentation, your `lab3` folder should look like this:

```
os-se-<YourStudentID>/
└── os-lab-<YourStudentID>/
    └── lab3/
        ├── README.md
        ├── images/
        │   ├── task1_challenge.png
        │   ├── task2_challenge.png
        │   ├── task3_snapshot.png
        │   ├── task3_timeout.png
        │   ├── task3_custom_entry.png
        │   ├── task3_background.png
        │   ├── task3_recovery.png
        │   ├── task3_break.png
        │   ├── task3_manual_boot.png
        │   ├── task3_restored.png
        │   ├── task3_challenge.png
        │   ├── task4_challenge.png
        │   ├── task5_pair_design.png
        │   ├── task5_pair_integration.png
        │   └── full_history.png
        ├── task1_wildcards.txt
        ├── task2_links.txt
        ├── task3_grub.txt
        ├── task4_shared_objects.txt
        ├── task5_shared_library.txt
        ├── task_history.txt
        ├── wildcard_lab/
        │   ├── report01.txt ... report10.txt
        │   ├── summary.txt, notes.txt, readme.txt
        │   ├── data01.csv ... data03.csv
        │   ├── image1.png ... image4.jpg
        │   ├── config.yaml, config.yml, settings.json
        │   ├── backup1.tar.gz, backup2.tar.gz
        │   └── memo_mon.txt ... memo_fri.txt
        ├── csv_archive/
        │   └── data01.csv ... data03.csv
        ├── links_lab/
        │   ├── config_hardlink.txt
        │   ├── config_symlink.txt -> (broken)
        │   ├── shared_data.txt, hr_data.txt, eng_data.txt
        │   ├── projects/frontend/index.html
        │   └── web_shortcut -> projects/frontend
        └── shared_lib_lab/
            ├── techcorp_sysinfo.h
            ├── techcorp_sysinfo.c
            ├── techcorp_memory.c
            ├── techcorp_sysinfo.o
            ├── techcorp_memory.o
            ├── libtechcorp_sysinfo.so
            ├── sysinfo_test.c
            ├── sysinfo_test
            ├── sysinfo_test_v2.c
            └── sysinfo_test_v2
```

> **Tip:** Run `tree lab3` from your `os-lab-<YourStudentID>` directory to verify your structure matches the one above before submitting.
