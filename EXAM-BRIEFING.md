# OS Practical Final — Exam Briefing (read before you start)

**2 hours · Labs 5–10 · five parts (A–E) · individual · submit by `git push`.**

This page explains the rules and exactly how the exam runs. Read it **before** the
exam. You can watch your live status any time in the **📝 final exam** tab of the site.

---

## The five parts (100 marks)

| Part | Topic | Marks |
|:---:|---|:---:|
| **A** | Threads, kernel mapping & signals | 18 |
| **B** | Files, permissions & special bits | 18 |
| **C** | Bash scripting, PATH & safe file scanning | 22 |
| **D** | Concurrency, a race condition & file locking (`flock`) | 20 |
| **E** | Backups, archiving & `cron` automation | 22 |

Each part also carries part of its marks for **evidence (screenshots + reports)** and a
**short written answer**. Parts **A, D and E** additionally include a **live curveball**.

---

## How it runs (timeline)

1. **Your paper is sealed** until the start time. When the invigilator opens it, it
   appears at:
   ```
   ~/exam-paper/FINAL-EXAM.md
   ```
   Next to it is a starter pack — unzip it to get the answer skeletons:
   ```
   cd ~/<your-OS-SE-repo>/final-exam
   unzip ~/exam-paper/final-exam-templates.zip      # README.md, commands.md, live_mods.md
   ```
2. **Work inside your existing course repo** (the `OS-SE-…` / `os-se-…` folder in your
   home that has a `.git`), in a new top-level **`final-exam/`** folder. Follow the tree
   in the paper. Scripts are lowercase `snake_case` with **no `.sh` extension**.
3. **Live curveballs** are released **once, late in the exam** (see below).
4. **Submit by git push** of your course repo **before the end** — `git add` · `commit`
   · `push`. **Uncommitted / unpushed work is not graded.**
5. **At the finish, SSH access is blocked automatically** — push before then.

---

## What is a "curveball"?

A **curveball** is a **live modification task** handed out **partway through the exam**.
It is **not** printed in your paper and **cannot be prepared in advance**, because:

- it **edits an artefact you already built** (your own script / program), and
- it depends on **state that only exists on your machine at that moment** — your
  process IDs (PIDs), your current stock value, your timestamps.

There are **three curveballs — one each for Parts A, D and E.** They are released
**together, once**, at a single announced checkpoint, and you get **one combined
time-box (~20 minutes)** for all three. An answer that ignores your issued value, or
that could have been written *before* the announcement, **scores zero** for that
curveball.

You record each curveball in **`live_mods.md`**: the issued value, the exact command(s)
you ran, the **live value(s)** you acted on, and a `live_<letter>.png` screenshot.

### Where is the curveball file?

Until the checkpoint it is **sealed** (you'll get *Permission denied*). When the
invigilator releases it, read **your own** copy here:

```
/srv/exam/<your-server-username>/curveball.md
```

For example, just run:

```
cat /srv/exam/$(whoami)/curveball.md
```

It lists your three curveballs (A, D, E) and the **specific value** each one uses. If
the file still says permission denied after the checkpoint is announced, raise your
hand.

---

## Rules

- **Server only**, your own account. **No `sudo`** — every task is scoped to your own
  files and processes.
- **Individual work.** No partner tasks; sharing answers or files is misconduct.
- **Script naming:** lowercase `snake_case`, **no `.sh`** (a `do_thing.sh` scores zero
  for that deliverable).
- **AI tools are allowed**, but you must record the **exact commands you ran** in
  `commands.md`, answer the written questions with **your own scenario numbers**, and be
  ready to **explain any line** you submit. Generic answers that ignore your numbers earn
  nothing.
- **Submission is by `git push`** of your course repo (labs + activities + this exam).

---

## Your live dashboard

Log in to the site and open the **📝 final exam** tab to see, in real time:

- countdowns to **exam start**, **curveball release / close**, and **exam finish**,
- your **completion %** per part,
- your **paper**, **curveball**, and **SSH** status.

Good luck.
