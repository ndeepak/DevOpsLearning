# Scheduling Section Introduction
What Scheduling is?

1. Manual Scheduling : Understand how to manually schedule pods to specific nodes.
2. Labels and Selectors: Learn how to use labels and selectors to manage and target specific groups of pods.
3. Resource Requests and Limits: See how resource constraints affect scheduling decisions.
4. Daemon Sets: Discover how to run a copy of a pod on each node in your cluster.
5. Multiple Schedulers:  Explore configuration strategies for running multiple schedulers within a cluster.
6. Scheduler Events: Learn how to monitor and troubleshoot scheduler events for optimal performance.

---


# What is Scheduling?

Scheduling is the process of selecting the **most appropriate worker node** on which a newly created Pod should run.

When you create a Pod, you do **not** usually specify the node where it should run. Instead, Kubernetes automatically decides the best node based on many factors.

For example:

```
kubectl apply -f nginx-pod.yaml
```

Suppose your cluster has three worker nodes.

```
                Control Plane
              +----------------+
              | API Server     |
              | Scheduler      |
              +-------+--------+
                      |
     -------------------------------------
     |                 |                 |
+---------+      +---------+      +---------+
| Worker1 |      | Worker2 |      | Worker3 |
+---------+      +---------+      +---------+
```

After the Pod is created:

1. API Server stores the Pod object.
2. Scheduler notices there is a Pod without a node assignment.
3. Scheduler evaluates all worker nodes.
4. Scheduler chooses the best node.
5. Scheduler assigns the Pod to that node.
6. Kubelet on that node starts the container.
---

# What Does the Scheduler Actually Do?
Many beginners think:
> "The scheduler starts the Pod."

This is **not true**.

The scheduler **only decides where the Pod should run**.

The actual execution is done by the kubelet.

Think of the scheduler like a travel planner.

```
You want to travel.

Travel Planner:
"You should go to City A."

Driver:
Actually drives you there.
```

Similarly,
```
Scheduler:
"Pod should run on Worker Node 2."

Kubelet:
Downloads image
Creates container
Starts Pod
```

---

# How Scheduling Works Internally
Imagine a new Pod is created.
```
kubectl apply -f pod.yaml
```
The API Server stores:
```
Pod:
  Name: nginx
  Node: <empty>
```

Notice that the **Node field is empty**.

The Scheduler continuously watches the API Server.

It sees:
```
NodeName = null
```

It now starts searching for a suitable node.

It checks:
- Available CPU
- Available Memory
- Node health
- Node labels
- Taints
- Affinity rules
- Resource requests
- Policies
- Constraints

After selecting a node:
```
Pod:
  Name: nginx
  Node: worker-2
```
The scheduler updates the Pod specification.

The kubelet running on `worker-2` notices:

> "A Pod has been assigned to me."

It then:
- Pulls image
- Creates container
- Starts Pod
- Reports status

---

# Scheduler Workflow
```
Create Pod
      │
      ▼
API Server stores Pod
      │
      ▼
Scheduler detects Pod
(NodeName is empty)
      │
      ▼
Collect information about nodes
      │
      ▼
Evaluate every node
      │
      ▼
Choose best node
      │
      ▼
Assign Pod to node
      │
      ▼
Kubelet starts Pod
      │
      ▼
Container Running
```

---

# Factors the Scheduler Considers
The scheduler does not randomly pick a node.

It evaluates many factors.

## 1. Available CPU

Suppose:
```
Worker1

CPU Total : 4 Core
CPU Used  : 3.8 Core

Available:
0.2 Core
```

Pod requires
```
1 CPU
```

Worker1 cannot host it.

---

## 2. Available Memory
Suppose
```
Worker2

Memory:
16 GB

Used:
15 GB

Available:
1 GB
```

Pod requests
```
4 GB
```

Scheduler skips Worker2.

---

## 3. Node Conditions
Scheduler checks whether a node is healthy.

Examples:
```
Ready
```

or
```
NotReady
```

Pods are generally scheduled only on Ready nodes.

---

## 4. Labels and Selectors
Suppose nodes have labels.
```
Worker1

disk=ssd
```

```
Worker2

disk=hdd
```

Pod requests

```
nodeSelector:

disk=ssd
```

Scheduler selects Worker1.

---

## 5. Taints and Tolerations
Suppose
```
Worker3

NoSchedule
```

Pods without the required toleration cannot run there.

---

## 6. Affinity Rules
Pods may request
```
Run close to another Pod.
```

or
```
Do not run on same node.
```

Scheduler respects these rules.

---

## 7. Resource Requests
Suppose
```
Pod

requests:
   cpu: 2
   memory: 4Gi
```

Scheduler only considers nodes with sufficient available resources.

---

# Scheduler is Intelligent
Imagine three nodes.
```
Worker1

CPU Free:
3 Core

Memory Free:
8 GB
```

```
Worker2

CPU Free:
0.5 Core

Memory Free:
10 GB
```

```
Worker3

CPU Free:
4 Core

Memory Free:
2 GB
```

Pod requires

```
CPU:
2

Memory:
4 GB
```

Which nodes qualify?

Worker1

```
CPU ✔
Memory ✔
```

Worker2

```
CPU ✖
```

Worker3

```
Memory ✖
```

Only Worker1 satisfies both requirements.

The scheduler assigns the Pod to Worker1.

---

# Is the Scheduler Always Perfect?

The scheduler attempts to find the **best feasible node**, not necessarily the "perfect" node.

It follows a two-phase process:

## Phase 1: Filtering
Remove nodes that cannot run the Pod.

Example:
```
Worker1
Not enough CPU
```
Discard.

```
Worker2
Wrong label
```
Discard.

```
Worker3
Ready
Enough resources
Correct label
```
Keep.

## Phase 2: Scoring
If multiple nodes remain, Kubernetes scores them.

Example:
```
Worker1
Score = 75
```

```
Worker2
Score = 90
```

```
Worker3
Score = 82
```

Highest score wins.

# What Happens If No Node Can Run the Pod?
Suppose every worker node is full.

```
Worker1
CPU Full
```

```
Worker2
Memory Full
```

```
Worker3
Not Ready
```

Scheduler cannot assign the Pod.

The Pod remains
```
Pending
```

Example:
```
kubectl get pods
NAME      READY   STATUS
nginx     0/1     Pending
```

Describing the Pod will usually show scheduling events such as insufficient CPU, insufficient memory, node affinity conflicts, or taint-related issues.

# Scheduling vs Kubelet
This is one of the most common interview questions.

|Scheduler|Kubelet|
|---|---|
|Chooses the node|Runs the Pod|
|Makes scheduling decisions|Creates containers|
|Watches unscheduled Pods|Watches Pods assigned to its node|
|Runs on the control plane|Runs on every worker node|
|Never starts containers|Starts and monitors containers|

---

# Scheduling in Real Production Environments
In production, scheduling decisions become more sophisticated. Common requirements include:

- Database Pods should run only on high-memory nodes.
- GPU workloads should run only on GPU-enabled nodes.
- Monitoring agents should run on every node.
- Critical applications should avoid sharing a node with each other.
- Certain workloads should run in specific availability zones or regions.
- High-priority Pods should be scheduled before lower-priority ones.

Kubernetes provides features such as **labels**, **node selectors**, **resource requests**, **taints and tolerations**, **affinity rules**, **priority classes**, and **multiple schedulers** to satisfy these requirements.

---

# Topics Covered in This Scheduling Section

Over the next lessons, we'll build up scheduling knowledge step by step:

## 1. Manual Scheduling

Learn how to bypass the scheduler and assign Pods directly to specific nodes using the `nodeName` field, and understand when this approach is appropriate.

## 2. Labels and Selectors

Use labels to organize Kubernetes objects and selectors to target specific Pods or nodes for scheduling and management.

## 3. Resource Requests and Limits

Understand how CPU and memory requests influence scheduling decisions, and how limits affect runtime resource usage.

## 4. DaemonSets

Learn how to ensure exactly one Pod (or one per eligible node) runs on every node, which is ideal for log collectors, monitoring agents, and networking components.

## 5. Multiple Schedulers

Explore scenarios where a cluster uses more than one scheduler, allowing specialized scheduling policies for different workloads.

## 6. Scheduler Events

Learn how to inspect scheduler events and diagnose why Pods are Pending or why they were scheduled to a particular node.

---

# Key Takeaways

- Scheduling is the process of selecting the most suitable node for a Pod.
- The Kubernetes Scheduler **does not run Pods**; it only assigns them to nodes.
- The **kubelet** on the selected node is responsible for pulling images, creating containers, and keeping Pods running.
- Scheduling decisions consider node health, available resources, labels, taints, affinity rules, and many other constraints.
- Scheduling generally follows a **filtering** phase (remove ineligible nodes) followed by a **scoring** phase (rank the remaining nodes).
- If no node satisfies the Pod's requirements, the Pod remains in the **Pending** state until the cluster can accommodate it.
- Understanding scheduling is essential before learning advanced topics such as node selectors, taints and tolerations, affinity/anti-affinity, DaemonSets, and custom schedulers.