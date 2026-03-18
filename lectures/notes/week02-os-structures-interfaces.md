# Week 2 — OS Structures & Interfaces

> **Date**: _______________  
> **Lecturer**: Heng Rathpisey  
> **Slides**: [ch2.pdf](../files/ch2.pdf)

---

## 1. Overview

_Write a one-sentence summary of what this topic is about:_

> 

---

## 2. Key Concepts & Definitions

| Term | Definition (in your own words) |
|------|-------------------------------|
| System Call | |
| API (Application Programming Interface) | |
| System Call Interface | |
| Monolithic Kernel | |
| Layered Architecture | |
| Microkernel | |
| Hybrid Kernel | |
| Loadable Kernel Module (LKM) | |
| Shell | |
| Command Interpreter | |
| POSIX | |

---

## 3. Detailed Notes

### 3.1 Operating System Services

_Notes:_


### 3.2 System Calls

_Notes:_


### 3.3 Types of System Calls

_List and describe each category:_

| Category | Purpose | Examples |
|----------|---------|----------|
| Process Control | | |
| File Management | | |
| Device Management | | |
| Information Maintenance | | |
| Communication | | |
| Protection | | |

### 3.4 System Call Implementation

_How does a system call work step-by-step?_

1. 
2. 
3. 
4. 

### 3.5 OS Structures

_Notes:_


---

## 4. Diagrams & Visuals

### System Call Flow Diagram

```
[ User Program ] → [ API call ] → [ System Call Interface ] → [ Kernel ] → [ Hardware ]

Expand and annotate this diagram:
```

### OS Structure Comparison

```
[ Draw monolithic vs microkernel vs layered architecture here ]
```

---

## 5. Key Comparisons

| Aspect | Monolithic | Layered | Microkernel | Hybrid |
|--------|-----------|---------|-------------|--------|
| Performance | | | | |
| Modularity | | | | |
| Security | | | | |
| Complexity | | | | |
| Real-world example | | | | |

| Aspect | System Call | Library Function |
|--------|-----------|-----------------|
| Runs in | | |
| Overhead | | |
| Example | | |

---

## 6. Examples

_Write concrete examples:_

- **System call in Linux (file operation)**:
  ```c
  // Example:
  ```

- **System call in Windows**:
  ```c
  // Example:
  ```

- **The path from `printf()` to actual I/O**:

---

## 7. Review Questions

- [ ] What is the difference between a system call and an API?
- [ ] List the six categories of system calls with one example each.
- [ ] Trace the execution path of `open()` from user space to kernel.
- [ ] Compare monolithic kernel and microkernel — advantages and disadvantages.
- [ ] Why do modern operating systems use hybrid approaches?
- [ ] What is the role of the system call interface?

---

## 8. Connections to Other Topics

- **Previous week (Intro to OS)**: Dual-mode operation enables system calls.
- **Next week (Processes)**: System calls are used to create and manage processes.
- **Week 7 (Synchronization)**: System calls provide synchronization primitives.

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
