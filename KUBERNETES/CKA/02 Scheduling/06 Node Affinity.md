[05 Node affinity](KUBERNETES/KCNA/3%20Scheduling/05%20Node%20affinity.md)
# Node Affinity in Kubernetes (Beginner to Advanced)

Before learning Node Affinity, let's remember what we learned previously.
We learned about **Node Selectors**.

A Pod could be scheduled like this:
```
spec:
  nodeSelector:
    size: Large
```

This means:
> "Run this Pod only on nodes whose label is `size=Large`."

Very simple.

But after working with Kubernetes for some time, people realized something.

> **Node Selectors are too simple.**

They can only perform **exact matching**.

Real production environments require much more flexibility.

That's why Kubernetes introduced **Node Affinity**.

---

# The Problem with Node Selectors

Suppose your company has these worker nodes.

|Node|Label|
|---|---|
|Worker1|size=Small|
|Worker2|size=Medium|
|Worker3|size=Large|

Imagine your application can run on either:
- Medium nodes
- Large nodes

But **not** on Small nodes.

Can Node Selector do this?
No.

Node Selector only supports:
```
nodeSelector:
  size: Large
```

or
```
nodeSelector:
  size: Medium
```

It cannot say:
```
Large OR Medium
```

It also cannot say:
```
Anything except Small
```

This is where Node Affinity becomes useful.

# Real World Analogy

Imagine you are booking a hotel.

The booking website allows filters.

You choose:
```
Location = Kathmandu
AND

Free WiFi
AND

Breakfast Included
```

Or maybe:
```
Location = Kathmandu OR Pokhara
```

Or
```
NOT Smoking Room
```

Node Affinity works exactly like these filters.

Instead of filtering hotels,

it filters Kubernetes Nodes.

---

# Another Analogy

Imagine you are hiring an employee.

Requirements:

```
Experience

>= 5 Years

AND

Knows Kubernetes

AND

Linux
```

You are not selecting one exact person.

You are describing the type of person you want.

Node Affinity works the same way.

Instead of saying:

```
Worker3
```

you say:

```
Any node

that satisfies

these conditions.
```

---

# Node Selector vs Node Affinity

Node Selector

```
nodeSelector:
  size: Large
```

Meaning

```
Exactly Large
```

---

Node Affinity
```
Large
OR
Medium

NOT Small

Has GPU

SSD Exists

Zone = us-east
```

Much more powerful.


# Before Using Node Affinity
Suppose our cluster looks like this.

```
                Kubernetes Cluster

          +------------------------+
          |     Control Plane      |
          +------------------------+

      +-----------+-----------+-----------+
      |           |           |           |
   Worker1     Worker2     Worker3
```

Labels
```
Worker1

size=Small
```

```
Worker2

size=Medium
```

```
Worker3

size=Large
```

Now let's create Pods.

# Basic Node Selector
Previously we wrote
```
spec:
  nodeSelector:
    size: Large
```

Scheduler checks
Worker1
No

Worker2
No

Worker3
Yes

Schedule.
Simple.

# Node Affinity Syntax
Now let's write the same thing using Node Affinity.

```
apiVersion: v1
kind: Pod
metadata:
  name: processor
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: size
            operator: In
            values:
            - Large
  containers:
  - name: nginx
    image: nginx
```

At first glance,
this looks much more complicated than Node Selector.

Don't worry.

We'll understand it line by line.

# Breaking It Down
## affinity
```
affinity:
```

This tells Kubernetes
> "I'm about to define scheduling preferences."

Think of it as the main section for advanced scheduling rules.

## nodeAffinity
```
nodeAffinity:
```

Affinity can apply to:
- Nodes
- Pods (Pod Affinity)
- Avoiding Pods (Pod Anti-Affinity)

Here we are talking about **Nodes**.

So we use
```
nodeAffinity
```

## requiredDuringSchedulingIgnoredDuringExecution
This long name scares beginners.

Let's split it.
```
Required

During
Scheduling

Ignored

During
Execution
```

Each word has a meaning.
### Required
Means
```
Mandatory
```

The scheduler **must** obey this rule.

If no node matches,
the Pod remains Pending.

### During Scheduling
Means
```
Only when
the Pod
is first scheduled.
```

Kubernetes checks affinity only during scheduling.

### Ignored During Execution
Suppose

Worker3
currently has
```
size=Large
```

Pod gets scheduled there.

Tomorrow,
someone changes the label.

```
size=Small
```

Will Kubernetes move the Pod?
No.

The Pod keeps running.
Because

```
Ignored During Execution
```

The rule is checked only once.

# Visual Timeline

```
Create Pod
↓

Scheduler checks affinity
↓

Pod assigned
↓

Pod starts running
↓

Node label changes
↓

Nothing happens
```

# nodeSelectorTerms
Inside Node Affinity,
you define one or more groups of matching rules.

```
nodeSelectorTerms:
```

Think of it as:
```
These are

the acceptable conditions.
```

# matchExpressions

This is where the actual filtering happens.

```
matchExpressions:
```

Each expression contains:

- key
- operator
- values

Exactly like a database query.

---

# key

Example

```
key: size
```

This refers to the node label key.

Node

```
size=Large
```

The key is

```
size
```

---

# Operator

This defines

**how** to compare the label.

There are several operators.

The most common are:
- In
- NotIn
- Exists
- DoesNotExist
- Gt
- Lt

Let's understand each.

---

# Operator: In
Example
```
matchExpressions:
- key: size
  operator: In
  values:
  - Large
```

Meaning

```
size
must be
Large
```

Worker1
```
Small
No
```

Worker2
```
Medium
No
```

Worker3
```
Large
Yes
```

---

# Multiple Values with In
Here's where Node Affinity becomes much more powerful than Node Selector.

```
matchExpressions:
- key: size
  operator: In
  values:
  - Medium
  - Large
```

Meaning

```
Medium
OR
Large
```

Worker1
```
Small
Rejected
```

Worker2
```
Medium
Accepted
```

Worker3
```
Large
Accepted
```

Node Selector cannot do this.

# Operator: NotIn
Suppose you never want Small nodes.
```
matchExpressions:
- key: size
  operator: NotIn
  values:
  - Small
```

Meaning
```
Everything
except
Small
```

Worker1
```
Small
Rejected
```

Worker2
```
Medium
Accepted
```

Worker3
```
Large
Accepted
```


# Operator: Exists
Sometimes
you don't care about the value.

You only want to know
whether a label exists.

Suppose nodes
```
Worker1
gpu=true
```

```
Worker2
gpu=false
```

```
Worker3
(no gpu label)
```

Affinity
```
matchExpressions:
- key: gpu
  operator: Exists
```

Scheduler checks
Worker1
Has gpu label
Yes

Worker2
Has gpu label
Yes

Worker3
No gpu label

Rejected

Notice,
it doesn't care whether the value is `true` or `false`. It only checks that the label key exists.

# Operator: DoesNotExist
Example
```
matchExpressions:
- key: gpu
  operator: DoesNotExist
```

Meaning
```
Choose nodes
without
gpu label
```

# Operator: Gt (Greater Than)
Useful for numeric labels.
Suppose
```
cpu=16
```

Affinity
```
matchExpressions:
- key: cpu
  operator: Gt
  values:
  - "8"
```

Meaning
```
CPU
>
8
```

# Operator: Lt (Less Than)
Example
```
matchExpressions:
- key: cpu
  operator: Lt
  values:
  - "16"
```

Only nodes with numeric label values less than 16 match.

# Preferred Scheduling

Until now we learned
```
Required
```

Now another type.

```
preferredDuringSchedulingIgnoredDuringExecution
```

Difference?

Required

```
Must satisfy.
```

Preferred

```
Try to satisfy.
If impossible,
still schedule.
```

Example
Suppose
No Large node exists.

Required
```
Pod
↓

Pending
```

Preferred

```
Pod
↓

Scheduler chooses
another node.
```

This is called a **soft rule**.

# Required vs Preferred

|Required|Preferred|
|---|---|
|Mandatory|Optional|
|Pod remains Pending if no match|Pod still runs on another node|
|Hard rule|Soft preference|


# Complete Example
Suppose
Nodes

```
worker1
size=Small
```

```
worker2
size=Medium
```

```
worker3
size=Large
```

Pod
```
apiVersion: v1
kind: Pod
metadata:
  name: analytics

spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: size
            operator: In
            values:
            - Medium
            - Large
  containers:
  - name: analytics
    image: nginx
```

Result
Worker1
No

Worker2
Yes

Worker3
Yes

Scheduler chooses one of the matching nodes based on its normal scheduling logic (resources, scoring, etc.).

# Node Affinity vs Node Selector

|Feature|Node Selector|Node Affinity|
|---|---|---|
|Exact match|Yes|Yes|
|OR conditions|No|Yes (`In`)|
|NOT conditions|No|Yes (`NotIn`)|
|Exists|No|Yes|
|Greater Than / Less Than|No|Yes (`Gt`, `Lt`)|
|Required or Preferred|No|Yes|
|Complexity|Simple|Advanced|

# Node Affinity vs Taints
This is another common source of confusion.

Suppose a node has:
```
Label
gpu=true
```

and also has:

```
Taint
gpu=true:NoSchedule
```

Your Pod contains:
```
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: gpu
          operator: In
          values:
          - "true"
```

The scheduler now knows **which node the Pod wants**.

But if the Pod **doesn't have a matching toleration**, the taint still blocks it.

To run successfully, the Pod needs **both**:

```
nodeAffinity:
  ...
```

and

```
tolerations:
- key: "gpu"
  operator: "Equal"
  value: "true"
  effect: "NoSchedule"
```

Think of it this way:
- **Node Affinity** says: "I want to go to the GPU node."
- **Toleration** says: "The GPU node allows me to enter."

Both conditions must be satisfied.

---

# Real Production Use Cases
## 1. GPU Workloads
Run AI or ML workloads only on GPU-enabled nodes.

## 2. High-Memory Applications
Ensure databases or analytics applications run on nodes with large memory.

## 3. Availability Zones
Keep workloads within specific availability zones for lower latency or regulatory requirements.

## 4. SSD Storage
Run I/O-intensive applications only on nodes with SSD storage.

## 5. Compliance
Schedule sensitive workloads only on nodes dedicated to regulated environments.


# Best Practices
- Use **Node Selectors** for simple exact-match requirements.
- Use **Node Affinity** when you need more expressive scheduling rules.
- Use `requiredDuringSchedulingIgnoredDuringExecution` for workloads that **must** run on specific nodes.
- Use `preferredDuringSchedulingIgnoredDuringExecution` when you have a preference but still want Pods to run if the preferred nodes are unavailable.
- Combine **Node Affinity** with **Taints and Tolerations** to both attract the correct workloads and protect specialized nodes from unwanted Pods.


# Key Takeaways
- **Node Affinity** is an advanced version of Node Selectors.
- It schedules Pods based on **labels assigned to nodes**.
- `requiredDuringSchedulingIgnoredDuringExecution` creates a **mandatory** scheduling rule.
- `preferredDuringSchedulingIgnoredDuringExecution` creates a **best-effort preference**.
- Node Affinity supports powerful operators such as **In**, **NotIn**, **Exists**, **DoesNotExist**, **Gt**, and **Lt**.
- Affinity rules are evaluated **only during scheduling**. By default, changes to node labels after a Pod is running do not cause the Pod to move.
- In production, Node Affinity is commonly combined with **Taints and Tolerations** to implement sophisticated scheduling strategies while protecting specialized infrastructure.