# Rolling Updates and Rollbacks
This topic is one of the highest probability questions in CKA.

You should understand **how Deployments actually work internally**, not just memorize commands.
# Before We Start
Suppose we have a Deployment.
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 5

  selector:
    matchLabels:
      app: myapp

  template:
    metadata:
      labels:
        app: myapp

    spec:
      containers:
      - name: nginx-container
        image: nginx:1.7.0
```

Create it
```
kubectl apply -f deployment.yaml
```

Immediately Kubernetes starts creating Pods.

But here's something many beginners don't know.

**Deployments never create Pods directly.**

Instead the chain is
```
Deployment
      │
      ▼
ReplicaSet
      │
      ▼
Pods
```

```
               Deployment
                    │
                    ▼
          ReplicaSet (Revision 1)
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      Pod1        Pod2        Pod3
```

This architecture is extremely important.

---

# What is a Rollout?
A rollout means
> Deploying a new version of your application.

Whenever Kubernetes detects a change in the Pod Template, it starts a new rollout.

Examples of changes that trigger a rollout:
- Image version changes
- Environment variables change
- Labels inside Pod template change
- Commands change
- Volumes change
- Resource requests change

Changes that **do not** trigger a rollout:
- Scaling replicas
- Updating Deployment annotations (outside pod template)
- Updating Deployment metadata labels

The important rule:
> Only changes inside **spec.template** create a new ReplicaSet.

---

# Understanding Revisions
Every rollout creates a new Deployment Revision.

Imagine this timeline.
```
Time
 │
 │
 ▼
Revision 1
nginx:1.7.0
↓

Revision 2
nginx:1.7.1
↓

Revision 3
nginx:1.8.0
↓

Revision 4
nginx:1.9.1
```

Each revision represents a complete snapshot of the Pod Template.

Kubernetes stores these revisions so they can be restored later.

---

# What Happens During Deployment Creation?
Suppose we execute
```
kubectl apply -f deployment.yaml
```

Internally Kubernetes performs
```
Deployment Created
↓

ReplicaSet Created
↓

Pods Created
↓

Pods Become Ready
↓

Revision 1 Stored
```

Visualization
```
Deployment
        │
        ▼
ReplicaSet-1
Image:
nginx:1.7.0
        │
        ▼
5 Pods
```

Revision History
```
Revision 1
ReplicaSet A
Image nginx:1.7.0
```

---

# How to Check Rollout Status
```
kubectl rollout status deployment/myapp-deployment
```

Example output
```
Waiting for deployment "myapp-deployment" rollout to finish...
deployment "myapp-deployment" successfully rolled out
```

What does Kubernetes check?
- Desired Pods
- Updated Pods
- Available Pods
- Ready Pods

Only after everything is Ready will rollout finish.

---

# Rollout History
```
kubectl rollout history deployment/myapp-deployment
```

Example
```
REVISION
1
2
3
```

More detailed
```
kubectl rollout history deployment/myapp-deployment --revision=2
```

Example
```
Revision: 2

Image:
nginx:1.7.1
```

---

# Updating a Deployment
Suppose we change
```
nginx:1.7.0
```

to
```
nginx:1.7.1
```

Two methods exist.
## Method 1
Modify YAML
```
containers:
- name: nginx-container
  image: nginx:1.7.1
```

Apply
```
kubectl apply -f deployment.yaml
```
Recommended.

Reason:
The YAML file remains the **source of truth**.

---

## Method 2
Update directly
```
kubectl set image deployment/myapp-deployment \
nginx-container=nginx:1.9.1
```

Example
Before
```
Image
nginx:1.7.0
```

After
```
Image
nginx:1.9.1
```

This changes the Deployment object immediately.

But notice
Your YAML file is still
```
image: nginx:1.7.0
```

This creates configuration drift.

Therefore in production, always update the YAML (or Helm/Kustomize/Git repository) as well.

---

# What Happens Internally?
Suppose we change
```
nginx:1.7.0
↓
nginx:1.7.1
```

Most beginners think Kubernetes simply updates Pods.

It does not.

Instead
```
Old Deployment
↓
New ReplicaSet Created
↓
New Pods Created
↓
Old Pods Deleted
```

Visualization
```
Before
Deployment
      │
ReplicaSet A
Image 1.7.0
      │
5 Pods
```

After update
```
Deployment
      │
 ┌──────────────┐
 │              │
 ▼              ▼
ReplicaSet A    ReplicaSet B
1.7.0           1.7.1
 │              │
Old Pods      New Pods
```

Notice
Both ReplicaSets temporarily coexist.

This is the foundation of Rolling Updates.

---

# Deployment Strategies
Kubernetes supports two deployment strategies.
```
Deployment
├── Recreate
└── RollingUpdate
```

# Strategy 1
## Recreate
Sequence
```
Old Pods
↓
Delete ALL Pods
↓
Application Down
↓
Create New Pods
```

Visualization
```
Old
OOOOO
↓
Delete
-----
↓
Create
NNNNN
```

O = Old Pod
N = New Pod

Problem
Application becomes unavailable.

Downtime exists.

Example
Five replicas
```
OOOOO
↓
00000
↓
NNNNN
```

During
```
00000
```

Nobody can access the application.

# Strategy 2
## Rolling Update
Default strategy.

Instead of deleting everything
```
Old Pod
↓
Delete One
↓
Create One New
↓
Repeat
```

Visualization
```
OOOOO
↓
NOOOO
↓
NNOOO
↓
NNNOO
↓
NNNNO
↓
NNNNN
```

Application remains available.

No downtime.

This is why Kubernetes chooses RollingUpdate by default.

---

# Default Strategy
Check
```
strategy:
  type: RollingUpdate
```

If omitted
Kubernetes automatically uses
```
RollingUpdate
```

---

# RollingUpdate Parameters
The strategy has two important settings.
```
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 25%
    maxSurge: 25%
```

These are frequently asked in interviews and useful for CKA.

## maxUnavailable
How many Pods are allowed to be unavailable during the update.
Example
10 replicas
```
10 Pods
```

```
maxUnavailable = 2
```
Kubernetes may stop 2 Pods.
Remaining
```
8 Pods Running
```

## maxSurge
How many **extra Pods** can temporarily exist.
Example
10 replicas
```
Desired
10
```

```
maxSurge = 2
```
During update
```
12 Pods
```
After completion
```
10 Pods
```
Again.
Temporary only.

Example
Desired
```
10 Pods
```

Configuration
```
maxUnavailable=2
maxSurge=3
```

Maximum
```
13 Pods
```

Minimum available
```
8 Pods
```

# Watching the Rollout
Run
```
kubectl get pods -w
```
During update
You'll observe
```
Old Pod Terminating
↓
New Pod Creating
↓
Ready
↓
Next Pod
```

One after another.
# Describe Deployment
```
kubectl describe deployment myapp-deployment
```
Important fields
```
StrategyType
RollingUpdate
```

```
RollingUpdateStrategy
25%
25%
```

Events
```
Scaled up ReplicaSet
Scaled down ReplicaSet
Scaled up ReplicaSet
Scaled down ReplicaSet
```

These events clearly show the rollout process.
# ReplicaSets During Upgrade
Suppose
Version
```
1.7.0
```
Upgrade
```
1.7.1
```
Before
```
ReplicaSet A
5 Pods
```

After update starts
```
ReplicaSet A
4 Pods

ReplicaSet B
1 Pod
```

Then
```
ReplicaSet A
3 Pods

ReplicaSet B
2 Pods
```

Eventually
```
ReplicaSet A
0 Pods

ReplicaSet B
5 Pods
```

Notice

Old ReplicaSet still exists.

Only its replica count becomes zero.

This is the reason rollbacks are possible.

# Check ReplicaSets
```
kubectl get rs
```

Example
```
NAME                    READY
myapp-5d9c8
0
myapp-7fd99
5
```

Old ReplicaSet
```
0 Pods
```

New ReplicaSet
```
5 Pods
```

---

# Rollback
Suppose version
```
1.9.1
```

contains a bug.

You want
```
1.7.1
```

again.

Command
```
kubectl rollout undo deployment/myapp-deployment
```

Internally
```
Current ReplicaSet
↓
Scaled Down
↓
Previous ReplicaSet
↓
Scaled Up
```

Visualization
```
Before
ReplicaSet A
0 Pods

ReplicaSet B
5 Pods
```

After rollback
```
ReplicaSet A
5 Pods

ReplicaSet B
0 Pods
```

No rebuilding required.

The old ReplicaSet already exists.
# Verify Rollback
```
kubectl get rs
```

```
kubectl rollout history deployment/myapp-deployment
```

```
kubectl describe deployment
```
# Complete Deployment Lifecycle
```
Deployment Created
↓
Revision 1
↓
ReplicaSet A
↓
Pods
↓
Image Updated
↓
Revision 2
↓
ReplicaSet B
↓
Rolling Update
↓
Problem Found
↓
Rollback
↓
ReplicaSet A Active Again
```

---

# Frequently Used Commands (CKA)
Create Deployment
```
kubectl apply -f deployment.yaml
```

List Deployments
```
kubectl get deployments
```

Watch Rollout
```
kubectl rollout status deployment/myapp-deployment
```

Rollout History
```
kubectl rollout history deployment/myapp-deployment
```

Detailed Revision
```
kubectl rollout history deployment/myapp-deployment --revision=2
```

Update Image
```
kubectl set image deployment/myapp-deployment nginx-container=nginx:1.9.1
```

Describe Deployment
```
kubectl describe deployment myapp-deployment
```

List ReplicaSets
```
kubectl get rs
```

Rollback
```
kubectl rollout undo deployment/myapp-deployment
```

Watch Pods During Update
```
kubectl get pods -w
```

---

# CKA Exam Tips
1. A **Deployment never manages Pods directly**. The hierarchy is always:
```
Deployment
    ↓
ReplicaSet
    ↓
Pods
```

2. Any change inside `spec.template` creates a **new ReplicaSet** and a **new Deployment revision**.
3. Scaling (`kubectl scale`) changes the replica count but **does not create a new revision** because the Pod template remains unchanged.
4. **RollingUpdate** is the default deployment strategy and is designed to minimize or eliminate downtime by gradually replacing old Pods with new ones.
5. A rollback does **not recreate** the previous version from scratch. Kubernetes simply scales up the previous ReplicaSet (which was retained) and scales down the current one.
6. During troubleshooting, remember this sequence:

```
kubectl rollout status deployment/<deployment-name>
kubectl rollout history deployment/<deployment-name>
kubectl describe deployment <deployment-name>
kubectl get rs
kubectl get pods -w
```

Understanding how Deployments, ReplicaSets, revisions, and rollout strategies interact internally is the key to answering most CKA questions on rolling updates and rollbacks.