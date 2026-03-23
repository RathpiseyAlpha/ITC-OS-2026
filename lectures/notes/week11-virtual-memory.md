# Week 11 — Virtual Memory

> **Date**: _______________  
> **Lecturer**: Heng Rathpisey  
> **Slides**: [ch11.pdf](../files/ch11.pdf)

---

## 1. Overview

_Write a one-sentence summary of what this topic is about:_

> 

---

## 2. Key Concepts & Definitions

| Term | Definition (in your own words) |
|------|-------------------------------|
| Virtual Memory | |
| Demand Paging | |
| Page Fault | |
| TLB (Translation Lookaside Buffer) | |
| Page Replacement | |
| FIFO Replacement | |
| Optimal (OPT) Replacement | |
| LRU (Least Recently Used) | |
| Thrashing | |
| Working Set | |
| Belady's Anomaly | |
| Copy-on-Write | |

---

## 3. Detailed Notes

### 3.1 Virtual Memory Concept

> **🎣 Hook:** Your computer has 8GB of RAM, but you're running programs that collectively need 20GB. Yet nothing crashes. How is the OS conjuring memory that doesn't physically exist?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What is the key insight that makes virtual memory possible? (Hint: locality of reference.)
> - How does virtual memory separate the *user's view* of memory from *physical reality*?
> - What are the benefits beyond just "more memory" (e.g., sharing, protection)?
> - What is the role of disk in virtual memory?


### 3.2 Demand Paging

> **🎣 Hook:** Why load an entire program into memory if the user might only click one button? Demand paging says: don't load a page until the process actually *needs* it. What happens when it does need it and the page isn't there?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What is a "valid/invalid" bit in the page table and how does it enable demand paging?
> - What is the performance impact of a page fault? How many clock cycles does it cost?
> - What is the effective access time formula with page faults?
> - Why does demand paging work well in practice? (Hint: programs use only a fraction of their pages at any time.)


### 3.3 Page Fault Handling Steps

> **🎣 Hook:** A page fault is a controlled crash — the CPU tries to access a page that's not in memory, the hardware traps to the OS, and a complex sequence of steps kicks in. What are those steps, and how fast does this need to happen?

1. 
2. 
3. 
4. 
5. 
6. 

> **❓ Questions You Should Be Asking:**
> - What happens if there's no free frame available when a page fault occurs?
> - How does the OS know where to find the page on disk?
> - What must be saved/restored when restarting the faulting instruction?
> - Can a single instruction cause multiple page faults?

### 3.4 Page Replacement Algorithms

#### FIFO

> **🎣 Hook:** The simplest idea: replace the page that's been in memory the longest. But sometimes adding MORE frames makes FIFO perform WORSE. This counterintuitive phenomenon is called Bélády's anomaly. How is that even possible?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Why does FIFO suffer from Bélády's anomaly while other algorithms don't?
> - Is FIFO ever a good choice in practice?

#### Optimal

> **🎣 Hook:** If you could see the future, you'd always replace the page that won't be needed for the longest time. This is OPT — it's provably the best, and completely impossible to implement. So why study it?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Why is OPT useful as a benchmark even though it can't be implemented?
> - How close can real algorithms get to OPT's performance?

#### LRU

> **🎣 Hook:** Since we can't see the future, we look at the past: replace the page that hasn't been used for the longest time. LRU is the practical gold standard — but tracking "least recently used" accurately is more expensive than you'd think.

_Notes:_


> **❓ Questions You Should Be Asking:**
> - How can you implement LRU with a counter? With a stack?
> - Why is a pure LRU implementation too expensive for most systems?
> - What approximations of LRU do real operating systems use (e.g., clock algorithm, reference bits)?
> - Does LRU suffer from Bélády's anomaly?


### 3.5 Thrashing & Working Set Model

> **🎣 Hook:** Your system is busy — CPU utilization drops to 5%, the disk is grinding constantly, and nothing seems to get done. The OS thinks it needs more processes, so it loads more — making things even *worse*. This death spiral is called thrashing.

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Why does the OS's response to low CPU utilization (adding more processes) make thrashing worse?
> - What is the working set of a process and how does it relate to thrashing?
> - How does the working set model prevent thrashing?
> - What is the relationship between the degree of multiprogramming and CPU utilization?
> - At what point should the OS *stop* admitting new processes?


---

## 4. Diagrams & Visuals

### Page Fault Handling Diagram

```
[ Draw the steps from page fault to resuming the process ]
```

### Page Replacement Trace

```
Reference string: _______________
Frames = ___

FIFO:
[ Trace table ]
Page faults = 

LRU:
[ Trace table ]
Page faults = 

OPT:
[ Trace table ]
Page faults = 
```

---

## 5. Key Comparisons

| Algorithm | FIFO | OPT | LRU |
|-----------|------|-----|-----|
| Implementation | | | |
| Performance | | | |
| Belady's anomaly? | | | |
| Practical? | | | |

---

## 6. Examples

_Trace a reference string through each algorithm:_

Reference string: `7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1`  
Frames = 3

---

## 7. Review Questions

- [ ] What is demand paging and why is it beneficial?
- [ ] Walk through the page-fault handling steps.
- [ ] Why is OPT not implementable?
- [ ] What is Belady's anomaly and which algorithms exhibit it?
- [ ] How does the working set model prevent thrashing?

---

## 8. Connections to Other Topics

- **Previous week (Memory Management)**: Paging fundamentals.
- **Week 12 (File Systems)**: Swap space is on disk.
- **Week 5 (Scheduling)**: Thrashing affects CPU utilization.

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
