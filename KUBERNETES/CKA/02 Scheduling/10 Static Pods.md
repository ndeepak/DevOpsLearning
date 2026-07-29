# Static Pods
Static Pods are one of the most misunderstood Kubernetes concepts because they look like normal Pods, but **they are created in a completely different way**.

To understand Static Pods, we first need to revisit how a normal Pod is created.

# First, Let's Recall Normal Pod Creation
When you execute:
```
kubectl apply -f nginx.yaml
```

Does the Pod get created immediately?
No.

There is an entire chain of events.

```scss
You
 │
 ▼
kubectl
 │
 ▼
API Server
 │
 ▼
etcd (stores Pod definition)
 │
 ▼
Scheduler
 │
 ▼
Selects a Node
 │
 ▼
Kubelet on that Node
 │
 ▼
Container Runtime
 │
 ▼
Container Starts
```

Notice something important.

The **Kubelet never decides by itself what Pod to create.**

It waits for instructions from the API Server.

Think of the Kubelet as an employee.

The API Server is the manager.

The employee never starts work without receiving an order.

---

# But What If There Is No API Server?
Imagine this situation.

You have only one Linux machine.

There is:
- No API Server
- No Scheduler
- No etcd
- No Controller Manager

Only these exist:
```scss
Linux Machine
+--------------------+
|                    |
|    Kubelet         |
|    Containerd      |
|                    |
+--------------------+
```

Question:
Can this machine still run containers?
Yes.

But...

Who tells the Kubelet which Pods to create?

Nobody.

Unless...

**You tell it directly.**

This is exactly why Static Pods exist.

---
# What Is a Static Pod?
A Static Pod is simply:
> **A Pod that is created directly by the Kubelet instead of through the API Server.**

No Scheduler.

No etcd.

No Deployment.

No ReplicaSet.

No API Server.

Only the Kubelet.

---

# Normal Pod vs Static Pod

Normal Pod
```scss
kubectl
    │
    ▼
API Server
    │
    ▼
Scheduler
    │
    ▼
Kubelet
    │
    ▼
Container
```

Static Pod
```
YAML File
     │
     ▼
Kubelet
     │
     ▼
Container
```

Much simpler.

---

# How Does the Kubelet Know Which Pods to Create?
The Kubelet watches a directory on the host.

Example:
```
/etc/kubernetes/manifests
```

Inside that folder you place Pod YAML files.

Example
```
/etc/kubernetes/manifests

├── nginx.yaml
├── api-server.yaml
├── etcd.yaml
└── scheduler.yaml
```

The Kubelet continuously watches this folder.

Every few seconds it checks:
> "Did someone add a new YAML file?"

If yes,
it creates the Pod.

---

# Think of It Like a Folder Watcher

Imagine Dropbox.

Whenever you copy a file into Dropbox,

it automatically syncs.

You don't press a Sync button.

The software watches the folder.

The Kubelet behaves similarly.

```
Manifest Folder

          nginx.yaml
               │
               ▼
          Kubelet notices
               │
               ▼
         Creates Pod
```

---

# What Happens If You Delete the File?
Suppose the folder contains:
```
/etc/kubernetes/manifests

nginx.yaml
```

The Kubelet creates
```
nginx Pod
```

Now delete the file.
```
rm nginx.yaml
```

The Kubelet notices:
> "The definition no longer exists."

So it deletes the Pod.
```
Manifest Deleted
       │
       ▼
Kubelet Deletes Pod
```

---

# What Happens If You Modify the File?
Suppose the original image is
```
image: nginx:1.26
```

You change it to
```
image: nginx:1.27
```

The Kubelet detects the change.

It deletes the old Pod.

Creates a new one.

Exactly like this:
```
Old Pod
↓
Delete
↓
Create New Pod
↓
Updated Version
```

---

# What Happens If the Container Crashes?
Suppose
```
nginx
```

crashes.

The Kubelet notices.

It restarts it automatically.

Exactly like a Deployment does.

Because one of the Kubelet's jobs is
> Keep desired Pods running.

---

# Configuring Static Pods
The Kubelet needs to know which directory to monitor.

One way is using
```
--pod-manifest-path
```

Example
```
--pod-manifest-path=/etc/kubernetes/manifests
```

This means
```
Kubelet
↓
Watch
↓
/etc/kubernetes/manifests
```

# Another Method
Instead of specifying the path directly,

the Kubelet can read a configuration file.

Example
```
staticPodPath: /etc/kubernetes/manifests
```

This is commonly used by **kubeadm**.

# Example Static Pod
Create
```
nginx.yaml
```

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

Copy it into
```
/etc/kubernetes/manifests/
```

Nothing else.

Don't run
```
kubectl apply
```

Don't run
```
kubectl create
```

The Kubelet automatically creates the Pod.

# Can We Create Deployments?
No.

Static Pods support only
```
Pod
```

You cannot create
- Deployment
- ReplicaSet
- StatefulSet
- DaemonSet
- Job
- CronJob
- Service

because these require the Kubernetes control plane.

The Kubelet only understands Pod definitions.

# Why?
Because controllers create these objects.

Example
Deployment
```
Deployment
↓
ReplicaSet
↓
Pods
```

Without the API Server and Controller Manager,

none of these controllers exist.

So only Pods can be created.
# Can We Use kubectl?
In a standalone environment,
No.

Because
```
kubectl
↓
API Server
```

But there is no API Server.

Instead,
you inspect containers directly.

Example
```
docker ps
```

or
```
crictl ps
```

or
```
ctr containers list
```

depending on the container runtime.

---
# Static Pods Inside a Kubernetes Cluster
Now imagine we have a normal cluster.

```
API Server
Scheduler
Controller Manager
etcd
Worker Nodes
```

Can Static Pods still exist?
Yes.

Now there are two sources of Pods.

### Source 1
Normal Kubernetes
```
kubectl
↓

API Server
↓

Kubelet
```

### Source 2
Static Pod
```
Manifest Folder
↓

Kubelet
```

The Kubelet now listens to both.

---

# Mirror Pods
Suppose the Kubelet creates
```
nginx
```

from
```
/etc/kubernetes/manifests
```

The API Server doesn't know about it.

So the Kubelet creates a **Mirror Pod**.

A Mirror Pod is **only a representation** of the Static Pod inside the API Server so you can see it with Kubernetes tools.
```
Static Pod
      │
      ▼
Kubelet
      │
      ▼
Mirror Pod
(API Server)
```

Now you can run
```
kubectl get pods
```

and you'll see something like:
```
NAME                 READY   STATUS

nginx-node01         1/1     Running
```

Notice the name often includes the node name (for example, `nginx-node01`) to show it originated from a Static Pod on that node.

---

# Can We Delete the Mirror Pod?
No.

Suppose you run
```
kubectl delete pod nginx-node01
```

What happens?

Nothing useful.

Because the real Pod is managed by the Kubelet.

The Kubelet immediately recreates the Mirror Pod.

To delete the Pod,
you must remove
```
nginx.yaml
```

from
```
/etc/kubernetes/manifests
```

---

# Real-World Use: Kubernetes Control Plane
This is where Static Pods become extremely important.

Think back to the Kubernetes architecture.

We have
- API Server
- Scheduler
- Controller Manager
- etcd

Question:
If the API Server itself is a Pod,

who creates it?
A Deployment?
Impossible.

The API Server must already exist for Deployments to work.

This is a **bootstrap problem**.

The solution is:
The **Kubelet** creates these critical components as **Static Pods**.

On a control-plane node (especially in clusters created with **kubeadm**), you'll often find:
```
/etc/kubernetes/manifests/

etcd.yaml

kube-apiserver.yaml

kube-scheduler.yaml

kube-controller-manager.yaml
```

The Kubelet watches this directory and ensures these control-plane Pods are always running.

If the API Server crashes, the Kubelet restarts it automatically.

This is one of the biggest real-world uses of Static Pods.

---
# Static Pods vs DaemonSets
These two are often confused because both can result in "one Pod per node."

The difference is **who creates and manages them**.

|Feature|Static Pod|DaemonSet|
|---|---|---|
|Created by|Kubelet directly|DaemonSet controller|
|Needs API Server|No|Yes|
|Created from|Local manifest file|Kubernetes object (`kubectl apply`)|
|Runs on every node automatically|No (you place a manifest on each node)|Yes|
|Common use|Control-plane components|Monitoring, logging, networking agents|
|Mirror Pod visible in API|Yes (if API Server exists)|Not applicable|

### Example
**Static Pod**
```
Node1
manifest folder
↓

API Server Pod
```

```
Node2
manifest folder
↓

API Server Pod
```

You must have the manifest on each node where you want the Pod.

---

**DaemonSet**
```
DaemonSet
↓

API Server
↓

Creates one Pod
↓

Every eligible node
```

The DaemonSet controller automatically creates Pods on all matching nodes.

---

# Interview Questions

### 1. What is a Static Pod?
A Static Pod is a Pod created and managed directly by the **Kubelet** from a local manifest file, without using the Kubernetes API Server.

### 2. Where are Static Pod manifests usually stored?
Typically in:
```
/etc/kubernetes/manifests
```
(or another directory configured via `--pod-manifest-path` or `staticPodPath`).

### 3. Can Static Pods be Deployments or ReplicaSets?
No. Static Pods support only **Pod** resources.

### 4. How do you modify a Static Pod?
Edit the manifest file in the static pod directory. The Kubelet detects the change and recreates the Pod automatically.

### 5. Why are Static Pods important?
They are commonly used to run critical Kubernetes control-plane components (API Server, Scheduler, Controller Manager, and etcd), especially in clusters created with `kubeadm`.

## Key Takeaways
- **Static Pods** are created directly by the **Kubelet**, not through the API Server.
- The Kubelet watches a local directory (commonly `/etc/kubernetes/manifests`) for Pod YAML files.
- Adding, modifying, or deleting a manifest file causes the Kubelet to create, recreate, or delete the corresponding Pod.
- Only **Pod** objects can be managed as Static Pods.
- In a cluster, the Kubelet creates a **Mirror Pod** in the API Server so the Static Pod is visible with `kubectl`, but the Mirror Pod is read-only.
- Static Pods are widely used to run Kubernetes **control-plane components**, solving the problem of starting the control plane before the control plane itself is available.
---

Labs commands


```bash
cd /etc/kubernetes/manifests &&  ls -la
    image: registry.k8s.io/kube-apiserver:v1.35.0
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: static-busybox
  namespace: default
spec:
  containers:
  - name: static-busybox
    image: busybox
    command:
    - sleep
    - "1000"
```

```bash
kubectl run static-busybox --image=busbybox --restart=Never --dry-run=client -o yaml --command -- sleep 1000 > static.yaml
```