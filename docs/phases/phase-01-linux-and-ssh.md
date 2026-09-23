# Phase 1: Linux Fundamentals and SSH

> **Goal:** Become comfortable operating a Linux server well enough to run and maintain a production application.

Linux is the foundation underneath much of modern deployment. Before working with Gunicorn, Nginx, Docker, cloud servers, or CI/CD, we need to understand the machine those tools are running on.

This phase is practical. Commands are not learned for the sake of collecting terminal trivia.

---

## What We Will Learn

* Linux filesystem and paths
* Users and groups
* File ownership
* File and directory permissions
* Processes and services
* Ports and basic networking
* Package management
* Environment variables
* `systemctl`
* `journalctl`
* CPU, memory, and disk inspection
* Firewall basics
* SSH
* SSH keys
* Remote commands and file transfer
* Root vs normal users
* Basic server hardening

---

# Progress

### Users, Groups, Ownership & Permissions

* [x] Identify the current user
* [x] Inspect groups
* [x] Understand UID and GID
* [x] Understand file ownership
* [x] Understand permission groups: owner, group, others
* [x] Understand `r`, `w`, and `x`
* [x] Read permissions from `ls -l`
* [x] Understand directory execute permission
* [x] Understand numeric permissions
* [x] Inspect metadata with `stat`
* [x] Change permissions with `chmod`
* [ ] Change file ownership with `chown`
* [ ] Practice group-based access

### Remaining Phase 1 Topics

* [ ] Processes
* [ ] Services
* [ ] Ports
* [ ] Package management
* [ ] Environment variables
* [ ] `systemctl`
* [ ] `journalctl`
* [ ] CPU, memory, and disk inspection
* [ ] Firewall basics
* [ ] SSH fundamentals
* [ ] SSH key authentication
* [ ] Remote commands
* [ ] File transfer over SSH
* [ ] Create a non-root deployment user
* [ ] Basic server hardening
* [ ] Production server practice

---

# Lesson 2: Users, Groups, Ownership, and Permissions

Linux needs to answer a basic question:

> **Who is allowed to do what?**

This becomes especially important on a production server where multiple users and processes may interact with the same system.

---

## 1. Current User

We used:

```bash
whoami
```

Result:

```text
sadik
```

This tells us which user is currently running the shell.

---

## 2. Groups

We used:

```bash
groups
```

Result:

```text
sadik wheel
```

The user belongs to:

* `sadik`
* `wheel`

Groups allow Linux to give shared permissions to multiple users.

---

## 3. User and Group IDs

We used:

```bash
id
```

Example result:

```text
uid=1000(sadik) gid=1000(sadik) groups=1000(sadik),10(wheel)
```

Important concepts:

* `UID` identifies a user.
* `GID` identifies a group.
* A user can belong to multiple groups.

---

# 4. File Ownership

We inspected files with:

```bash
ls -l
```

Example:

```text
-rw-r--r--. 1 sadik sadik 2240 README.md
```

The important ownership section is:

```text
sadik sadik
```

Meaning:

```text
owner: sadik
group: sadik
```

Linux permissions are then applied based on:

```text
owner | group | others
```

---

# 5. Reading Linux Permissions

A permission string such as:

```text
-rw-r--r--
```

can be separated into:

```text
-   rw-   r--   r--
    │     │     │
    │     │     └── others
    │     └──────── group
    └────────────── owner
```

The first character identifies the type:

```text
-   regular file
d   directory
l   symbolic link
```

---

# 6. Read, Write, Execute

Linux uses three basic permissions:

| Permission | Meaning            |
| ---------- | ------------------ |
| `r`        | read               |
| `w`        | write              |
| `x`        | execute / traverse |

For a regular file:

* `r` allows reading
* `w` allows modifying
* `x` allows executing

For a directory:

* `r` allows listing directory contents
* `w` allows creating/removing entries
* `x` allows entering/traversing the directory

That difference matters. Directory `x` does not mean "run the directory." Humans invented enough confusing terminology already.

---

# 7. Numeric Permissions

We learned that permissions can also be represented numerically:

```text
r = 4
w = 2
x = 1
```

Therefore:

```text
rw- = 4 + 2 = 6
r-- = 4
r-x = 4 + 1 = 5
rwx = 4 + 2 + 1 = 7
```

For example:

```text
-rw-r--r--
```

becomes:

```text
644
```

because:

```text
rw- = 6
r-- = 4
r-- = 4
```

A directory such as:

```text
drwxr-xr-x
```

is:

```text
755
```

---

# 8. Inspecting Directories

We used:

```bash
ls -ld .
ls -ld docs
```

This lets us inspect the directory itself instead of listing its contents.

Example:

```text
drwxr-xr-x. 1 sadik sadik ...
```

The important parts are:

```text
d        directory
rwx      owner permissions
r-x      group permissions
r-x      others permissions
```

---

# 9. Inspecting File Metadata

We used:

```bash
stat README.md
```

This showed information including:

* file size
* inode
* permissions
* UID
* GID
* ownership
* access time
* modification time
* change time

For now, the important part is using `stat` when `ls -l` does not provide enough information.

---

# 10. Practical Permissions Lab

We created a reusable lab:

```text
labs/phase-01-linux-and-ssh/
└── permissions/
    ├── private/
    │   └── private.txt
    ├── public/
    │   └── public.txt
    └── README.md
```

This lab will continue to be used as we learn more about permissions and ownership.

---

## 11. Changing Permissions with `chmod`

We changed the private file from its normal permissions:

```text
-rw-r--r--
```

to:

```bash
chmod 444 labs/phase-01-linux-and-ssh/permissions/private/private.txt
```

We then inspected it:

```bash
ls -l labs/phase-01-linux-and-ssh/permissions/private/private.txt
```

Result:

```text
-r--r--r--
```

The owner no longer had write permission.

When we attempted to edit the file in VS Code, VS Code reported that the file was read-only.

This was an important practical result:

> Linux permissions are not theoretical. They directly control what applications can do with files.

We restored the permissions with:

```bash
chmod 644 labs/phase-01-linux-and-ssh/permissions/private/private.txt
```

The file became writable again.

---

# Commands Practiced

```bash
whoami
groups
id
ls -l
ls -ld .
ls -ld docs
stat README.md
chmod 444 <file>
chmod 644 <file>
```

---

# Key Takeaways

By the end of this lesson, we understand that:

1. Linux identifies users with UIDs.
2. Users can belong to multiple groups.
3. Files and directories have owners and groups.
4. Permissions are divided into owner, group, and others.
5. `r`, `w`, and `x` have different meanings for files and directories.
6. Permissions can be represented numerically.
7. `chmod` changes permissions.
8. File permissions affect real applications such as VS Code.
9. We should practice permissions on controlled lab files before touching important system files.

---

## Practical Rule

We will continue using the same lab instead of creating disposable test files.

As new concepts are learned, the lab and this document will be updated with the commands we actually used, the results we observed, and the problems we encountered.

**Nothing gets marked complete until it has been understood and practiced.**
