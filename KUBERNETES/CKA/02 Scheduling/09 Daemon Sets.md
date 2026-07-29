# DaemonSets in Kubernetes 

DaemonSets are one of the easiest Kubernetes objects to understand once you know **ReplicaSets** and **Deployments**.

Most beginners think:
> "A DaemonSet is just another way of creating Pods."

That's not quite true.

A DaemonSet has a **very specific purpose**:
> **Run exactly one copy of a Pod on every node.**

That's it.

Once you understand this single idea, everything else becomes much easier.

---

# Before Learning DaemonSets
Let's quickly compare what you've already learned.

## Pod
Creates one Pod.
```
Pod
    nginx
```

## ReplicaSet
Maintains a specified number of Pods.

Example:
```
replicas: 3
```

Result:
```
ReplicaSet
Node1        nginx
Node2        nginx
Node3        nginx
```

If one Pod dies,
ReplicaSet creates another one.

Its job is **maintaining the desired number of Pods**, not deciding where each one runs.

## Deployment
Deployment manages ReplicaSets.

It provides:
- Rolling updates
- Rollbacks
- Scaling
- Version management

```
Deployment
      │
      ▼
 ReplicaSet
      │
      ▼
    3 Pods
```

Still,
the Deployment only cares about the **number of Pods**, not "one Pod per node."

---

# Now Imagine This Situation
Suppose you have a cluster.
```scss
             Kubernetes Cluster

      +---------+---------+---------+
      |         |         |         |
    Node1     Node2     Node3
```

Now your company wants to install:
- A monitoring agent
- A log collector
- A network plugin

Question:
How many copies should run?
Maybe two?
Maybe three?
No.

The requirement is:
> **Every node must have exactly one copy.**

Because every node needs monitoring.

Every node generates logs.

Every node needs networking.

# Why ReplicaSet Cannot Solve This
Suppose you create:
```
replicas: 3
```

Scheduler may place Pods like this.

```
Node1
Monitoring Agent
```

```
Node2
Monitoring Agent
```

```
Node3
Monitoring Agent
```

Looks good.

But imagine a new node is added.

```
Node4
```

ReplicaSet still says
```
replicas: 3
```
So Node4 gets **nothing**.

Nobody is monitoring Node4.

This is a problem.

---

# DaemonSet Solves This
Instead of saying
> I want 3 Pods

DaemonSet says
> I want **one Pod on every node**.

Now the cluster looks like this.
```
Node1
Monitoring Agent
```

```
Node2
Monitoring Agent
```

```
Node3
Monitoring Agent
```

Add a new node.
```
Node4
```

Immediately

DaemonSet creates another Monitoring Agent.

```
Node4
Monitoring Agent
```

No manual work.

---

# Remove a Node
Suppose Node2 crashes.

```
Node2
(Removed)
```

DaemonSet automatically removes the Pod associated with that node.

You don't need to clean anything up.

---

# The Rule of DaemonSet
Think of this sentence.
> **One node = One Pod**

Not
> One cluster = One Pod

Not
> Three replicas

Instead
```
Every Node
↓
Exactly One Pod
```

---

# A School Analogy
Imagine a school.

Every classroom needs:
- One CCTV camera
- One fire alarm
- One attendance machine

If the school builds another classroom,

what happens?

Do you manually remember to install them?

No.

The rule is:
> Every classroom gets one.

DaemonSet works exactly like that.

Replace:
Classroom
with
Node

Replace:
CCTV
with
Monitoring Agent

That's DaemonSet.

---

# Real Production Example
Suppose you install Prometheus Node Exporter.

What does Node Exporter do?
It collects:
- CPU usage
- Memory usage
- Disk usage
- Network statistics

Question:
Should it run on only one node?
No.

It needs to collect metrics from every node.

So Kubernetes creates
```
Node1
Node Exporter
```

```
Node2
Node Exporter
```

```
Node3
Node Exporter
```

Exactly one on each node.

---

# Another Example — Log Collection

Every node produces logs.

Applications write logs locally.

You install Fluentd or Fluent Bit.

Should only one machine collect logs?
No.

Each node has different logs.

So every node runs one Fluentd Pod.
```
Node1
Fluentd
```

```
Node2
Fluentd
```

```
Node3
Fluentd
```

Each Pod collects logs only from its own node.

---

# Another Example — kube-proxy
Every worker node needs kube-proxy.

Without kube-proxy,
Services cannot correctly route traffic.

Therefore,
Kubernetes installs one kube-proxy Pod per node.

```
Node1
kube-proxy
```

```
Node2
kube-proxy
```

```
Node3
kube-proxy
```

This is why kube-proxy is deployed as a DaemonSet.

---

# Another Example — CNI Plugins
Networking plugins such as:
- Calico
- Weave Net
- Cilium

must configure networking on every node.

Therefore,
they also use DaemonSets.

---

# DaemonSet YAML
It looks almost identical to a ReplicaSet.

```
apiVersion: apps/v1
kind: DaemonSet

metadata:
  name: monitoring-daemon

spec:
  selector:
    matchLabels:
      app: monitoring-agent

  template:
    metadata:
      labels:
        app: monitoring-agent

    spec:
      containers:
      - name: monitoring-agent
        image: monitoring-agent
```

Notice something.

There is **no** `replicas` field.

ReplicaSet
```
replicas: 5
```

DaemonSet
```
# No replicas
```

Why?
Because Kubernetes calculates the number automatically.

If there are
```
5 Nodes
```

Then
```
5 Pods
```

If there are
```
20 Nodes
```

Then
```
20 Pods
```

---

# Creating a DaemonSet
Save the YAML.
```
daemonset.yaml
```

Deploy it.
```
kubectl apply -f daemonset.yaml
```

or
```
kubectl create -f daemonset.yaml
```

---

# Checking DaemonSets
List them.
```
kubectl get daemonsets
```

Example
```
NAME                  DESIRED   CURRENT   READY
monitoring-daemon     3         3         3
```

What do these columns mean?

|Column|Meaning|
|---|---|
|DESIRED|Number of Pods that should exist (one per eligible node)|
|CURRENT|Number currently created|
|READY|Number ready and running|

If your cluster has three eligible nodes,

DESIRED should be three.

---

# See More Details
```
kubectl describe daemonset monitoring-daemon
```

You'll see:
- Events
- Labels
- Node selector
- Update strategy
- Pods managed
- Scheduling information

---

# How Does Kubernetes Decide Which Nodes?
Earlier (before Kubernetes v1.12),

DaemonSets often relied on directly setting `nodeName` internally.

Today,
DaemonSets use the **default scheduler** together with **Node Affinity** to ensure one Pod is scheduled onto each eligible node.

This is much more flexible and works well with modern scheduling features.

---

# Can DaemonSets Run on Every Node?
Usually, yes.

But sometimes you don't want that.

Suppose your cluster has:
```
Node1
Linux
```

```
Node2
Linux
```

```
Node3
Windows
```

A Linux monitoring agent obviously cannot run on Windows.

So you use **Node Selectors** or **Node Affinity**.

Example
```
spec:
  template:
    spec:
      nodeSelector:
        kubernetes.io/os: linux
```

Now the DaemonSet only runs on Linux nodes.

---

# DaemonSet + Taints
Remember Control Plane nodes?

They are usually tainted.

```
node-role.kubernetes.io/control-plane:NoSchedule
```

Will a normal DaemonSet run there?
No.

Unless you add the required **toleration**.

Example
```
tolerations:
- key: node-role.kubernetes.io/control-plane
  operator: Exists
  effect: NoSchedule
```

Now the DaemonSet is allowed to run on control-plane nodes too.

This is how components like CNI plugins or monitoring agents can be deployed across **all** nodes, including tainted ones when necessary.

---

# DaemonSet vs ReplicaSet vs Deployment

|Feature|Pod|ReplicaSet|Deployment|DaemonSet|
|---|---|---|---|---|
|Maintains Pods|No|Yes|Yes|Yes|
|Rolling Updates|No|No|Yes|Yes|
|Scales with `replicas`|No|Yes|Yes|No|
|One Pod per Node|No|No|No|Yes|
|Automatically covers new nodes|No|No|No|Yes|
|Common Use|Single workload|Maintain replica count|Manage application lifecycle|Run node-level services|

---

# Common Production Uses

|Application|Why DaemonSet?|
|---|---|
|Prometheus Node Exporter|Collect node metrics from every node|
|Fluentd / Fluent Bit|Collect logs from every node|
|kube-proxy|Manage Service networking on every node|
|Calico|Configure networking on every node|
|Weave Net|Configure networking on every node|
|Cilium|Configure networking on every node|
|Security agents (e.g., Falco)|Monitor system activity on every node|

---

# Visual Summary
```scss
Cluster

        +---------+---------+---------+
        |         |         |         |
      Node1     Node2     Node3
         │          │          │
         ▼          ▼          ▼
   Monitoring  Monitoring  Monitoring
      Agent       Agent       Agent
```

If another node joins:
```scss
        +---------+
        | Node4   |
        +---------+
             │
             ▼
     Monitoring Agent
```

No manual action is required.

---

# Interview Questions
### 1. What is a DaemonSet?
A DaemonSet ensures **exactly one Pod runs on every eligible node** in a Kubernetes cluster.

### 2. Does a DaemonSet use `replicas`?
No. The number of Pods is automatically determined by the number of eligible nodes.

### 3. What happens when a new node is added?
The DaemonSet automatically schedules a new Pod onto that node if it matches the DaemonSet's scheduling rules.

### 4. Name some real-world uses of DaemonSets.
- `kube-proxy`
- Prometheus Node Exporter
- Fluentd / Fluent Bit
- Calico
- Weave Net
- Cilium
- Falco

# Key Takeaways
- A **DaemonSet** guarantees **one Pod per eligible node**, not a fixed number of replicas.
- As nodes are **added**, the DaemonSet automatically creates Pods on them.
- As nodes are **removed**, the corresponding Pods are also removed.
- DaemonSets are ideal for **node-level services**, such as monitoring, logging, networking, and security agents.
- A DaemonSet does **not** use a `replicas` field.
- Modern Kubernetes uses the **default scheduler with Node Affinity** to place DaemonSet Pods.
- You can combine DaemonSets with **Node Selectors**, **Node Affinity**, and **Tolerations** to control exactly which nodes receive the Pods.


---
Labs commands

```bash
kubectl get daemonsets
kubectl get daemonsets -A

kubectl describe daemonsets kube-proxy -n kube-system

kubectl describe daemonsets kube-flannel-ds -n kube-system

kubectl create deployment elastisearch -n kube-system --image=k8s.gcr.io/fluentd-elasticsearch:1.20 --dry-run=client -o yaml
```

```yaml
apiVersion: apps/v1
kind: DaemonSet

metadata:
  name: elastisearch

spec:
  selector:
    matchLabels:
      app: elastisearch

  template:
    metadata:
      labels:
        app: elastisearch
ff
    spec:
      containers:
      - name: fluentd-elastisearch
        image: k8s.gcr.io/fluentd-elasticsearch:1.20
```

```
kubectl create -f fluentd.yaml
```


