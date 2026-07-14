# Node Selectors
Before learning Node Selectors, let's understand **why Kubernetes introduced them**.
Many beginners confuse **Node Selectors** with **Taints and Tolerations** because both influence scheduling.
The easiest way to remember them is:
- **Taints** → Keep unwanted Pods **away** from a node.
- **Node Selectors** → Tell Kubernetes **where a Pod wants to run**.

Think of it like this:
- **Node Selector = Attraction**
- **Taint = Repulsion**

In production, they are often used **together**.

# The Problem
Suppose your cluster has three worker nodes.
```
                Kubernetes Cluster

              +-------------------+
              |  Control Plane    |
              +-------------------+

       +-----------+-----------+-----------+
       |           |           |           |
    Worker1     Worker2     Worker3
```

Now suppose:

|Node|Hardware|
|---|---|
|Worker1|2 CPU, 4 GB RAM|
|Worker2|2 CPU, 4 GB RAM|
|Worker3|32 CPU, 128 GB RAM|

Worker3 is a powerful machine.

Your company runs two kinds of applications.
## Normal Web Applications
These don't require much CPU.
```
Frontend
Backend
API
```

## Data Processing Application
This application performs
- Machine Learning
- Video Processing
- Image Rendering
- Large Data Analysis

It needs lots of CPU and memory.
Clearly,
you want this application to run on
```
Worker3
```

But Kubernetes doesn't know that.

Without any scheduling rules,

the scheduler may do this.

```
Worker1

Data Processing Pod
```

Now your heavy workload is running on a tiny server.

Performance becomes terrible.


# How Can We Solve This?
We need some way to tell Kubernetes:
> "This Pod should only run on powerful machines."

The solution is
# Node Selectors

# Real World Analogy

Imagine three classrooms.
```
Room A

Capacity: 20 Students
```

```
Room B

Capacity: 20 Students
```

```
Room C

Capacity: 300 Students
```

Now suppose there is a conference with 250 people.

You obviously want
```
Room C
```

You wouldn't randomly assign it to Room A.

Node Selectors do exactly this.

They help Kubernetes choose the appropriate node.

# Another Analogy
Imagine booking a hotel.

You search

```
Swimming Pool

Free WiFi

Breakfast Included
```

The booking website only shows hotels matching your preferences.

Node Selectors work the same way.

The Pod specifies

```
I want these properties.
```

Scheduler searches for nodes matching those properties.

# How Does Kubernetes Identify Nodes?
Every Kubernetes Node can have
**Labels**.
Just like Pods have labels,
Nodes also have labels.
Example
```
Worker1
size=Small
```

```
Worker2
size=Small
```

```
Worker3
size=Large
```

Notice
The nodes are now categorized.

# Step 1 — Add Labels to Nodes
First, label your nodes.

Command
```
kubectl label nodes worker1 size=Small
```

Output
```
node/worker1 labeled
```

Worker2
```
kubectl label nodes worker2 size=Small
```

Worker3
```
kubectl label nodes worker3 size=Large
```

Now check labels.
```
kubectl get nodes --show-labels
```

Example output
```
NAME       STATUS   LABELS
worker1    Ready    size=Small
worker2    Ready    size=Small
worker3    Ready    size=Large
```

Now Kubernetes understands which node is large.

# Step 2 — Create a Pod
Normal Pod
```
apiVersion: v1
kind: Pod
metadata:
  name: processor
spec:
  containers:
  - name: processor
    image: nginx
```

Notice
There is no scheduling rule.
The scheduler may place it anywhere.
# Step 3 — Add a Node Selector
Now modify the Pod.
```
apiVersion: v1
kind: Pod
metadata:
  name: processor
spec:
  nodeSelector:
    size: Large
  containers:
  - name: processor
    image: nginx
```

Look carefully.

```
nodeSelector:
  size: Large
```

means
> "I only want a node whose label is `size=Large`."

# Scheduler Workflow
Scheduler receives the Pod.
```
Pod
↓
Looking for
size=Large
```

Checks Worker1

```
size=Small
↓
Rejected
```

Checks Worker2
```
size=Small
↓
Rejected
```

Checks Worker3
```
size=Large
↓
Perfect
↓
Schedule Here
```

The Pod runs on Worker3.

# Complete Example
## Label the Node
```
kubectl label nodes worker3 size=Large
```
## Verify
```
kubectl get nodes --show-labels
```
Output
```
worker3
size=Large
```

## Create Pod
```
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  nodeSelector:
    size: Large
  containers:
  - name: nginx
    image: nginx
```

Deploy
```
kubectl apply -f pod.yaml
```

Check where it runs.
```
kubectl get pods -o wide
```

Output
```
NAME
myapp

NODE
worker3
```

Perfect.
# What Happens Internally?
When you create the Pod,
the Scheduler sees
```
nodeSelector:
  size: Large
```

It searches every node.
```
Worker1
size=Small
```

No match.
```
Worker2
size=Small
```

No match.
```
Worker3
size=Large
```

Match found.

Scheduler assigns the Pod.
# What If No Node Matches?
Suppose
Every node
```
size=Small
```

Your Pod requests
```
nodeSelector:
  size: Large
```

Scheduler checks.

Worker1
No.

Worker2
No.

Worker3
No.

Result
```
Pod
STATUS
Pending
```

Because Kubernetes cannot find a matching node.

You can verify the reason by describing the Pod:

```
kubectl describe pod myapp
```

You may see events similar to:

```
0/3 nodes are available:
3 node(s) didn't match Pod's node selector.
```

---

# Multiple Labels
A node can have many labels.

Example
```
Worker3
size=Large
zone=us-east
disk=ssd
gpu=true
```

Your Pod may require
```
nodeSelector:
  size: Large
  disk: ssd
```

This means
```
size=Large
AND
disk=ssd
```

Both conditions must match.
# Important Rule
Node Selectors only support

**Exact matching**.

Example
```
nodeSelector:
  size: Large
```

means
```
size
must equal
Large
```

You cannot say
```
Large OR Medium
```

You also cannot say
```
Anything except Small
```

These are limitations of node selectors.

# Why Node Selectors Have Limitations
Suppose you want
```
Large
OR
Medium
```

Node Selector cannot express that.

Suppose you want

```
NOT Small
```

Impossible.

Suppose you want

```
SSD
AND
GPU
AND
Zone A
```

Some combinations become difficult or impossible with basic node selectors.

For these advanced scheduling requirements, Kubernetes provides **Node Affinity**, which supports operators such as `In`, `NotIn`, `Exists`, and `DoesNotExist`. We'll study Node Affinity after mastering Node Selectors.

---

# Node Selector vs Taints
This is another common interview topic.

Suppose
Worker3

```
size=Large
```

Pod
```
nodeSelector:
  size: Large
```

This tells Kubernetes

```
I WANT

Large node.
```

Now suppose Worker3 is also tainted.

```
special=true:NoSchedule
```

The Pod has

```
No toleration.
```

Will it run?

No.

Why?

The Pod found the correct node.

But the node rejected it.

---

Now add a toleration.

```
tolerations:

- key: "special"
  operator: "Equal"
  value: "true"
  effect: "NoSchedule"
```

Now the Pod

- Wants the node (Node Selector)
- Is allowed on the node (Toleration)

Perfect.

This is the most common production design.

---

# Production Example

Suppose your company has

```
GPU Server
```

Node label

```
gpu=true
```

Node taint

```
gpu=true:NoSchedule
```

AI Pod

```
apiVersion: v1
kind: Pod

metadata:
  name: ai-model

spec:

  nodeSelector:

    gpu: "true"

  tolerations:

  - key: "gpu"
    operator: "Equal"
    value: "true"
    effect: "NoSchedule"

  containers:

  - name: model
    image: tensorflow/tensorflow:latest
```

What happens?

1. The `nodeSelector` tells the scheduler to consider only nodes labeled `gpu=true`.
2. The taint on the GPU node blocks ordinary Pods.
3. The Pod's toleration allows it to be scheduled onto the tainted GPU node.

This ensures that only GPU workloads run on expensive GPU hardware.

---

# Common Mistakes

## Mistake 1

Adding a node selector without labeling the node.

```
nodeSelector:

  size: Large
```

But no node has

```
size=Large
```

Result

```
Pending
```

Always verify node labels first.

---

## Mistake 2

Assuming Node Selector overrides taints.

It does not.

If the selected node has a taint,

the Pod still needs the correct toleration.

---

## Mistake 3

Using Node Selector for complex scheduling.

If you need conditions like:

- Large **or** Medium
- Not Small
- Region A **or** Region B

Use **Node Affinity**, not Node Selectors.

---

# Commands You'll Use Frequently

View node labels:

```
kubectl get nodes --show-labels
```

Add a label:

```
kubectl label nodes worker3 size=Large
```

Update a label:

```
kubectl label nodes worker3 size=Medium --overwrite
```

Remove a label:

```
kubectl label nodes worker3 size-
```

Describe a node:

```
kubectl describe node worker3
```

---

# Node Selector vs Node Affinity

|Feature|Node Selector|Node Affinity|
|---|---|---|
|Exact match|Yes|Yes|
|OR conditions|No|Yes|
|NOT conditions|No|Yes|
|Complex expressions|No|Yes|
|Simplicity|Very simple|More flexible|
|Best for|Basic scheduling|Advanced scheduling|

---

# Node Selector vs Taints

|Feature|Node Selector|Taints|
|---|---|---|
|Applied to|Pod|Node|
|Works using|Node labels|Node taints|
|Purpose|Attract Pods to matching nodes|Repel unwanted Pods|
|Forces scheduling|Requires matching labels|No|
|Commonly combined|Yes|Yes|

---

# Key Takeaways

- **Node Selectors** allow a Pod to request nodes with specific labels.
- Before using a node selector, the target node must already have the required label.
- The scheduler compares the Pod's `nodeSelector` with the labels on every node and schedules the Pod only on matching nodes.
- If no node matches the requested labels, the Pod remains in the **Pending** state.
- Node Selectors support only **exact key-value matching** and cannot express complex conditions.
- For advanced scheduling rules such as **OR**, **NOT**, or more expressive matching, use **Node Affinity**.
- In production, **Node Selectors** are often combined with **Taints and Tolerations**: labels attract the correct workloads, while taints keep unrelated workloads away.

---
