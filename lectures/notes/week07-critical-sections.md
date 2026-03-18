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

_Notes:_


### 3.2 Requirements for a Solution

_Notes:_

1. **Mutual Exclusion**:
2. **Progress**:
3. **Bounded Waiting**:

### 3.3 Peterson's Solution

_Notes:_


### 3.4 Hardware Solutions (Test-and-Set, CAS)

_Notes:_


### 3.5 Mutex Locks

_Notes:_


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
