```
 ██████╗ ██████╗ ███████╗██████╗  █████╗ ████████╗██╗███╗   ██╗ ██████╗
██╔═══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║████╗  ██║██╔════╝
██║   ██║██████╔╝█████╗  ██████╔╝███████║   ██║   ██║██╔██╗ ██║██║  ███╗
██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗██╔══██║   ██║   ██║██║╚██╗██║██║   ██║
╚██████╔╝██║     ███████╗██║  ██║██║  ██║   ██║   ██║██║ ╚████║╚██████╔╝
 ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝

███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗███████╗
██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║██╔════╝
███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║███████╗
╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║╚════██║
███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║███████║
╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝╚══════╝
```

<div align="center">

**Institute of Technology of Cambodia** · Department of Information and Communication Engineering

📖 Course Materials for **Operating Systems & Software Engineering**

[![GitHub](https://img.shields.io/badge/GitHub-ITC--OS--2026-181717?logo=github&style=for-the-badge)](https://github.com/RathpiseyAlpha/ITC-OS-2026)
[![License](https://img.shields.io/badge/License-Educational-blue?style=for-the-badge)](#)
[![Web View](https://img.shields.io/badge/🖥️_Web_View-Terminal_Theme-00ff41?style=for-the-badge&logo=html5&logoColor=white)](https://rathpiseyalpha.github.io/ITC-OS-2026/)

---

> **🌐 [View the interactive terminal-themed web page →](https://rathpiseyalpha.github.io/ITC-OS-2026/)**

</div>

## ⚡ Quick Start

```bash
$ git clone https://github.com/RathpiseyAlpha/ITC-OS-2026.git
$ cd ITC-OS-2026
$ tree -L 2
```

---

## 📂 Repository Structure

```
ITC-OS-2026/
├── README.md                  # ← You are here
├── index.html                 # Landing page (terminal theme)
├── course-outline.md          # Full course outline & weekly schedule
│
├── lectures/
│   ├── files/                 # Lecture slide PDFs
│   │   ├── ch1.pdf            #   Ch 1 — Introduction to OS
│   │   ├── ch2.pdf            #   Ch 2 — OS Structures & Interfaces
│   │   ├── ch3.pdf            #   Ch 3 — Processes
│   │   ├── ch4.pdf            #   Ch 4 — Threads & Multicore
│   │   ├── ch5.pdf            #   Ch 5 — CPU Scheduling I
│   │   ├── ch6.pdf            #   Ch 6 — CPU Scheduling II
│   │   ├── ch7.pdf            #   Ch 7 — Critical Sections
│   │   ├── ch8.pdf            #   Ch 8 — Semaphores & Sync Problems
│   │   ├── ch9.pdf            #   Ch 9 — Deadlocks
│   │   └── ch10.pdf           #   Ch 10 — Memory Management I
│   │
│   ├── notes/                 # 📝 Note-taking templates (one per week)
│   │   ├── README.md          #   Guide & template structure
│   │   ├── week01-introduction-to-os.md
│   │   ├── week02-os-structures-interfaces.md
│   │   ├── week03-processes.md
│   │   ├── week04-threads-multicore.md
│   │   ├── week05-cpu-scheduling-1.md
│   │   ├── week06-cpu-scheduling-2.md
│   │   ├── week07-critical-sections.md
│   │   ├── week08-semaphores-sync.md
│   │   ├── week09-deadlocks.md
│   │   ├── week10-memory-management.md
│   │   ├── week11-virtual-memory.md
│   │   └── week12-file-systems.md
│   │
│   └── class-activity/        # 🧪 Hands-on programming activities
│       ├── README.md          #   Activity index
│       ├── class-activity1.md #   System Calls with POSIX (Linux)
│       ├── class-activity2.md #   Processes & IPC (Linux + Windows)
│       ├── class-activity3.md #   Socket Communication & Multithreading
│       ├── class-activity4.md #   Shared File API: C++ Mutex & Java synchronized
│       ├── class-activity5.md #   Semaphores: Particle Pairs & HELLO Ordering
│       └── class-activity6.md #   Deadlock Simulation: Bank Account Transfers
│
└── labs/
    ├── lab1/                  # Lab 1 — Exploring OS Basics
    │   ├── lab1-instruction.md
    │   ├── README.md
    │   ├── guides/
    │   └── pictures/
    ├── lab2/                  # Lab 2 — Linux Navigation & File Management
    │   ├── lab2-instruction.md
    │   ├── README.md
    │   └── guides/
    ├── lab3/                  # Lab 3 — Wildcards, Links, GRUB & Shared Libraries
    │   ├── lab3-instruction.md
    │   ├── README.md
    │   └── guides/
    ├── lab4/                  # Lab 4 — I/O Redirection, Pipelines & Process Mgmt
    │   ├── lab4-instruction.md
    │   └── README.md
    ├── lab5/                  # Lab 5 — Threads, Kernel Workers & Process Signals
    │   ├── lab5-instruction.md
    │   └── README.md
    ├── lab6/                  # Lab 6 — Linux Security, Users, Groups & Permissions
    │   ├── lab6-instruction.md
    │   └── README.md
    ├── lab7/                  # Lab 7 — Bash Scripting, Permissions & Automation
    │   ├── lab7-instruction.md
    │   └── README.md
    ├── lab8/                  # Lab 8 — Secure Bash Scripting, Race Conditions & File Locking
    │   ├── lab8-instruction.md
    │   └── README.md
    └── lab9/                  # Lab 9 — Vault Deadlock & Recovery
        ├── lab9-instruction.md
        └── README.md
```

---

## 📖 Course Overview

> *This course provides a comprehensive understanding of how operating systems function, focusing on their architecture, resource management, concurrency, scheduling, and memory handling.*

**Instructor:** Heng Rathpisey  
**Department:** Information and Communication Engineering  
**Institute:** Institute of Technology of Cambodia

### 🎯 Learning Objectives

- Understand the architecture and core functions of operating systems
- Analyze process management, memory allocation, and file systems
- Compare and apply scheduling and resource management algorithms
- Solve synchronization and concurrency problems
- Understand real-world implementations in Linux, Windows, and macOS

---

## 📅 Weekly Schedule

| Wk | Topic | Slides | Lab |
|:--:|-------|:------:|:---:|
| 1 | Introduction to OS | [ch1.pdf](lectures/files/ch1.pdf) | — |
| 2 | OS Structures & Interfaces | [ch2.pdf](lectures/files/ch2.pdf) | — |
| 3 | Processes | [ch3.pdf](lectures/files/ch3.pdf) | [Lab 1](labs/lab1/) |
| 4 | Threads & Multicore | [ch4.pdf](lectures/files/ch4.pdf) | — |
| 5 | CPU Scheduling I | [ch5.pdf](lectures/files/ch5.pdf) | [Lab 2](labs/lab2/) |
| 6 | CPU Scheduling II | [ch6.pdf](lectures/files/ch6.pdf) | [Lab 3](labs/lab3/) |
| 7 | Critical Sections | [ch7.pdf](lectures/files/ch7.pdf) | [Lab 4](labs/lab4/) |
| 8 | Semaphores & Sync Problems | [ch8.pdf](lectures/files/ch8.pdf) | — |
| 9 | Deadlocks | [ch9.pdf](lectures/files/ch9.pdf) | [Lab 9](labs/lab9/) |
| 10 | Memory Management I | [ch10.pdf](lectures/files/ch10.pdf) | — |
| 11 | Virtual Memory | *Coming Soon* | — |
| 12 | File Systems | *Coming Soon* | [Lab 6](labs/lab6/) |

> 📋 See the full [course-outline.md](course-outline.md) for detailed weekly learning objectives.

---

## 🔬 Labs

| Lab | Title | Status | Link |
|:---:|-------|:------:|:----:|
| 1 | Exploring Operating System Basics | ✅ Available | [Instructions](labs/lab1/lab1-instruction.md) |
| 2 | Linux Navigation & File Management | ✅ Available | [Instructions](labs/lab2/lab2-instruction.md) |
| 3 | Wildcards, Links, GRUB & Shared Libraries | ✅ Available | [Instructions](labs/lab3/lab3-instruction.md) |
| 4 | I/O Redirection, Pipelines & Process Management | ✅ Available | [Instructions](labs/lab4/lab4-instruction.md) |
| 5 | Threads, Kernel Workers & Process Signals | ✅ Available | [Instructions](labs/lab5/lab5-instruction.md) |
| 6 | Linux Security, Users, Groups & File Permissions | ✅ Available | [Instructions](labs/lab6/lab6-instruction.md) |
| 7 | Bash Scripting, Permissions & Server Automation | ✅ Available | [Instructions](labs/lab7/lab7-instruction.md) |
| 8 | Secure Bash Scripting, Race Conditions & File Locking | ✅ Available | [Instructions](labs/lab8/lab8-instruction.md) |
| 9 | Vault Deadlock, Resource Ordering & Recovery | ✅ Available | [Instructions](labs/lab9/lab9-instruction.md) |

### Lab 1 Highlights

Lab 1 covers foundational Linux skills through **6 hands-on tasks**:

```
Task 1 ─ OS & Kernel Identification      (uname, lsb_release)
Task 2 ─ File & Directory Commands        (pwd, ls, mkdir, cp, mv, rm)
Task 3 ─ Package Management with APT      (install, remove, purge)
Task 4 ─ Programs vs Processes             (sleep, ps, background jobs)
Task 5 ─ Multitasking & Real Applications  (htop, tmux, http.server)
Task 6 ─ Virtualization Detection          (systemd-detect-virt, lscpu)
```

### Lab 3 Highlights

Lab 3 covers wildcards, links, bootloader administration, and shared libraries through **5 tasks** (Tasks 1–4 individual, Task 5 pair):

```
Task 1 ─ Mastering Wildcards              (*, ?, [], {})
Task 2 ─ Hard Links & Symbolic Links       (ln, ln -s, ls -li, stat)
Task 3 ─ GRUB Exploration & Recovery       (VM / Linux Machine — not WSL)
Task 4 ─ Shared Objects Exploration        (ldd, ldconfig, readelf)
Task 5 ─ Build a Shared Library (Pair)     (gcc -shared -fPIC, ldconfig)
```

> ⚠️ Task 3 (GRUB) requires a **VM or real Linux machine** — WSL does not have GRUB.

---

## 📚 Lecture Slides

| Chapter | Topic | Download |
|:-------:|-------|:--------:|
| 1 | Introduction to Operating Systems | [📄 ch1.pdf](lectures/files/ch1.pdf) |
| 2 | OS Structures & Interfaces | [📄 ch2.pdf](lectures/files/ch2.pdf) |
| 3 | Processes | [📄 ch3.pdf](lectures/files/ch3.pdf) |
| 4 | Threads & Multicore Programming | [📄 ch4.pdf](lectures/files/ch4.pdf) |
| 5 | CPU Scheduling I | [📄 ch5.pdf](lectures/files/ch5.pdf) |
| 6 | CPU Scheduling II | [📄 ch6.pdf](lectures/files/ch6.pdf) |
| 7 | Critical Sections | [📄 ch7.pdf](lectures/files/ch7.pdf) |
| 8 | Semaphores & Sync Problems | [📄 ch8.pdf](lectures/files/ch8.pdf) |
| 9 | Deadlocks | [📄 ch9.pdf](lectures/files/ch9.pdf) |
| 10 | Memory Management I | [📄 ch10.pdf](lectures/files/ch10.pdf) |

> More chapters will be added as the course progresses.

---

## � Lecture Notes Templates

Standardized note-taking templates are provided for every week of the course. Each template includes sections for key concepts, detailed notes, diagrams, comparisons, examples, review questions, and personal reflection.

→ Browse them in [`lectures/notes/`](lectures/notes/)

| Week | Template |
|:----:|----------|
| 1 | [Introduction to OS](lectures/notes/week01-introduction-to-os.md) |
| 2 | [OS Structures & Interfaces](lectures/notes/week02-os-structures-interfaces.md) |
| 3 | [Processes](lectures/notes/week03-processes.md) |
| 4 | [Threads & Multicore](lectures/notes/week04-threads-multicore.md) |
| 5 | [CPU Scheduling I](lectures/notes/week05-cpu-scheduling-1.md) |
| 6 | [CPU Scheduling II](lectures/notes/week06-cpu-scheduling-2.md) |
| 7 | [Critical Sections](lectures/notes/week07-critical-sections.md) |
| 8 | [Semaphores & Sync Problems](lectures/notes/week08-semaphores-sync.md) |
| 9 | [Deadlocks](lectures/notes/week09-deadlocks.md) |
| 10 | [Memory Management I](lectures/notes/week10-memory-management.md) |
| 11 | [Virtual Memory](lectures/notes/week11-virtual-memory.md) |
| 12 | [File Systems](lectures/notes/week12-file-systems.md) |

---

## 🧪 Class Activities

Hands-on programming activities that accompany the lecture topics.

| # | Activity | Topic | Related Lecture |
|---|----------|-------|-----------------|
| 1 | [System Calls in Practice](lectures/class-activity/class-activity1.md) | POSIX System Calls (Linux) + Optional Windows API | Week 2 |
| 2 | [Processes & Inter-Process Communication](lectures/class-activity/class-activity2.md) | Processes & IPC (Linux + Windows) | Week 3–4 |
| 3 | [Socket Communication & Multithreading](lectures/class-activity/class-activity3.md) | Sockets, pthreads, Java threading, thread observation | Week 3–4 |
| 4 | [Shared File API](lectures/class-activity/class-activity4.md) | Client/server API, shared file, C++ mutex, Java synchronization | Week 7–8 |
| 5 | [Semaphores: Particle Pairs & HELLO Ordering](lectures/class-activity/class-activity5.md) | Producer/consumer semaphores, ordering constraints, deadlock checks | Week 8–9 |
| 6 | [Deadlock Simulation: Bank Account Transfers](lectures/class-activity/class-activity6.md) | Deadlock, circular wait, lock ordering, prevention | Week 9 |

→ Browse them in [`lectures/class-activity/`](lectures/class-activity/)

---

## �🛠️ Tools & Environment

| Tool | Purpose |
|------|---------|
| **WSL / Ubuntu** | Primary Linux environment for labs |
| **VS Code** | Code editor & Markdown documentation |
| **Git & GitHub** | Version control and submission |
| **GCC / Python3** | Programming & scripting |

---

## 🚀 Getting Started for Students

```bash
# 1. Clone the course repo for reference
$ git clone https://github.com/RathpiseyAlpha/ITC-OS-2026.git

# 2. Create your personal submission repo
$ mkdir -p os-se-<YourStudentID>/os-lab-<YourStudentID>/lab1
$ cd os-se-<YourStudentID>

# 3. Initialize git and connect to your GitHub repo
$ git init
$ git remote add origin https://github.com/<YourUsername>/OS-SE-<YourStudentID>.git

# 4. Start working on labs!

# 5. When class activities are assigned, create the activity folder you need:
$ mkdir -p os-class-activities-<YourStudentID>/activity6
```

### 📂 Your Submission Repo Structure

```
os-se-<YourStudentID>/
├── os-lab-<YourStudentID>/                # Lab submissions
│   ├── lab1/
│   │   ├── README.md                      # Submission with screenshots
│   │   └── ...
│   ├── lab2/
│   └── ...
│
└── os-class-activities-<YourStudentID>/   # Class activity submissions
    ├── activity1/
    │   ├── README.md                      # Screenshots + answers + reflection
    │   ├── screenshots/
    │   ├── task1/
    │   ├── task2/
    │   └── task3/
    ├── activity2/
    │   ├── README.md
    │   └── ...
    ├── activity3/
    │   ├── README.md
    │   └── ...
    ├── activity4/
    │   ├── README.md
    │   ├── screenshots/
    │   ├── cpp_before/
    │   ├── cpp_after/
    │   ├── java_before/
    │   └── java_after/
    ├── activity5/
    │   ├── README.md
    │   ├── screenshots/
    │   ├── task1_particles/
    │   └── task2_hello/
    ├── activity6/
    │   ├── README.md
    │   ├── screenshots/
    │   ├── task1_deadlock/
    │   └── task2_prevention/
    └── ...
```

> Each activity folder must contain a **README.md** with your name, student ID, and screenshot evidence of your programs running. Templates are provided in each activity's instructions.

---

<div align="center">

**Operating Systems — ITC 2026**

Made with 🖥️ at the Institute of Technology of Cambodia

</div>
