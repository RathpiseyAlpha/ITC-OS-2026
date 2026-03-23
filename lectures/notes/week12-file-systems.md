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

> **🎣 Hook:** You think of a file as "that essay I saved on my desktop." But to the OS, a file is an abstract container with metadata, access permissions, and a location on disk. What makes a file more than just its contents?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What attributes (metadata) does the OS store about every file?
> - What is the difference between a file's *name* and its *identifier* (inode number)?
> - How does the OS distinguish between file types — by extension, magic number, or metadata?
> - Where are file attributes stored — in the file itself or in a separate structure?


### 3.2 File Access Methods

> **🎣 Hook:** Reading a file from start to end is easy. But what if you need byte #50,000 in a 1GB file — do you really have to read through the first 49,999 bytes to get there?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What's the difference between sequential and direct (random) access?
> - Which access method do databases need, and why?
> - How does the OS support "seeking" to a position in a file?
> - What is indexed access and when is it used?


### 3.3 Directory Structure

> **🎣 Hook:** Your files are organized in folders inside folders — a tree structure. But the earliest systems had a single flat list of files for the whole disk. What problems did that cause, and what design evolution led to the directory trees we have today?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What are the trade-offs between single-level, two-level, and tree-structured directories?
> - How do hard links and symbolic links work within a directory structure?
> - What happens if the directory structure allows cycles (acyclic-graph vs. general graph)?
> - How does the OS resolve a path like `/home/user/docs/file.txt` to an actual file on disk?


### 3.4 Disk Space Allocation Methods

#### Contiguous Allocation

> **🎣 Hook:** Store each file in a single continuous run of blocks on disk — fast to read, but what happens when the file grows and there's no room next to it?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Why is contiguous allocation excellent for sequential *and* random access?
> - What is the external fragmentation problem with this approach?
> - How does the OS handle file growth under contiguous allocation?

#### Linked Allocation

> **🎣 Hook:** Each block contains a pointer to the next block — like a linked list. No fragmentation, but what happens if one pointer in the chain gets corrupted?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Why is linked allocation terrible for random access?
> - How does FAT (File Allocation Table) improve on basic linked allocation?
> - What is the reliability concern with pointer chains on disk?

#### Indexed Allocation

> **🎣 Hook:** What if you gave each file its own "index block" that lists all its data blocks? Random access is fast again — but now every file needs at least one extra block just for its index. Is the overhead worth it?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - How does the inode in Unix/Linux implement indexed allocation?
> - What are direct, indirect, double-indirect, and triple-indirect blocks?
> - What is the maximum file size supported by the index block structure?
> - Why is this the dominant approach in modern file systems?


### 3.5 Free Space Management

> **🎣 Hook:** When you delete a file, the blocks are freed — but how does the OS keep track of which blocks are free and which are used? The strategy affects both performance and how fast you can create new files.

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What are the pros and cons of a bitmap vs. a linked list for free space?
> - How does grouping or counting improve the linked-list approach?
> - When a file is deleted, is the data actually erased? (Security implication!)
> - How does the free space management strategy affect allocation speed?


### 3.6 File System Security & Protection

> **🎣 Hook:** On a shared Linux server, your classmates should be able to read your public webpage but not your private notes. The file system must enforce *who* can do *what* to every file. How does it pull this off?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - How does the Unix permission model (rwx for owner/group/other) work?
> - What are the limitations of basic Unix permissions vs. ACLs?
> - What does the `setuid` bit do and why is it a security concern?
> - How does Windows NTFS handle permissions differently from Unix?


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
