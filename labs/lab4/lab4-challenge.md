# Lab 4 Post-Lab Challenge: Find the Suspicious Client

## Overview

You are given a small challenge folder in your home directory. Inside it are several files, including one log file and some decoy files.

Your goal is to investigate the dataset using Ubuntu command-line tools and produce **one final result only**.

---

## Challenge Folder

Your dataset is located at:

```bash
~/lab4-challenge/
```

---

## Task

Find the final answer in this format:

```text
IP|URL|COUNT
```

Where:

* `IP` = the IP address that made the most suspicious requests
* `URL` = the URL requested by that IP with status code `403`
* `COUNT` = the total number of requests made by that IP in the log

---

## Output Requirement

Write **only one line** into this file:

```bash
~/lab4-challenge/final_answer.txt
```

Example format only:

```text
10.21.4.8|/admin/export|6
```

Do not copy this example as your answer unless it is truly the result from your own dataset.

---

## Commands Used

Document every command you used to solve the challenge, in order, inside this file:

```bash
~/lab4-challenge/commands.txt
```

Write one command per line. Include the full pipeline if you used one. For example:

```text
ls ~/lab4-challenge/
cat access.log | head -20
grep 403 access.log | awk '{print $1}' | sort | uniq -c | sort -rn
```

This file is **required** — it shows your thought process and how you arrived at the answer.

---

## Rules

* Use terminal commands only.
* Work only inside your own challenge folder.
* You may inspect files, search text, filter logs, and use pipelines.
* Do not edit the dataset files except `final_answer.txt` and `commands.txt`.
* Final grading checks the content of `final_answer.txt` and `commands.txt`.

---

## Skills You May Need

This task may require some of the following:

* `ls`
* `cat`
* `head`
* `tail`
* `grep`
* `cut`
* `awk`
* `sort`
* `uniq -c`
* pipelines using `|`
* output redirection using `>`

You do not need to use every command above.

---

## What You Submit

Your submission is complete when **both** of these files are ready:

1. **`~/lab4-challenge/final_answer.txt`** — contains your one-line answer (`IP|URL|COUNT`)
2. **`~/lab4-challenge/commands.txt`** — contains the commands you used, one per line

---

## Reminder

Each student has a different dataset.

Even if the task is the same, your final answer should come from **your own files**.
