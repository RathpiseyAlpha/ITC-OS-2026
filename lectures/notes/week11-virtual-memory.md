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

_Notes:_


### 3.2 Demand Paging

_Notes:_


### 3.3 Page Fault Handling Steps

1. 
2. 
3. 
4. 
5. 
6. 

### 3.4 Page Replacement Algorithms

#### FIFO

_Notes:_


#### Optimal

_Notes:_


#### LRU

_Notes:_


### 3.5 Thrashing & Working Set Model

_Notes:_


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
