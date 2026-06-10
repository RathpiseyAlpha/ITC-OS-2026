# Class Activity 7 - Reasoning About Deadlock: RAG &amp; Banker's Algorithm

> **Related Lectures**: Week 9 - Deadlocks  
> **Topics**: Resource allocation graph (RAG), request vs assignment edges, cycle detection, single- vs multi-instance resources, safe/unsafe state, Banker's Algorithm, safe sequence, deadlock avoidance vs detection  
> **Format**: **Reasoning activity — no programming.** You analyze, predict, hand-trace, construct, and explain. You use the interactive visualizations to *check* your work, not to do it for you.  
> **Tools**: The three deadlock visualizations (links below). Any browser.

---

## Why this activity has no coding

You could ask an AI to write a deadlock detector or a Banker's Algorithm implementation in ten seconds — so a coding task would prove nothing about *your* understanding. This activity instead asks you to **reason**: predict what will happen, trace the algorithms by hand, build scenarios that meet specific conditions, and explain *why*. Marks are awarded for **your shown reasoning and your own screenshots**, not for correct final numbers alone (the tools already give those). Pasting an AI answer without your own traced work and your own constructed scenarios will score poorly and is easy to spot.

> Be prepared to **explain any step of your submission out loud** if asked.

---

## 🎬 Interactive Visualizations (your checking tools)

- **Resource Allocation Graph** (single-instance): [open live](https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/rag-deadlock.html) · [source](../visualizations/rag-deadlock.html)
- **Banker's Algorithm**: [open live](https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/bankers-algorithm.html) · [source](../visualizations/bankers-algorithm.html)
- **Multi-Instance Deadlock Detection**: [open live](https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/deadlock-detection.html) · [source](../visualizations/deadlock-detection.html)

See [visualizations/README.md](../visualizations/README.md) for the GitHub Pages links and offline use.

---

## Task Overview

| Task | What you do | Evidence you submit |
|------|-------------|---------------------|
| **Task 1** | Analyze and **build** resource allocation graphs (single-instance) | Your predictions + tool screenshots |
| **Task 2** | Show that a **cycle is not always a deadlock** (multi-instance RAG) | Given scenario + constructed scenario + explanation |
| **Task 3** | **Hand-trace** the Banker's safety algorithm and requests on *your* personalized data | Filled work tables + tool screenshots |
| **Task 4** | **Model semaphore programs** as graphs and use the tools to decide if each can deadlock | YES/NO per case + tool screenshots |
| **Task 5** | Apply the concepts in writing | Short reasoned answers |

**Golden rule for every task: predict first, then verify.** Write your prediction *before* you press Play. If the tool disagrees with you, do **not** silently fix your answer — keep your prediction and add a short note explaining where your reasoning went wrong. That note is worth marks.

---

## Setup

No environment to install. Create a folder for your evidence:

```text
activity7/
|-- README.md          (your written answers and traced tables; README.pdf also accepted)
`-- screenshots/       (your own screenshots from the tools)
```

Hand-written traced tables are acceptable if you photograph them clearly and embed the image.

---

## Task 1 — Reasoning About Resource Allocation Graphs (single-instance)

Tool: **rag-deadlock.html** (use **Build your own** mode). All resources here are single-instance, so the rule is **a cycle = deadlock**.

### Part A — Predict, then verify

Two graphs are given as edge lists. Remember: `R → P` = *assignment* (held by), `P → R` = *request* (waiting for).

**Graph 1**
```text
R0 → P0      P0 → R1
R1 → P1      P1 → R2
R2 → P2      P2 → R0
```

**Graph 2**
```text
R0 → P0      P0 → R1
R1 → P1      P1 → R2
R2 → P2
```

For **each** graph, in your report:

1. **Predict (before the tool):** Is there a cycle? Is the system deadlocked? If deadlocked, write the cycle as a path (e.g., `P0 → R1 → P1 → … → P0`). If not, explain which process can finish first and why the others then unblock.
2. **Verify:** Rebuild the graph in the tool (add the processes, resources, and edges), step to the **Detection** step, and screenshot the result.
3. **Compare:** Did the tool match your prediction? If not, explain the gap in your reasoning.

> Tip: the tool auto-names nodes `P0, P1, …` and `R0, R1, …` — use the same names as the edge lists above.

### Part B — Construct to a specification

Using **Build your own**, create each of the following, then screenshot it at the Detection step and write one sentence explaining why it satisfies the requirement:

- **(i)** A **deadlocked** graph with **exactly 3 processes and 3 resources** whose cycle passes through **all three** processes.
- **(ii)** A graph with **at least 4 process/resource nodes** that has **no cycle** (no deadlock), in which **at least one** process is waiting for a resource.

A scenario where *nobody* is waiting does not count for (ii) — at least one request edge must exist, yet the system must still be deadlock-free.

---

## Task 2 — A Cycle Is Not Always a Deadlock (multi-instance RAG)

Tool: **deadlock-detection.html**. Here resources can have **multiple instances**, so a cycle is **necessary but not sufficient** for deadlock.

### Warm-up — the built-in examples

1. **Examples.** Open the **"Cycle, NO deadlock"** example and step through the reduction. In your own words: a cycle clearly exists — so **why is the system not deadlocked**? Name the process that finishes first and explain the role of the **spare instance**.
2. **One small change.** Switch to **"Cycle, deadlock"**. Identify the **single difference** between the two scenarios and explain why that one change makes the system deadlock.

### Part A — Predict, then verify (given scenario)

Here is a multi-instance system to analyze. `Allocation` = units currently held; `Request` = units each process is still waiting for. Use the tool's resource/process names (`R1, R2, R3` and `P1, P2, P3`).

```text
            Allocation            Request
            R1  R2  R3            R1  R2  R3
P1           1   0   0            0   1   0
P2           0   1   1            1   0   0
P3           1   0   1            0   0   0

Instances (Total):   R1 = 2,   R2 = 1,   R3 = 2
```

1. **Available.** Compute `Available = Total − Σ Allocation`. Show the arithmetic.
2. **Find the cycle.** There *is* a cycle here. Write it as a path (e.g., `P1 → R2 → P2 → … → P1`). Which process is in the cycle but can still finish, and why?
3. **Reduce by hand.** Set `Work = Available` and run the reduction. Fill this table in the order you reduce processes — a process can finish when its `Request ≤ Work`, then it returns its allocation to `Work`:

   | Step | Process chosen | Why Request ≤ Work? | Work after it releases |
   |------|----------------|---------------------|------------------------|
   | 1 | | | |
   | 2 | | | |
   | 3 | | | |

   State your conclusion: **DEADLOCKED** or **NOT deadlocked** (give the finishing order).
4. **Verify.** Enter the scenario in **Build your own** (add R3, set the **Instances** row to `2, 1, 2`, then fill Allocation and Request), step to **Detection**, and screenshot it. Did it match your hand trace?
5. **One change → deadlock.** Now change **only P3's request** from `R1 R2 R3 = 0 0 0` to `0 1 0` (P3 now also waits for `R2`). Predict the new outcome **before** re-running, then verify and screenshot. Explain *in reduction terms* why this one change deadlocks the system — i.e., which process could previously start the reduction, and why none can now satisfy `Request ≤ Work`.

### Part B — Build your own (different from Part A and the examples)

In **Build your own**, set at least one resource to have **2 or more instances** and construct a scenario that **has a cycle but is NOT deadlocked**. Screenshot it. Then make **one change** (e.g., add a request, or reduce an instance count) that turns it into a **deadlock**, and screenshot that. Explain what your change did in terms of the reduction algorithm (which process could no longer get `Request ≤ Work`).

---

## Task 3 — Hand-Tracing the Banker's Algorithm (personalized)

Tool: **bankers-algorithm.html** (use **Custom data**). The tool's default custom scenario already matches the base below, so you only edit two cells.

### Your personalized scenario

Base scenario (3 processes, 3 resource types; **Instances/Total** A=10, B=5, C=7):

```text
        Allocation            Max (base)
        A   B   C             A   B   C
P0      0   1   0             7   5   3
P1      2   0   0             3   2   2
P2      3   0   2             9   0   2
```

Let **a** = the **last digit** of your student ID, and **b** = the **second-to-last digit**.

Personalize the **Max** matrix (Allocation and Totals stay the same):

```text
Max[P0][A] = 7 + (a mod 3)
Max[P2][C] = 2 + (b mod 4)
```

Write your two computed values at the top of Task 3 and use this scenario for everything below. (Changing only Max keeps Allocation ≤ Max and keeps Available unchanged, so your scenario is always valid — the tool will confirm.)

### What to do — by hand first

1. **Need matrix.** Compute `Need = Max − Allocation` for all three processes. Show the full matrix.
2. **Available.** Compute `Available = Total − Σ Allocation`. Show the arithmetic.
3. **Safety by hand.** Decide whether your state is **safe**. Fill in this trace table *by hand*, in the order you select processes — show the **Work** vector after each process finishes:

   | Step | Process chosen | Why Need ≤ Work? | Work after it releases |
   |------|----------------|------------------|------------------------|
   | 1 | | | |
   | 2 | | | |
   | 3 | | | |

   State your conclusion: **SAFE** (give the safe sequence) or **UNSAFE** (explain why no process can proceed at some point).
4. **Verify safety.** Enter your scenario into the tool (Custom data → set the two Max cells → *Apply & Animate*, Safety check). Screenshot the final result. Note whether it matched your hand trace; if your safe sequence differs from the tool's, explain why **both can still be valid**.
5. **Requests (your choice).** Propose **two** resource requests on your scenario:
   - one you predict will be **granted**, and
   - one you predict will be **denied**.

   For each, show the reasoning by hand: check (1) `Request ≤ Need`, (2) `Request ≤ Available`, and (3) whether the tentative state is safe. State your verdict. Then verify each in the tool (**Resource request** mode) and screenshot it. Explain any request that was denied — *which* check failed, or *why* the tentative state was unsafe.

---

## Task 4 — Semaphores and Deadlock (model, then check with the tool)

These three sets of processes coordinate with **counting semaphores** (`wait`/`signal`). For each set you must decide: **can it deadlock?** Then you will model the worst-case interleaving in a tool and verify your answer.

> A semaphore deadlock is just a resource deadlock in disguise. Treat each **semaphore as a resource** whose **number of instances = its initial value**, and each **process as a process node**. Then it is exactly the graphs you built in Tasks 1 and 2.

### Modeling recipe (use for every case)

- A process that has run `wait(s)` but not yet the matching `signal(s)` **holds** one unit of `s` → assignment edge **`s → P`**.
- A process blocked at `wait(s)` is **requesting** `s` → request edge **`P → s`**.
- Build the **most dangerous snapshot**: let each process advance *in program order*, acquiring every semaphore it can, until it is blocked on the next `wait`. Then run **Detection**.
- "Can it deadlock?" means **does any reachable state contain an unbreakable cycle?** The tool only tells you whether the *snapshot you built* is deadlocked — so the reasoning (finding the bad interleaving) is yours; the tool confirms it.

### Which tool

- **Cases 1 and 2** — every semaphore starts at `1` (single-instance) → use **rag-deadlock.html** (Build your own).
- **Case 3** — `s1` starts at `2`, so that resource has **two instances** → use **deadlock-detection.html** (multi-instance). This is the same "spare instance" idea from Task 2.

### The three cases

**Case 1** — `s1 = 1, s2 = 1, s3 = 1`
```text
P1:            P2:            P3:
wait(s1)       wait(s2)       wait(s1)
wait(s2)       wait(s3)       wait(s2)
print("1")     print("2")     wait(s3)
signal(s2)     signal(s3)     print("3")
signal(s1)     signal(s2)     signal(s3)
                              signal(s2)
                              signal(s1)
```

**Case 2** — `s1 = 1, s2 = 1, s3 = 1` (only P3 changed — it now takes `s2 → s3 → s1`)
```text
P1:            P2:            P3:
wait(s1)       wait(s2)       wait(s2)
wait(s2)       wait(s3)       wait(s3)
print("1")     print("2")     wait(s1)
signal(s2)     signal(s3)     print("3")
signal(s1)     signal(s2)     signal(s1)
                              signal(s3)
                              signal(s2)
```

**Case 3** — same code as Case 2, but `s1 = 2, s2 = 1, s3 = 1`

For **each** case, in your report:

1. **Predict (before the tool):** Answer **YES** (can deadlock) or **NO** (cannot). If YES, give the interleaving and write the wait-for cycle (e.g., `P1 → s2 → P3 → s1 → P1`). If NO, explain *why* no cycle can form (hint: compare the **order** in which each process acquires its semaphores).
2. **Model & verify:** Build your most-dangerous snapshot in the correct tool (single- vs multi-instance), step to **Detection**, and screenshot the result.
3. **Confirm:** Does the tool agree a deadlock is reachable? For Case 3, explain in one sentence *what the extra instance of `s1` does* (which `wait` no longer blocks).

> Tip: when every process acquires its semaphores in the **same numeric order** (`s1` before `s2` before `s3`), a circular wait is impossible. Watch which case breaks that rule.

### Optional — run it yourself (confirmation only, not graded as code)

Want to *watch* the deadlock happen instead of only reasoning about it? Save the script below as `semaphore_deadlock.py` and run it with `python semaphore_deadlock.py`. It runs all three cases, deliberately inserting a tiny sleep after each `wait` to widen the race window, and uses a **2-second watchdog**: if the threads have not all finished, the case is reported as a deadlock. This only *confirms* your prediction — your marks still come from your reasoning and your tool screenshots, not from this output.

```python
import threading
import time

# Each process is a list of operations:
#   ('w', s) = wait(s)    ('s', s) = signal(s)    ('p', d) = print digit d
def run_case(title, inits, programs, timeout=2.0):
    sems = {name: threading.Semaphore(v) for name, v in inits.items()}
    finished = set()

    def worker(name, ops):
        for kind, arg in ops:
            if kind == 'w':
                sems[arg].acquire()
                time.sleep(0.02)        # widen the window so races actually occur
            elif kind == 's':
                sems[arg].release()
            elif kind == 'p':
                pass                    # this is where the process would print(arg)
        finished.add(name)

    threads = [threading.Thread(target=worker, args=(n, ops), name=n, daemon=True)
               for n, ops in programs.items()]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout)

    if len(finished) == len(programs):
        print(f"{title}: NO deadlock — all finished {sorted(finished)}")
    else:
        stuck = sorted(t.name for t in threads if t.is_alive())
        print(f"{title}: DEADLOCK — stuck: {stuck}; finished: {sorted(finished)}")

# P3 differs between the cases; P1 and P2 are the same throughout.
P1 = [('w','s1'),('w','s2'),('p','1'),('s','s2'),('s','s1')]
P2 = [('w','s2'),('w','s3'),('p','2'),('s','s3'),('s','s2')]
P3_case1 = [('w','s1'),('w','s2'),('w','s3'),('p','3'),('s','s3'),('s','s2'),('s','s1')]
P3_case2 = [('w','s2'),('w','s3'),('w','s1'),('p','3'),('s','s1'),('s','s3'),('s','s2')]

run_case("Case 1 (s1=s2=s3=1)",
         {'s1':1,'s2':1,'s3':1},
         {'P1':P1, 'P2':P2, 'P3':P3_case1})

run_case("Case 2 (s1=s2=s3=1)",
         {'s1':1,'s2':1,'s3':1},
         {'P1':P1, 'P2':P2, 'P3':P3_case2})

run_case("Case 3 (s1=2)",
         {'s1':2,'s2':1,'s3':1},
         {'P1':P1, 'P2':P2, 'P3':P3_case2})
```

Because deadlock is a *race*, run the script a few times. One case should reliably hang (the watchdog reports `DEADLOCK`), while the other two always finish — and that pattern should match the YES/NO answers you derived by hand. If a case you predicted as deadlocking happens to slip through and finish, run it again; the bug is still there, the schedule just got lucky.

---

## Task 5 — Apply the Concepts (short written answers)

Answer in your own words. Where a scenario is asked for, **do not reuse the textbook 4-way-intersection example** — invent your own (e.g., from printers, database locks, a kitchen, road traffic).

1. State the **four necessary conditions** for deadlock, and map each one to a single concrete situation you invent. Which **one** condition would be easiest to remove in your situation, and what would that cost?
2. In a **single-instance** RAG, a cycle proves deadlock. In a **multi-instance** system it does not. Explain the difference in one or two sentences.
3. What is the difference between an **unsafe state** and a **deadlocked state**? Give a one-line example of a state that is unsafe but not (yet) deadlocked.
4. Compare deadlock **avoidance** (Banker's) with deadlock **detection + recovery**. Name one cost of each, and one kind of system where you would choose each.
5. Why does the Banker's Algorithm require each process to declare its **maximum** demand in advance? What real-world problem does that requirement cause?

---

## Deliverables & Submission

Submit a written report and your own screenshots — **no source code**.

### Required screenshots (your own, from the tools)

```text
screenshots/task1_graph1.png          screenshots/task1_graph2.png
screenshots/task1_build_deadlock.png  screenshots/task1_build_nocycle.png
screenshots/task2_given_nodeadlock.png    screenshots/task2_given_deadlock.png
screenshots/task2_cycle_nodeadlock.png    screenshots/task2_deadlock.png
screenshots/task3_safety.png              screenshots/task3_request_grant.png
screenshots/task3_request_deny.png        screenshots/task4_case1.png
screenshots/task4_case2.png               screenshots/task4_case3.png
```

### Submission folder structure

```text
os-se-<YourStudentID>/
└── os-class-activities-<YourStudentID>/
    └── activity7/
        ├── README.md                  # ← your written answers + traced tables (README.pdf also accepted)
        └── screenshots/               # your own screenshots from the tools
            ├── task1_graph1.png
            ├── task1_graph2.png
            ├── task1_build_deadlock.png
            ├── task1_build_nocycle.png
            ├── task2_given_nodeadlock.png
            ├── task2_given_deadlock.png
            ├── task2_cycle_nodeadlock.png
            ├── task2_deadlock.png
            ├── task3_safety.png
            ├── task3_request_grant.png
            ├── task3_request_deny.png
            ├── task4_case1.png
            ├── task4_case2.png
            └── task4_case3.png
```

### README Template

````markdown
# Class Activity 7 - Reasoning About Deadlock

- **Student Name:** [Your Name]
- **Student ID:** [Your ID]
- **My personalization:** a = [last digit], b = [second-to-last digit]

---

## Task 1 — Resource Allocation Graphs

### Part A
**Graph 1 — my prediction:** [cycle? deadlock? the cycle path / why not]
![Graph 1](screenshots/task1_graph1.png)
Matched the tool? [yes/no — if no, what I got wrong]

**Graph 2 — my prediction:** [...]
![Graph 2](screenshots/task1_graph2.png)
Matched the tool? [...]

### Part B
**(i) Deadlocked 3×3 graph** — edges I used + why it deadlocks:
![Built deadlock](screenshots/task1_build_deadlock.png)

**(ii) No-cycle graph (≥4 nodes, ≥1 request)** — why it is deadlock-free:
![Built no-cycle](screenshots/task1_build_nocycle.png)

---

## Task 2 — Cycle ≠ Deadlock

**Warm-up (built-in examples)**
1. Why the "Cycle, NO deadlock" example is not deadlocked: [...]
2. The single change that causes deadlock: [...]

**Part A — given scenario**
- Available = Total − ΣAlloc = [...]
- The cycle (as a path): [...]   Process in the cycle that can still finish + why: [...]

| Step | Process | Why Request ≤ Work | Work after release |
|------|---------|--------------------|--------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

Conclusion: [DEADLOCKED / NOT deadlocked — finishing order = …]
![Given scenario](screenshots/task2_given_nodeadlock.png)
After changing P3's request to `0 1 0` — my prediction + why it deadlocks (reduction terms):
![Given scenario, deadlock](screenshots/task2_given_deadlock.png)

**Part B — my own scenario**
![Cycle, no deadlock](screenshots/task2_cycle_nodeadlock.png)
My change that caused deadlock + why (reduction terms):
![Deadlock](screenshots/task2_deadlock.png)

---

## Task 3 — Banker's Algorithm (my personalized scenario)

- Max[P0][A] = 7 + (a mod 3) = [...]   Max[P2][C] = 2 + (b mod 4) = [...]
- **Need matrix:** [...]
- **Available:** Total − ΣAlloc = [...]

**Safety trace (by hand):**

| Step | Process | Why Need ≤ Work | Work after release |
|------|---------|-----------------|--------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

Conclusion: [SAFE — safe sequence = … / UNSAFE — because …]
![Safety check](screenshots/task3_safety.png)
Matched the tool? [...]

**Request I predicted GRANTED:** [process + vector], checks: [...]
![Grant](screenshots/task3_request_grant.png)

**Request I predicted DENIED:** [process + vector], which check failed / why unsafe: [...]
![Deny](screenshots/task3_request_deny.png)

---

## Task 4 — Semaphores and Deadlock

**Case 1 (s1=s2=s3=1) — my answer:** [YES / NO] — interleaving + wait-for cycle, or why no cycle can form:
![Case 1](screenshots/task4_case1.png)
Tool confirmed? [...]

**Case 2 (s1=s2=s3=1) — my answer:** [YES / NO] — [...]
![Case 2](screenshots/task4_case2.png)
Tool confirmed? [...]

**Case 3 (s1=2) — my answer:** [YES / NO] — what the extra instance of s1 does:
![Case 3](screenshots/task4_case3.png)
Tool confirmed? [...]

---

## Task 5 — Applied Concepts
1. [...]  2. [...]  3. [...]  4. [...]  5. [...]

---

## Reflection

_What did this activity teach you about why a cycle does not always mean deadlock, and about the trade-off between deadlock avoidance (Banker's) and detection + recovery in real systems such as databases or operating systems?_
````

---

## Grading Criteria

| Criteria | Points | Description |
|----------|--------|-------------|
| **Task 1 predictions + verification** | 15 | Correct cycle/deadlock reasoning *and* a prediction recorded before verifying, with honest comparison notes. |
| **Task 1 constructed graphs** | 15 | Both built graphs meet the exact specification, with a correct one-line justification each. |
| **Task 2 multi-instance** | 15 | Correct reduction on the given scenario *and* a self-built scenario flipped from no-deadlock to deadlock, each with a clear cycle ≠ deadlock explanation. |
| **Task 3 hand trace** | 20 | Correct Need/Available, a complete Work-vector trace, and a valid safe sequence (or correct unsafe argument) for *your* personalized data. |
| **Task 3 requests** | 15 | One grant + one deny, each justified by the three checks, verified against the tool. |
| **Task 4 semaphores** | 10 | Correct YES/NO for all three cases, each modeled in the right (single- vs multi-instance) tool with the deadlock interleaving or the ordering argument shown. |
| **Task 5 applied concepts** | 10 | Reasoned, in-your-own-words answers using original examples. |
| **Total** | **100** | |

> Up to **20 points** may be deducted across the activity for answers that show only final values with **no reasoning or no predictions** — the point of this activity is your thinking, not the tool's output.

---

## Tips

- **Predict before you click.** The whole grade rests on your reasoning; the tool is the answer key, not the worker.
- Use the tools' **Prev/Next** buttons to study one step at a time — especially the **Work** vector growing in Banker's and the reduction in the multi-instance tool.
- A safe sequence is **not unique**. If yours differs from the tool's and both let every process finish, both are correct — say so.
- "Unsafe" never means "already deadlocked." It means the OS cannot *prove* everyone can finish, so it refuses the request to be safe.
- For Task 2, the easiest way to flip a no-deadlock scenario into a deadlock is to remove the spare instance or add a request that consumes the last free unit — watch what that does to `Available`.
- Keep your screenshots **yours**: they should show *your* personalized numbers and *your* constructed graphs, not the default examples.
