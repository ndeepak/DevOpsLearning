# Cluster Upgrade Introduction — CKA Deep Dive

Now we are back to the main topic: **Cluster Upgrades**.

The previous two topics give us the foundation:

```
Software releases
      ↓
Kubernetes versions
      ↓
Component versions
      ↓
Version skew
      ↓
Cluster upgrade
```

The goal here is not just to memorize:

```
kubeadm upgrade plan
kubeadm upgrade apply
```

You should understand **why the upgrade happens in a particular order**, what happens to the control plane, what happens to workers, and how Kubernetes keeps applications running during the process.

One important note before we start: the material you pasted uses older Kubernetes examples such as `1.10`, `1.11`, and `1.12`, and its "three most recent minor versions" statement reflects the historical support model. Modern Kubernetes has a different support window and current version-skew policy. The **upgrade concepts remain useful**, but don't memorize those old numbers as current rules.

---

# 1. What Is a Kubernetes Cluster Upgrade?

Suppose your cluster currently runs:

```
Kubernetes v1.33
```

and you want:

```
Kubernetes v1.34
```

A cluster upgrade means bringing the Kubernetes components and nodes through a supported upgrade process.

Conceptually:

```
                    CURRENT
                   v1.33.x
                       |
                       |
                       v
                 Upgrade Process
                       |
                       |
                       v
                    TARGET
                   v1.34.x
```

But the cluster isn't one single program.

There are multiple components:

```
Control Plane
│
├── kube-apiserver
├── kube-scheduler
├── kube-controller-manager
├── kubeadm
└── kubelet

Workers
│
├── kubelet
├── kube-proxy
└── container runtime
```

And external components such as:

```
etcd
CoreDNS
CNI plugin
CSI components
```

may have their own upgrade considerations.

So a cluster upgrade is really a **coordinated component upgrade**.

---

# 2. Why Can't We Upgrade Everything at Once?

Imagine this production cluster:

```
                 CONTROL PLANE
                      |
                  API Server
                      |
          +-----------+-----------+
          |           |           |
       worker-1    worker-2    worker-3
          |           |           |
        Pods        Pods        Pods
```

Suppose you shut everything down:

```
CONTROL PLANE    X
worker-1         X
worker-2         X
worker-3         X
```

You have a major outage.

Instead, Kubernetes upgrades are designed to allow a controlled transition:

```
Control Plane
      ↓
worker-1
      ↓
worker-2
      ↓
worker-3
```

while maintaining as much application availability as possible.

This is the basic idea behind a **rolling upgrade**.

---

# 3. The API Server Is the Center of the Upgrade

The most important control-plane component to understand is:

```
kube-apiserver
```

Think of it as the central communication endpoint.

```
                    kube-apiserver
                          |
        +-----------------+----------------+
        |                 |                |
  controller         scheduler         kubelets
  manager
```

The other Kubernetes components interact through the API server.

Therefore, Kubernetes version-skew rules are largely expressed relative to the API server version.

The basic historical principle in your course material is:

> **The API server should not be older than components that depend on it, and components should stay within the supported version-skew range.**

Don't memorize the old `1.10/1.9/1.8` numbers from the lesson as current policy. The current Kubernetes version-skew documentation should be used when determining exact supported combinations.

---

# 4. Why Can Components Have Different Versions?

Suppose:

```
API Server       v1.34
Scheduler        v1.33
Controller       v1.33
Worker kubelet   v1.33
```

Why would Kubernetes allow this?

Because otherwise upgrading a cluster would require:

```
Everything
    ↓
Stop
    ↓
Upgrade simultaneously
    ↓
Start
```

That would be extremely disruptive.

Instead, Kubernetes supports carefully controlled version differences.

So an upgrade can look temporarily like:

```
             API Server
                v1.34
                  |
       +----------+----------+
       |                     |
Scheduler                  Worker
v1.33                     kubelet
                          v1.33
```

Then gradually:

```
worker-1 → v1.34
worker-2 → v1.34
worker-3 → v1.34
```

---

# 5. The Most Important Rule

Think:

```
                 API SERVER
                    |
             compatibility
                    |
      +-------------+-------------+
      |             |             |
 Scheduler     Controller      Kubelet
```

The exact allowed skew depends on the current Kubernetes version and component.

Therefore, during a real upgrade:

> **Always check the version-skew policy for the Kubernetes release you are upgrading to.**

For CKA, however, the conceptual model is what matters most:

```
API Server
    ↓
control-plane compatibility
    ↓
worker compatibility
```

---

# 6. `kubectl` Is Different

Your course mentions:

```
kubectl
```

as an exception.

That's because `kubectl` is a client, not a core cluster control-plane component.

Think:

```
You
 |
 v
kubectl
 |
 v
API Server
```

It doesn't run inside the cluster to maintain cluster state.

Therefore, `kubectl` has its own client/server compatibility considerations.

This is different from:

```
kube-apiserver
kube-scheduler
kube-controller-manager
kubelet
```

---

# 7. When Should You Upgrade?

This is where version lifecycle matters.

Suppose:

```
Current:
v1.33
```

and:

```
Available:
v1.34
```

You shouldn't wait until:

```
v1.33
```

is completely unsupported before thinking about the upgrade.

A good operational approach is:

```
New Kubernetes release
        ↓
Test it
        ↓
Check compatibility
        ↓
Check deprecated APIs
        ↓
Upgrade non-production
        ↓
Upgrade production
```

---

# 8. Why Not Jump Multiple Minor Versions?

Suppose:

```
Current = v1.31
Target  = v1.34
```

You might think:

```
v1.31 → v1.34
```

But Kubernetes upgrade paths are constrained by version-skew and kubeadm upgrade rules.

The safer conceptual approach is:

```
v1.31
  ↓
v1.32
  ↓
v1.33
  ↓
v1.34
```

One supported minor release at a time.

This is especially important for kubeadm-managed clusters.

---

# 9. Why Minor Versions Matter

Consider:

```
v1.34.1
```

The:

```
34
```

is the minor version.

A transition:

```
v1.33 → v1.34
```

is a **minor upgrade**.

But:

```
v1.34.1 → v1.34.2
```

is a **patch upgrade**.

The operational complexity is different.

Generally:

```
Patch upgrade
    ↓
bug/security/stability fixes

Minor upgrade
    ↓
features
API changes
deprecations
behavior changes
compatibility considerations
```

Therefore, minor Kubernetes upgrades require much more planning.

---

# 10. The Two Major Parts of a Cluster Upgrade

Your course is correct to divide the process into:

```
Cluster Upgrade
      |
      +----------------+
      |                |
Control Plane       Workers
Upgrade             Upgrade
```

Let's understand each independently.

---

# 11. Control Plane Upgrade

Suppose:

```
Current:

API Server             v1.33
Scheduler              v1.33
Controller Manager     v1.33
```

Target:

```
v1.34
```

The control plane must be upgraded first.

Conceptually:

```
Before:

API Server       v1.33
Scheduler        v1.33
Controller       v1.33

After:

API Server       v1.34
Scheduler        v1.34
Controller       v1.34
```

Workers may temporarily remain:

```
kubelet v1.33
```

subject to supported version skew.

---

# 12. What Happens During Control Plane Upgrade?

This is important.

The API server may become temporarily unavailable during parts of the control-plane maintenance.

During that period:

```
kubectl commands
        |
        X
```

may fail.

Controllers and scheduler may also temporarily stop functioning.

But the worker nodes and containers don't automatically disappear just because the API server is temporarily unavailable.

Imagine:

```
API Server
    X

worker-1
    |
    +-- nginx
    +-- backend

worker-2
    |
    +-- frontend
```

The containers may continue running.

Therefore:

```
Control plane unavailable
        ≠
All application containers immediately stop
```

This is a very important distinction.

---

# 13. But There Is a Risk

Suppose the control plane is unavailable.

Then:

```
Pod crashes
```

The kubelet may still handle local operations, but cluster-level reconciliation depends on the control plane.

For example:

```
Deployment wants:
3 replicas

Actual:
2 replicas
```

The controller manager isn't available to create the missing replica.

Therefore:

```
Control plane outage
       ↓
existing workloads may continue
       ↓
but cluster management/reconciliation is impaired
```

This is why control-plane upgrades should be short and carefully planned.

---

# 14. Control Plane Upgrade Using kubeadm

For a kubeadm-managed cluster, the general process is:

```
1. Upgrade kubeadm
2. kubeadm upgrade plan
3. kubeadm upgrade apply
4. Upgrade kubelet
5. Restart kubelet
6. Verify
```

This is the core CKA workflow.

---

# 15. Step 1 — Upgrade kubeadm

Suppose you're upgrading:

```
v1.33 → v1.34
```

First, install the appropriate:

```
kubeadm v1.34.x
```

The package command depends on your OS and repository configuration.

Conceptually:

```
package-manager install kubeadm=<target-version>
```

The reason for upgrading kubeadm first is simple:

```
Old kubeadm
      |
      X
May not know how to perform
the target-version upgrade

New kubeadm
      |
      v
Understands target release
```

---

# 16. Step 2 — `kubeadm upgrade plan`

Now:

```
kubeadm upgrade plan
```

This is your pre-flight check.

Think:

```
kubeadm upgrade plan
        |
        +-- Current cluster version
        +-- kubeadm version
        +-- Available upgrades
        +-- Control-plane components
        +-- Target version
        +-- Preflight information
```

This is one of the commands you should immediately associate with:

> **"Before upgrading a kubeadm cluster."**

---

# 17. Step 3 — `kubeadm upgrade apply`

Suppose the plan says your target is:

```
v1.34.x
```

You apply the control-plane upgrade:

```
sudo kubeadm upgrade apply v1.34.x
```

The exact version must match the valid target available in your environment.

Conceptually:

```
kubeadm upgrade apply
          |
          v
Control Plane
          |
    +-----+-----+
    |     |     |
   API  Scheduler Controller
```

The command handles the kubeadm-managed control-plane upgrade process.

---

# 18. What About etcd?

Your course says to keep:

```
etcd
CoreDNS
```

aside initially.

That's a useful way to learn the basic Kubernetes upgrade flow.

But in a real cluster upgrade, you absolutely must account for them.

For kubeadm-managed clusters, kubeadm handles certain control-plane upgrade tasks, including etcd considerations, depending on the cluster configuration and release.

The important CKA distinction is:

```
Kubernetes control-plane upgrade
        ≠
"manually upgrade every dependency blindly"
```

Always understand what kubeadm is managing.

---

# 19. Step 4 — Upgrade kubelet

This is one of the biggest points from your lesson.

After:

```
kubeadm upgrade apply
```

the control plane may now be:

```
v1.34
```

but the kubelet on the control-plane node may still be:

```
v1.33
```

Why?

Because:

> **kubeadm does not upgrade the kubelet package for you.**

You must upgrade it separately.

---

# 20. Why `kubectl get nodes` Can Be Confusing

This is an excellent CKA detail.

You might run:

```
kubectl get nodes
```

and see:

```
NAME       STATUS   VERSION
master     Ready    v1.33.x
worker-1   Ready    v1.33.x
worker-2   Ready    v1.33.x
```

even though you just upgraded the control plane to:

```
v1.34
```

Why?

Because the `VERSION` shown for a node corresponds to the **kubelet/node version**, not simply:

```
"What version is the API server?"
```

This is extremely important.

---

# 21. Two Different Things

After `kubeadm upgrade apply`:

```
Control Plane

API Server
v1.34

Scheduler
v1.34

Controller Manager
v1.34
```

But:

```
Node kubelet
v1.33
```

Therefore:

```
kubectl get nodes
```

can still show:

```
v1.33
```

for that node.

Then you upgrade the kubelet.

---

# 22. Step 5 — Restart kubelet

After installing the appropriate kubelet version:

```
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

Then:

```
kubectl get nodes
```

You should eventually see the expected node version.

---

# 23. Control Plane Upgrade — Complete Picture

So:

```
                CONTROL PLANE UPGRADE

                     v1.33
                       |
                       v
              Upgrade kubeadm
                       |
                       v
             kubeadm upgrade plan
                       |
                       v
             kubeadm upgrade apply
                       |
                       v
                 Control Plane
                     v1.34
                       |
                       v
                Upgrade kubelet
                       |
                       v
                 Restart kubelet
                       |
                       v
                    Verify
```

This is the sequence you should know for CKA.

---

# 24. Now the Workers

Suppose after control-plane upgrade:

```
Control Plane    v1.34
worker-1         v1.33
worker-2         v1.33
worker-3         v1.33
```

Now we upgrade the workers.

The safest common strategy is:

```
worker-1
   ↓
worker-2
   ↓
worker-3
```

one at a time.

---

# 25. Why One Worker at a Time?

Suppose:

```
worker-1
worker-2
worker-3
```

are all running application replicas.

If you upgrade all three simultaneously:

```
worker-1   X
worker-2   X
worker-3   X
```

you've removed all compute capacity.

Instead:

```
worker-1   X
worker-2   Ready
worker-3   Ready
```

Applications can continue using worker-2 and worker-3.

Then:

```
worker-1   Ready
worker-2   X
worker-3   Ready
```

and so on.

This is the basis of a rolling node upgrade.

---

# 26. Worker Upgrade — Step 1

Before upgrading worker-1:

```
kubectl get nodes
```

Then:

```
kubectl get pods -A -o wide
```

Find what is running on the node.

---

# 27. Worker Upgrade — Step 2: Drain

Run:

```
kubectl drain worker-1 --ignore-daemonsets
```

This:

```
worker-1
    |
    +-- application Pods
           |
           v
       eviction
           |
           v
controllers recreate them elsewhere
```

Now the node is safe to maintain.

Depending on the workload, you may need other drain options.

---

# 28. Worker Upgrade — Step 3: Upgrade kubeadm

Install the target kubeadm version:

```
kubeadm v1.34.x
```

Again, use the package manager and repository configured for the environment.

---

# 29. Worker `kubeadm upgrade node`

For a worker node, you don't use:

```
kubeadm upgrade apply
```

That is for applying the control-plane upgrade.

Instead, the worker-side process uses:

```
sudo kubeadm upgrade node
```

This updates the node's kubeadm-managed configuration as required.

Think:

```
Control Plane:
kubeadm upgrade apply

Worker:
kubeadm upgrade node
```

This distinction is worth memorizing.

---

# 30. Worker Upgrade — Step 4: Upgrade Kubelet

Then install the target kubelet version:

```
kubelet v1.34.x
```

Restart it:

```
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

Then verify:

```
kubectl get nodes
```

---

# 31. Worker Upgrade — Step 5: Uncordon

Once the node is healthy:

```
kubectl uncordon worker-1
```

Now:

```
worker-1
   |
   +-- Ready
   +-- Scheduling enabled
```

Move to:

```
worker-2
```

and repeat.

---

# 32. Complete Worker Upgrade

The pattern is:

```
worker-1

     ↓
drain
     ↓
upgrade kubeadm
     ↓
kubeadm upgrade node
     ↓
upgrade kubelet
     ↓
restart kubelet
     ↓
verify
     ↓
uncordon
     ↓
worker-1 complete
```

Then:

```
worker-2
```

Then:

```
worker-3
```

---

# 33. Three Worker Upgrade Strategies

Your lesson mentions three strategies.

Let's understand why each exists.

## Strategy 1 — Upgrade everything simultaneously

```
worker-1 ──┐
worker-2 ──┼──> upgrade
worker-3 ──┘
```

### Advantage

Fast.

### Disadvantage

Potential downtime.

If all workloads depend on those workers:

```
All workers unavailable
       ↓
Application unavailable
```

Usually not what you want for production.

---

# 34. Strategy 2 — One Worker at a Time

```
worker-1
   ↓
drain
   ↓
upgrade
   ↓
uncordon

worker-2
   ↓
drain
   ↓
upgrade
   ↓
uncordon

worker-3
   ↓
...
```

This is a classic rolling upgrade.

### Advantage

Workloads can continue running on the remaining workers.

### Disadvantage

Takes longer.

For many clusters, this is the safer approach.

---

# 35. Strategy 3 — Blue/Green Node Replacement

This is a very interesting strategy.

Suppose:

```
OLD

worker-1   v1.33
worker-2   v1.33
worker-3   v1.33
```

Instead of upgrading existing machines, create:

```
NEW

worker-4   v1.34
worker-5   v1.34
worker-6   v1.34
```

Now:

```
OLD NODES              NEW NODES

worker-1 v1.33         worker-4 v1.34
worker-2 v1.33         worker-5 v1.34
worker-3 v1.33         worker-6 v1.34
```

Move workloads onto the new nodes.

Then remove the old nodes.

This is conceptually similar to:

```
Blue
 ↓
Green
```

or infrastructure replacement.

---

# 36. Why Is Strategy 3 Powerful?

Because you can prepare the new infrastructure before touching the old infrastructure.

Conceptually:

```
OLD
   |
   | still serving
   |
   +------------------+
                      |
                      v
                 NEW NODES
                      |
                   testing
                      |
                      v
                  migrate
                      |
                      v
                remove OLD
```

This can reduce operational risk.

But it requires:

- Extra capacity
- Infrastructure automation
- Scheduling controls
- Workload migration planning
- Potential storage/network considerations

So it's more operationally involved.

---

# 37. What Happens to Applications During Worker Upgrade?

Suppose:

```
Deployment
replicas: 3
```

Pods:

```
worker-1 → Pod A
worker-2 → Pod B
worker-3 → Pod C
```

Drain worker-1:

```
worker-1 → empty
```

ReplicaSet sees:

```
Desired = 3
Available = 2
```

It creates:

```
Pod A-new
```

Scheduler chooses:

```
worker-2
```

or:

```
worker-3
```

depending on scheduling constraints and available resources.

Result:

```
worker-2 → Pod B + Pod A-new
worker-3 → Pod C
```

Then worker-1 is upgraded.

---

# 38. This Is Why Pod Replicas Matter

If you have:

```
replicas: 3
```

you have much better upgrade resilience than:

```
replicas: 1
```

With:

```
replicas: 1
```

draining its node means the application has to wait for a replacement Pod.

Therefore, application availability during infrastructure maintenance depends heavily on workload design.

---

# 39. PodDisruptionBudget Again

Suppose:

```
apiVersion: policy/v1
kind: PodDisruptionBudget
spec:
  minAvailable: 2
```

and:

```
3 replicas
```

You can safely drain one node.

But if:

```
2 replicas
minAvailable: 2
```

you cannot voluntarily evict one of them without violating the PDB.

This means:

```
Drain
  |
  +-- respects eviction safety
  |
  X
PDB prevents unsafe disruption
```

This is why a CKA drain question can sometimes appear to "hang" or refuse eviction.

---

# 40. What Happens to the API Server During Upgrade?

This deserves another look.

Suppose:

```
API Server
   X
```

during a short control-plane maintenance window.

Then:

```
kubectl get pods
```

may fail.

For example:

```
Unable to connect to the server
```

But:

```
worker-1
   |
   +-- nginx
```

doesn't necessarily stop just because the API server is temporarily unavailable.

Think:

```
Control plane
    |
    | manages/reconciles
    v
Workers
    |
    v
Applications
```

Temporary control-plane interruption primarily affects **management and reconciliation**, not immediate execution of every already-running container.

---

# 41. A Very Important Upgrade Principle

You should now understand why we upgrade:

```
CONTROL PLANE FIRST
        ↓
WORKERS SECOND
```

Because the API server is the reference point for component compatibility.

So:

```
Before:

API Server     v1.33
Workers        v1.33
```

Then:

```
Control plane:

API Server     v1.34
Workers        v1.33
```

Then:

```
Worker upgrade:

API Server     v1.34
worker-1       v1.34
worker-2       v1.33
worker-3       v1.33
```

Then:

```
API Server     v1.34
worker-1       v1.34
worker-2       v1.34
worker-3       v1.33
```

Finally:

```
API Server     v1.34
worker-1       v1.34
worker-2       v1.34
worker-3       v1.34
```

That is the rolling transition.

---

# 42. Important CKA Distinction: `kubeadm upgrade apply` vs `kubeadm upgrade node`

Memorize this:

```
CONTROL PLANE
------------------------------
kubeadm upgrade apply <version>
```

versus:

```
WORKER
------------------------------
kubeadm upgrade node
```

Think:

```
             kubeadm upgrade
                    |
          +---------+---------+
          |                   |
    Control Plane           Worker
          |                   |
        apply                node
```

---

# 43. The Complete CKA Upgrade Flow

Suppose:

```
Current = v1.33.x
Target  = v1.34.x
```

## Control Plane

```
1. Check current cluster
2. Upgrade kubeadm
3. kubeadm upgrade plan
4. kubeadm upgrade apply v1.34.x
5. Upgrade kubelet
6. Restart kubelet
7. Verify
```

## Worker 1

```
1. kubectl drain worker-1
2. Upgrade kubeadm
3. kubeadm upgrade node
4. Upgrade kubelet
5. Restart kubelet
6. Verify
7. kubectl uncordon worker-1
```

## Worker 2

Repeat.

## Worker 3

Repeat.

Finally:

```
kubectl get nodes
```

Expected:

```
NAME       STATUS   VERSION
master     Ready    v1.34.x
worker-1   Ready    v1.34.x
worker-2   Ready    v1.34.x
worker-3   Ready    v1.34.x
```

---

# 44. What Does `kubectl get nodes` Really Tell You?

This is worth emphasizing again.

If you see:

```
NAME       STATUS   VERSION
master     Ready    v1.34.x
worker-1   Ready    v1.33.x
```

don't automatically conclude:

> "The API server is v1.33 on worker-1."

The `VERSION` column is showing the Kubernetes version reported by the node's kubelet.

Therefore:

```
API Server version
```

and:

```
Node/kubelet version
```

are related but not identical concepts.

---

# 45. Upgrade Verification

After everything:

```
kubectl get nodes
```

Then:

```
kubectl get pods -A
```

Then:

```
kubectl get deployments -A
```

Look for:

```
Ready
Running
Available
```

and investigate:

```
Pending
CrashLoopBackOff
ImagePullBackOff
NotReady
```

You should also inspect:

```
kubectl get nodes -o wide
```

---

# 46. What Can Go Wrong During an Upgrade?

This is where real-world understanding becomes important.

Possible problems include:

```
API deprecations
        |
        v
Application breaks
```

```
Insufficient node capacity
        |
        v
Drained Pods remain Pending
```

```
PDB too restrictive
        |
        v
Drain blocked
```

```
Version skew
        |
        v
Unsupported component combination
```

```
Bad package repository
        |
        v
Wrong kubeadm/kubelet version
```

```
CNI incompatibility
        |
        v
Networking problems
```

```
CSI/storage compatibility
        |
        v
Storage problems
```

This is why production Kubernetes upgrades require testing.

---

# 47. The Upgrade Philosophy

The entire topic can be reduced to this:

```
                 SAFE UPGRADE

                   PLAN
                    |
                    v
                 PREPARE
                    |
                    v
              CONTROL PLANE
                    |
                    v
                WORKER-1
                    |
                    v
                WORKER-2
                    |
                    v
                WORKER-3
                    |
                    v
                 VERIFY
```

Not:

```
apt upgrade
      ↓
pray
```

---

# 48. CKA Memory Map

For the exam, I want you to mentally associate these commands with these situations:

|Situation|Command/concept|
|---|---|
|Check nodes|`kubectl get nodes`|
|Inspect node|`kubectl describe node`|
|Stop new scheduling|`kubectl cordon`|
|Evict workloads|`kubectl drain`|
|Allow scheduling|`kubectl uncordon`|
|Check upgrade path|`kubeadm upgrade plan`|
|Upgrade control plane|`kubeadm upgrade apply`|
|Upgrade worker configuration|`kubeadm upgrade node`|
|Upgrade node agent|`kubelet` package|
|Restart node agent|`systemctl restart kubelet`|
|Check cluster workloads|`kubectl get pods -A`|

---

# 49. The One Diagram to Remember

```
                    KUBERNETES UPGRADE

                         Current
                         v1.33.x
                            |
                            v
                  +-------------------+
                  | Upgrade kubeadm   |
                  +---------+---------+
                            |
                            v
                  +-------------------+
                  | kubeadm upgrade    |
                  | plan               |
                  +---------+---------+
                            |
                            v
                  +-------------------+
                  | Control Plane     |
                  | upgrade            |
                  |                   |
                  | upgrade apply      |
                  +---------+---------+
                            |
                            v
                    Upgrade kubelet
                            |
                            v
                    Restart kubelet
                            |
                            v
                    CONTROL PLANE DONE
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
           Worker-1      Worker-2      Worker-3
              |             |             |
            drain         drain         drain
              |             |             |
           upgrade       upgrade       upgrade
              |             |             |
          kubelet       kubelet       kubelet
              |             |             |
          uncordon       uncordon       uncordon
              |             |             |
              +-------------+-------------+
                            |
                            v
                         VERIFY
                            |
                            v
                     CLUSTER READY
```

## The core rule

If you remember only this:

```
CONTROL PLANE FIRST
        ↓
WORKERS ONE AT A TIME
        ↓
DRAIN BEFORE WORKER MAINTENANCE
        ↓
UPGRADE KUBELET SEPARATELY
        ↓
UNCORDON AFTER VERIFICATION
```

And the three most important kubeadm commands:

```
kubeadm upgrade plan
kubeadm upgrade apply <version>
kubeadm upgrade node
```

Then you have the conceptual foundation needed for the **actual CKA cluster upgrade lab**.