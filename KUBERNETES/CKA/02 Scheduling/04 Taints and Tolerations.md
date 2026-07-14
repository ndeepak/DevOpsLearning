# 04 Taints and Tolerations
[03 Taints and Tolerations](KUBERNETES/KCNA/3%20Scheduling/03%20Taints%20and%20Tolerations.md)

# Taints and Tolerations in Kubernetes 
One of the biggest mistakes beginners make is thinking:
> **"Taints tell Kubernetes where to run a Pod."**

This is **NOT true.**

Taints **do not tell Kubernetes where to run a Pod.**

Instead, they answer a completely different question:

> **"Which Pods are NOT allowed to run on this node?"**

This small difference is extremely important.


# Before Learning Taints
Let's first understand a problem.
Suppose you have a Kubernetes cluster.
```
                 Kubernetes Cluster

            +------------------------+
            |     Control Plane      |
            +------------------------+

        +------------+------------+------------+
        |            |            |            |
      Worker1      Worker2      Worker3
```

Suppose there are three worker nodes.

Now you create four Pods.

```
Pod A
Pod B
Pod C
Pod D
```

The scheduler starts placing Pods.

Maybe it does this.

```
Worker1

Pod A
Pod B
```

```
Worker2

Pod C
```

```
Worker3

Pod D
```

Everything looks good.

The scheduler automatically balances the workload.

---

## But Now Imagine This...

Suppose Worker3 is a **very powerful machine.**

It has
- 64 CPUs
- 256 GB RAM
- Fast SSD

Your database must always run here.

You do NOT want normal application Pods running there.

But Kubernetes doesn't know that.

Tomorrow someone creates
```
Pod E
Pod F
Pod G
```

The scheduler may place them on Worker3.

```
Worker3
Database

Pod E
Pod F
```

Now your expensive database server is running random Pods.

That is not what you want.

So how do you tell Kubernetes:

> "Don't schedule ordinary Pods here."

This is exactly why **Taints** exist.


# The Simplest Analogy
Imagine three houses.
```
House A

Everyone Welcome
```

```
House B

Everyone Welcome
```

```
House C

No Visitors Allowed
```

How do people know?

There is a board.

```
NO VISITORS
```

Anyone without permission stays away.

Only authorized people can enter.

Exactly the same thing happens in Kubernetes.

```
Node
↓
Has a warning sign
↓
Only allowed Pods may enter
```

That warning sign is called a **Taint**.

# Another Analogy (Mosquito Spray)
This is the analogy used in many Kubernetes courses.
Imagine a person sprays mosquito repellent.

```
Person
↓
Mosquito Spray
```

Mosquitoes try to land.

Mosquito A
```
No immunity
↓
Cannot land
```

Mosquito B
```
Has immunity
↓
Can land
```

Mapping this to Kubernetes

|Real World|Kubernetes|
|---|---|
|Person|Node|
|Mosquito|Pod|
|Spray|Taint|
|Immunity|Toleration|

Very simple.

**Taints repel Pods.**

**Tolerations allow Pods to ignore the repellent.**

# What is a Taint?
A **taint** is a property added to a **Node**.

It tells Kubernetes
> "Don't schedule Pods here unless they tolerate this taint."

Notice something important.

The taint is **NOT added to the Pod.**

It is added to the **Node.**

Example
```
Worker1
Taint

app=blue:NoSchedule
```

Now Worker1 becomes protected.


# Taint Syntax
General syntax
```
kubectl taint nodes <node-name> key=value:effect
```

Example
```
kubectl taint nodes worker1 app=blue:NoSchedule
```

Let's understand every part.

## Part 1
```
app
```

This is called the **Key**.

It is just a name.

It could be anything.

Examples
```
app
team
gpu
database
```

## Part 2
```
blue
```

This is the **Value**.

Again,

it can be anything.

Example
```
app=blue
```

or
```
team=finance
```

or
```
gpu=nvidia
```

## Part 3
```
NoSchedule
```

This is the **Effect.**

This tells Kubernetes
> "What should happen if a Pod does NOT tolerate this taint?"

This is the most important part.

# Understanding the Effect
Suppose we write
```
kubectl taint nodes worker1 app=blue:NoSchedule
```

This means
```
Worker1
↓
Do not schedule Pods
↓
unless they tolerate
app=blue
```

That's all.

# Cluster Before Taint
Suppose
```
Worker1
Pod A
```

```
Worker2
Pod B
```

```
Worker3
Pod C
```

Everything is normal.

Now apply

```
kubectl taint nodes worker1 app=blue:NoSchedule
```

Now Worker1 becomes

```
Worker1
TAINTED
app=blue:NoSchedule
```

Now create another Pod.
```
Pod D
```
Pod D has **no toleration.**

Scheduler thinks
```
Can I put it on Worker1?
↓
No
↓
Node has taint
↓
Pod doesn't tolerate it
```

So it chooses
```
Worker2
```

or
```
Worker3
```

instead.

# What is a Toleration?
Now suppose one Pod SHOULD be allowed on Worker1.

We add a toleration.

Example
```
apiVersion: v1
kind: Pod

metadata:
  name: nginx

spec:
  tolerations:
  - key: "app"
    operator: "Equal"
    value: "blue"
    effect: "NoSchedule"

  containers:
  - image: nginx
    name: nginx
```

Now this Pod says

> "I can tolerate app=blue."

Now Kubernetes allows it on Worker1.

# Does Toleration Force Scheduling?
This is the biggest interview question.

Suppose
Worker1
```
app=blue:NoSchedule
```
Pod
```
tolerations:
- key: app
  value: blue
```

Will Kubernetes definitely schedule it on Worker1?
**NO**

It only becomes **eligible**.

Scheduler still checks
- CPU
- Memory
- Node health
- Affinity
- Resources

Maybe Worker2 is a better choice.

The scheduler may place it there instead.

This is extremely important.

> **Toleration allows scheduling.**> 
> **It never forces scheduling.**

# Complete Example
## Step 1
Check nodes
```
kubectl get nodes
```

Output
```
NAME
worker1
worker2
worker3
```

## Step 2
Add taint
```
kubectl taint nodes worker1 app=blue:NoSchedule
```
Output
```
node/worker1 tainted
```
## Step 3
Verify
```
kubectl describe node worker1
```
Output
```
Taints:
app=blue:NoSchedule
```

## Step 4
Create Pod WITHOUT toleration
```
apiVersion: v1
kind: Pod

metadata:
  name: pod1

spec:
  containers:
  - image: nginx
    name: nginx
```

Apply
```
kubectl apply -f pod1.yaml
```

Scheduler behavior
```
worker1
↓
Rejected
```

Pod goes to
```
worker2
```

or
```
worker3
```

## Step 5
Create Pod WITH toleration
```
apiVersion: v1
kind: Pod
metadata:
  name: pod2
spec:
  tolerations:
  - key: "app"
    operator: "Equal"
    value: "blue"
    effect: "NoSchedule"

  containers:
  - image: nginx
    name: nginx
```

Apply
```
kubectl apply -f pod2.yaml
```

Now
```
worker1
↓
Allowed
```

Remember
Allowed
≠
Guaranteed

# The Three Effects
There are only three effects.

# 1. NoSchedule
Most commonly used.
Meaning
```
Future Pods
↓
No toleration
↓
Cannot run here
```

Existing Pods
```
Remain running
```

Example
```
kubectl taint nodes worker1 app=blue:NoSchedule
```

# 2. PreferNoSchedule
Think of this as
> "Please avoid this node."

Example
```
kubectl taint nodes worker1 app=blue:PreferNoSchedule
```

Scheduler thinks
```
Can I use another node?
↓
Yes
↓
Use another node.
```
But
```
No other node available
↓
Okay
↓
Use worker1
```

This is only a preference.
# 3. NoExecute
This is the strongest effect.
Imagine
Worker1
```
Pod A

Pod B

Pod C
```

Now
```
kubectl taint nodes worker1 app=blue:NoExecute
```

Scheduler checks every Pod.

Pod A
```
No toleration
↓
Evicted
```

Pod B
```
No toleration
↓
Evicted
```

Pod C
```
Has toleration
↓
Continues Running
```

New Pods without toleration
```
Rejected
```

So NoExecute does two things.
- Rejects future Pods
- Removes existing Pods

---

# Understanding the Operator
Inside toleration
```
operator: Equal
```
means
Everything must match.
Node
```
app=blue
```

Pod
```
key=app
value=blue
```

Perfect match.

Allowed.

Another operator
```
operator: Exists
```
means
Ignore value.

Just check key.
Node
```
gpu=nvidia
```
Pod
```
key: gpu
operator: Exists
```
Matches.

Node
```
gpu=amd
```
Still matches.

Only key matters.

# Removing a Taint
Current
```
app=blue:NoSchedule
```

Remove
```
kubectl taint nodes worker1 app=blue:NoSchedule-
```

Notice the
```
-
```
at the end.

Without it,
the taint is not removed.


# Control Plane Nodes
If you inspect your control-plane node,
```
kubectl describe node control-plane
```

You'll probably see something like
```
node-role.kubernetes.io/control-plane:NoSchedule
```
Why?
Because Kubernetes does not want normal applications running on the control plane.

The control plane runs critical components such as:
- kube-apiserver
- etcd
- kube-scheduler
- kube-controller-manager

Keeping user workloads away helps maintain cluster stability.

# Taints vs Node Selector
Suppose
Worker1
```
app=blue:NoSchedule
```

Pod
```
toleration:
```

Will it definitely go there?
No.

Now add
```
nodeSelector:
  color: blue
```

Now the Pod says
```
I WANT
blue node
```

The taint says
```
Only allowed Pods
may enter
```

Together
the Pod is both **allowed** and **directed** to the appropriate node.

This combination is very common in production.
# Real Production Example
Suppose your company has one GPU server.
You don't want normal applications running there.
Add taint
```
kubectl taint nodes gpu-node gpu=true:NoSchedule
```

Machine
```
GPU NODE
↓
Protected
```

AI workload
```
tolerations:
- key: gpu
  operator: Equal
  value: "true"
  effect: NoSchedule
```

Only AI workloads can run there.

# Summary

|Component|Applied On|Purpose|
|---|---|---|
|**Taint**|Node|Repels Pods that don't tolerate it|
|**Toleration**|Pod|Allows the Pod to be scheduled onto a matching tainted node|
|**NoSchedule**|Node|Prevent new Pods without toleration|
|**PreferNoSchedule**|Node|Try to avoid scheduling Pods without toleration|
|**NoExecute**|Node|Reject new Pods and evict existing Pods without toleration|

---

# Key Takeaways

- **Taints are applied to nodes**, not Pods.
- **Tolerations are applied to Pods**, not nodes.
- A taint acts like a protective barrier that repels Pods without matching tolerations.
- A toleration **does not force** a Pod onto a tainted node—it only makes the Pod eligible to run there.
- The scheduler still evaluates CPU, memory, node health, affinity, and other scheduling constraints before choosing a node.
- **NoSchedule** blocks new Pods, **PreferNoSchedule** is a soft preference to avoid the node, and **NoExecute** both blocks new Pods and evicts existing non-tolerating Pods.
- In production, taints are commonly used to reserve nodes for databases, GPU workloads, specialized hardware, maintenance operations, and to protect control-plane nodes from regular application workloads.
- The most common production pattern is to **combine taints with node labels and node selectors (or node affinity)**: labels attract the right workloads, while taints keep unwanted workloads away.

----


## Lab
controlplane ~ ➜  kubectl describe node node01

controlplane ~ ➜  kubectl taint nodes node01 spray=mortein:NoSchedule

controlplane ~ ✖ kubectl run mosquito --image=nginx


```bash
cat sample.yaml 
apiVersion: v1
kind: Pod
metadata:
  name: bee
  labels:
    run: bee
spec:
  containers:
  - name: nginx
    image: nginx
  tolerations:
  - key: "spray"
    operator: "Equal"
    value: "mortein"
    effect: "NoSchedule"
```

```bash
controlplane ~ ➜  kubectl taint nodes controlplane node-role.kubernetes.io/control-plane:NoSchedule-
node/controlplane untainted
```