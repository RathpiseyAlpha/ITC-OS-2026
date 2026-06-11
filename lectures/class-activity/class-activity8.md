# Class Activity 8 - Memory Management & Virtual Memory: Reason + Simulate

> **Related Lectures**: Week 10 - Memory Management, Week 11 - Virtual Memory  
> **Topics**: Logical vs physical addresses, paging, address translation, page tables, internal fragmentation, demand paging, page faults, page replacement (FIFO, LRU, OPT)  
> **Format**: **Two layers.** First you **reason and hand-trace** (Part A) — this is what proves you understand. Then you **build a simulator** (Part B) and use it to **verify your own hand work**. Part C is applied reasoning.  
> **Language**: Any programming language · **Environment**: any runtime

---

## How this activity works (read first)

A coding-only task proves little — an AI can write a page-table translator or an LRU simulator instantly. So here the **simulator is a tool, not the point**: you must first work the problems **by hand** on your own personalized data, then build the program and use it to **check your traces**. Marks go to your **hand-traces, predictions, and explanations** as much as to the working code. A simulator with no hand-trace, or hand-traces that don't match your own simulator with no explanation, will score poorly.

> Be prepared to **reproduce any translation or trace on paper** if asked.

### 🎬 Interactive Visualizations (your checking tools)

Use these to **verify** your Part A hand-work — after you have traced it yourself, not before:

- **Paging, TLB & Address Translation** (Part A1 / B1): [open live](https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/paging-translation.html) · [source](../visualizations/paging-translation.html)
- **Page Replacement — FIFO / LRU / OPT** (Part A2 / B2, incl. Belady's anomaly): [open live](https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/page-replacement.html) · [source](../visualizations/page-replacement.html)
- **Contiguous Allocation & Fit Algorithms** (external fragmentation, Part C Q1): [open live](https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/contiguous-allocation.html) · [source](../visualizations/contiguous-allocation.html)
- **Effective Access Time (EAT)** (why the TLB matters): [open live](https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/eat-calculator.html) · [source](../visualizations/eat-calculator.html)

Each has a **Build your own** mode — plug in your personalized address and reference string to check your traces. See [visualizations/README.md](../visualizations/README.md) for GitHub Pages links and offline use.

### Your personalization

Let **a** = the **last digit** of your student ID, **b** = the **second-to-last digit**. You will plug these into the data below so your numbers are your own.

---

## Part A — Reason &amp; Hand-Trace (no code yet)

### A1 — Address translation by hand

Memory model (fixed for everyone):

```text
Page size:             16 bytes
Logical address space: 8 pages   (logical addresses 0 .. 127)
Page table:            page→frame, with two invalid (not-resident) pages

Page | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7
Frame| 5 | 2 | 1 | – | 7 | – | 0 | 4      (pages 3 and 5 are invalid)
```

Translate these **six** logical addresses **by hand** — five fixed plus one of your own:

```text
20,  100,  48,  16,  127,   and   N = (10·a + b) mod 128
```

Fill this table (show your arithmetic for `page = LA / 16`, `offset = LA mod 16`, `physical = frame·16 + offset`):

| Logical (LA) | page = LA/16 | offset = LA%16 | valid? | frame | physical = frame·16+offset |
|---|---|---|---|---|---|
| 20  | | | | | |
| 100 | | | | | |
| 48  | | | | | |
| 16  | | | | | |
| 127 | | | | | |
| N = | | | | | |

Then answer:
1. For a valid page, **why is the offset identical** in the logical and physical address?
2. The page size is 16 bytes — what is the **largest valid offset**, and **how many bits** does the offset need?
3. A process needs **(60 + a)** bytes with 16-byte pages: how many **pages** are allocated, and how much **internal fragmentation** (wasted bytes in the last page) results? Show the calculation.

### A2 — Page replacement by hand (FIFO vs LRU)

Build **your** reference string from the lecture string by changing the first page to your digit:

```text
Base:  7 0 1 2 0 3 0 4 2 3 0 3        (first 12 of the Week 11 string)
Yours: replace the FIRST number 7 with (a mod 7), keep the rest.
Frames: 3   (start empty; loading into an empty frame still counts as a fault)
```

**Predict first (before tracing):** will **FIFO** or **LRU** cause more page faults on your string — or a tie? One sentence why.

Now hand-trace **both** algorithms. Fill a row per reference; mark HIT/FAULT, the three frame slots, and the victim evicted (if any):

**FIFO** (evict the page resident longest)

| Ref | H/F | F1 | F2 | F3 | Evicted |
|-----|-----|----|----|----|---------|
| … (12 rows) | | | | | |

**Total FIFO faults: ____**

**LRU** (evict the page unused for longest; **hits also update recency**)

| Ref | H/F | F1 | F2 | F3 | Evicted |
|-----|-----|----|----|----|---------|
| … (12 rows) | | | | | |

**Total LRU faults: ____**

State which algorithm faulted more on **your** string, and whether it matched your prediction.

---

## Part B — Build the Simulator (and verify Part A)

Now write programs that perform exactly what you did by hand, and **run your Part A data through them to check yourself**.

### Setup

```bash
mkdir -p activity8/{task1_paging,task2_demand_paging,screenshots}
cd activity8
```

```text
task1_paging/paging_translation.<ext>
task2_demand_paging/page_replacement.<ext>
```

### B1 — Paging address-translation simulator

Write a program that translates logical addresses using the page table above (and its valid bits).

**Required behavior**
- store the page size, page table, and valid bits
- translate at least the six A1 addresses (including your `N` and at least one **invalid** page)
- for a valid address print page, offset, frame, and physical address
- for an invalid page print exactly: `Page fault: page not in memory`

**Output example**
```text
Logical 20  -> page 1, offset 4  -> frame 2 -> physical 36
Logical 48  -> page 3 -> Page fault: page not in memory
```

**Pseudocode**
```text
P = 16
page_table = { 0:5, 1:2, 2:1, 4:7, 6:0, 7:4 }   # valid pages only
for LA in addresses:
    page = LA / P;  offset = LA % P
    if page in page_table: print page, offset, frame, frame*P+offset
    else:                  print "Page fault: page not in memory"
```

**Verify:** confirm every row of your A1 table matches the program. Screenshot → `screenshots/task1_translation.png`.

### B2 — Demand-paging simulator (FIFO &amp; LRU)

Run **two** reference strings through both FIFO and LRU: (i) the **full lecture string** below, and (ii) **your A2 string**.

```text
Full string:  7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1
Frames: 3   (start empty)
```

**Required behavior (per algorithm)**
- process one reference at a time; decide HIT or FAULT
- on a fault, load the page; if memory is full, evict the algorithm's victim
- print the frame contents after each reference and the **total fault count**
- FIFO evicts the oldest-loaded page; LRU evicts the least-recently-used page (**hits update recency**)

**Output example**
```text
=== FIFO ===
Ref 7 | FAULT | frames: [7, _, _]
Ref 0 | FAULT | frames: [7, 0, _]
Ref 2 | FAULT | frames: [2, 0, 1]  (evicted 7)
...
Total page faults (FIFO): 15
FIFO faults: 15 | LRU faults: 12
```

**Verify:** confirm the program's counts for **your A2 string** match your hand-trace totals. If they differ, fix your trace (or your code) and explain what was wrong. Screenshots → `screenshots/task2_fifo.png`, `screenshots/task2_lru.png`.

> The most common bug: forgetting that **LRU updates recency on hits**, not just faults. If FIFO and LRU give identical counts, check that first.

### Optional Extension — OPT &amp; Belady's anomaly
- **OPT**: evict the page whose next use is farthest in the future; its fault count should be the lowest of the three.
- **Belady's anomaly**: run **FIFO** on `1 2 3 4 1 2 5 1 2 3 4 5` with **3** frames, then **4** frames, and show 4 frames gives **more** faults. Screenshot → `screenshots/ext_belady.png`.

---

## Part C — Applied Reasoning

Answer in your own words (original examples — don't reuse the lecture's):

1. Why is paging free of **external** fragmentation, while contiguous allocation is not?
2. Why does loading a page into an **empty** frame still count as a page fault?
3. On your A2 string, **why** did LRU and FIFO differ (or tie)? Point to the specific reference where their behavior diverged.
4. What is **thrashing**, and what would you observe if you re-ran B2 with only **1** frame for a working set that needs several pages?
5. Demand paging loads a page only when first referenced. Give one **benefit** and one **risk** of this versus loading the whole program up front.

---

## Deliverables &amp; Submission

Submit a written report (Part A traces + Part C answers), your source files, and your screenshots.

```text
os-se-<YourStudentID>/
`-- os-class-activities-<YourStudentID>/
    `-- activity8/
        |-- README.md                 # Part A hand-traces & predictions, Part C answers
        |-- task1_paging/
        |   `-- paging_translation.<ext>
        |-- task2_demand_paging/
        |   `-- page_replacement.<ext>
        `-- screenshots/
            |-- task1_translation.png
            |-- task2_fifo.png
            `-- task2_lru.png
```

### README template

````markdown
# Class Activity 8 - Memory Management & Virtual Memory

- **Student Name:** [Your Name]   **Student ID:** [Your ID]
- **Personalization:** a = [last digit], b = [2nd-last] → N = (10a+b) mod 128 = [...]
- **Programming Language Used:** [...]

## Part A1 — Address translation (by hand)
[your filled translation table]
1. Offset unchanged because: …
2. Largest offset = …, bits = …
3. (60 + a) = … bytes → … pages, internal fragmentation = … bytes (show working)

## Part A2 — Page replacement (by hand)
- My reference string: …    Prediction (FIFO vs LRU): …
[FIFO trace table] → FIFO faults: …
[LRU trace table]  → LRU faults: …
Which faulted more, and did it match my prediction: …

## Part B — Simulator verification
![Translation](screenshots/task1_translation.png)
![FIFO](screenshots/task2_fifo.png)
![LRU](screenshots/task2_lru.png)
- Did the simulator match my A1 table? …
- Did the simulator's counts for my A2 string match my hand totals? … (if not, what was wrong)

## Part C — Applied reasoning
1. …  2. …  3. …  4. …  5. …
````

---

## Grading Criteria

| Criteria | Points | Description |
|----------|--------|-------------|
| **A1 hand translation** | 15 | Correct page/offset/frame/physical for all six addresses (incl. your N and an invalid page), with shown arithmetic and the fragmentation calculation. |
| **A2 hand traces + prediction** | 20 | Complete FIFO and LRU trace tables for *your* string, correct fault totals, and a recorded prediction. |
| **B1 simulator** | 15 | Correct translation program incl. the invalid-page message. |
| **B2 simulator** | 20 | Correct FIFO and LRU (hits update recency), per-step trace, and fault counts on both strings. |
| **Verification (A↔B)** | 10 | Hand-traces compared against the simulator with honest notes on any mismatch. |
| **Part C reasoning** | 10 | In-your-own-words answers using original examples. |
| **Report & screenshots** | 10 | Traces, predictions, source files, and screenshots all present and clear. |
| **Total** | **100** | |

> Up to **15 points** may be deducted for a working simulator submitted with **no hand-traces or no predictions** — the reasoning is what is being assessed.

---

## Tips

- Keep page size a power of two: `page = LA >> 4`, `offset = LA & 15` — and the offset-bits answer falls right out.
- Do Part A **before** writing any code; the simulator is your answer key, not your calculator.
- A FIFO queue (oldest-first) and an LRU recency order are **different** structures — don't reuse one for the other.
- With 3 empty frames, the first 3 distinct pages always fault — that's expected.
- For Belady's anomaly use exactly `1 2 3 4 1 2 5 1 2 3 4 5`; not every string shows it.
