# Week 7 — Critical Sections

> **Date**: _______________  
> **Lecturer**: Heng Rathpisey  
> **Slides**: [ch7.pdf](../files/ch7.pdf)

---

## 1. Overview

_Write a one-sentence summary of what this topic is about:_

> 

---

## 2. Key Concepts & Definitions

| Term | Definition (in your own words) |
|------|-------------------------------|
| Critical Section | |
| Race Condition | |
| Mutual Exclusion | |
| Progress | |
| Bounded Waiting | |
| Peterson's Solution | |
| Test-and-Set | |
| Compare-and-Swap | |
| Mutex Lock | |
| Spinlock | |
| Busy Waiting | |

---

## 3. Detailed Notes

### 3.1 The Critical Section Problem

> **🎣 Hook:** Two threads both try to update the same bank balance at the same time. One adds $100, the other subtracts $50. The final balance? It depends on *who goes first* — and sometimes, the answer is just wrong. How do you prevent this chaos?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What exactly is a "critical section" — is it a concept or an actual piece of code?
> - Why doesn't this problem exist on a single-threaded system?
> - How does interleaving of instructions at the hardware level cause race conditions?
> - Can you always tell by looking at code whether it has a critical section problem?


### 3.2 Requirements for a Solution

> **🎣 Hook:** You can't just slap a lock on everything — a correct solution must satisfy *three* strict requirements. Miss even one, and your solution is broken. What are they, and why is each one essential?

_Notes:_

1. **Mutual Exclusion**:
2. **Progress**:
3. **Bounded Waiting**:

> **❓ Questions You Should Be Asking:**
> - If you only guarantee mutual exclusion but not progress, what goes wrong?
> - What does "bounded waiting" protect against — and for whom?
> - Can a solution satisfy mutual exclusion and progress but fail bounded waiting? Give an example.
> - Are these requirements sufficient for a *good* solution, or just a *correct* one?

### 3.3 Peterson's Solution

> **🎣 Hook:** In 1981, Gary Peterson came up with an elegant two-process solution using just two variables and no hardware support. It's beautiful, it works in theory — and it fails on modern CPUs. Why?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - How do the `flag[]` array and `turn` variable work together to guarantee mutual exclusion?
> - Why does Peterson's solution break on modern hardware? (Hint: instruction reordering.)
> - Does Peterson's solution satisfy all three requirements (mutual exclusion, progress, bounded waiting)?
> - Can Peterson's solution be extended to more than two processes?


### 3.4 Hardware Solutions (Test-and-Set, CAS)

> **🎣 Hook:** Software-only solutions are fragile. What if the CPU itself gave you an instruction that atomically checks-and-sets a value in one uninterruptible step? That's exactly what modern CPUs provide.

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Why must test-and-set be *atomic* — what breaks if it isn't?
> - How does Compare-and-Swap (CAS) differ from Test-and-Set?
> - Do hardware solutions alone satisfy bounded waiting? Why or why not?
> - What is the performance cost of these atomic instructions on multi-core systems?


### 3.5 Mutex Locks

> **🎣 Hook:** Atomic instructions are great for hardware, but programmers need something higher-level. Enter the mutex lock: `acquire()` before the critical section, `release()` after. Simple — but what happens if you forget to release?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What is the difference between a mutex and a spinlock?
> - When is busy waiting (spinning) acceptable, and when is it wasteful?
> - What happens if a thread holding a mutex crashes — is the lock released?
> - On a single-core system, does a spinlock ever make sense?


---

## 4. Diagrams & Visuals

### Critical Section Structure

```
do {
    [ entry section ]
        critical section
    [ exit section ]
        remainder section
} while (true);
```

### Race Condition Example

```
[ Illustrate a race condition with a shared counter ]
```

---

## 5. Key Comparisons

| Aspect | Peterson's | Test-and-Set | Mutex |
|--------|-----------|-------------|-------|
| Hardware support needed | | | |
| Busy waiting | | | |
| Number of processes | | | |

---

## 6. Examples

- **Race condition with shared counter**:
- **Peterson's solution walkthrough**:

---

## 7. Review Questions

- [ ] What are the three requirements for solving the critical section problem?
- [ ] Why is Peterson's solution not practical on modern hardware?
- [ ] How does test-and-set achieve mutual exclusion?
- [ ] What is the disadvantage of busy waiting?
- [ ] When would you use a spinlock vs a mutex?

---

## 8. Connections to Other Topics

- **Previous week (Scheduling)**: Scheduling determines when threads access critical sections.
- **Next week (Semaphores)**: Semaphores are a more powerful synchronization tool.
- **Week 4 (Threads)**: Threads in the same process share data — need synchronization.

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
