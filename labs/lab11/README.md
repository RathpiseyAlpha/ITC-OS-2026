# OS Extra Lab (Bonus) - Linux Disk Management Utilities

> Rename this file to `README.md` inside your `lab11/` submission folder, then fill in every section.
> Replace each `![...](images/...)` line so your screenshots actually display.
> Delete these quote-block instructions before submitting.

> ⭐ **This is the optional BONUS lab.** Points here are added to your lab total; there is no penalty for skipping it.

| | |
|---|---|
| **Student Name** | <YourName> |
| **Student ID** | <YourStudentID> |
| **Linux Username** | <YourUsername> |
| **Date** | <YYYY-MM-DD> |
| **Mounted with** | `fuse2fs` (no sudo) / `sudo mount -o loop` *(circle one)* |

---

## Level 0 - Storage Inventory

What the inventory showed (which filesystem holds my home, how full it is):

`<your notes>`

![Level 0 - inventory](images/level0_inventory.png)

---

## Level 1 - Usage Analysis: `df` vs `du`

The biggest directory under my sample tree and how I found it:

`<your notes>`

![Level 1 - usage](images/level1_usage.png)

---

## Level 2 - Create a Virtual Disk Image

Apparent size (`ls -lh`) vs real usage (`du -h`) for the sparse image, and why they differ:

`<your notes>`

![Level 2 - image](images/level2_image.png)

---

## Level 3 - Format & Inspect a Filesystem

The filesystem type, label, and UUID I created (from `file` / `blkid`):

| Field | Value |
|-------|-------|
| Type | `<ext4>` |
| Label | `QT_SCRATCH` |
| UUID | `<your UUID>` |
| Block size | `<from dumpe2fs>` |

![Level 3 - format](images/level3_format.png)

---

## Level 4 - Mount Without Root (FUSE)

How I mounted the image without sudo and the files I wrote onto it:

`<your notes>`

![Level 4 - mount](images/level4_mount.png)

---

## Level 5 - Build the Disk Utility Script

What `disk_report` prints and when it raises the threshold alert:

`<your notes>`

![Level 5 - utility](images/level5_utility.png)

---

## Level 6 - Maintenance: Check & Grow

Block count before and after growing the image to 128 MB:

| | Block count |
|---|---|
| Before resize | `<value>` |
| After resize | `<value>` |

![Level 6 - maintenance](images/level6_maintenance.png)

---

## Level 7 - Design Your Own Disk Tool

**What my tool answers:** `<describe>`

**Commands it uses:** `<e.g. df -i, du, blkid>`

**How I would schedule it to watch storage over time:** `<your cron idea>`

![Level 7 - my own tool](images/level7_own_tool.png)

---

## Level 8 - Teardown and Reset

How I confirmed nothing was left mounted and removed the images:

`<your notes>`

![Level 8 - teardown](images/level8_teardown.png)

---

## Lab Questions

1. **Difference between `df` and `du`, and one case where they disagree:**
   `<answer>`

2. **`ls -lh` vs `du -h` for the sparse image - what is a sparse file?**
   `<answer>`

3. **Why could you run `mkfs.ext4` / `e2fsck` without `sudo` here, but not on a real `/dev/sda1`?**
   `<answer>`

4. **What does `fuse2fs` give you that a normal `mount` does not, and why is that useful on a shared server?**
   `<answer>`

5. **Why does growing a volume need two steps (`truncate` then `resize2fs`)? What if you skip the first?**
   `<answer>`

6. **What is a filesystem UUID, and why do real systems mount by UUID in `/etc/fstab` instead of by device name?**
   `<answer>`

7. **What does the use% in `df` mean, and why might writes fail before it reaches 100% (reserved blocks, inodes)?**
   `<answer>`

8. **Describe the tool you wrote in Level 7: the question it answers, the commands it uses, and how you would schedule it.**
   `<answer>`
