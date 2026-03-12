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

---

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
│   │   └── ch4.pdf            #   Ch 4 — Threads & Multicore
│   └── class-activity/        # In-class exercises (TBA)
│
└── labs/
    ├── lab1/                  # Lab 1 — Exploring OS Basics
    │   ├── lab1-instruction.md
    │   ├── README.md
    │   ├── guides/
    │   └── pictures/
    ├── lab2/                  # Lab 2 — (Coming Soon)
    │   └── lab2-instruction.md
    ├── lab3/                  # Lab 3 — (Coming Soon)
    │   └── lab3-instruction.md
    ├── lab4/                  # Lab 4 — (Coming Soon)
    └── lab5/                  # Lab 5 — (Coming Soon)
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
| 5 | CPU Scheduling I | *Coming Soon* | — |
| 6 | CPU Scheduling II | *Coming Soon* | — |
| 7 | Critical Sections | *Coming Soon* | — |
| 8 | Semaphores & Sync Problems | *Coming Soon* | — |
| 9 | Deadlocks | *Coming Soon* | — |
| 10 | Memory Management I | *Coming Soon* | — |
| 11 | Virtual Memory | *Coming Soon* | — |
| 12 | File Systems | *Coming Soon* | — |

> 📋 See the full [course-outline.md](course-outline.md) for detailed weekly learning objectives.

---

## 🔬 Labs

| Lab | Title | Status | Link |
|:---:|-------|:------:|:----:|
| 1 | Exploring Operating System Basics | ✅ Available | [Instructions](labs/lab1/lab1-instruction.md) |
| 2 | *TBA* | 🔜 Coming Soon | [Placeholder](labs/lab2/) |
| 3 | *TBA* | 🔜 Coming Soon | [Placeholder](labs/lab3/) |
| 4 | *TBA* | 🔜 Coming Soon | [Placeholder](labs/lab4/) |
| 5 | *TBA* | 🔜 Coming Soon | [Placeholder](labs/lab5/) |

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

---

## 📚 Lecture Slides

| Chapter | Topic | Download |
|:-------:|-------|:--------:|
| 1 | Introduction to Operating Systems | [📄 ch1.pdf](lectures/files/ch1.pdf) |
| 2 | OS Structures & Interfaces | [📄 ch2.pdf](lectures/files/ch2.pdf) |
| 3 | Processes | [📄 ch3.pdf](lectures/files/ch3.pdf) |
| 4 | Threads & Multicore Programming | [📄 ch4.pdf](lectures/files/ch4.pdf) |

> More chapters will be added as the course progresses.

---

## 🛠️ Tools & Environment

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
```

---

<div align="center">

**Operating Systems — ITC 2026**

Made with 🖥️ at the Institute of Technology of Cambodia

</div>
