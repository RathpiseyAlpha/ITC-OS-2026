# Week 6 — CPU Scheduling II

> **Date**: _______________  
> **Lecturer**: Heng Rathpisey  
> **Slides**: [ch6.pdf](../files/ch6.pdf)

---

## 1. Overview

_Write a one-sentence summary of what this topic is about:_

> 

---

## 2. Key Concepts & Definitions

| Term | Definition (in your own words) |
|------|-------------------------------|
| Round Robin (RR) | |
| Time Quantum | |
| Priority Scheduling | |
| Starvation | |
| Aging | |
| Multilevel Queue (MLQ) | |
| Multilevel Feedback Queue (MLFQ) | |
| Real-Time Scheduling | |

---

## 3. Detailed Notes

### 3.1 Round Robin Scheduling

> **🎣 Hook:** What if every process got an equal slice of CPU time, like taking turns in a game? That's Round Robin — but what happens if the time slice is too big? Too small? Finding the sweet spot changes everything.

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What happens when the time quantum is set to infinity? (Hint: it becomes another algorithm.)
> - What happens when the time quantum is set extremely small? What's the hidden cost?
> - How does Round Robin handle I/O-bound vs. CPU-bound processes differently?
> - Is Round Robin fair? What does "fair" even mean in scheduling?


### 3.2 Priority Scheduling

> **🎣 Hook:** Not all processes are created equal — your virus scanner shouldn't get the same priority as your video call. But who assigns priorities, and what happens to the unlucky low-priority process that never gets to run?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - How are priorities assigned — statically or dynamically?
> - What is the starvation problem in priority scheduling?
> - Can priority scheduling be combined with other algorithms?
> - What real-world systems use strict priority scheduling?


### 3.3 Starvation & Aging

> **🎣 Hook:** Imagine standing in line forever because someone more "important" keeps cutting ahead. That's starvation. So how do you guarantee that every process eventually gets served?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - How does aging work — at what rate should priority increase?
> - Is starvation a theoretical concern or does it actually happen in real systems?
> - Does aging completely solve the problem, or are there edge cases?
> - Which scheduling algorithms are vulnerable to starvation?


### 3.4 Multilevel Queue Scheduling

> **🎣 Hook:** What if you had separate waiting lines for different types of travelers at an airport — first class, business, economy? That's the idea behind multilevel queues. But how do you decide which line gets served first?

_Notes:_


> **❓ Questions You Should Be Asking:**
> - How are processes assigned to queues — can they move between queues?
> - What scheduling algorithm runs *within* each queue?
> - How is CPU time divided *between* queues?
> - What happens to background processes when foreground processes keep arriving?


### 3.5 Multilevel Feedback Queue Scheduling

> **🎣 Hook:** Multilevel queues are rigid — once you're in economy, you stay there. MLFQ fixes this by letting processes move between queues based on their behavior. It's the most sophisticated scheduler we'll study — and it comes with a lot of design knobs.

_Notes:_


> **❓ Questions You Should Be Asking:**
> - What behavior causes a process to be demoted to a lower queue?
> - How does MLFQ distinguish between CPU-bound and I/O-bound processes *automatically*?
> - What parameters define an MLFQ (number of queues, quantum per level, promotion/demotion rules)?
> - Can a process game the system by voluntarily giving up the CPU right before its quantum expires?


---

## 4. Diagrams & Visuals

### Round Robin Gantt Chart

```
Time quantum = ___

[ Draw here with calculations ]
```

### Multilevel Feedback Queue Diagram

```
[ Draw the queue levels and promotion/demotion rules ]
```

---

## 5. Key Comparisons

| Criteria | RR | Priority | MLQ | MLFQ |
|----------|-----|----------|-----|------|
| Preemptive? | | | | |
| Starvation? | | | | |
| Fairness | | | | |
| Complexity | | | | |

---

## 6. Examples

_Work through a Round Robin problem (quantum = 4):_

| Process | Arrival Time | Burst Time |
|---------|-------------|------------|
| P1 | | |
| P2 | | |
| P3 | | |

---

## 7. Review Questions

- [ ] How does the choice of time quantum affect Round Robin performance?
- [ ] How does aging prevent starvation in priority scheduling?
- [ ] What distinguishes MLQ from MLFQ?
- [ ] Design an MLFQ with 3 levels — describe the rules.
- [ ] Which scheduling algorithm would you choose for an interactive system? Why?

---

## 8. Connections to Other Topics

- **Previous week (Scheduling I)**: Builds on FCFS and SJF.
- **Week 3 (Processes)**: Scheduling interacts with process states.
- **Week 4 (Threads)**: Thread scheduling vs process scheduling.

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
