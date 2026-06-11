# 🧪 Class Activities

This folder contains hands-on programming activities that accompany the lecture topics. Each activity gives you practical experience with the OS concepts covered in class.

## How to Use

1. Read the full activity instructions before starting.
2. Set up your environment (Linux VM, WSL, or native Linux).
3. Complete the **required tasks** first, then attempt the **optional/bonus** tasks.
4. Submit your code and report in your personal repo (see Submission below).

## Activities

| # | Activity | Related Lecture | Topic |
|---|----------|----------------|-------|
| 1 | [Class Activity 1](class-activity1.md) | Week 2 — OS Structures & Interfaces | System Calls with POSIX (Linux) |
| 2 | [Class Activity 2](class-activity2.md) | Week 3–4 — Processes & Threads | Processes & IPC (Linux + Windows) |
| 3 | [Class Activity 3](class-activity3.md) | Week 3–4 — Processes & Threads | Socket Communication & Multithreading |
| 4 | [Class Activity 4](class-activity4.md) | Week 7–8 — Critical Sections & Synchronization | Shared File API, C++ Mutex & Java Synchronization |
| 5 | [Class Activity 5](class-activity5.md) | Week 8–9 — Semaphores & Deadlocks | Particle Buffer Semaphores and HELLO Ordering |
| 6 | [Class Activity 6](class-activity6.md) | Week 9 — Deadlocks | Bank Transaction Deadlock Simulation |
| 7 | [Class Activity 7](class-activity7.md) | Week 9 — Deadlocks | Reasoning about deadlock — RAG & Banker's (no-code, uses visualizations) |
| 8 | [Class Activity 8](class-activity8.md) | Week 10–11 — Memory Management & Virtual Memory | Paging & Page Replacement — reason (hand-trace) + simulate |

_More activities will be added as the course progresses._

## Submission Structure

All class activities are submitted inside your personal `os-se-<YourStudentID>/` repository, in a dedicated folder that follows the same naming convention as your lab submissions:

```
os-se-<YourStudentID>/
├── os-lab-<YourStudentID>/                # Lab submissions (existing)
│   ├── lab1/
│   ├── lab2/
│   └── ...
│
└── os-class-activities-<YourStudentID>/   # Class activity submissions
    ├── activity1/
    │   ├── README.md              # ← Required: screenshots + answers + reflection
    │   ├── screenshots/           # Screenshot images
    │   ├── task1/                 # Source code for task 1
    │   ├── task2/                 # Source code for task 2
    │   └── task3/                 # Source code for task 3
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
    ├── activity7/
    │   ├── README.md              # ← Reasoning activity: written answers + traced tables
    │   └── screenshots/           # ← Your own screenshots from the visualizations
    ├── activity8/
    │   ├── README.md              # ← Part A hand-traces & predictions, Part C answers
    │   ├── screenshots/
    │   ├── task1_paging/          # ← Part B simulator source
    │   └── task2_demand_paging/
    └── ...
```

### Important Rules

- **Every activity folder must have a `README.md`** with your name, student ID, and embedded screenshots showing your programs running.
- A README template is provided in each activity's instruction file — copy and fill it in.
- Place screenshots in a `screenshots/` subfolder and reference them with relative paths.
- Commit and push regularly so your work is backed up.
