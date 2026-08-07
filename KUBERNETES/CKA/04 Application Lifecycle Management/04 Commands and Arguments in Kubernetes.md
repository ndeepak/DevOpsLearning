# Commands and Arguments in Kubernetes (CKA + CKS)

This is one of the most confusing Kubernetes topics because there are **three different layers** involved:
1. Dockerfile (`ENTRYPOINT` and `CMD`)
2. Docker (`docker run`)
3. Kubernetes (`command` and `args`)

Most people memorize:
> command = ENTRYPOINT

> args = CMD

While that is technically correct, it doesn't explain **why**.

To understand Kubernetes, we must first understand what Kubernetes actually does.
# The Big Picture
Suppose you execute:
```
kubectl apply -f pod.yaml
```

Does Kubernetes execute your application directly?
No.

The flow is:
```
kubectl apply
        │
        ▼
API Server
        │
        ▼
Scheduler
        │
        ▼
Node
        │
        ▼
kubelet
        │
        ▼
Container Runtime
(containerd / CRI-O)
        │
        ▼
Runs Container
```

Notice something important.

Kubernetes **does not run containers itself.**

The **container runtime** (containerd, CRI-O) does.

Therefore Kubernetes must tell the runtime
> "Here is the command you should execute."

This is exactly where `command` and `args` come into the picture.

---
# Review: Docker Behavior
Suppose our Dockerfile is
```
FROM ubuntu

ENTRYPOINT ["sleep"]

CMD ["5"]
```

When we run
```
docker run ubuntu-sleeper
```

Docker internally executes
```
sleep 5
```

because
```
ENTRYPOINT
+
CMD

↓
sleep 5
```

Now suppose
```
docker run ubuntu-sleeper 10
```

Docker executes
```
sleep 10
```
because runtime arguments replace CMD.

---
# How Kubernetes Starts Containers
Suppose we create this Pod.
```
apiVersion: v1
kind: Pod
metadata:
  name: sleeper
spec:
  containers:
  - name: sleeper
    image: ubuntu-sleeper
```

What happens?

The image contains
```
ENTRYPOINT ["sleep"]
CMD ["5"]
```

Kubernetes does **not** specify any command.

Therefore the runtime simply uses the image defaults.

Result
```
sleep 5
```

Visualization
```
Docker Image
ENTRYPOINT = sleep
CMD = 5
        │
        ▼
Kubernetes
(no command)
(no args)
        │
        ▼
Runtime executes
sleep 5
```

---

# Kubernetes Doesn't Care About Dockerfile
This is a very important statement.

Many beginners think Kubernetes reads Dockerfiles.

It doesn't.
The Dockerfile is already converted into an image.

Kubernetes only receives the image metadata.

Example
```
ubuntu-sleeper
↓
Image Metadata

ENTRYPOINT
sleep

CMD
5
```

Kubernetes only decides

Should I keep these?
Should I replace them?

---

# The args Field
Suppose our Pod is
```
apiVersion: v1
kind: Pod

metadata:
  name: sleeper

spec:
  containers:
  - name: sleeper
    image: ubuntu-sleeper
    args: ["10"]
```

Many students ask

"What exactly does args do?"

Let's understand.

The image already has
```
ENTRYPOINT ["sleep"]
CMD ["5"]
```

Kubernetes says
"I don't want CMD."
"I want a different argument."

So internally
```
ENTRYPOINT
sleep

CMD
5

↓
Replace CMD
↓
10
```

Result
```
sleep 10
```

Visualization
```
Docker Image
ENTRYPOINT
sleep

CMD
5
        │
        ▼
Kubernetes args
10
        │
        ▼
Runtime
sleep 10
```

Notice
ENTRYPOINT never changed.

Only CMD changed.

---

# Another Example
Dockerfile
```
FROM ubuntu
ENTRYPOINT ["ping"]
CMD ["localhost"]
```

Normally
```
docker run image
```
executes
```
ping localhost
```

Now Kubernetes
```
containers:
- image: ping-image
  args:
  - google.com
```

Result
```
ping google.com
```

Only the destination changed.

The executable remains
```
ping
```

---

# The command Field
Now suppose
```
containers:
- image: ubuntu-sleeper
  command:
  - sleep2.0
```

What happens?
Image
```
ENTRYPOINT ["sleep"]
CMD ["5"]
```

Kubernetes says
Ignore ENTRYPOINT.

Use
```
sleep2.0
```
instead.

Visualization
```
Image
ENTRYPOINT
sleep
↓
Ignored
↓
Kubernetes command
sleep2.0
```

Result
```
sleep2.0 5
```

Notice something.

The CMD still exists.

Only ENTRYPOINT changed.

---

# command + args Together
Suppose
```
containers:
- image: ubuntu-sleeper
  command:
  - sleep2.0
  args:
  - "20"
```

Image
```
ENTRYPOINT ["sleep"]
CMD ["5"]
```

Everything gets replaced.

Runtime becomes
```
sleep2.0 20
```

Visualization
```
ENTRYPOINT
sleep

↓
sleep2.0

CMD
5
↓
20
↓

sleep2.0 20
```

---

# The Mapping
Docker
```
ENTRYPOINT ["sleep"]
CMD ["5"]
```

Docker command
```
docker run image 10
```

Result
```
sleep 10
```

Equivalent Kubernetes
```
containers:
- image: image
  args:
  - "10"
```
Exactly identical.

---

Docker
```
docker run \
--entrypoint sleep2.0 \
image \
10
```

Equivalent Kubernetes
```
containers:
- image: image
  command:
  - sleep2.0
  args:
  - "10"
```

Exactly the same behavior.

---
# What Happens Internally?
Suppose
```
containers:
- image: ubuntu-sleeper
  command:
  - sleep
  args:
  - "30"
```

Internally Kubernetes creates something similar to
```
Executable
sleep

Arguments
30
```
Then sends this request to containerd
```
Create Container

Executable
sleep

Arguments
30
```

The runtime executes
```
sleep 30
```

Notice
The runtime doesn't know
- Dockerfile
- YAML
- Kubernetes

It simply receives
```
Executable
+
Arguments
```

---

# Multiple Arguments
Example
Dockerfile
```
ENTRYPOINT ["ping"]
```

Kubernetes
```
containers:
- image: ping-image
  args:
  - "-c"
  - "5"
  - "google.com"
```

Runtime executes
```
ping -c 5 google.com
```
Exactly like Linux.

---
# Example with Python
Dockerfile
```
ENTRYPOINT ["python3"]
```

Kubernetes
```
containers:
- image: python-image
  args:
  - app.py
  - --port
  - "8080"
```

Runtime executes
```
python3 app.py --port 8080
```

---

# Example with Java
Dockerfile
```
ENTRYPOINT ["java"]
```

Kubernetes
```
containers:
- image: java-image
  args:
  - -jar
  - app.jar
```

Result
```
java -jar app.jar
```

---

# What if There Is No ENTRYPOINT?
Suppose Dockerfile
```
FROM ubuntu
CMD ["sleep","5"]
```

Kubernetes
```
containers:
- image: ubuntu
  args:
  - "10"
```

Now things become interesting.

There is no ENTRYPOINT.

The image command is actually the CMD itself (`sleep 5`).

When you specify only `args`, Kubernetes replaces the image's default arguments. Depending on how the image was built, this may not produce the result you expect because there is no fixed executable defined by an ENTRYPOINT.

This is one reason why many production images define both `ENTRYPOINT` and `CMD`.

---

# Common Mistake
Many students think
```
command:
- sleep
- "10"
```

means
```
command = sleep
args = 10
```

Wrong.

Actually
```
command:
- sleep
- "10"
```

means
```
Executable
sleep

Argument
10
```

Everything is inside **command**.

Equivalent Linux command
```
sleep 10
```

No args field involved.

Although valid, it's less flexible than separating the executable and its arguments.

A cleaner version is
```
command:
- sleep
args:
- "10"
```

because now only the arguments can change without replacing the executable.

---

# Why Are command and args Arrays?
Notice
```
command:
- sleep

args:
- "10"
```

Instead of
```
command: sleep 10
```

Why?
Because Kubernetes does **not** invoke a shell by default.

It executes the process directly using an argument vector (similar to the Linux `execve()` system call).

For example,
```
command:
- ping

args:
- -c
- "4"
- google.com
```

becomes
```
argv[0] = ping
argv[1] = -c
argv[2] = 4
argv[3] = google.com
```

This avoids shell parsing issues, quoting problems, and command injection.

---

# Visual Summary
## Image Only
```
ENTRYPOINT ["sleep"]

CMD ["5"]
```

Result
```
sleep 5
```

---

## Image + args
```
args:
- "10"
```

Result
```
sleep 10
```

---

## Image + command
```
command:
- sleep2.0
```

Result
```
sleep2.0 5
```

---

## Image + command + args
```
command:
- sleep2.0

args:
- "20"
```

Result
```
sleep2.0 20
```

---

# Docker vs Kubernetes Mapping

|Docker Concept|Kubernetes Field|Effect|
|---|---|---|
|`ENTRYPOINT`|`command`|Replaces the image's executable|
|`CMD`|`args`|Replaces or supplies the executable's default arguments|
|`docker run image`|Pod with no `command` or `args`|Uses image defaults|
|`docker run image 10`|`args: ["10"]`|Replaces the image's CMD arguments|
|`docker run --entrypoint sleep2.0 image 10`|`command: ["sleep2.0"]`, `args: ["10"]`|Replaces both the executable and its arguments|

---

# CKA Exam Tips

1. Remember the execution order:

```
Docker Image
   │
   ├── ENTRYPOINT
   └── CMD
          │
          ▼
Kubernetes
   │
   ├── command (overrides ENTRYPOINT)
   └── args (overrides CMD)
          │
          ▼
Container Runtime
          │
          ▼
Linux Process
```

2. `command` and `args` are arrays because Kubernetes executes the program directly, not through a shell.
3. If you omit both `command` and `args`, the image's `ENTRYPOINT` and `CMD` are used unchanged.
4. If you specify only `args`, Kubernetes keeps the image's executable (`ENTRYPOINT`) and replaces only the default arguments (`CMD`).
5. If you specify `command`, Kubernetes replaces the image's executable. If you also specify `args`, those become the arguments passed to the new executable.

These concepts are heavily tested in CKA because many troubleshooting questions require determining exactly **which process** is actually running inside a container based on the image metadata and the Pod specification.