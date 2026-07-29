# Resource Requirements in Kubernetes 
This is one of the **most important topics in Kubernetes** because **every Pod needs CPU and Memory to run**.

If you don't understand Resource Requests and Limits, you will eventually face problems like:
- Pods stuck in **Pending**
- Applications becoming slow
- One application consuming all server resources
- Pods getting **OOMKilled**
- Cluster instability

By the end of this lesson, you'll understand:
- How Kubernetes schedules Pods based on resources
- Resource Requests
- Resource Limits
- CPU vs Memory behaviour
- OOMKilled
- The four request/limit scenarios
- Which scenario is best
- LimitRanges
- ResourceQuotas
- Production best practices

---

# Before Learning Resource Requests
Let's first understand something about a Kubernetes cluster.

Suppose we have this cluster.
```scss
                    Kubernetes Cluster

               +----------------------+
               |    Control Plane     |
               +----------------------+

        +------------+------------+------------+
        |            |            |            |
      Worker1      Worker2      Worker3
```

Each worker node is simply a Linux machine.

Every machine has limited resources.

Example:

|Node|CPU|Memory|
|---|---|---|
|Worker1|4 CPU|8 GB|
|Worker2|8 CPU|16 GB|
|Worker3|2 CPU|4 GB|

Unlike cloud storage, CPU and RAM are **not unlimited**.

Once they're used, they're gone until something frees them.

---

# Think of a Node Like a Hotel
Imagine a hotel.

The hotel has:
- 100 rooms

Once all rooms are occupied,
no new guests can stay.

Exactly the same happens with Kubernetes.

A node has:
```
8 CPUs
16 GB RAM
```

Once these resources are fully allocated,

new Pods cannot be scheduled there.


# Another Analogy — Pizza
Imagine one pizza.
```
8 slices
```

Four friends come.

Friend A
Needs
```
2 slices
```

Friend B
Needs
```
3 slices
```

Friend C
Needs
```
2 slices
```

Already used
```
7 slices
```

Friend D
Needs
```
2 slices
```

Can he eat?
No.

Only
```
1 slice
```
is available.

Exactly what Kubernetes does.

---

# What Does the Scheduler Check?
When you create a Pod,
the Scheduler does **not** randomly pick a node.

It checks:
- CPU
- Memory
- Taints
- Affinity
- Node Selector
- Resource Requests
- Other scheduling constraints

Today we're focusing on **Resources**.

---

# Example
Suppose Worker1 has
```
CPU
4 Core
```

Memory
```
8 GB
```

Already running Pods consume
```
CPU
3 Core
```

Memory
```
6 GB
```

Remaining
```
CPU
1 Core
```

Memory
```
2 GB
```

Now a new Pod requests
```
CPU
2 Core
```

Memory
```
4 GB
```

Can Kubernetes schedule it?
No.

Worker1 doesn't have enough resources.

The scheduler checks Worker2.

If Worker2 has enough resources,
the Pod runs there.

---

# If No Node Has Enough Resources
Suppose every node is full.

Your Pod requests
```
CPU
4 Core
```

Memory
```
8 GB
```

No node satisfies the request.

Result
```
STATUS
Pending
```

The Pod is **not broken**.

It is simply waiting.

---

# How Do We Troubleshoot?
Always describe the Pod.

```
kubectl describe pod myapp
```

Near the bottom you'll see Events.

Example
```
Warning  FailedScheduling
0/3 nodes are available
Insufficient cpu
```

or
```
Insufficient memory
```

This is one of the most common troubleshooting commands in Kubernetes.

---

# What are Resource Requests?
This is the most important concept.

A **Resource Request** is the **minimum amount of resources a container needs**.

Think of it as a reservation.

Imagine booking a hotel.

You say
> "I need one room."

The hotel reserves one room.

Similarly,
a Pod tells Kubernetes

```
I need

2 CPU

4 GB RAM
```

Scheduler now searches for a node that can guarantee these resources.

---

# Pod Without Requests
```
apiVersion: v1
kind: Pod

metadata:
  name: nginx

spec:
  containers:
  - name: nginx
    image: nginx
```

Notice

No resources.

Scheduler doesn't know how much CPU or memory the Pod needs.

It assumes no explicit reservation.

---

# Pod With Requests
```
apiVersion: v1
kind: Pod

metadata:
  name: nginx

spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      requests:
        cpu: "1"
        memory: "1Gi"
```

Now Kubernetes knows
This container requires
```
CPU
1 Core
```

Memory
```
1 GiB
```

The Pod will only be scheduled on a node that has at least these available resources.

---

# Understanding CPU Values
CPU is measured in **cores**.
```
1 CPU
```

means
- 1 AWS vCPU
- 1 Azure vCPU
- 1 Google Cloud vCPU
- 1 logical CPU (hyper-thread) on many virtualized systems

You can also request fractional CPUs.
```
cpu: "0.5"
```

means

Half a CPU.

Usually written as
```
cpu: "500m"
```

The **m** stands for **millicpu**.
```scss
1000m
=
1 CPU
```

Examples

|Value|Meaning|
|---|---|
|100m|0.1 CPU|
|250m|0.25 CPU|
|500m|0.5 CPU|
|1000m|1 CPU|
|2000m|2 CPU|

Production deployments commonly use `m` because it avoids decimal notation.

---

# Understanding Memory
Memory units
```
memory: "512Mi"
```

means
512 Mebibytes.

Other examples
```
memory: "1Gi"
```

1 Gibibyte.

Common units

|Unit|Approximate Size|
|---|---|
|Mi|Mebibyte (2²⁰ bytes)|
|Gi|Gibibyte (2³⁰ bytes)|

Kubernetes also accepts SI units like `M` and `G`, but `Mi` and `Gi` are the most common because they use binary units.

---

# What are Resource Limits?
Requests reserve resources.

Limits cap how much a container can use.

Think of a mobile data plan.

You buy
```
10 GB
```

Even if you want
```
100 GB
```

you cannot exceed your plan.

A limit works the same way.

---

Example
```
resources:
  requests:
    cpu: "1"
    memory: "1Gi"
  limits:
    cpu: "2"
    memory: "2Gi"
```

Meaning

Guaranteed
```
1 CPU
1 Gi Memory
```

Maximum allowed
```
2 CPU
2 Gi Memory
```

The container may use anything between those values if resources are available.

---

# Requests vs Limits
Imagine a restaurant.

You reserve a table for four people.

That reservation is your **request**.

The restaurant also has a fire safety rule:

Maximum six people at that table.

That's the **limit**.

You are guaranteed four seats.

You can never exceed six.

---

# CPU Limit Behaviour
Suppose
```
limits:
  cpu: "2"
```

Application suddenly wants
```
5 CPU
```

Can it use them?
No.

Linux cgroups throttle the container.

It slows down.

The container **keeps running**.

This behaviour is called **CPU throttling**.

---

# Memory Limit Behaviour
Suppose
```
limits:
  memory: "2Gi"
```

Application suddenly uses
```
3 Gi
```

Can Kubernetes throttle memory?
No.

Memory cannot be throttled the same way CPU can.

Instead,
the Linux kernel's **Out Of Memory (OOM) killer** terminates the container.

The Pod may restart depending on its restart policy.

---

# OOMKilled
This is one of the most common Kubernetes problems.

Suppose
Limit
```
2 Gi
```

Application grows.

Eventually
```
2.5 Gi
```

Kernel says

Not enough memory.

Container terminated.

You may see

```
kubectl get pods
```

Output
```
NAME
api-server
STATUS
OOMKilled
```

or after a restart:

```
STATUS
Running
RESTARTS
5
```

Describe the Pod:

```
kubectl describe pod api-server
```

Events or container status often show:

```
Reason: OOMKilled
```

This usually means the application needs more memory or has a memory leak.

---

# The Four Resource Scenarios
This is one of the most important interview topics.

## Scenario 1
No Requests
No Limits
```
resources:
```

Nothing defined.

Behaviour
- No guaranteed CPU
- No guaranteed memory
- No usage limit

The container may consume all available resources, potentially starving other workloads.

Production?
Not recommended.

## Scenario 2
No Requests
Limits Only
```
resources:
  limits:
    cpu: "1"
    memory: "1Gi"
```

Kubernetes automatically sets:
```
Request = Limit
```

So effectively:

|Request|Limit|
|---|---|
|1 CPU|1 CPU|
|1Gi|1Gi|

The Pod is guaranteed exactly those resources and cannot burst beyond them.

Good?

Acceptable for simple workloads, but can be restrictive for applications with varying demand.

## Scenario 3
Requests and Limits
```
resources:
  requests:
    cpu: "1"
    memory: "1Gi"
  limits:
    cpu: "2"
    memory: "2Gi"
```

Guaranteed
```
1 CPU
```

Can burst up to
```
2 CPU
```

Guaranteed
```
1 Gi
```

Maximum
```
2 Gi
```

This is the most common configuration in production because it balances guarantees with flexibility.

## Scenario 4
Requests Only
```
resources:
  requests:
    cpu: "1"
    memory: "1Gi"
```

Guaranteed
```
1 CPU
1 Gi
```

No upper limit.

If the node has spare capacity, the container can use more.

Risk

One application can consume excessive CPU or memory and affect neighbouring workloads.

Useful for carefully controlled environments but often paired with monitoring.

# Which Scenario is Best?

|Scenario|Recommended?|Why|
|---|---|---|
|No Requests, No Limits|❌ No|Unpredictable and can starve other Pods|
|Limits Only|⚠ Sometimes|Guaranteed resources, but no bursting beyond the limit|
|Requests + Limits|✅ Best for most production workloads|Balanced guarantees and controlled bursting|
|Requests Only|✅ Good for some workloads|Guarantees minimum resources while allowing unlimited growth if appropriate|

There is **no single best answer for every workload**.

Modern Kubernetes guidance often recommends:

- **Requests** should almost always be set.
- **Limits** depend on the workload. CPU limits are sometimes omitted for latency-sensitive applications to avoid throttling, while memory limits are commonly set to prevent a single container from exhausting node memory.

---

# LimitRanges
What if developers forget to specify resources?
Namespace administrators can enforce defaults.

Example
```
apiVersion: v1
kind: LimitRange
metadata:
  name: cpu-limit
spec:
  limits:
  - type: Container
    default:
      cpu: "500m"
    defaultRequest:
      cpu: "250m"
    max:
      cpu: "1"
    min:
      cpu: "100m"
```

Meaning:
- Default CPU limit = 500m
- Default CPU request = 250m
- Minimum allowed = 100m
- Maximum allowed = 1 CPU

If a developer creates a Pod without specifying CPU values, Kubernetes applies these defaults within that namespace.

LimitRanges affect **newly created or updated Pods**, not existing running Pods.

---

# ResourceQuotas
LimitRange controls **individual containers**.

ResourceQuota controls the **entire namespace**.

Example
Development namespace

Maximum
```
20 CPU
40 Gi Memory
```

No matter how many Pods are created,

the namespace cannot exceed those totals.

Example
```
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dev-quota
spec:
  hard:
    requests.cpu: "4"
    requests.memory: "4Gi"
    limits.cpu: "10"
    limits.memory: "10Gi"
```

Meaning:
- Total requested CPU across all Pods ≤ 4 CPUs
- Total requested memory ≤ 4 GiB
- Total CPU limits ≤ 10 CPUs
- Total memory limits ≤ 10 GiB

This is especially useful in **multi-team** or **multi-tenant** clusters.

# LimitRange vs ResourceQuota

|Feature|LimitRange|ResourceQuota|
|---|---|---|
|Scope|Individual container/Pod defaults and constraints|Entire namespace|
|Purpose|Default values and min/max validation|Restrict total resource consumption|
|Used By|Namespace administrators|Namespace administrators|


# Real Production Example
Imagine your company has three namespaces:
```
development
```

```
testing
```

```
production
```

Development team accidentally creates:
```
100 Pods
```

Without quotas,
they could consume most of the cluster.

With a ResourceQuota,
their namespace stops creating new Pods once the quota is reached, protecting the rest of the cluster.

# Visual Summary
```scss
                Kubernetes Resources

        Node
     +--------------------------+
     | CPU: 8                   |
     | Memory: 16Gi             |
     +--------------------------+
              |
              |
     -----------------------------
     |            |              |
   Pod A        Pod B         Pod C

 Requests reserve resources.
 Limits cap maximum usage.
 Scheduler uses requests to place Pods.
 CPU over limit -> throttled.
 Memory over limit -> OOMKilled.
```

---

# Key Takeaways
- Every Kubernetes node has **finite CPU and memory**.
- The scheduler uses **resource requests** to decide where a Pod can be placed.
- If no node has enough requested resources available, the Pod remains **Pending**.
- **Requests** represent the minimum guaranteed resources a container needs.
- **Limits** define the maximum resources a container is allowed to use.
- **CPU** can be throttled when it exceeds its limit.
- **Memory cannot be throttled**. Exceeding the memory limit results in an **OOMKilled** container.
- The most common production configuration is to define **both requests and limits**, though CPU limits may be omitted for certain performance-sensitive applications.
- **LimitRanges** provide default and minimum/maximum resource settings within a namespace.
- **ResourceQuotas** control the total amount of resources that all Pods in a namespace can consume.
- When troubleshooting scheduling problems, start with:

```
kubectl describe pod <pod-name>
```

It often reveals whether the issue is insufficient CPU, insufficient memory, quota violations, or another scheduling constraint.



---
Labs Commands

```bash
kubectl get pods

kubectl describe pod rabbit

kubectl delete pod rabbit

kubectl get pods

kubectl describe pod elephant

kubectl get pod elephant -o yaml > my-elephant-pod.yaml
%% memory to 20Mi %%

kubectl replace --force -f my-elephant-pod.yaml
```