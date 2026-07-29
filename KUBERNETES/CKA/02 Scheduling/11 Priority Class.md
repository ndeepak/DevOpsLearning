# Priority Classes

Priority Classes are one of those Kubernetes features that seem simple at first ("just give Pods a priority"), but once you understand **why they exist**, they become very logical.

To understand Priority Classes, we first need to understand **how the Kubernetes scheduler normally behaves**.

# Imagine You're the Kubernetes Scheduler
Suppose you have a cluster with one node.
```
Node01

CPU: 8
Memory: 16Gi
```

Several Pods are waiting to run.
```
Database
API Server
Frontend
Backup Job
Log Cleaner
```

Question:
> Which Pod should Kubernetes schedule first?

Without any extra information...

**It doesn't know.**

To Kubernetes, every Pod looks equally important.

---

# Real Life Analogy
Imagine you are a doctor in an emergency room.

Five patients arrive at the same time.
```
Patient A
Broken finger

Patient B
Heart attack

Patient C
Fever

Patient D
Small cut

Patient E
Sprained ankle
```

Should you treat them in arrival order?
No.

You treat based on **priority**.

Heart attack comes first.

Broken finger can wait.

Kubernetes has exactly the same problem.

Some Pods are much more important than others.

---

# Different Types of Workloads
Imagine a production Kubernetes cluster.

It may contain:
```
Cluster

├── Kubernetes API Server
├── etcd
├── Scheduler
├── Controller Manager
├── Database
├── Payment Service
├── Backend API
├── Frontend
├── Monitoring
├── Batch Jobs
├── Backup Jobs
└── Report Generator
```

Are all of these equally important?
Definitely not.

Let's rank them.

|Workload|Importance|
|---|---|
|API Server|Extremely Critical|
|etcd|Extremely Critical|
|Database|Critical|
|Payment Service|Critical|
|Backend API|High|
|Frontend|Medium|
|Monitoring|Medium|
|Batch Job|Low|
|Report Generator|Very Low|

If the cluster runs out of resources,

which Pods should get CPU first?
Obviously
- API Server
- Database
- Payment Service

Not
- Report Generator

This is exactly what **Priority Classes** solve.

---

# What is a Priority Class?
A Priority Class is simply
> **A label that gives Pods a numerical priority value.**

```scss
Higher number
↓
Higher importance

Lower number
↓
Lower importance
```

---

# Think of Priority Like VIP Passes
Imagine an airport.

Passengers have different boarding passes.
```scss
Economy
↓

Business
↓

First Class
↓

VIP
```

Who boards first?
VIP.

Exactly the same happens in Kubernetes.

Pods with higher priority get preference.

---

# How Kubernetes Sees It
Suppose we have four Pods.
```
Backup Job
Priority = 10
```

```
Frontend
Priority = 50
```

```
Database
Priority = 100
```

```
API Server
Priority = 1000
```

Scheduler thinks:
```
1000
↓

100
↓

50
↓

10
```

Highest goes first.

```scss
 kubectl get priorityclass
NAME                      VALUE        GLOBAL-DEFAULT   AGE   PREEMPTIONPOLICY
system-cluster-critical   2000000000   false            20d   PreemptLowerPriority
system-node-critical      2000001000   false            20d   PreemptLowerPriority
```

---

# Important Clarification
Priority **does not mean**

> This Pod always runs first.

It means
> **When Kubernetes has to make scheduling decisions, higher-priority Pods are favoured.**

If enough resources exist,
every Pod runs.

Priority only matters when resources become limited.

---

# Default Priority
Suppose you create a Pod.
```
apiVersion: v1
kind: Pod
metadata:
  name: nginx
```

No priority specified.

Kubernetes automatically assigns
```
Priority = 0
```
Every Pod without a PriorityClass gets
```
0
```

---

# Existing System Priority Classes
Run
```
kubectl get priorityclass
```

Example
```
NAME                      VALUE
system-cluster-critical   2000000000
system-node-critical      2000010000
```

These are reserved by Kubernetes.

They are used for components like
- kube-apiserver
- etcd
- scheduler
- kube-proxy

You should **not** use these values for your own applications.

---

# Creating Your Own Priority Class
Priority Classes are Kubernetes objects.

Example
```
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 100000
description: "Critical production applications"
```

Create it
```
kubectl apply -f priorityclass.yaml
```

Now Kubernetes knows
```
high-priority
↓

100000
```
# Using a Priority Class
Now create a Pod.
```
apiVersion: v1
kind: Pod
metadata:
  name: payment-service
spec:
  priorityClassName: high-priority
  containers:
  - name: payment
    image: nginx
```

Now this Pod automatically receives
```
Priority = 100000
```

---

# Example Cluster
Suppose Node01 has
```
4 CPUs
```
Pods waiting:
```
Database
Priority = 100
```

```
Payment

Priority = 80
```

```
Frontend

Priority = 40
```

```
Batch Job

Priority = 10
```

Scheduler chooses
```
Database
↓

Payment
↓

Frontend
↓

Batch Job
```

---

# What Happens When Resources Run Out?
Suppose Node01
```
CPU = 4
```

Already running
```
Batch Job

Priority = 5
```

Consumes
```
CPU = 4
```

Node is full.

Now
Database arrives.
```
Priority = 100
```

No CPU left.

What happens?
This introduces a new concept.

---

# Preemption
# What is Preemption?
Preemption means
> Remove lower-priority Pods to make room for higher-priority Pods.

Think about a VIP event.

All seats are occupied.

A government minister arrives.

Do they stand outside?
No.

Someone with a regular ticket may be asked to leave so the VIP can be seated.

That is exactly **preemption**.

# Example
Running Pod
```
Batch Job
Priority = 5
```

New Pod
```
Database
Priority = 100
```

Scheduler says
```
Database is more important.
```

Batch Job gets evicted.

Database starts.

# Visual Example
Before
```
Node01

Batch Job
Priority = 5
```

After
```
Node01

Database
Priority = 100
```

Batch Job becomes
```
Pending
```

until resources become available again.

# Preemption Policy
Every PriorityClass has a
```
preemptionPolicy
```

There are two options.

## 1. PreemptLowerPriority (Default)
```
preemptionPolicy: PreemptLowerPriority
```

Meaning
> Remove lower-priority Pods if necessary.

Example
```
Database arrives
↓

Node Full
↓

Batch Job Removed
↓

Database Starts
```

This is the default behaviour.

## 2. Never
```
preemptionPolicy: Never
```
Meaning
Even though the Pod has higher priority,

it will **not** evict anyone.
Instead
```
Database
↓

Pending
↓

Wait for resources
```

until CPU or memory becomes free naturally.

---

# Why Would We Use "Never"?
Imagine
```
Analytics Job
Priority = High
```

You want it to run before other future jobs,

but you don't want it to interrupt currently running work.

In that case,
```
preemptionPolicy: Never
```
is appropriate.

# globalDefault
Normally
Pods without a PriorityClass

receive
```
Priority = 0
```

But suppose your organisation wants every Pod to have
```
Priority = 100
```

Instead of manually assigning it,
you create
```
globalDefault: true
```

Example
```
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: default-priority
value: 100
globalDefault: true
```

Now
every Pod without a `priorityClassName`

automatically receives
```
Priority = 100
```

Only **one** PriorityClass in the cluster can have
```
globalDefault: true
```

---

# Choosing Priority Values
Kubernetes lets you use a very wide range of integers for user-defined PriorityClasses (roughly from **−2 billion** up to **+1 billion**).

The exact number doesn't matter nearly as much as their **relative order**.

A common approach is:

|Priority|Example|
|---|---|
|1,000,000|Production databases|
|500,000|Payment services|
|100,000|Backend APIs|
|10,000|Frontend applications|
|1,000|Monitoring|
|100|Batch jobs|
|10|Report generation|

The scheduler only compares the values. A Pod with `500000` has higher priority than one with `100000`.

---

# Priority vs Resource Requests
Many beginners confuse these.

They solve different problems.

## Resource Requests

Answer:
> **Can this Pod fit on the node?**

Example
```
resources:
  requests:
    cpu: "2"
```

Scheduler checks
> Does the node have 2 CPUs available?

---

## Priority
Answers
> **If multiple Pods are competing, who should go first?**

Priority **does not create resources**.

It only influences scheduling and preemption decisions.

---

# Priority vs Node Affinity
These are also different.

Node Affinity answers:
> **Where should this Pod run?**

Priority answers:
> **How important is this Pod compared to others?**

One decides **placement**.

The other decides **importance**.

---

# Real Production Example
Imagine an e-commerce company.

```
Production Cluster

├── API Server
├── etcd
├── Payment Service
├── Orders Service
├── Product Service
├── Frontend
├── Monitoring
├── Report Generator
└── Nightly Backup
```

Suggested priorities:

|Application|Priority|
|---|---|
|API Server|System Critical|
|etcd|System Critical|
|Payment Service|Very High|
|Orders Service|High|
|Product Service|High|
|Frontend|Medium|
|Monitoring|Medium|
|Report Generator|Low|
|Nightly Backup|Very Low|

If the cluster becomes full, Kubernetes prefers to keep the business-critical services running.

---

# Common Interview Questions
### 1. What is a PriorityClass?

A PriorityClass assigns a numerical priority to Pods so Kubernetes can make better scheduling and preemption decisions.
### 2. What priority does a Pod receive if none is specified?
It receives a priority value of **0**, unless a cluster-wide `globalDefault` PriorityClass has been configured.

### 3. Does a higher priority guarantee that a Pod always runs first?
No.
If resources are sufficient, all Pods can run.

Priority mainly matters when Pods compete for limited resources or during preemption.

### 4. What is preemption?
Preemption is the process where Kubernetes evicts lower-priority Pods to free resources for higher-priority Pods, when the PriorityClass allows it.

### 5. What is the difference between `PreemptLowerPriority` and `Never`?
- `PreemptLowerPriority`: Higher-priority Pods may evict lower-priority Pods.
- `Never`: Higher-priority Pods wait for resources instead of evicting other Pods.

---

# Key Takeaways
- **Priority Classes** assign a numeric importance level to Pods.
- Higher values mean **higher scheduling priority**.
- Pods without a PriorityClass receive a default priority of **0** (unless overridden by a global default).
- Priority influences **scheduling order** and **preemption** when resources are scarce.
- `PreemptLowerPriority` allows Kubernetes to evict lower-priority Pods.
- `Never` prevents eviction and makes the Pod wait.
- Priority is different from **Resource Requests**, **Node Selectors**, and **Node Affinity**—it controls **importance**, not resource size or placement.


---


```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority
value: 1000
globalDefault: false
description: "Priority class for low-priority workloads."



## Pod
apiVersion: v1
kind: Pod
metadata:
  name: high-prio-pod
spec:
  priorityClassName: high-priority
  containers:
  - name: high-priority-pod-container
    image: nginx
```

```
kubectl get pods -o custom-columns="NAME:.metadata.name,PRIORITY:.spec.priorityClassName"
```