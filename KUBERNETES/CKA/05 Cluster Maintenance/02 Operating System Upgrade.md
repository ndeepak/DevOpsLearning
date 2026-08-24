# OS Upgrades in Kubernetes — CKA Deep Dive

This lesson is really about one operational problem:

> **How do you safely take a Kubernetes node offline without unnecessarily disrupting applications?**

The key concepts are:

```
Node maintenance
      |
      +-- cordon
      |
      +-- drain
      |
      +-- OS upgrade / reboot
      |
      +-- uncordon
```

Let's understand the reasoning behind each step.

---

# 1. Why do we need OS upgrades?

A Kubernetes node is ultimately a Linux machine.

For example:

```
worker-1
│
├── Linux OS
├── Kernel
├── containerd
├── kubelet
├── kube-proxy
└── Pods
    ├── nginx
    ├── backend
    └── frontend
```

The operating system periodically needs:

- Security patches
- Kernel updates
- Package updates
- Vulnerability fixes
- Driver updates
- Runtime updates
- System maintenance
- Reboots

The problem is that applications may currently be running on that node.

If you simply do:

```
sudo reboot
```

you are effectively doing:

```
worker-1
   |
   +-- Pod A
   +-- Pod B
   +-- Pod C
          |
          ↓
       REBOOT
          |
          ↓
      EVERYTHING
      TEMPORARILY
      UNAVAILABLE
```

That may cause unnecessary downtime.

Kubernetes therefore gives us a controlled mechanism.

---

# 2. The Safe OS Maintenance Workflow

The basic workflow is:

```
                worker-1
                   |
                   v
               CORDON
                   |
                   v
                DRAIN
                   |
                   v
            OS maintenance
                   |
                   v
                REBOOT
                   |
                   v
             Verify node
                   |
                   v
              UNCORDON
```

Commands:

```
kubectl cordon worker-1
kubectl drain worker-1
# perform OS maintenance
# reboot
kubectl uncordon worker-1
```

But don't just memorize those commands.

You need to understand **why each one exists**.

---

# 3. What Happens When a Node Goes Down?

Suppose your cluster looks like this:

```
             Kubernetes Cluster

       worker-1       worker-2       worker-3
          |              |              |
       Pod A           Pod B           Pod C
       Pod D           Pod E           Pod F
```

Now:

```
worker-1
    X
```

The Pods running on worker-1 are affected.

For example:

```
worker-1
   X
   |
   +-- Pod A
   +-- Pod D
```

Those Pods cannot continue serving traffic normally while their node is unavailable.

What happens next depends heavily on **how those Pods are managed**.

---

# 4. ReplicaSet-Managed Pod vs Standalone Pod

This is extremely important.

Imagine:

```
Deployment
    |
ReplicaSet
    |
    +-- Pod A
    +-- Pod B
    +-- Pod C
```

Suppose Pod A is on:

```
worker-1
```

and worker-1 fails.

The Deployment/ReplicaSet knows:

```
Desired replicas = 3
Current available replicas = 2
```

Therefore Kubernetes attempts to create another Pod:

```
worker-1
   X

worker-2
   |
   +-- Pod B
   +-- Pod A-new

worker-3
   |
   +-- Pod C
```

The important principle is:

> Controllers maintain the desired state.

---

# 5. What About a Standalone Pod?

Suppose you created:

```
kubectl run nginx --image=nginx
```

and it exists as a standalone Pod.

There may be no Deployment or ReplicaSet maintaining it.

If its node disappears:

```
worker-1
   X
   |
   +-- nginx
```

Kubernetes does not have a ReplicaSet saying:

```
"I need one nginx Pod to exist."
```

Therefore, you shouldn't assume that Kubernetes will recreate that Pod somewhere else.

This is one reason Kubernetes applications are normally managed using controllers such as:

```
Deployment
StatefulSet
DaemonSet
Job
CronJob
```

rather than manually created standalone Pods.

---

# 6. The "Five Minute" Concept

The lesson mentions the node being down for around five minutes.

You should understand the general idea rather than treating five minutes as an absolute law.

Kubernetes has node health monitoring and eviction behavior controlled by the control plane's configuration.

When a node becomes unreachable:

```
worker-1
   |
   X
```

the control plane detects:

```
NodeNotReady
```

Eventually, depending on the configured node-monitoring and pod-eviction behavior, workloads may be recreated elsewhere if they are managed by controllers.

For CKA purposes, the important mental model is:

```
Node temporarily unavailable
        |
        v
Control plane detects failure
        |
        v
Controller evaluates desired state
        |
        v
Replacement Pods may be created
```

Don't memorize "exactly five minutes" as though it applies identically to every Kubernetes configuration.

---

# 7. Scenario 1 — Short Maintenance

Suppose:

```
worker-1
```

needs a quick reboot.

You expect:

```
downtime < recovery time
```

and your applications have multiple replicas.

For example:

```
Deployment: frontend
replicas: 3
```

Distribution:

```
worker-1       worker-2       worker-3
   |              |              |
frontend-1    frontend-2    frontend-3
```

If worker-1 goes down:

```
worker-1 X      worker-2       worker-3
                |                 |
             frontend-2       frontend-3
```

There are still two replicas.

If your service is properly configured, users may continue accessing the application.

But this is not the safest general maintenance strategy.

---

# 8. Scenario 2 — Long or Uncertain Maintenance

Suppose:

```
OS upgrade
+
kernel upgrade
+
reboot
+
testing
```

You don't know exactly how long it will take.

This is where you should use:

```
kubectl drain worker-1
```

The purpose is:

> **Gracefully move workloads away before taking the node offline.**

---

# 9. What Does Drain Actually Do?

When you execute:

```
kubectl drain worker-1
```

Kubernetes attempts to:

1. Mark the node unschedulable.
2. Evict eligible Pods.
3. Allow controllers to recreate those Pods elsewhere.
4. Leave the node without normal application workloads.

Conceptually:

```
BEFORE

worker-1
│
├── frontend-1
├── backend-1
└── redis-1
```

After draining:

```
worker-1
│
└── no evictable application Pods

worker-2
│
├── frontend-1
└── backend-1

worker-3
│
└── redis-1
```

Now you can safely work on worker-1.

---

# 10. Why Does Drain Also Cordon?

This is an important detail.

When you drain a node, you don't want Kubernetes to immediately schedule another Pod there while you're trying to empty the node.

Imagine:

```
drain Pod A
     ↓
Pod A recreated on worker-2
```

But if the node were still schedulable, the scheduler could potentially place another workload on worker-1.

You'd end up fighting Kubernetes:

```
Pod removed
   ↓
new Pod scheduled
   ↓
Pod removed
   ↓
new Pod scheduled
```

Therefore draining makes the node:

```
unschedulable
```

as part of the process.

---

# 11. Cordon

Now let's isolate the `cordon` operation.

Run:

```
kubectl cordon worker-1
```

Result:

```
worker-1
STATUS:
Ready,SchedulingDisabled
```

The node is still running.

Existing Pods:

```
Pod A
Pod B
Pod C
```

remain there.

New Pods cannot be scheduled there.

So:

```
CORDON

Existing Pods
     |
     +-- remain

New Pods
     |
     X
   blocked
```

---

# 12. Cordon Does NOT Move Pods

This is one of the most common mistakes.

If you run:

```
kubectl cordon worker-1
```

you have **not** moved anything.

For example:

```
worker-1
│
├── nginx
├── api
└── database
```

After:

```
kubectl cordon worker-1
```

you still have:

```
worker-1
│
├── nginx
├── api
└── database
```

The only change is:

```
No new Pods scheduled here.
```

---

# 13. Drain Actually Removes Workloads

Now:

```
kubectl drain worker-1
```

The goal becomes:

```
worker-1
│
└── application workloads removed
```

and:

```
worker-2
│
├── nginx replacement
├── api replacement
└── ...
```

This is why:

```
cordon ≠ drain
```

---

# 14. Cordon vs Drain

Memorize this table:

|Operation|New Pods|Existing Pods|
|---|---|---|
|`cordon`|Blocked|Stay|
|`drain`|Blocked|Evicted|
|`uncordon`|Allowed|Already-running Pods stay where they are|

The simplest mental model:

```
cordon:
"Don't send anything new here."

drain:
"Empty this node safely."

uncordon:
"Allow scheduling here again."
```

---

# 15. What Happens After the Node Comes Back?

This is another important point from the lesson.

Suppose:

```
worker-1
```

was drained.

The Pods were recreated elsewhere:

```
worker-2
   |
   +-- nginx-1

worker-3
   |
   +-- api-1
```

Then worker-1 comes back:

```
worker-1
   |
   +-- Ready
```

You run:

```
kubectl uncordon worker-1
```

Does Kubernetes automatically move the Pods back?

**No.**

This is extremely important.

After uncordon:

```
worker-1
   |
   +-- can receive NEW Pods
```

But Kubernetes doesn't say:

```
"Hey, nginx used to live here.
Let's move it back."
```

There is no automatic "return to original node" behavior.

---

# 16. Why Doesn't Kubernetes Move Them Back?

Kubernetes scheduling is based on the **current desired state and scheduling constraints**, not historical ownership of a node.

Suppose you have:

```
Deployment
replicas: 3
```

After the drain:

```
worker-2 → Pod A
worker-3 → Pod B
worker-2 → Pod C
```

When worker-1 returns, the desired state is already satisfied:

```
3 replicas = 3 replicas
```

There is no reason to move them.

So:

```
uncordon
```

means:

> This node is eligible for future scheduling.

It does not mean:

> Move workloads back to this node.

---

# 17. Why Cordon Alone Can Be Dangerous

Suppose:

```
worker-1
│
├── frontend
├── backend
└── api
```

You run:

```
kubectl cordon worker-1
```

Now:

```
worker-1
│
├── frontend
├── backend
└── api

Scheduling disabled
```

Existing Pods continue running.

But suppose your application suddenly needs another replica:

```
Deployment
replicas: 4
```

Kubernetes cannot schedule the new replica on worker-1.

It must find another eligible node.

If the remaining nodes don't have sufficient capacity:

```
Pod
 |
 +-- Pending
```

This is why cordoning isn't equivalent to preparing a node for shutdown.

If your intention is:

> "I am about to turn this node off."

you normally want:

```
drain
```

rather than merely:

```
cordon
```

---

# 18. `kubectl drain` in the Real World

In real clusters, this command often encounters problems.

For example:

```
kubectl drain worker-1
```

might produce:

```
error: cannot delete DaemonSet-managed Pods
```

You may then use:

```
kubectl drain worker-1 --ignore-daemonsets
```

This means:

> Don't treat DaemonSet-managed Pods as a reason to fail the drain.

Why?

DaemonSets are specifically designed to run on nodes.

Examples:

```
worker-1
│
├── kube-proxy
├── node-exporter
└── logging-agent
```

These may be DaemonSet-managed.

---

# 19. `emptyDir` and Drain

Another common CKA situation is:

```
Pod uses emptyDir
```

Example:

```
volumes:
  - name: cache
    emptyDir: {}
```

The data in `emptyDir` is tied to that Pod's lifetime on that node.

When the Pod is removed during drain:

```
Pod
 |
 +-- emptyDir
       |
       X
```

the data is lost.

Kubernetes may warn you about this.

Depending on the task and circumstances, you may encounter:

```
kubectl drain worker-1 --ignore-daemonsets --delete-emptydir-data
```

This explicitly permits deletion of Pods using `emptyDir`.

Do not treat that option as harmless: understand that local `emptyDir` contents are ephemeral.

---

# 20. Standalone Pods and `--force`

Suppose:

```
worker-1
│
└── standalone-pod
```

There is no Deployment or ReplicaSet.

Drain may refuse because deleting the Pod could mean permanent workload loss.

In a controlled situation, you may encounter:

```
kubectl drain worker-1 --force
```

But the reasoning is:

```
Why won't drain proceed?
        |
        v
Standalone Pod
        |
        v
No controller will recreate it
```

Therefore, `--force` should not be a command you blindly append to every drain.

---

# 21. PodDisruptionBudget and Drain

Suppose:

```
Deployment
replicas: 3
```

and:

```
minAvailable: 2
```

Your Pods are:

```
worker-1 → Pod A
worker-2 → Pod B
worker-3 → Pod C
```

You attempt:

```
kubectl drain worker-1
```

Evicting Pod A leaves:

```
Pod B
Pod C
```

That's two available replicas, so it may be allowed.

But imagine only:

```
worker-1 → Pod A
worker-2 → Pod B
```

with:

```
minAvailable: 2
```

Trying to evict Pod A would leave:

```
1 available
```

which violates:

```
minAvailable: 2
```

Therefore eviction may be blocked.

This is a key operational concept:

> **A drain respects disruption safety mechanisms.**

---

# 22. Complete OS Upgrade Example

Imagine:

```
NAME       STATUS
master     Ready
worker-1   Ready
worker-2   Ready
worker-3   Ready
```

You need to upgrade the OS on:

```
worker-2
```

First inspect:

```
kubectl get nodes
```

Then:

```
kubectl describe node worker-2
```

Check what workloads are there:

```
kubectl get pods -A -o wide
```

Then:

```
kubectl cordon worker-2
```

Then drain:

```
kubectl drain worker-2 --ignore-daemonsets
```

If appropriate and the task requires it, you may need additional drain flags depending on the Pods present.

Now:

```
worker-2
   |
   +-- maintenance safe
```

Perform the OS work:

```
sudo apt update
sudo apt upgrade
```

or on an RPM-based system:

```
sudo dnf update
```

Then reboot:

```
sudo reboot
```

After it comes back:

```
kubectl get nodes
```

Wait for:

```
worker-2   Ready
```

Then:

```
kubectl uncordon worker-2
```

Finally:

```
kubectl get nodes
kubectl get pods -A -o wide
```

---

# 23. Important: Verify After Maintenance

Don't stop after:

```
kubectl uncordon worker-2
```

Check:

```
kubectl get nodes
```

Then:

```
kubectl get pods -A
```

For application-specific verification:

```
kubectl get deployments -A
```

You want to make sure:

```
Desired = Current = Ready
```

For example:

```
NAME       READY   UP-TO-DATE   AVAILABLE
frontend   3/3     3            3
backend    3/3     3            3
```

---

# 24. The Most Important CKA Scenario

If the question says:

> "Node worker-1 needs to be taken offline for maintenance."

Your brain should immediately execute:

```
          worker-1
             |
             v
        kubectl cordon
             |
             v
         kubectl drain
             |
             v
       OS maintenance
             |
             v
           reboot
             |
             v
      wait until Ready
             |
             v
       kubectl uncordon
             |
             v
          verify
```

Typical command sequence:

```
kubectl get nodes

kubectl cordon worker-1

kubectl drain worker-1 --ignore-daemonsets

# Perform maintenance / reboot

kubectl get nodes

kubectl uncordon worker-1

kubectl get nodes
kubectl get pods -A -o wide
```

---

# 25. One Important Correction to Memorize

Don't think:

```
drain
 ↓
Pods move to another node
```

More accurately:

```
drain
 ↓
Pod is evicted/deleted
 ↓
Controller notices desired replicas are missing
 ↓
Controller creates replacement Pod
 ↓
Scheduler chooses a suitable node
```

This distinction is fundamental to understanding Kubernetes.

For a Deployment:

```
Deployment
    |
ReplicaSet
    |
Pod A
```

After eviction:

```
Deployment
    |
ReplicaSet
    |
Pod A missing
    |
    v
Create replacement
    |
    v
Scheduler
    |
    v
worker-2
```

So Kubernetes isn't literally picking up the existing Pod and carrying it to another node.

**Pods are recreated, not migrated.**

---

# 26. CKA Traps to Watch For

### Trap 1

```
kubectl cordon worker-1
```

does **not** evict existing Pods.

---

### Trap 2

```
kubectl drain worker-1
```

does not mean Kubernetes will move the same Pod object to another node.

Pods are evicted and controllers create replacements.

---

### Trap 3

```
kubectl uncordon worker-1
```

doesn't move old workloads back.

---

### Trap 4

```
kubectl delete node worker-1
```

is **not** the normal maintenance workflow.

---

### Trap 5

Don't blindly use:

```
--force
--delete-emptydir-data
--ignore-daemonsets
```

Understand why the drain needs them.

---

# 27. Final Mental Model

If you remember only one diagram from this lesson, remember this:

```
                 NODE MAINTENANCE

                      worker-1
                         |
                         |
                  "I need to
                   take it down"
                         |
                         v
                    ┌─────────┐
                    │ CORDON  │
                    └────┬────┘
                         |
                  Stop NEW Pods
                         |
                         v
                    ┌─────────┐
                    │  DRAIN  │
                    └────┬────┘
                         |
                  Evict eligible Pods
                         |
                         v
             Controllers recreate Pods
                         |
                         v
                  Other nodes run them
                         |
                         v
                 OS upgrade/reboot
                         |
                         v
                  Node comes back
                         |
                         v
                    ┌─────────┐
                    │UNCORDON  │
                    └────┬────┘
                         |
                  Allow NEW Pods
                         |
                         v
                      Ready
```

And the three commands:

```
kubectl cordon <node>
kubectl drain <node>
kubectl uncordon <node>
```

can be remembered as:

```
CORDON   = STOP NEW
DRAIN    = REMOVE EXISTING
UNCORDON = ALLOW NEW
```

That is the core of **OS Upgrades and Node Maintenance** for CKA.