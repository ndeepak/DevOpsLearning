# Multiple Schedulers in Kubernetes
## Before learning Multiple Schedulers...

Let's first answer a simple question.

**Who decides where a Pod runs?**

Suppose you execute:
```
kubectl apply -f nginx.yaml
```

Does the Pod immediately know which node it should run on?
No.

Initially, the Pod is created without being assigned to any node.

```
Pod Created
nodeName = ?
```

Some component has to decide:
> "Should this Pod go to node01 or node02 or node03?"

That component is the **Scheduler**.

This is one of the more advanced Kubernetes scheduling topics. To understand it properly, we first need to understand **how scheduling actually works internally**.

Most tutorials simply say:
> "You can run multiple schedulers."

That doesn't explain **why**, **how**, or **when**.

Let's build it from the ground up.


---

# Part 1. Why Does Kubernetes Need a Scheduler?

Recall what happens when you create a Pod.

You execute

```
kubectl apply -f nginx.yaml
```

The API Server stores the Pod in etcd.

The Pod object initially looks something like

```
Pod
------------------------
Name: nginx
Node: <empty>
Status: Pending
```

Notice something important.

There is **no node assigned**.

The Pod exists.

But Kubernetes doesn't know where to run it.

Someone must decide

```
Should this Pod run on Node1?
Node2?
Node3?
```

That "someone" is the Scheduler.

The scheduler continuously watches the API Server.

```scss
             API Server
                  |
                  |
         Watches Unscheduled Pods
                  |
            kube-scheduler
                  |
        Chooses Best Node
                  |
        Updates Pod.Spec.Node
                  |
             kubelet starts Pod
```

The scheduler **never starts containers.**

Its only job is

> Pick the best node.

Nothing more.


# Part 2. What Exactly Does the Scheduler Do?

Suppose your cluster has
```
Node1
8 CPU
16GB RAM

Node2
4 CPU
8GB RAM

Node3
16 CPU
64GB RAM
```

A Pod requests

```
resources:
  requests:
    cpu: "2"
    memory: "4Gi"
```

Scheduler begins evaluating.

Step 1
Can Node1 run it?
Yes.

Step 2
Can Node2 run it?
Yes.

Step 3
Can Node3 run it?
Yes.

Now Kubernetes scores every node.

Example
```
Node1 Score = 78

Node2 Score = 40

Node3 Score = 92
```

Highest score wins.

Pod gets assigned
```
spec:
  nodeName: node3
```

Done.


# Part 3. What If I Don't Like Kubernetes' Decision?
Imagine your company has special rules.

Example:
```
AI workloads

↓

must always run on GPU nodes

↓

unless GPU usage >80%

↓

then choose cheapest GPU

↓

unless customer is Premium

↓

then ignore GPU usage
```

Default scheduler doesn't know your business logic.

Its job is generic scheduling.

Your company may need
```
Custom Logic
```

That's where custom schedulers come in.


# Part 4. Why Multiple Schedulers?

Most beginners think

> Replace kube-scheduler.

Actually, Kubernetes allows both to exist.

Example

```
Cluster

Default Scheduler

Custom Scheduler

Finance Scheduler

GPU Scheduler

AI Scheduler
```

Each scheduler watches Pods.

But each scheduler only picks Pods that belong to it.

---

Example

Pod A

```
schedulerName: default-scheduler
```

Default scheduler schedules it.

---

Pod B

```
schedulerName: gpu-scheduler
```

GPU scheduler schedules it.

---

Pod C

```
schedulerName: ai-scheduler
```

AI scheduler schedules it.

Each scheduler ignores Pods intended for others.


# Part 5. How Does Kubernetes Know Which Scheduler to Use?
Every Pod contains
```
spec:
  schedulerName:
```

If omitted
```
schedulerName = default-scheduler
```

automatically.

Example
```
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - image: nginx
```

Equivalent to
```
spec:
  schedulerName: default-scheduler
```

# Part 6. How Does Scheduler Watch Pods?

Schedulers continuously watch the API Server.

Internally

```
Watch API
↓

Receive Event
↓

Pod Created
↓

schedulerName == me?
↓

YES
↓

Schedule
↓

NO
↓

Ignore
```

Think of it like multiple employees.
```
Employee A
Only handles HR files.

Employee B
Only handles Finance files.

Employee C
Only handles Sales files.
```

They all monitor the same inbox.

Each processes only relevant work.

Exactly the same idea.

---

# Part 7. Scheduler Configuration
Configuration tells kube-scheduler
> What is my name?

Example
```
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration

profiles:
- schedulerName: my-scheduler
```

This is not scheduling Pods.

It only tells the scheduler
```
My identity is

my-scheduler
```

Another scheduler
```
profiles:
- schedulerName: gpu-scheduler
```

Another
```
profiles:
- schedulerName: finance-scheduler
```

Each has a unique identity.

---

# Part 8. Why Must Scheduler Names Be Unique?
Imagine
```
Scheduler A

name = my-scheduler
```

and
```
Scheduler B

name = my-scheduler
```

Now Pod
```
schedulerName: my-scheduler
```

Which scheduler owns it?
Both.

Both race.

Chaos.

Therefore every scheduler must have a unique name.

---

# Part 9. Deploying Another Scheduler
A scheduler is just another program.

You can start
```
kube-scheduler
```

again.

Different configuration.
```
First Process
kube-scheduler
↓

default-scheduler
```

Second Process
```
kube-scheduler
↓

my-scheduler
```

Same executable.

Different configuration.

Different identity.

Exactly like
```
chrome --profile=Personal
chrome --profile=Office
```

Same Chrome.

Different configuration.

---

Service example
```
kube-scheduler.service
↓

ExecStart
↓

kube-scheduler
↓

--config default.yaml
```

Another service
```
my-scheduler.service
↓

kube-scheduler
↓

--config custom.yaml
```

Same binary.

Different config.

---

# Part 10. Running Scheduler Inside Kubernetes
Modern clusters don't usually run scheduler directly as Linux services.

Instead
Scheduler itself runs as a Pod.

```
Control Plane
API Server Pod
Controller Pod
Scheduler Pod
etcd Pod
```

So your custom scheduler can also be

```
Pod
Deployment
StatefulSet
```

Usually Deployment.

Example
```
containers:
- name: kube-scheduler
  image: my-custom-scheduler
```

Nothing magical.

It is just another Pod.

---

# Part 11. Why Does Scheduler Need RBAC?
Scheduler continuously reads
Pods
Nodes
PersistentVolumes
PersistentVolumeClaims
CSI storage
PriorityClasses
Leases
Events
Services
Namespaces


It also updates
```
Pod.Binding
```

or
```
spec.nodeName
```

Therefore scheduler needs permissions.

Without RBAC

Scheduler cannot
```
Read Pods

Read Nodes

Bind Pods

Create Events
```

Example
```
Forbidden

cannot list pods
```

Scheduler stops functioning.

That's why
```
ClusterRole

ClusterRoleBinding

ServiceAccount
```

are created.

---

# Part 12. Why ConfigMap?
Instead of embedding configuration into image

```
Image

↓

Contains scheduler binary only
```

Configuration stays outside

```
ConfigMap

↓

Mounted

↓

/etc/kubernetes/
```

Advantages

```
Change config

↓

Restart Pod

↓

Done
```

No rebuilding image.

---

# Part 13. Leader Election

Suppose you run

```
Scheduler Replica 1

Scheduler Replica 2

Scheduler Replica 3
```

If all three schedule Pods

```
Pod A

↓

Node1

Replica1

Replica2

Replica3
```

Three decisions.

Impossible.

Only one should be active.

Leader election solves this.

```
Replica1

Leader

Schedules Pods

Replica2

Standby

Replica3

Standby
```

If leader crashes

```
Replica2

↓

Becomes Leader
```

Scheduling continues.

---

Leader election uses

```
Lease object
```

stored in Kubernetes.

Only lease owner schedules Pods.

Everyone else waits.

---

# Part 14. Why leaderElect: false?

Example

```
leaderElection:
  leaderElect: false
```

This means

```
Only one replica exists.

No need for election.
```

If Deployment

```
replicas: 1
```

leader election is unnecessary.

If

```
replicas: 3
```

leader election should be enabled.

---

# Part 15. How Does a Pod Choose Custom Scheduler?

Pod YAML

```
apiVersion: v1
kind: Pod

metadata:
  name: nginx

spec:
  schedulerName: my-scheduler

  containers:
  - image: nginx
```

Scheduler flow

```
API Server

↓

New Pod

↓

schedulerName

↓

my-scheduler

↓

my-scheduler notices it

↓

Chooses Node

↓

Updates spec.nodeName

↓

kubelet starts container
```

---

# Part 16. What If Scheduler Doesn't Exist?

Example

```
schedulerName: abc
```

But cluster only has

```
default-scheduler

gpu-scheduler
```

No scheduler named

```
abc
```

Result

```
Pod

Status

Pending
```

Forever.

Nobody schedules it.

Checking

```
kubectl describe pod nginx
```

You'll often see events indicating that no scheduler has processed the Pod, because none matches its `schedulerName`.

---

# Part 17. How Can We Verify Which Scheduler Scheduled a Pod?

Run

```
kubectl get events -o wide
```

Output

```
SOURCE

my-custom-scheduler
```

or

```
SOURCE

default-scheduler
```

This immediately tells you who scheduled it.

---

You can also inspect the Pod:

```
kubectl describe pod nginx
```

Typical event

```
Normal  Scheduled

Successfully assigned default/nginx

by my-custom-scheduler
```

---

# Part 18. Internal Architecture

Complete flow

```
                   kubectl apply
                         |
                         |
                  API Server
                         |
                Stores Pod in etcd
                         |
                 schedulerName
                         |
        +----------------+----------------+
        |                                 |
default-scheduler                 my-scheduler
        |                                 |
Ignore if not mine               Ignore if not mine
        |                                 |
Choose Node                      Choose Node
        |                                 |
Update spec.nodeName             Update spec.nodeName
        |                                 |
          API Server updates Pod
                   |
                kubelet
                   |
             Starts Container
```

Notice that **all schedulers communicate through the API Server**. They do not talk directly to kubelets or to each other.

# Part 19. Real-World Use Cases

Large organisations often introduce custom schedulers when the default placement logic is not enough. Common examples include:

1. GPU scheduling
    - Prefer nodes with specific GPU models.
    - Reserve high-end GPUs for premium workloads.
2. AI/ML clusters
    - Place training jobs close to large datasets.
    - Balance GPU memory usage instead of only CPU and RAM.
3. Financial systems
    - Keep latency-sensitive services on dedicated hardware.
    - Avoid colocating critical workloads with batch jobs.
4. Telecom and edge computing
    - Schedule workloads on edge nodes closest to users.
    - Enforce regulatory or geographical placement rules.
5. Research and HPC
    - Implement scheduling based on licences, accelerators, or custom hardware that Kubernetes doesn't understand by default.

# Part 20. Interview Questions

**Q1. Why would you use multiple schedulers instead of modifying the default scheduler?**

Because different workloads may require different scheduling policies. Running multiple schedulers allows specialised logic for specific Pods while keeping the default scheduler for general workloads.

---

**Q2. How does Kubernetes know which scheduler should schedule a Pod?**

Using the `spec.schedulerName` field. Each scheduler watches only the Pods whose `schedulerName` matches its configured `schedulerName`.

---

**Q3. What happens if a Pod specifies a scheduler that doesn't exist?**

The Pod remains in the `Pending` state because no scheduler claims responsibility for assigning it to a node.

---

**Q4. Can two schedulers have the same name?**

No. Scheduler names must be unique. Otherwise, multiple schedulers could attempt to process the same Pods, leading to conflicts.

---

**Q5. Does a scheduler create or run containers?**

No. The scheduler only selects a node and updates the Pod's binding (`spec.nodeName`). The kubelet on the chosen node is responsible for creating and running the containers.

This topic also forms the foundation for understanding **Scheduling Framework**, **Scheduler Plugins (Filter, Score, Reserve, Permit, Bind)**, and **writing a scheduler using the Kubernetes Scheduler Framework**, which are the modern mechanisms used to customise scheduling logic without maintaining a completely separate scheduler binary. Those are the next logical topics after understanding multiple schedulers.
---

Custom scheduler

```
spec:
  schedulerName: my-scheduler
```

Now only

```
my-scheduler
```

looks at it.

---


---
# The Default Scheduler
Every Kubernetes cluster already comes with one scheduler.

Its name is:
```
default-scheduler
```

Think of it as the cluster's traffic manager.
```scss
          API Server
               │
               │
       New Pod Created
               │
               ▼
      default-scheduler
               │
               ▼
Chooses Best Node
               │
               ▼
Node01 / Node02 / Node03
```

Every normal Pod uses this scheduler automatically.

---

# What does the Default Scheduler check?

When deciding where to place a Pod, it evaluates many things:
- Available CPU
- Available memory
- Taints and tolerations
- Node affinity
- Node selectors
- Pod priority
- Resource requests
- Existing workloads

It tries to find the **best** node.

---

# Then Why Do We Need Multiple Schedulers?
Imagine a company with different kinds of applications.

```
Cluster

├── AI Workloads
├── Database
├── Finance
├── Machine Learning
├── Video Rendering
├── Batch Jobs
```

The default scheduler uses Kubernetes' built-in algorithm.

But suppose your company has a special rule.

For example:
> "AI Pods must only run on GPU nodes that currently have GPU utilization below 50%."

The default scheduler doesn't know anything about GPU utilization.

Or perhaps:
> "Financial applications must never run in the same rack."

Again, the default scheduler doesn't understand your company's business rules.

You need your own scheduler.

---

# Real-Life Analogy
Imagine a hospital.

Normally there is one receptionist.

```
Receptionist
↓

Assign patient to doctor
```

But now suppose there are special patients.

```
Heart Patients
↓

Cardiology Receptionist
```

```
Children
↓

Pediatric Receptionist
```

```
Cancer Patients
↓

Oncology Receptionist
```

Now there are multiple people assigning patients.

Each follows different rules.

Exactly the same idea applies in Kubernetes.

---

# What is a Custom Scheduler?
A custom scheduler is simply another scheduler running alongside the default scheduler.

```scss
Cluster

          API Server

               │

      ┌────────┴─────────┐

      │                  │

Default Scheduler     My Scheduler

      │                  │

Normal Pods        AI Pods
```

Each scheduler can have its own scheduling algorithm.

---

## Do Multiple Schedulers Replace the Default Scheduler?
No.

This is a common misconception.

The default scheduler continues to work.

You simply add another scheduler.

```
Before
Cluster
↓

Default Scheduler
```

After
```
Cluster
↓

Default Scheduler
↓

My Scheduler
↓

GPU Scheduler
↓

Finance Scheduler
```

They all run together.

---

# How Does a Pod Know Which Scheduler to Use?
Every Pod has a field called:
```
schedulerName
```

This field tells Kubernetes
> "Which scheduler should schedule me?"

---

## Default Behaviour
If you don't specify anything,

```
apiVersion: v1
kind: Pod

metadata:
  name: nginx

spec:
  containers:
  - image: nginx
```

Kubernetes automatically assumes
```
schedulerName: default-scheduler
```

You don't normally see it because Kubernetes fills it in implicitly.

---

## Using a Custom Scheduler
Suppose you have created a scheduler named
```
my-custom-scheduler
```

Now create a Pod.

```
apiVersion: v1
kind: Pod

metadata:
  name: nginx

spec:
  schedulerName: my-custom-scheduler

  containers:
  - name: nginx
    image: nginx
```

Now the default scheduler ignores this Pod.

Instead,
```
My Custom Scheduler
↓

Reads Pod
↓

Chooses Node
↓

Binds Pod
```

Exactly as described in the source material.

---

# Internal Workflow
Suppose the cluster has
```
Node01
Node02
Node03
```

You create
```
schedulerName: my-custom-scheduler
```

Internally
```
API Server
↓

Stores Pod
↓

schedulerName = my-custom-scheduler
```

The default scheduler checks
```
schedulerName
↓

Not Mine
↓

Ignore
```

Your scheduler checks
```
schedulerName
↓

Matches
↓

Schedule Pod
```

Only one scheduler is responsible for that Pod.

---

# Creating a Scheduler
A scheduler is configured using a `KubeSchedulerConfiguration`.

Example:
```
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration

profiles:
- schedulerName: my-scheduler
```

This configuration simply gives the scheduler its identity.

---

# Why Must Scheduler Names Be Unique?
Imagine two schedulers both named
```
my-scheduler
```

Now a Pod says
```
schedulerName: my-scheduler
```

Which scheduler should process it?
Impossible to know.

That's why every scheduler requires a unique name.

---

# Running Multiple Scheduler Processes
You can run multiple instances of the scheduler binary, each using a different configuration.

Example:
```
Scheduler Process 1
↓

Name = default-scheduler
```

```
Scheduler Process 2
↓

Name = my-scheduler
```

```
Scheduler Process 3
↓

Name = gpu-scheduler
```

Each reads only the Pods intended for it.

---

# Deploying as a Pod
Modern Kubernetes clusters usually run the scheduler itself as a Pod.

```
kube-system
├── kube-apiserver
├── kube-controller-manager
├── kube-scheduler
├── etcd
```

You can deploy your own scheduler Pod in the same namespace.

The uploaded material shows a scheduler Pod running the `kube-scheduler` binary with a custom configuration file.

---

# Deploying as a Deployment
Instead of a standalone Pod, you can package the scheduler into a container image and deploy it using a Deployment.

The general process is:
1. Build a scheduler image.
2. Create a ServiceAccount.
3. Grant the required RBAC permissions.
4. Store the scheduler configuration in a ConfigMap.
5. Deploy it as a Deployment.

This is the approach commonly used in modern Kubernetes environments.

---

# Leader Election
This is an important concept.

Suppose you run two identical copies of the same scheduler for high availability.

```
Scheduler-1
Scheduler-2
```

If both try to schedule the same Pod,

you could end up with conflicts.

Instead, Kubernetes performs **leader election**.

```
Scheduler-1
↓

Leader
```

```
Scheduler-2
↓

Standby
```

Only the leader actively schedules Pods.

If the leader crashes,

```
Scheduler-2
↓

Becomes Leader
```

This provides fault tolerance without duplicate scheduling. The uploaded lesson highlights leader election as an important configuration for HA environments.

---

# How Do You Verify Which Scheduler Scheduled a Pod?
Run:
```
kubectl get events -o wide
```

Example output:
```
Scheduled
Source
my-custom-scheduler
```

If you see
```
SOURCE
my-custom-scheduler
```

then you know your scheduler handled the Pod.

---

# If the Pod Stays Pending
Suppose you create:
```
schedulerName: my-custom-scheduler
```

but that scheduler is not running.

What happens?
```
API Server
↓

Pod Created
↓

Waiting...
↓

No Scheduler
↓

Pending
```

The Pod remains in the `Pending` state because no scheduler is available to process it.

---

# Viewing Scheduler Logs
If your custom scheduler isn't working correctly, inspect its logs:

```
kubectl logs my-custom-scheduler -n kube-system
```

This helps verify that the scheduler has started correctly and, if leader election is enabled, whether it successfully became the leader.

---

# Complete Flow
```
Pod Created
↓

schedulerName = my-custom-scheduler
↓

API Server stores Pod
↓

Default Scheduler ignores it
↓

My Scheduler notices it
↓

Checks Nodes
↓

Chooses Best Node
↓

Creates Binding
↓

Kubelet Starts Container
↓

Running
```

---

# When Would You Actually Use Multiple Schedulers?
Although most clusters use only the default scheduler, custom schedulers are useful when you need specialized placement logic, such as:

- AI/ML workloads that should consider GPU-specific metrics.
- Financial or regulated workloads with custom placement rules.
- Research environments experimenting with new scheduling algorithms.
- Multi-tenant platforms implementing organization-specific scheduling policies.

For most day-to-day Kubernetes deployments, the default scheduler is sufficient, but Kubernetes provides this extension point for advanced use cases.

---

# CKA Exam Tips
- A cluster can run **multiple schedulers simultaneously**.
- The **default scheduler** is named `default-scheduler`.
- Pods choose a scheduler using the `schedulerName` field.
- If the specified scheduler is unavailable, the Pod remains **Pending**.
- Scheduler events (`kubectl get events -o wide`) show **which scheduler** assigned the Pod.
- Leader election ensures that only **one instance** of a scheduler actively schedules Pods in a high-availability setup.