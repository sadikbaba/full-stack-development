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
- [x] Safely terminate a test process
- [x] Inspect a real parent-child relationship

### Services and systemd

- [x] Understand program vs process vs service
- [x] Understand `systemd`
- [x] Understand `systemctl`
- [x] Understand `sshd`
- [x] Use `systemctl status`
- [x] Start and stop a service
- [x] Restart a service
- [x] Understand `enable` vs `start`
- [x] Understand `disable` vs `stop`
- [x] Use `journalctl`
- [x] Read basic `sshd` start, stop, and restart logs

### Ports and Sockets

- [x] Understand ports
- [x] Understand listening ports
- [x] Inspect sockets with `ss`
- [x] Understand TCP vs UDP at a basic level
- [x] Understand socket vs port
- [x] Understand Local Address:Port
- [x] Understand Peer Address:Port
- [x] Understand localhost (`127.0.0.1`)
- [x] Understand `0.0.0.0` binding
- [x] Identify a process and PID from `ss` output

### Remaining Phase 1 Topics

- [ ] Package management
- [ ] Environment variables
- [ ] Basic networking commands
- [ ] CPU, memory, and disk inspection
- [ ] Basic firewall concepts
- [ ] SSH practical connection
- [ ] SSH key authentication
- [ ] Remote commands
- [ ] File transfer
- [ ] Non-root deployment user
- [ ] Basic server hardening
- [ ] Production VPS lab
- [ ] Explain every open port on the VPS

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

Example:

```text
bash
└── sleep
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

We practiced this using a background `sleep` process and inspected its PID and PPID.

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

We safely practiced both using a test `sleep` process.

---

# Services and systemd

A **service** is functionality that normally runs for a long time in the background and waits to perform work.

`systemd` is the Linux system and service manager.

`systemctl` is the command used to manage and inspect `systemd`.

Example relationship:

```text
systemctl
   ↓
systemd
   ↓
sshd service
   ↓
sshd process
```

`sshd` is the SSH daemon that waits for incoming SSH connections.

## Inspecting and Managing Services

We practiced:

```bash
systemctl status sshd
sudo systemctl start sshd
sudo systemctl stop sshd
sudo systemctl restart sshd
```

`start` and `stop` affect the service now.

`enable` and `disable` affect whether the service starts automatically at boot.

We practiced:

```bash
systemctl is-enabled sshd
sudo systemctl enable sshd
sudo systemctl disable sshd
```

## Reading Service Logs

We used:

```bash
journalctl -u sshd -n 20 --no-pager
```

to inspect recent `sshd` log entries.

We observed events such as:

```text
Starting sshd.service
Server listening on port 22
Started sshd.service
Received signal 15; terminating
Stopped sshd.service
```

This showed the relationship between:

```text
systemd
service
process
logs
```

and also connected service shutdown with `SIGTERM`.

---

# Ports and Sockets

A **port** is a numbered network endpoint used to reach a specific service on a machine.

Examples:

```text
22  → SSH
80  → HTTP
443 → HTTPS
```

A **listening port** means a process is waiting for incoming network communication on that port.

## Inspecting Network Sockets

We used:

```bash
ss -tulpn
```

to inspect real socket information on Fedora.

Important fields include:

```text
protocol
state
Local Address:Port
Peer Address:Port
process
PID
```

We inspected real output from VS Code and Chrome.

Examples identified:

```text
VS Code → TCP
Chrome  → UDP
```

## TCP and UDP

TCP establishes a connection and provides reliable, ordered delivery.

UDP does not use the same connection model and does not guarantee delivery or ordering.

At this phase, the important distinction is:

```text
TCP
→ connection-oriented
→ reliable
→ ordered

UDP
→ no TCP-style connection setup
→ delivery not guaranteed
→ order not guaranteed
```

## Socket vs Port

A port is a number.

Example:

```text
39013
```

A socket is a communication endpoint used by a process.

Example:

```text
127.0.0.1:39013
```

Here:

```text
127.0.0.1 → address
39013     → port
```

## Local and Peer Address

`Local Address:Port` represents this machine's side of the socket.

`Peer Address:Port` represents the other endpoint.

For a listening socket, an entry such as:

```text
0.0.0.0:*
```

in the peer column means there is no specific peer connected yet.

## localhost

```text
127.0.0.1
```

is the IPv4 localhost address.

A service bound to:

```text
127.0.0.1:39013
```

is reachable through the local machine only.

## `0.0.0.0`

When `0.0.0.0` appears in the **local address** column:

```text
0.0.0.0:22
```

it means the socket is bound to all local IPv4 interfaces.

It does not mean the machine's real IP address is `0.0.0.0`.

The meaning depends on which column it appears in:

```text
Local Address:Port
0.0.0.0:22
→ all local IPv4 interfaces

Peer Address:Port
0.0.0.0:*
→ no specific peer for the listening socket
```

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
ps -ef
ps -f
ps aux | head
ps aux | tail
top

sleep 300 &
kill PID
kill -9 PID

systemctl status sshd
systemctl is-enabled sshd
sudo systemctl start sshd
sudo systemctl stop sshd
sudo systemctl restart sshd
sudo systemctl enable sshd
sudo systemctl disable sshd

journalctl -u sshd -n 20 --no-pager

ss -tulpn
```

---

## Rule

A topic is marked complete only after it has been **understood and practiced**.

The phase documentation records what was actually learned, while the lab folders contain the practical exercises.

---

## Current Position

Completed and practiced so far:

```text
permissions
↓
processes
↓
services and systemd
↓
service logs
↓
ports and sockets
```

Next:

```text
basic networking
```