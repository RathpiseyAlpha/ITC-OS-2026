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

> **🎣 Hook:** A web browser loads images, renders HTML, and runs JavaScript all at the same time — within a *single process*. If a process can only do one thing at a time, how is this possible?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Why not just create more *processes* instead of threads?
> - What do threads share within a process, and what does each thread get its own copy of?
> - If threads share memory, what new dangers does that introduce?


### 3.2 Multicore Programming Challenges

> **🎣 Hook:** You buy a shiny 8-core processor, but your program only runs twice as fast. Why doesn't doubling the cores double the speed? What's the ceiling on parallelism?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What are the five key challenges of multicore programming?
> - How does Amdahl's Law define the limit on speedup from adding cores?
> - Is the bottleneck usually the parallel part or the serial part of a program?
> - Why is dividing work evenly across cores (load balancing) so difficult?


### 3.3 Threading Models

> **🎣 Hook:** The OS manages kernel threads, but your program might create user-level threads that the OS doesn't even know about. How do you map one world to the other — and why does the mapping strategy matter?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - In the Many-to-One model, what happens if one user thread blocks on I/O?
> - Why does the One-to-One model limit the number of threads you can create?
> - Which model gives the best concurrency, and what's the trade-off?
> - Which model does Linux use? What about Windows?


### 3.4 Thread Libraries (Pthreads, Windows, Java)

> **🎣 Hook:** Writing concurrent code means using a thread library — but the API you use on Linux looks completely different from Windows. Is there a universal way to think about threads across platforms?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What is Pthreads — an implementation or a specification?
> - How does Java's threading model abstract away OS-level threading details?
> - What function do you call to create a thread, and what must you pass to it?
> - How do you wait for a thread to finish, and why would you need to?


### 3.5 Implicit Threading (Thread Pools, OpenMP)

> **🎣 Hook:** Manually managing threads is hard and error-prone. What if the runtime or compiler could figure out the threading for you? That's the idea behind implicit threading — but what do you give up in return?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Why is creating a new thread for every request a bad idea (and how do thread pools solve it)?
> - What does OpenMP do when it sees `#pragma omp parallel`?
> - When should you use implicit threading vs. explicit thread management?
> - What is Grand Central Dispatch (GCD) and how does it differ from thread pools?


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
