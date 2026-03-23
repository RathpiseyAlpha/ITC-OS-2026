# Week 9 — Deadlocks

> **Date**: _______________  
> **Lecturer**: Heng Rathpisey  
> **Slides**: [ch9.pdf](../files/ch9.pdf)

---

## 1. Overview

_Write a one-sentence summary of what this topic is about:_

> 

---

## 2. Key Concepts & Definitions

| Term | Definition (in your own words) |
|------|-------------------------------|
| Deadlock | |
| Mutual Exclusion | |
| Hold and Wait | |
| No Preemption | |
| Circular Wait | |
| Resource Allocation Graph | |
| Safe State | |
| Unsafe State | |
| Banker's Algorithm | |
| Deadlock Prevention | |
| Deadlock Avoidance | |
| Deadlock Detection | |
| Deadlock Recovery | |

---

## 3. Detailed Notes

### 3.1 Deadlock Conditions (All Four Required)

> **🎣 Hook:** Four cars arrive at a 4-way intersection at exactly the same time. Each waits for the car on their right to go first. Nobody moves — ever. This is deadlock, and it happens in your OS too. But what if you could guarantee even *one* of the four conditions doesn't hold?

1. **Mutual Exclusion**:
2. **Hold and Wait**:
3. **No Preemption**:
4. **Circular Wait**:

> **❓ Questions You Should Be Asking:**
> - Why must *all four* conditions hold simultaneously for deadlock?
> - Which condition is easiest to break in practice? Which is hardest?
> - Can deadlock happen with a single resource type?
> - How do you recognize these conditions in real code?

### 3.2 Resource Allocation Graph

> **🎣 Hook:** What if you could *draw* a picture of which process holds which resource and who's waiting for what — and just by looking at the graph, instantly tell whether deadlock exists?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What do the nodes and edges represent in a resource allocation graph?
> - Does a cycle in the graph *always* mean deadlock? When might it not?
> - How do you distinguish between a request edge and an assignment edge?
> - Can the graph help not just detect deadlock but also *prevent* it?


### 3.3 Deadlock Prevention

> **🎣 Hook:** If deadlock needs all four conditions, just make sure one can never happen. Sounds simple — but each prevention strategy comes with a painful trade-off. Which pain are you willing to accept?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - How do you prevent "Hold and Wait"? What's the downside?
> - How does imposing a total ordering on resources prevent "Circular Wait"?
> - Why is preventing "Mutual Exclusion" usually not practical?
> - Is prevention too restrictive for real-world systems?


### 3.4 Deadlock Avoidance — Banker's Algorithm

> **🎣 Hook:** A banker has limited cash and multiple customers with credit lines. The banker only approves a loan if, *after granting it*, there's still a way to satisfy everyone. This analogy is exactly how the OS can avoid deadlock — if it knows the future needs of every process.

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What information does the Banker's Algorithm need in advance?
> - What is a "safe state" vs. an "unsafe state"? Does unsafe always mean deadlock?
> - What is the time complexity of the Banker's Algorithm — is it practical for large systems?
> - How does the algorithm find a "safe sequence"?


### 3.5 Deadlock Detection & Recovery

> **🎣 Hook:** What if you don't prevent or avoid deadlock at all — you just let it happen, detect it, and then fix it? Most real operating systems actually take this approach. But "fixing" a deadlock means killing processes or rolling back — who pays the price?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - How often should the OS run the detection algorithm? What's the trade-off?
> - When deadlock is detected, which process should be terminated — and how do you choose?
> - What is the difference between process termination and resource preemption as recovery strategies?
> - Does the "ostrich algorithm" (ignoring deadlock) ever make sense?


---

## 4. Diagrams & Visuals

### Resource Allocation Graph (Deadlock Example)

```
[ Draw a resource allocation graph showing circular wait ]
```

### Banker's Algorithm Worked Example

```
Allocation | Max | Available
           |     |
           |     |

Need = Max - Allocation

Safe sequence: 
```

---

## 5. Key Comparisons

| Strategy | Prevention | Avoidance | Detection |
|----------|-----------|-----------|-----------|
| When applied | | | |
| Overhead | | | |
| Resource utilization | | | |
| Practical? | | | |

---

## 6. Examples

- **Banker's Algorithm worked example**:
- **Real-world deadlock scenario**:

---

## 7. Review Questions

- [ ] State the four necessary conditions for deadlock.
- [ ] How can you prevent deadlock by breaking each condition?
- [ ] Walk through Banker's Algorithm for a given scenario.
- [ ] How does the OS detect deadlock?
- [ ] What are the options for deadlock recovery?

---

## 8. Connections to Other Topics

- **Previous week (Semaphores)**: Incorrect semaphore usage causes deadlock.
- **Week 7 (Critical Sections)**: Locks can lead to deadlock if misused.
- **Week 3 (Processes)**: Deadlocked processes consume resources.

---

## 9. Reflection

_What was the most interesting part of this lecture?_

> 

_What concepts are still unclear?_

> 

_What do you want to explore further?_

> 

---

## 10. Summary

_Write a 3–5 sentence summary of this week's topic in your own words:_

> 
