# 🎬 Interactive Visualizations

Step-through, animated explanations of OS concepts. Each file is **self-contained HTML** (no dependencies, works offline). Controls: **Next / Prev / Play / Reset**, or keyboard **→ ← Space**.

| Visualization | Topic | Activity |
|---------------|-------|----------|
| [producer-consumer.html](producer-consumer.html) | Semaphores & producer/consumer (bounded buffer): why FIFO buffering, precedence with a semaphore = 0, counting semaphores (`chars`/`space`), and `lock = 1` as a mutex for two producers — each shown broken ✗ then fixed ✓ | Week 8 (Ch 8) |
| [rag-deadlock.html](rag-deadlock.html) | Resource Allocation Graph & cycle-based deadlock detection (single-instance) | Activity 7 · Task 1 |
| [bankers-algorithm.html](bankers-algorithm.html) | Banker's Algorithm: safety check + resource requests | Activity 7 · Task 2 |
| [deadlock-detection.html](deadlock-detection.html) | Multi-instance deadlock detection (reduction algorithm) — shows a cycle that is *not* a deadlock | Activity 7 · Task 1 extension |
| [paging-translation.html](paging-translation.html) | Paging address translation: logical → page + offset → page-table lookup → physical address, with valid/invalid bits | Activity 8 · Task 1 (Ch 9) |
| [tlb.html](tlb.html) | TLB cache: reference-stream step-through with hits, misses, LRU eviction, and running hit ratio | Chapter 9 |
| [page-replacement.html](page-replacement.html) | Demand paging & page replacement: FIFO / LRU / OPT step-through, fault counts, Belady's anomaly | Activity 8 · Task 2 (Ch 10) |
| [demand-paging.html](demand-paging.html) | Demand paging & virtual memory: page faults, swap in / swap out, victim eviction, valid/invalid bits and page-table updates | Chapter 9 |
| [contiguous-allocation.html](contiguous-allocation.html) | Contiguous allocation with First / Best / Worst fit, external fragmentation, and compaction | Chapter 9 |
| [eat-calculator.html](eat-calculator.html) | Effective Access Time vs TLB hit ratio — interactive sliders + live graph | Chapter 9 |

Each one has two modes:

- **Examples / Safety check** — the guided, pre-built scenarios from Activity 7.
- **Build your own / Custom data** — a sandbox where students define their own scenario:
  - *RAG*: add processes, resources, and request/assignment edges, then run cycle detection on their own graph.
  - *Banker's*: choose the number of resource types and processes, edit the Allocation / Max / Total matrices (Available is computed live), and test their own resource request for grant/deny.

> ⚠️ **GitHub does not run `.html` files** — clicking the links above on github.com shows the *source code*, not the animation. Use one of the live options below.

---

## Option 1 — Live now (no setup): htmlpreview

These links render the pages immediately through `htmlpreview.github.io`:

- **Semaphores — Producer/Consumer** → https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/producer-consumer.html
- **RAG / Deadlock** → https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/rag-deadlock.html
- **Banker's Algorithm** → https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/bankers-algorithm.html
- **Multi-Instance Deadlock Detection** → https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/deadlock-detection.html
- **Paging & Address Translation** → https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/paging-translation.html
- **TLB (Translation Look-Aside Buffer)** → https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/tlb.html
- **Page Replacement (FIFO/LRU/OPT)** → https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/page-replacement.html
- **Demand Paging & Virtual Memory** → https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/demand-paging.html
- **Contiguous Allocation & Fit Algorithms** → https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/contiguous-allocation.html
- **Effective Access Time (EAT)** → https://htmlpreview.github.io/?https://github.com/RathpiseyAlpha/ITC-OS-2026/blob/main/lectures/visualizations/eat-calculator.html

## Option 2 — Clean URLs: GitHub Pages (recommended)

Enable once, then the pages are served from your own domain.

**To enable (one time):**

1. Go to the repo on GitHub → **Settings** → **Pages**.
2. Under **Build and deployment → Source**, choose **Deploy from a branch**.
3. Set **Branch = `main`**, **Folder = `/ (root)`**, then **Save**.
4. Wait ~1 minute for the first build.

**Then the visualizations live at:**

- Menu → https://rathpiseyalpha.github.io/ITC-OS-2026/lectures/visualizations/
- Semaphores — Producer/Consumer → https://rathpiseyalpha.github.io/ITC-OS-2026/lectures/visualizations/producer-consumer.html
- RAG / Deadlock → https://rathpiseyalpha.github.io/ITC-OS-2026/lectures/visualizations/rag-deadlock.html
- Banker's Algorithm → https://rathpiseyalpha.github.io/ITC-OS-2026/lectures/visualizations/bankers-algorithm.html
- Multi-Instance Deadlock Detection → https://rathpiseyalpha.github.io/ITC-OS-2026/lectures/visualizations/deadlock-detection.html
- Paging & Address Translation → https://rathpiseyalpha.github.io/ITC-OS-2026/lectures/visualizations/paging-translation.html
- TLB (Translation Look-Aside Buffer) → https://rathpiseyalpha.github.io/ITC-OS-2026/lectures/visualizations/tlb.html
- Page Replacement (FIFO/LRU/OPT) → https://rathpiseyalpha.github.io/ITC-OS-2026/lectures/visualizations/page-replacement.html
- Demand Paging & Virtual Memory → https://rathpiseyalpha.github.io/ITC-OS-2026/lectures/visualizations/demand-paging.html
- Contiguous Allocation & Fit Algorithms → https://rathpiseyalpha.github.io/ITC-OS-2026/lectures/visualizations/contiguous-allocation.html
- Effective Access Time (EAT) → https://rathpiseyalpha.github.io/ITC-OS-2026/lectures/visualizations/eat-calculator.html

## Option 3 — Local

Download/clone the repo and double-click any `.html` file, or open it in VS Code with the *Live Server* extension.
