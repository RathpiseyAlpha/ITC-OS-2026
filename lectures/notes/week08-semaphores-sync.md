# Week 8 — Semaphores & Synchronization Problems

> **Date**: _______________  
> **Lecturer**: Heng Rathpisey  
> **Slides**: [ch8.pdf](../files/ch8.pdf)

---

## 1. Overview

_Write a one-sentence summary of what this topic is about:_

> 

---

## 2. Key Concepts & Definitions

| Term | Definition (in your own words) |
|------|-------------------------------|
| Semaphore | |
| Counting Semaphore | |
| Binary Semaphore | |
| `wait()` / `P()` | |
| `signal()` / `V()` | |
| Monitor | |
| Condition Variable | |
| Producer-Consumer Problem | |
| Readers-Writers Problem | |
| Dining Philosophers Problem | |

---

## 3. Detailed Notes

### 3.1 Semaphore Operations

_Notes:_


### 3.2 Semaphore Implementation (with/without busy waiting)

_Notes:_


### 3.3 Classic Synchronization Problems

#### Producer-Consumer

_Notes:_


#### Readers-Writers

_Notes:_


#### Dining Philosophers

_Notes:_


### 3.4 Monitors

_Notes:_


---

## 4. Diagrams & Visuals

### Producer-Consumer with Bounded Buffer

```
[ Draw the buffer, producer, consumer, and semaphores ]
```

### Dining Philosophers Layout

```
[ Draw 5 philosophers and 5 chopsticks ]
```

---

## 5. Key Comparisons

| Aspect | Binary Semaphore | Counting Semaphore | Mutex | Monitor |
|--------|-----------------|-------------------|-------|---------|
| Values | | | | |
| Use case | | | | |
| Deadlock risk | | | | |

---

## 6. Examples

- **Producer-Consumer pseudocode**:
- **Dining Philosophers solution**:

---

## 7. Review Questions

- [ ] How do `wait()` and `signal()` work on a semaphore?
- [ ] How do you solve Producer-Consumer with semaphores?
- [ ] What causes deadlock in the Dining Philosophers problem?
- [ ] What advantage do monitors have over semaphores?
- [ ] Can a semaphore be used as a mutex? How?

---

## 8. Connections to Other Topics

- **Previous week (Critical Sections)**: Semaphores solve critical section problems.
- **Next week (Deadlocks)**: Improper use of semaphores can cause deadlocks.
- **Week 4 (Threads)**: Synchronization is essential for multithreaded programs.

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
