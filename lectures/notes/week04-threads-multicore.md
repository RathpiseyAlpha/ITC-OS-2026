# Week 4 — Threads & Multicore Programming

> **Date**: _______________  
> **Lecturer**: Heng Rathpisey  
> **Slides**: [ch4.pdf](../files/ch4.pdf)

---

## 1. Overview

_Write a one-sentence summary of what this topic is about:_

> 

---

## 2. Key Concepts & Definitions

| Term | Definition (in your own words) |
|------|-------------------------------|
| Thread | |
| Multithreading | |
| User-Level Thread | |
| Kernel-Level Thread | |
| Many-to-One Model | |
| One-to-One Model | |
| Many-to-Many Model | |
| Thread Pool | |
| Thread-Local Storage | |
| Amdahl's Law | |
| Data Parallelism | |
| Task Parallelism | |

---

## 3. Detailed Notes

### 3.1 Thread Concept — Why Threads?

_Notes:_


### 3.2 Multicore Programming Challenges

_Notes:_


### 3.3 Threading Models

_Notes:_


### 3.4 Thread Libraries (Pthreads, Windows, Java)

_Notes:_


### 3.5 Implicit Threading (Thread Pools, OpenMP)

_Notes:_


---

## 4. Diagrams & Visuals

### Single-threaded vs Multithreaded Process

```
[ Draw or describe the diagram here ]
```

### Threading Models Comparison

```
[ Draw Many-to-One, One-to-One, Many-to-Many diagrams ]
```

---

## 5. Key Comparisons

| Aspect | Process | Thread |
|--------|---------|--------|
| Memory space | | |
| Creation overhead | | |
| Communication | | |
| Context switch cost | | |

| Aspect | User-Level Threads | Kernel-Level Threads |
|--------|-------------------|---------------------|
| Managed by | | |
| Scheduling | | |
| Blocking behavior | | |

---

## 6. Examples

- **Pthread creation example**:
  ```c
  // Write or paste a short example
  ```

- **Amdahl's Law calculation**: If 75% of a program is parallelizable with 4 cores, speedup = ?

---

## 7. Review Questions

- [ ] Why are threads preferred over processes for concurrency?
- [ ] What are the challenges of multicore programming?
- [ ] Compare the three multithreading models.
- [ ] What is the benefit of a thread pool?
- [ ] Apply Amdahl's Law to a given scenario.

---

## 8. Connections to Other Topics

- **Previous week (Processes)**: Threads live within processes.
- **Week 7 (Critical Sections)**: Threads sharing data need synchronization.
- **Week 8 (Semaphores)**: Synchronization primitives for thread safety.

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
