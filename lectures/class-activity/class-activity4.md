# Class Activity 4 — Shared File API: C++ Mutex & Java `synchronized`

> **Related Lectures**: Week 7 — Critical Sections, Week 8 — Synchronization  
> **Topics**: Race conditions, shared files, client/server design, C++ `std::mutex`, Java `synchronized`  
> **Language**: C++, Java  
> **Environment**: Two student machines on the same network, with `g++` and Java JDK

---

## Objective

In this activity, each pair builds a small **server program** that acts like an API for updating a shared file. One student's machine will run the server. Both students will run client programs from their own machines at the same time.

Clients do **not** update the file directly. Instead, clients connect to the server and send a request such as:

```text
ADD studentA
```

The server receives the request and updates:

```text
shared_score.txt
```

You will run the server in two versions:

1. **Before synchronization** — race condition can happen.
2. **After synchronization** — C++ uses `std::mutex`, Java uses `synchronized`.

By the end, you should understand why one server program can safely control a shared file, and why the server still needs synchronization when it handles multiple client requests at the same time.

---

## Key Idea

Without a server:

```text
Client A writes shared_score.txt
Client B writes shared_score.txt
Client C writes shared_score.txt
```

Many programs touch the same file directly. Race conditions are likely.

With a server:

```text
Client A ─┐
Client B ─┼──> Server API ───> shared_score.txt
Client C ─┘
```

Only the server touches the file. The clients send requests.

However, if the server creates one thread per client, then multiple server threads may still update the file at the same time. That is why the server needs a mutex or synchronized method.

---

## Task Overview

| Task | What You Do | Screenshot Required |
|------|-------------|--------------------|
| **Task 1** | Run C++ server/client before mutex | C++ before mutex |
| **Task 2** | Run C++ server/client after mutex | C++ after mutex |
| **Task 3** | Run Java server/client before `synchronized` | Java before synchronized |
| **Task 4** | Run Java server/client after `synchronized` | Java after synchronized |

You must submit **4 screenshots total**. Each screenshot may be a combined screenshot/collage, but it must include the server terminal and both client terminals:

1. C++ server before mutex
2. C++ server after mutex
3. Java server before `synchronized`
4. Java server after `synchronized`

Each screenshot must show:

- The server terminal
- Student A's client terminal
- Student B's client terminal
- The final `shared_score.txt` value

---

## Pair Setup

Choose one machine to be the **server machine**. Both students will use their own machines as clients.

On the server machine, create your activity folder:

```bash
$ mkdir -p activity4/{cpp_before,cpp_after,java_before,java_after,screenshots}
$ cd activity4
$ echo 0 > shared_score.txt
```

Find the server machine's IP address:

```bash
$ hostname -I
```

Write this IP address in your README. Your partner will use it when running the client.

Example:

```text
Server IP: 192.168.1.25
```

Whenever you see `<SERVER_IP>` in a command, replace it with the real IP address of the server machine.

Example:

```bash
$ ./cpp_before/client 192.168.1.25 A_1
$ java -cp java_before ScoreClient 192.168.1.25 B_1
```

If a port is already used on your machine, change the port number in both the matching server and client.

Both students need a copy of the client program folder on their own machines. The server machine needs both the server and client files.

Suggested ports:

| Version | Port |
|---------|------|
| C++ before mutex | 9001 |
| C++ after mutex | 9002 |
| Java before synchronized | 9011 |
| Java after synchronized | 9012 |

---

## Task 1: C++ Server Before Mutex

### Goal

Run a C++ server that handles each client in a separate thread, but does **not** protect the shared file.

### Create `cpp_before/server_no_mutex.cpp`

```cpp
#include <arpa/inet.h>
#include <chrono>
#include <fstream>
#include <iostream>
#include <string>
#include <thread>
#include <unistd.h>

const int PORT = 9001;
const std::string FILE_NAME = "shared_score.txt";

int update_score(const std::string& name) {
    std::ifstream input(FILE_NAME);
    int score = 0;
    input >> score;
    input.close();

    std::this_thread::sleep_for(std::chrono::milliseconds(200));

    score++;

    std::ofstream output(FILE_NAME);
    output << score << std::endl;
    output.close();

    std::cout << name << " updated score to " << score << std::endl;
    return score;
}

void handle_client(int client_socket) {
    char buffer[1024] = {0};
    read(client_socket, buffer, sizeof(buffer) - 1);

    std::string name = buffer;
    int score = update_score(name);
    std::string reply = "Score is now " + std::to_string(score) + "\n";

    send(client_socket, reply.c_str(), reply.size(), 0);
    close(client_socket);
}

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    sockaddr_in address{};
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    bind(server_fd, (sockaddr*)&address, sizeof(address));
    listen(server_fd, 20);

    std::cout << "C++ no-mutex server running on port " << PORT << std::endl;

    while (true) {
        int client_socket = accept(server_fd, nullptr, nullptr);
        std::thread(handle_client, client_socket).detach();
    }
}
```

### Create `cpp_before/client.cpp`

```cpp
#include <arpa/inet.h>
#include <iostream>
#include <string>
#include <unistd.h>

const int PORT = 9001;

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cout << "Usage: ./client <server_ip> <student_name>" << std::endl;
        return 1;
    }

    std::string server_ip = argv[1];
    std::string name = argv[2];

    int sock = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in server{};
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);
    inet_pton(AF_INET, server_ip.c_str(), &server.sin_addr);

    connect(sock, (sockaddr*)&server, sizeof(server));
    send(sock, name.c_str(), name.size(), 0);

    char buffer[1024] = {0};
    read(sock, buffer, sizeof(buffer) - 1);
    std::cout << buffer;

    close(sock);
    return 0;
}
```

### Compile and Run

Open Terminal 1:

```bash
$ cd activity4
$ echo 0 > shared_score.txt
$ g++ -std=c++17 cpp_before/server_no_mutex.cpp -o cpp_before/server_no_mutex -pthread
$ ./cpp_before/server_no_mutex
```

On Student A's machine:

```bash
$ cd activity4
$ g++ -std=c++17 cpp_before/client.cpp -o cpp_before/client
$ for i in {1..10}; do ./cpp_before/client <SERVER_IP> A_$i & done
$ wait
```

On Student B's machine, run at the same time:

```bash
$ cd activity4
$ g++ -std=c++17 cpp_before/client.cpp -o cpp_before/client
$ for i in {1..10}; do ./cpp_before/client <SERVER_IP> B_$i & done
$ wait
```

On the server machine:

```bash
$ cat shared_score.txt
```

Expected idea:

```text
Expected score: 20
Actual score may be less than 20
```

Repeat the test several times. Reset the file before each test:

```bash
$ echo 0 > shared_score.txt
```

The race condition may not appear every time because it depends on timing.

Take one screenshot:

```text
screenshots/cpp_before_mutex.png
```

The screenshot must show the server terminal and both students' client terminals.

---

## Task 2: C++ Server After Mutex

### Goal

Fix the server by protecting the file update with `std::mutex`.

### Create `cpp_after/server_mutex.cpp`

Use the same server as Task 1, but add a mutex.

```cpp
#include <arpa/inet.h>
#include <chrono>
#include <fstream>
#include <iostream>
#include <mutex>
#include <string>
#include <thread>
#include <unistd.h>

const int PORT = 9002;
const std::string FILE_NAME = "shared_score.txt";
std::mutex file_mutex;

int update_score(const std::string& name) {
    std::lock_guard<std::mutex> lock(file_mutex);

    std::ifstream input(FILE_NAME);
    int score = 0;
    input >> score;
    input.close();

    std::this_thread::sleep_for(std::chrono::milliseconds(200));

    score++;

    std::ofstream output(FILE_NAME);
    output << score << std::endl;
    output.close();

    std::cout << name << " updated score to " << score << std::endl;
    return score;
}

void handle_client(int client_socket) {
    char buffer[1024] = {0};
    read(client_socket, buffer, sizeof(buffer) - 1);

    std::string name = buffer;
    int score = update_score(name);
    std::string reply = "Score is now " + std::to_string(score) + "\n";

    send(client_socket, reply.c_str(), reply.size(), 0);
    close(client_socket);
}

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    sockaddr_in address{};
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    bind(server_fd, (sockaddr*)&address, sizeof(address));
    listen(server_fd, 20);

    std::cout << "C++ mutex server running on port " << PORT << std::endl;

    while (true) {
        int client_socket = accept(server_fd, nullptr, nullptr);
        std::thread(handle_client, client_socket).detach();
    }
}
```

### Create `cpp_after/client.cpp`

Same as the previous C++ client, but change the port:

```cpp
const int PORT = 9002;
```

### Compile and Run

Terminal 1:

```bash
$ cd activity4
$ echo 0 > shared_score.txt
$ g++ -std=c++17 cpp_after/server_mutex.cpp -o cpp_after/server_mutex -pthread
$ ./cpp_after/server_mutex
```

On Student A's machine:

```bash
$ cd activity4
$ g++ -std=c++17 cpp_after/client.cpp -o cpp_after/client
$ for i in {1..10}; do ./cpp_after/client <SERVER_IP> A_$i & done
$ wait
```

On Student B's machine, run at the same time:

```bash
$ cd activity4
$ g++ -std=c++17 cpp_after/client.cpp -o cpp_after/client
$ for i in {1..10}; do ./cpp_after/client <SERVER_IP> B_$i & done
$ wait
```

On the server machine:

```bash
$ cat shared_score.txt
```

Expected result:

```text
20
```

Repeat the test multiple times. After adding the mutex, the final result should be consistent.

Take one screenshot:

```text
screenshots/cpp_after_mutex.png
```

The screenshot must show the server terminal and both students' client terminals.

---

## Task 3: Java Server Before `synchronized`

### Goal

Run a Java server that handles each client in a new thread, but does **not** protect the shared file.

### Create `java_before/ScoreServerNoSync.java`

```java
import java.io.*;
import java.net.*;

public class ScoreServerNoSync {
    private static final int PORT = 9011;
    private static final String FILE_NAME = "shared_score.txt";

    private static int updateScore(String name) throws Exception {
        File file = new File(FILE_NAME);
        int score = 0;

        if (file.exists()) {
            BufferedReader reader = new BufferedReader(new FileReader(file));
            String line = reader.readLine();
            reader.close();
            if (line != null && !line.isBlank()) {
                score = Integer.parseInt(line.trim());
            }
        }

        Thread.sleep(200);

        score++;

        FileWriter writer = new FileWriter(file, false);
        writer.write(score + "\n");
        writer.close();

        System.out.println(name + " updated score to " + score);
        return score;
    }

    private static void handleClient(Socket socket) {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

            String name = in.readLine();
            int score = updateScore(name);
            out.println("Score is now " + score);

            socket.close();
        } catch (Exception e) {
            System.out.println("Client error: " + e.getMessage());
        }
    }

    public static void main(String[] args) throws Exception {
        ServerSocket server = new ServerSocket(PORT);
        System.out.println("Java no-sync server running on port " + PORT);

        while (true) {
            Socket socket = server.accept();
            new Thread(() -> handleClient(socket)).start();
        }
    }
}
```

### Create `java_before/ScoreClient.java`

```java
import java.io.*;
import java.net.*;

public class ScoreClient {
    private static final int PORT = 9011;

    public static void main(String[] args) throws Exception {
        if (args.length < 2) {
            System.out.println("Usage: java ScoreClient <server_ip> <student_name>");
            return;
        }

        String serverIp = args[0];
        String name = args[1];

        Socket socket = new Socket(serverIp, PORT);
        BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

        out.println(name);
        System.out.println(in.readLine());

        socket.close();
    }
}
```

### Compile and Run

Terminal 1:

```bash
$ cd activity4
$ echo 0 > shared_score.txt
$ javac java_before/ScoreServerNoSync.java java_before/ScoreClient.java
$ java -cp java_before ScoreServerNoSync
```

On Student A's machine:

```bash
$ cd activity4
$ for i in {1..10}; do java -cp java_before ScoreClient <SERVER_IP> A_$i & done
$ wait
```

On Student B's machine, run at the same time:

```bash
$ cd activity4
$ for i in {1..10}; do java -cp java_before ScoreClient <SERVER_IP> B_$i & done
$ wait
```

On the server machine:

```bash
$ cat shared_score.txt
```

Expected idea:

```text
Expected score: 20
Actual score may be less than 20
```

Repeat the test several times. Reset the file before each test:

```bash
$ echo 0 > shared_score.txt
```

Take one screenshot:

```text
screenshots/java_before_synchronized.png
```

The screenshot must show the server terminal and both students' client terminals.

---

## Task 4: Java Server After `synchronized`

### Goal

Fix the Java server by protecting the file update with `synchronized`.

### Create `java_after/ScoreServerSync.java`

```java
import java.io.*;
import java.net.*;

public class ScoreServerSync {
    private static final int PORT = 9012;
    private static final String FILE_NAME = "shared_score.txt";

    private static synchronized int updateScore(String name) throws Exception {
        File file = new File(FILE_NAME);
        int score = 0;

        if (file.exists()) {
            BufferedReader reader = new BufferedReader(new FileReader(file));
            String line = reader.readLine();
            reader.close();
            if (line != null && !line.isBlank()) {
                score = Integer.parseInt(line.trim());
            }
        }

        Thread.sleep(200);

        score++;

        FileWriter writer = new FileWriter(file, false);
        writer.write(score + "\n");
        writer.close();

        System.out.println(name + " updated score to " + score);
        return score;
    }

    private static void handleClient(Socket socket) {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

            String name = in.readLine();
            int score = updateScore(name);
            out.println("Score is now " + score);

            socket.close();
        } catch (Exception e) {
            System.out.println("Client error: " + e.getMessage());
        }
    }

    public static void main(String[] args) throws Exception {
        ServerSocket server = new ServerSocket(PORT);
        System.out.println("Java synchronized server running on port " + PORT);

        while (true) {
            Socket socket = server.accept();
            new Thread(() -> handleClient(socket)).start();
        }
    }
}
```

### Create `java_after/ScoreClient.java`

Same as the previous Java client, but change the port:

```java
private static final int PORT = 9012;
```

### Compile and Run

Terminal 1:

```bash
$ cd activity4
$ echo 0 > shared_score.txt
$ javac java_after/ScoreServerSync.java java_after/ScoreClient.java
$ java -cp java_after ScoreServerSync
```

On Student A's machine:

```bash
$ cd activity4
$ for i in {1..10}; do java -cp java_after ScoreClient <SERVER_IP> A_$i & done
$ wait
```

On Student B's machine, run at the same time:

```bash
$ cd activity4
$ for i in {1..10}; do java -cp java_after ScoreClient <SERVER_IP> B_$i & done
$ wait
```

On the server machine:

```bash
$ cat shared_score.txt
```

Expected result:

```text
20
```

Repeat the test multiple times. After adding `synchronized`, the final result should be consistent.

Take one screenshot:

```text
screenshots/java_after_synchronized.png
```

The screenshot must show the server terminal and both students' client terminals.

---

## Questions

Answer these in your `README.md`:

1. Why should clients send requests to the server instead of writing the file directly?
2. Why does the server still have a race condition before mutex or `synchronized`?
3. In the C++ fixed version, what does `std::lock_guard<std::mutex>` protect?
4. In the Java fixed version, what does `synchronized` protect?
5. Why is the final score expected to be 20 when Student A sends 10 requests and Student B sends 10 requests?
6. What could happen if two separate servers update the same file at the same time?

---

## Deliverables & Submission

### Required Screenshots

Submit these 4 screenshots:

```text
screenshots/cpp_before_mutex.png
screenshots/cpp_after_mutex.png
screenshots/java_before_synchronized.png
screenshots/java_after_synchronized.png
```

Each screenshot should show:

- Server running
- Student A's client program running from Student A's machine
- Student B's client program running from Student B's machine
- Final `shared_score.txt` value

### Pair Submission Rule

Both partners should upload the **same result files, source files, and screenshots** to their own Git repositories. You may work together and share the same evidence, but each student must still submit it inside their own `os-class-activities-<YourStudentID>/activity4/` folder.

### Submission Folder Structure

```
os-se-<YourStudentID>/
└── os-class-activities-<YourStudentID>/
    └── activity4/
        ├── README.md
        ├── shared_score.txt
        ├── screenshots/
        │   ├── cpp_before_mutex.png
        │   ├── cpp_after_mutex.png
        │   ├── java_before_synchronized.png
        │   └── java_after_synchronized.png
        ├── cpp_before/
        │   ├── server_no_mutex.cpp
        │   └── client.cpp
        ├── cpp_after/
        │   ├── server_mutex.cpp
        │   └── client.cpp
        ├── java_before/
        │   ├── ScoreServerNoSync.java
        │   └── ScoreClient.java
        └── java_after/
            ├── ScoreServerSync.java
            └── ScoreClient.java
```

### README Template

````markdown
# Class Activity 4 — Shared File API

- **Student Name:** [Your Name]
- **Student ID:** [Your ID]
- **Partner Name:** [Partner Name]
- **Partner Student ID:** [Partner ID]
- **Server Machine Owner:** [Your Name or Partner Name]
- **Server IP Address:** [Example: 192.168.1.25]

---

## Task 1: C++ Before Mutex

![C++ before mutex](screenshots/cpp_before_mutex.png)

- Expected score after 20 total client requests:
- Actual score:
- What happened:

---

## Task 2: C++ After Mutex

![C++ after mutex](screenshots/cpp_after_mutex.png)

- Expected score after 20 total client requests:
- Actual score:
- What changed after adding mutex:

---

## Task 3: Java Before Synchronized

![Java before synchronized](screenshots/java_before_synchronized.png)

- Expected score after 20 total client requests:
- Actual score:
- What happened:

---

## Task 4: Java After Synchronized

![Java after synchronized](screenshots/java_after_synchronized.png)

- Expected score after 20 total client requests:
- Actual score:
- What changed after adding synchronized:

---

## Questions

1. Why should clients send requests to the server instead of writing the file directly?
2. Why does the server still have a race condition before mutex or synchronized?
3. In the C++ fixed version, what does `std::lock_guard<std::mutex>` protect?
4. In the Java fixed version, what does `synchronized` protect?
5. Why is the final score expected to be 20 when Student A sends 10 requests and Student B sends 10 requests?
6. What could happen if two separate servers update the same file at the same time?

---

## Reflection

_Compare the C++ and Java synchronization approaches. What did this activity teach you about protecting shared resources?_
````

---

## Grading Criteria

| Criteria | Points | Description |
|----------|--------|-------------|
| **C++ Before Mutex** | 20 | Server/client compile and run. Screenshot shows race condition or explains observed result. |
| **C++ After Mutex** | 20 | Server/client compile and run. Mutex protects file update and final score is correct. |
| **Java Before Synchronized** | 20 | Server/client compile and run. Screenshot shows race condition or explains observed result. |
| **Java After Synchronized** | 20 | Server/client compile and run. `synchronized` protects file update and final score is correct. |
| **README + Questions** | 20 | Screenshots embedded, answers are clear, and reflection compares C++ and Java. |
| **Total** | **100** | |

---

## Tips

- Always reset the file before each test:

```bash
$ echo 0 > shared_score.txt
```

- Stop a server with `Ctrl+C` before starting another server on the same port.
- If a port is already used, change the port number in both the server and client.
- If the unsafe version accidentally gives `20`, run it again. Race conditions depend on timing.
- The server is the only program that should update `shared_score.txt`.
