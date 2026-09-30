# Phase 1: Linux Fundamentals and SSH

> **Goal:** Operate a Linux system well enough to eventually run and maintain a production application.

Linux is the foundation underneath tools such as Gunicorn, Nginx, Docker, PostgreSQL, Redis, and Celery.

This phase focuses on understanding the machine before deploying applications on top of it.

---

## Phase Progress

### Files, Users, Ownership and Permissions

- [x] Current user with `whoami`
- [x] Groups with `groups`
- [x] UID and GID with `id`
- [x] File ownership
- [x] Owner, group, and others
- [x] `r`, `w`, and `x`
- [x] Numeric permissions
- [x] `ls -l`
- [x] `ls -ld`
- [x] `stat`
- [x] `chmod`
- [x] Symbolic permissions such as `u+w`, `u-w`, and `g+w`
- [x] Directory traversal with `x`
- [x] `chown`
- [x] Root vs normal-user ownership
- [ ] Group-based access with different users

### Processes

- [x] Understand what a process is
- [x] Understand PID
- [x] Understand process ownership
- [x] Understand parent and child processes
- [x] Understand PPID
- [x] Use `ps`
- [x] Understand `ps aux`
- [x] Understand `ps -ef`
- [x] Understand pipes with `|`
- [x] Understand `head` and `tail`
- [x] Use `top`
- [x] Understand CPU and memory columns at a basic level
- [x] Understand running and sleeping states
- [x] Understand `kill` and `SIGTERM`
- [x] Understand `kill -9` and `SIGKILL`
- [ ] Safely terminate a test process
- [ ] Inspect a real parent-child relationship

### Remaining Phase 1 Topics

- [ ] Services
- [ ] Ports
- [ ] Package management
- [ ] Environment variables
- [ ] `systemctl`
- [ ] `journalctl`
- [ ] CPU, memory, and disk inspection
- [ ] Basic networking
- [ ] Firewall
- [ ] SSH fundamentals
- [ ] SSH key authentication
- [ ] Remote commands
- [ ] File transfer
- [ ] Non-root deployment user
- [ ] Basic server hardening
- [ ] Production server lab

---

# Users, Ownership and Permissions

Linux permissions answer:

> **Who is allowed to do what?**

Files and directories have:

```text
owner
group
permissions
```

Example:

```text
-rw-r--r--  sadik sadik
```

Permission values:

```text
r = 4
w = 2
x = 1
```

Therefore:

```text
644 = rw-r--r--
755 = rwxr-xr-x
```

For files, `x` means executable.

For directories, `x` means the user can traverse or access the directory.

We tested this by removing directory execute permission and receiving a permission error.

## Changing Permissions

Numeric:

```bash
chmod 444 file
chmod 644 file
```

Symbolic:

```bash
chmod u-w file
chmod u+w file
chmod g+w file
```

## Changing Ownership

```bash
sudo chown root:root file
```

changed ownership to:

```text
root root
```

We restored it with:

```bash
sudo chown sadik:sadik file
```

A normal user could not assign the file to `root` without `sudo`.

---

# Processes

A **program** is code available to run.

A **process** is a running instance of that program.

Linux identifies each process using a:

```text
PID
```

Processes also run as Linux users, so normal file permissions still apply to them.

## Inspecting Processes

```bash
ps
```

shows a small process view for the current terminal/session.

```bash
ps aux
```

shows a broad detailed process list.

```bash
ps -ef
```

includes information useful for identifying parent and child processes.

```bash
top
```

shows process activity continuously.

## Parent and Child Processes

A process that starts another process is the parent.

The process it starts is the child.

```text
bash
└── python
```

Linux records this using:

```text
PID  = Process ID
PPID = Parent Process ID
```

The relationship is identified using:

```text
child PPID = parent PID
```

Not by assuming the smaller PID is the parent.

## Process States

Two states observed in `top`:

```text
R = running
S = sleeping/waiting
```

A sleeping process is still alive. It is waiting for work or another event.

## Stopping Processes

```bash
kill PID
```

normally sends `SIGTERM`, asking the process to terminate cleanly.

```bash
kill -9 PID
```

sends `SIGKILL`, which forces immediate termination.

`SIGKILL` should not normally be the first option.

---

# Commands Practiced

```bash
whoami
groups
id
ls -l
ls -ld
stat
chmod
chown
ps
ps aux
ps aux | head
ps aux | tail
top
```

Commands understood but still requiring practical testing:

```bash
ps -ef
kill PID
kill -9 PID
```

---

## Rule

A topic is marked complete only after it has been **understood and practiced**.

The phase documentation records what was actually learned, while the lab folders contain the practical exercises.