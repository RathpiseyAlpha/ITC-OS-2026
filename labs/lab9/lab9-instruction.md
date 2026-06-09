# OS Lab 9 - Virtual Vault Deadlock, Resource Ordering & Recovery (Hands-on)

| | |
|---|---|
| **Course** | Operating Systems |
| **Lab Title** | The Quantum Vault Deadlock |
| **Chapter** | File Systems, Process Synchronization, Deadlocks |
| **Duration** | 3 Hours |
| **Lab Type** | Individual, with paired cross-site testing |

---

**Source reference:** This canonical lab instruction was adapted from the original Quantum Vault Deadlock brief.

---

> **IMPORTANT - READ EVERYTHING FIRST**
>
> This lab uses files and folders in two places:
>
> 1. Your **submission folder** inside `~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9`
> 2. Your **working folders** outside the repo: `~/bin` and `~/os-lab-deadlock`
>
> The working folders are required because the scripts must be executable from your shell and the virtual vault images must be mounted from your home directory. Before submitting, you must copy evidence and scripts back into your `lab9` folder.
>
> **Document structure:**
> 1. **Lab Objectives** - What you will learn
> 2. **Mission Briefing** - Disaster recovery scenario
> 3. **Task Overview** - Summary of all levels
> 4. **Lab Setup** - Repository, working folders, and naming rules
> 5. **Quick Reference** - `dd`, `mkfs`, `udisksctl`, `flock`, process inspection
> 6. **Levels 1-7 (Required)** - Vault provisioning, local deadlock, cross-site deadlock, ordering, timeout recovery, teardown
> 7. **Deliverables & Submission** - Complete tree structure, README template, git push
> 8. **Screenshot Checklist** - Every screenshot you need, in one place

---

## Lab Objectives

After completing this lab, students will be able to:

1. Create virtual disk image files and format them as Linux file systems.
2. Mount loopback devices as a normal user using `udisksctl`.
3. Use `flock` to simulate exclusive resource access between concurrent Bash scripts.
4. Demonstrate a local deadlock caused by circular wait.
5. Demonstrate a partner-based cross-site deadlock using shared lock files.
6. Explain how global resource ordering prevents deadlock.
7. Use timeout-based lock acquisition to recover instead of waiting forever.
8. Safely unmount and detach loopback devices during teardown.

> **Scenario:** You are a disaster recovery engineer at **QuantumTech**. Two virtual vault drives, **Vault Alpha** and **Vault Beta**, store replicated particle research data. The recovery scripts are supposed to synchronize the vaults, but during a failover drill the scripts freeze. Your job is to reproduce the deadlock, diagnose the circular wait, then patch the synchronization strategy.

---

## Task Overview

| Level | Title | Key Commands / Concepts | Screenshots Required |
|:---:|-------|-------------------------|:-------------------:|
| **1** | Virtual Vault Provisioning | `dd`, `mkfs.ext4`, `udisksctl`, symlinks | yes |
| **2** | Naive Sync Scripts | `flock`, file descriptors, resource order | evidence file |
| **3** | Local Deadlock | two terminals, circular wait, `ps` | yes |
| **4** | Site-to-Site Sync | partner lock files, permissions | yes |
| **5** | Global Resource Ordering | Alpha-before-Beta rule | yes |
| **6** | Timeout Recovery | `flock -w`, bounded waiting | yes |
| **7** | Safe Ejection | unmount, loop-delete, cleanup | yes |

---

## Lab Setup

Navigate into your existing lab submission repository and create the `lab9` directory:

```bash
cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>
mkdir -p lab9
cd lab9
mkdir -p images scripts
```

Create the working folders used by the running scripts:

```bash
mkdir -p ~/bin
mkdir -p ~/os-lab-deadlock
```

### Required Working Locations

Your executable scripts must live in:

```bash
~/bin/
```

Your virtual vault images, mount shortcuts, and partner shared folders must live in:

```bash
~/os-lab-deadlock/
```

Your submission files and screenshots must be saved in:

```bash
~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9/
```

### Rules for This Lab

1. Use the shared Linux server with your assigned student account.
2. Do not use `sudo`.
3. Use `udisksctl` instead of `mount` for loopback mounting.
4. Script names must be lowercase, snake_case, and have no file extension.
5. Work with at least one classmate for Levels 4 and 5.
6. Copy your final scripts from `~/bin` into `lab9/scripts` before submitting.
7. Include every required working file and submission file in the tree checklist below.

---

## Quick Reference

### Virtual Disk and Mounting

| Command | Purpose |
|---------|---------|
| `dd if=/dev/zero of=file.img bs=1M count=10` | Create a 10 MB blank image file |
| `mkfs.ext4 -F file.img` | Format an image as an ext4 file system |
| `udisksctl loop-setup -f file.img` | Attach an image to a loop device |
| `udisksctl mount -b /dev/loopX` | Mount a loop device as a normal user |
| `findmnt -nr -o TARGET /dev/loopX` | Print the mount point for a mounted device |
| `ln -sfn target shortcut` | Create or replace a symbolic link |
| `udisksctl unmount -b /dev/loopX` | Unmount a device |
| `udisksctl loop-delete -b /dev/loopX` | Detach a loop device |

### Locks and Deadlock

| Command / Concept | Purpose |
|-------------------|---------|
| `flock -x 200` | Take an exclusive lock on file descriptor 200 |
| `exec 200> "$lockfile"` | Connect file descriptor 200 to a lock file |
| `flock -w 5 200` | Wait up to 5 seconds for a lock |
| circular wait | Each process holds one resource and waits for the other |
| global ordering | Every process locks resources in the same order |

### Process Inspection

| Command | Purpose |
|---------|---------|
| `ps aux | grep sync_` | Find running sync scripts |
| `jobs -l` | Show background jobs in the current shell |
| `kill <PID>` | Stop a process by PID |
| `df -h | grep loop` | Show mounted loopback file systems |

---

## Level 1 - Virtual Vault Provisioning

**Scenario:** *"Before the recovery drill can run, you must provision two virtual vault drives without administrator access."*

1. Move into the working folder:

```bash
cd ~/os-lab-deadlock
```

2. Create two 10 MB virtual vault images:

```bash
dd if=/dev/zero of=vault_alpha.img bs=1M count=10
dd if=/dev/zero of=vault_beta.img bs=1M count=10
```

3. Format both images:

```bash
mkfs.ext4 -F vault_alpha.img
mkfs.ext4 -F vault_beta.img
```

4. Attach both images to loop devices and save the device names:

```bash
alpha_loop=$(udisksctl loop-setup -f vault_alpha.img | awk '{print $NF}' | tr -d '.')
beta_loop=$(udisksctl loop-setup -f vault_beta.img | awk '{print $NF}' | tr -d '.')
echo "$alpha_loop" > alpha_loop.txt
echo "$beta_loop" > beta_loop.txt
cat alpha_loop.txt beta_loop.txt
```

5. Mount both loop devices:

```bash
udisksctl mount -b "$alpha_loop"
udisksctl mount -b "$beta_loop"
```

6. Create stable shortcuts named `mount_alpha` and `mount_beta`:

```bash
alpha_mount=$(findmnt -nr -o TARGET "$alpha_loop")
beta_mount=$(findmnt -nr -o TARGET "$beta_loop")
ln -sfn "$alpha_mount" mount_alpha
ln -sfn "$beta_mount" mount_beta
touch mount_alpha/lockfile
touch mount_beta/lockfile
```

7. Save evidence:

```bash
{
    echo "=== loop devices ==="
    cat ~/os-lab-deadlock/alpha_loop.txt
    cat ~/os-lab-deadlock/beta_loop.txt
    echo "=== vault files ==="
    ls -lh ~/os-lab-deadlock/vault_alpha.img ~/os-lab-deadlock/vault_beta.img
    echo "=== mount symlinks ==="
    ls -l ~/os-lab-deadlock/mount_alpha ~/os-lab-deadlock/mount_beta
    echo "=== mounted loop filesystems ==="
    df -h | grep loop
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9/task1_vaults.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9/task1_vaults.txt
```

> **Required Screenshot 1:** Save as `images/level1_vaults.png` and embed it in `README.md`.

---

## Level 2 - Naive Sync Scripts

**Scenario:** *"The first version of the recovery scripts locks both vaults, but each script chooses a different order."*

Create `sync_up`:

```bash
nano ~/bin/sync_up
```

Use this script:

```bash
#!/bin/bash

base="$HOME/os-lab-deadlock"
alpha_lock="$base/mount_alpha/lockfile"
beta_lock="$base/mount_beta/lockfile"

exec 200> "$alpha_lock"
exec 201> "$beta_lock"

echo "sync_up: waiting for Vault Alpha"
flock -x 200
echo "sync_up: locked Vault Alpha"
sleep 5

echo "sync_up: waiting for Vault Beta"
flock -x 201
echo "sync_up: locked Vault Beta"

echo "sync_up: synchronizing Alpha to Beta"
sleep 2
echo "sync_up: complete"
```

Create `sync_down`:

```bash
nano ~/bin/sync_down
```

Use this script:

```bash
#!/bin/bash

base="$HOME/os-lab-deadlock"
alpha_lock="$base/mount_alpha/lockfile"
beta_lock="$base/mount_beta/lockfile"

exec 200> "$alpha_lock"
exec 201> "$beta_lock"

echo "sync_down: waiting for Vault Beta"
flock -x 201
echo "sync_down: locked Vault Beta"
sleep 5

echo "sync_down: waiting for Vault Alpha"
flock -x 200
echo "sync_down: locked Vault Alpha"

echo "sync_down: synchronizing Beta to Alpha"
sleep 2
echo "sync_down: complete"
```

Make both scripts executable:

```bash
chmod +x ~/bin/sync_up ~/bin/sync_down
```

Save evidence:

```bash
{
    echo "=== sync script permissions ==="
    ls -l ~/bin/sync_up ~/bin/sync_down
    echo "=== sync_up lock order ==="
    grep -E "waiting for|locked Vault" ~/bin/sync_up
    echo "=== sync_down lock order ==="
    grep -E "waiting for|locked Vault" ~/bin/sync_down
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9/task2_sync_scripts.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9/task2_sync_scripts.txt
```

---

## Level 3 - Local Deadlock

**Scenario:** *"Both sync scripts run during the same failover window. Each script grabs one vault and waits forever for the other."*

1. Open two terminal windows.

2. In Terminal 1, run:

```bash
sync_up
```

3. Within 2 seconds, in Terminal 2, run:

```bash
sync_down
```

4. The expected result is a freeze:
   - `sync_up` holds Vault Alpha and waits for Vault Beta.
   - `sync_down` holds Vault Beta and waits for Vault Alpha.

5. In a third terminal, save evidence:

```bash
{
    echo "=== running sync processes ==="
    ps aux | grep '[s]ync_'
    echo "=== explanation ==="
    echo "sync_up holds Alpha and waits for Beta."
    echo "sync_down holds Beta and waits for Alpha."
    echo "This is circular wait, so neither script can continue."
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9/task3_local_deadlock.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9/task3_local_deadlock.txt
```

6. Stop the frozen scripts with `Ctrl+C` in each terminal.

> **Required Screenshot 2:** Save as `images/level3_local_deadlock.png` and embed it in `README.md`.

---

## Level 4 - Site-to-Site Sync with a Partner

**Scenario:** *"QuantumTech has two disaster recovery sites. Your local vault must sync with your partner's public recovery lock."*

Pair with a classmate. Decide who is **Player A** and who is **Player B**.

### Player A Setup

Player A creates a public Alpha recovery folder:

```bash
mkdir -p ~/os-lab-deadlock/public_dr_alpha
touch ~/os-lab-deadlock/public_dr_alpha/vault.lock
chmod o+x "$HOME"
chmod o+x ~/os-lab-deadlock
chmod 755 ~/os-lab-deadlock/public_dr_alpha
chmod o+rw ~/os-lab-deadlock/public_dr_alpha/vault.lock
```

Player A creates `cross_sync_alpha`:

```bash
nano ~/bin/cross_sync_alpha
```

Use this script, replacing `<PartnerUsername>` with Player B's Linux username:

```bash
#!/bin/bash

local_lock="$HOME/os-lab-deadlock/public_dr_alpha/vault.lock"
partner_lock="/home/<PartnerUsername>/os-lab-deadlock/public_dr_beta/vault.lock"

exec 200> "$local_lock"
exec 201> "$partner_lock"

echo "cross_sync_alpha: waiting for local Alpha"
flock -x 200
echo "cross_sync_alpha: locked local Alpha"
sleep 5

echo "cross_sync_alpha: waiting for partner Beta"
flock -x 201
echo "cross_sync_alpha: locked partner Beta"

echo "cross_sync_alpha: complete"
```

### Player B Setup

Player B creates a public Beta recovery folder:

```bash
mkdir -p ~/os-lab-deadlock/public_dr_beta
touch ~/os-lab-deadlock/public_dr_beta/vault.lock
chmod o+x "$HOME"
chmod o+x ~/os-lab-deadlock
chmod 755 ~/os-lab-deadlock/public_dr_beta
chmod o+rw ~/os-lab-deadlock/public_dr_beta/vault.lock
```

Player B creates `cross_sync_beta`:

```bash
nano ~/bin/cross_sync_beta
```

Use this script, replacing `<PartnerUsername>` with Player A's Linux username:

```bash
#!/bin/bash

local_lock="$HOME/os-lab-deadlock/public_dr_beta/vault.lock"
partner_lock="/home/<PartnerUsername>/os-lab-deadlock/public_dr_alpha/vault.lock"

exec 200> "$local_lock"
exec 201> "$partner_lock"

echo "cross_sync_beta: waiting for local Beta"
flock -x 200
echo "cross_sync_beta: locked local Beta"
sleep 5

echo "cross_sync_beta: waiting for partner Alpha"
flock -x 201
echo "cross_sync_beta: locked partner Alpha"

echo "cross_sync_beta: complete"
```

### Run the Cross-Site Deadlock

Make your role script executable:

```bash
chmod +x ~/bin/cross_sync_alpha 2>/dev/null
chmod +x ~/bin/cross_sync_beta 2>/dev/null
```

Player A and Player B should run their scripts at nearly the same time:

```bash
cross_sync_alpha
```

or:

```bash
cross_sync_beta
```

Save evidence in a third terminal:

```bash
{
    echo "=== public DR permissions ==="
    ls -ld "$HOME" ~/os-lab-deadlock ~/os-lab-deadlock/public_dr_* 2>/dev/null
    ls -l ~/os-lab-deadlock/public_dr_* 2>/dev/null
    echo "=== running cross sync processes ==="
    ps aux | grep '[c]ross_sync'
    echo "=== partner role ==="
    echo "Partner username: <PartnerUsername>"
    echo "My role: Player A or Player B"
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9/task4_cross_deadlock.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9/task4_cross_deadlock.txt
```

Stop the frozen scripts with `Ctrl+C`.

> **Required Screenshot 3:** Save as `images/level4_cross_deadlock.png` and embed it in `README.md`.

---

## Level 5 - Global Resource Ordering Patch

**Scenario:** *"The recovery policy is changed: every script must lock Alpha before Beta. Same order means circular wait is impossible."*

The global rule is:

```text
Always lock Alpha first, then Beta.
```

Player A's `cross_sync_alpha` already follows this order:

```text
local Alpha -> partner Beta
```

Player B must edit `cross_sync_beta` so it locks partner Alpha first, then local Beta:

```bash
nano ~/bin/cross_sync_beta
```

Player B should use this patched structure:

```bash
#!/bin/bash

partner_alpha="/home/<PartnerUsername>/os-lab-deadlock/public_dr_alpha/vault.lock"
local_beta="$HOME/os-lab-deadlock/public_dr_beta/vault.lock"

exec 200> "$partner_alpha"
exec 201> "$local_beta"

echo "cross_sync_beta: waiting for partner Alpha"
flock -x 200
echo "cross_sync_beta: locked partner Alpha"
sleep 5

echo "cross_sync_beta: waiting for local Beta"
flock -x 201
echo "cross_sync_beta: locked local Beta"

echo "cross_sync_beta: complete"
```

Run both scripts again at nearly the same time. This time, one script may wait, but both should eventually complete.

Save evidence:

```bash
{
    echo "=== global ordering rule ==="
    echo "All scripts lock Alpha before Beta."
    echo "=== my role script order ==="
    grep -E "waiting for|locked" ~/bin/cross_sync_alpha ~/bin/cross_sync_beta 2>/dev/null
    echo "=== result ==="
    echo "Both cross-site scripts completed without deadlock."
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9/task5_ordering_patch.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9/task5_ordering_patch.txt
```

> **Required Screenshot 4:** Save as `images/level5_ordering_patch.png` and embed it in `README.md`.

---

## Level 6 - Timeout Recovery

**Scenario:** *"A production recovery script must not wait forever. If it cannot acquire the next lock, it should fail clearly and release what it holds."*

Create `sync_timeout`:

```bash
nano ~/bin/sync_timeout
```

Use this script:

```bash
#!/bin/bash

base="$HOME/os-lab-deadlock"
alpha_lock="$base/mount_alpha/lockfile"
beta_lock="$base/mount_beta/lockfile"

exec 200> "$alpha_lock"
exec 201> "$beta_lock"

echo "sync_timeout: waiting for Vault Alpha"
if ! flock -w 5 200; then
    echo "ERROR: could not lock Vault Alpha within 5 seconds"
    exit 1
fi
echo "sync_timeout: locked Vault Alpha"

sleep 2

echo "sync_timeout: waiting for Vault Beta"
if ! flock -w 5 201; then
    echo "ERROR: could not lock Vault Beta within 5 seconds"
    exit 2
fi
echo "sync_timeout: locked Vault Beta"

echo "sync_timeout: complete"
```

Make it executable:

```bash
chmod +x ~/bin/sync_timeout
```

Test the timeout:

1. In Terminal 1, run the old script:

```bash
sync_down
```

2. Quickly, in Terminal 2, run:

```bash
sync_timeout
echo "exit status: $?"
```

3. `sync_timeout` should eventually print an error instead of waiting forever.

4. Stop `sync_down` with `Ctrl+C`.

Save evidence:

```bash
{
    echo "=== sync_timeout permissions ==="
    ls -l ~/bin/sync_timeout
    echo "=== timeout evidence ==="
    echo "Paste the timeout error and exit status shown in your terminal."
    echo "=== process check after stopping old script ==="
    ps aux | grep '[s]ync_' || true
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9/task6_timeout_recovery.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9/task6_timeout_recovery.txt
```

> **Required Screenshot 5:** Save as `images/level6_timeout_recovery.png` and embed it in `README.md`.

---

## Level 7 - Safe Ejection

**Scenario:** *"The drill is complete. The vault images must be safely unmounted and detached so the server is not left with stale loop devices."*

Create `teardown`:

```bash
nano ~/bin/teardown
```

Use this script:

```bash
#!/bin/bash

base="$HOME/os-lab-deadlock"

alpha_loop="$(cat "$base/alpha_loop.txt" 2>/dev/null)"
beta_loop="$(cat "$base/beta_loop.txt" 2>/dev/null)"

if [ -n "$alpha_loop" ]; then
    echo "Unmounting Alpha: $alpha_loop"
    udisksctl unmount -b "$alpha_loop" 2>/dev/null
    echo "Detaching Alpha: $alpha_loop"
    udisksctl loop-delete -b "$alpha_loop" 2>/dev/null
fi

if [ -n "$beta_loop" ]; then
    echo "Unmounting Beta: $beta_loop"
    udisksctl unmount -b "$beta_loop" 2>/dev/null
    echo "Detaching Beta: $beta_loop"
    udisksctl loop-delete -b "$beta_loop" 2>/dev/null
fi

rm -f "$base/mount_alpha" "$base/mount_beta"

echo "Remaining loop mounts:"
df -h | grep loop || echo "No loop mounts found."
```

Make it executable and run it:

```bash
chmod +x ~/bin/teardown
teardown
```

Save evidence:

```bash
{
    echo "=== teardown script ==="
    ls -l ~/bin/teardown
    echo "=== loop mount check ==="
    df -h | grep loop || echo "No loop mounts found."
    echo "=== remaining working folder ==="
    ls -l ~/os-lab-deadlock
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9/task7_teardown.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9/task7_teardown.txt
```

> **Required Screenshot 6:** Save as `images/level7_teardown.png` and embed it in `README.md`.

---

## Copy Scripts for Submission

Before submitting, copy your scripts into your lab folder:

```bash
cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab9
mkdir -p scripts
cp ~/bin/sync_up scripts/
cp ~/bin/sync_down scripts/
cp ~/bin/sync_timeout scripts/
cp ~/bin/teardown scripts/
cp ~/bin/cross_sync_alpha scripts/ 2>/dev/null || true
cp ~/bin/cross_sync_beta scripts/ 2>/dev/null || true
```

Also save a small operational README in the working folder:

```bash
cat > ~/os-lab-deadlock/README.md <<'EOF'
Quantum Vault Deadlock working folder

Student ID: <YourStudentID>
Role: Player A or Player B
Partner username: <PartnerUsername>

This folder contains virtual vault image files, loop device records,
mount shortcuts, and public disaster recovery lock files used by Lab 9.
EOF
```

---

## Lab Questions

Answer these in your `README.md`:

1. Why does this lab use `udisksctl` instead of the normal `mount` command?
2. What do `vault_alpha.img` and `vault_beta.img` simulate?
3. In the local deadlock, which resource did `sync_up` hold, and which resource did it wait for?
4. In the local deadlock, which resource did `sync_down` hold, and which resource did it wait for?
5. Which four deadlock conditions were present in Level 3?
6. How does the global Alpha-before-Beta ordering rule break circular wait?
7. Why is `flock -w` useful for recovery even though it does not prevent every deadlock?
8. Why is safe teardown important when working with loopback devices?

---

## Screenshot Checklist

Before submitting, verify you have all required screenshots:

| # | File Name | Level | What It Shows |
|:-:|-----------|:----:|---------------|
| 1 | `level1_vaults.png` | Level 1 | Loop devices, mounted vaults, and `mount_alpha` / `mount_beta` symlinks |
| 2 | `level3_local_deadlock.png` | Level 3 | Frozen `sync_up` and `sync_down` terminals or process evidence |
| 3 | `level4_cross_deadlock.png` | Level 4 | Partner cross-site scripts frozen in circular wait |
| 4 | `level5_ordering_patch.png` | Level 5 | Ordered locking completes without deadlock |
| 5 | `level6_timeout_recovery.png` | Level 6 | Timeout error and nonzero exit status |
| 6 | `level7_teardown.png` | Level 7 | Clean loop mount check after teardown |

---

## Final Submission

### Required Working Tree Outside the Repo

These files and folders must exist while you are running the lab:

```text
~/
|-- bin/
|   |-- sync_up
|   |-- sync_down
|   |-- sync_timeout
|   |-- teardown
|   `-- cross_sync_alpha OR cross_sync_beta
`-- os-lab-deadlock/
    |-- README.md
    |-- alpha_loop.txt
    |-- beta_loop.txt
    |-- vault_alpha.img
    |-- vault_beta.img
    |-- mount_alpha -> mounted Alpha vault path
    |-- mount_beta -> mounted Beta vault path
    `-- public_dr_alpha/ OR public_dr_beta/
        `-- vault.lock
```

After Level 7, `mount_alpha` and `mount_beta` should be removed by `teardown`. The tree above documents what must exist during the active deadlock tasks.

### Required Submission Tree

```text
os-se-<YourStudentID>/
`-- os-lab-<YourStudentID>/
    `-- lab9/
        |-- README.md
        |-- task1_vaults.txt
        |-- task2_sync_scripts.txt
        |-- task3_local_deadlock.txt
        |-- task4_cross_deadlock.txt
        |-- task5_ordering_patch.txt
        |-- task6_timeout_recovery.txt
        |-- task7_teardown.txt
        |-- scripts/
        |   |-- sync_up
        |   |-- sync_down
        |   |-- sync_timeout
        |   |-- teardown
        |   `-- cross_sync_alpha OR cross_sync_beta
        `-- images/
            |-- level1_vaults.png
            |-- level3_local_deadlock.png
            |-- level4_cross_deadlock.png
            |-- level5_ordering_patch.png
            |-- level6_timeout_recovery.png
            `-- level7_teardown.png
```

### Git Push

```bash
cd ~/os-se-<YourStudentID>
git add .
git commit -m "Lab 9: Virtual vault deadlock and recovery"
git push origin main
```

---

## Grading Criteria

| Criteria | Points | Description |
|----------|--------|-------------|
| **Level 1: Virtual vault provisioning** | 15 | Creates, formats, mounts, links, and documents Alpha and Beta vault images without `sudo`. |
| **Level 2: Naive sync scripts** | 10 | `sync_up` and `sync_down` use `flock` and intentionally opposite lock orders. |
| **Level 3: Local deadlock analysis** | 15 | Demonstrates and explains circular wait using local scripts. |
| **Level 4: Cross-site partner deadlock** | 15 | Configures partner-visible lock files and demonstrates cross-user deadlock. |
| **Level 5: Global ordering patch** | 15 | Applies Alpha-before-Beta ordering and proves both scripts complete. |
| **Level 6: Timeout recovery** | 10 | Uses `flock -w` to avoid waiting forever and reports timeout behavior clearly. |
| **Level 7: Safe teardown** | 10 | Unmounts, detaches loop devices, removes symlinks, and verifies a clean state. |
| **README, screenshots, and organization** | 10 | Submission tree is complete, screenshots are embedded, and answers show understanding. |
| **Total** | **100** | |

---

## Tips

- If `mount_alpha/lockfile` does not exist, confirm that the symlink points to a mounted vault.
- If `udisksctl mount` fails, check whether the loop device name in `alpha_loop.txt` or `beta_loop.txt` is correct.
- If your partner cannot access your `vault.lock`, check traversal permission on your home directory and `~/os-lab-deadlock`.
- If both scripts still freeze after Level 5, recheck the lock order. Every cross-site script must lock Alpha before Beta.
- Do not skip teardown. Stale loop devices make later testing confusing.
