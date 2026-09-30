# Linux Processes Lab

This lab records the process-management concepts practiced during Phase 1.

## What I Learned

A **process** is a running instance of a program.

Linux gives each process a unique:

```text
PID = Process ID
```

A process can also start another process.

```text
PPID = Parent Process ID
```

If Bash starts Python:

```text
bash
└── python
```

Bash is the parent process and Python is the child process.

## Commands Learned

### `ps`

Shows processes connected to the current terminal/session.

```bash
ps
```

### `ps aux`

Shows a broad and detailed list of processes across the system.

```bash
ps aux
```

Useful information includes:

- user running the process
- PID
- CPU usage
- memory usage
- command

### `ps -ef`

Shows all processes in full format, including PID and PPID.

```bash
ps -ef
```

A process is the parent when:

```text
child PPID = parent PID
```

A smaller PID does not automatically mean it is the parent.

### `top`

Shows live process and system activity.

```bash
top
```

We observed:

- running processes
- sleeping processes
- CPU usage
- memory usage
- process owners

`R` means running.

`S` means sleeping or waiting.

Sleeping processes are still alive.

## Pipes

The pipe:

```text
|
```

passes the output of one command into another.

Example:

```bash
ps aux | head
```

`head` shows the beginning of the output.

```bash
ps aux | tail
```

`tail` shows the end.

## Stopping Processes

```bash
kill PID
```

normally sends `SIGTERM`.

This asks the process to terminate cleanly.

```bash
kill -9 PID
```

sends `SIGKILL`.

This forces the process to stop immediately and should not normally be the first choice.

We also learned not to experiment with `kill -9` on the Bash process running our current terminal.

## Current Status

- [x] Understand processes
- [x] Understand PID
- [x] Understand PPID
- [x] Understand parent and child processes
- [x] Understand `ps`
- [x] Understand `ps aux`
- [x] Understand `ps -ef`
- [x] Understand `top`
- [x] Understand basic process states
- [x] Understand `SIGTERM`
- [x] Understand `SIGKILL`
- [ ] Safely terminate a test process
- [ ] Inspect a real parent-child process relationship