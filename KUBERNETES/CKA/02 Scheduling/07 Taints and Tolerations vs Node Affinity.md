# Taints and Tolerations vs Node Affinity

This is one of the **most important Kubernetes scheduling concepts**.

Many beginners learn:
- Taints and Tolerations
- Node Selectors
- Node Affinity

as separate topics.

But in real production environments, they are almost always **used together**.

The biggest confusion comes from questions like:
- Why do we need both?
- Isn't Node Affinity enough?
- Doesn't a Taint already reserve a node?
- Which one should I use?

By the end of this lesson, you'll clearly understand **what problem each feature solves** and **why combining them is the best practice**.
# Let's Start with a Simple Cluster
Suppose we have four worker nodes.

```
                    Kubernetes Cluster

          +---------------------------------+
          |        Control Plane            |
          +---------------------------------+

      +---------+---------+---------+---------+
      |         |         |         |         |
    Node1     Node2     Node3     Node4
```

Now suppose each node is dedicated to a different application.

|Node|Purpose|
|---|---|
|Node1|Blue Application|
|Node2|Red Application|
|Node3|Green Application|
|Node4|General Purpose|

We also have four Pods.
```
Blue Pod

Red Pod

Green Pod

Other Pod
```

Our goal is:

|Pod|Should Run On|
|---|---|
|Blue Pod|Blue Node|
|Red Pod|Red Node|
|Green Pod|Green Node|
|Other Pod|General Node|

Simple enough.

Now let's see how Kubernetes behaves.

# Scenario 1 – No Scheduling Rules
Initially,
none of the nodes have labels.
No taints.

No affinity.

No tolerations.

The scheduler simply looks for available resources.

It may schedule like this:

```
Node1 (Blue)

Red Pod
```

```
Node2 (Red)

Other Pod
```

```
Node3 (Green)

Blue Pod
```

```
Node4

Green Pod
```

Everything is technically valid.

The scheduler has no idea that Blue Pods belong on Blue Nodes.

It only sees CPU, memory, and available resources.

This is why scheduling rules are needed.

# Solution 1 – Using Only Taints and Tolerations
Let's taint every node.

```
Node1

color=blue:NoSchedule
```

```
Node2

color=red:NoSchedule
```

```
Node3

color=green:NoSchedule
```

Node4 remains untainted.

Now add matching tolerations.

Blue Pod

```
tolerations:
- key: color
  value: blue
  operator: Equal
  effect: NoSchedule
```

Red Pod

```
tolerations:
- key: color
  value: red
  operator: Equal
  effect: NoSchedule
```

Green Pod

```
tolerations:
- key: color
  value: green
  operator: Equal
  effect: NoSchedule
```

Looks perfect...

Or is it?

---

## What Actually Happens?

Remember what tolerations do.

They say
> "I am allowed to run on this node."

They **do not** say
> "I must run on this node."

This is the biggest misconception.

Suppose the Blue Pod is created.

The scheduler checks.

Blue Node?

Allowed.

General Node?

Also allowed (because it has no taint).

The scheduler might choose the general node.

Example

```
Blue Node

(empty)
```

```
General Node

Blue Pod
```

This is completely valid.

Why?

Because tolerations **allow** scheduling.

They never **force** scheduling.

---

# Limitation of Taints and Tolerations

They answer only one question:

> **"Can this Pod enter this node?"**

They never answer

> **"Which node should this Pod choose?"**

Think of a VIP pass.

Imagine four conference rooms.

Room A
```
VIP Only
```

Room B
```
VIP Only
```

Room C
```
VIP Only
```

Room D
```
Everyone Welcome
```

You have a VIP badge.

Can you enter Room A?
Yes.

Can you enter Room D?
Also yes.

The badge doesn't tell you which room to enter.

It only tells security to let you in.

Tolerations work exactly the same way.

---

# Solution 2 – Using Only Node Affinity
Now remove all taints.

Instead,
label nodes.
```
Node1

color=blue
```

```
Node2

color=red
```

```
Node3

color=green
```

Blue Pod

```
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: color
          operator: In
          values:
          - blue
```

Perfect.

The scheduler now places Blue Pod on Blue Node.

Exactly what we wanted.

---

## But There's Still a Problem
Imagine another Pod.

```
apiVersion: v1
kind: Pod
metadata:
  name: random-pod
spec:
  containers:
  - image: nginx
```

This Pod has
- No affinity
- No selector

The scheduler may place it anywhere.

Including
```
Blue Node

Blue Pod

Random Pod
```

Oops.

Blue Node is no longer dedicated.

Node Affinity attracted the Blue Pod.

But it didn't stop unrelated Pods from entering.

---

# Limitation of Node Affinity
Node Affinity answers
> "Where should this Pod go?"

It never answers
> "Who else is allowed here?"

That is not its job.

---

# Visual Comparison
## Taints
```
Node
↓
Blocks unwanted Pods
```

---

## Node Affinity

```
Pod
↓

Looks for matching nodes
```

Notice

They solve opposite problems.

---

# The Best Solution — Use Both Together
Now let's combine them.

Node1
Label
```
color=blue
```

Taint
```
color=blue:NoSchedule
```

Blue Pod

Affinity
```
color=blue
```

Toleration
```
color=blue
```

Now let's follow the scheduler step by step.

---

## Step 1
Blue Pod says
> I want

```
color=blue
```

Scheduler searches.

Blue Node found.

## Step 2
Scheduler checks

Can I schedule here?
Node has

```
color=blue:NoSchedule
```

Does Pod tolerate it?
Yes.

Allowed.

## Step 3
Random Pod arrives.

No affinity.

Scheduler considers Blue Node.
Node has taint.

Random Pod has no toleration.
Rejected.

Scheduler moves to another node.
Perfect.

Now the Blue Node contains only Blue workloads.

---

# Complete Example
## Step 1 – Label Nodes
```
kubectl label node worker1 color=blue
kubectl label node worker2 color=red
kubectl label node worker3 color=green
```

Verify:
```
kubectl get nodes --show-labels
```

## Step 2 – Apply Taints
```
kubectl taint nodes worker1 color=blue:NoSchedule
kubectl taint nodes worker2 color=red:NoSchedule
kubectl taint nodes worker3 color=green:NoSchedule
```

Verify:
```
kubectl describe node worker1
```

You should see:
```
Taints:
color=blue:NoSchedule
```

## Step 3 – Create the Blue Pod
```
apiVersion: v1
kind: Pod
metadata:
  name: blue-app
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: color
            operator: In
            values:
            - blue

  tolerations:
  - key: "color"
    operator: "Equal"
    value: "blue"
    effect: "NoSchedule"

  containers:
  - name: nginx
    image: nginx
```

Deploy it:
```
kubectl apply -f blue-pod.yaml
```

Verify:
```
kubectl get pods -o wide
```

The Blue Pod should be running on `worker1`.

## Step 4 – Create a Random Pod
```
apiVersion: v1
kind: Pod
metadata:
  name: random-pod
spec:
  containers:
  - name: nginx
    image: nginx
```

This Pod has:
- No node affinity
- No toleration

When scheduled:
- It cannot run on `worker1`, `worker2`, or `worker3` because of their taints.
- It will be placed on an untainted node (for example, the general-purpose `worker4`).


# Why Production Clusters Use Both
Suppose your company has:
- GPU servers
- Database servers
- High-memory servers
- SSD servers

You want:
- AI workloads only on GPU nodes
- Databases only on database nodes
- Analytics only on high-memory nodes

If you use only Node Affinity:
Other workloads can still land there.

If you use only Taints:
The specialized workloads may still choose general-purpose nodes.

Combining both gives you:
- **Node Affinity** attracts the correct workloads.
- **Taints** repel unrelated workloads.
- **Tolerations** allow only the intended workloads onto protected nodes.

This creates dedicated infrastructure for specialized applications.

---

# Real Production Example
Suppose you have a GPU node.

Label it:
```
gpu=true
```

Taint it:
```
gpu=true:NoSchedule
```

An AI Pod would look like:
```
apiVersion: v1
kind: Pod
metadata:
  name: ai-training
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: gpu
            operator: In
            values:
            - "true"

  tolerations:
  - key: "gpu"
    operator: "Equal"
    value: "true"
    effect: "NoSchedule"

  containers:
  - name: trainer
    image: tensorflow/tensorflow:latest
```

Result:
- The Pod searches only for GPU nodes.
- The GPU node accepts it because of the matching toleration.
- Ordinary Pods without the toleration cannot use the GPU node.

# Comparison Table

|Feature|Taints & Tolerations|Node Affinity|
|---|---|---|
|Applied To|Taints → Nodes, Tolerations → Pods|Pods|
|Uses|Node taints|Node labels|
|Purpose|Repel unwanted Pods|Attract Pods to matching nodes|
|Forces scheduling to a node|No|Yes (when using `requiredDuringSchedulingIgnoredDuringExecution` and a matching node exists)|
|Prevents other Pods from using the node|Yes (if they lack the required toleration)|No|
|Common Use|Reserve and protect nodes|Direct workloads to suitable nodes|

> **Note:** Even with `requiredDuringSchedulingIgnoredDuringExecution`, the scheduler may choose **any** node that satisfies the affinity rules if multiple matching nodes exist. It does not force a specific node unless only one node matches.

---

# Easy Way to Remember

Imagine a private office building.

The **building directory** tells visitors where to go.

That's **Node Affinity**.

The **security guard** checks whether they have an access card.
That's **Taints and Tolerations**.

You need **both**:
- The directory guides the right people to the correct office.
- Security prevents unauthorized people from entering.

If you have only the directory, unauthorized visitors can still walk in.

If you have only security, authorized visitors may wander into the wrong office.

Together, they provide the intended behavior.

---

# Key Takeaways
- **Taints and Tolerations** answer: **"Which Pods are allowed on this node?"**
- **Node Affinity** answers: **"Which nodes should this Pod run on?"**
- Tolerations **permit** scheduling onto tainted nodes but do **not** attract Pods to them.
- Node Affinity **directs** Pods to matching nodes but does **not** prevent unrelated Pods from using those nodes.
- Combining **Node Affinity** with **Taints and Tolerations** is the standard production pattern for dedicating nodes to specific workloads while keeping unrelated workloads away.
- This combination is widely used for GPU nodes, database servers, high-memory machines, SSD-backed storage nodes, and multi-tenant Kubernetes clusters.