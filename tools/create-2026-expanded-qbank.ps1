param(
    [string]$OutputFile = "moodle-qbanks\questions-2026-se-os-expanded-midterm-pool.xml"
)

function E($value) {
    return [System.Security.SecurityElement]::Escape([string]$value)
}

$categories = @(
    @{
        Path = '$course$/top/2026-se-os/2026-se-os-Midterm Updated Pool/2026-se-os-lecture1-os-foundations'
        Questions = @(
            @('L1-NEW-Q01','A user program tries to access hardware directly. Which OS protection idea prevents this?','Dual-mode operation','File compression','Message queue priority','Thread pooling'),
            @('L1-NEW-Q02','Why does an interrupt improve I/O efficiency compared with constant polling?','The CPU can do other work until the device signals completion','It disables the kernel during I/O','It removes the need for device controllers','It stores all data permanently in cache'),
            @('L1-NEW-Q03','During boot, what is the first major purpose of the bootstrap program?','Load the operating system kernel into memory','Run every user application','Delete old temporary files','Start all network clients'),
            @('L1-NEW-Q04','Which component is the core part of the OS that runs with privileged control?','Kernel','Shell script','User application','Compiler'),
            @('L1-NEW-Q05','A disk controller transfers a block directly into memory with little CPU involvement. What mechanism is this?','DMA','Trap','Spooling','Context switching'),
            @('L1-NEW-Q06','Which storage is usually fastest but smallest?','CPU registers','Hard disk','Optical disk','Cloud archive'),
            @('L1-NEW-Q07','What happens when a hardware interrupt occurs?','The CPU pauses the current task and jumps to an interrupt handler','The process is permanently deleted','All processes enter kernel mode forever','The bootloader restarts the machine'),
            @('L1-NEW-Q08','Why is user mode important?','It limits what normal programs can do to protect the system','It makes every instruction faster','It allows programs to bypass the OS','It disables system calls'),
            @('L1-NEW-Q09','What does multiprogramming try to improve?','CPU utilization by keeping several jobs in memory','Disk size by compressing files','Monitor brightness automatically','Compiler warning messages'),
            @('L1-NEW-Q10','A software interrupt caused by a program requesting OS service is commonly called what?','Trap','DMA','Cache hit','Bootstrap')
        )
    },
    @{
        Path = '$course$/top/2026-se-os/2026-se-os-Midterm Updated Pool/2026-se-os-lecture2-activity1-system-calls'
        Questions = @(
            @('L2-A1-NEW-Q01','In Activity 1, replacing printf() with write() demonstrates what idea?','Library functions often use system calls underneath','System calls are only for Windows','The shell cannot run C programs','The kernel is the same as GCC'),
            @('L2-A1-NEW-Q02','Which POSIX call opens or creates a file and returns a file descriptor?','open()','printf()','malloc()','pthread_create()'),
            @('L2-A1-NEW-Q03','What does file descriptor 1 usually represent in Linux?','Standard output','Standard input','Standard error only','The boot partition'),
            @('L2-A1-NEW-Q04','Why must a program call close() after using a file descriptor?','To release the kernel resource associated with the open file','To compile the program','To increase file permissions','To create a child process'),
            @('L2-A1-NEW-Q05','What does strace help students observe?','The system calls made by a running program','Only Java bytecode instructions','Only hidden files in a directory','The physical memory chips'),
            @('L2-A1-NEW-Q06','What is the main difference between a system call and a normal function call?','A system call crosses from user mode into kernel service code','A system call never returns','A function call always creates a process','A function call requires root permission'),
            @('L2-A1-NEW-Q07','Which Linux virtual filesystem exposes kernel and process information used in Activity 1?','/proc','/home','/tmp','/boot/efi'),
            @('L2-A1-NEW-Q08','The shell is best described as what?','A command interpreter between the user and OS services','The CPU scheduler itself','A hardware interrupt line','A shared library file only'),
            @('L2-A1-NEW-Q09','Which OS structure keeps many services in user space to reduce kernel size?','Microkernel','Monolithic-only kernel','Flat file system','Ready queue'),
            @('L2-A1-NEW-Q10','What does the mode argument 0644 commonly mean when creating a file?','Owner read/write, group read, others read','Everyone execute only','Owner no access, others full access','Kernel mode only')
        )
    },
    @{
        Path = '$course$/top/2026-se-os/2026-se-os-Midterm Updated Pool/2026-se-os-lecture3-activity2-processes-ipc'
        Questions = @(
            @('L3-A2-NEW-Q01','In Activity 2, what does fork() create?','A child process that is a copy of the parent at that moment','A new kernel module','A new file descriptor only','A Java thread pool'),
            @('L3-A2-NEW-Q02','What does exec() do after a successful fork?','Replaces the current process image with another program','Duplicates the parent again','Deletes the process table','Creates shared memory automatically'),
            @('L3-A2-NEW-Q03','Why does the parent often call waitpid()?','To wait for and collect the child process exit status','To start the bootloader','To map shared memory','To convert byte order'),
            @('L3-A2-NEW-Q04','What is a zombie process?','A terminated child whose parent has not collected its exit status','A process waiting for keyboard input','A process adopted after its parent exits','A thread that owns a mutex'),
            @('L3-A2-NEW-Q05','What is an orphan process?','A child process whose parent has terminated first','A child whose parent called wait() immediately','A process with no code section','A process that cannot receive signals'),
            @('L3-A2-NEW-Q06','Shared memory IPC is fast mainly because processes can do what?','Access a common mapped memory region directly','Send every byte through the shell','Avoid all synchronization needs','Run only in kernel mode'),
            @('L3-A2-NEW-Q07','Message queues differ from shared memory because they use what communication style?','Send and receive discrete messages managed by the OS','Direct pointer access to another process stack','Only file rename operations','Only hardware interrupts'),
            @('L3-A2-NEW-Q08','Which structure stores a process state, program counter, registers, and scheduling information?','PCB','GRUB menu','Shell alias','Shared object table only'),
            @('L3-A2-NEW-Q09','Which process state means the process is able to run but not currently on the CPU?','Ready','Waiting','Terminated','Newly compiled'),
            @('L3-A2-NEW-Q10','Why are processes isolated from each other by default?','To protect memory and resources between programs','To make IPC impossible','To force all programs to share one stack','To remove the need for scheduling')
        )
    },
    @{
        Path = '$course$/top/2026-se-os/2026-se-os-Midterm Updated Pool/2026-se-os-lecture4-activity3-threads-sockets'
        Questions = @(
            @('L4-A3-NEW-Q01','In Activity 3, a TCP server normally calls which sequence before accepting clients?','socket(), bind(), listen(), accept()','fork(), wait(), exec(), close()','open(), read(), write(), unlink()','sort(), uniq(), wc(), grep()'),
            @('L4-A3-NEW-Q02','Why does the client usually call connect() instead of bind() in the simple TCP activity?','It initiates a connection to the server address and port','It creates a new kernel thread','It waits for all child processes','It formats an access log'),
            @('L4-A3-NEW-Q03','What is a thread?','A unit of execution inside a process sharing that process resources','A separate bootloader partition','A file descriptor for stdin','A type of hard link'),
            @('L4-A3-NEW-Q04','What do threads in the same process typically share?','Code, data, heap, and open files','Each thread has a separate address space','Only its own process ID','Nothing at all'),
            @('L4-A3-NEW-Q05','What is private to each thread?','Its stack and register state','The whole heap','All open files','The process code section'),
            @('L4-A3-NEW-Q06','Why did Activity 3 use pthread_mutex_lock() around a shared counter?','To prevent a race condition on shared data','To create a new TCP port','To delete a zombie process','To load a shared library'),
            @('L4-A3-NEW-Q07','What does pthread_join() do?','Waits for a thread to finish','Starts a server listening socket','Creates a new process image','Lists kernel modules'),
            @('L4-A3-NEW-Q08','Which Java approach separates the task from the thread object?','Implementing Runnable','Calling fork()','Using chmod','Creating a hard link'),
            @('L4-A3-NEW-Q09','A thread pool is useful because it does what?','Reuses a limited number of worker threads for many tasks','Guarantees no code ever blocks','Deletes unused processes from disk','Replaces all system calls'),
            @('L4-A3-NEW-Q10','In Linux ps output, LWP is commonly used to refer to what?','A schedulable thread/lightweight process ID','A file extension','A bootloader variable','A network port state')
        )
    },
    @{
        Path = '$course$/top/2026-se-os/2026-se-os-Lab Updated Pool/2026-se-os-lab1-os-linux-basics'
        Questions = @(
            @('LAB1-NEW-Q01','Which command records kernel and system information in Lab 1?','uname -a','mkdir -p','apt-get purge','cat /etc/passwd'),
            @('LAB1-NEW-Q02','What does lsb_release -a show?','Linux distribution information','Running background jobs only','File permissions only','CPU cache lines only'),
            @('LAB1-NEW-Q03','What does > do in a command such as uname -a > info.txt?','Redirects output and overwrites the target file','Appends output without overwriting','Runs the command in background','Creates a hard link'),
            @('LAB1-NEW-Q04','What is the difference between apt-get remove and apt-get purge?','purge also removes package configuration files','remove deletes the kernel','purge only updates package lists','They are exactly identical'),
            @('LAB1-NEW-Q05','In sleep 120 &, what does & do?','Runs the command in the background','Redirects errors','Creates a directory','Shows hidden files'),
            @('LAB1-NEW-Q06','Which command shows currently running processes in the basic Lab 1 task?','ps','touch','mv','tree'),
            @('LAB1-NEW-Q07','Which command can detect whether the OS is running in a virtualized environment?','systemd-detect-virt','echo','cp','mkdir'),
            @('LAB1-NEW-Q08','What is the purpose of which htop tmux?','Show the path of installed commands if found','Install both packages','Remove both packages','Start a web server'),
            @('LAB1-NEW-Q09','Why does Lab 1 compare a program with a running process?','To show that a program becomes a process when executed','To prove files cannot be copied','To disable multitasking','To replace the shell'),
            @('LAB1-NEW-Q10','What does python3 -m http.server 8080 start in Lab 1?','A simple web server process on port 8080','A compiler','A package manager','A bootloader menu')
        )
    },
    @{
        Path = '$course$/top/2026-se-os/2026-se-os-Lab Updated Pool/2026-se-os-lab2-navigation-files'
        Questions = @(
            @('LAB2-NEW-Q01','What does pwd display?','The current working directory','All package updates','The kernel version only','A process tree only'),
            @('LAB2-NEW-Q02','Which command lists hidden files in long format?','ls -la','ls -R only','cd ..','rm -r'),
            @('LAB2-NEW-Q03','What does cd .. do?','Moves to the parent directory','Moves to root always','Deletes the current folder','Copies files recursively'),
            @('LAB2-NEW-Q04','Which path is absolute?','/home/user/docs','../docs','docs/report.txt','./script.sh'),
            @('LAB2-NEW-Q05','Why use mkdir -p?','To create nested directories without failing if parents are missing','To print the current directory','To purge a package','To view process status'),
            @('LAB2-NEW-Q06','Which command copies a file?','cp source.txt backup.txt','mv source.txt backup.txt','rm source.txt','cd source.txt'),
            @('LAB2-NEW-Q07','Which command renames or moves a file?','mv','cp','pwd','cat'),
            @('LAB2-NEW-Q08','What does rm remove by default?','Files','The current user account','The kernel','The shell history only'),
            @('LAB2-NEW-Q09','Which command shows a recursive directory tree if installed?','tree','touch','grep','wait'),
            @('LAB2-NEW-Q10','What does cd - do?','Returns to the previous directory','Moves to the root directory','Deletes a directory','Shows file size sorted output')
        )
    },
    @{
        Path = '$course$/top/2026-se-os/2026-se-os-Lab Updated Pool/2026-se-os-lab3-wildcards-links-grub-libraries'
        Questions = @(
            @('LAB3-NEW-Q01','Which wildcard matches zero or more characters?','*','?','[]','{} only'),
            @('LAB3-NEW-Q02','Which wildcard matches exactly one character?','?','*','..','|'),
            @('LAB3-NEW-Q03','What does ln target hardlink create by default?','A hard link','A symbolic link','A process','A pipe'),
            @('LAB3-NEW-Q04','What does ln -s target shortcut create?','A symbolic link','A hard link only','A shared memory object','A boot entry'),
            @('LAB3-NEW-Q05','What happens to a symbolic link if its target is removed?','It becomes a broken link','It becomes a hard link','It turns into a directory','It repairs the target automatically'),
            @('LAB3-NEW-Q06','What is GRUB responsible for?','Loading and starting the operating system boot process','Counting lines in a file','Creating POSIX threads','Managing message queues'),
            @('LAB3-NEW-Q07','Which command is commonly used to inspect shared library dependencies of an executable?','ldd','pwd','jobs','mkdir'),
            @('LAB3-NEW-Q08','What file extension commonly identifies Linux shared objects?','.so','.exe','.txt','.md'),
            @('LAB3-NEW-Q09','Why is -fPIC used when compiling a shared library?','To create position-independent code suitable for shared objects','To force a process to fork','To format a disk partition','To find hidden files'),
            @('LAB3-NEW-Q10','What does ldconfig do after installing a shared library?','Updates the dynamic linker cache','Deletes all shared libraries','Starts GRUB recovery mode','Converts source code to Java bytecode')
        )
    },
    @{
        Path = '$course$/top/2026-se-os/2026-se-os-Lab Updated Pool/2026-se-os-lab4-redirection-pipelines-processes'
        Questions = @(
            @('LAB4-NEW-Q01','What does >> do?','Appends standard output to a file','Overwrites standard error only','Runs a command in foreground','Creates a symbolic link'),
            @('LAB4-NEW-Q02','What does 2> redirect?','Standard error','Standard input','Only successful output','The process ID'),
            @('LAB4-NEW-Q03','What does a pipe | do?','Sends stdout of one command into stdin of another','Deletes a file','Creates a child process','Starts GRUB'),
            @('LAB4-NEW-Q04','Which command counts lines, words, or bytes?','wc','grep','kill','nohup'),
            @('LAB4-NEW-Q05','Which command filters lines matching a pattern?','grep','cut','cd','touch'),
            @('LAB4-NEW-Q06','Which command extracts fields from delimited text?','cut','ps','top','bg'),
            @('LAB4-NEW-Q07','Why are top and htop documented with screenshots in Lab 4?','They are interactive tools that continuously refresh','They cannot show processes','They only work in Windows','They are shell redirection operators'),
            @('LAB4-NEW-Q08','Which signal cannot be caught or ignored by a process?','SIGKILL','SIGTERM','SIGCONT','SIGHUP'),
            @('LAB4-NEW-Q09','What does bg do for a stopped job?','Resumes it in the background','Deletes it','Moves it to a directory','Shows only hidden files'),
            @('LAB4-NEW-Q10','Why can a zombie process not be killed with kill -9?','It is already terminated and only its process table entry remains','It is protected by chmod','It is running in Java only','It is a symbolic link')
        )
    }
)

$xmlParts = @('<?xml version="1.0" encoding="UTF-8"?>', '<quiz>')
$questionId = 2026000

foreach ($category in $categories) {
    $questionId++
    $xmlParts += "  <!-- question: $questionId category -->"
    $xmlParts += '  <question type="category">'
    $xmlParts += '    <category>'
    $xmlParts += "      <text>$(E $category.Path)</text>"
    $xmlParts += '    </category>'
    $xmlParts += '    <info format="html"><text></text></info>'
    $xmlParts += '    <idnumber></idnumber>'
    $xmlParts += '  </question>'

    foreach ($q in $category.Questions) {
        $questionId++
        $name = $q[0]
        $prompt = $q[1]
        $correct = $q[2]
        $distractors = $q[3..5]

        $xmlParts += "  <!-- question: $questionId -->"
        $xmlParts += '  <question type="multichoice">'
        $xmlParts += "    <name><text>$(E $name)</text></name>"
        $xmlParts += "    <questiontext format=`"html`"><text><![CDATA[<p>$(E $prompt)</p>]]></text></questiontext>"
        $xmlParts += '    <generalfeedback format="html"><text></text></generalfeedback>'
        $xmlParts += '    <defaultgrade>1.0000000</defaultgrade>'
        $xmlParts += '    <penalty>0.3333333</penalty>'
        $xmlParts += '    <hidden>0</hidden>'
        $xmlParts += '    <idnumber></idnumber>'
        $xmlParts += '    <single>true</single>'
        $xmlParts += '    <shuffleanswers>true</shuffleanswers>'
        $xmlParts += '    <answernumbering>abc</answernumbering>'
        $xmlParts += '    <showstandardinstruction>0</showstandardinstruction>'
        $xmlParts += '    <correctfeedback format="html"><text><![CDATA[<p>Correct.</p>]]></text></correctfeedback>'
        $xmlParts += '    <partiallycorrectfeedback format="html"><text></text></partiallycorrectfeedback>'
        $xmlParts += '    <incorrectfeedback format="html"><text><![CDATA[<p>Review the related lecture/activity/lab concept.</p>]]></text></incorrectfeedback>'
        $xmlParts += "    <answer fraction=`"100`" format=`"html`"><text><![CDATA[<p>$(E $correct)</p>]]></text><feedback format=`"html`"><text></text></feedback></answer>"
        foreach ($answer in $distractors) {
            $xmlParts += "    <answer fraction=`"0`" format=`"html`"><text><![CDATA[<p>$(E $answer)</p>]]></text><feedback format=`"html`"><text></text></feedback></answer>"
        }
        $xmlParts += '  </question>'
    }
}

$xmlParts += '</quiz>'

$outputPath = Join-Path (Get-Location) $OutputFile
Set-Content -LiteralPath $outputPath -Value ($xmlParts -join "`r`n") -Encoding UTF8
Write-Output "Wrote $outputPath"
Write-Output "Categories: $($categories.Count)"
Write-Output "Questions: $($categories.Count * 10)"
