# Week 10 — Memory Management I

> **Date**: _______________  
> **Lecturer**: Heng Rathpisey  
> **Slides**: [ch10.pdf](../files/ch10.pdf)

---

## 1. Overview

_Write a one-sentence summary of what this topic is about:_

> 

---

## 2. Key Concepts & Definitions

| Term | Definition (in your own words) |
|------|-------------------------------|
| Logical Address | |
| Physical Address | |
| Address Binding | |
| MMU (Memory Management Unit) | |
| Base & Limit Register | |
| Contiguous Allocation | |
| Paging | |
| Page Table | |
| Frame | |
| Internal Fragmentation | |
| External Fragmentation | |
| Swapping | |
| Compaction | |

---

## 3. Detailed Notes

### 3.1 Address Binding (Compile, Load, Execution Time)

> **🎣 Hook:** When you write `int x = 5;` in your program, the variable needs an actual address in physical memory. But *when* is that address decided — when you compile, when you load, or when you run? The answer determines how flexible your OS can be.

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What's the advantage of delaying address binding until execution time?
> - Why would compile-time binding ever be used? (Hint: embedded systems.)
> - What hardware support is needed for execution-time binding?
> - How does the loader participate in the binding process?


### 3.2 Logical vs Physical Address Space

> **🎣 Hook:** Every process thinks it owns all the memory in the world — from address 0 to some large number. But that's a lie. The real physical addresses are completely different. Who maintains this illusion, and how?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Why does the OS give each process its own private "logical" address space?
> - Who performs the translation from logical to physical — software or hardware?
> - What is the MMU and where does it sit in the system?
> - Can two processes have the same logical address pointing to different physical locations?


### 3.3 Contiguous Memory Allocation

> **🎣 Hook:** The simplest approach: give each process a single continuous block of memory. Easy to understand, fast to access — but over time, memory turns into Swiss cheese. Why?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What are the base and limit registers, and how do they provide protection?
> - What is the difference between first-fit, best-fit, and worst-fit allocation?
> - Which strategy produces the best memory utilization in practice?
> - Why does contiguous allocation inevitably lead to fragmentation?


### 3.4 Fragmentation

> **🎣 Hook:** You have 100MB free in memory, but the largest contiguous block is only 20MB. A 50MB process can't be loaded even though there's enough *total* space. This is external fragmentation — and it's a silent killer of memory efficiency.

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What's the difference between internal and external fragmentation?
> - Which types of allocation cause which types of fragmentation?
> - What is compaction, and why is it expensive?
> - How does paging solve the fragmentation problem?


### 3.5 Paging

> **🎣 Hook:** What if you could break a process into tiny fixed-size pieces and scatter them *anywhere* in physical memory? No more needing contiguous space, no more external fragmentation. That's paging — the foundation of modern memory management.

_Notes:_


> **❓ Questions You Should Be Asking:**
> - How does the page table map a logical page to a physical frame?
> - What is the "page offset" and why does it stay the same in logical and physical addresses?
> - What is a TLB, and why would address translation be unbearably slow without it?
> - What is the trade-off of small pages vs. large pages?
> - Does paging eliminate *all* fragmentation? (Hint: internal fragmentation still exists.)


### 3.6 Swapping

> **🎣 Hook:** What happens when your system runs out of physical memory but you still want to run more processes? The OS kicks some processes out to disk temporarily. But disk is 100,000x slower than RAM — how does this not destroy performance?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What gets swapped out — the entire process or just parts of it?
> - How does the OS decide which process to swap out?
> - What is the "swap space" on disk and how is it different from the file system?
> - How does swapping relate to the virtual memory concept we'll see next week?


---

## 4. Diagrams & Visuals

### Address Translation with MMU

```
[ Draw logical → physical address translation ]
```

### Paging: Page Table Lookup

```
Logical address: | page number | offset |
                       ↓
                  [ Page Table ]
                       ↓
Physical address: | frame number | offset |
```

---

## 5. Key Comparisons

| Aspect | Contiguous | Paging |
|--------|-----------|--------|
| Fragmentation type | | |
| External fragmentation? | | |
| Address translation | | |
| Memory utilization | | |

| Aspect | Internal Fragmentation | External Fragmentation |
|--------|----------------------|----------------------|
| Where it occurs | | |
| Cause | | |
| Solution | | |

---

## 6. Examples

- **Address translation calculation**: Given page size 4KB, translate logical address 13000.
- **Fragmentation example**:

---

## 7. Review Questions

- [ ] What is the difference between logical and physical addresses?
- [ ] When does address binding happen?
- [ ] How does paging eliminate external fragmentation?
- [ ] Calculate the physical address given a page table.
- [ ] What are the trade-offs of different page sizes?

---

## 8. Connections to Other Topics

- **Next week (Virtual Memory)**: Extends paging with demand paging.
- **Week 3 (Processes)**: Each process has its own address space.
- **Week 1 (Storage Hierarchy)**: Memory is part of the hierarchy.

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
