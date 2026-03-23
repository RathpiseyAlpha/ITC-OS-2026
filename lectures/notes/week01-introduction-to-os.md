# Week 1 — Introduction to Operating Systems

> **Date**: _______________  
> **Lecturer**: Heng Rathpisey  
> **Slides**: [ch1.pdf](../files/ch1.pdf)

---

## 1. Overview

_Write a one-sentence summary of what this topic is about:_

> 

---

## 2. Key Concepts & Definitions

| Term | Definition (in your own words) |
|------|-------------------------------|
| Operating System | |
| Kernel | |
| Von Neumann Architecture | |
| Interrupt | |
| Trap (Software Interrupt) | |
| Dual-Mode Operation | |
| User Mode vs Kernel Mode | |
| Bootstrap / Booting | |
| System Bus | |
| Device Controller | |
| DMA (Direct Memory Access) | |

---

## 3. Detailed Notes

### 3.1 What is an Operating System?

> **🎣 Hook:** Every time you click a file, type a letter, or open an app — something invisible is making it all work. What is it, and what would happen if it didn't exist?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Is the OS just the kernel, or does it include everything that ships with the system?
> - Can a computer run without an OS? What would that look like?
> - Who decides what counts as part of the OS vs. an application?


### 3.2 Computer System Organization

> **🎣 Hook:** Your computer has a CPU, memory, disk, keyboard, and screen — but how do they actually talk to each other without stepping on each other's toes?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Why can't the CPU just talk directly to every device?
> - What role does the system bus play in connecting components?
> - How does the device controller offload work from the CPU?


### 3.3 Interrupts and I/O

> **🎣 Hook:** Imagine you're writing an essay and someone taps your shoulder — you pause, deal with it, then go back to writing. That's exactly how the CPU handles I/O. But what if 10 people tap your shoulder at once?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What happens if two interrupts arrive at the same time?
> - How does the CPU know *where* to go when an interrupt occurs?
> - Why is polling less efficient than interrupt-driven I/O?
> - What is the interrupt vector table and why does it matter?


### 3.4 Storage Hierarchy

> **🎣 Hook:** Why can't we just make all memory as fast as CPU registers? If we could, operating systems would be dramatically simpler. So what's stopping us?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Why is there a trade-off between speed, size, and cost?
> - Where does caching fit in the hierarchy, and who manages it?
> - What happens when data is needed but it's in a slower layer?
> - How does the OS decide what stays in memory vs. what goes to disk?


### 3.5 Dual-Mode Operation & Protection

> **🎣 Hook:** What stops a buggy app from crashing your entire computer or a malicious program from reading your passwords straight from memory?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What would happen if there were no distinction between user mode and kernel mode?
> - How does the CPU physically enforce mode switching?
> - What triggers a transition from user mode to kernel mode?
> - Can a program ever *stay* in kernel mode? Should it?


### 3.6 Bootstrap Process

> **🎣 Hook:** When you press the power button, the CPU has no idea what to do — there's nothing in memory. So how does the OS "pull itself up by its own bootstraps"?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Where is the boot loader stored and why can't it be in RAM?
> - What is the exact sequence from power-on to a running OS?
> - What happens if the boot loader is corrupted?
> - Why is the bootstrap called a "chicken-and-egg" problem?


---

## 4. Diagrams & Visuals

_Sketch or describe key diagrams from the lecture:_

### Computer System Architecture Diagram

```
[ Draw or describe the diagram here ]
```

### Storage Hierarchy Pyramid

```
[ Draw or describe the diagram here ]
```

### Interrupt Timeline

```
[ Draw or describe the diagram here ]
```

---

## 5. Key Comparisons

| Aspect | User Mode | Kernel Mode |
|--------|-----------|-------------|
| Access level | | |
| Instructions allowed | | |
| Example operations | | |

| Aspect | Hardware Interrupt | Software Interrupt (Trap) |
|--------|-------------------|--------------------------|
| Triggered by | | |
| Purpose | | |
| Example | | |

---

## 6. Examples

_Write concrete examples for the concepts above:_

- **Interrupt example**:
- **Dual-mode switching example**:
- **DMA example**:

---

## 7. Review Questions

- [ ] What are the four main components of a computer system?
- [ ] Why does an OS need dual-mode operation?
- [ ] What happens when a hardware interrupt occurs?
- [ ] Describe the boot process from power-on to user login.
- [ ] How does the storage hierarchy balance speed and capacity?

---

## 8. Connections to Other Topics

- **Next week (OS Structures)**: How does the OS interface with user programs?
- **Week 3 (Processes)**: How do interrupts relate to process scheduling?

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
