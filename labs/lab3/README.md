# OS Lab 3 Submission — Wildcards, Links, GRUB & Shared Libraries

- **Student Name:** [Your Name Here]
- **Student ID:** [Your Student ID Here]
- **Partner Name (Task 7):** [Partner Name Here]
- **Partner ID (Task 7):** [Partner Student ID Here]

---

## Task Output Files

During the lab, each task redirected its output into `.txt` files. These files are your primary proof of work for the **guided portions** of each task. Make sure all of the following files are present in your `lab3/` folder:

- [ ] `task1_wildcards.txt`
- [ ] `task2_links.txt`
- [ ] `task3_grub.txt`
- [ ] `task4_shared_objects.txt`
- [ ] `task5_boot_recovery.txt`
- [ ] `task6_grub_custom.txt`
- [ ] `task7_shared_library.txt`
- [ ] `task_history.txt`

---

## Screenshots

The screenshots below document the **Challenge sections**, **VM tasks**, **pair task**, and **command history**. The guided task outputs are already captured in the `.txt` files above.

---

### Screenshot 1 — Task 1 Challenge: Wildcards

Show the terminal where you ran your wildcard challenge commands **1a–1d** (listing files with `r*`, single-character match with `?`, brace expansion for `memo_` files, and removing `.log` files). This should show both the commands you typed and their output.

<!-- Insert your screenshot below: -->
![Task 1 Challenge](images/task1_challenge.png)

---

### Screenshot 2 — Task 2 Challenge: Links

Show the terminal where you ran your link challenge commands **2a–2c** (creating hard links to `shared_data.txt`, creating a symlink to a directory, and testing what happens when the original is deleted). Show the inode numbers and link counts.

<!-- Insert your screenshot below: -->
![Task 2 Challenge](images/task2_challenge.png)

---

### Screenshot 3 — Task 4 Challenge: Shared Objects

Show the terminal where you ran your shared objects challenge commands **4a–4d** (inspecting `ssh`/`curl` libraries, listing `libm*` files, following the `libc.so.6` symlink chain, and compiling/inspecting a test program). Show the `ldd` and `readlink` output.

<!-- Insert your screenshot below: -->
![Task 4 Challenge](images/task4_challenge.png)

---

### Screenshot 4 — Task 5 Step 1: VM Snapshot

Show your VM's snapshot panel confirming the "Before Boot Lab" snapshot was created.

<!-- Insert your screenshot below: -->
![Task 5 Step 1](images/task5_step1.png)

---

### Screenshot 5 — Task 5 Step 2: GRUB Menu

Show the GRUB boot menu with the available kernel entries and "Advanced options" visible.

<!-- Insert your screenshot below: -->
![Task 5 Step 2](images/task5_step2.png)

---

### Screenshot 6 — Task 5 Step 3: Recovery Mode

Show the Recovery Menu options and the root shell with the output of `whoami`, `mount | grep "on / "`, and `uname -r`.

<!-- Insert your screenshot below: -->
![Task 5 Step 3](images/task5_step3.png)

---

### Screenshot 7 — Task 5 Step 4: Broken GRUB

Show the `grub>` command line prompt that appears after the GRUB configuration was removed.

<!-- Insert your screenshot below: -->
![Task 5 Step 4](images/task5_step4.png)

---

### Screenshot 8 — Task 5 Step 5: Manual Boot

Show the manual GRUB commands you typed (`set root`, `linux`, `initrd`, `boot`) and the system beginning to start up.

<!-- Insert your screenshot below: -->
![Task 5 Step 5](images/task5_step5.png)

---

### Screenshot 9 — Task 5 Step 6: Restored GRUB

Show the output of `ls -la /boot/grub/grub.cfg` and `head -5 /boot/grub/grub.cfg` confirming the configuration was restored.

<!-- Insert your screenshot below: -->
![Task 5 Step 6](images/task5_step6.png)

---

### Screenshot 10 — Task 5 Step 7: Normal Boot

Show the system booted normally with the output of `uname -r` and `uptime`.

<!-- Insert your screenshot below: -->
![Task 5 Step 7](images/task5_step7.png)

---

### Screenshot 11 — Task 6 Step 1: GRUB Timeout Config

Show the modified `/etc/default/grub` with `GRUB_TIMEOUT=10` and the cleared `GRUB_CMDLINE_LINUX_DEFAULT`.

<!-- Insert your screenshot below: -->
![Task 6 Step 1](images/task6_step1.png)

---

### Screenshot 12 — Task 6 Step 2: Custom GRUB Entry

Show the GRUB menu displaying your custom "TechCorp Training VM — Boot Standard" entry.

<!-- Insert your screenshot below: -->
![Task 6 Step 2](images/task6_step2.png)

---

### Screenshot 13 — Task 6 Step 3: GRUB Background Image

Show the GRUB menu with your custom background image visible behind the menu text.

<!-- Insert your screenshot below: -->
![Task 6 Step 3](images/task6_step3.png)

---

### Screenshot 14 — Task 7: Shared Library (Pair Task)

Show the terminal with: (1) the `gcc` compilation of the shared library, (2) `ldconfig -p | grep techcorp` showing registration, (3) `ldd ./sysinfo_test` showing the library is resolved, and (4) the test program output displaying hostname, uptime, and CPU count.

<!-- Insert your screenshot below: -->
![Task 7 Pair](images/task7_pair.png)

---

### Screenshot 15 — Full Command History

Run the following command and take a screenshot:

```bash
history | tail -n 100
```

<!-- Insert your screenshot below: -->
![Full History](images/full_history.png)
