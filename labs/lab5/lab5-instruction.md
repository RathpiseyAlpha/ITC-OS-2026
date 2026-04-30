# OS Lab 5 — Threads, Kernel Workers & Process Signals (Hands-on)

| | |
|---|---|
| **Course** | Operating Systems |
| **Lab Title** | Thread Models, Kernel Workers & Basic Process Signals |
| **Chapter** | Threads & Concurrency, Process Management |
| **Duration** | 3 Hours |
| **Lab Type** | Individual |

---

> ⚠️ **IMPORTANT — READ EVERYTHING FIRST**
>
> **Before you type a single command, read through this ENTIRE document from top to bottom.** Scan every section — the tasks, the challenges, the deliverables, the folder structure, and the README template. Understand the full scope of what is expected **before** you start working.
>
> **Document structure:**
> 1. **Lab Objectives** — What you'll learn
> 2. **Task Overview** — Summary of all tasks at a glance
> 3. **Lab Setup** — Repository and folder preparation
> 4. **Quick Reference Tables** — Command and API cheat sheets
> 5. **Tasks 1–4 (Required)** — Threads vs Processes, Thread Interaction, Visualizing Threads, Process Signals
> 6. **Deliverables & Submission** — Folder structure, README template, git push
> 7. **Screenshot Checklist** — Every screenshot you need, in one place

---

## Lab Objectives

After completing this lab, students will be able to:

1. Understand the difference between processes and threads in Linux.
2. Use POSIX threads (`pthreads`) to create, manage, and join threads in C.
3. Visualize the 1:1 thread model mapping user threads to kernel-level threads (LWPs).
4. Visualize and distinguish between user threads and kernel worker threads using tools like `ps`, `top`, and `htop`.
5. Understand the limits of interacting with kernel threads.
6. Send, receive, and handle POSIX signals (`SIGINT`, `SIGTERM`, `SIGKILL`) in C programs (a recall and extension from Lab 4).
7. Apply learned concepts to solve synchronization and signal handling challenges.

> **Scenario:** You are **Alex**, still building your systems engineering skills at **TechCorp Inc.** Your manager says: *"Our backend applications are becoming too slow because they process tasks sequentially. I need you to learn how to make them multithreaded. Also, you need to understand how the Linux kernel maps user threads to kernel threads, manages its own worker threads, and how to safely write code to handle signals when things go wrong."*

---

## Task Overview

| Task | Title | Key Commands/APIs | Screenshots Required |
|:---:|-------|-------------|:-----------:|
| **1** | Processes vs. Threads | `fork()`, `pthread_create()` | ✅ (Execution output) |
| **2** | Thread Interaction | `pthread_join()`, `pthread_exit()` | ✅ (Execution output) |
| **3** | Visualizing Kernel & User Threads | `ps -eLf`, `/proc/`, `htop` | ✅ (ps/proc mapping & htop) |
| **4** | Recall: Process Signals | `kill`, `signal()`, `SIGINT` | ✅ (Signal handling) |

---

## Lab Setup

Navigate into your existing lab submission repository and create the `lab5` directory:

```bash
$ cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>
$ mkdir lab5
$ cd lab5
```

### Documenting Your Work

1. **Screenshots:** All tasks in this lab require screenshots to prove successful execution. These are your primary proof of work.
2. **Save All Images:** Save all screenshots to an `images/` folder in your `lab5` directory.

---

## Quick Reference

### Thread API (pthreads)

| Function | Purpose |
|----------|---------|
| `pthread_create` | Spawns a new thread executing a specific function |
| `pthread_join` | Waits for a thread to terminate |
| `pthread_exit` | Terminates the calling thread |
| `pthread_self` | Returns the ID of the calling thread |

### Process & Thread Monitoring

| Command | Purpose |
|---------|---------|
| `ps -eLf` | Shows all threads (LWP - Light Weight Processes) |
| `top -H` | Shows threads individually instead of grouping by process |
| `htop` | Interactive viewer (press `H` to toggle user threads, `K` to toggle kernel threads) |
| `/proc/[pid]/task/` | Directory containing subdirectories for every thread belonging to a process |

### Common Linux Signals

| Signal | Number | Default Action | Purpose |
|--------|--------|----------------|---------|
| `SIGHUP` | 1 | Terminate | Hangup detected on controlling terminal |
| `SIGINT` | 2 | Terminate | Interrupt from keyboard (`Ctrl+C`) |
| `SIGKILL` | 9 | Terminate | Kill signal (cannot be caught or ignored) |
| `SIGTERM` | 15 | Terminate | Termination signal (can be caught/handled) |

---

## Task 1 — Processes vs. Threads

**Scenario:** *"Before we write multithreaded code, you need to prove you understand the difference in resource sharing between a process (using `fork`) and a thread."*

**Instructions:**

1. Setup:
   ```bash
   $ mkdir -p thread_lab
   $ cd thread_lab
   ```

2. Create a C file to demonstrate process memory separation (`process_test.c`):
   ```c
   #include <stdio.h>
   #include <unistd.h>
   #include <sys/wait.h>

   int global_var = 10;

   int main() {
       pid_t pid = fork();

       if (pid == 0) { // Child process
           global_var += 20;
           printf("Child process: global_var = %d\n", global_var);
       } else { // Parent process
           wait(NULL); // Wait for child to finish
           printf("Parent process: global_var = %d\n", global_var);
       }
       return 0;
   }
   ```

3. Compile and run:
   ```bash
   $ gcc -o process_test process_test.c
   $ ./process_test
   ```
   > **Observe:** The child modifies `global_var`, but the parent's copy remains unchanged because processes do not share memory space.
   
   > 📸 **Required Screenshot 1:** Take a screenshot of the `process_test` execution output. Save as `process_vs_thread_1.png`.

4. Create a C file to demonstrate thread memory sharing (`thread_test.c`):
   ```c
   #include <stdio.h>
   #include <pthread.h>
   #include <unistd.h>

   int global_var = 10;

   void* thread_func(void* arg) {
       global_var += 20;
       printf("Thread: global_var = %d\n", global_var);
       return NULL;
   }

   int main() {
       pthread_t thread;
       pthread_create(&thread, NULL, thread_func, NULL);
       pthread_join(thread, NULL); // Wait for thread to finish

       printf("Main thread: global_var = %d\n", global_var);
       return 0;
   }
   ```

5. Compile and run (note the `-pthread` flag):
   ```bash
   $ gcc -o thread_test thread_test.c -pthread
   $ ./thread_test
   ```
   > **Observe:** The thread modifies `global_var`, and the main thread sees the change because threads share the same memory space.

   > 📸 **Required Screenshot 2:** Take a screenshot of the `thread_test` execution output. Save as `process_vs_thread_2.png`.

6. Return to `lab5`:
   ```bash
   $ cd ..
   ```

---

## Task 2 — Thread Interaction

**Scenario:** *"Now that you know threads share memory, let's create multiple threads and have them interact by passing data back and forth."*

**Instructions:**

1. Enter your lab directory:
   ```bash
   $ cd thread_lab
   ```

2. Create `multi_thread.c`:
   ```c
   #include <stdio.h>
   #include <stdlib.h>
   #include <pthread.h>

   #define NUM_THREADS 3

   void* worker_func(void* thread_id) {
       long tid = (long)thread_id;
       printf("Worker thread %ld starting...\n", tid);
       
       // Simulate some work
       long result = tid * 100;
       
       printf("Worker thread %ld finishing. Returning %ld\n", tid, result);
       pthread_exit((void*)result);
   }

   int main() {
       pthread_t threads[NUM_THREADS];
       int rc;
       long t;
       void* status;

       for(t = 0; t < NUM_THREADS; t++) {
           printf("Main: creating thread %ld\n", t);
           rc = pthread_create(&threads[t], NULL, worker_func, (void*)t);
           if (rc) {
               printf("ERROR; return code from pthread_create() is %d\n", rc);
               exit(-1);
           }
       }

       // Wait for all threads to complete and collect their results
       for(t = 0; t < NUM_THREADS; t++) {
           rc = pthread_join(threads[t], &status);
           if (rc) {
               printf("ERROR; return code from pthread_join() is %d\n", rc);
               exit(-1);
           }
           printf("Main: joined with thread %ld, status: %ld\n", t, (long)status);
       }

       printf("Main: program completed. Exiting.\n");
       return 0;
   }
   ```

3. Compile and run:
   ```bash
   $ gcc -o multi_thread multi_thread.c -pthread
   $ ./multi_thread
   ```

   > 📸 **Required Screenshot 3:** Take a screenshot of the `multi_thread` execution output. Save as `thread_interaction.png`.

4. Return to `lab5`:
   ```bash
   $ cd ..
   ```

---

## Task 3 — Visualizing Kernel Threads & Userspace Mapping

**Scenario:** *"Linux uses a 1:1 threading model and manages background work using 'Kernel Threads'. I need you to identify the mapping between user threads and kernel threads, and understand why you can't just kill system kernel workers."*

**Instructions:**

1. **Visualize the 1:1 Thread Model (User to Kernel Mapping):**
   Linux maps every user-level thread directly to one kernel-level thread (known as a Lightweight Process, or LWP). Let's visualize this mapping.
   We will run a sleeper thread process in the background:
   
   Create a quick script `sleeper_threads.c` in `thread_lab`:
   ```bash
   $ cd thread_lab
   $ cat << 'EOF' > sleeper_threads.c
   #include <pthread.h>
   #include <unistd.h>
   void* sleep_func(void* arg) { sleep(60); return NULL; }
   int main() {
       pthread_t t1, t2;
       pthread_create(&t1, NULL, sleep_func, NULL);
       pthread_create(&t2, NULL, sleep_func, NULL);
       sleep(60);
       return 0;
   }
   EOF
   $ gcc -o sleeper_threads sleeper_threads.c -pthread
   ```

   Run it in the background:
   ```bash
   $ ./sleeper_threads &
   $ MAIN_PID=$!
   ```

   Now, use `ps -eLf` to see the threads (LWPs) associated with that PID:
   ```bash
   $ ps -eLf | grep $MAIN_PID
   ```
   > **Observe:** You will see 3 rows for the same PID. The `LWP` column shows the unique kernel thread ID assigned to the main process and its two spawned user threads.

   Explore the `/proc` filesystem to see the threads directly at the kernel level:
   ```bash
   $ ls -l /proc/$MAIN_PID/task/
   ```
   > Each directory name here corresponds to an LWP (kernel thread) backing your user threads.
   
   > 📸 **Required Screenshot 4:** Take a screenshot showing either the `ps -eLf` output or the `/proc` task directory contents, proving the 1:1 mapping of threads. Save as `user_kernel_mapping.png`.

2. **Visualizing Kernel Workers with `htop`:**
   Kernel threads usually have a PPID (Parent Process ID) of 2 (kthreadd). They run entirely in kernel space to perform system tasks.
   
   Open `htop`:
   ```bash
   $ htop
   ```
   - Press `F2` -> Display options -> check "Show custom thread names" and ensure "Hide kernel threads" is **unchecked**.
   - Press `K` to toggle kernel threads on/off.
   - Press `H` to toggle user threads on/off.
   
   > 📸 **Required Screenshot 5:** Take a screenshot of `htop` showing kernel threads (look for green bracketed names or use the toggle to highlight them). Save as `htop_kernel_threads.png`.
   
   Exit `htop` (press `q`).

3. **Attempting to interact with kernel threads:**
   Pick a kernel thread PID from `htop` (e.g., `[kworker/...]`). Try to send a stop signal to it (replace `<PID>` with the actual PID).
   ```bash
   $ kill -STOP <PID>
   ```
   > **Note:** Even as root, interacting with kernel threads is severely restricted. They run in kernel space and are vital for system stability. You usually cannot stop, kill, or trace them like normal user processes.

4. Return to `lab5`:
   ```bash
   $ cd ..
   ```

---

## Task 4 — Recall: Process Signals and Handling

**Scenario:** *"In Lab 4, you learned how to send signals to manage processes from the shell. Now, we are going to dive deeper. You must understand how to write C code that actually catches those signals to perform graceful cleanup before exiting."*

**Instructions:**

1. Enter your lab directory:
   ```bash
   $ cd thread_lab
   ```

2. Create a C program that catches signals (`signal_handler.c`):
   ```c
   #include <stdio.h>
   #include <stdlib.h>
   #include <unistd.h>
   #include <signal.h>

   void sig_handler(int signo) {
       if (signo == SIGINT) {
           printf("\n[Signal Caught] Received SIGINT (Ctrl+C). Performing graceful shutdown...\n");
           // Simulate cleanup
           sleep(1);
           printf("Cleanup complete. Exiting safely.\n");
           exit(0);
       } else if (signo == SIGTERM) {
           printf("\n[Signal Caught] Received SIGTERM (kill). Saving state...\n");
           exit(0);
       }
   }

   int main() {
       // Register signal handlers
       if (signal(SIGINT, sig_handler) == SIG_ERR) {
           printf("Cannot catch SIGINT\n");
       }
       if (signal(SIGTERM, sig_handler) == SIG_ERR) {
           printf("Cannot catch SIGTERM\n");
       }

       printf("Process running with PID: %d\n", getpid());
       printf("Try pressing Ctrl+C or sending 'kill %d' from another terminal.\n", getpid());
       printf("Entering infinite loop...\n");

       while(1) {
           printf("Working...\n");
           sleep(2);
       }
       return 0;
   }
   ```

3. Compile the program:
   ```bash
   $ gcc -o signal_handler signal_handler.c
   ```

4. **Test SIGINT (Ctrl+C):**
   Run the program, wait a few seconds, then press `Ctrl+C`.
   ```bash
   $ ./signal_handler
   ```
   > 📸 **Required Screenshot 6:** Take a screenshot showing the output when you press `Ctrl+C` and the program gracefully catches `SIGINT`. Save as `signal_sigint.png`.

5. **Test SIGTERM (kill):**
   Run the program in the background:
   ```bash
   $ ./signal_handler &
   $ HANDLER_PID=$!
   ```
   Send the `SIGTERM` signal:
   ```bash
   $ kill -SIGTERM $HANDLER_PID
   ```
   Check that it exited gracefully.

6. **Test SIGKILL (kill -9):**
   `SIGKILL` cannot be caught or ignored. Let's prove it.
   Modify `signal_handler.c` to try and catch `SIGKILL` by adding:
   ```c
       if (signal(SIGKILL, sig_handler) == SIG_ERR) {
           printf("Warning: Cannot catch SIGKILL\n");
       }
   ```
   Compile and run:
   ```bash
   $ gcc -o signal_handler signal_handler.c
   $ ./signal_handler &
   $ kill -9 $!
   ```
   > You will see the warning that `SIGKILL` cannot be caught, and the process will be instantly killed when `kill -9` is issued without executing your cleanup block.

7. Return to `lab5`:
   ```bash
   $ cd ..
   ```

---

## 🧩 Challenge — Multithreading with Signals

**Task:** Create a C program named `challenge.c` in `thread_lab` that combines threads and signals. 
1. The main program should set up a signal handler for `SIGINT` (`Ctrl+C`).
2. It should spawn **two** worker threads that continuously print their thread ID and sleep for 1 second in an infinite loop.
3. When `SIGINT` is received, the signal handler should set a global flag `keep_running = 0`.
4. The worker threads should check this flag in their loop. If `0`, they should `pthread_exit`.
5. The main thread should `pthread_join` both threads and then print `"All threads cleanly exited. Goodbye."` before terminating.

Compile it and run it. Press `Ctrl+C` to watch it shut down gracefully.
> 📸 **Required Screenshot 7:** Take a screenshot of your `challenge.c` execution shutting down gracefully after receiving `Ctrl+C`. Save as `challenge_shutdown.png`.

---

## Final Submission

### Required Folder Structure

```
os-se-<YourStudentID>/
└── os-lab-<YourStudentID>/
    └── lab5/
        ├── README.md                   ← Your documentation
        ├── thread_lab/
        │   ├── process_test.c
        │   ├── thread_test.c
        │   ├── multi_thread.c
        │   ├── sleeper_threads.c
        │   ├── signal_handler.c
        │   └── challenge.c
        └── images/
            ├── process_vs_thread_1.png
            ├── process_vs_thread_2.png
            ├── thread_interaction.png
            ├── user_kernel_mapping.png
            ├── htop_kernel_threads.png
            ├── signal_sigint.png
            └── challenge_shutdown.png
```

### Git Push

```bash
$ cd ~/os-se-<YourStudentID>
$ git add .
$ git commit -m "Lab 5: Threads, Kernel Workers & Signals"
$ git push origin main
```
