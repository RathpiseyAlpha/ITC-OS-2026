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

> **🎣 Hook:** A mutex is like a bathroom lock — only one person at a time. But what if you have a parking lot with 10 spots? You need a counter that goes up and down atomically. That's a semaphore — and it's one of the most powerful tools in concurrent programming.

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Why are the operations called `wait()` and `signal()` (or `P()` and `V()`)?
> - What is the key invariant that a semaphore maintains?
> - What happens when `wait()` is called on a semaphore with value 0?
> - Can a different thread call `signal()` than the one that called `wait()`? (How does this differ from a mutex?)


### 3.2 Semaphore Implementation (with/without busy waiting)

> **🎣 Hook:** The simplest semaphore implementation spins in a loop wasting CPU cycles. Can we do better — can a waiting process actually *sleep* instead of spinning?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - How does the "sleeping" implementation use a waiting queue?
> - What happens if `signal()` is called when no process is waiting?
> - Which implementation (spinning vs. blocking) is better for short waits? For long waits?
> - How do you ensure that `wait()` and `signal()` themselves are atomic?


### 3.3 Classic Synchronization Problems

#### Producer-Consumer

> **🎣 Hook:** One thread produces data and puts it in a buffer; another thread takes data out. If the buffer is full, the producer must wait. If it's empty, the consumer must wait. How do you coordinate this dance without losing data or deadlocking?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - How many semaphores do you need for bounded-buffer producer-consumer? What does each one represent?
> - What goes wrong if you swap the order of `wait()` calls?
> - Can the buffer size be 1? What special case does that create?

#### Readers-Writers

> **🎣 Hook:** Multiple readers can safely read a database at the same time, but a writer needs exclusive access. How do you let readers in concurrently while still giving writers a chance to write?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - In the "first readers-writers" problem, can writers starve? Why?
> - What changes in the "second readers-writers" variant?
> - How does a read-write lock formalize this pattern in real systems?

#### Dining Philosophers

> **🎣 Hook:** Five philosophers sit at a round table, each needing two chopsticks to eat. If they all pick up their left chopstick at the same time, nobody can eat — ever. This toy problem captures a *real* and dangerous pattern in concurrent systems.

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Why does the naive solution ("pick up left, then right") deadlock?
> - What are at least three different strategies to prevent deadlock here?
> - How does this problem relate to real-world resource allocation?


### 3.4 Monitors

> **🎣 Hook:** Semaphores are powerful but dangerous — one misplaced `wait()` or `signal()` and you get deadlock or data corruption. Monitors wrap synchronization into a structured, object-oriented abstraction. Is there a catch?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - How does a monitor automatically enforce mutual exclusion?
> - What are condition variables, and how do `wait()` and `signal()` on a condition variable differ from semaphore operations?
> - What language features support monitors? (Think Java `synchronized`.)
> - Can you have deadlock with monitors? Under what conditions?


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
