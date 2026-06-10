# Class Activity 7 - Resource Allocation Graph & Banker's Algorithm

> **Related Lectures**: Week 9 - Deadlocks  
> **Topics**: Resource allocation graph (RAG), request vs assignment edges, cycle detection, deadlock detection, safe vs unsafe state, deadlock avoidance, Banker's Algorithm, safe sequence  
> **Language**: Any programming language  
> **Environment**: Linux, WSL, macOS, or Windows with any language runtime

---

## Objective

Activity 6 made a deadlock *happen* with two threads and account locks. This activity steps up a level: instead of producing a deadlock, you will **reason about** resource states the way the OS does — first by **detecting** deadlock from a graph, then by **avoiding** it before it can occur.

Task 1 builds a **Resource Allocation Graph (RAG)**. Processes and resources are nodes; a **request edge** points from a process to a resource it wants, and an **assignment edge** points from a resource to the process holding it. When every resource has a single instance, a **cycle in the graph means deadlock**. Your program will read a graph and report whether the system is deadlocked.

Task 2 builds the **Banker's Algorithm**. Like a cautious banker approving loans only when everyone can still be repaid, the OS grants a resource request only if the resulting state is **safe** — meaning at least one ordering of processes (a **safe sequence**) can finish. Your program will run the safety algorithm and decide whether a pending request can be granted.

By the end, you should be able to look at a resource state and say not just "is it deadlocked now?" but "could granting this request *lead* to deadlock?"

---

## Task Overview

| Task | What You Do | Screenshot Required |
|------|-------------|--------------------|
| **Task 1** | Build a Resource Allocation Graph deadlock detector (cycle detection) | Deadlocked graph + safe graph results |
| **Task 2** | Build the Banker's Algorithm (safety check + request decision) | Safe sequence + a granted and a denied request |
| **Task 3** | Explain detection vs avoidance using the lecture concepts | README answers |

You may use any programming language, but your README must clearly say which language you used and how to run each program.

---

## Setup

Create your activity folder:

```bash
mkdir -p activity7/{task1_rag,task2_bankers,screenshots}
cd activity7
```

Recommended filenames:

```text
task1_rag/rag_detector.<extension>
task2_bankers/bankers.<extension>
README.md
screenshots/task1_deadlocked.png
screenshots/task1_safe.png
screenshots/task2_safe_sequence.png
screenshots/task2_requests.png
```

Examples:

```text
rag_detector.py
RagDetector.java
bankers.cpp
Bankers.java
```

---

## Task 1: Resource Allocation Graph (Deadlock Detection)

### Goal

Write a program that reads a resource allocation graph and reports whether the system is **deadlocked**, by detecting a **cycle**.

### Graph Model

Use **single-instance resources** for this task (one unit per resource), so the rule is simple:

```text
A cycle in the graph  ==  deadlock
```

Nodes:

- Processes: `P1, P2, P3, ...`
- Resources: `R1, R2, R3, ...`

Edges:

| Edge | Direction | Meaning |
|------|-----------|---------|
| **Assignment edge** | `R -> P` | resource `R` is currently held by process `P` |
| **Request edge** | `P -> R` | process `P` is waiting for resource `R` |

### Required Behavior

Your program must:

- represent the graph (an edge list or adjacency list is fine)
- run on **two graphs**: one that is **deadlocked** (has a cycle) and one that is **safe** (no cycle)
- detect whether a cycle exists
- if deadlocked, print the cycle (the processes/resources involved)
- if not, print that no deadlock exists

### Required Test Graphs

**Graph A — Deadlocked (circular wait):**

```text
R1 -> P1     (R1 held by P1)
P1 -> R2     (P1 waits for R2)
R2 -> P2     (R2 held by P2)
P2 -> R1     (P2 waits for R1)
```

This forms the cycle `P1 -> R2 -> P2 -> R1 -> P1`.

**Graph B — Safe (no cycle):**

```text
R1 -> P1     (R1 held by P1)
P2 -> R1     (P2 waits for R1)
R2 -> P2     (R2 held by P2)
```

`P2` waits for `R1`, but `P1` is not waiting for anything, so `P1` will finish and release `R1`. No cycle.

You may add your own graphs, but you must keep at least one deadlocked and one safe case.

### Required Output Format

For the deadlocked graph, print exactly:

```text
Deadlock detected
```

Then print the cycle, for example:

```text
Cycle: P1 -> R2 -> P2 -> R1 -> P1
```

For the safe graph, print exactly:

```text
No deadlock detected
```

### Pseudocode

```text
build directed graph from edges (processes and resources are both nodes)

detect_cycle(graph):
    use DFS with a "visiting" / "visited" coloring
    if you revisit a node currently on the DFS stack -> cycle found

if detect_cycle(graph):
    print "Deadlock detected"
    print the cycle
else:
    print "No deadlock detected"
```

### Screenshots

Take two screenshots:

```text
screenshots/task1_deadlocked.png
screenshots/task1_safe.png
```

- The deadlocked screenshot must show `Deadlock detected` and the cycle.
- The safe screenshot must show `No deadlock detected`.

---

## Task 2: Banker's Algorithm (Deadlock Avoidance)

### Goal

Write a program that implements the **Banker's Algorithm**: given the current allocation state, determine whether the state is **safe** and find a **safe sequence**; then decide whether a specific resource **request** can be granted.

### Required Data

Use this classic configuration (5 processes, 3 resource types). It is a standard textbook state and is easy to verify:

```text
Total resources:  A=10  B=5  C=7

           Allocation        Max
Process    A   B   C       A   B   C
  P0       0   1   0       7   5   3
  P1       2   0   0       3   2   2
  P2       3   0   2       9   0   2
  P3       2   1   1       2   2   2
  P4       0   0   2       4   3   3
```

Your program must compute:

```text
Need = Max - Allocation

Available = Total - sum(Allocation per resource)
```

You may use your own data, but it must have multiple resource types and at least one valid safe sequence.

### Required Behavior — Part A: Safety Check

Run the safety algorithm on the initial state:

- compute `Need` and `Available`
- find a **safe sequence** (an order in which all processes can finish)
- print whether the state is **safe** or **unsafe**
- if safe, print the safe sequence

For the data above, `Available` starts at `A=3 B=3 C=2` and one valid safe sequence is:

```text
P1 -> P3 -> P4 -> P0 -> P2
```

(Other valid sequences may exist; any correct one is acceptable.)

### Required Behavior — Part B: Resource Request

Implement the **resource-request algorithm**. Given a request from a process:

1. If `Request > Need`, reject it (process exceeded its declared maximum).
2. If `Request > Available`, the process must wait (resources unavailable).
3. Otherwise, **pretend** to grant it (update Allocation, Need, Available) and run the safety check.
   - If the resulting state is **safe**, grant the request.
   - If it is **unsafe**, deny the request and roll back.

Test **two requests in order** and show both outcomes. The requests are sequential: evaluate Request 1 first, actually apply it if granted, then evaluate Request 2 on the **resulting** state:

```text
Request 1:  P1 requests (1, 0, 2)   -> should be GRANTED (resulting state is safe)
Request 2:  P0 requests (0, 2, 0)   -> should be DENIED  (resulting state is unsafe)
```

> Important: Request 2 is only unsafe **because Request 1 was granted first**. If you evaluate `P0 (0,2,0)` against the original state, it is actually safe. Apply the requests in order to reproduce the GRANTED-then-DENIED result.

### Required Output Format

For the safety check, print exactly one of:

```text
State is SAFE. Safe sequence: P1 -> P3 -> P4 -> P0 -> P2
```

```text
State is UNSAFE. No safe sequence exists.
```

For a request, print exactly one of:

```text
Request granted
```

```text
Request denied: would lead to an unsafe state
```

(or the appropriate `Request denied: exceeds maximum` / `Request denied: resources unavailable` message).

### Pseudocode

```text
safety_check(Available, Allocation, Need):
    Work = copy(Available)
    Finish[i] = false for all processes

    repeat:
        find a process i where Finish[i] == false AND Need[i] <= Work
        if found:
            Work = Work + Allocation[i]
            Finish[i] = true
            append i to safe_sequence
        else:
            break

    if all Finish are true:
        return SAFE, safe_sequence
    else:
        return UNSAFE

request(i, Req):
    if Req > Need[i]:  reject (exceeds maximum)
    if Req > Available: process must wait
    # tentative grant
    Available -= Req
    Allocation[i] += Req
    Need[i] -= Req
    if safety_check(...) == SAFE:
        grant
    else:
        roll back the tentative grant
        deny
```

### Screenshots

Take two screenshots:

```text
screenshots/task2_safe_sequence.png
screenshots/task2_requests.png
```

- The safe-sequence screenshot must show the Need matrix (or Available) and the `State is SAFE. Safe sequence: ...` line.
- The requests screenshot must show **both** the granted request and the denied request.

---

## Optional Extension: Make It Unsafe

After both tasks work, you may add one of the following:

1. **Force an unsafe state** in Task 2 by changing `Available` to `A=1 B=1 C=0` and re-running the safety check. Show that no safe sequence exists and the output is `State is UNSAFE`.

2. **Multi-instance detection** in Task 1: extend the detector to resources with multiple instances, where a cycle is *necessary but not sufficient* for deadlock. Show a graph with a cycle that is **not** deadlocked.

Optional screenshot:

```text
screenshots/task3_unsafe_or_multi.png
```

---

## Questions

Answer these in your `README.md`:

1. In Task 1, what is the difference between a **request edge** and an **assignment edge**?
2. In Task 1, why does a cycle guarantee deadlock when every resource has a **single instance**, but not when resources have **multiple instances**?
3. Which of the **four deadlock conditions** does a cycle in the RAG represent?
4. In Task 2, what does it mean for a state to be **safe**? Does an **unsafe** state always mean deadlock?
5. In Task 2, how does the safety algorithm choose the next process for the safe sequence?
6. Why does the Banker's Algorithm need each process's **maximum** demand declared **in advance**?
7. What is the key difference between deadlock **detection** (Task 1) and deadlock **avoidance** (Task 2)?

---

## Deliverables & Submission

### Required Screenshots

```text
screenshots/task1_deadlocked.png
screenshots/task1_safe.png
screenshots/task2_safe_sequence.png
screenshots/task2_requests.png
```

### Required Source Files

Submit your source files. Use names that match your language.

Examples:

```text
task1_rag/rag_detector.py
task2_bankers/bankers.py
```

or:

```text
task1_rag/RagDetector.java
task2_bankers/Bankers.java
```

### Submission Folder Structure

```text
os-se-<YourStudentID>/
`-- os-class-activities-<YourStudentID>/
    `-- activity7/
        |-- README.md
        |-- task1_rag/
        |   `-- rag_detector.<extension>
        |-- task2_bankers/
        |   `-- bankers.<extension>
        `-- screenshots/
            |-- task1_deadlocked.png
            |-- task1_safe.png
            |-- task2_safe_sequence.png
            `-- task2_requests.png
```

### README Template

````markdown
# Class Activity 7 - Resource Allocation Graph & Banker's Algorithm

- **Student Name:** [Your Name]
- **Student ID:** [Your ID]
- **Programming Language Used:** [Python / C / C++ / Java / Other]

---

## Task 1: Resource Allocation Graph (Detection)

![Deadlocked graph](screenshots/task1_deadlocked.png)
![Safe graph](screenshots/task1_safe.png)

- Edges of the deadlocked graph:
- Cycle detected:
- Edges of the safe graph:
- Why the safe graph has no cycle:

---

## Task 2: Banker's Algorithm (Avoidance)

![Safe sequence](screenshots/task2_safe_sequence.png)
![Requests](screenshots/task2_requests.png)

- Available at start:
- Safe sequence found:
- Request 1 (process + amount) and outcome:
- Request 2 (process + amount) and outcome:

---

## Questions

1. What is the difference between a request edge and an assignment edge?
2. Why does a cycle guarantee deadlock with single-instance resources but not with multiple instances?
3. Which of the four deadlock conditions does a cycle in the RAG represent?
4. What does it mean for a state to be safe? Does unsafe always mean deadlock?
5. How does the safety algorithm choose the next process for the safe sequence?
6. Why must each process's maximum demand be declared in advance?
7. What is the key difference between deadlock detection and deadlock avoidance?

---

## Reflection

_What did this activity teach you about how an OS can reason about deadlock before it happens, instead of only reacting after threads are already stuck?_
````

---

## Grading Criteria

| Criteria | Points | Description |
|----------|--------|-------------|
| **Task 1 graph + cycle detection** | 25 | Correctly models request/assignment edges and detects a cycle. |
| **Task 1 both cases** | 10 | Reports `Deadlock detected` (with cycle) and `No deadlock detected` for the two graphs. |
| **Task 2 safety check** | 25 | Correctly computes Need/Available and finds a valid safe sequence. |
| **Task 2 request decisions** | 20 | Correctly grants a safe request and denies an unsafe one with the right messages. |
| **Task 2 correctness of state** | 5 | Tentative grants are rolled back when a request is denied. |
| **README and screenshots** | 15 | Screenshots embedded, source files submitted, and questions answered clearly. |
| **Total** | **100** | |

---

## Tips

- In Task 1, treat processes and resources as **the same kind of node** in one directed graph; the cycle detector does not care which is which.
- A single-instance cycle means deadlock. If you do the multi-instance extension, remember a cycle is then only a *warning*, not a proof.
- In Task 2, the most common bug is forgetting to add a finished process's `Allocation` back into `Work` — that release is what lets the next process proceed.
- Always compute `Need = Max - Allocation` first; almost every safety check works off `Need`, not `Max`.
- When a request is denied for being unsafe, you **must roll back** the tentative changes to Allocation, Need, and Available, or the rest of your run will be wrong.
- A state being *unsafe* does not mean it is *deadlocked* — it means the OS cannot prove all processes can finish, so it refuses the request to stay on the safe side.
- This activity builds on Activity 6: there you *caused* a deadlock; here you *detect* and *avoid* one.
