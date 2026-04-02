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

## Rules

* Use terminal commands only.
* Work only inside your own challenge folder.
* You may inspect files, search text, filter logs, and use pipelines.
* Do not edit the dataset files except `final_answer.txt`.
* Final grading checks only the content of `final_answer.txt`.

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

Your submission is complete when this file contains the final result:

```bash
~/lab4-challenge/final_answer.txt
```

---

## Reminder

Each student has a different dataset.

Even if the task is the same, your final answer should come from **your own files**.
