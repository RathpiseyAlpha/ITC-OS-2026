# Week 3 — Processes

> **Date**: _______________  
> **Lecturer**: Heng Rathpisey  
> **Slides**: [ch3.pdf](../files/ch3.pdf)

---

## 1. Overview

_Write a one-sentence summary of what this topic is about:_

> 

---

## 2. Key Concepts & Definitions

| Term | Definition (in your own words) |
|------|-------------------------------|
| Process | |
| Process Control Block (PCB) | |
| Process State | |
| Context Switch | |
| Process Scheduling | |
| Ready Queue | |
| Wait Queue | |
| Parent / Child Process | |
| `fork()` | |
| `exec()` | |
| `wait()` | |
| Orphan Process | |
| Zombie Process | |

---

## 3. Detailed Notes

### 3.1 Process Concept

> **🎣 Hook:** Right now, your computer is running hundreds of processes. But a program sitting on disk is just a file — so what transforms a lifeless file into a living, running process?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What's the difference between a *program* and a *process*?
> - Can two processes run the same program? What would differ between them?
> - What constitutes a process beyond just the code — what other state does it carry?


### 3.2 Process States & Transitions

> **🎣 Hook:** A process is born, gets ready, runs, sometimes waits, and eventually dies. But what *triggers* each of these transitions? Can a process skip a state?

_Notes:_

| State | Description |
|-------|-------------|
| New | |
| Ready | |
| Running | |
| Waiting | |
| Terminated | |

> **❓ Questions You Should Be Asking:**
> - Can a process go from "Waiting" directly to "Running"? Why or why not?
> - What event moves a process from "Running" to "Ready"?
> - What happens to a process's data when it's in the "Waiting" state?
> - Is there a limit to how many processes can be in the "Ready" state?

### 3.3 Process Control Block (PCB)

> **🎣 Hook:** The OS juggles hundreds of processes, pausing and resuming them constantly. How does it remember exactly where each process left off and what it was doing?

_What does a PCB contain?_


> **❓ Questions You Should Be Asking:**
> - Why is the PCB sometimes called the most important data structure in the OS?
> - What would happen if the PCB was lost or corrupted for a running process?
> - How large is a typical PCB, and where is it stored in memory?


### 3.4 Process Scheduling

> **🎣 Hook:** Your CPU can only run *one* process at a time (per core), but it feels like everything runs simultaneously. How does the OS create this illusion?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What's the difference between the job queue, ready queue, and device queue?
> - Who decides which process runs next — the OS or the hardware?
> - How often does the OS make scheduling decisions, and what triggers them?


### 3.5 Process Creation & Termination

> **🎣 Hook:** In Unix, every process has a parent, forming a tree that traces all the way back to process #1. What happens when a parent dies before its children? Or a child dies but nobody collects its exit status?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What exactly does `fork()` duplicate — everything, or just some parts?
> - Why does `fork()` return two different values (one to parent, one to child)?
> - What's the difference between an orphan process and a zombie process?
> - Why would a parent call `wait()` on its child?


### 3.6 Interprocess Communication (IPC)

> **🎣 Hook:** Processes run in isolated memory spaces for safety — but sometimes they *need* to talk to each other. How do you let processes communicate without breaking the isolation that protects them?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - When would you choose shared memory over message passing, and vice versa?
> - Who sets up the shared memory region — the OS or the processes themselves?
> - Is message passing always slower than shared memory? Under what conditions?
> - How does a pipe or socket relate to these two IPC models?


---

## 4. Diagrams & Visuals

### Process State Diagram

```
[ Draw the 5-state process diagram with transitions here ]
```

### Context Switch Diagram

```
[ Draw or describe the context switch between two processes ]
```

---

## 5. Key Comparisons

| Aspect | Shared Memory | Message Passing |
|--------|--------------|-----------------|
| Speed | | |
| Ease of use | | |
| Synchronization | | |
| Use case | | |

---

## 6. Examples

- **`fork()` example**:
  ```c
  // Describe what happens:
  ```

- **Process state transitions for opening a file**:

---

## 7. Review Questions

- [ ] What are the five states of a process?
- [ ] What information does a PCB contain and why?
- [ ] What happens during a context switch?
- [ ] What does `fork()` return to the parent vs the child?
- [ ] Compare shared memory and message passing for IPC.

---

## 8. Connections to Other Topics

- **Previous week (OS Structures)**: System calls create/manage processes.
- **Next week (Threads)**: Threads exist within a process.
- **Week 5 (Scheduling)**: The scheduler decides which process runs next.

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
