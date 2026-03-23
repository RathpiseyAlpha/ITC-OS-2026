# OS Lab 3 — Wildcards, Links, GRUB & Shared Libraries (Hands-on)

| | |
|---|---|
| **Course** | Operating Systems |
| **Lab Title** | Wildcards, Links, Boot Loader Exploration & Shared Libraries |
| **Chapter** | OS Structures & Bootstrap Process |
| **Duration** | 3 Hours |
| **Lab Type** | Individual + Pair (Task 7) |

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
> 5. **Tasks 1–5 (Required, Individual)** — Wildcards, Links, GRUB exploration, Shared objects, Boot recovery
> 6. **Task 6 (Required, Individual)** — GRUB customization on your own VM
> 7. **Task 7 (Required, Pair)** — Create and register a custom shared library
> 8. **Deliverables & Submission** — Folder structure, README template, git push
> 9. **Screenshot Checklist** — Every screenshot you need, in one place

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
| Task 3: GRUB Exploration | [▶ Task 3](#task-3--grub-bootloader-exploration) |
| Task 4: Shared Objects | [▶ Task 4](#task-4--shared-objects-dynamic-libraries-exploration) |
| Task 5: Boot Recovery | [▶ Task 5](#task-5--simulate-a-safe-boot-break-and-recovery-vm-only) |
| Task 6: GRUB Customization | [▶ Task 6](#task-6--grub-customization-vm-only) |
| Task 7: Build a Shared Library (Pair) | [▶ Task 7](#task-7--build-and-register-a-shared-library-pair-task) |
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
| **3** | GRUB Bootloader Exploration | Individual | WSL / Server | `cat`, `ls`, `uname -r`, `dmesg`, `head` | `task3_grub.txt` |
| **4** | Shared Objects Exploration | Individual | WSL / Server | `ldd`, `ldconfig -p`, `file`, `readelf` | `task4_shared_objects.txt` |
| **5** | Boot Break & Recovery | Individual | **VM only** | GRUB CLI, `update-grub`, `mount` | `task5_boot_recovery.txt` + screenshots |
| **6** | GRUB Customization | Individual | **VM only** | `/etc/default/grub`, `update-grub` | `task6_grub_custom.txt` + screenshots |
| **7** | Build a Shared Library | **Pair** | WSL / Server | `gcc -shared`, `ldconfig`, `ldd` | `task7_shared_library.txt` |

---

## Lab Setup

Navigate into your existing lab submission repository and create the `lab3` directory:

```bash
cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>
mkdir lab3
cd lab3
```

### Documenting Your Work (Taking Screenshots)

Each task in this lab redirects its output into `.txt` files, which serve as your **primary proof of work** for the guided portions. You also need screenshots for challenges, VM tasks, and GRUB customization:

1. **Output Files (No Screenshots Needed for Guided Steps):** The guided steps in each task automatically save results to `.txt` files (e.g., `task1_wildcards.txt`). These files will be committed to your repository as proof of completion.
2. **Challenge Screenshots:** When you reach the 🧩 **Challenge** sections in Tasks 1, 2, and 4, take a screenshot of your terminal showing the commands you used and their output.
3. **VM Screenshots (Tasks 5 & 6):** Boot recovery and GRUB customization involve the VM console/display, so they must be documented with screenshots.
4. **Pair Task Screenshot (Task 7):** Take a screenshot showing the shared library compilation, registration, and test program output.
5. **Full History Screenshot:** After finishing all tasks, run `history | tail -n 100` and take a screenshot.
6. **Save All Images:** Save all screenshots to a folder on your host machine. You will add them to an `images/` folder in your `README.md` later.

> **See the [Screenshot Checklist](#screenshot-checklist) at the end of this document for the complete list of every screenshot you need.**

### Lab Workflow Overview

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          WSL / Linux Terminal                                │
│                                                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐          │
│  │ Task 1  │  │ Task 2  │  │ Task 3  │  │ Task 4  │  │ Task 7   │          │
│  │Wildcards│─▶│  Links  │─▶│  GRUB   │─▶│ Shared  │─▶│ Build .so│          │
│  │         │  │         │  │ Explore │  │ Objects │  │  (Pair)  │          │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └────┬─────┘          │
│                                                             │                │
│                                                             ▼                │
│                                                      ┌───────────┐           │
│                                                      │ git push  │           │
│                                                      │ to GitHub │           │
│                                                      └─────┬─────┘           │
└─────────────────────────────────────────────────────────────┼────────────────┘
                                                              │
                 ┌────────────────────────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                          VM (VirtualBox / VMware)                             │
│                                                                              │
│  ┌──────────┐   ┌──────────┐                                                │
│  │ Task 5   │──▶│ Task 6   │                                                │
│  │Boot Break│   │GRUB Skin │                                                │
│  │& Recovery│   │& Timeout │                                                │
│  └──────────┘   └──────────┘                                                │
└──────────────────────────────────────────────────────────────────────────────┘
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

## Task 3 — GRUB Bootloader Exploration

**Scenario:** A senior engineer tells you: *"Every sysadmin needs to understand how Linux boots. If a server can't boot, nothing else matters. Start by reading our GRUB configuration and understanding what each piece does."*

**Purpose:** Explore the GRUB (GRand Unified Bootloader) configuration and understand the Linux boot sequence from power-on to a running OS. This task connects directly to the **Bootstrap Process** concept from Week 1 lectures.

**Commands Used:**

- `cat` / `less` — view file contents
- `ls` — list directory contents
- `grub-mkconfig` — generate/preview GRUB configuration
- `uname -r` — display current kernel version
- `dmesg` — display kernel boot messages

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

**Output File:** `task3_grub.txt`

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

## Task 5 — Simulate a Safe Boot "Break" and Recovery (VM Only)

**Scenario:** Your manager says: *"We have a training VM that I want you to practice on. I need you to simulate a boot failure, enter rescue mode, and restore normal boot. This is a critical skill — if a production server can't boot, you need to know how to fix it WITHOUT reinstalling the OS."*

**Purpose:** Practice emergency boot recovery in a safe, controlled environment. You will intentionally "break" the GRUB configuration on a virtual machine, enter rescue mode, and restore normal booting.

> ⚠️ **WARNING:** This task must be performed **only on a virtual machine** (VirtualBox, VMware, or a cloud VM). **Never** perform these steps on a physical machine or your primary development system. Take a VM snapshot before starting so you can always roll back.

**Commands Used:**

- VM snapshot tools (VirtualBox: `Snapshots` panel)
- GRUB menu (hold `Shift` during boot, or `Esc` for UEFI)
- Recovery mode boot options
- `mount`, `chroot` — repair commands in rescue mode
- `grub-install`, `update-grub` — reinstall/reconfigure GRUB

> **Background — Linux Recovery Modes:**
>
> | Mode | How to Enter | What It Does |
> |---|---|---|
> | **Recovery Mode** | Select from GRUB menu → "Advanced options" → "(recovery mode)" | Boots into single-user mode with limited services; root shell access |
> | **GRUB Command Line** | Press `c` at the GRUB menu | Manual boot commands when GRUB menu entries are broken |
> | **Live USB Rescue** | Boot from external USB/ISO | Full rescue environment when GRUB itself is destroyed |

**Instructions:**

### Step 1 — Take a VM Snapshot (Safety Net)

Before anything else, create a snapshot of your VM so you can always restore it:

- **VirtualBox:** Machine → Take Snapshot → Name it `"Before Boot Lab"`
- **VMware:** VM → Snapshot → Take Snapshot

> 📸 **Screenshot `task5_step1.png`:** Take a screenshot showing your snapshot has been created.

### Step 2 — Explore the Current GRUB Menu

1. Reboot your VM:

   ```bash
   sudo reboot
   ```

2. During startup, **hold `Shift`** (BIOS systems) or press **`Esc`** (UEFI systems) to access the GRUB menu.

3. You should see a menu with entries like:
   - `Ubuntu`
   - `Advanced options for Ubuntu`

4. Select **`Advanced options for Ubuntu`** and observe the available kernel entries and recovery mode options. **Do not select anything yet** — just take note of what you see.

> 📸 **Screenshot `task5_step2.png`:** Take a screenshot of the GRUB menu showing the available entries.

### Step 3 — Boot into Recovery Mode

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

> 📸 **Screenshot `task5_step3.png`:** Take a screenshot showing the recovery menu, and another showing the root shell.

### Step 4 — Simulate a GRUB Configuration Break

From the recovery root shell (or after rebooting back to normal mode):

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

> 📸 **Screenshot `task5_step4.png`:** Take a screenshot showing the `grub>` prompt.

### Step 5 — Manual Boot from GRUB Command Line

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

   > Replace `<kernel-version>` with the actual kernel version you noted in Step 2 (e.g., `5.15.0-91-generic`). Replace `(hd0,msdos1)` and `/dev/sda1` with the correct values for your VM.

> 📸 **Screenshot `task5_step5.png`:** Take a screenshot showing the manual GRUB commands and the system starting to boot.

### Step 6 — Restore the GRUB Configuration

Once the system boots (you may need to log in):

1. **Restore the backed-up configuration:**

   ```bash
   sudo mv /boot/grub/grub.cfg.broken /boot/grub/grub.cfg
   ```

   Or, regenerate it completely:

   ```bash
   sudo update-grub
   ```

2. **Verify the configuration is back:**

   ```bash
   ls -la /boot/grub/grub.cfg
   head -5 /boot/grub/grub.cfg
   ```

> 📸 **Screenshot `task5_step6.png`:** Take a screenshot showing the restored configuration.

### Step 7 — Verify Normal Boot

1. Reboot the VM:

   ```bash
   sudo reboot
   ```

2. Confirm that the GRUB menu appears normally and the system boots without issues.

3. After login, run:

   ```bash
   echo "Boot recovery successful on $(date)" > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task5_boot_recovery.txt
   uname -r >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task5_boot_recovery.txt
   uptime >> ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab3/task5_boot_recovery.txt
   ```

> 📸 **Screenshot `task5_step7.png`:** Take a screenshot showing the system has booted normally and the output of the commands above.

**Output File:** `task5_boot_recovery.txt` and screenshots `task5_step1.png` through `task5_step7.png`

---

## Final Submission: GitHub and VS Code Documentation

You have finished the terminal work. Now push your folder to GitHub and document it.

### Phase 1: Push Your Terminal Work to GitHub (From WSL)

1. Verify your folder structure with `tree`:

   ```bash
   cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>
   tree lab3
   ```

2. Commit and push your work:

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

4. **Create README:** Inside the `lab3` folder, create a `README.md` file. Use the Lab 3 README template provided by your instructor. You can preview the file in VS Code by pressing <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>V</kbd>.

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
        │   ├── task4_challenge.png
        │   ├── task5_step1.png
        │   ├── task5_step2.png
        │   ├── task5_step3.png
        │   ├── task5_step4.png
        │   ├── task5_step5.png
        │   ├── task5_step6.png
        │   ├── task5_step7.png
        │   └── full_history.png
        ├── task1_wildcards.txt
        ├── task2_links.txt
        ├── task3_grub.txt
        ├── task4_shared_objects.txt
        ├── task5_boot_recovery.txt
        ├── wildcard_lab/
        │   ├── report01.txt
        │   ├── report02.txt
        │   ├── report03.txt
        │   ├── report10.txt
        │   ├── summary.txt
        │   ├── notes.txt
        │   ├── readme.txt
        │   ├── data01.csv
        │   ├── data02.csv
        │   ├── data03.csv
        │   ├── image1.png
        │   ├── image2.png
        │   ├── image3.jpg
        │   ├── image4.jpg
        │   ├── config.yaml
        │   ├── config.yml
        │   ├── settings.json
        │   ├── backup1.tar.gz
        │   ├── backup2.tar.gz
        │   └── memo_{mon,tue,wed,thu,fri}.txt
        ├── csv_archive/
        │   ├── data01.csv
        │   ├── data02.csv
        │   └── data03.csv
        └── links_lab/
            ├── config_hardlink.txt
            ├── config_symlink.txt
            ├── shared_data.txt
            ├── hr_data.txt
            ├── eng_data.txt
            ├── projects/
            │   └── frontend/
            │       └── index.html
            └── web_shortcut -> projects/frontend
```

> **Tip:** Run `tree lab3` from your `os-lab-<YourStudentID>` directory to verify your structure matches the one above before submitting.
