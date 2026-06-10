# Class Activity 8 - Memory Management & Virtual Memory Simulators

> **Related Lectures**: Week 10 - Memory Management, Week 11 - Virtual Memory  
> **Topics**: Logical vs physical addresses, paging, address translation, page tables, internal fragmentation, demand paging, page faults, page replacement (FIFO, LRU, OPT)  
> **Language**: Any programming language  
> **Environment**: Linux, WSL, macOS, or Windows with any language runtime

---

## Objective

In this activity, you will turn two core memory ideas into running programs.

Task 1 makes the **paging illusion** visible. Every process believes it owns a clean, continuous block of memory starting at address `0`. In reality the OS scatters the process across physical frames and uses a **page table** to translate each logical address into a physical address. Your program will perform that translation, the same way the MMU does in hardware.

Task 2 makes **virtual memory** visible. Physical memory is smaller than the addresses a process can use, so the OS keeps only some pages in memory and fetches the rest from disk on demand. When a needed page is not resident, a **page fault** occurs and a **page replacement algorithm** decides which resident page to evict. Your program will run a reference string through FIFO and LRU and count the page faults.

By the end, you should understand how an address becomes a physical location, and why the choice of replacement algorithm changes how often a process touches the disk.

---

## Task Overview

| Task | What You Do | Screenshot Required |
|------|-------------|--------------------|
| **Task 1** | Build a paging address-translation simulator | Translation table + invalid-access message |
| **Task 2** | Build a demand-paging simulator with FIFO and LRU page replacement | Per-step trace + page-fault counts |
| **Task 3** | Explain your results using the lecture concepts | README answers |

You may use any programming language, but your README must clearly say which language you used and how to run each program.

---

## Setup

Create your activity folder:

```bash
mkdir -p activity8/{task1_paging,task2_demand_paging,screenshots}
cd activity8
```

Recommended filenames:

```text
task1_paging/paging_translation.<extension>
task2_demand_paging/page_replacement.<extension>
README.md
screenshots/task1_translation.png
screenshots/task2_fifo.png
screenshots/task2_lru.png
```

Examples:

```text
paging_translation.py
PagingTranslation.java
paging_translation.c
page_replacement.cpp
```

---

## Task 1: Paging Address-Translation Simulator

### Goal

Write a program that translates **logical addresses** into **physical addresses** using a page table, exactly the way an MMU does.

### Memory Model

Use a small, easy-to-check configuration:

```text
Page size:            16 bytes
Logical address space: 8 pages   (logical addresses 0 .. 127)
Physical memory:       8 frames  (physical addresses 0 .. 127)
```

Define a page table that maps some pages to frames. Leave at least one page **invalid** (not loaded) so you can demonstrate an invalid reference:

```text
Page | Frame | Valid?
-----+-------+-------
  0  |   5   |  yes
  1  |   2   |  yes
  2  |   1   |  yes
  3  |   -   |  no     (not in memory)
  4  |   7   |  yes
  5  |   3   |  no     (not in memory)
  6  |   0   |  yes
  7  |   4   |  yes
```

You may choose your own page size, table, and mappings, but you **must** keep at least one invalid page.

### Translation Rule

For a logical address `LA` and page size `P`:

```text
page_number = LA / P        (integer division)
offset      = LA % P
```

Look up `page_number` in the page table:

- If the page is **valid**, the physical address is:

  ```text
  physical_address = (frame_number * P) + offset
  ```

- If the page is **invalid**, do not translate. Print the required message instead (see below).

### Required Behavior

Your program must:

- store the page size, the page table, and the valid bits
- translate a **list of at least 6 logical addresses**, including at least one that lands on an **invalid** page
- for each valid address, print the page number, offset, frame number, and final physical address
- for each invalid address, print the required invalid-access message
- report the **internal fragmentation** for one allocation (see questions)

### Required Output Format

For a valid translation, print a clear breakdown, for example:

```text
Logical 20  -> page 1, offset 4  -> frame 2 -> physical 36
Logical 100 -> page 6, offset 4  -> frame 0 -> physical 4
```

For an invalid reference, print exactly:

```text
Page fault: page not in memory
```

(In Task 1 this stands for an invalid/not-resident page. In Task 2 you will actually handle the fault.)

### Pseudocode

```text
P = 16
page_table = { 0:5, 1:2, 2:1, 4:7, 6:0, 7:4 }   # only valid pages
addresses  = [20, 100, 48, 16, 127, 80]          # 48 and 80 hit invalid pages

for LA in addresses:
    page   = LA / P
    offset = LA % P
    if page is in page_table:
        frame    = page_table[page]
        physical = frame * P + offset
        print translation breakdown
    else:
        print "Page fault: page not in memory"
```

### Screenshot

Take one screenshot:

```text
screenshots/task1_translation.png
```

Your screenshot must show:

- the page table or configuration printed
- at least 6 logical addresses translated
- at least one valid translation with its full breakdown
- at least one `Page fault: page not in memory` message

---

## Task 2: Demand Paging & Page Replacement Simulator

### Goal

Simulate **demand paging** with a limited number of physical frames. Run the same reference string through **FIFO** and **LRU**, count page faults, and print a per-step trace.

### Required Configuration

Use this reference string and frame count (the same one from the Week 11 notes), so your results are easy to check:

```text
Reference string: 7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1
Number of frames: 3
```

The simulation starts with **all frames empty**. Loading a page into an empty frame still counts as a page fault (this is a cold-start / demand-paging fault).

### Required Behavior

For **each** algorithm (FIFO and LRU), your program must:

- process the reference string one page at a time
- for each reference, decide **HIT** (page already resident) or **FAULT** (page not resident)
- on a fault, load the page; if all frames are full, evict the victim chosen by the algorithm
- print the frame contents after each reference
- print whether each reference was a HIT or FAULT
- print the **total page-fault count** at the end

### Algorithm Rules

| Algorithm | Victim chosen on a full-memory fault |
|-----------|--------------------------------------|
| **FIFO**  | the page that has been resident the **longest** (oldest load time) |
| **LRU**   | the page that was **least recently used** (oldest last-access time) |

In LRU, **every reference** — both hits and faults — updates how recently a page was used.

### Required Output Format

Print a readable trace, for example:

```text
=== FIFO ===
Ref 7 | FAULT | frames: [7, _, _]
Ref 0 | FAULT | frames: [7, 0, _]
Ref 1 | FAULT | frames: [7, 0, 1]
Ref 2 | FAULT | frames: [2, 0, 1]   (evicted 7)
Ref 0 | HIT   | frames: [2, 0, 1]
...
Total page faults (FIFO): 15
```

### Pseudocode

```text
frames = empty list of size N
faults = 0

for page in reference_string:
    if page in frames:
        record HIT
        (LRU only: mark page as just used)
    else:
        record FAULT
        faults += 1
        if frames not full:
            add page
        else:
            victim = choose_victim()      # FIFO: oldest loaded; LRU: oldest used
            replace victim with page
    print step trace

print total faults
```

### Required Comparison

After both runs, print a one-line comparison, for example:

```text
FIFO faults: 15 | LRU faults: 12
```

> Note: with 3 frames and the reference string above, FIFO and LRU produce **different** fault counts. Your numbers should reflect that difference — if they are identical, check your eviction logic.

### Screenshots

Take two screenshots:

```text
screenshots/task2_fifo.png
screenshots/task2_lru.png
```

Each screenshot must show:

- the reference string and number of frames
- the per-step HIT/FAULT trace with frame contents
- the total page-fault count for that algorithm

---

## Optional Extension: Optimal (OPT) & Belady's Anomaly

After FIFO and LRU work, you may add either or both:

1. **OPT** — on a fault with full memory, evict the page whose **next use is farthest in the future** (or never used again). Compare its fault count to FIFO and LRU. It should be the lowest.

2. **Belady's anomaly** — run **FIFO** with the reference string `1 2 3 4 1 2 5 1 2 3 4 5` using **3 frames**, then **4 frames**. Show that 4 frames produces **more** faults than 3 — the counterintuitive anomaly discussed in lecture.

Optional screenshot:

```text
screenshots/task3_opt_or_belady.png
```

---

## Questions

Answer these in your `README.md`:

1. In Task 1, why does the **offset** stay the same in the logical and the physical address?
2. In Task 1, for page size 16 bytes, what is the largest valid offset, and how many bits are needed for the offset?
3. In Task 1, if a process needs 70 bytes and the page size is 16 bytes, how many pages are allocated and how much **internal fragmentation** results?
4. Why is paging free of **external** fragmentation, while contiguous allocation is not?
5. In Task 2, why does loading a page into an empty frame still count as a page fault?
6. In Task 2, why does **LRU** generally cause fewer faults than **FIFO** on this reference string?
7. What is **thrashing**, and how would it appear if you ran Task 2 with too few frames for the process's working set?

---

## Deliverables & Submission

### Required Screenshots

```text
screenshots/task1_translation.png
screenshots/task2_fifo.png
screenshots/task2_lru.png
```

### Required Source Files

Submit your source files. Use names that match your language.

Examples:

```text
task1_paging/paging_translation.py
task2_demand_paging/page_replacement.py
```

or:

```text
task1_paging/PagingTranslation.java
task2_demand_paging/PageReplacement.java
```

### Submission Folder Structure

```text
os-se-<YourStudentID>/
`-- os-class-activities-<YourStudentID>/
    `-- activity8/
        |-- README.md
        |-- task1_paging/
        |   `-- paging_translation.<extension>
        |-- task2_demand_paging/
        |   `-- page_replacement.<extension>
        `-- screenshots/
            |-- task1_translation.png
            |-- task2_fifo.png
            `-- task2_lru.png
```

### README Template

````markdown
# Class Activity 8 - Memory Management & Virtual Memory

- **Student Name:** [Your Name]
- **Student ID:** [Your ID]
- **Programming Language Used:** [Python / C / C++ / Java / Other]

---

## Task 1: Paging Address-Translation Simulator

![Address translation](screenshots/task1_translation.png)

- Page size used:
- Number of pages / frames:
- Page table (page -> frame):
- Example valid translation (show the full breakdown):
- Invalid reference shown:
- Internal fragmentation for a 70-byte process:

---

## Task 2: Demand Paging & Page Replacement

![FIFO trace](screenshots/task2_fifo.png)
![LRU trace](screenshots/task2_lru.png)

- Reference string:
- Number of frames:
- FIFO total page faults:
- LRU total page faults:
- Which algorithm performed better, and why:

---

## Questions

1. In Task 1, why does the offset stay the same in the logical and the physical address?
2. For page size 16 bytes, what is the largest valid offset, and how many bits are needed for the offset?
3. If a process needs 70 bytes with 16-byte pages, how many pages are allocated and how much internal fragmentation results?
4. Why is paging free of external fragmentation, while contiguous allocation is not?
5. Why does loading a page into an empty frame still count as a page fault?
6. Why does LRU generally cause fewer faults than FIFO on this reference string?
7. What is thrashing, and how would it appear with too few frames?

---

## Reflection

_What did these simulators teach you about how the OS turns the illusion of a large, private address space into real physical memory and disk?_
````

---

## Grading Criteria

| Criteria | Points | Description |
|----------|--------|-------------|
| **Task 1 translation correctness** | 25 | Correctly computes page number, offset, frame, and physical address for valid references. |
| **Task 1 invalid handling** | 10 | Detects invalid/not-resident pages and prints the required message. |
| **Task 2 FIFO** | 20 | Correct FIFO eviction, per-step trace, and fault count. |
| **Task 2 LRU** | 20 | Correct LRU eviction (hits update recency), per-step trace, and fault count. |
| **Task 2 comparison** | 10 | Reports both fault counts and shows FIFO and LRU differ. |
| **README and screenshots** | 15 | Screenshots embedded, source files submitted, and questions answered clearly. |
| **Total** | **100** | |

---

## Tips

- In Task 1, keep the page size a power of two (like 16). Then `page = LA >> 4` and `offset = LA & 15`, which makes the bit-splitting in question 2 obvious.
- Print your page table at the start of Task 1 so your screenshot is self-explanatory.
- In Task 2, the most common bug is forgetting that **LRU updates recency on hits too**, not just on faults. If FIFO and LRU give the same count, this is usually why.
- A FIFO queue (oldest-first) and an LRU ordering (recently-used-last) are different bookkeeping structures — do not reuse one for the other.
- Loading into an empty frame is still a fault: with 3 frames, the first 3 distinct pages always fault.
- For the optional Belady's anomaly, use the exact string `1 2 3 4 1 2 5 1 2 3 4 5`; not every reference string exhibits the anomaly.
