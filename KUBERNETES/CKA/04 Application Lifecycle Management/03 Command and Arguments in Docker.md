# Command and Arguments in Docker

The key idea is this:
> **A Docker container is nothing more than a Linux process running in an isolated environment.**

Everything else (`CMD`, `ENTRYPOINT`, `docker run`, Kubernetes `command` and `args`) revolves around **what process Docker starts**.

We'll build this understanding from the Linux process level.

---

# Part 1: What actually is a Docker container?
Most beginners imagine Docker like this:
```
Docker Container
├── Ubuntu OS
├── Bash
├── Files
├── Network
└── Applications
```

Not exactly.

Internally it is closer to this:
```scss
Host Linux Kernel
        │
        │
  Namespaces + Cgroups
        │
        ▼
+----------------------+
| Container            |
|                      |
| Root Filesystem      |
| Environment          |
|                      |
| Process PID 1        |
+----------------------+
```

Notice something important.

A container **must have a process**.

Without a running process,
the container dies.

Think of the container as a shell around a process.

---

# A Container Lives as Long as Its Main Process Lives
Imagine you run
```
docker run nginx
```

Internally
```
Container
PID 1
↓
nginx
```

The nginx process keeps running forever.

Therefore
```
Container = Running
```

Now imagine
```
docker run ubuntu
```
What process starts?
Let's investigate.

---

# Part 2: What does `docker run ubuntu` actually do?
When you execute
```
docker run ubuntu
```

Docker performs several steps.
```
1. Find Image
↓

2. Create Writable Layer
↓

3. Create Container
↓

4. Start PID 1
↓

5. Wait until PID 1 exits
```

Everything depends on Step 4.

Docker must know

**Which command should I execute?**
That answer comes from the Docker image itself.

---
# Every Docker Image Has Metadata
An image is not just files.

It also contains metadata.

Example
```
ubuntu image
Filesystem
+

Environment Variables
+

Working Directory
+

Entrypoint
+

CMD
```

These last two are extremely important.
```
ENTRYPOINT

CMD
```

---

# Let's Inspect Ubuntu
Run
```
docker image inspect ubuntu
```

You'll see something similar to
```
"Config": {
    "Cmd": [
        "/bin/bash"
    ]
}
```

or depending on the version
```
"Cmd": ["bash"]
```

This means
Docker automatically runs
```
bash
```
inside the container.

So internally
```
docker run ubuntu
```

becomes
```
docker run ubuntu bash
```

---

# Why does Ubuntu immediately exit?
Because Bash is just a shell.

Imagine you SSH into Linux.
```
login
↓

bash starts
↓

You type exit
↓

bash ends
```
The shell terminates.

Exactly the same happens.

Since there is
- no interactive terminal
- no command to execute

bash exits immediately.

When PID 1 exits
Docker says
```
Main process ended.
↓

Container finished.
↓

Container stopped.
```

Therefore
```
docker ps
```
shows nothing.

But
```
docker ps -a
```

shows
```
Exited (0)
```

---
# Why does nginx not exit?
The nginx image has
```
CMD ["nginx","-g","daemon off;"]
```

Notice
```
daemon off
```

Normally nginx becomes a background service.

Docker containers do **not** like background services.

Docker wants the process in the foreground.

So nginx never exits.

```
Container
↓

PID 1
↓

nginx
↓

Still Running
↓

Container Running
```

---

# Part 3
## What is CMD?
CMD means
> Default command to execute when the container starts.

Example
```
FROM ubuntu
CMD ["sleep","5"]
```

When someone runs
```
docker run ubuntu-sleeper
```

Docker actually runs
```
sleep 5
```

Visualization
```
Image
CMD
↓

sleep 5
↓

Container Starts
↓

sleep 5
↓

5 seconds
↓

Exit
↓

Container Stops
```

---

# What is `docker run ubuntu sleep 5`?
This is probably the most asked Docker question.

Suppose image contains
```
CMD ["bash"]
```

You execute
```
docker run ubuntu sleep 5
```

Docker says
"I don't care about the image CMD anymore."

Instead
Use
```
sleep 5
```

instead of
```
bash
```

Internally
Instead of
```
bash
```

Docker runs
```
sleep 5
```

Timeline
```
Container
↓

sleep
↓

5 seconds
↓

Exit
↓

Container exits
```

After five seconds
```
docker ps
```
Nothing.

Because sleep finished.

---

# CMD can always be overridden
Dockerfile
```
FROM ubuntu
CMD ["sleep","5"]
```

Run normally
```
docker run ubuntu-sleeper
```

Result
```
sleep 5
```

Run with another command
```
docker run ubuntu-sleeper sleep 20
```

Result
```
sleep 20
```

Run
```
docker run ubuntu-sleeper bash
```

Result
```
bash
```

Everything after image name replaces CMD.

Rule
```
docker run IMAGE SOMETHING
↓

Replace CMD
↓

Run SOMETHING
```

---

# Part 4
## What is ENTRYPOINT?
ENTRYPOINT changes the behavior completely.
Suppose
```
FROM ubuntu
ENTRYPOINT ["sleep"]
```

Notice
There is **no CMD**.

Now Docker always executes
```
sleep
```

When you run
```
docker run ubuntu-sleeper
```

Docker executes
```
sleep
```

Problem
sleep needs a number.

Linux returns
```
sleep: missing operand
```

because
```
sleep WHAT?
```
No argument supplied.

---

Now run
```
docker run ubuntu-sleeper 10
```

Docker combines them.
```
ENTRYPOINT
sleep
+

Runtime Argument
10
↓

sleep 10
```

Notice
The runtime value
did NOT replace
ENTRYPOINT.

It became an argument.

---

Visualization
```
ENTRYPOINT
sleep
Runtime
10
↓
sleep 10
```

---

# Part 5
## ENTRYPOINT + CMD together
This is the most common pattern.
Dockerfile
```
FROM ubuntu
ENTRYPOINT ["sleep"]
CMD ["5"]
```

Many students memorize this.

Instead understand the formula.

Docker internally creates
```
ENTRYPOINT
+
CMD
```

Meaning
```
sleep
+
5
↓
sleep 5
```

Run
```
docker run ubuntu-sleeper
```

Result
```
sleep 5
```

Now run
```
docker run ubuntu-sleeper 20
```

What happens?
Does Docker replace everything?

No.

Only CMD gets replaced.

ENTRYPOINT stays.

Result
```
sleep 20
```

Visualization
```
ENTRYPOINT
sleep

CMD
5

↓
sleep 5

Runtime
20
↓

sleep 20
```

---

# Difference between CMD and ENTRYPOINT
Imagine the image
```
ENTRYPOINT ["sleep"]
CMD ["5"]
```

Run
```
docker run image
```

Result
```
sleep 5
```

Run
```
docker run image 10
```

Result
```
sleep 10
```

Now compare with
```
CMD ["sleep","5"]
```

Run
```
docker run image
```

Result
```
sleep 5
```

Run
```
docker run image 10
```

Result
```
10
```

Docker tries to execute
```
10
```
which obviously fails because "10" is not a program.

This is the biggest behavioral difference.

---

# Part 6
## What does `docker build` actually do?
Suppose
```
FROM ubuntu
CMD ["sleep","5"]
```

Run
```
docker build -t ubuntu-sleeper .
```

Docker performs
```
Read Dockerfile
↓

FROM ubuntu
↓

Download base image
↓

Execute each instruction
↓

Create image layers
↓

Save metadata
↓

Create Image
```
Notice

Nothing runs permanently.

Docker is only **building an image**.

The container does not exist yet.

Visualization
```
Dockerfile
↓

docker build
↓

Image
↓

docker run
↓

Container
↓

Running Process
```

This distinction is fundamental:
- `docker build` creates an **image** (a template).
- `docker run` creates a **container** (a running instance of that template).

# Complete Relationship
```
Dockerfile
    │
    ├── FROM
    ├── RUN
    ├── COPY
    ├── ENV
    ├── WORKDIR
    ├── ENTRYPOINT
    └── CMD
           │
           ▼
docker build
           │
           ▼
Docker Image
           │
           ▼
docker run
           │
           ▼
Container
           │
           ▼
PID 1 Process
```
# CMD vs ENTRYPOINT (Summary)

|Feature|CMD|ENTRYPOINT|
|---|---|---|
|Purpose|Default command or arguments|Main executable that always runs|
|Can be overridden by `docker run <image> ...`?|Yes, completely replaced|No, runtime values are appended as arguments|
|Best use|Provide sensible defaults|Define the fixed executable|
|Typical example|`CMD ["5"]`|`ENTRYPOINT ["sleep"]`|
|Combined behavior|Used as default arguments to ENTRYPOINT|Executes with CMD/runtime arguments|

---

# Why This Matters for Kubernetes
The reason Docker teaches `CMD` and `ENTRYPOINT` is because Kubernetes maps directly to them.

In a Pod specification:
- `command:` overrides Docker's **ENTRYPOINT**.
- `args:` overrides Docker's **CMD** (or provides arguments to the entrypoint).

Understanding Docker's process model makes Kubernetes `command` and `args` much easier to understand. That is the natural next topic after mastering `CMD` and `ENTRYPOINT`.