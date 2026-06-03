# Class Activity 5 - Semaphores: Particle Pairs and HELLO Ordering

> **Related Lectures**: Week 8 - Semaphores, Week 9 - Deadlocks  
> **Topics**: Counting semaphores, mutex semaphores, producer/consumer, ordering constraints, deadlock prevention  
> **Language**: Any programming language  
> **Environment**: Linux, WSL, macOS, or Windows with a language runtime that supports threads and semaphores

---

## Objective

In this activity, you will turn two worksheet semaphore problems into running programs.

Problem 1 asks you to protect a shared particle buffer. Multiple producer machines create entangled particle pairs. One packaging machine consumes pairs. Your program must use semaphores so the buffer never underflows, never overflows, and never mixes particles from different pairs.

Problem 2 asks you to coordinate three concurrent processes so they print the word:

```text
HELLO
```

By the end, you should understand how semaphores can solve both resource-counting problems and execution-ordering problems.

---

## Task Overview

| Task | What You Do | Screenshot Required |
|------|-------------|--------------------|
| **Task 1A** | Simulate Problem 1 before semaphores | Broken particle buffer result |
| **Task 1B** | Simulate Problem 1 after semaphores | Correct particle producer/packager running |
| **Task 2A** | Simulate Problem 2 before semaphores | Wrong or unpredictable letter ordering |
| **Task 2B** | Simulate Problem 2 after semaphores | Correct `HELLO` output |

You may use any programming language, but your README must clearly say which language you used and how to run each program.

---

## Worksheet Reference

This activity is based on:

```text
semaphore and deadlock worksheet.pdf
```

Use Problem 1 for Task 1 and Problem 2 for Task 2.

---

## Setup

Create your activity folder:

```bash
mkdir -p activity5/{task1_particles,task2_hello,screenshots}
cd activity5
```

Recommended filenames:

```text
task1_particles/particles_before.<extension>
task1_particles/particles_after.<extension>
task2_hello/hello_before.<extension>
task2_hello/hello_after.<extension>
README.md
screenshots/task1_before_semaphore.png
screenshots/task1_after_semaphore.png
screenshots/task2_before_semaphore.png
screenshots/task2_after_semaphore.png
```

Examples:

```text
particles.py
particles.c
Particles.java
particles.cpp
```

---

## Task 1: Problem 1 - Entangled Particle Pair Buffer

### Scenario

Schro Dinger's company produces pairs of entangled particles. There are multiple producer machines. Each producer creates a pair:

```text
P1, P2
```

The pair is placed into a shared particle buffer. Each pair takes exactly two consecutive buffer slots. One packaging machine removes two particles at a time and packages them for shipment.

### Required Simulation

Write two versions of the Problem 1 simulation:

1. **Before semaphore version** - intentionally unsafe or incomplete synchronization.
2. **After semaphore version** - corrected using semaphores.

The before version exists so you can observe why semaphores are needed. It may stop with one of the required error messages. The after version should keep running correctly until you stop it manually.

### Required Simulation

Your after-semaphore program must:

- use multiple producer threads, tasks, or processes
- use one consumer thread, task, or process
- use semaphores to protect the shared buffer
- keep running in an infinite loop while the system is correct
- display how many particle pairs have been produced
- display how many particle pairs have been packaged
- stop only if an error condition is detected

### Required Buffer Rules

Use a shared buffer with capacity:

```text
100 particles = 50 particle pairs
```

The following rules must always be true:

1. A producer may add a pair only when two buffer spaces are available.
2. The two particles in a pair must be placed in consecutive buffer slots.
3. The buffer capacity must never exceed 100 particles.
4. The consumer may fetch only when at least two particles are available.
5. The two particles fetched by the consumer must belong to the same pair.

### Required Error Checks

Both the before and after versions must include these checks. If any error happens, break the loop and print the exact required message.

#### Empty Buffer Error

If the consumer tries to fetch from an empty buffer, stop and print:

```text
The packaging machine is broken
```

#### Full Buffer Error

If a producer tries to add an item to a full buffer, stop and print:

```text
The producing machine is broken
```

#### Incorrect Pair Error

If the packaged items are not from the same pair, stop and print:

```text
Pairs are incorrect
```

Different pair means `P1` and `P2` came from different producer machines or different pair IDs.

### Particle Format

Use a format that lets you verify the pair.

Example:

```text
Machine 2 creates pair 17:
M2-17-P1
M2-17-P2
```

Valid packaged pair:

```text
M2-17-P1 + M2-17-P2
```

Invalid packaged pair:

```text
M2-17-P1 + M4-88-P2
```

### Suggested Semaphore Design

You may use a different correct design, but this is a good starting point:

| Semaphore | Initial Value | Purpose |
|-----------|---------------|---------|
| `empty_pairs` | 50 | Counts available pair spaces in the buffer |
| `full_pairs` | 0 | Counts completed pairs available to package |
| `mutex` | 1 | Protects shared buffer updates |

Producer idea:

```text
repeat forever:
    produce P1, P2
    wait(empty_pairs)
    wait(mutex)
        add P1 and P2 consecutively
        increment produced counter
    signal(mutex)
    signal(full_pairs)
```

Consumer idea:

```text
repeat forever:
    wait(full_pairs)
    wait(mutex)
        remove P1 and P2
        verify they belong to the same pair
        increment packaged counter
    signal(mutex)
    signal(empty_pairs)
```

### Output Requirements

Your program must continuously print status lines. Keep the output readable.

Example:

```text
Produced pairs: 42 | Packaged pairs: 39 | Buffer particles: 6
Produced pairs: 43 | Packaged pairs: 40 | Buffer particles: 6
Produced pairs: 44 | Packaged pairs: 41 | Buffer particles: 6
```

Because this is an infinite-loop simulation, stop it manually with `Ctrl+C` after you have enough evidence for your screenshot.

### Screenshots

Take two screenshots:

```text
screenshots/task1_before_semaphore.png
screenshots/task1_after_semaphore.png
```

The before screenshot must show:

- the unsafe/before program running
- the error message, incorrect pair, empty-buffer access, full-buffer access, or explanation of the broken behavior visible in the terminal

The after screenshot must show:

- the semaphore/fixed program running
- produced pair counter
- packaged pair counter
- no error message during normal operation

---

## Task 2: Problem 2 - Print HELLO with Semaphores

### Scenario

Problem 2 has three concurrent processes. Without semaphores, the letters can print in the wrong order. Your job is to coordinate the processes so the output is:

```text
HELLO
```

### Process Roles

Simulate these three processes using threads, tasks, or processes:

| Process | Prints |
|---------|--------|
| Process 1 | `H` and `E` |
| Process 2 | `L` |
| Process 3 | `O` |

### Required Simulation

Write two versions of the Problem 2 simulation:

1. **Before semaphore version** - starts the three workers without ordering protection.
2. **After semaphore version** - uses semaphores to force the correct order.

The before version should demonstrate that concurrent workers can print letters in the wrong or unpredictable order. The after version must always print `HELLO`.

### Required Simulation

Your after-semaphore program must:

- create three concurrent workers
- use semaphores to control print order
- print the word `HELLO`
- avoid printing the letters in the wrong order
- terminate normally after printing `HELLO`

### Suggested Semaphore Design

You may use a different correct design. One possible design:

| Semaphore | Initial Value | Meaning |
|-----------|---------------|---------|
| `start_h` | 1 | Allows Process 1 to print `H` first |
| `after_e` | 0 | Allows Process 2 to print first `L` after `HE` |
| `after_l1` | 0 | Allows Process 2 or a second step to print second `L` |
| `after_l2` | 0 | Allows Process 3 to print `O` |

Simple order idea:

```text
Process 1:
    wait(start_h)
    print H
    print E
    signal(after_e)

Process 2:
    wait(after_e)
    print L
    signal(after_l1)
    wait(after_l1)
    print L
    signal(after_l2)

Process 3:
    wait(after_l2)
    print O
```

Your exact implementation can be different, but the visible output must be:

```text
HELLO
```

### Optional Extension

After the once-only version works, you may extend it to print:

```text
HELLO
HELLO
HELLO
```

If you do this extension, make sure each line still prints in the correct order.

### Screenshots

Take two screenshots:

```text
screenshots/task2_before_semaphore.png
screenshots/task2_after_semaphore.png
```

The before screenshot must show:

- the before program command
- output before semaphore ordering is applied
- a short note in the terminal or README explaining whether the order was wrong or unpredictable

The after screenshot must show:

- the program command
- the output `HELLO`
- normal program termination

---

## Questions

Answer these in your `README.md`:

1. In Task 1, why does a producer need to wait before adding a pair to the buffer?
2. In Task 1, why does the consumer need to wait before removing a pair from the buffer?
3. Which semaphore protects the critical section in your particle buffer program?
4. How does your program verify that `P1` and `P2` belong to the same pair?
5. In Task 2, why can the program print letters in the wrong order without semaphores?
6. Which semaphore or synchronization step forces `H` to print before `E`, `L`, `L`, and `O`?
7. What could cause deadlock in either of your simulations?

---

## Deliverables & Submission

### Required Screenshots

Submit these screenshots:

```text
screenshots/task1_before_semaphore.png
screenshots/task1_after_semaphore.png
screenshots/task2_before_semaphore.png
screenshots/task2_after_semaphore.png
```

### Required Source Files

Submit your source files. Use names that match your language.

Examples:

```text
task1_particles/particles_before.py
task1_particles/particles_after.py
task2_hello/hello_before.py
task2_hello/hello_after.py
```

or:

```text
task1_particles/particles_before.cpp
task1_particles/particles_after.cpp
task2_hello/hello_before.cpp
task2_hello/hello_after.cpp
```

### Submission Folder Structure

```text
os-se-<YourStudentID>/
`-- os-class-activities-<YourStudentID>/
    `-- activity5/
        |-- README.md
        |-- task1_particles/
        |   |-- particles_before.<extension>
        |   `-- particles_after.<extension>
        |-- task2_hello/
        |   |-- hello_before.<extension>
        |   `-- hello_after.<extension>
        `-- screenshots/
            |-- task1_before_semaphore.png
            |-- task1_after_semaphore.png
            |-- task2_before_semaphore.png
            `-- task2_after_semaphore.png
```

### README Template

````markdown
# Class Activity 5 - Semaphores

- **Student Name:** [Your Name]
- **Student ID:** [Your ID]
- **Programming Language Used:** [Python / C / C++ / Java / Other]

---

## Task 1A: Particle Pair Buffer Before Semaphores

![Particle simulation before semaphores](screenshots/task1_before_semaphore.png)

- What error or incorrect behavior appeared:
- Why did this happen without semaphore protection:

---

## Task 1B: Particle Pair Buffer After Semaphores

![Particle simulation after semaphores](screenshots/task1_after_semaphore.png)

- Number of producer machines:
- Buffer capacity:
- Semaphores used:
- Produced pair count shown in screenshot:
- Packaged pair count shown in screenshot:
- Did any error appear during normal operation?

---

## Task 2A: HELLO Before Semaphores

![HELLO before semaphores](screenshots/task2_before_semaphore.png)

- Output before semaphore ordering:
- Why this output can be wrong or unpredictable:

---

## Task 2B: HELLO After Semaphores

![HELLO after semaphores](screenshots/task2_after_semaphore.png)

- Processes or threads used:
- Semaphores used:
- Final output:

---

## Questions

1. In Task 1, why does a producer need to wait before adding a pair to the buffer?
2. In Task 1, why does the consumer need to wait before removing a pair from the buffer?
3. Which semaphore protects the critical section in your particle buffer program?
4. How does your program verify that `P1` and `P2` belong to the same pair?
5. In Task 2, why can the program print letters in the wrong order without semaphores?
6. Which semaphore or synchronization step forces `H` to print before `E`, `L`, `L`, and `O`?
7. What could cause deadlock in either of your simulations?

---

## Reflection

_What did these simulations teach you about using semaphores for shared resources and ordered execution?_
````

---

## Grading Criteria

| Criteria | Points | Description |
|----------|--------|-------------|
| **Task 1 before semaphores** | 15 | Demonstrates the broken/unsafe particle buffer behavior before synchronization. |
| **Task 1 after semaphores** | 30 | Uses semaphores correctly for multiple producers, one consumer, counters, and a shared buffer. |
| **Task 1 validation checks** | 15 | Detects empty buffer, full buffer, and incorrect pair errors with the required messages. |
| **Task 2 before semaphores** | 10 | Demonstrates wrong or unpredictable letter ordering before synchronization. |
| **Task 2 after semaphores** | 15 | Uses semaphores to print `HELLO` in the correct order with concurrent workers. |
| **README and screenshots** | 15 | Four screenshots are embedded, source files are submitted, and questions are answered clearly. |
| **Total** | **100** | |

---

## Tips

- Do not use random sleeps as your main synchronization strategy. Use semaphores.
- It is okay to add small sleeps only to make the output easier to read.
- Keep the particle pair identity simple and easy to compare.
- If Task 1 stops with an error during normal operation, your semaphore logic is probably wrong.
- If Task 2 sometimes prints anything other than `HELLO`, your semaphore ordering is incomplete.
