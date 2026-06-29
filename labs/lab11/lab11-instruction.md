# OS Extra Lab (Bonus) - Linux Disk Management Utilities (Hands-on)

| | |
|---|---|
| **Course** | Operating Systems |
| **Lab Title** | The QuantumTech Storage Capacity Drill |
| **Chapter** | Storage, Filesystems, Disk Management |
| **Duration** | 2-3 Hours |
| **Lab Type** | Individual |
| **Status** | ⭐ **EXTRA LAB - BONUS POINTS ONLY** |

---

> **⭐ THIS IS A BONUS LAB**
>
> This lab is **optional**. It does **not** replace any required lab and there is **no penalty** for skipping it. Completing it adds **bonus points** to your Operating Systems lab total (see the Grading table). Treat it as a chance to go deeper on real storage administration skills.

---

**Source reference:** This canonical lab instruction continues the QuantumTech series from Labs 7-10. Like Lab 10, the **core path runs entirely with a normal user account** - it manages **disk-image files** (not real hardware) and mounts them with **FUSE** (`fuse2fs`), so **no `sudo` and no real partitions are required**. Wherever a step would normally need root on real hardware, the lab shows the no-sudo equivalent and clearly marks the `sudo`-only alternative as *optional*.

---

> **IMPORTANT - READ EVERYTHING FIRST**
>
> This lab uses files and folders in two places:
>
> 1. Your **submission folder** inside `~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11`
> 2. Your **working folder** outside the repo: `~/os-lab-disk` (and scripts in `~/bin`)
>
> The working folder holds the **virtual disk images** you will create, format, mount, fill, check, and resize. None of this touches the server's real disks, so it is safe to repeat.
>
> **Why disk images instead of real disks?** On a shared server you cannot be handed a spare physical disk, and `fdisk`/`mkfs` on a real device would destroy other students' data. A **disk image** is just a regular file that Linux can treat as a block device. You learn the *exact same commands* (`mkfs`, `e2fsck`, `resize2fs`, `df`, `du`, `blkid`, `dumpe2fs`) against a file you own, with zero risk.
>
> **A note on the mount step:** mounting a filesystem normally requires root. This lab uses **`fuse2fs`** (a userspace FUSE driver shipped with `e2fsprogs`) so you can mount your ext4 image **without `sudo`**. If `fuse2fs` is missing on your server, an *optional* `sudo mount -o loop` path is given - use it only if your instructor allows sudo.
>
> **Document structure:**
> 1. **Lab Objectives** - What you will learn
> 2. **Mission Briefing** - Storage scenario
> 3. **Task Overview** - Summary of all levels
> 4. **Lab Setup** - Repository, working folder, naming rules, tool check
> 5. **Quick Reference** - Inspection, images, filesystems, mounting, maintenance
> 6. **Levels 0-8** - Inventory, usage analysis, image creation, formatting, mounting, the utility script, maintenance/resize, design-your-own, teardown
> 7. **Deliverables & Submission** - Tree structure, README template, git push
> 8. **Screenshot Checklist** - Every screenshot you need, in one place

---

## Lab Objectives

After completing this lab, students will be able to:

1. Inventory a Linux system's block devices, partitions, and mounted filesystems using `lsblk`, `findmnt`, `blkid`, and `df -hT`.
2. Distinguish **disk space used by the filesystem** (`df`) from **space consumed by files** (`du`), and locate the largest space consumers on a system.
3. Create **virtual disk images** with `truncate`, `fallocate`, and `dd`, and explain the difference between a **sparse** file and a fully **allocated** one.
4. Put a real filesystem on an image with `mkfs.ext4` and inspect its metadata with `file`, `blkid`, `dumpe2fs`, and `tune2fs`.
5. **Mount** an ext4 image without root using `fuse2fs` (FUSE), read and write files on it, and cleanly unmount with `fusermount -u`.
6. Build a reusable Bash **disk-management utility** that reports mounted filesystems, per-directory usage, the top space consumers, and raises a threshold alert.
7. Run filesystem maintenance: check and repair with `e2fsck`, and **grow** a filesystem by enlarging its image and running `resize2fs`.
8. Independently design a disk-related diagnostic script from scratch.
9. Cleanly tear down mounts and remove image files without leaving stray loop/FUSE mounts behind.

> **Scenario:** You are an **SRE / DevOps engineer** at **QuantumTech**. A build server keeps running low on disk space, an analytics job filled a volume overnight, and nobody could say *which directory* ate the space or *how much headroom* was left. Management wants a repeatable storage drill: inventory the disks, measure real usage, stand up a scratch volume, prove you can format, mount, fill, check, and grow it, and ship a small utility that reports capacity at a glance. You will rehearse the entire workflow safely on disk **images** so the production disks are never at risk.

---

## Task Overview

| Level | Title | Key Commands / Concepts | Screenshots Required |
|:---:|-------|-------------------------|:-------------------:|
| **0** | Storage Inventory | `lsblk`, `findmnt`, `df -hT`, `blkid`, `mount` | yes |
| **1** | Usage Analysis: `df` vs `du` | `df`, `du`, `sort -h`, top consumers | yes |
| **2** | Create a Virtual Disk Image | `truncate`, `fallocate`, `dd`, sparse vs allocated | yes |
| **3** | Format & Inspect a Filesystem | `mkfs.ext4`, `file`, `blkid`, `dumpe2fs`, `tune2fs` | yes |
| **4** | Mount Without Root (FUSE) | `fuse2fs`, `fusermount -u`, `df` of the mount | yes |
| **5** | Build the Disk Utility Script | functions, `df`, `du`, threshold alert, logging | yes |
| **6** | Maintenance: Check & Grow | `e2fsck -f`, `truncate` grow, `resize2fs` | yes |
| **7** | Design Your Own Disk Tool | student-authored diagnostic script | yes |
| **8** | Teardown and Reset | `fusermount -u`, remove images, verify clean | yes |

---

## Lab Setup

Navigate into your existing lab submission repository and create the `lab11` directory:

```bash
cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>
mkdir -p lab11
cd lab11
mkdir -p images scripts
```

Create the working folder used by the disk drill (outside the repo):

```bash
mkdir -p ~/bin
mkdir -p ~/os-lab-disk
mkdir -p ~/os-lab-disk/images
mkdir -p ~/os-lab-disk/mnt
mkdir -p ~/os-lab-disk/logs
```

### Required Working Locations

| Path | Holds |
|------|-------|
| `~/bin/` | Your executable scripts |
| `~/os-lab-disk/images/` | The virtual disk-image files (`.img`) you create and format |
| `~/os-lab-disk/mnt/` | Mount point where you attach an image with `fuse2fs` |
| `~/os-lab-disk/logs/` | Logs and reports written by your utility script |
| `~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/` | Submission files and screenshots |

### Make `~/bin` Runnable (if it is not already)

```bash
export PATH="$HOME/bin:$PATH"
```

### Tool Check (run this first)

Confirm the disk tools you need are present. Most are in `coreutils` and `e2fsprogs`:

```bash
for t in lsblk findmnt blkid df du truncate fallocate dd mkfs.ext4 dumpe2fs tune2fs e2fsck resize2fs fuse2fs fusermount; do
    if command -v "$t" >/dev/null 2>&1; then
        printf '%-12s OK   %s\n' "$t" "$(command -v "$t")"
    else
        printf '%-12s MISSING\n' "$t"
    fi
done
```

> **If `fuse2fs` is MISSING:** you can still complete Levels 0-3 and 6-8 (image, format, inspect, check, resize) without it. For Level 4 (mounting), use the *optional* `sudo mount -o loop` path shown in that level, **only** if your instructor permits sudo. `fuse2fs` ships with `e2fsprogs` on most modern distros.

### Rules for This Lab

1. Use the shared Linux server with your assigned student account.
2. The **core path uses no `sudo`**. Only mount your **own** image files; never run `mkfs`, `fdisk`, or `mount` against a real device such as `/dev/sda`.
3. Keep all image files inside `~/os-lab-disk/images/`. Use small images (64-128 MB) so formatting is fast.
4. Script names must be lowercase, snake_case, and have no file extension.
5. Every report your utility writes must be timestamped and saved under `~/os-lab-disk/logs/`.
6. Always **unmount** an image with `fusermount -u` before deleting it (Level 8).
7. Copy your final scripts from `~/bin` into `lab11/scripts` before submitting.

> **⚠️ Safety:** `mkfs` and `dd` are destructive **on real devices**. In this lab they only ever target a **file** (e.g. `~/os-lab-disk/images/scratch.img`). Double-check the target every time - never put a `/dev/...` path where the lab says `*.img`.

---

## Quick Reference

### Inspecting Disks and Filesystems

| Command | Purpose |
|---------|---------|
| `lsblk -f` | Tree of block devices with filesystem, label, mountpoint |
| `findmnt` | Tree of all current mounts (source, target, type, options) |
| `df -hT` | Mounted filesystems: type, size, used, avail, use% |
| `df -i` | Filesystems by **inode** usage (files-count limit, not bytes) |
| `blkid <img>` | UUID, type, and label of a filesystem (works on an image file) |
| `mount` / `cat /proc/mounts` | Raw list of what is mounted where |

### Measuring Usage: `df` vs `du`

| Command | Purpose |
|---------|---------|
| `df -h <path>` | How full the **filesystem** holding `<path>` is |
| `du -sh <dir>` | Total size of **files** under `<dir>` |
| `du -h --max-depth=1 <dir>` | Size of each immediate subdirectory |
| `du -h --max-depth=1 <dir> \| sort -h` | Same, sorted smallest-to-largest |
| `du -ah <dir> \| sort -h \| tail -n 10` | The 10 biggest files/dirs |

> **`df` vs `du`:** `df` measures the **filesystem** (what the kernel says is used/free on the device). `du` adds up the **files** you can see. They disagree when files are deleted but still held open, or because of reserved blocks and sparse files.

### Creating Disk Images

| Command | Result |
|---------|--------|
| `truncate -s 64M disk.img` | **Sparse** 64 MB image (uses ~0 bytes until written) |
| `fallocate -l 64M disk.img` | **Allocated** 64 MB image (reserves all blocks now) |
| `dd if=/dev/zero of=disk.img bs=1M count=64` | 64 MB image written zero-by-zero (slow, fully written) |
| `du -h disk.img` vs `ls -lh disk.img` | Real disk usage vs apparent size (reveals sparseness) |

### Filesystem Creation, Inspection, Maintenance

| Command | Purpose |
|---------|---------|
| `mkfs.ext4 -F disk.img` | Make an ext4 filesystem **inside the image file** (no root needed) |
| `file disk.img` | Identify the filesystem type written into the image |
| `dumpe2fs -h disk.img` | Superblock summary: block size, counts, features |
| `tune2fs -l disk.img` | Tunable parameters and filesystem state |
| `e2fsck -f disk.img` | Force a consistency check (and repair) of the image |
| `resize2fs disk.img` | Grow/shrink the ext filesystem to the image's new size |

### Mounting Without Root (FUSE)

| Command | Purpose |
|---------|---------|
| `fuse2fs disk.img mnt` | Mount the ext image at `mnt` **as a normal user** |
| `df -hT mnt` / `findmnt mnt` | Confirm the FUSE mount and its free space |
| `fusermount -u mnt` | Unmount the FUSE filesystem cleanly |

> **Optional sudo alternative (only if allowed):** `sudo mount -o loop disk.img mnt` then `sudo umount mnt`. The lab's graded path uses `fuse2fs`, so use this only if `fuse2fs` is unavailable.

---

## Level 0 - Storage Inventory

**Scenario:** *"Before you can fix a capacity problem you must see the whole storage picture: which block devices exist, what filesystems are on them, where they are mounted, and how full each one is."*

1. List block devices with their filesystems and mount points (read-only, safe):

```bash
lsblk -f
```

2. Show the mount tree and the mounted filesystems with type and usage:

```bash
findmnt
df -hT
```

3. Show **inode** usage too (a filesystem can be "full" on inodes while bytes remain free):

```bash
df -i
```

4. Identify the filesystem that holds your home directory, and read its details:

```bash
df -hT "$HOME"
findmnt --target "$HOME"
```

5. Save evidence:

```bash
{
    echo "=== block devices (lsblk -f) ==="
    lsblk -f
    echo "=== mounted filesystems (df -hT) ==="
    df -hT
    echo "=== inode usage (df -i) ==="
    df -i
    echo "=== filesystem holding HOME ==="
    df -hT "$HOME"
    findmnt --target "$HOME"
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task0_inventory.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task0_inventory.txt
```

> **Required Screenshot 1:** Save as `images/level0_inventory.png` and embed it in `README.md`. It must show `lsblk -f` and `df -hT`.

---

## Level 1 - Usage Analysis: `df` vs `du`

**Scenario:** *"The build server is 'full' but nobody knows which directory is to blame. Learn the two measuring tools - `df` for the filesystem, `du` for the files - and hunt down the biggest consumers."*

1. Create a small sample tree with some bulky files so there is something to measure:

```bash
mkdir -p ~/os-lab-disk/sample/logs ~/os-lab-disk/sample/data ~/os-lab-disk/sample/cache
seq 1 200000 > ~/os-lab-disk/sample/logs/app.log
dd if=/dev/zero of=~/os-lab-disk/sample/data/blob.bin bs=1M count=8
yes "cache line" | head -n 100000 > ~/os-lab-disk/sample/cache/cache.txt
```

2. Compare **filesystem** usage with **file** usage for the same place:

```bash
df -h ~/os-lab-disk/sample
du -sh ~/os-lab-disk/sample
```

3. Break the total down per subdirectory, sorted so the biggest is last:

```bash
du -h --max-depth=1 ~/os-lab-disk/sample | sort -h
```

4. Find the **10 largest files or folders** under the sample tree:

```bash
du -ah ~/os-lab-disk/sample | sort -h | tail -n 10
```

5. Save evidence:

```bash
{
    echo "=== df (filesystem view) ==="
    df -h ~/os-lab-disk/sample
    echo "=== du (files view) ==="
    du -sh ~/os-lab-disk/sample
    echo "=== per-directory breakdown (sorted) ==="
    du -h --max-depth=1 ~/os-lab-disk/sample | sort -h
    echo "=== top 10 consumers ==="
    du -ah ~/os-lab-disk/sample | sort -h | tail -n 10
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task1_usage.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task1_usage.txt
```

> **Required Screenshot 2:** Save as `images/level1_usage.png` and embed it in `README.md`. It must show the per-directory breakdown and the top-10 list.

---

## Level 2 - Create a Virtual Disk Image

**Scenario:** *"You need a scratch volume to rehearse on. Instead of a real disk, you will carve out an image file - and learn why a 'sparse' image can claim 64 MB while using almost no real space."*

1. Move into the images folder:

```bash
cd ~/os-lab-disk/images
```

2. Create a **sparse** 64 MB image and a **fully allocated** 64 MB image:

```bash
truncate -s 64M sparse.img
fallocate -l 64M full.img
```

3. Compare **apparent size** (`ls -lh`) against **real disk usage** (`du -h`). The sparse file looks 64 MB but consumes almost nothing yet; the allocated file consumes the full 64 MB:

```bash
ls -lh sparse.img full.img
du -h sparse.img full.img
```

4. Create the working image you will use for the rest of the lab with `dd` (this one is fully written with zeros):

```bash
dd if=/dev/zero of=scratch.img bs=1M count=64 status=progress
ls -lh scratch.img
```

5. Save evidence:

```bash
{
    echo "=== apparent size (ls -lh) ==="
    ls -lh ~/os-lab-disk/images/sparse.img ~/os-lab-disk/images/full.img
    echo "=== real disk usage (du -h) -> note sparse uses ~0 ==="
    du -h ~/os-lab-disk/images/sparse.img ~/os-lab-disk/images/full.img
    echo "=== working image created with dd ==="
    ls -lh ~/os-lab-disk/images/scratch.img
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task2_image.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task2_image.txt
```

> **Required Screenshot 3:** Save as `images/level2_image.png` and embed it in `README.md`. The difference between `ls -lh` (apparent) and `du -h` (real) for the **sparse** image must be visible.

---

## Level 3 - Format & Inspect a Filesystem

**Scenario:** *"An empty image is just bytes. Now put a real ext4 filesystem on it - the same `mkfs` an admin runs on a real partition - and read its metadata to confirm what you built."*

1. Create an **ext4** filesystem inside `scratch.img`. The `-F` forces `mkfs` to accept a plain file (not a block device). **No root needed** - you own the file:

```bash
cd ~/os-lab-disk/images
mkfs.ext4 -F -L QT_SCRATCH scratch.img
```

2. Confirm what the image now is, and read its UUID, label, and type:

```bash
file scratch.img
blkid scratch.img
```

3. Read the superblock summary and the tunable parameters:

```bash
dumpe2fs -h scratch.img
tune2fs -l scratch.img | grep -E 'Filesystem (volume name|state|UUID)|Block size|Inode count|Block count'
```

4. Save evidence:

```bash
{
    echo "=== file type of the formatted image ==="
    file ~/os-lab-disk/images/scratch.img
    echo "=== blkid (UUID / LABEL / TYPE) ==="
    blkid ~/os-lab-disk/images/scratch.img
    echo "=== superblock summary (dumpe2fs -h) ==="
    dumpe2fs -h ~/os-lab-disk/images/scratch.img
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task3_format.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task3_format.txt
```

> **Required Screenshot 4:** Save as `images/level3_format.png` and embed it in `README.md`. It must show `file scratch.img` reporting an ext4 filesystem and the `blkid` line with the `QT_SCRATCH` label.

---

## Level 4 - Mount Without Root (FUSE)

**Scenario:** *"A filesystem you cannot mount is useless. Normally mounting needs root, but `fuse2fs` lets you attach your own ext4 image as an ordinary user. Mount it, write data to it, prove it works, then unmount it cleanly."*

1. Mount `scratch.img` at your prepared mount point using FUSE (no sudo):

```bash
cd ~/os-lab-disk
fuse2fs images/scratch.img mnt
```

> If `fuse2fs` printed a warning about `fakeroot` or permissions but `findmnt mnt` (next step) shows the mount, you are fine.

2. Confirm the mount and its free space:

```bash
findmnt mnt
df -hT mnt
```

3. Write real data onto the mounted volume, then confirm the filesystem usage changed:

```bash
echo "QuantumTech scratch volume online" > mnt/hello.txt
seq 1 50000 > mnt/numbers.txt
ls -lh mnt
df -h mnt
```

4. Unmount cleanly with `fusermount -u` and confirm it is gone:

```bash
fusermount -u mnt
findmnt mnt || echo "scratch.img is unmounted"
```

5. Save evidence:

```bash
# (re-mount briefly so the evidence shows a live mount, then unmount again)
fuse2fs ~/os-lab-disk/images/scratch.img ~/os-lab-disk/mnt
{
    echo "=== mount confirmed (findmnt) ==="
    findmnt ~/os-lab-disk/mnt
    echo "=== filesystem usage of the mount (df -hT) ==="
    df -hT ~/os-lab-disk/mnt
    echo "=== files written onto the volume ==="
    ls -lh ~/os-lab-disk/mnt
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task4_mount.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task4_mount.txt
fusermount -u ~/os-lab-disk/mnt
```

> **Optional sudo alternative** (only if `fuse2fs` is unavailable and your instructor allows sudo):
> ```bash
> sudo mount -o loop ~/os-lab-disk/images/scratch.img ~/os-lab-disk/mnt
> df -hT ~/os-lab-disk/mnt
> sudo umount ~/os-lab-disk/mnt
> ```

> **Required Screenshot 5:** Save as `images/level4_mount.png` and embed it in `README.md`. It must show `findmnt`/`df -hT` for the mount and the files you wrote onto it.

---

## Level 5 - Build the Disk Utility Script

**Scenario:** *"Capacity should be one command away, not a forensic investigation each time. Package the inspection skills into one reusable utility that prints mounted filesystems, the biggest directories under a target, and raises an alert when any filesystem crosses a usage threshold."*

1. Create `disk_report`:

```bash
nano ~/bin/disk_report
```

2. Use this script:

```bash
#!/bin/bash
set -euo pipefail

base="$HOME/os-lab-disk"
logdir="$base/logs"
report="$logdir/disk_report.log"
target="${1:-$HOME}"     # directory to analyze; defaults to $HOME
threshold=80             # percent filesystem usage that triggers an alert

mkdir -p "$logdir"
stamp() { date '+%Y-%m-%d %H:%M:%S'; }

{
    echo "===== QuantumTech disk report at $(stamp) ====="
    echo "target directory   : $target"
    echo

    echo "----- mounted filesystems -----"
    df -hT

    echo
    echo "----- top 5 directories under target -----"
    du -h --max-depth=1 "$target" 2>/dev/null | sort -h | tail -n 5

    echo
    echo "----- filesystem holding target -----"
    df -h "$target"

    # Threshold alert: read the use% of the filesystem holding the target.
    usage=$(df -P "$target" | awk 'NR==2 {gsub("%",""); print $5}')
    echo
    if [ "$usage" -ge "$threshold" ]; then
        echo "ALERT: filesystem for $target is ${usage}% full (>= ${threshold}% threshold)!"
    else
        echo "status: OK - filesystem for $target is ${usage}% full (below ${threshold}%)."
    fi
    echo
} | tee -a "$report"
```

3. Make it executable and run it twice - once on the default target, once on your sample tree:

```bash
chmod +x ~/bin/disk_report
disk_report
disk_report ~/os-lab-disk/sample
```

4. Confirm the report log is append-only (it grew on the second run):

```bash
tail -n 30 ~/os-lab-disk/logs/disk_report.log
```

5. (Optional) Force the alert branch to prove it works, by lowering the threshold for one run:

```bash
sed 's/^threshold=80/threshold=0/' ~/bin/disk_report | bash -s ~/os-lab-disk/sample | grep ALERT
```

6. Save evidence:

```bash
{
    echo "=== disk_report script permissions ==="
    ls -l ~/bin/disk_report
    echo "=== disk_report run on the sample tree ==="
    disk_report ~/os-lab-disk/sample
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task5_utility.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task5_utility.txt
```

> **Required Screenshot 6:** Save as `images/level5_utility.png` and embed it in `README.md`. It must show `disk_report` output including the mounted filesystems, the top directories, and the status/alert line.

---

## Level 6 - Maintenance: Check & Grow

**Scenario:** *"Volumes get corrupted and volumes fill up. Two core admin skills close the loop: run a filesystem check, then grow the filesystem when it runs out of room - exactly what you would do to an LVM volume in production, rehearsed safely on your image."*

1. Make sure the image is **not mounted**, then force a full consistency check:

```bash
fusermount -u ~/os-lab-disk/mnt 2>/dev/null || true
e2fsck -f ~/os-lab-disk/images/scratch.img
```

A clean image reports passes 1-5 with no errors.

2. Record the current size (the filesystem currently fills the 64 MB image):

```bash
ls -lh ~/os-lab-disk/images/scratch.img
tune2fs -l ~/os-lab-disk/images/scratch.img | grep -E 'Block count|Block size'
```

3. **Grow** the image file to 128 MB, then grow the filesystem to fill the new space. `resize2fs` requires a clean filesystem, so check it first:

```bash
truncate -s 128M ~/os-lab-disk/images/scratch.img
e2fsck -f ~/os-lab-disk/images/scratch.img
resize2fs ~/os-lab-disk/images/scratch.img
```

4. Confirm the filesystem is now larger - the block count should have roughly doubled:

```bash
ls -lh ~/os-lab-disk/images/scratch.img
tune2fs -l ~/os-lab-disk/images/scratch.img | grep -E 'Block count|Block size'
```

5. (Proof it still mounts and shows the new capacity)

```bash
fuse2fs ~/os-lab-disk/images/scratch.img ~/os-lab-disk/mnt
df -h ~/os-lab-disk/mnt
fusermount -u ~/os-lab-disk/mnt
```

6. Save evidence:

```bash
{
    echo "=== e2fsck (clean check) ==="
    e2fsck -f -n ~/os-lab-disk/images/scratch.img
    echo "=== size after growing to 128M ==="
    ls -lh ~/os-lab-disk/images/scratch.img
    echo "=== block count after resize2fs ==="
    tune2fs -l ~/os-lab-disk/images/scratch.img | grep -E 'Block count|Block size'
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task6_maintenance.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task6_maintenance.txt
```

> **Required Screenshot 7:** Save as `images/level6_maintenance.png` and embed it in `README.md`. It must show the `e2fsck` pass and the block count growing after `resize2fs`.

---

## Level 7 - Design Your Own Disk Tool (Capstone)

**Scenario:** *"You have copied working examples all lab. Now prove you understand storage tooling by building one diagnostic entirely yourself - you choose the question it answers, write the Bash, and explain it."*

> This is the only level with **no finished script handed to you**. You design it. Do not reuse `disk_report` - write something new.

### Step 1 - Choose a diagnostic task

Pick one small, useful tool (or invent your own):

| Idea | What the script does |
|------|----------------------|
| Inode watcher | Report `df -i` and warn if any filesystem is over an inode threshold |
| Big-file finder | Print the 10 largest files under a directory you pass in |
| Mount lister | List every current mount with type and free space, timestamped |
| Image inspector | Take an image path and print its `blkid` + `dumpe2fs -h` summary |
| Growth tracker | Append the current `du -sh` of a folder to a log so growth is visible over time |

### Step 2 - Write your script

Create `my_disktool` in `~/bin`. It **must**:

- start with the `#!/bin/bash` shebang and `set -euo pipefail`
- accept the directory or image to inspect as `$1` (with a sensible default)
- write **timestamped** output to its own log in `~/os-lab-disk/logs/`
- be made executable with `chmod +x`

```bash
nano ~/bin/my_disktool
```

```bash
#!/bin/bash
set -euo pipefail

base="$HOME/os-lab-disk"
logfile="$base/logs/my_disktool.log"
target="${1:-$HOME}"

# TODO: replace the line below with YOUR own disk diagnostic.
echo "$(date '+%Y-%m-%d %H:%M:%S') | largest under $target: $(du -ah "$target" 2>/dev/null | sort -h | tail -n 1)" >> "$logfile"
```

Test it by hand first - never trust a tool you have not run once:

```bash
chmod +x ~/bin/my_disktool
my_disktool ~/os-lab-disk/sample
cat ~/os-lab-disk/logs/my_disktool.log
```

### Step 3 - Save evidence

```bash
{
    echo "=== my disk tool ==="
    cat ~/bin/my_disktool
    echo "=== output it produced ==="
    cat ~/os-lab-disk/logs/my_disktool.log
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task7_own_tool.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task7_own_tool.txt
```

In your `README.md`, explain **in your own words**: what your tool answers, which commands it uses, and how you would schedule it (e.g., with the Lab 10 crontab) to monitor storage over time.

> **Required Screenshot 8:** Save as `images/level7_own_tool.png` and embed it in `README.md`. It must show your script and the log it produced.

---

## Level 8 - Teardown and Reset

**Scenario:** *"The drill is over. Leave nothing mounted and no stray images behind - a forgotten FUSE mount or a 128 MB image is exactly the kind of clutter that fills a real server."*

1. Make sure **nothing is still mounted** from this lab:

```bash
fusermount -u ~/os-lab-disk/mnt 2>/dev/null || true
findmnt ~/os-lab-disk/mnt || echo "mnt is clean (nothing mounted)"
```

2. Record what exists before you delete it:

```bash
{
    echo "=== images before teardown ==="
    ls -lh ~/os-lab-disk/images/
    echo "=== any lab mounts still present? ==="
    findmnt | grep -i 'os-lab-disk' || echo "(none)"
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/state_before_teardown.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/state_before_teardown.txt
```

3. Remove the practice images (keep your **scripts** and **logs** - they are part of your submission):

```bash
rm -f ~/os-lab-disk/images/sparse.img ~/os-lab-disk/images/full.img ~/os-lab-disk/images/scratch.img
ls -lh ~/os-lab-disk/images/ || echo "images folder empty"
```

> **Keep your logs.** Do **not** delete `~/os-lab-disk/logs/` - `disk_report.log` and `my_disktool.log` are evidence. Only the `.img` files are removed.

4. Confirm the system is back to a clean state:

```bash
findmnt | grep -i 'os-lab-disk' && echo "WARNING: still mounted" || echo "clean: no lab mounts remain"
df -hT
```

5. Save evidence:

```bash
{
    echo "=== state BEFORE teardown ==="
    cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/state_before_teardown.txt
    echo "=== images AFTER teardown (should be empty) ==="
    ls -lh ~/os-lab-disk/images/ 2>&1 || echo "(empty)"
    echo "=== mounts AFTER teardown (should be none) ==="
    findmnt | grep -i 'os-lab-disk' || echo "(no lab mounts remain)"
} > ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task8_teardown.txt
cat ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11/task8_teardown.txt
```

> **Required Screenshot 9:** Save as `images/level8_teardown.png` and embed it in `README.md`. It must show no lab mounts remain and the images folder is empty.

---

## Copy Scripts for Submission

```bash
cd ~/os-se-<YourStudentID>/os-lab-<YourStudentID>/lab11
mkdir -p scripts
cp ~/bin/disk_report   scripts/
cp ~/bin/my_disktool   scripts/
```

Also save a small operational README in the working folder:

```bash
cat > ~/os-lab-disk/README.md <<'EOF'
QuantumTech Storage Capacity Drill working folder

Student ID: <YourStudentID>

This folder held the virtual disk images, FUSE mount point, and the
logs/reports produced by the disk-management utility used in the
Extra Lab (Bonus). Scripts live in ~/bin. The core path used no sudo:
images were formatted with mkfs.ext4 on a file and mounted with fuse2fs.
EOF
```

---

## Lab Questions

Answer these in your `README.md`:

1. What is the difference between `df` and `du`? Give one situation where they would disagree about how much space is used.
2. From Level 2, what was the difference between `ls -lh` and `du -h` for the **sparse** image, and why? What is a sparse file?
3. Why could you run `mkfs.ext4` and `e2fsck` on your image **without `sudo`**, when formatting a real `/dev/sda1` would require root?
4. What does `fuse2fs` give you that a normal `mount` does not, and why is that useful on a shared multi-user server?
5. In Level 6 you grew the volume in two steps (`truncate` then `resize2fs`). Why are **two** steps needed, and what would happen if you ran `resize2fs` without first enlarging the image?
6. Read your `blkid` output: what is a filesystem **UUID** and why do real systems mount by UUID (in `/etc/fstab`) instead of by device name like `/dev/sdb1`?
7. What does the use% in `df` mean, and why might a filesystem refuse writes before it shows 100% (hint: reserved blocks, inodes)?
8. Describe the tool you wrote in Level 7: what question it answers, which commands it uses, and how you would schedule it to watch storage over time.

---

## Screenshot Checklist

| # | File Name | Level | What It Shows |
|:-:|-----------|:----:|---------------|
| 1 | `level0_inventory.png` | 0 | `lsblk -f` and `df -hT` storage inventory |
| 2 | `level1_usage.png` | 1 | Per-directory `du` breakdown and the top-10 consumers |
| 3 | `level2_image.png` | 2 | Sparse image: apparent size (`ls -lh`) vs real usage (`du -h`) |
| 4 | `level3_format.png` | 3 | `file` reporting ext4 and `blkid` with the `QT_SCRATCH` label |
| 5 | `level4_mount.png` | 4 | FUSE mount confirmed (`findmnt`/`df -hT`) with files written to it |
| 6 | `level5_utility.png` | 5 | `disk_report` output: mounts, top dirs, status/alert line |
| 7 | `level6_maintenance.png` | 6 | `e2fsck` pass and block count growing after `resize2fs` |
| 8 | `level7_own_tool.png` | 7 | Your own script and the log it produced |
| 9 | `level8_teardown.png` | 8 | No lab mounts remain, images folder empty |

---

## Final Submission

> **README template:** Reuse the lab README pattern from earlier labs - a header, one section per level with its screenshot embedded, the Lab Questions answered, and a note that this is the **bonus** lab.

### Required Working Tree Outside the Repo (before teardown)

```text
~/
|-- bin/
|   |-- disk_report
|   `-- my_disktool
`-- os-lab-disk/
    |-- README.md
    |-- images/
    |   |-- sparse.img
    |   |-- full.img
    |   `-- scratch.img        (removed in Level 8)
    |-- mnt/                   (mount point; empty when unmounted)
    |-- sample/
    |   |-- logs/app.log
    |   |-- data/blob.bin
    |   `-- cache/cache.txt
    `-- logs/
        |-- disk_report.log
        `-- my_disktool.log
```

### Required Submission Tree

```text
os-se-<YourStudentID>/
`-- os-lab-<YourStudentID>/
    `-- lab11/
        |-- README.md
        |-- task0_inventory.txt
        |-- task1_usage.txt
        |-- task2_image.txt
        |-- task3_format.txt
        |-- task4_mount.txt
        |-- task5_utility.txt
        |-- task6_maintenance.txt
        |-- task7_own_tool.txt
        |-- task8_teardown.txt
        |-- state_before_teardown.txt
        |-- scripts/
        |   |-- disk_report
        |   `-- my_disktool
        `-- images/
            |-- level0_inventory.png
            |-- level1_usage.png
            |-- level2_image.png
            |-- level3_format.png
            |-- level4_mount.png
            |-- level5_utility.png
            |-- level6_maintenance.png
            |-- level7_own_tool.png
            `-- level8_teardown.png
```

### Git Push

```bash
cd ~/os-se-<YourStudentID>
git add .
git commit -m "Extra Lab (Bonus): Linux disk management utilities"
git push origin main
```

---

## Grading Criteria (Bonus)

> These points are **added to your lab total as bonus**. There is no penalty for not attempting this lab.

| Criteria | Bonus Points | Description |
|----------|:---:|-------------|
| **Level 0: Storage inventory** | 2 | Captures `lsblk -f`, `findmnt`, `df -hT`, and identifies the home filesystem. |
| **Level 1: Usage analysis** | 3 | Compares `df` vs `du`, breaks usage down per directory, lists top consumers. |
| **Level 2: Create disk image** | 3 | Creates sparse and allocated images and shows apparent vs real size. |
| **Level 3: Format & inspect** | 4 | `mkfs.ext4` on the image; verifies type, UUID, label, superblock. |
| **Level 4: Mount without root** | 4 | Mounts with `fuse2fs`, writes data, confirms with `df`/`findmnt`, unmounts. |
| **Level 5: Disk utility script** | 5 | `disk_report` lists mounts, top dirs, and raises a threshold alert. |
| **Level 6: Maintenance & grow** | 4 | `e2fsck` clean check and a successful `resize2fs` after enlarging the image. |
| **Level 7: Design your own tool** | 3 | Student-authored diagnostic script with timestamped logging, explained. |
| **Level 8: Teardown** | 1 | Unmounts cleanly and removes images; no stray mounts remain. |
| **README, screenshots, answers** | 1 | Submission tree complete, screenshots embedded, questions answered. |
| **Total (Bonus)** | **30** | |

---

## Tips

- Everything destructive in this lab targets a **file** (`*.img`), never a real device. If you ever see a `/dev/...` path where the lab said `*.img`, **stop** - that would touch real hardware.
- `df` tells you how full the **filesystem** is; `du` tells you how big the **files** are. Reach for `du -h --max-depth=1 | sort -h` to find what is eating space.
- A **sparse** image (`truncate`) costs almost no real disk until you write to it; an **allocated** image (`fallocate`) reserves it all up front. `du -h` reveals the truth, `ls -lh` shows the claim.
- `mkfs.ext4 -F` is needed because the target is a plain file, not a block device. The `-F` just says "yes, I mean this file."
- Always **unmount before deleting**: `fusermount -u ~/os-lab-disk/mnt`. Deleting an image while it is still mounted leaves a stale mount.
- To grow a filesystem you must enlarge the **container first** (`truncate`), then the **filesystem** (`resize2fs`). `resize2fs` also insists the filesystem is clean, so run `e2fsck -f` first.
- Real servers mount by **UUID** (from `blkid`) in `/etc/fstab` because device names like `/dev/sdb` can change between boots; a UUID never does.
- If `fuse2fs` is unavailable, you can still do every level except the live mount - and the optional `sudo mount -o loop` path covers mounting if your instructor allows sudo.
- Run Level 8 teardown. A forgotten FUSE mount or a stray 128 MB image is exactly the clutter this drill teaches you to prevent.
```