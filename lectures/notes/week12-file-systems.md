# Week 12 — File Systems

> **Date**: _______________  
> **Lecturer**: Heng Rathpisey  
> **Slides**: [ch12.pdf](../files/ch12.pdf)

---

## 1. Overview

_Write a one-sentence summary of what this topic is about:_

> 

---

## 2. Key Concepts & Definitions

| Term | Definition (in your own words) |
|------|-------------------------------|
| File | |
| Directory | |
| File Attributes (Metadata) | |
| File Access Methods | |
| Sequential Access | |
| Direct (Random) Access | |
| Disk Allocation Methods | |
| Contiguous Allocation | |
| Linked Allocation | |
| Indexed Allocation | |
| FAT (File Allocation Table) | |
| Inode | |
| Free Space Management | |
| ACL (Access Control List) | |

---

## 3. Detailed Notes

### 3.1 File Concept & Attributes

_Notes:_


### 3.2 File Access Methods

_Notes:_


### 3.3 Directory Structure

_Notes:_


### 3.4 Disk Space Allocation Methods

#### Contiguous Allocation

_Notes:_


#### Linked Allocation

_Notes:_


#### Indexed Allocation

_Notes:_


### 3.5 Free Space Management

_Notes:_


### 3.6 File System Security & Protection

_Notes:_


---

## 4. Diagrams & Visuals

### Directory Tree Structure

```
[ Draw a directory tree example ]
```

### Disk Allocation Comparison

```
[ Illustrate contiguous, linked, and indexed allocation on disk ]
```

---

## 5. Key Comparisons

| Aspect | Contiguous | Linked | Indexed |
|--------|-----------|--------|---------|
| Sequential access | | | |
| Random access | | | |
| Fragmentation | | | |
| Overhead | | | |

| Aspect | FAT | ext4 (inode-based) | NTFS |
|--------|-----|-------------------|------|
| OS | | | |
| Max file size | | | |
| Features | | | |

---

## 6. Examples

- **File permission example (Unix)**:
  ```
  rwxr-xr-- 
  Meaning: 
  ```

- **Indexed allocation block layout**:

---

## 7. Review Questions

- [ ] Compare sequential and direct access methods.
- [ ] What are the pros and cons of contiguous allocation?
- [ ] How does FAT work vs inode-based file systems?
- [ ] What are ACLs and how do they provide fine-grained access control?
- [ ] How is free space tracked on disk?

---

## 8. Connections to Other Topics

- **Week 2 (System Calls)**: File system calls (open, read, write, close).
- **Week 10 (Memory)**: Memory-mapped files bridge memory and file systems.
- **Week 9 (Deadlocks)**: File locking can cause deadlocks.

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
