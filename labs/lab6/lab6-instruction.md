# OS Lab 6 — Linux Security, Users, Groups & File Permissions (Hands-on)

| | |
|---|---|
| **Course** | Operating Systems |
| **Lab Title** | Linux Security: Users, Groups & File Permissions |
| **Chapter** | File Systems, OS Security & Access Control |
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
> 4. **Quick Reference Tables** — Command cheat sheets
> 5. **Tasks 1–5 (Required)** — User management, groups, permissions, special bits, ACLs
> 6. **Deliverables & Submission** — Folder structure, README template, git push
> 7. **Screenshot Checklist** — Every screenshot you need, in one place

---

## Lab Objectives

After completing this lab, students will be able to:

1. Create, modify, and delete Linux user accounts using `useradd`, `usermod`, and `userdel`.
2. Create and manage user groups using `groupadd`, `groupmod`, and `gpasswd`.
3. Interpret and modify file and directory permissions using `chmod` (symbolic and octal notation).
4. Change file ownership using `chown` and `chgrp`.
5. Understand and apply special permission bits: `setuid`, `setgid`, and the sticky bit.
6. Use `sudo` for privilege escalation and audit the sudoers configuration safely.
7. Apply Access Control Lists (ACLs) with `getfacl` and `setfacl` for fine-grained permission control.

> **Scenario:** You are **Alex**, a junior systems engineer at **TechCorp Inc.** Your manager says: *"We're onboarding a new project team. I need you to set up user accounts and groups, lock down sensitive directories, and make sure that no one can accidentally delete each other's files. Security is our top priority — get it right."*

---

## Task Overview

| Task | Title | Key Commands | Screenshots Required |
|:---:|-------|-------------|:-----------:|
| **1** | User Account Management | `useradd`, `passwd`, `usermod`, `userdel` | ✅ (User creation & verification) |
| **2** | Group Management | `groupadd`, `gpasswd`, `id`, `groups` | ✅ (Group setup & membership) |
| **3** | File & Directory Permissions | `chmod`, `chown`, `chgrp`, `ls -l` | ✅ (Permission changes) |
| **4** | Special Permission Bits | `setuid`, `setgid`, sticky bit | ✅ (Special bits in action) |
| **5** | Access Control Lists (ACLs) | `getfacl`, `setfacl` | ✅ (ACL configuration) |

---

## Lab Setup

Navigate into your existing lab submission repository and create the `lab6` directory:

```bash
$ cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>
$ mkdir lab6
$ cd lab6
```

### Documenting Your Work

1. **Screenshots:** All tasks require screenshots as proof of execution.
2. **Save All Images:** Save all screenshots to an `images/` folder inside your `lab6` directory.
3. **Output Files:** Redirect command outputs into `.txt` files as directed in each task.

---

## Quick Reference

### User & Group Management

| Command | Purpose |
|---------|---------|
| `useradd -m -s /bin/bash <name>` | Create a user with home directory and bash shell |
| `passwd <name>` | Set or change a user's password |
| `usermod -aG <group> <user>` | Add a user to a supplementary group |
| `usermod -l <newname> <oldname>` | Rename a user account |
| `userdel -r <name>` | Delete a user and their home directory |
| `groupadd <group>` | Create a new group |
| `groupmod -n <newname> <oldname>` | Rename a group |
| `gpasswd -d <user> <group>` | Remove a user from a group |
| `id <user>` | Show UID, GID, and supplementary groups |
| `groups <user>` | List all groups a user belongs to |

### Permission & Ownership

| Command | Purpose |
|---------|---------|
| `ls -l` | Long listing showing permissions, owner, group |
| `chmod 755 <file>` | Set permissions using octal notation |
| `chmod u+x <file>` | Add execute for owner (symbolic) |
| `chown user:group <file>` | Change owner and group |
| `chgrp <group> <file>` | Change group only |
| `umask` | Show/set default permission mask |

### Special Bits

| Bit | Octal | Effect on File | Effect on Directory |
|-----|-------|---------------|---------------------|
| `setuid` | `4xxx` | Run as file owner | — |
| `setgid` | `2xxx` | Run as file group | New files inherit group |
| Sticky | `1xxx` | — | Only owner can delete own files |

### Key Files

| File | Purpose |
|------|---------|
| `/etc/passwd` | User account database |
| `/etc/shadow` | Hashed passwords (root-readable only) |
| `/etc/group` | Group database |
| `/etc/sudoers` | Sudo privilege configuration (edit with `visudo`) |

---

## Task 1 — User Account Management

**Scenario:** *"We have two new engineers joining the project: `dev_alice` and `dev_bob`. Create their accounts, set passwords, and verify the accounts are properly configured."*

**Instructions:**

1. Set up your working directory:
   ```bash
   $ mkdir -p security_lab
   $ cd security_lab
   ```

2. Create two new user accounts:
   ```bash
   $ sudo useradd -m -s /bin/bash dev_alice
   $ sudo useradd -m -s /bin/bash dev_bob
   ```

3. Set passwords for both users:
   ```bash
   $ sudo passwd dev_alice
   $ sudo passwd dev_bob
   ```
   > Use a simple password like `Password123` for this lab exercise.

4. Verify the accounts were created — check the `/etc/passwd` entries:
   ```bash
   $ grep "dev_alice\|dev_bob" /etc/passwd
   ```

5. Verify the home directories exist:
   ```bash
   $ ls -la /home/ | grep "dev_alice\|dev_bob"
   ```

6. Redirect the verification output to a file:
   ```bash
   $ grep "dev_alice\|dev_bob" /etc/passwd > task1_users.txt
   $ ls -la /home/ >> task1_users.txt
   $ cat task1_users.txt
   ```

   > 📸 **Required Screenshot 1:** Take a screenshot showing the output of `cat task1_users.txt`. Save as `task1_user_creation.png`.

7. Modify `dev_alice` — add a comment (GECOS) field with her full name:
   ```bash
   $ sudo usermod -c "Alice Developer" dev_alice
   $ grep dev_alice /etc/passwd
   ```

   > 📸 **Required Screenshot 2:** Take a screenshot showing the updated `/etc/passwd` entry for `dev_alice`. Save as `task1_user_modify.png`.

8. Return to `lab6`:
   ```bash
   $ cd ..
   ```

---

## Task 2 — Group Management

**Scenario:** *"The two new engineers belong to the `devteam` group. Create it, add them both, and then verify the memberships."*

**Instructions:**

1. Create a new group called `devteam`:
   ```bash
   $ sudo groupadd devteam
   ```

2. Add both users to the group:
   ```bash
   $ sudo usermod -aG devteam dev_alice
   $ sudo usermod -aG devteam dev_bob
   ```

3. Verify group membership using two different methods:
   ```bash
   $ groups dev_alice
   $ id dev_bob
   ```

4. Inspect the `/etc/group` file entry:
   ```bash
   $ grep devteam /etc/group
   ```

5. Save the output:
   ```bash
   $ groups dev_alice > task2_groups.txt
   $ id dev_bob >> task2_groups.txt
   $ grep devteam /etc/group >> task2_groups.txt
   $ cat task2_groups.txt
   ```

   > 📸 **Required Screenshot 3:** Take a screenshot of `cat task2_groups.txt`. Save as `task2_group_setup.png`.

6. Create an additional group called `auditors` and add only `dev_alice`:
   ```bash
   $ sudo groupadd auditors
   $ sudo usermod -aG auditors dev_alice
   $ id dev_alice
   ```

   > 📸 **Required Screenshot 4:** Take a screenshot of the `id dev_alice` output showing both `devteam` and `auditors` memberships. Save as `task2_multi_group.png`.

---

## Task 3 — File & Directory Permissions

**Scenario:** *"Create a shared project directory for the `devteam` group. Set up permissions so that only team members can read and write files, but others cannot access the folder at all."*

**Instructions:**

1. Create a shared project directory:
   ```bash
   $ sudo mkdir -p /opt/techcorp/devproject
   ```

2. Set the group owner to `devteam`:
   ```bash
   $ sudo chown root:devteam /opt/techcorp/devproject
   ```

3. Set permissions — owner full, group read/write/execute, others none:
   ```bash
   $ sudo chmod 770 /opt/techcorp/devproject
   $ ls -ld /opt/techcorp/devproject
   ```

4. Create a test file inside the directory:
   ```bash
   $ sudo touch /opt/techcorp/devproject/project_notes.txt
   $ sudo chown dev_alice:devteam /opt/techcorp/devproject/project_notes.txt
   $ sudo chmod 664 /opt/techcorp/devproject/project_notes.txt
   ```

5. Show the full permission listing:
   ```bash
   $ ls -l /opt/techcorp/devproject/
   ```

6. Save the output:
   ```bash
   $ ls -ld /opt/techcorp/devproject > task3_permissions.txt
   $ ls -l /opt/techcorp/devproject/ >> task3_permissions.txt
   $ cat task3_permissions.txt
   ```

   > 📸 **Required Screenshot 5:** Take a screenshot of `cat task3_permissions.txt`. Save as `task3_dir_permissions.png`.

7. Test access control — attempt to read the file as a user **not** in `devteam`:
   ```bash
   $ sudo useradd -m -s /bin/bash temp_user
   $ sudo su - temp_user -c "cat /opt/techcorp/devproject/project_notes.txt"
   ```
   > **Expected:** `Permission denied` — because `temp_user` is not in `devteam`.

   > 📸 **Required Screenshot 6:** Take a screenshot showing the `Permission denied` error. Save as `task3_access_denied.png`.

8. Create a personal report of the permission change workflow:
   ```bash
   $ stat /opt/techcorp/devproject > task3_stat_output.txt
   $ cat task3_stat_output.txt
   ```

---

## Task 4 — Special Permission Bits

**Scenario:** *"Now configure the shared directory so that new files automatically inherit the group ownership (`setgid`), and no one can delete another user's files from the directory (sticky bit)."*

**Instructions:**

1. Apply the `setgid` bit to the shared directory:
   ```bash
   $ sudo chmod g+s /opt/techcorp/devproject
   $ ls -ld /opt/techcorp/devproject
   ```
   > **Observe:** The group execute bit changes from `x` to `s`, indicating setgid is active.

2. Test `setgid` — switch to `dev_bob` and create a file:
   ```bash
   $ sudo su - dev_bob -c "touch /opt/techcorp/devproject/bob_file.txt"
   $ ls -l /opt/techcorp/devproject/
   ```
   > **Observe:** `bob_file.txt` should be owned by `dev_bob` but have `devteam` as the group — inherited from the directory.

   > 📸 **Required Screenshot 7:** Take a screenshot showing the setgid directory listing and `bob_file.txt` with `devteam` group. Save as `task4_setgid.png`.

3. Apply the **sticky bit** to the directory:
   ```bash
   $ sudo chmod +t /opt/techcorp/devproject
   $ ls -ld /opt/techcorp/devproject
   ```
   > **Observe:** The others execute bit shows `t`, indicating the sticky bit is set.

4. Test the sticky bit — `dev_bob` should NOT be able to delete `dev_alice`'s file:
   ```bash
   $ sudo su - dev_bob -c "rm /opt/techcorp/devproject/project_notes.txt"
   ```
   > **Expected:** `Operation not permitted` — because `project_notes.txt` belongs to `dev_alice`.

   > 📸 **Required Screenshot 8:** Take a screenshot showing both the sticky bit in `ls -ld` and the `Operation not permitted` error. Save as `task4_sticky_bit.png`.

5. Demonstrate `setuid` on an executable — create a simple C program:
   ```bash
   $ cd security_lab
   ```

   Create `whoami_suid.c`:
   ```c
   #include <stdio.h>
   #include <unistd.h>

   int main() {
       printf("Real UID:      %d\n", getuid());
       printf("Effective UID: %d\n", geteuid());
       printf("Running as:    ");
       fflush(stdout);
       execlp("whoami", "whoami", NULL);
       return 0;
   }
   ```

6. Compile, set ownership, and apply setuid:
   ```bash
   $ gcc -o whoami_suid whoami_suid.c
   $ sudo chown root:root whoami_suid
   $ sudo chmod u+s whoami_suid
   $ ls -l whoami_suid
   ```
   > **Observe:** The owner execute bit shows `s` (setuid active).

7. Run the program as `dev_alice`:
   ```bash
   $ sudo su - dev_alice -c "/home/$(whoami)/os-lab-<YourStudentID>/lab6/security_lab/whoami_suid"
   ```
   > **Note:** Adjust the path to match your actual lab directory. The effective UID will be `0` (root), while the real UID is `dev_alice`'s UID.

   > 📸 **Required Screenshot 9:** Take a screenshot showing `ls -l whoami_suid` with the setuid bit and the program's UID output. Save as `task4_setuid.png`.

8. Save a summary:
   ```bash
   $ ls -ld /opt/techcorp/devproject > task4_special_bits.txt
   $ ls -l whoami_suid >> task4_special_bits.txt
   $ cat task4_special_bits.txt
   ```

---

## Task 5 — Access Control Lists (ACLs)

**Scenario:** *"The `auditors` group needs read-only access to the project directory — but we cannot change the primary group of the directory. Use ACLs to grant fine-grained access without modifying standard permissions."*

**Instructions:**

1. Check if ACL support is available:
   ```bash
   $ getfacl /opt/techcorp/devproject
   ```

2. Grant the `auditors` group read and execute (traverse) access via ACL:
   ```bash
   $ sudo setfacl -m g:auditors:rx /opt/techcorp/devproject
   $ sudo setfacl -m g:auditors:r /opt/techcorp/devproject/project_notes.txt
   ```

3. View the resulting ACL:
   ```bash
   $ getfacl /opt/techcorp/devproject
   $ getfacl /opt/techcorp/devproject/project_notes.txt
   ```
   > **Observe:** You will see a `group:auditors:r-x` ACE (Access Control Entry) in addition to the standard entries.

   > 📸 **Required Screenshot 10:** Take a screenshot of `getfacl /opt/techcorp/devproject`. Save as `task5_acl_dir.png`.

4. Test ACL access — `dev_alice` is in `auditors` and should now be able to read the file:
   ```bash
   $ sudo su - dev_alice -c "cat /opt/techcorp/devproject/project_notes.txt"
   ```
   > **Expected:** Command succeeds (file may be empty, but no permission error).

5. Verify `temp_user` (not in `auditors`) still cannot access the directory:
   ```bash
   $ sudo su - temp_user -c "ls /opt/techcorp/devproject"
   ```
   > **Expected:** `Permission denied`.

   > 📸 **Required Screenshot 11:** Take a screenshot showing `dev_alice` succeeding and `temp_user` being denied. Save as `task5_acl_test.png`.

6. Save the ACL output to a file:
   ```bash
   $ getfacl /opt/techcorp/devproject > task5_acl.txt
   $ getfacl /opt/techcorp/devproject/project_notes.txt >> task5_acl.txt
   $ cat task5_acl.txt
   ```

   > 📸 **Required Screenshot 12:** Take a screenshot of `cat task5_acl.txt`. Save as `task5_acl_output.png`.

7. Clean up the ACL entry:
   ```bash
   $ sudo setfacl -x g:auditors /opt/techcorp/devproject
   $ getfacl /opt/techcorp/devproject
   ```

---

## Challenge — Secure Shared Drop-Box

> ⭐ **Bonus Challenge (10 extra points)**

**Scenario:** *"Create a `/opt/techcorp/dropbox` directory that behaves like a shared drop-box: any user can create files inside, but no user can read or delete another user's files. Apply setgid so all files belong to `devteam`, and the sticky bit so only owners can delete their own files."*

**Requirements:**

1. Create `/opt/techcorp/dropbox` with `devteam` as the group owner.
2. Set permissions so all `devteam` members can write into it, but cannot read or delete others' files.
3. Apply both `setgid` and the sticky bit in a single `chmod` call.
4. Test by:
   - Switching to `dev_alice` and creating a file.
   - Switching to `dev_bob` and attempting to delete `dev_alice`'s file (should fail).
   - Verifying `dev_bob` can create his own file.
5. Document with screenshots and redirect output to `challenge_dropbox.txt`.

> 📸 **Challenge Screenshot:** Show the final `ls -ld /opt/techcorp/dropbox` and the failed deletion attempt. Save as `challenge_dropbox.png`.

---

## Screenshot Checklist

Before submitting, verify you have **all** required screenshots:

| # | File Name | Task | What It Shows |
|:-:|-----------|:----:|---------------|
| 1 | `task1_user_creation.png` | Task 1 | Output of `cat task1_users.txt` |
| 2 | `task1_user_modify.png` | Task 1 | Updated `/etc/passwd` entry |
| 3 | `task2_group_setup.png` | Task 2 | `cat task2_groups.txt` output |
| 4 | `task2_multi_group.png` | Task 2 | `id dev_alice` with two groups |
| 5 | `task3_dir_permissions.png` | Task 3 | `cat task3_permissions.txt` |
| 6 | `task3_access_denied.png` | Task 3 | `Permission denied` error |
| 7 | `task4_setgid.png` | Task 4 | Directory listing with `s` bit |
| 8 | `task4_sticky_bit.png` | Task 4 | `t` bit in listing + deletion error |
| 9 | `task4_setuid.png` | Task 4 | `s` bit on binary + UID output |
| 10 | `task5_acl_dir.png` | Task 5 | `getfacl` directory output |
| 11 | `task5_acl_test.png` | Task 5 | Alice succeeds, temp_user denied |
| 12 | `task5_acl_output.png` | Task 5 | `cat task5_acl.txt` |

---

## Final Submission

### Required Folder Structure

```
os-se-<YourStudentID>/
└── os-lab-<YourStudentID>/
    └── lab6/
        ├── README.md                       ← Your documentation
        ├── task1_users.txt
        ├── task2_groups.txt
        ├── task3_permissions.txt
        ├── task3_stat_output.txt
        ├── task4_special_bits.txt
        ├── task5_acl.txt
        ├── security_lab/
        │   └── whoami_suid.c
        └── images/
            ├── task1_user_creation.png
            ├── task1_user_modify.png
            ├── task2_group_setup.png
            ├── task2_multi_group.png
            ├── task3_dir_permissions.png
            ├── task3_access_denied.png
            ├── task4_setgid.png
            ├── task4_sticky_bit.png
            ├── task4_setuid.png
            ├── task5_acl_dir.png
            ├── task5_acl_test.png
            └── task5_acl_output.png
```

### Git Push

```bash
$ cd ~/os-se-<YourStudentID>
$ git add .
$ git commit -m "Lab 6: Linux Security, Users, Groups & File Permissions"
$ git push origin main
```
