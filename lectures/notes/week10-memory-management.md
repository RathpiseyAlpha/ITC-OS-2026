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

_Notes:_


### 3.2 Logical vs Physical Address Space

_Notes:_


### 3.3 Contiguous Memory Allocation

_Notes:_


### 3.4 Fragmentation

_Notes:_


### 3.5 Paging

_Notes:_


### 3.6 Swapping

_Notes:_


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
