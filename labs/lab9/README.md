# OS Lab 9 Submission - The Quantum Vault Deadlock

- **Student Name:** [Your Name Here]
- **Student ID:** [Your Student ID Here]
- **Linux Username:** [Your Linux Username Here]
- **Partner Username:** [Partner Username Here]
- **My Role:** [Player A or Player B]

---

## Required Working Files Outside the Repo

Confirm these files and folders existed while you ran the lab:

- [ ] `~/bin/sync_up`
- [ ] `~/bin/sync_down`
- [ ] `~/bin/sync_timeout`
- [ ] `~/bin/teardown`
- [ ] `~/bin/cross_sync_alpha` OR `~/bin/cross_sync_beta`
- [ ] `~/os-lab-deadlock/README.md`
- [ ] `~/os-lab-deadlock/vault_alpha/README.txt`
- [ ] `~/os-lab-deadlock/vault_alpha/vault.lock`
- [ ] `~/os-lab-deadlock/vault_beta/README.txt`
- [ ] `~/os-lab-deadlock/vault_beta/vault.lock`
- [ ] `~/os-lab-deadlock/public_dr_alpha/vault.lock` OR `~/os-lab-deadlock/public_dr_beta/vault.lock`

---

## Task Output Files

Make sure all of the following files are present in your `lab9/` folder:

- [ ] `task1_vaults.txt`
- [ ] `task2_sync_scripts.txt`
- [ ] `task3_local_deadlock.txt`
- [ ] `task4_cross_deadlock.txt`
- [ ] `task5_ordering_patch.txt`
- [ ] `task6_timeout_recovery.txt`
- [ ] `task7_teardown.txt`
- [ ] `scripts/sync_up`
- [ ] `scripts/sync_down`
- [ ] `scripts/sync_timeout`
- [ ] `scripts/teardown`
- [ ] `scripts/cross_sync_alpha` OR `scripts/cross_sync_beta`

---

## Screenshots

Insert your screenshots below.

### Screenshot 1 - Level 1: Vault Workspace Setup
Show `vault_alpha`, `vault_beta`, and their `vault.lock` files.

![vault setup](images/level1_vaults.png)

---

### Screenshot 2 - Level 3: Local Deadlock
Show frozen `sync_up` and `sync_down` terminals or process evidence.

![local deadlock](images/level3_local_deadlock.png)

---

### Screenshot 3 - Level 4: Site-to-Site Deadlock
Show partner cross-site scripts frozen in circular wait.

![cross deadlock](images/level4_cross_deadlock.png)

---

### Screenshot 4 - Level 5: Global Resource Ordering Patch
Show ordered locking completing without deadlock.

![ordering patch](images/level5_ordering_patch.png)

---

### Screenshot 5 - Level 6: Timeout Recovery
Show the timeout error and nonzero exit status.

![timeout recovery](images/level6_timeout_recovery.png)

---

### Screenshot 6 - Level 7: Cleanup and Reset
Show the process check and final working tree.

![cleanup reset](images/level7_teardown.png)

---

## Deadlock Observation Table

| Level | Script A Held | Script A Waited For | Script B Held | Script B Waited For | Result |
|:----:|---------------|---------------------|---------------|---------------------|--------|
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

---

## Answers to Lab Questions

1. **What does each `vault.lock` file represent in this lab?**
   > _Your answer here_

2. **Why does `flock` require every script to lock the same shared file to coordinate correctly?**
   > _Your answer here_

3. **In the local deadlock, which resource did `sync_up` hold, and which resource did it wait for?**
   > _Your answer here_

4. **In the local deadlock, which resource did `sync_down` hold, and which resource did it wait for?**
   > _Your answer here_

5. **Which four deadlock conditions were present in Level 3?**
   > _Your answer here_

6. **How does the global Alpha-before-Beta ordering rule break circular wait?**
   > _Your answer here_

7. **Why is `flock -w` useful for recovery even though it does not prevent every deadlock?**
   > _Your answer here_

8. **Why should you check for stuck processes before finishing a deadlock lab?**
   > _Your answer here_

---

## Reflection

> _What did this lab teach you about shared resources, process synchronization, deadlock prevention, and deadlock recovery?_
