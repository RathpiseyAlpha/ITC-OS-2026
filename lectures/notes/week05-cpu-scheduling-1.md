# Week 5 — CPU Scheduling I

> **Date**: _______________  
> **Lecturer**: Heng Rathpisey  
> **Slides**: [ch5.pdf](../files/ch5.pdf)

---

## 1. Overview

_Write a one-sentence summary of what this topic is about:_

> 

---

## 2. Key Concepts & Definitions

| Term | Definition (in your own words) |
|------|-------------------------------|
| CPU Scheduling | |
| CPU Burst / I/O Burst | |
| Preemptive Scheduling | |
| Non-Preemptive Scheduling | |
| Dispatcher | |
| Dispatch Latency | |
| Turnaround Time | |
| Waiting Time | |
| Response Time | |
| Throughput | |
| FCFS (First-Come First-Served) | |
| SJF (Shortest Job First) | |
| SRTF (Shortest Remaining Time First) | |

---

## 3. Detailed Notes

### 3.1 Basic Scheduling Concepts

> **🎣 Hook:** Your CPU is the most valuable resource in the system, and dozens of processes are fighting for it. Who gets to use it next — and is there a *fair* way to decide?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - When exactly does the OS need to make a scheduling decision?
> - What is a CPU burst vs. an I/O burst, and why does this pattern matter for scheduling?
> - What's the difference between a *long-term*, *short-term*, and *medium-term* scheduler?


### 3.2 Scheduling Criteria

> **🎣 Hook:** Should we optimize for getting the most work done? Or for making each user feel like the system is responsive? These goals often *conflict* — so which one wins?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Can you maximize throughput AND minimize response time at the same time?
> - What's the difference between waiting time and turnaround time?
> - Which criterion matters most for an interactive desktop vs. a batch server?
> - How do you actually *measure* these criteria in a real system?


### 3.3 FCFS Scheduling

> **🎣 Hook:** "First come, first served" sounds perfectly fair — until one process takes 100ms and makes everyone else wait. Why is the simplest scheduling algorithm often the worst?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What is the "convoy effect" and why does it hurt FCFS?
> - Is FCFS preemptive or non-preemptive? What does that mean in practice?
> - In what scenarios would FCFS actually perform reasonably well?


### 3.4 SJF Scheduling

> **🎣 Hook:** Mathematically, SJF gives the best possible average waiting time. So why don't real operating systems just use it? There's a fatal flaw hiding in plain sight.

_Notes:_


> **❓ Questions You Should Be Asking:**
> - Why is SJF provably optimal for average waiting time?
> - How can you know the *next* CPU burst length in advance? (Hint: you can't — so how do you approximate it?)
> - What is exponential averaging and how does it predict burst time?
> - Can SJF cause starvation? For which type of processes?


### 3.5 SRTF (Preemptive SJF)

> **🎣 Hook:** What if a brand-new short job arrives while a longer job is already running? Should we kick the running job off the CPU? SRTF says *yes* — but at what cost?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - How does SRTF differ from SJF in behavior when a new process arrives?
> - Does SRTF always produce a better average waiting time than SJF?
> - What's the overhead of frequent preemptions (context switches)?
> - How would you handle a tie when two processes have the same remaining time?


---

## 4. Diagrams & Visuals

### Gantt Chart — FCFS Example

```
| Process | Arrival | Burst |
|---------|---------|-------|
|         |         |       |

Gantt chart:
[ Draw here ]

Avg Waiting Time = 
Avg Turnaround Time = 
```

### Gantt Chart — SJF Example

```
[ Draw here with calculations ]
```

---

## 5. Key Comparisons

| Criteria | FCFS | SJF | SRTF |
|----------|------|-----|------|
| Preemptive? | | | |
| Starvation? | | | |
| Optimal? | | | |
| Convoy effect? | | | |

---

## 6. Examples

_Work through a scheduling problem:_

| Process | Arrival Time | Burst Time |
|---------|-------------|------------|
| P1 | | |
| P2 | | |
| P3 | | |
| P4 | | |

_Calculate average waiting time for FCFS and SJF._

---

## 7. Review Questions

- [ ] What is the convoy effect in FCFS?
- [ ] Why is SJF optimal for average waiting time?
- [ ] What is the main problem with SJF in practice?
- [ ] Differentiate preemptive vs non-preemptive scheduling.
- [ ] When does the dispatcher get involved?

---

## 8. Connections to Other Topics

- **Previous week (Threads)**: Scheduler picks threads/processes to run.
- **Next week (Scheduling II)**: More advanced scheduling algorithms.
- **Week 3 (Processes)**: Process states determine scheduling eligibility.

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
