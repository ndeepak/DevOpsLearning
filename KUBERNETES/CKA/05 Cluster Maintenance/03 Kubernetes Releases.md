# Kubernetes Releases — From Zero to Understanding

We will build this from:
```
What is a software release?
        ↓
What is a version?
        ↓
What does vX.Y.Z mean?
        ↓
Semantic Versioning
        ↓
How Kubernetes releases versions
        ↓
Kubernetes release history
        ↓
Kubernetes components
        ↓
Component versions
        ↓
Version skew
        ↓
How upgrades actually work
```

---

# 1. What Is a Software Release?
Let's start with the simplest definition.
A **software release** is a particular version of software that is made available for users to install or upgrade to.

For example, imagine you have:
```
MyApplication
```

The developers initially release:

```
MyApplication v1.0.0
```

Later they fix bugs:

```
MyApplication v1.0.1
```

Then they add functionality:

```
MyApplication v1.1.0
```

Then they make a major change:

```
MyApplication v2.0.0
```

So:

```
Software
   |
   +-- v1.0.0
   +-- v1.0.1
   +-- v1.1.0
   +-- v2.0.0
```

Each version represents a particular state of the software.

---

# 2. Why Do We Need Software Versions?

Imagine there were no versions.

You download:

```
kubernetes
```

But you don't know:

- Which code?
- Which features?
- Which bugs?
- Which API behavior?
- Which dependencies?
- Which security fixes?
- Which compatibility guarantees?

Versions solve this.

Instead of:

```
Kubernetes
```

we can say:

```
Kubernetes v1.34.1
```

Now everyone knows approximately which release we're talking about.

---

# 3. What Does `vX.X.X` Mean?

You've probably seen:

```
v1.34.1
```

The general pattern is:

```
vMAJOR.MINOR.PATCH
```

For example:

```
v1.34.1
│ │  │
│ │  └── PATCH
│ └───── MINOR
└─────── MAJOR
```

Let's understand each.

---

# 4. MAJOR Version

The first number is:

```
1
```

in:

```
v1.34.1
```

So:

```
MAJOR = 1
```

Traditionally, in Semantic Versioning, a major version indicates potentially breaking changes.

For example:

```
v1.x.x
```

to:

```
v2.x.x
```

could indicate significant compatibility changes.

However, there is an important Kubernetes-specific point:

> **Kubernetes has remained in the `v1.x` major-version series for many years.**

Therefore, don't assume Kubernetes follows every theoretical SemVer convention exactly as a normal application might.

Kubernetes uses:

```
v1.MINOR.PATCH
```

for its releases.

---

# 5. MINOR Version

Consider:

```
v1.34.1
```

Here:

```
MINOR = 34
```

So:

```
v1.32
v1.33
v1.34
v1.35
```

represent different Kubernetes minor releases.

A minor release can introduce:

- New features
- API changes
- New functionality
- Deprecations
- Behavioral changes
- Improvements
- Bug fixes
- Security fixes

For CKA, the minor version is particularly important.

For example:

```
v1.33
   ↓
v1.34
```

is a Kubernetes minor-version upgrade.

---

# 6. PATCH Version

Consider:

```
v1.34.1
```

The final:

```
1
```

is the patch version.

You might see:

```
v1.34.0
v1.34.1
v1.34.2
v1.34.3
```

Generally, patch releases contain things like:

- Bug fixes
- Security fixes
- Stability improvements
- Critical corrections

You normally don't expect a patch release to introduce an entirely new Kubernetes feature.

Think:

```
v1.34.0
     |
     +-- initial 1.34 release
     |
     +-- v1.34.1
     |     bug/security fixes
     |
     +-- v1.34.2
     |     more fixes
     |
     +-- v1.34.3
           more fixes
```

---

# 7. Example

Take:

```
v1.34.2
```

Break it down:

```
v1.34.2
│ │  │
│ │  └──── Patch = 2
│ └─────── Minor = 34
└───────── Major = 1
```

So:

```
Major   = 1
Minor   = 34
Patch   = 2
```

---

# 8. Why Does Kubernetes Use `v1` for So Long?

This is an interesting Kubernetes-specific topic.

You might wonder:

> "If Kubernetes has been around for years, why is it still v1?"

Because:

```
v1
```

doesn't mean:

> "This software is only one year old."

It represents the major API/release series.

Kubernetes has evolved significantly while remaining within the `v1` series.

So:

```
v1.20
v1.25
v1.30
v1.34
```

are all part of the Kubernetes `v1` major series.

---

# 9. Kubernetes Version Examples

You will commonly see versions like:

```
v1.28.15
v1.29.14
v1.30.10
v1.31.x
v1.32.x
v1.33.x
v1.34.x
```

The exact currently supported versions change over time because Kubernetes has a rapid release lifecycle.

For CKA, what matters conceptually is:

```
v1.XX.0
   |
   +-- minor release

v1.XX.1
   |
   +-- patch release
```

---

# 10. Kubernetes Does Not Release One Giant Binary

This is extremely important.

When we say:

```
Kubernetes v1.34
```

we aren't necessarily talking about one single executable.

Kubernetes is composed of multiple components.

For example:

```
Kubernetes
│
├── kube-apiserver
├── kube-scheduler
├── kube-controller-manager
├── kubelet
├── kube-proxy
├── kubeadm
├── kubectl
└── etcd
```

Each component has its own build/version information.

---

# 11. Kubernetes Architecture

Let's visualize a cluster.

```
                 Kubernetes Cluster

                    CONTROL PLANE
                         |
          +--------------+--------------+
          |              |              |
    kube-apiserver   scheduler    controller-manager
          |
         etcd
          |
          |
    +-----+-----------------------------+
    |                  |                |
 worker-1            worker-2        worker-3
    |                  |                |
 kubelet             kubelet         kubelet
 kube-proxy          kube-proxy      kube-proxy
    |                  |                |
 containers          containers       containers
```

Now let's understand what these components actually do.

---

# 12. kube-apiserver

The API server is essentially the central API endpoint of Kubernetes.

When you execute:

```
kubectl get pods
```

the request goes approximately:

```
kubectl
   |
   v
kube-apiserver
   |
   +----> authentication
   +----> authorization
   +----> admission
   |
   v
etcd / controllers / other components
```

The API server exposes the Kubernetes API.

---

# 13. kube-scheduler

The scheduler determines:

> "Which node should run this Pod?"

For example:

```
Pod
 |
 | scheduler
 v
worker-1
```

It considers things such as:

- CPU
- Memory
- Node selectors
- Affinity
- Taints/tolerations
- Topology constraints
- Other scheduling rules

---

# 14. kube-controller-manager

The controller manager contains various controllers.

For example:

```
Deployment
ReplicaSet
Node
Job
Namespace
ServiceAccount
```

Controllers continuously compare:

```
Desired State
      vs
Current State
```

Example:

```
Desired replicas = 3
Current replicas = 2
```

Controller:

```
"Need one more."
```

Then a replacement Pod gets created.

---

# 15. etcd

etcd is the distributed key-value store used by Kubernetes for cluster state.

Think:

```
etcd
 |
 +-- Pods
 +-- Deployments
 +-- Services
 +-- Secrets
 +-- ConfigMaps
 +-- Nodes
 +-- RBAC
 +-- Cluster configuration
```

This is why etcd is extremely important for:

```
Backup
Restore
Disaster Recovery
```

---

# 16. kubelet

kubelet runs on each node.

Its job is approximately:

> "Make sure the containers described for this node are actually running."

Architecture:

```
API Server
     |
     v
 kubelet
     |
     v
container runtime
     |
     v
containers
```

The kubelet communicates with the container runtime through the CRI.

Modern Kubernetes commonly uses:

```
containerd
```

or another CRI-compatible runtime.

---

# 17. kube-proxy

`kube-proxy` runs on nodes and participates in implementing Kubernetes Service networking.

For example:

```
Client
  |
  v
Service
  |
  v
kube-proxy/networking rules
  |
  +----> Pod A
  +----> Pod B
  +----> Pod C
```

Modern Kubernetes networking can involve different implementations and technologies, but for CKA you should understand the traditional role of kube-proxy.

---

# 18. kubeadm

This one is different.

`kubeadm` isn't a continuously running control-plane component like:

```
kube-apiserver
```

Instead, it's a tool used to:

- Initialize clusters
- Join nodes
- Upgrade clusters
- Perform certain cluster lifecycle operations

For example:

```
kubeadm init
```

and:

```
kubeadm join ...
```

and:

```
kubeadm upgrade plan
```

---

# 19. kubectl

`kubectl` is the Kubernetes command-line client.

You use:

```
kubectl get pods
```

```
kubectl get nodes
```

```
kubectl create deployment nginx --image=nginx
```

Conceptually:

```
You
 |
 v
kubectl
 |
 v
API Server
 |
 v
Kubernetes
```

`kubectl` itself isn't the cluster's control plane.

It's a client.

---

# 20. So What Does "Kubernetes v1.34" Actually Mean?

When someone says:

```
Kubernetes v1.34
```

they generally mean the Kubernetes release line where the core Kubernetes components correspond to that minor release.

You could have:

```
kube-apiserver     v1.34.x
kube-scheduler     v1.34.x
controller-manager v1.34.x
kubelet            v1.34.x
kube-proxy         v1.34.x
kubeadm            v1.34.x
kubectl             v1.34.x
```

But **they don't necessarily have to all be identical at every moment**.

This is where Kubernetes **version skew** becomes important.

---

# 21. What Is Version Skew?

Version skew means:

> Different Kubernetes components are running different versions.

For example:

```
Control Plane
    |
    +-- API Server        v1.34
    +-- Scheduler         v1.34
    +-- Controller        v1.34

Worker-1
    |
    +-- kubelet           v1.33

Worker-2
    |
    +-- kubelet           v1.33
```

Is this automatically invalid?

No.

Kubernetes explicitly defines supported version-skew policies.

This is one reason rolling upgrades are possible.

---

# 22. Why Version Skew Exists

Imagine upgrading a large cluster:

```
100 worker nodes
```

You don't want to shut down all 100 simultaneously.

Instead:

```
Control Plane
     ↓
worker-1
     ↓
worker-2
     ↓
worker-3
     ↓
...
     ↓
worker-100
```

During the upgrade process, some nodes will temporarily run an older version.

Kubernetes therefore defines compatibility rules.

---

# 23. Important Version-Skew Principle

For CKA, remember:

> **Don't assume every Kubernetes component must always have exactly the same version.**

Instead, Kubernetes has supported skew relationships between components.

For example, during an upgrade you might temporarily have:

```
API Server       v1.34
kubelet          v1.33
```

before upgrading the worker.

That is part of the reason Kubernetes upgrades can be performed incrementally.

---

# 24. But Version Skew Has Limits

You cannot arbitrarily run:

```
API Server v1.34
kubelet v1.20
```

and expect everything to work.

Kubernetes publishes version-skew policies specifying supported combinations.

Therefore:

```
Supported skew
       ↓
     OK

Unsupported skew
       ↓
     Risk / unsupported
```

This becomes very important when planning cluster upgrades.

---

# 25. Kubernetes Release Cycle

Historically, Kubernetes followed a roughly quarterly minor-release cadence.

The release pattern looks approximately like:

```
v1.30
   ↓
v1.31
   ↓
v1.32
   ↓
v1.33
   ↓
v1.34
   ↓
v1.35
```

Each minor release is followed by patch releases.

For example:

```
v1.34.0
v1.34.1
v1.34.2
v1.34.3
...
```

The exact release schedule and supported versions change over time, so for current production planning you should always check the official Kubernetes release/support documentation rather than relying on an old course.

---

# 26. Kubernetes Release History

Let's understand the history at a high level.

Kubernetes originated at Google and was open-sourced in **2014**.

The first stable Kubernetes release was:

```
v1.0
```

in **2015**.

Since then, Kubernetes has gone through a long sequence of minor releases:

```
v1.0
v1.1
v1.2
v1.3
...
v1.20
v1.21
...
v1.30
v1.31
v1.32
v1.33
v1.34
...
```

The important thing isn't memorizing every version.

For CKA, you should understand the progression:

```
Kubernetes 1.x
      |
      +-- rapidly evolving platform
      |
      +-- new APIs/features
      |
      +-- deprecated APIs
      |
      +-- removed APIs
      |
      +-- security fixes
      |
      +-- performance improvements
```

---

# 27. Why Kubernetes Releases So Frequently

Kubernetes is a very large project with contributions from:

- Cloud providers
- Kubernetes SIGs
- Enterprises
- Open-source developers
- CNCF ecosystem projects

New releases allow the project to introduce:

```
Features
Bug fixes
Security fixes
API improvements
Performance improvements
Deprecations
Graduations from alpha → beta → stable
```

For example, a Kubernetes feature might progress conceptually like:

```
Alpha
  ↓
Beta
  ↓
Stable
```

Not every feature follows exactly the same path, but this is a useful model.

---

# 28. API Version vs Kubernetes Version

This is another concept that confuses beginners.

Consider:

```
Kubernetes v1.34
```

and:

```
apps/v1
```

They are completely different things.

`v1.34`:

```
Kubernetes software release
```

`apps/v1`:

```
Kubernetes API group/version
```

For example:

```
apiVersion: apps/v1
kind: Deployment
```

Here:

```
apps/v1
```

is the API version of the Kubernetes resource.

It does **not** mean the cluster is Kubernetes v1.0.

---

# 29. Another Example

You could have:

```
Kubernetes cluster:
v1.34.x
```

while your Deployment uses:

```
apiVersion: apps/v1
```

This is perfectly normal.

Think:

```
Software version
      ↓
v1.34.x

Resource API version
      ↓
apps/v1
```

Two different concepts.

---

# 30. Kubernetes Components and Version Example

Imagine a cluster during an upgrade:

```
CONTROL PLANE

kube-apiserver
v1.34.1

kube-scheduler
v1.34.1

kube-controller-manager
v1.34.1

etcd
v3.x
```

Worker:

```
WORKER-1

kubelet
v1.33.x

kube-proxy
v1.33.x

containerd
2.x
```

Notice:

```
etcd ≠ Kubernetes version
containerd ≠ Kubernetes version
```

This is another important point.

---

# 31. etcd Has Its Own Version

You might see:

```
Kubernetes
v1.34.x
```

and:

```
etcd
v3.x
```

They don't share the same version number.

For example:

```
Kubernetes v1.34
etcd v3.6.x
```

The exact compatible etcd version depends on the Kubernetes release and distribution.

So don't think:

```
Kubernetes v1.34
etcd v1.34
```

That's incorrect.

---

# 32. Container Runtime Has Its Own Version

Similarly:

```
containerd
```

has its own version.

Example:

```
Kubernetes
v1.34.x

containerd
2.x
```

Again:

```
Kubernetes version
      ≠
container runtime version
```

The runtime must satisfy the Kubernetes version's compatibility requirements.

---

# 33. Linux Kernel Has Its Own Version

And the OS has:

```
Linux kernel
6.x
```

while:

```
kubelet
v1.34.x
```

and:

```
containerd
2.x
```

So a node might look conceptually like:

```
Linux
 └── Kernel 6.x
      |
      ├── containerd 2.x
      |
      └── kubelet v1.34.x
```

This is why "Kubernetes version" does not mean the version of everything installed on the machine.

---

# 34. The Complete Version Stack

Think of a Kubernetes worker like this:

```
+--------------------------------------+
| Kubernetes Workloads                 |
|                                      |
| Pods / Containers                    |
+--------------------------------------+
| Container Runtime                    |
| containerd / CRI-O                  |
+--------------------------------------+
| kubelet                              |
| v1.x.x                               |
+--------------------------------------+
| kube-proxy                           |
| v1.x.x                               |
+--------------------------------------+
| Linux OS / Kernel                    |
| e.g. 6.x                             |
+--------------------------------------+
| Hardware / VM                        |
+--------------------------------------+
```

And the control plane:

```
+--------------------------------------+
| kube-apiserver       v1.x.x          |
| kube-scheduler       v1.x.x          |
| kube-controller      v1.x.x          |
| kubeadm              v1.x.x          |
+--------------------------------------+
| etcd                 v3.x.x          |
+--------------------------------------+
| Linux OS / Kernel                    |
+--------------------------------------+
```

---

# 35. Why This Matters for Cluster Upgrade

Now you can understand why upgrading Kubernetes isn't simply:

```
apt upgrade
```

Suppose you're upgrading:

```
v1.33 → v1.34
```

There are several layers:

```
                  Upgrade
                     |
       +-------------+-------------+
       |                           |
 Control Plane                   Workers
       |                           |
       v                           v
 kubeadm                       kubeadm
       |                           |
       v                           v
 API server                    kubelet
 scheduler                     kube-proxy
 controller                    runtime considerations
       |
       v
     etcd
```

And you need to respect supported version skew.

---

# 36. Why `kubeadm upgrade plan` Exists

Now the command from your previous lesson makes much more sense:

```
kubeadm upgrade plan
```

It essentially helps answer:

```
What version am I running?
What versions can I upgrade to?
What components will change?
Is the cluster ready?
What must I upgrade separately?
```

That's why you should run it before applying an upgrade.

---

# 37. Example Upgrade

Imagine:

```
Current:

Control Plane
v1.33.4

Workers
v1.33.4
```

Target:

```
v1.34.x
```

You don't just immediately run:

```
kubeadm upgrade apply v1.34.x
```

You first establish:

```
Current version
       ↓
Available version
       ↓
Supported upgrade path
       ↓
Preflight checks
       ↓
Upgrade
```

This is the operational mindset CKA wants you to develop.

---

# 38. `kubectl version` and Component Versions

You will encounter commands such as:

```
kubectl version
```

Depending on your kubectl version and server configuration, output can show client/server information.

Also:

```
kubectl get nodes
```

can show node Kubernetes versions:

```
NAME       STATUS   VERSION
master     Ready    v1.34.x
worker-1   Ready    v1.34.x
worker-2   Ready    v1.33.x
```

The `VERSION` column is particularly useful when checking kubelet versions across nodes.

---

# 39. `kubeadm version`

On a kubeadm-managed cluster:

```
kubeadm version
```

shows the installed kubeadm version.

For example:

```
kubeadm version: v1.34.x
```

You should understand:

```
kubeadm version
       ≠
cluster version necessarily
```

during an upgrade process.

That's because you may upgrade the kubeadm package before actually applying the control-plane upgrade.

---

# 40. Version Relationships

A simplified picture:

```
                 Kubernetes Release
                       v1.34.x
                          |
         +----------------+----------------+
         |                |                |
     API Server       Scheduler        Controller
       v1.34.x          v1.34.x           v1.34.x
         |
         |
     +---+-----------------------+
     |                           |
 worker-1                    worker-2
     |                           |
 kubelet                      kubelet
 v1.34.x                      v1.34.x
```

But during a rolling upgrade:

```
API Server
v1.34.x

worker-1 kubelet
v1.34.x

worker-2 kubelet
v1.33.x

worker-3 kubelet
v1.33.x
```

may temporarily exist, subject to Kubernetes' supported version-skew rules.

---

# 41. One More Important Concept: Deprecated APIs

Software releases don't only add things.

They can also remove old functionality.

For example, conceptually:

```
Old release
   |
   +-- API v1beta1
```

Later:

```
New release
   |
   +-- API v1
```

Eventually:

```
Old API
   |
   X
removed
```

Therefore, before upgrading Kubernetes, you should care about:

```
API deprecations
API removals
```

An application that works perfectly on:

```
v1.30
```

might fail after an upgrade to:

```
v1.34
```

if it depends on an API that was removed.

This is one reason production Kubernetes upgrades require preparation rather than simply updating packages.

---

# 42. Release vs Upgrade

Don't confuse:

```
Release
```

with:

```
Upgrade
```

### Release

The Kubernetes project publishes a new version:

```
v1.34.0
```

### Upgrade

You take **your cluster** from:

```
v1.33.x
```

to:

```
v1.34.x
```

So:

```
Kubernetes project
       |
       | releases
       v
v1.34
       |
       | you perform upgrade
       v
Your cluster now runs v1.34
```

A release can exist without your cluster being upgraded.

---

# 43. Release History — What You Actually Need for CKA

You do **not** need to memorize:

```
v1.1 → v1.2 → v1.3 → ...
```

Instead understand these concepts:

```
Kubernetes
   |
   +-- Major: 1
   |
   +-- Minor releases: 30, 31, 32, 33, 34...
   |
   +-- Patch releases: .0, .1, .2...
```

And:

```
Minor release
    ↓
features + changes + deprecations

Patch release
    ↓
bug/security/stability fixes
```

---

# 44. The Most Important Versioning Distinction

You now have several different versions:

```
Kubernetes release
      |
      +-- v1.34.x

API version
      |
      +-- apps/v1

etcd version
      |
      +-- v3.x

containerd version
      |
      +-- 2.x

Linux kernel
      |
      +-- 6.x
```

These are **not interchangeable**.

---

# 45. CKA Exam Mental Model

When you see:

```
v1.34.2
```

immediately think:

```
v
|
+-- 1     → major
|
+-- 34    → minor
|
+-- 2     → patch
```

When you see:

```
apiVersion: apps/v1
```

think:

```
Kubernetes API version
```

When you see:

```
kubectl get nodes
```

and:

```
VERSION
v1.34.x
```

think:

```
kubelet/node Kubernetes version
```

When you see:

```
kubeadm upgrade plan
```

think:

```
"Before upgrading, determine the valid upgrade path and available versions."
```

When you see:

```
etcd v3.x
```

think:

```
"Separate component with its own version."
```

---

# 46. One Final Diagram

This is the diagram I recommend keeping in your CKA notes:

```
                         KUBERNETES

                           Release
                             |
                           v1.34.2
                             |
              +--------------+--------------+
              |              |              |
           Major           Minor          Patch
             1              34              2


                  Kubernetes Components
                           |
       +-------------------+-------------------+
       |                   |                   |
 Control Plane           Workers            Storage
       |                   |                   |
       |                   |                   |
 API Server             kubelet              etcd
 Scheduler              kube-proxy           v3.x
 Controller             runtime
 kubeadm
       |
       +---- versions must follow
             Kubernetes compatibility
             / version-skew rules


                     Applications
                           |
                           v
                    Kubernetes APIs
                           |
                       apps/v1
```

The most important sentence to remember is:

> **A Kubernetes release is a versioned release of the Kubernetes platform, while individual components, APIs, the container runtime, etcd, and the operating system have their own versions and compatibility rules.**


## References:
[https://kubernetes.io/docs/concepts/overview/kubernetes-api/](https://kubernetes.io/docs/concepts/overview/kubernetes-api/)

Here is a link to Kubernetes documentation if you want to learn more about this topic (You don’t need it for the exam, though):

[https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md)

[https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api_changes.md](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api_changes.md)


