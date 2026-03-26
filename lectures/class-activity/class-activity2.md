# Class Activity 2 — Processes & Inter-Process Communication (IPC)

> **Related Lectures**: Week 3 — Processes, Week 4 — Threads & Multicore  
> **Topics**: Process Creation (`fork`, `exec`), Windows Process Creation, Shared Memory IPC, Message Queue IPC  
> **Language**: C  
> **Environment**: Linux (native, VM, or WSL) + Windows (native, VS Code / MinGW)

---

> ⚠️ **IMPORTANT — READ EVERYTHING FIRST**
>
> **Before you write a single line of code, read through this ENTIRE document from top to bottom.** Scan every section — the background, the tasks, the deliverables, and the README template. Understand the full scope of what is expected **before** you start working.
>
> ⏱️ **Estimated time**: Reading this document takes about **20–30 minutes**. Completing all tasks takes approximately **3–4 hours** depending on your experience.
>
> **Document structure:**
> 1. **Objective** — What you'll learn
> 2. **Prerequisites** — What you need set up
> 3. **Background** — Process creation and IPC concepts
> 4. **Task Overview** — Summary of all tasks at a glance
> 5. **Tasks 1–4 (Required)** — Detailed instructions for each task
> 6. **Deliverables & Submission** — Folder structure, README template, git push
> 7. **Grading Criteria** — How your work will be evaluated

---

## Quick Navigation

| Section | Jump To |
|---------|---------|
| Objective | [▶ Objective](#objective) |
| Prerequisites | [▶ Prerequisites](#prerequisites) |
| Background | [▶ Background](#background) |
| Task Overview | [▶ Task Overview](#task-overview) |
| Task 1: Process Creation (Linux) | [▶ Task 1](#task-1-process-creation-on-linux-fork--exec) |
| Task 2: Process Creation (Windows) | [▶ Task 2](#task-2-process-creation-on-windows) |
| Task 3: Shared Memory IPC | [▶ Task 3](#task-3-shared-memory-ipc-linux) |
| Task 4: Message Queue IPC | [▶ Task 4](#task-4-message-queue-ipc-linux) |
| Deliverables & Submission | [▶ Deliverables](#deliverables--submission) |
| Grading Criteria | [▶ Grading](#grading-criteria) |
| References & Tips | [▶ References](#helpful-references) · [▶ Tips](#tips) |

---

## Objective

In the lectures, you learned that the operating system manages **processes** — running instances of programs — and provides mechanisms for processes to **communicate** with each other. In this activity, you will:

1. **Create child processes** on Linux using `fork()` and `exec()` system calls.
2. **Create child processes** on Windows using the `CreateProcess()` Win32 API.
3. **Exchange data between processes** using POSIX **shared memory**.
4. **Exchange data between processes** using POSIX **message queues**.

By the end, you will have hands-on experience with process creation on two different operating systems and two different IPC mechanisms.

---

## Prerequisites

- Basic C programming knowledge
- Completed Class Activity 1 (familiarity with compiling and running C programs)
- A Linux environment (Ubuntu VM, WSL, or native Linux)
- GCC compiler installed (`gcc --version` to verify)
- A Windows environment with a C compiler (MinGW / MSYS2 / Visual Studio)

### Quick Setup (if using WSL on Windows)

```bash
# Install WSL if not already present (run in PowerShell as Admin)
wsl --install

# Inside WSL, install build tools
sudo apt update
sudo apt install build-essential -y
```

---

## Background

### Process Creation

A **process** is a program in execution. Operating systems provide system calls to create new processes:

#### Linux: `fork()` and `exec()`

On Linux/UNIX, new processes are created in two steps:

1. **`fork()`** — Creates an exact copy (child) of the current process. Both parent and child continue executing from the same point, but `fork()` returns different values:
   - Returns `0` to the **child** process
   - Returns the **child's PID** to the **parent** process
   - Returns `-1` on **error**

2. **`exec()` family** — Replaces the current process image with a new program. After `exec()`, the process runs a completely different program. Common variants:
   - `execlp(file, arg0, arg1, ..., NULL)` — searches `PATH` for the executable
   - `execvp(file, argv[])` — like `execlp` but takes an argument array

```
Parent Process
     │
     ├── fork() ──► Child Process (copy of parent)
     │                    │
     │                    ├── exec("ls") ──► Child now runs "ls"
     │                    │
     │              Child terminates
     │
     ├── wait() ◄── Parent waits for child
     │
   Parent continues
```

#### Windows: `CreateProcess()`

On Windows, process creation is a **single step** — there is no `fork()`. Instead, `CreateProcess()` creates a new process and immediately loads the specified program:

```c
BOOL CreateProcess(
    LPCTSTR lpApplicationName,    // Path to executable (e.g., "C:\\Windows\\System32\\mspaint.exe")
    LPTSTR  lpCommandLine,        // Command line arguments (can be NULL)
    ...                           // Security attributes, inheritance, flags, etc.
    LPSTARTUPINFO lpStartupInfo,  // Startup configuration
    LPPROCESS_INFORMATION lpProcessInformation  // Receives process info (handle, PID)
);
```

Key differences from Linux:
- No `fork()` equivalent — Windows creates a process and loads a program in one call
- Uses **handles** (`HANDLE`) instead of integer file descriptors or PIDs
- The parent receives a `PROCESS_INFORMATION` structure containing the child's handle and PID

### Inter-Process Communication (IPC)

Processes are **isolated** from each other — they have separate address spaces. To exchange data, the OS provides **IPC mechanisms**:

#### Shared Memory

Two or more processes map the **same region of physical memory** into their address spaces. This is the **fastest** IPC method because data does not need to be copied between processes.

```
 ┌──────────────┐                ┌──────────────┐
 │  Producer     │                │  Consumer     │
 │  (Process A)  │                │  (Process B)  │
 │               │                │               │
 │  ptr ─────────┼───┐      ┌────┼── ptr         │
 └──────────────┘    │      │    └──────────────┘
                     ▼      ▼
              ┌──────────────────┐
              │  Shared Memory   │
              │  "Hello Pisey!"  │
              └──────────────────┘
```

Key POSIX functions:
- `shm_open()` — Create or open a shared memory object
- `ftruncate()` — Set the size of the shared memory
- `mmap()` — Map shared memory into the process's address space
- `shm_unlink()` — Remove the shared memory object

#### Message Queues

Processes communicate by sending and receiving **messages** through a named queue managed by the OS. Messages are stored in order (FIFO) and each message is an independent unit of data.

```
 ┌──────────┐         ┌──────────────────┐         ┌──────────┐
 │  Sender   │ ──send──►  Message Queue   │──recv──► │ Receiver │
 │ (Process) │         │  [msg1][msg2]... │         │ (Process)│
 └──────────┘         └──────────────────┘         └──────────┘
```

Key POSIX functions:
- `mq_open()` — Create or open a message queue
- `mq_send()` — Send a message to the queue
- `mq_receive()` — Receive a message from the queue
- `mq_close()` — Close the queue descriptor
- `mq_unlink()` — Remove the queue

---

## Task Overview

| Task | What You Do | Where | Key Concepts |
|------|------------|-------|-------------|
| **Task 1** | Write a C program using `fork()` + `exec()` to create a child process that runs `ls` | Linux | `fork()`, `exec()`, `wait()`, process hierarchy |
| **Task 2** | Write a C program using `CreateProcess()` to launch `mspaint.exe` as a child process | Windows | `CreateProcess()`, process handles, Task Manager |
| **Task 3** | Compile and run a shared memory producer/consumer pair | Linux | `shm_open()`, `mmap()`, shared memory IPC |
| **Task 4** | Create and run a message queue sender/receiver pair | Linux | `mq_open()`, `mq_send()`, `mq_receive()` |

---

## Task 1: Process Creation on Linux (`fork` + `exec`)

### Goal

Write a C program called `forkchild.c` that:
1. Calls `fork()` to create a child process.
2. In the child process, uses `execlp()` to run the `ls -la` command.
3. In the parent process, waits for the child to finish, then prints a message.

### Step-by-Step Instructions

#### 1. Navigate to your task folder

```bash
cd activity2/task1
```

#### 2. Create the source file

Create a file named `forkchild.c` with your preferred editor (nano, vim, VS Code, etc.).

#### 3. Write the program

Here is a **starter template** — read the comments and fill in the missing parts:

```c
/* forkchild.c — Process creation with fork() and exec() */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid;

    printf("Parent process (PID: %d) — creating child...\n", getpid());

    pid = fork();

    if (pid < 0) {
        /* fork failed */
        perror("fork");
        exit(EXIT_FAILURE);
    }
    else if (pid == 0) {
        /* ---- CHILD PROCESS ---- */
        printf("Child process (PID: %d, Parent PID: %d)\n", getpid(), getppid());

        /*
         * Sleep for 30 seconds so you have time to observe
         * the parent-child process tree in another terminal
         * using ps, top, or htop (see step 5 below).
         */
        printf("Child: sleeping 30s — observe the process tree now!\n");
        sleep(30);

        printf("Child: now executing 'ls -la'...\n");

        /* Replace this process with "ls -la" */
        execlp("ls", "ls", "-la", NULL);

        /* If execlp returns, it means it failed */
        perror("execlp");
        exit(EXIT_FAILURE);
    }
    else {
        /* ---- PARENT PROCESS ---- */
        int status;
        printf("Parent: waiting for child (PID: %d) to finish...\n", pid);

        waitpid(pid, &status, 0);

        if (WIFEXITED(status)) {
            printf("Parent: child exited with status %d\n", WEXITSTATUS(status));
        }
        printf("Parent: done.\n");
    }

    return 0;
}
```

#### 4. Compile and run

```bash
gcc -o forkchild forkchild.c
```

Run the program and save the output to a file:

```bash
./forkchild > result_forkchild.txt 2>&1
```

View the result:

```bash
cat result_forkchild.txt
```

#### 5. Observe the parent-child process tree

The child process sleeps for 30 seconds before running `ls`. **While it is sleeping**, open a **second terminal** (or a new SSH session) and use the following commands to observe the parent-child relationship:

**Option A — `ps` with forest view (recommended):**

```bash
ps -ef --forest | grep forkchild
```

This shows a tree view where the child process appears indented under the parent. You should see something like:

```
yourname  12345     1  0 10:00 pts/0  00:00:00 ./forkchild
yourname  12346 12345  0 10:00 pts/0  00:00:00  \_ ./forkchild
```

Notice that the child's **PPID** (Parent PID) matches the parent's **PID**.

**Option B — `pstree`:**

```bash
pstree -p $(pgrep -o forkchild)
```

This displays a compact tree with PIDs, e.g.: `forkchild(12345)───forkchild(12346)`

**Option C — `top` or `htop` (tree mode):**

```bash
# Using top — press Shift+V to toggle tree/forest view, then q to quit
top

# Or using htop — press F5 to toggle tree view, then q to quit
htop
```

In `htop`, press **F5** to switch to tree mode. You will see `forkchild` with its child indented below it.

> 📸 **Required Screenshot**: Take a screenshot of the process tree showing the parent-child relationship with PIDs visible. Use any of the commands above.

#### 6. Save your command history

```bash
history | tail -n 20 > command_used_forkchild.txt
```

### What to Submit for Task 1

| File | Description |
|------|-------------|
| `forkchild.c` | Your source code |
| `result_forkchild.txt` | Program output |
| `command_used_forkchild.txt` | Your terminal command history |
| Screenshot | Terminal showing compilation and execution |
| Screenshot | **Process tree** (`ps --forest`, `pstree`, or `htop` tree view) showing parent → child |

### Questions for Task 1

Answer these in your `README.md`:

1. **What does `fork()` return to the parent? What does it return to the child?**
2. **What happens if you remove the `waitpid()` call? Why might the output look different?**
3. **What does `execlp()` do? Why don't we see "execlp failed" when it succeeds?**
4. **Draw the process tree for your program (parent → child). Include PIDs from your output.**
5. **Which command did you use to view the process tree (`ps --forest`, `pstree`, or `htop`)? What information does each column show?**

---

## Task 2: Process Creation on Windows

### Goal

Write a C program called `winprocess.c` that uses the Windows API `CreateProcess()` to launch `mspaint.exe` as a child process. You will also take a screenshot of Task Manager to prove that `mspaint.exe` is running as a child of your program.

### Step-by-Step Instructions

> ⚠️ This task runs on **Windows**, not on the SSH server. Use your local machine with a C compiler (MinGW, MSYS2, or Visual Studio).

#### 1. Create the source file

Create a file named `winprocess.c`:

```c
/* winprocess.c — Process creation on Windows using CreateProcess() */
#include <stdio.h>
#include <windows.h>

int main() {
    STARTUPINFO si;
    PROCESS_INFORMATION pi;

    /* Zero out the structures */
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    printf("Parent process (PID: %lu) — creating child...\n", GetCurrentProcessId());

    /*
     * CreateProcess() parameters:
     *   lpApplicationName  — Full path to the executable
     *   lpCommandLine      — Command line string (NULL if using lpApplicationName)
     *   ... other parameters set to defaults ...
     *   lpStartupInfo      — Pointer to STARTUPINFO
     *   lpProcessInformation — Receives the new process info
     *
     * NOTE: The path to mspaint.exe is typically:
     *   "C:\\Windows\\System32\\mspaint.exe"
     *
     * If mspaint.exe is not at this path on your system, open Task Manager,
     * run mspaint manually, right-click the process, and select
     * "Open file location" to find the correct path.
     */
    if (!CreateProcess(
            "C:\\Windows\\System32\\mspaint.exe",  /* Application path */
            NULL,           /* Command line */
            NULL,           /* Process security attributes */
            NULL,           /* Thread security attributes */
            FALSE,          /* Inherit handles */
            0,              /* Creation flags */
            NULL,           /* Environment */
            NULL,           /* Current directory */
            &si,            /* Startup info */
            &pi             /* Process information */
        ))
    {
        fprintf(stderr, "CreateProcess failed (error %lu).\n", GetLastError());
        return 1;
    }

    printf("Child process created!\n");
    printf("  Child PID:       %lu\n", pi.dwProcessId);
    printf("  Child Thread ID: %lu\n", pi.dwThreadId);

    /*
     * Wait for the child process to finish.
     * mspaint will stay open — close it manually when you're done observing.
     * WaitForSingleObject blocks until the child terminates.
     */
    printf("Parent: waiting for child (mspaint) to exit...\n");
    printf(">>> Open Task Manager now and take a screenshot! <<<\n");
    printf(">>> Then close mspaint to let this program finish. <<<\n");

    WaitForSingleObject(pi.hProcess, INFINITE);

    printf("Parent: child has exited. Cleaning up.\n");

    /* Close process and thread handles */
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return 0;
}
```

#### 2. Compile

**Using MinGW (GCC):**

```powershell
gcc -o winprocess winprocess.c
```

**Using Visual Studio Developer Command Prompt:**

```cmd
cl winprocess.c
```

#### 3. Run

```powershell
.\winprocess.exe
```

The program will create `mspaint.exe` as a child process. **While mspaint is running**, observe the parent-child process tree in Task Manager:

#### Viewing the Process Tree in Task Manager

**Method 1 — Processes tab (tree view):**

1. Press `Ctrl + Shift + Esc` to open Task Manager.
2. Click on the **"Processes"** tab.
3. Find your terminal / compiler entry (e.g., **Windows Terminal**, **PowerShell**, **VS Code**).
4. Click the **expand arrow** (▶) next to it — you should see `mspaint.exe` nested underneath, showing the parent-child hierarchy visually.
5. **Take a screenshot** of this tree view.

> 📸 **Required Screenshot #1**: Task Manager **Processes tab** showing the expanded tree with `mspaint.exe` nested under your parent program.

**Method 2 — Details tab (PID & Parent PID columns):**

1. In Task Manager, click on the **"Details"** tab.
2. Right-click any column header → **"Select columns"** → check **"PID"** and **"Parent PID"** (PPID).
3. Find `mspaint.exe` in the list and verify that its **Parent PID** matches the **PID** of your `winprocess.exe`.
4. **Take a screenshot** showing both PID columns.

> 📸 **Required Screenshot #2**: Task Manager **Details tab** with PID and Parent PID columns visible, showing that `mspaint.exe`'s Parent PID matches your program's PID.

> 💡 **Tip:** You can also sort by the "Parent PID" column to group child processes under their parents.

#### 4. Close mspaint

Close the mspaint window. Your `winprocess.exe` program will detect that the child has exited and will print the final message.

### What to Submit for Task 2

| File | Description |
|------|-------------|
| `winprocess.c` | Your source code |
| Screenshot | **Task Manager Processes tab** — tree view showing mspaint nested under your program |
| Screenshot | **Task Manager Details tab** — PID and Parent PID columns showing the relationship |
| Screenshot | Terminal output showing parent/child PIDs |

### Questions for Task 2

Answer these in your `README.md`:

1. **What is the key difference between how Linux creates a process (`fork` + `exec`) and how Windows does it (`CreateProcess`)?**
2. **What does `WaitForSingleObject()` do? What is its Linux equivalent?**
3. **Why do we need to call `CloseHandle()` at the end? What happens if we don't?**
4. **In Task Manager, what was the PID of your parent program and the PID of mspaint? Do they match your program's output?**
5. **Compare the Processes tab (tree view) and the Details tab (PID/PPID columns). Which view makes it easier to understand the parent-child relationship? Why?**

---

## Task 3: Shared Memory IPC (Linux)

### Goal

Compile and run a **producer** and **consumer** program that communicate through POSIX shared memory. The producer writes a message to shared memory, and the consumer reads it.

### Step-by-Step Instructions

#### 1. Navigate to your task folder

```bash
cd activity2/task3_shm
```

#### 2. Create the producer

Create a file named `shm-producer.c` with your preferred editor.

Use the following code:

```c
/* shm-producer.c — Writes to POSIX shared memory */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

int main() {
    /* Size of the shared memory region (in bytes) */
    const int SIZE = 4096;

    /*
     * Name of the shared memory object.
     * ⚠️ IMPORTANT: Change "OS-yourname" to use YOUR OWN NAME.
     * Use a unique name to avoid conflicts if sharing the same machine.
     * Example: "OS-sokha", "OS-dara", "OS-chantha"
     */
    const char *name = "OS-yourname";

    /* Messages to write */
    const char *message_0 = "Hello, ";
    const char *message_1 = "this is shared memory IPC!";

    int shm_fd;      /* Shared memory file descriptor */
    void *ptr;        /* Pointer to mapped memory */

    /* Create the shared memory object (or open if it already exists) */
    shm_fd = shm_open(name, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        perror("shm_open");
        exit(EXIT_FAILURE);
    }

    /* Set the size of the shared memory region */
    if (ftruncate(shm_fd, SIZE) == -1) {
        perror("ftruncate");
        exit(EXIT_FAILURE);
    }

    /* Map the shared memory into this process's address space */
    ptr = mmap(0, SIZE, PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (ptr == MAP_FAILED) {
        perror("mmap");
        exit(EXIT_FAILURE);
    }

    /* Write messages to shared memory */
    sprintf(ptr, "%s", message_0);
    ptr += strlen(message_0);
    sprintf(ptr, "%s", message_1);
    ptr += strlen(message_1);

    printf("Producer: wrote to shared memory '%s'\n", name);
    printf("Producer: message = \"%s%s\"\n", message_0, message_1);

    return 0;
}
```

> ⚠️ **IMPORTANT:** Change `"OS-yourname"` to a name unique to you (e.g., `"OS-sokha"`).

#### 3. Create the consumer

Create a file named `shm-consumer.c` with your preferred editor.

Use the following code:

```c
/* shm-consumer.c — Reads from POSIX shared memory */
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

int main() {
    /* Must match the size used by the producer */
    const int SIZE = 4096;

    /*
     * Name of the shared memory object.
     * ⚠️ This MUST match the name used in shm-producer.c!
     */
    const char *name = "OS-yourname";

    int shm_fd;
    void *ptr;

    /* Open the existing shared memory object (read-only) */
    shm_fd = shm_open(name, O_RDONLY, 0666);
    if (shm_fd == -1) {
        perror("shm_open");
        fprintf(stderr, "Hint: Did you run shm-producer first?\n");
        exit(EXIT_FAILURE);
    }

    /* Map the shared memory into this process's address space */
    ptr = mmap(0, SIZE, PROT_READ, MAP_SHARED, shm_fd, 0);
    if (ptr == MAP_FAILED) {
        perror("mmap");
        exit(EXIT_FAILURE);
    }

    /* Read and display the contents */
    printf("Consumer: reading from shared memory '%s'\n", name);
    printf("Consumer: message = \"%s\"\n", (char *)ptr);

    /* Clean up — remove the shared memory object */
    if (shm_unlink(name) == -1) {
        perror("shm_unlink");
        exit(EXIT_FAILURE);
    }
    printf("Consumer: shared memory unlinked.\n");

    return 0;
}
```

> ⚠️ **IMPORTANT:** Make sure the `name` variable matches **exactly** what you used in `shm-producer.c`.

#### 4. Compile both programs

```bash
gcc -o shm-producer shm-producer.c -lrt
gcc -o shm-consumer shm-consumer.c -lrt
```

> 💡 The `-lrt` flag links the POSIX real-time library, which provides `shm_open()` and related functions.

#### 5. Run the producer, then the consumer

```bash
# Step 1: Run the producer (writes to shared memory)
./shm-producer

# Step 2: Run the consumer (reads from shared memory and saves output)
./shm-consumer > result-shm-ipc.txt

# View the result
cat result-shm-ipc.txt
```

#### 6. Save your command history

```bash
history | tail -n 20 > command_used_shm.txt
```

### What to Submit for Task 3

| File | Description |
|------|-------------|
| `shm-producer.c` | Producer source code (with your unique name) |
| `shm-consumer.c` | Consumer source code (with matching name) |
| `result-shm-ipc.txt` | Consumer output |
| `command_used_shm.txt` | Your terminal command history |
| Screenshot | Terminal showing compilation and both programs running |

### Questions for Task 3

Answer these in your `README.md`:

1. **What does `shm_open()` do? How is it different from `open()`?**
2. **What does `mmap()` do? Why is shared memory faster than other IPC methods?**
3. **Why must the shared memory name match between producer and consumer?**
4. **What does `shm_unlink()` do? What would happen if the consumer didn't call it?**
5. **If the consumer runs before the producer, what happens? Try it and describe the error.**

---

## Task 4: Message Queue IPC (Linux)

### Goal

Create and run a **sender** and **receiver** program that communicate through POSIX message queues. The sender puts a message into the queue, and the receiver retrieves it.

### Step-by-Step Instructions

#### 1. Navigate to your task folder

```bash
cd activity2/task4_mq
```

#### 2. Create the common header file

Create a file named `common.h` with your preferred editor.

Use the following code:

```c
/* common.h — Shared constants for message queue IPC */
#ifndef COMMON_H
#define COMMON_H

/*
 * ⚠️ IMPORTANT: Change the queue name to something unique to you!
 * The name MUST start with a forward slash '/'.
 * Example: "/queue-sokha", "/queue-dara", "/queue-chantha"
 */
#define QUEUE_NAME  "/queue-yourname"
#define MAX_SIZE    1024

#endif
```

> ⚠️ **IMPORTANT:** Change `"/queue-yourname"` to a name unique to you. Queue names **must** start with a `/`.

#### 3. Create the sender

Create a file named `sender.c` with your preferred editor.

Use the following code:

```c
/* sender.c — Sends a message through a POSIX message queue */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mqueue.h>
#include <fcntl.h>
#include <sys/stat.h>
#include "common.h"

int main() {
    mqd_t mq;
    struct mq_attr attr;

    /* Configure queue attributes */
    attr.mq_flags   = 0;          /* Blocking mode */
    attr.mq_maxmsg  = 10;         /* Max messages in queue */
    attr.mq_msgsize = MAX_SIZE;   /* Max size of each message */
    attr.mq_curmsgs = 0;          /* Number of messages currently in queue */

    /* Create (or open) the message queue */
    mq = mq_open(QUEUE_NAME, O_CREAT | O_WRONLY, 0644, &attr);
    if (mq == (mqd_t)-1) {
        perror("mq_open");
        exit(EXIT_FAILURE);
    }

    /* Prepare and send the message */
    const char *message = "Hello from sender! This is message queue IPC.";

    if (mq_send(mq, message, strlen(message) + 1, 0) == -1) {
        perror("mq_send");
        exit(EXIT_FAILURE);
    }

    printf("Sender: message sent to queue '%s'\n", QUEUE_NAME);
    printf("Sender: message = \"%s\"\n", message);

    /* Close the queue (does not delete it) */
    mq_close(mq);

    return 0;
}
```

#### 4. Create the receiver

Create a file named `receiver.c` with your preferred editor.

Use the following code:

```c
/* receiver.c — Receives a message from a POSIX message queue */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mqueue.h>
#include <fcntl.h>
#include "common.h"

int main() {
    mqd_t mq;
    struct mq_attr attr;
    char buffer[MAX_SIZE + 1];

    /* Open the existing message queue (read-only) */
    mq = mq_open(QUEUE_NAME, O_RDONLY);
    if (mq == (mqd_t)-1) {
        perror("mq_open");
        fprintf(stderr, "Hint: Did you run sender first?\n");
        exit(EXIT_FAILURE);
    }

    /* Get queue attributes to know the message size */
    mq_getattr(mq, &attr);

    /* Receive a message from the queue */
    if (mq_receive(mq, buffer, attr.mq_msgsize, NULL) == -1) {
        perror("mq_receive");
        exit(EXIT_FAILURE);
    }

    printf("Receiver: message received from queue '%s'\n", QUEUE_NAME);
    printf("Receiver: message = \"%s\"\n", buffer);

    /* Close and remove the queue */
    mq_close(mq);

    if (mq_unlink(QUEUE_NAME) == -1) {
        perror("mq_unlink");
        exit(EXIT_FAILURE);
    }
    printf("Receiver: queue unlinked.\n");

    return 0;
}
```

#### 5. Compile both programs

```bash
gcc -o sender sender.c -lrt
gcc -o receiver receiver.c -lrt
```

> 💡 The `-lrt` flag links the POSIX real-time library, required for `mq_open()` and related functions.

#### 6. Run the sender, then the receiver

```bash
# Step 1: Run the sender (puts a message in the queue)
./sender

# Step 2: Run the receiver (reads the message and saves output)
./receiver > result-mq-ipc.txt

# View the result
cat result-mq-ipc.txt
```

#### 7. Save your command history

```bash
history | tail -n 20 > command_used_mq.txt
```

### What to Submit for Task 4

| File | Description |
|------|-------------|
| `common.h` | Shared header file (with your unique queue name) |
| `sender.c` | Sender source code |
| `receiver.c` | Receiver source code |
| `result-mq-ipc.txt` | Receiver output |
| `command_used_mq.txt` | Your terminal command history |
| Screenshot | Terminal showing compilation and both programs running |

### Questions for Task 4

Answer these in your `README.md`:

1. **How is a message queue different from shared memory? When would you use one over the other?**
2. **Why does the queue name in `common.h` need to start with `/`?**
3. **What does `mq_unlink()` do? What happens if neither the sender nor receiver calls it?**
4. **What happens if you run the receiver before the sender?**
5. **Can multiple senders send to the same queue? Can multiple receivers read from the same queue?**

---

## Deliverables & Submission

### What to Submit

Everything goes in your **README.md** — there is no separate answers file. Your `README.md` must contain:

1. **Your name and student ID**
2. **Screenshots** of compiling and running each task
3. **Answers** to all questions listed under each task
4. **Source code** files in the task folders
5. **Output files** (`.txt` files) as specified in each task

### Submission Folder Structure

All class activities go inside your personal `os-se-<YourStudentID>/` repository:

```
os-se-<YourStudentID>/
├── os-lab-<YourStudentID>/                  # ← Your lab submissions (existing)
│   └── ...
│
└── os-class-activities-<YourStudentID>/     # ← Your class activity submissions
    ├── activity1/                            # ← Activity 1 (already done)
    │   └── ...
    └── activity2/
        ├── README.md                         # ← Your report: screenshots + answers
        ├── screenshots/                      # Screenshot images
        │   ├── task1_compile_run.png
        │   ├── task1_process_tree.png
        │   ├── task2_compile_run.png
        │   ├── task2_taskmanager_tree.png
        │   ├── task2_taskmanager_details.png
        │   ├── task3_compile_run.png
        │   └── task4_compile_run.png
        ├── task1/
        │   ├── forkchild.c
        │   ├── result_forkchild.txt
        │   └── command_used_forkchild.txt
        ├── task2/
        │   └── winprocess.c
        ├── task3_shm/
        │   ├── shm-producer.c
        │   ├── shm-consumer.c
        │   ├── result-shm-ipc.txt
        │   └── command_used_shm.txt
        └── task4_mq/
            ├── common.h
            ├── sender.c
            ├── receiver.c
            ├── result-mq-ipc.txt
            └── command_used_mq.txt
```

### Setting Up Your Activity Folder

```bash
# Navigate to your existing submission repo
cd os-se-<YourStudentID>

# Create the activity 2 folder structure
mkdir -p os-class-activities-<YourStudentID>/activity2/{task1,task2,task3_shm,task4_mq,screenshots}

# Start working
cd os-class-activities-<YourStudentID>/activity2
```

### Pushing to Git

```bash
# Make sure you are in the root of your repo
cd os-se-<YourStudentID>

# Stage your class activity files
git add os-class-activities-<YourStudentID>/activity2/

# Commit with a meaningful message
git commit -m "Add class activity 2 — Processes & IPC"

# Push to your remote repository
git push origin main
```

> **Reminder:** Commit and push **regularly** as you work — do not wait until the last minute.

### README Template for Activity 2

Create a `README.md` inside your `activity2/` folder using this template:

````markdown
# Class Activity 2 — Processes & Inter-Process Communication

- **Student Name:** [Your Name Here]
- **Student ID:** [Your Student ID Here]
- **Date:** [Date of Submission]

---

## Task 1: Process Creation on Linux (fork + exec)

### Compilation & Execution

Screenshot of compiling and running `forkchild.c`:

![Task 1 - Compile & Run](screenshots/task1_compile_run.png)

### Process Tree

Screenshot of the parent-child process tree (using `ps --forest`, `pstree`, or `htop` tree view):

![Task 1 - Process Tree](screenshots/task1_process_tree.png)

### Output

```
[Paste the content of result_forkchild.txt here]
```

### Questions

1. **What does `fork()` return to the parent? What does it return to the child?**

   > [Your answer]

2. **What happens if you remove the `waitpid()` call? Why might the output look different?**

   > [Your answer]

3. **What does `execlp()` do? Why don't we see "execlp failed" when it succeeds?**

   > [Your answer]

4. **Draw the process tree for your program (parent → child). Include PIDs from your output.**

   > [Your answer / diagram]

5. **Which command did you use to view the process tree (`ps --forest`, `pstree`, or `htop`)? What information does each column show?**

   > [Your answer]

---

## Task 2: Process Creation on Windows

### Compilation & Execution

Screenshot of compiling and running `winprocess.c`:

![Task 2 - Compile & Run](screenshots/task2_compile_run.png)

### Task Manager Screenshots

Screenshot showing process tree in the **Processes** tab (mspaint nested under your program):

![Task 2 - Task Manager Tree](screenshots/task2_taskmanager_tree.png)

Screenshot showing PID and Parent PID in the **Details** tab:

![Task 2 - Task Manager Details](screenshots/task2_taskmanager_details.png)

### Questions

1. **What is the key difference between how Linux creates a process (`fork` + `exec`) and how Windows does it (`CreateProcess`)?**

   > [Your answer]

2. **What does `WaitForSingleObject()` do? What is its Linux equivalent?**

   > [Your answer]

3. **Why do we need to call `CloseHandle()` at the end? What happens if we don't?**

   > [Your answer]

4. **In Task Manager, what was the PID of your parent program and the PID of mspaint? Do they match your program's output?**

   > [Your answer]

5. **Compare the Processes tab (tree view) and the Details tab (PID/PPID columns). Which view makes it easier to understand the parent-child relationship? Why?**

   > [Your answer]

---

## Task 3: Shared Memory IPC

### Compilation & Execution

Screenshot of compiling and running `shm-producer` and `shm-consumer`:

![Task 3 - Compile & Run](screenshots/task3_compile_run.png)

### Output

```
[Paste the content of result-shm-ipc.txt here]
```

### Questions

1. **What does `shm_open()` do? How is it different from `open()`?**

   > [Your answer]

2. **What does `mmap()` do? Why is shared memory faster than other IPC methods?**

   > [Your answer]

3. **Why must the shared memory name match between producer and consumer?**

   > [Your answer]

4. **What does `shm_unlink()` do? What would happen if the consumer didn't call it?**

   > [Your answer]

5. **If the consumer runs before the producer, what happens? Try it and describe the error.**

   > [Your answer]

---

## Task 4: Message Queue IPC

### Compilation & Execution

Screenshot of compiling and running `sender` and `receiver`:

![Task 4 - Compile & Run](screenshots/task4_compile_run.png)

### Output

```
[Paste the content of result-mq-ipc.txt here]
```

### Questions

1. **How is a message queue different from shared memory? When would you use one over the other?**

   > [Your answer]

2. **Why does the queue name in `common.h` need to start with `/`?**

   > [Your answer]

3. **What does `mq_unlink()` do? What happens if neither the sender nor receiver calls it?**

   > [Your answer]

4. **What happens if you run the receiver before the sender?**

   > [Your answer]

5. **Can multiple senders send to the same queue? Can multiple receivers read from the same queue?**

   > [Your answer]

---

## Reflection

What did you learn from this activity? What was the most interesting difference between Linux and Windows process creation? Which IPC method do you prefer and why?

> [Write your reflection here]
````

---

## Grading Criteria

| Criteria | Points |
|----------|--------|
| Task 1 — `forkchild.c` compiles, runs, output saved | 10 |
| Task 1 — Process tree screenshot (`ps --forest` / `pstree` / `htop`) | 10 |
| Task 1 — Questions answered thoughtfully | 10 |
| Task 2 — `winprocess.c` compiles and runs mspaint as child | 5 |
| Task 2 — Task Manager screenshots (Processes tree + Details PID/PPID) | 10 |
| Task 2 — Questions answered thoughtfully | 5 |
| Task 3 — Shared memory producer/consumer compile and run | 10 |
| Task 3 — `result-shm-ipc.txt` shows correct output | 5 |
| Task 3 — Questions answered thoughtfully | 10 |
| Task 4 — Message queue sender/receiver compile and run | 10 |
| Task 4 — `result-mq-ipc.txt` shows correct output | 5 |
| Task 4 — Questions answered thoughtfully | 10 |
| **Total** | **100** |

---

## Helpful References

- **`fork()` man page**: `man 2 fork` or [online](https://man7.org/linux/man-pages/man2/fork.2.html)
- **`exec()` family**: `man 3 exec` or [online](https://man7.org/linux/man-pages/man3/exec.3.html)
- **`wait()` / `waitpid()`**: `man 2 waitpid` or [online](https://man7.org/linux/man-pages/man2/waitpid.2.html)
- **Windows `CreateProcess()`**: [Microsoft Docs](https://learn.microsoft.com/en-us/windows/win32/procthread/creating-processes)
- **POSIX Shared Memory**: `man 7 shm_overview` or [online](https://man7.org/linux/man-pages/man7/shm_overview.7.html)
- **POSIX Message Queues**: `man 7 mq_overview` or [online](https://man7.org/linux/man-pages/man7/mq_overview.7.html)

---

## Tips

- **Always check return values.** System calls return `-1` on error — use `perror()` to print meaningful error messages.
- **Use unique names** for shared memory and message queues to avoid conflicts.
- **Run the producer/sender first**, then the consumer/receiver. The consumer/receiver cannot read data that hasn't been written yet.
- **Don't forget `-lrt`** when compiling shared memory and message queue programs. Without it, you'll get "undefined reference" errors.
- **For Task 2 (Windows):** If `mspaint.exe` is not at `C:\Windows\System32\mspaint.exe`, open Task Manager, start mspaint manually, and check the executable path from the process details.
- **Save your work frequently** with `git commit` and `git push`.
