# Class Activity 8 - Memory Management & Virtual Memory: Reason + Simulate

> **Related Lectures**: Week 10 - Memory Management, Week 11 - Virtual Memory  
> **Topics**: Logical vs physical addresses, paging, address translation, page tables, the **TLB** and **Effective Access Time (EAT)**, internal fragmentation, demand paging, page faults, page replacement (FIFO, LRU, OPT)  
> **Format**: **Two layers.** First you **reason and hand-trace** — this is what proves you understand. Then you **build a simulator** and use it to **verify your own hand work**. The activity is grouped by topic: **Part 1** is paging, address translation and the TLB; **Part 2** is page replacement and demand paging; **Part 3** is applied reasoning.  
> **Language**: Any programming language · **Environment**: any runtime

---

## How this activity works (read first)

A coding-only task proves little — an AI can write a page-table translator or an LRU simulator instantly. So here the **simulator is a tool, not the point**: in each part you first work the problems **by hand** on your own personalized data, then build the program and use it to **check your traces**. Marks go to your **hand-traces, predictions, and explanations** as much as to the working code. A simulator with no hand-trace, or hand-traces that don't match your own simulator with no explanation, will score poorly.

> Be prepared to **reproduce any translation or trace on paper** if asked.

### 🎬 Interactive Visualizations (your checking tools)

Use these to **verify** your hand-work — after you have traced it yourself, not before:

- **Paging & Address Translation** (Part 1A / 1C): [open live](https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/paging-translation.html) · [source](../visualizations/paging-translation.html)
- **TLB (Translation Look-Aside Buffer)** (Part 1B): [open live](https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/tlb.html) · [source](../visualizations/tlb.html)
- **Effective Access Time (EAT)** (Part 1B — why the TLB matters): [open live](https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/eat-calculator.html) · [source](../visualizations/eat-calculator.html)
- **Page Replacement — FIFO / LRU / OPT** (Part 2A / 2B, incl. Belady's anomaly): [open live](https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/page-replacement.html) · [source](../visualizations/page-replacement.html)
- **Contiguous Allocation & Fit Algorithms** (external fragmentation, Part 3 Q1): [open live](https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/contiguous-allocation.html) · [source](../visualizations/contiguous-allocation.html)

Each has a **Build your own** mode — plug in your personalized address, reference string, and TLB hit ratio to check your traces. See [visualizations/README.md](../visualizations/README.md) for GitHub Pages links and offline use.

---

## Task Overview

| Task | What you do | Evidence you submit |
|------|-------------|---------------------|
| **Part 1A** — Address translation **by hand** | Translate six logical addresses (incl. your `N` and an invalid page) through the page table | Filled translation table + arithmetic |
| **Part 1B** — TLB lookup & **EAT** **by hand** | Trace a page-reference stream through a 4-entry **TLB**, then compute **Effective Access Time** | TLB trace table + EAT calculation + EAT screenshot |
| **Part 1C** — Paging simulator | Program the translation (and optionally a TLB cache); verify Part 1A/1B | Source + `task1_translation.png` |
| **Part 2A** — Page replacement **by hand** | Predict, then hand-trace **FIFO** and **LRU** on *your* reference string | Two trace tables + prediction |
| **Part 2B** — Demand-paging simulator | Program FIFO & LRU; verify Part 2A | Source + `task2_fifo.png`, `task2_lru.png` |
| **Part 3** — Applied reasoning | Explain fragmentation, faults, thrashing, the TLB and demand paging in your own words | Short written answers |

**Golden rule for every part: hand-trace first, then verify.** Do Part A of each part *before* you write or run any code. If the simulator disagrees with your trace, do **not** silently overwrite your answer — keep it and add a short note on where your reasoning went wrong. That note is worth marks.

### Your personalization

Let **a** = the **last digit** of your student ID, **b** = the **second-to-last digit**. You will plug these into the data below so your numbers are your own.

---

## Part 1 — Paging, Address Translation & the TLB

### Part 1A — Address translation by hand

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

### Part 1B — TLB lookup & Effective Access Time by hand

Every translation above had to read the **page table in memory**. A **TLB** (Translation Look-Aside Buffer) caches recent page→frame entries so most translations skip that extra memory read. Here you trace the cache, then compute what it buys you.

**TLB model:**

```text
TLB: 4 entries, fully associative, empty at start.
A TLB HIT  -> frame known immediately (no page-table read).
A TLB MISS -> read the page table in memory to get the frame, then load
              that page→frame entry into the TLB.

Your stream below touches at most 4 distinct pages, so the TLB never fills
past its 4 entries — once a page is loaded it stays, and nothing is ever
evicted. (What to do when a cache is already full — replacement policies —
comes later, with demand paging in Part 2.)
```

Use the **same page table** as Part 1A. Build **your** page-reference stream by setting **p = (a mod 3)**:

```text
Stream (pages):  p  2  4  p  7  2  4  p  7  2      with p = a mod 3
Pages p, 2, 4 and 7 are all valid, so every reference resolves to a frame.
If p = 2 your stream has 3 distinct pages; otherwise it has 4.
```

**Predict first (before tracing):** how many of the 10 references do you expect to be TLB **hits**? (Hint: a page can only *miss* the first time it is touched.) One sentence why.

Now hand-trace the TLB. One row per reference — mark HIT/MISS and the TLB contents after the reference:

| Ref (page) | HIT / MISS | Page table read? | TLB contents after |
|------------|------------|------------------|--------------------|
| … (10 rows) | | | |

**Measured hits: ____ / 10  →  hit ratio α = ____**

**Now compute Effective Access Time.** Use these timings (personalized):

```text
Memory access time   t_mem = (10 + a) ns
TLB search time      t_tlb = 1 ns
EAT = α·(t_tlb + t_mem) + (1 − α)·(t_tlb + 2·t_mem)
```

1. Compute **EAT at your measured α** from the trace above. Show the substitution.
2. Compute EAT at the lecture's **α = 0.80** and **α = 0.99**, and at **no TLB** (every access pays `t_tlb + 2·t_mem`). Show all three.
3. In one sentence: how much **faster** (in %) is the 99% case than having no TLB at all?

**Verify:** open the **EAT calculator** visualization, set `t_mem`, `t_tlb` and the hit ratio to your numbers (use the *80% hit* / *99% hit* presets to check those two), and confirm the EAT it reports matches your arithmetic. Screenshot → `screenshots/part1_eat.png`. You may also rebuild your stream in the **TLB** visualization (leave the TLB size at 4) to check your hit/miss column — with this stream the TLB never fills, so nothing is ever evicted → `screenshots/part1_tlb.png`.

### Part 1C — Paging address-translation simulator

Write a program that translates logical addresses using the page table above (and its valid bits), and run your Part 1A data through it to check yourself.

**Required behavior**
- store the page size, page table, and valid bits
- translate at least the six Part 1A addresses (including your `N` and at least one **invalid** page)
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

**Optional — TLB cache + EAT:** add a 4-entry TLB in front of the page table (no replacement needed — your stream has at most 4 distinct pages), feed it your Part 1B stream, count hits/misses, and print the measured hit ratio and EAT. Confirm both match your Part 1B hand numbers.

**Verify:** confirm every row of your Part 1A table matches the program. Screenshot → `screenshots/task1_translation.png`.

---

## Part 2 — Page Replacement & Demand Paging

### Part 2A — Page replacement by hand (FIFO vs LRU)

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

### Part 2B — Demand-paging simulator (FIFO & LRU)

Now write a program that performs exactly what you did by hand, and run your Part 2A data through it to check yourself. Run **two** reference strings through both FIFO and LRU: (i) the **full lecture string** below, and (ii) **your Part 2A string**.

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

**Verify:** confirm the program's counts for **your Part 2A string** match your hand-trace totals. If they differ, fix your trace (or your code) and explain what was wrong. Screenshots → `screenshots/task2_fifo.png`, `screenshots/task2_lru.png`.

> The most common bug: forgetting that **LRU updates recency on hits**, not just faults. If FIFO and LRU give identical counts, check that first.

#### Optional Extension — OPT & Belady's anomaly
- **OPT**: evict the page whose next use is farthest in the future; its fault count should be the lowest of the three.
- **Belady's anomaly**: run **FIFO** on `1 2 3 4 1 2 5 1 2 3 4 5` with **3** frames, then **4** frames, and show 4 frames gives **more** faults. Screenshot → `screenshots/ext_belady.png`.

---

## Part 3 — Applied Reasoning

Answer in your own words (original examples — don't reuse the lecture's):

1. Why is paging free of **external** fragmentation, while contiguous allocation is not?
2. Why does loading a page into an **empty** frame still count as a page fault?
3. A program with a **99%** TLB hit ratio runs much closer to ideal speed than one at **80%**, even though both "usually hit." Using your Part 1B EAT numbers, explain why that last 1% matters so much.
4. On your Part 2A string, **why** did LRU and FIFO differ (or tie)? Point to the specific reference where their behavior diverged.
5. What is **thrashing**, and what would you observe if you re-ran Part 2B with only **1** frame for a working set that needs several pages? What happens to both the page-fault rate *and* the TLB hit ratio?
6. Demand paging loads a page only when first referenced. Give one **benefit** and one **risk** of this versus loading the whole program up front.

---

## Deliverables & Submission

Submit a written report (Part 1A/1B + Part 2A traces, and Part 3 answers), your source files, and your screenshots.

```text
os-se-<YourStudentID>/
`-- os-class-activities-<YourStudentID>/
    `-- activity8/
        |-- README.md                 # hand-traces & predictions (1A, 1B, 2A) + Part 3 answers
        |-- task1_paging/
        |   `-- paging_translation.<ext>
        |-- task2_demand_paging/
        |   `-- page_replacement.<ext>
        `-- screenshots/
            |-- task1_translation.png
            |-- part1_tlb.png
            |-- part1_eat.png
            |-- task2_fifo.png
            `-- task2_lru.png
```

### README template

````markdown
# Class Activity 8 - Memory Management & Virtual Memory

- **Student Name:** [Your Name]   **Student ID:** [Your ID]
- **Personalization:** a = [last digit], b = [2nd-last] → N = (10a+b) mod 128 = [...]
- **Programming Language Used:** [...]

## Part 1A — Address translation (by hand)
[your filled translation table]
1. Offset unchanged because: …
2. Largest offset = …, bits = …
3. (60 + a) = … bytes → … pages, internal fragmentation = … bytes (show working)

## Part 1B — TLB & Effective Access Time (by hand)
- My page-reference stream: …    Prediction (expected hits): …
[TLB trace table] → measured hits = …/10, α = …
- EAT at my α: … ns   |   EAT at 80% = … |   99% = … |   no TLB = …  (show substitutions)
- Why 99% beats no-TLB by …%: …
![EAT](screenshots/part1_eat.png)   ![TLB](screenshots/part1_tlb.png)

## Part 1C — Paging simulator verification
![Translation](screenshots/task1_translation.png)
- Did the simulator match my 1A table? …
- (Optional) Did the TLB sim reproduce my 1B hit ratio / EAT? …

## Part 2A — Page replacement (by hand)
- My reference string: …    Prediction (FIFO vs LRU): …
[FIFO trace table] → FIFO faults: …
[LRU trace table]  → LRU faults: …
Which faulted more, and did it match my prediction: …

## Part 2B — Demand-paging simulator verification
![FIFO](screenshots/task2_fifo.png)   ![LRU](screenshots/task2_lru.png)
- Did the simulator's counts for my 2A string match my hand totals? … (if not, what was wrong)

## Part 3 — Applied reasoning
1. …  2. …  3. …  4. …  5. …  6. …
````

---

## Grading Criteria

| Criteria | Points | Description |
|----------|--------|-------------|
| **1A hand translation** | 12 | Correct page/offset/frame/physical for all six addresses (incl. your N and an invalid page), with shown arithmetic and the fragmentation calculation. |
| **1B TLB trace + EAT** | 13 | Complete TLB hit/miss trace for *your* stream with correct TLB contents per row, a recorded prediction, and correct EAT at your α, 80%, 99% and no-TLB with shown substitutions. |
| **1C paging simulator** | 12 | Correct translation program incl. the invalid-page message (TLB/EAT extension optional). |
| **2A hand traces + prediction** | 18 | Complete FIFO and LRU trace tables for *your* string, correct fault totals, and a recorded prediction. |
| **2B demand-paging simulator** | 18 | Correct FIFO and LRU (hits update recency), per-step trace, and fault counts on both strings. |
| **Verification (hand ↔ simulator)** | 8 | Hand-traces compared against the simulator with honest notes on any mismatch. |
| **Part 3 reasoning** | 9 | In-your-own-words answers using original examples. |
| **Report & screenshots** | 10 | Traces, predictions, source files, and screenshots all present and clear. |
| **Total** | **100** | |

> Up to **15 points** may be deducted for a working simulator submitted with **no hand-traces or no predictions** — the reasoning is what is being assessed.

---

## Tips

- Keep page size a power of two: `page = LA >> 4`, `offset = LA & 15` — and the offset-bits answer falls right out.
- Do the **by-hand** part of each section *before* writing any code; the simulator is your answer key, not your calculator.
- For the TLB, a page **misses only the first time** you touch it and **hits** every time after — with a 4-page working set the 4-entry TLB never fills, so nothing is ever evicted (replacement policies arrive in Part 2).
- In the EAT formula a TLB **miss** costs *two* memory accesses (page table, then data); a **hit** costs *one*. That single extra access is the whole story.
- A FIFO queue (oldest-first) and an LRU recency order are **different** structures — don't reuse one for the other.
- With 3 empty frames, the first 3 distinct pages always fault — that's expected.
- For Belady's anomaly use exactly `1 2 3 4 1 2 5 1 2 3 4 5`; not every string shows it.
