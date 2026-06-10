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
| **Task 2** | **Hand-trace** the Banker's safety algorithm and requests on *your* personalized data | Filled work tables + tool screenshots |
| **Task 3** | Show that a **cycle is not always a deadlock** (multi-instance) | Two constructed scenarios + explanation |
| **Task 4** | Apply the concepts in writing | Short reasoned answers |

**Golden rule for every task: predict first, then verify.** Write your prediction *before* you press Play. If the tool disagrees with you, do **not** silently fix your answer — keep your prediction and add a short note explaining where your reasoning went wrong. That note is worth marks.

---

## Setup

No environment to install. Create a folder for your evidence:

```text
activity7/
├── report.md          (or report.pdf — your written answers and traced tables)
└── screenshots/       (your own screenshots from the tools)
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

## Task 2 — Hand-Tracing the Banker's Algorithm (personalized)

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

Write your two computed values at the top of Task 2 and use this scenario for everything below. (Changing only Max keeps Allocation ≤ Max and keeps Available unchanged, so your scenario is always valid — the tool will confirm.)

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

## Task 3 — A Cycle Is Not Always a Deadlock (multi-instance)

Tool: **deadlock-detection.html**. Here resources can have **multiple instances**, so a cycle is **necessary but not sufficient** for deadlock.

1. **Examples.** Open the **"Cycle, NO deadlock"** example and step through the reduction. In your own words: a cycle clearly exists — so **why is the system not deadlocked**? Name the process that finishes first and explain the role of the **spare instance**.
2. **One small change.** Switch to **"Cycle, deadlock"**. Identify the **single difference** between the two scenarios and explain why that one change makes the system deadlock.
3. **Build your own (different from the examples).** In **Build your own**, set at least one resource to have **2 or more instances** and construct a scenario that **has a cycle but is NOT deadlocked**. Screenshot it. Then make **one change** (e.g., add a request, or reduce an instance count) that turns it into a **deadlock**, and screenshot that. Explain what your change did in terms of the reduction algorithm (which process could no longer get `Request ≤ Work`).

---

## Task 4 — Apply the Concepts (short written answers)

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
screenshots/task2_safety.png          screenshots/task2_request_grant.png
screenshots/task2_request_deny.png    screenshots/task3_cycle_nodeadlock.png
screenshots/task3_deadlock.png
```

### Submission folder structure

```text
os-se-<YourStudentID>/
`-- os-class-activities-<YourStudentID>/
    `-- activity7/
        |-- report.md            (or report.pdf)
        `-- screenshots/
            |-- task1_graph1.png
            |-- task1_graph2.png
            |-- task1_build_deadlock.png
            |-- task1_build_nocycle.png
            |-- task2_safety.png
            |-- task2_request_grant.png
            |-- task2_request_deny.png
            |-- task3_cycle_nodeadlock.png
            `-- task3_deadlock.png
```

### Report template

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

## Task 2 — Banker's Algorithm (my personalized scenario)

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
![Safety check](screenshots/task2_safety.png)
Matched the tool? [...]

**Request I predicted GRANTED:** [process + vector], checks: [...]
![Grant](screenshots/task2_request_grant.png)

**Request I predicted DENIED:** [process + vector], which check failed / why unsafe: [...]
![Deny](screenshots/task2_request_deny.png)

---

## Task 3 — Cycle ≠ Deadlock

1. Why the "Cycle, NO deadlock" example is not deadlocked: [...]
2. The single change that causes deadlock: [...]
3. My own scenario:
![Cycle, no deadlock](screenshots/task3_cycle_nodeadlock.png)
My change that caused deadlock + why (reduction terms):
![Deadlock](screenshots/task3_deadlock.png)

---

## Task 4 — Applied Concepts
1. [...]  2. [...]  3. [...]  4. [...]  5. [...]
````

---

## Grading Criteria

| Criteria | Points | Description |
|----------|--------|-------------|
| **Task 1 predictions + verification** | 20 | Correct cycle/deadlock reasoning *and* a prediction recorded before verifying, with honest comparison notes. |
| **Task 1 constructed graphs** | 15 | Both built graphs meet the exact specification, with a correct one-line justification each. |
| **Task 2 hand trace** | 25 | Correct Need/Available, a complete Work-vector trace, and a valid safe sequence (or correct unsafe argument) for *your* personalized data. |
| **Task 2 requests** | 15 | One grant + one deny, each justified by the three checks, verified against the tool. |
| **Task 3 multi-instance** | 15 | Clear explanation of cycle ≠ deadlock and a self-built scenario flipped from no-deadlock to deadlock with a correct explanation. |
| **Task 4 applied concepts** | 10 | Reasoned, in-your-own-words answers using original examples. |
| **Total** | **100** | |

> Up to **20 points** may be deducted across the activity for answers that show only final values with **no reasoning or no predictions** — the point of this activity is your thinking, not the tool's output.

---

## Tips

- **Predict before you click.** The whole grade rests on your reasoning; the tool is the answer key, not the worker.
- Use the tools' **Prev/Next** buttons to study one step at a time — especially the **Work** vector growing in Banker's and the reduction in the multi-instance tool.
- A safe sequence is **not unique**. If yours differs from the tool's and both let every process finish, both are correct — say so.
- "Unsafe" never means "already deadlocked." It means the OS cannot *prove* everyone can finish, so it refuses the request to be safe.
- For Task 3, the easiest way to flip a no-deadlock scenario into a deadlock is to remove the spare instance or add a request that consumes the last free unit — watch what that does to `Available`.
- Keep your screenshots **yours**: they should show *your* personalized numbers and *your* constructed graphs, not the default examples.
