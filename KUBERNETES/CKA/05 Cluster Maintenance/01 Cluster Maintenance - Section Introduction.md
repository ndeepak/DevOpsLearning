# Cluster Maintenance - Section Introduction
1. Cluster Upgrade Process
2. Operating System Upgrades
3. Backup and Restore Methodologies

---
# Summary Notes
# Cluster Maintenance — CKA
## 1. What does "Cluster Maintenance" actually mean?
Imagine you have this cluster:
```
                    Kubernetes Cluster
                           |
             +-------------+-------------+
             |                           |
       Control Plane                  Workers
             |                    +------+------+
       +-----+-----+              |             |
       |           |           worker-1      worker-2
    API Server   etcd
    Scheduler
    Controller
```

During normal operation, Kubernetes is continuously running workloads.

But administrators eventually need to:
- Patch the operating system
- Reboot a node
- Replace a failed node
- Upgrade Kubernetes
- Upgrade kubelet
- Upgrade container runtime
- Perform kernel updates
- Back up cluster state
- Restore after disaster
- Remove nodes safely

The central principle is:
> **Never perform maintenance blindly on a node that may be running workloads.**

Instead, Kubernetes provides mechanisms to safely make a node unavailable.

The most important commands for this section are:
```
kubectl cordon
kubectl drain
kubectl uncordon
kubeadm upgrade plan
kubeadm upgrade apply
kubectl get nodes
kubectl describe node
```

And for backup:
```
ETCDCTL_API=3 etcdctl snapshot save
ETCDCTL_API=3 etcdctl snapshot status
ETCDCTL_API=3 etcdctl snapshot restore
```

---

# 2. The Three Most Important Node Maintenance Commands
Before going deeper, memorize this relationship:
```scss
              Node Maintenance
                     |
        +------------+------------+
        |            |            |
      cordon       drain       uncordon
        |            |            |
    Stop new      Evict         Allow
    scheduling    workloads     scheduling
```

They solve different problems.

---

# 3. `kubectl cordon`
Suppose:
```
worker-1
   |
   +-- nginx
   +-- redis
   +-- api
```
You need to perform maintenance on `worker-1`.

First:
```
kubectl cordon worker-1
```

Now:
```
worker-1
   |
   +-- nginx
   +-- redis
   +-- api

No NEW pods scheduled here
```

Existing Pods remain running.

You can verify:
```
kubectl get nodes
```

Example:
```
NAME       STATUS
master     Ready
worker-1   Ready,SchedulingDisabled
worker-2   Ready
```

The important part is:
```
SchedulingDisabled
```

### What did cordon actually do?
It marks the node as:
```
unschedulable
```

Kubernetes scheduler will no longer place **new Pods** onto that node.

But:
```
Existing Pods = remain
```
This distinction is extremely important for CKA.

---

# 4. `kubectl drain`
Cordon is not enough if you want to safely shut down the node.

Suppose:
```
worker-1

Pod A
Pod B
Pod C
```
You want to reboot the server.

If you simply reboot it:
```
worker-1
    ↓
 REBOOT
    ↓
Pod A
Pod B
Pod C
```

Those workloads become unavailable.

Instead:
```
kubectl drain worker-1
```

Conceptually:

```
worker-1
   |
   +-- Pod A ──┐
   +-- Pod B ──┼──> Evicted
   +-- Pod C ──┘
```

Kubernetes attempts to safely evict the Pods.

If those Pods are managed by a Deployment/ReplicaSet:

```
worker-1
   |
   +-- nginx Pod
```

The Deployment controller can create replacement Pods elsewhere:

```
worker-1                  worker-2
   |                         |
   X                         +-- nginx
                             +-- nginx
```

This is why draining is safer than simply shutting down a node.

---

# 5. `cordon` vs `drain`

This is a classic CKA question.

|Command|New Pods?|Existing Pods?|
|---|---|---|
|`cordon`|Prevents|Keeps running|
|`drain`|Prevents|Evicts|
|`uncordon`|Allows|Existing unaffected|

Think:

```
CORDON
"Don't put anything new here."

DRAIN
"Move everything that can safely move away."

UNCORDON
"Okay, this node can receive workloads again."
```

---

# 6. `kubectl uncordon`

After maintenance:

```
kubectl uncordon worker-1
```

Now:

```
worker-1
Scheduling enabled
```

Check:

```
kubectl get nodes
```

You should see:

```
worker-1   Ready
```

instead of:

```
worker-1   Ready,SchedulingDisabled
```

---

# 7. Complete Node Maintenance Workflow

This is one of the workflows you should know extremely well for CKA.

Suppose:

```
worker-1
```

needs an OS upgrade.

### Step 1 — Check the node

```
kubectl get nodes
```

Then:

```
kubectl describe node worker-1
```

Look at:

- Pods
- Conditions
- Taints
- Allocatable resources
- Capacity

---

### Step 2 — Cordon

```
kubectl cordon worker-1
```

Now no new workloads are scheduled there.

---

### Step 3 — Drain

```
kubectl drain worker-1
```

Depending on the workloads, you may need options.

Common CKA command:

```
kubectl drain worker-1 --ignore-daemonsets
```

Why?

Because DaemonSet Pods are designed to run on nodes.

For example:

```
worker-1
   |
   +-- kube-proxy
   +-- monitoring-agent
   +-- logging-agent
```

These may be managed by DaemonSets.

Kubernetes does not normally evict DaemonSet-managed Pods using a normal drain.

Therefore:

```
kubectl drain worker-1 --ignore-daemonsets
```

---

# 8. Why `--ignore-daemonsets`?

Suppose:

```
kubectl drain worker-1
```

returns something like:

```
error: cannot delete DaemonSet-managed Pods
```

You can use:

```
kubectl drain worker-1 --ignore-daemonsets
```

This tells Kubernetes:

> Ignore Pods managed by DaemonSets while draining.

Important:

It does **not** mean those Pods continue serving normally during a node shutdown.

The node itself is still going offline.

---

# 9. Other Drain Options You Need to Know

Another common situation is a Pod that isn't managed by a controller.

For example:

```
kubectl run nginx --image=nginx
```

That Pod isn't necessarily managed by a Deployment.

Drain may refuse to remove it.

You may see a message indicating that the Pod is unmanaged.

In appropriate situations:

```
kubectl drain worker-1 --ignore-daemonsets --force
```

`--force` allows eviction/removal of certain Pods that aren't managed by a controller.

But understand the danger:

```
Deployment-managed Pod
       ↓
safe to recreate elsewhere

Standalone Pod
       ↓
may disappear permanently
```

Therefore, don't blindly use:

```
--force
```

in production.

---

# 10. PodDisruptionBudget

Another important concept is:

```
PodDisruptionBudget
```

Suppose you have:

```
3 replicas

Pod A
Pod B
Pod C
```

And a PDB:

```
minAvailable: 2
```

Kubernetes should maintain at least two available Pods during voluntary disruptions.

If you try:

```
kubectl drain worker-1
```

Kubernetes may refuse to evict a Pod if doing so would violate the PDB.

This is actually a **good thing**.

It protects application availability.

---

# 11. Complete Maintenance Example

Suppose:

```
NAME       STATUS
master     Ready
worker-1   Ready
worker-2   Ready
```

Workloads:

```
worker-1:
  nginx-1
  api-1

worker-2:
  nginx-2
  api-2
```

You need to patch `worker-1`.

### Cordon

```
kubectl cordon worker-1
```

### Drain

```
kubectl drain worker-1 --ignore-daemonsets
```

Pods are moved/recreated elsewhere.

Now:

```
worker-1
  No normal application workloads

worker-2
  nginx
  api
  replacements
```

Perform OS maintenance:

```
sudo dnf update
sudo reboot
```

After reboot:

```
kubectl get nodes
```

Wait until:

```
worker-1   Ready
```

Then:

```
kubectl uncordon worker-1
```

Finally:

```
kubectl get nodes
kubectl get pods -A -o wide
```

---

# 12. Why Node Maintenance Matters

Consider a cluster with:

```
3 worker nodes

worker-1
worker-2
worker-3
```

and:

```
10 application Pods
```

If you randomly shut down:

```
worker-1
```

you could lose several Pods simultaneously.

But if you:

```
cordon
   ↓
drain
   ↓
maintenance
   ↓
uncordon
```

you allow Kubernetes to maintain workloads as much as possible.

This is the core operational philosophy of Kubernetes:

> **Make infrastructure changes while preserving application availability.**

---

# 13. OS Upgrades

Now let's move to the next topic.

An OS upgrade could mean:

```
Ubuntu upgrade
RHEL patching
Kernel upgrade
Security patches
Container runtime updates
System libraries
```

For example:

```
worker-1
    |
    +-- Kubernetes kubelet
    +-- container runtime
    +-- Linux kernel
    +-- Pods
```

You don't want to upgrade the OS while workloads are actively depending on that node.

Therefore:

```
kubectl cordon
        ↓
kubectl drain
        ↓
OS upgrade
        ↓
reboot
        ↓
verify node
        ↓
kubectl uncordon
```

This workflow is fundamental.

---

# 14. What If a Node Is Lost Unexpectedly?

Now imagine:

```
worker-1
     X
  FAILED
```

Maybe:

- hardware failure
- kernel panic
- network failure
- power failure
- disk failure

Kubernetes detects:

```
worker-1   NotReady
```

Check:

```
kubectl get nodes
```

Example:

```
NAME       STATUS
master     Ready
worker-1   NotReady
worker-2   Ready
```

You should investigate:

```
kubectl describe node worker-1
```

And on the actual machine:

```
systemctl status kubelet
```

```
journalctl -u kubelet
```

You may also inspect:

```
systemctl status containerd
```

or:

```
systemctl status docker
```

depending on the runtime.

---

# 15. Kubernetes Versioning

Now we enter the most important part of Cluster Maintenance:

# Cluster Upgrades

Kubernetes releases versions such as:

```
v1.28
v1.29
v1.30
v1.31
v1.32
...
```

A Kubernetes cluster contains multiple components.

For example:

```
Control Plane
│
├── kube-apiserver
├── kube-controller-manager
├── kube-scheduler
├── etcd
└── kubelet

Worker
│
├── kubelet
├── kube-proxy
└── container runtime
```

During an upgrade, these components don't necessarily change simultaneously.

---

# 16. Why Kubernetes Upgrades Are Done Carefully

Imagine:

```
Current:

API Server       v1.30
Controller       v1.30
Scheduler        v1.30
kubelet          v1.30
```

You want:

```
v1.31
```

A Kubernetes upgrade isn't simply:

```
apt upgrade kubernetes
```

There is a controlled sequence.

For kubeadm-managed clusters, the typical conceptual sequence is:

```
1. Upgrade kubeadm
2. kubeadm upgrade plan
3. kubeadm upgrade apply
4. Upgrade kubelet
5. Restart kubelet
6. Drain workers
7. Upgrade worker kubeadm/kubelet
8. Uncordon workers
```

The exact package commands depend on your OS/package repository.

---

# 17. `kubeadm upgrade plan`

Before upgrading:

```
kubeadm upgrade plan
```

This performs preflight checks and shows available upgrade versions.

Think of it as:

```
"What can I safely upgrade to?"
```

It can provide information about:

```
Current cluster version
Available versions
Components
Upgrade path
Potential issues
```

This is why the course emphasizes it.

---

# 18. `kubeadm upgrade apply`

After reviewing the plan, on the control-plane node you apply the upgrade:

```
sudo kubeadm upgrade apply <version>
```

For example:

```
sudo kubeadm upgrade apply v1.31.x
```

The exact version must be one that is valid for your cluster and supported by your kubeadm version.

Conceptually:

```
kubeadm upgrade plan
        ↓
Review
        ↓
kubeadm upgrade apply
        ↓
Control plane upgraded
```

---

# 19. Control Plane vs Worker Upgrade

This distinction is critical.

### Control plane

Contains:

```
API Server
Scheduler
Controller Manager
etcd
```

### Worker

Contains:

```
kubelet
kube-proxy
container runtime
```

Therefore:

```
CONTROL PLANE
      |
      | kubeadm upgrade apply
      ↓
Control plane components
```

Then:

```
WORKER
      |
      | upgrade kubelet/kubeadm
      ↓
Worker components
```

---

# 20. Important CKA Upgrade Mental Model

Remember:

```scss
                 Cluster Upgrade
                       |
             +---------+---------+
             |                   |
        Control Plane          Workers
             |                   |
      kubeadm upgrade       drain node
      apply version              |
             |              upgrade packages
             |                   |
             |              restart kubelet
             |                   |
             |              uncordon node
```

---

# 21. Why Drain Before Worker Upgrade?

Suppose:

```
worker-1
   |
   +-- application Pod
   +-- application Pod
```

You upgrade kubelet while applications are running.

Instead:

```
kubectl drain worker-1 --ignore-daemonsets
```

Then upgrade:

```
kubeadm
kubelet
```

Restart:

```
sudo systemctl restart kubelet
```

Check:

```
kubectl get nodes
```

Then:

```
kubectl uncordon worker-1
```

---

# 22. Kubernetes Upgrade Strategy

For a cluster:

```
control-plane
worker-1
worker-2
worker-3
```

You generally don't upgrade all workers simultaneously.

Instead:

```
Control Plane
      ↓
worker-1
      ↓
worker-2
      ↓
worker-3
```

Why?

Because you want to maintain application capacity.

If you have:

```
3 workers
```

and take all three offline:

```
worker-1 X
worker-2 X
worker-3 X
```

you've effectively removed the cluster's compute capacity.

Instead:

```
worker-1 X
worker-2 Ready
worker-3 Ready
```

then:

```
worker-1 Ready
worker-2 X
worker-3 Ready
```

and so on.

---

# 23. Backup and Disaster Recovery

Now the final major topic.

Kubernetes stores important cluster state.

One of the most important components is:

```
etcd
```

Think of etcd as:

> **The database containing Kubernetes cluster state.**

For example:

```
etcd
 |
 +-- Pods
 +-- Deployments
 +-- Services
 +-- ConfigMaps
 +-- Secrets
 +-- Nodes
 +-- RBAC objects
 +-- Cluster configuration
```

Therefore:

```
etcd backup
     =
cluster-state backup
```

This is extremely important for disaster recovery.

---

# 24. Kubernetes Backup Types

There are two major backup concepts you should distinguish.

### 1. Resource/Object backup

You can export Kubernetes objects:

```
kubectl get deployments -A -o yaml
```

or:

```
kubectl get all -A -o yaml
```

You can also back up specific resources:

```
kubectl get configmap -A -o yaml
kubectl get secret -A -o yaml
```

But this isn't a complete cluster backup.

---

### 2. etcd snapshot

A more complete cluster-state backup is an etcd snapshot:

```
ETCDCTL_API=3 etcdctl snapshot save snapshot.db
```

This captures etcd's data.

For CKA, this is extremely important.

---

# 25. `etcdctl`

`etcdctl` is the command-line client for etcd.

You may see commands such as:

```
ETCDCTL_API=3 etcdctl snapshot save snapshot.db
```

The environment variable:

```
ETCDCTL_API=3
```

specifies the etcd API version.

For Kubernetes clusters using modern etcd:

```
API v3
```

is what you generally use.

---

# 26. etcd Snapshot

Conceptually:

```
Kubernetes
    |
    v
   etcd
    |
    | snapshot
    v
snapshot.db
```

You can store:

```
snapshot.db
```

somewhere safe.

For example:

```
/opt/backup/etcd-snapshot.db
```

But remember:

> A backup sitting on the same failed machine isn't a great disaster-recovery strategy.

In real environments, backups should be copied to durable external storage according to the organization's backup architecture.

---

# 27. Checking an etcd Snapshot

You can inspect a snapshot using:

```
ETCDCTL_API=3 etcdctl snapshot status snapshot.db
```

Depending on the etcdctl version, you may also see options such as:

```
etcdutl snapshot status
```

Modern etcd tooling has evolved, so always pay attention to the version installed in the exam environment.

For CKA, recognize the underlying operation:

```
snapshot save
snapshot status
snapshot restore
```

---

# 28. Restoring etcd

Suppose disaster occurs:

```
etcd
  X
```

You have:

```
snapshot.db
```

You can restore it:

```
ETCDCTL_API=3 etcdctl snapshot restore snapshot.db
```

The restore creates a new etcd data directory.

Conceptually:

```
snapshot.db
     |
     ↓
restore
     |
     ↓
new etcd data directory
     |
     ↓
etcd
     |
     ↓
Kubernetes
```

---

# 29. Very Important: Backup Does Not Mean Restore Is Automatic

Suppose you have:

```
etcd-snapshot.db
```

That doesn't mean:

```
Kubernetes automatically recovers
```

You need to understand:

```
Where is etcd data stored?
What is the etcd endpoint?
Where is the certificate?
Where is the key?
Where is the CA certificate?
What is the new data directory?
How is etcd configured?
```

Typical etcd TLS parameters look like:

```
--endpoints=https://127.0.0.1:2379
```

and certificate-related options such as:

```
--cacert=...
--cert=...
--key=...
```

---

# 30. The Big CKA Picture

You should now have this mental model:

```scss
                 CLUSTER MAINTENANCE
                         |
       +-----------------+------------------+
       |                 |                  |
   Node/OS             Upgrade          Backup
   Maintenance             |                |
       |              +-----+-----+          |
       |              |           |          |
    cordon        Control Plane  Workers     etcd
       |              |           |           |
     drain         kubeadm       drain     snapshot
       |           upgrade        |           |
   maintenance       apply      upgrade     restore
       |              |           |           |
   uncordon           +-----------+           |
                                              |
                                          Disaster
                                          Recovery
```

---

# 31. CKA Commands You Should Memorize

## Node maintenance

```
kubectl get nodes
```

```
kubectl describe node <node>
```

```
kubectl cordon <node>
```

```
kubectl drain <node> --ignore-daemonsets
```

```
kubectl uncordon <node>
```

---

## Kubernetes upgrade

```
kubeadm version
```

```
kubeadm upgrade plan
```

```
kubeadm upgrade apply <version>
```

```
kubectl get nodes
```

---

## Node/package maintenance

Depending on the OS:

```
apt update
apt install kubeadm=<version>
```

or RPM-based systems may use:

```
dnf install kubeadm-<version>
```

Then:

```
kubeadm upgrade node
```

and upgrade kubelet:

```
apt install kubelet=<version>
```

or the corresponding package-manager command.

Then:

```
systemctl daemon-reload
systemctl restart kubelet
```

The exact package syntax varies by repository and Kubernetes version, so on the CKA exam **read the environment carefully rather than blindly copying commands from old tutorials**.

---

# 32. etcd Backup Commands

Core pattern:

```
ETCDCTL_API=3 etcdctl snapshot save <file>
```

Check:

```
ETCDCTL_API=3 etcdctl snapshot status <file>
```

Restore:

```
ETCDCTL_API=3 etcdctl snapshot restore <file>
```

And remember TLS:

```
--endpoints
--cacert
--cert
--key
```

These frequently appear in CKA tasks.

---

# 33. What You Should Understand vs Memorize

### Understand deeply

```
cordon
drain
uncordon
```

Understand why they exist.

```
kubeadm upgrade plan
kubeadm upgrade apply
```

Understand the difference between control-plane and worker upgrades.

Understand:

```
etcd = Kubernetes cluster state
```

Understand:

```
snapshot = backup
restore = disaster recovery
```

### Memorize command patterns

```
kubectl cordon <node>

kubectl drain <node> --ignore-daemonsets

kubectl uncordon <node>

kubeadm upgrade plan

kubeadm upgrade apply <version>

ETCDCTL_API=3 etcdctl snapshot save <file>

ETCDCTL_API=3 etcdctl snapshot status <file>

ETCDCTL_API=3 etcdctl snapshot restore <file>
```

---

# 34. CKA Exam Mental Checklist

When you see:

> "Perform maintenance on node worker-1"

Think:

```
1. kubectl get nodes
2. kubectl cordon worker-1
3. kubectl drain worker-1 --ignore-daemonsets
4. Perform maintenance
5. Verify node
6. kubectl uncordon worker-1
```

When you see:

> "Upgrade Kubernetes"

Think:

```
1. Check current versions
2. Upgrade kubeadm
3. kubeadm upgrade plan
4. kubeadm upgrade apply
5. Upgrade kubelet
6. Restart kubelet
7. Drain workers
8. Upgrade workers
9. Uncordon workers
10. Verify
```

When you see:

> "Back up the cluster"

Think:

```
Kubernetes state
      ↓
    etcd
      ↓
snapshot
```

When you see:

> "Restore the cluster"

Think:

```
snapshot
   ↓
etcd restore
   ↓
etcd
   ↓
Kubernetes state
```

---

## One crucial distinction

Don't confuse these three:

```
cordon  ≠ drain
drain   ≠ delete node
delete node ≠ delete workload
```

For example:

```
kubectl delete node worker-1
```

removes the **Node object from the Kubernetes API**.

It does **not** perform the same safe workload migration procedure as:

```
kubectl drain worker-1
```

This distinction is very important in CKA troubleshooting and maintenance questions.