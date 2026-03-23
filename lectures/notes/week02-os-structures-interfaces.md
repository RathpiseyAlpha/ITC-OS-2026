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

> **🎣 Hook:** You open a file, print a document, and browse the web — all at the same time. Behind the scenes, who's coordinating all of this? What services does the OS quietly provide that you never think about?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What's the difference between services for the *user* vs. services for the *system*?
> - Which OS services are present on every operating system, regardless of type?
> - How does the OS decide which services to expose and which to hide?


### 3.2 System Calls

> **🎣 Hook:** Every time you write `printf("Hello")` in C, your program eventually asks the OS for help. But your code never calls the kernel directly — so how does the request actually get there?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Why can't user programs just call kernel functions directly?
> - What role does the trap instruction play in a system call?
> - How does a system call differ from a regular function call in terms of CPU mode?


### 3.3 Types of System Calls

> **🎣 Hook:** Every interaction between your program and the OS falls into one of six categories. Can you guess what they are just by thinking about what programs need to do?

_List and describe each category:_

| Category | Purpose | Examples |
|----------|---------|----------|
| Process Control | | |
| File Management | | |
| Device Management | | |
| Information Maintenance | | |
| Communication | | |
| Protection | | |

> **❓ Questions You Should Be Asking:**
> - Why does the OS group system calls into these specific categories?
> - What would happen if "Protection" system calls didn't exist?
> - Which category gets called most frequently during normal computer use?

### 3.4 System Call Implementation

> **🎣 Hook:** When you call `open()` in your program, a number gets passed to the kernel through a table. The program never needs to know *how* the OS opens the file. Why is this layer of indirection so powerful?

_How does a system call work step-by-step?_

1. 
2. 
3. 
4. 

> **❓ Questions You Should Be Asking:**
> - Why does the system call interface use numbers (indices) rather than direct function pointers?
> - How are parameters passed to the kernel — registers, stack, or memory block?
> - What happens if a program passes an invalid system call number?

### 3.5 OS Structures

> **🎣 Hook:** Should an OS be one giant program where everything can access everything? Or should it be split into tiny independent pieces? The answer shaped the design of every OS you use today.

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Why did early OS designers choose monolithic kernels if they're harder to maintain?
> - What's the real-world cost of message passing in a microkernel?
> - Why do most modern OS (Linux, Windows, macOS) end up as *hybrids*?
> - If you were designing an OS from scratch today, which structure would you pick and why?


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
