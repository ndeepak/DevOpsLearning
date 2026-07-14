# Manual Scheduling in Kubernetes
[01 Manual Scheduling](KUBERNETES/KCNA/3%20Scheduling/01%20Manual%20Scheduling.md)
## Introduction
In a normal Kubernetes cluster, **you never decide which node a Pod runs on**.

Instead:
1. You create a Pod.
2. The API Server stores the Pod.
3. The Scheduler finds the best node.
4. The Scheduler updates the Pod's `nodeName`.
5. The kubelet on that node starts the Pod.

This automatic scheduling works well for almost every production workload.

However, Kubernetes also allows you to **bypass the scheduler** and manually assign a Pod to a specific node.

This process is called **Manual Scheduling**.

---

# Why Would We Manually Schedule Pods?

In real production environments, manual scheduling is **rare** because Kubernetes' scheduler is highly optimized.

However, there are situations where it becomes useful.

Examples include:

- Testing Kubernetes internals
- Learning how scheduling works
- Running a Pod on a specific machine for debugging
- Temporary maintenance
- Custom schedulers
- Bootstrap environments where no scheduler exists

For normal applications, **manual scheduling is not recommended**.

---

# How Automatic Scheduling Normally Works

Suppose we have a cluster:

```
             Control Plane
        +----------------------+
        | API Server           |
        | Scheduler            |
        +----------+-----------+
                   |
        -------------------------
        |           |           |
     Worker1     Worker2     Worker3
```

You create a Pod.

```
kubectl apply -f pod.yaml
```

Initially, Kubernetes stores:

```
Pod
Name: nginx

NodeName: <empty>
```

The Scheduler continuously watches for Pods whose `nodeName` is empty.

It performs scheduling.

```
Scheduler
↓
Find Best Node
↓
Worker2
```

The scheduler updates:

```
nodeName: worker2
```

Now kubelet on Worker2 creates the Pod.

---

# The `nodeName` Field

Every Pod object contains a field called:

```
spec:
  nodeName:
```

This field tells Kubernetes:

> "This Pod must run on this node."

Normally, you never write it.

Instead, the Scheduler fills it automatically.

Example before scheduling:

```
spec:
  containers:
  - image: nginx
```

Notice:

```
nodeName does not exist
```

Scheduler later changes it internally into:

```
spec:
  nodeName: worker2
```

---

# Basic Pod Without nodeName

This is the standard Pod manifest.

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

Here,

```
nodeName = empty
```

Scheduler will choose a node.

---

# Manual Scheduling

Instead of waiting for the Scheduler, you can tell Kubernetes exactly where to run the Pod.

Example:

```
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  nodeName: node02
  containers:
  - name: nginx
    image: nginx
```

Now Kubernetes does **not** ask the Scheduler.

The kubelet running on **node02** notices:

> "This Pod is assigned to me."

It starts the container immediately.

---

# Internal Workflow

Without manual scheduling:

```
Create Pod
↓
API Server
↓
Scheduler
↓
node02 selected
↓
Kubelet
↓
Running
```

With manual scheduling:

```
Create Pod
↓
API Server
↓
nodeName already exists
↓
Scheduler skipped
↓
Kubelet on node02
↓
Running
```

Notice that the Scheduler is completely bypassed.

---

# Demonstration
Create Pod

```
kubectl apply -f nginx.yaml
```

Check Pods

```
kubectl get pods -o wide
```

Example

```
NAME      READY   STATUS    NODE
nginx     1/1     Running   node02
```

The Pod immediately appears on node02 because the scheduler was never involved.

---

# What Happens If node02 Doesn't Exist?

Suppose you specify
```
nodeName: node99
```

But your cluster only has
```
node01
node02
node03
```

Result
```
Pod
STATUS
Pending
```

Why?

Because:
- Scheduler is skipped.
- No kubelet exists on node99.
- No one can run the Pod.

This is one of the biggest risks of manual scheduling.

---

# What If node02 Is Not Ready?
Suppose
```
node02

STATUS

NotReady
```

Your manifest
```
nodeName: node02
```

Result
```
Pending
```

The scheduler would normally choose another healthy node.

Manual scheduling removes that intelligence.

---

# Manual Scheduling Does NOT Check Resources
Imagine

Node:
```
CPU Available

0.1 Core
```

Your Pod requests

```
resources:
  requests:
    cpu: "2"
```

Normally

Scheduler says:

```
No
Insufficient CPU
```

But with manual scheduling,

Kubernetes directly assigns the Pod.

The kubelet may fail to start it because the node lacks sufficient resources, leaving the Pod Pending or causing resource contention depending on the workload and node state.

This illustrates an important point:

> **Manual scheduling bypasses scheduler decision-making, not the node's actual resource limitations.**

---

# Can We Change nodeName Later?

No.

Once a Pod is created,
```
nodeName
```

is **immutable**.

Example

Current
```
nodeName: node01
```

Trying
```
nodeName: node03
```

Results in an error similar to:
```
The Pod is invalid.
field is immutable
```

Reason:
Pods are designed to run on one node for their lifetime.

If you need the Pod on another node, Kubernetes expects you to create a new Pod.

---

# Why Can't Kubernetes Simply Move the Pod?

Imagine
```
Node01
Running MySQL
```

If Kubernetes suddenly moved it to Node02:
- Memory contents would be lost.
- Running processes would stop.
- Open network connections would break.
- File handles would disappear.

Containers cannot simply "teleport" between machines.

Instead,
Kubernetes destroys the old Pod and creates a new one.

---

# What Is a Binding Object?
The Scheduler itself doesn't directly edit the Pod in a special way. Instead, it performs a **binding** operation through the Kubernetes API.

A **Binding object** represents the association between a Pod and a Node.

Conceptually:
```
Pod
↓
Bind
↓
Node
```

Example:
```
apiVersion: v1
kind: Binding

metadata:
  name: nginx

target:
  apiVersion: v1
  kind: Node
  name: node02
```

This tells Kubernetes:
> "Bind the Pod named `nginx` to `node02`."

---

# Using the Binding API
The Binding resource is a specialized API endpoint. Instead of creating it with `kubectl apply`, it is typically sent as a POST request.

Example:

```
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data @binding.json \
  http://$SERVER/api/v1/namespaces/default/pods/nginx/binding
```

Here:
- `binding.json` contains the binding object.
- The request targets the Pod's `/binding` subresource.
- Kubernetes processes the binding similarly to how the default scheduler does.

> **Important:** In modern Kubernetes, this mechanism is primarily used by schedulers and advanced integrations. As an end user, you would almost never bind Pods manually in a production environment.

---

# Manual Scheduling vs Default Scheduler

|Feature|Default Scheduler|Manual Scheduling|
|---|---|---|
|Chooses best node|Yes|No|
|Checks available CPU|Yes|No (scheduler is bypassed)|
|Checks available memory|Yes|No (scheduler is bypassed)|
|Honors affinity and anti-affinity|Yes|No|
|Honors taints and tolerations|Yes|No|
|Balances workloads|Yes|No|
|User specifies node|No|Yes|

---

# Advantages
- Complete control over Pod placement.
- Useful for testing scheduler behavior.
- Helpful in debugging.
- Can be used in clusters without a scheduler.
- Useful when developing custom schedulers.

---

# Disadvantages
- No automatic resource-based placement.
- No load balancing across nodes.
- No high availability decisions.
- Easy to choose an unavailable or overloaded node.
- Not scalable for large clusters.
- Generally unsuitable for production application workloads.

---

# Real Production Use Cases
Although uncommon for everyday applications, manual scheduling or direct node assignment can be useful in specific scenarios:

### 1. Scheduler Development
When building or testing a custom scheduler, you may manually bind Pods to validate scheduling logic.

### 2. Bootstrap Clusters
During the initial setup of a Kubernetes control plane, before the scheduler is running, certain critical Pods may need explicit node assignments.

### 3. Debugging a Node
Suppose only `worker03` has a hardware issue that you want to investigate. You can force a troubleshooting Pod onto that node.

```
spec:
  nodeName: worker03
```

### 4. Lab Environments
In learning environments, manually assigning Pods helps you understand how scheduling works internally before exploring advanced scheduling features.

---

# Best Practices
- Let the Kubernetes scheduler make placement decisions whenever possible.
- Use `nodeName` only for testing, debugging, or specialized scenarios.
- Avoid using manual scheduling in production applications.
- For production placement requirements, prefer features such as **node selectors**, **node affinity**, **taints and tolerations**, or **custom schedulers** instead of hardcoding node names.

---

# Key Takeaways
- Every Pod has a `spec.nodeName` field that identifies the node where it will run.
- By default, this field is empty, and the Kubernetes Scheduler selects an appropriate node.
- Setting `nodeName` in the Pod manifest bypasses the scheduler and assigns the Pod directly to that node.
- If the specified node does not exist or is unavailable, the Pod remains in the **Pending** state because the scheduler is not involved.
- The `nodeName` field is immutable after Pod creation.
- A **Binding** object is the API mechanism used by schedulers to associate a Pod with a Node.
- Manual scheduling is primarily intended for testing, debugging, bootstrap scenarios, or custom scheduler development—not for routine production deployments.