# OS Lab 1 — Introduction to Operating Systems (Hands-on)

| | |
|---|---|
| **Course** | Operating Systems |
| **Lab Title** | Exploring Operating System Basics |
| **Chapter** | Introduction to Operating Systems |
| **Duration** | 2 Hours |
| **Lab Type** | Individual |

---

## Lab Objectives

After completing this lab, students will be able to:

1. Identify basic operating system and kernel information.
2. Use essential Linux file and directory commands.
3. Install, remove, and purge software using the APT package manager.
4. Understand the difference between a program and a running process.
5. Observe multitasking in a running operating system.
6. Detect whether an operating system is running on a virtualized environment.

> This lab establishes a foundation for later labs on process scheduling, threads, and memory management.

---

## Lab Setup

Create your lab submission folder structure and enter the `lab1` directory. Be sure to replace `<YourStudentID>` with your actual student ID (e.g., `10023456`):

```bash
mkdir -p os-se-<YourStudentID>/os-lab-<YourStudentID>/lab1
cd os-se-<YourStudentID>/os-lab-<YourStudentID>/lab1
```

### Documenting Your Work (Taking Screenshots)

In this course, you will **not** submit lab reports using Word or PDF documents. Instead, you will use **Markdown and Git**.

**Workflow for this Lab:**

1. **Take Screenshots:** As you complete each task below in WSL/Terminal, use your host machine's screenshot tool (e.g., Windows Snipping Tool, Mac Screenshot) to capture your terminal.
2. **Save Temporarily:** Save these images temporarily to a folder on your host machine (like your Windows Desktop or Pictures folder). Name them clearly (e.g., `task1.png`, `task2.png`).
3. **Document Later:** You will add these images to a `README.md` file in VS Code after you finish all terminal tasks and push your text files to GitHub. Instructions for this are at the end of the lab.

### Lab Workflow Overview

The diagram below shows the overall flow of this lab from start to submission:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        WSL / Linux Terminal                         │
│                                                                     │
│    ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐    │
│    │  Task 1   │   │  Task 2   │   │  Task 3   │   │  Task 4   │    │
│    │ OS & Kern │──▶│ File Cmds │──▶│ APT Pkgs  │──▶│ Processes │    │
│    └───────────┘   └───────────┘   └───────────┘   └─────┬─────┘    │
│                                                          │          │
│                    ┌───────────┐   ┌───────────┐         │          │
│                    │  Task 6   │   │  Task 5   │         │          │
│                    │ Virt Det  │◀──│ Multitask │◀────────┘          │
│                    └─────┬─────┘   └───────────┘                    │
│                          │                                          │
│                          ▼                                          │
│                   ┌─────────────┐                                   │
│                   │  git push   │                                   │
│                   │  to GitHub  │                                   │
│                   └──────┬──────┘                                   │
└──────────────────────────┼──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Host OS (Windows / Mac)                       │
│                                                                     │
│   ┌──────────────┐   ┌───────────────┐   ┌─────────────────────┐    │
│   │ Clone Repo   │──▶│ Add Images &  │──▶│ Final git push      │    │
│   │ in VS Code   │   │ Write README  │   │ to GitHub           │    │
│   └──────────────┘   └───────────────┘   └──────────┬──────────┘    │
└─────────────────────────────────────────────────────┼───────────────┘
                                                      │
                                                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Local Lab Server (SSH)                        │
│                                                                     │
│   ┌───────────────────┐   ┌─────────────────────────────────────┐   │
│   │ SSH into server   │──▶│ git clone / git pull repo           │   │
│   │ with credentials  │   │ into home directory (~/)            │   │
│   └───────────────────┘   └─────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```
![Lab Workflow](pictures/lab-workflow.png)

### A Brief Note on Output Redirection (`>` and `>>`)

Throughout this lab, you will see commands followed by `>` or `>>`. This is called **output redirection**, and it is used to send the results of a command into a text file instead of printing them on your screen.

- **`>` (Overwrite):** Saves the output to a file. If the file already exists, it will be completely erased and overwritten with the new data.
- **`>>` (Append):** Adds the output to the end of an existing file, preserving the original contents.

---

## Task 1 — Operating System Identification

**Purpose:** Identify the operating system and kernel currently running on the system.

**Commands Used:**

- `uname` — displays kernel and system information
- `lsb_release` — displays Ubuntu distribution details

**Instructions:**

```bash
uname -a > task1_os_info.txt
lsb_release -a >> task1_os_info.txt
```

**Output File:** `task1_os_info.txt`

---

## Task 2 — Essential Linux File and Directory Commands

**Purpose:** Practice essential Linux file system commands and understand how to navigate and manipulate files.

**Commands Introduced:**

- `pwd` — Print Working Directory (shows your current location).
- `ls` — List directory contents (shows files and folders).
- `mkdir` / `cd` — Make a new directory / Change into a directory.
- `touch` — Creates a new, empty file.
- `echo` — Prints text (often redirected to insert text into a file).
- `cat` — Concatenates and displays the contents of a file.
- `cp` / `mv` / `rm` — Copy, Move/Rename, and Remove (delete) files.

> **Note on Linux Paths:** In Linux, `..` represents the parent directory. When you use `../` at the beginning of a file path, you are telling the system to look for or create that file exactly one folder level above your current location. Similarly, `cd ..` moves you up one folder.

**Instructions:**

1. Create and enter a working directory:

   ```bash
   mkdir task2_files
   cd task2_files
   ```

2. Record the current directory and initial file list:

   ```bash
   pwd > ../task2_file_commands.txt
   ls >> ../task2_file_commands.txt
   ```

3. Create files and list them:

   ```bash
   touch a.txt b.txt
   ls >> ../task2_file_commands.txt
   ```

4. Write content into the files and record their contents:

   ```bash
   echo "This is file A" > a.txt
   echo "This is file B" > b.txt
   cat a.txt b.txt >> ../task2_file_commands.txt
   ```

5. Copy a file and record the change:

   ```bash
   cp a.txt a_copy.txt
   ls >> ../task2_file_commands.txt
   ```

6. Rename a file and record the change:

   ```bash
   mv b.txt b_renamed.txt
   ls >> ../task2_file_commands.txt
   ```

7. Delete a file and record the final state:

   ```bash
   rm a_copy.txt
   ls >> ../task2_file_commands.txt
   ```

8. Return to the main lab folder:

   ```bash
   cd ..
   ```

**Output File:** `task2_file_commands.txt`

---

## Task 3 — Package Management Using APT

**Purpose:** Understand how the operating system installs, removes, and manages software using the Advanced Package Tool (APT). You will explicitly observe the crucial difference between *removing* a package (which leaves configuration files behind) and *purging* it (which deletes everything).

**Commands Used:**

- `apt-get update`, `apt-get install`
- `apt-get remove`, `apt-get purge`
- `ls` — used here to check for the existence of configuration directories

**Instructions:**

1. Update the package list:

   ```bash
   sudo apt-get update > task3_apt_update.txt
   ```

2. Install `mc` (Midnight Commander), a terminal-based file manager that generates system-wide configuration files in the `/etc` directory:

   ```bash
   sudo apt-get install mc -y > task3_apt_install.txt
   ```

3. Verify the installation and confirm that its configuration folder was created:

   ```bash
   which mc > task3_verify_install.txt
   ls -ld /etc/mc >> task3_verify_install.txt
   ```

4. **Demonstrating `remove`:**

   Remove the package (this uninstalls the program binaries but keeps the configuration files):

   ```bash
   sudo apt-get remove mc -y > task3_apt_remove.txt
   ```

   Check the configuration folder again (notice that it still exists!):

   ```bash
   ls -ld /etc/mc > task3_config_after_remove.txt
   ```

5. **Demonstrating `purge`:**

   Purge the package completely (this removes the remaining configuration files):

   ```bash
   sudo apt-get purge mc -y > task3_apt_purge.txt
   ```

   Check the configuration folder one last time. (We use `2>&1` to capture the "No such file or directory" error message into our output file, proving the folder is gone):

   ```bash
   ls -ld /etc/mc > task3_config_after_purge.txt 2>&1
   ```

**Output Files:** `task3_apt_update.txt`, `task3_apt_install.txt`, `task3_verify_install.txt`, `task3_apt_remove.txt`, `task3_config_after_remove.txt`, `task3_apt_purge.txt`, `task3_config_after_purge.txt`

---

## Task 4 — Programs vs Processes (Single Process)

**Purpose:** Demonstrate that a program becomes a running process when it is executed.

**Commands Used:**

- `sleep` — runs a program that simply pauses for a specified duration
- `&` — added to the end of a command to run a program in the background
- `ps` — lists currently running processes

**Instructions:**

1. Run a background process:

   ```bash
   sleep 120 &
   ```

2. Capture the list of running processes:

   ```bash
   ps > task4_process_list.txt
   ```

**Output File:** `task4_process_list.txt`

---

## Task 5 — Installing Real Applications & Observing Multitasking

**Purpose:** Install commonly used, server-friendly CLI applications and observe multiple programs running simultaneously under the OS.

**Commands Used:**

- `apt-get install`
- `python3` (built-in tool to run a background web server)

**Instructions:**

1. Install `htop` (an interactive process viewer) and `tmux` (a terminal multiplexer):

   ```bash
   sudo apt-get install htop tmux -y
   ```

2. Verify their installations:

   ```bash
   which htop tmux > task5_app_verify.txt
   ```

3. Start multiple background applications to simulate a multitasking environment:

   ```bash
   sleep 500 &
   sleep 600 &
   python3 -m http.server 8080 &
   ```

4. Capture the process list showing your simultaneous background applications:

   ```bash
   ps > task5_multitasking.txt
   ```

> **Optional cleanup:** You can stop the web server by typing `kill %3` if it was the third background job.

**Output Files:** `task5_app_verify.txt`, `task5_multitasking.txt`

---

## Task 6 — Virtualization and Hypervisor Detection

**Purpose:** Check whether the operating system is running on physical hardware or a virtual machine.

**Commands Used:**

- `systemd-detect-virt`
- `lscpu`
- `uname`, `hostname`

**Instructions:**

```bash
systemd-detect-virt > task6_virtualization_check.txt
lscpu | grep -i hypervisor >> task6_virtualization_check.txt
uname -r >> task6_virtualization_check.txt
hostname >> task6_virtualization_check.txt
```

**Output File:** `task6_virtualization_check.txt`

---

## Final Submission: GitHub and VS Code Documentation

You have finished the terminal work. Now you will push your folder to GitHub, clone it to your host computer, and document it using VS Code.

### Phase 1: Push Your Terminal Work to GitHub (From WSL)

1. Organize your `os-se-<YourStudentID>` folder so the text files are inside their respective task folders.
2. Install the `tree` utility so you can visualize and verify your folder structure before pushing:

   ```bash
   sudo apt-get install tree -y
   ```

   Then run `tree` from your top-level `os-se-<YourStudentID>` directory to check that everything is in place:

   ```bash
   cd ../..    # make sure you are in os-se-<YourStudentID>
   tree
   ```

3. Go to GitHub and create a new repository named `OS-SE-<YourStudentID>` (keep it empty, no README or license).
4. In your WSL terminal, run the following commands to push your work:

   ```bash
   # Move up to the top os-se-<YourStudentID> folder
   cd ../..

   # Initialize Git and commit your text files
   git init
   git add .
   git commit -m "Initial commit of Lab 1 text files"
   git branch -M main

   # Link to GitHub and push (Replace with your actual URL)
   git remote add origin https://github.com/<your-username>/OS-SE-<YourStudentID>.git
   git push -u origin main
   ```

### Phase 2: Clone & Document in VS Code (From Host OS)

Now that your folder structure is on GitHub, move over to your host machine (Windows/Mac) to build your lab report.

1. **Clone the Repository:** Open a terminal or command prompt on your host machine (e.g., Windows Command Prompt), navigate to where you want to work (like your Documents folder), and clone your repo:

   ```bash
   git clone https://github.com/<your-username>/OS-SE-<YourStudentID>.git
   cd OS-SE-<YourStudentID>
   ```

2. **Open in VS Code:** Open the cloned folder in Visual Studio Code.

3. **Add Images:** Inside the `os-lab-<YourStudentID>/lab1` folder, create a new folder called `images`. Drag and drop all the temporary screenshots you took earlier into this `images` folder.

4. **Create README:** Inside the `lab1` folder, create a `README.md` file. Use the Lab 1 README template provided by your instructor to document your findings and link your images. You can preview the file in VS Code by pressing <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>V</kbd>.

5. **Final Push:** Once your report looks good, commit and push the newly added images and README to GitHub from your host terminal or VS Code Source Control panel:

   ```bash
   git add .
   git commit -m "Added README report and screenshots"
   git push
   ```

### Phase 3: Pull Your Work to the Lab Server

After your final push to GitHub, you must also pull your repository onto the local lab server so that your instructor can review it directly.

1. **Connect to the server** using SSH with the credentials provided by your instructor:

   ```bash
   ssh <YourUsername>@<server-address>
   ```

   Enter your password when prompted.

2. **Clone your repository** into your home directory on the server (first time only):

   ```bash
   cd ~
   git clone https://github.com/<your-username>/OS-SE-<YourStudentID>.git
   ```

   If you have already cloned it from a previous session, pull the latest changes instead:

   ```bash
   cd ~/OS-SE-<YourStudentID>
   git pull
   ```

3. **Verify** that your files are present:

   ```bash
   tree ~/OS-SE-<YourStudentID>
   ```

4. **Log out** of the server:

   ```bash
   exit
   ```

**Submission:** Submit the link to your GitHub repository's `lab1` folder to your instructor via the course portal. Ensure that your repository has also been pulled to the lab server.

---

## Expected Folder Structure

After completing all tasks and documentation, your repository should look like this:

```
os-se-<YourStudentID>/
└── os-lab-<YourStudentID>/
    └── lab1/
        ├── README.md
        ├── images/
        │   ├── task1.png
        │   ├── task2.png
        │   ├── task3.png
        │   ├── task4.png
        │   ├── task5.png
        │   └── task6.png
        ├── task1_os_info.txt
        ├── task2_file_commands.txt
        ├── task2_files/
        │   ├── a.txt
        │   └── b_renamed.txt
        ├── task3_apt_install.txt
        ├── task3_apt_purge.txt
        ├── task3_apt_remove.txt
        ├── task3_apt_update.txt
        ├── task3_config_after_purge.txt
        ├── task3_config_after_remove.txt
        ├── task3_verify_install.txt
        ├── task4_process_list.txt
        ├── task5_app_verify.txt
        ├── task5_multitasking.txt
        └── task6_virtualization_check.txt
```

> **Tip:** Run `tree` from your `os-se-<YourStudentID>` directory to verify your structure matches the one above before submitting.