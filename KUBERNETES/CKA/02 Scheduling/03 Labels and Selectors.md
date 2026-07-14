# Labels and Selectors
[02 Labels and Selectors](KUBERNETES/KCNA/3%20Scheduling/02%20Labels%20and%20Selectors.md)

Labels and Selectors are among the **most fundamental concepts** in Kubernetes. They are used everywhere—from scheduling Pods to connecting Services, ReplicaSets, Deployments, NetworkPolicies, Jobs, and many other resources.

If you understand Labels and Selectors well, you'll understand **how Kubernetes "connects" different resources together**.

---

# Why Do We Need Labels?
Imagine you have a Kubernetes cluster running hundreds or even thousands of Pods.
```
Cluster

├── Pod
├── Pod
├── Pod
├── Pod
├── Pod
├── Pod
├── Pod
├── Pod
├── Pod
└── Pod
```

Now imagine you want to answer questions like:

- Which Pods belong to the frontend?
- Which Pods are running in production?
- Which Pods belong to Team A?
- Which Pods should receive traffic from a Service?
- Which Pods should a ReplicaSet manage?
- Which Pods should be monitored?

Without a way to organize resources, Kubernetes would have no efficient way to identify them.

This is where **Labels** come in.

# Real World Analogy
Think about an online shopping website.

Suppose you search for laptops.

There are thousands of products.
```
Electronics

Laptop
Phone
Tablet
Camera
Monitor
Printer
```

You apply filters.
```
Brand = Dell
RAM = 16GB
Price < $1000
Operating System = Linux
```

Those filters immediately narrow down the products.

Those product attributes are exactly like Kubernetes labels.

Another example:
YouTube videos.
```
Video

Tags:
Programming
Docker
Kubernetes
Linux
DevOps
```

When someone searches for Kubernetes videos,

YouTube searches the tags.

Again,Tags = Labels

Search Query = Selector
# What is a Label?
A label is simply a **key-value pair** attached to a Kubernetes object.

Example:
```
labels:
  app: nginx
  environment: production
  tier: frontend
```

Here,

|Key|Value|
|---|---|
|app|nginx|
|environment|production|
|tier|frontend|

Labels describe the object.

They do **not** change how the Pod runs.

They simply provide information that other Kubernetes components can use.
# Labels are Metadata
Every Kubernetes object contains metadata.
Example:
```
metadata:
  name: nginx
```

Labels are part of metadata.
```
metadata:
  name: nginx
  labels:
    app: nginx
    tier: frontend
    environment: production
```

Everything inside
```
metadata:
```
describes the object.

Everything inside
```
spec:
```
defines how the object behaves.

# What Can Have Labels?
Almost every Kubernetes object.

Examples
```
Pod
ReplicaSet
Deployment
DaemonSet
StatefulSet
Job
CronJob
Node
Namespace
PersistentVolume
PersistentVolumeClaim
Service
```

This consistency is one of Kubernetes' strengths. Because labels are universal, different resources can work together without needing to know about each other directly.
# Multiple Labels
An object can have one label.
```
labels:
  app: nginx
```

Or many labels.
```
labels:
  app: nginx
  tier: frontend
  version: v1
  team: payments
  environment: production
  region: us-east
```
  
There is no strict limit in everyday usage, but labels should be meaningful and not overloaded with unrelated information.
# Why Multiple Labels?
Suppose you have 100 Pods.
Some belong to
Frontend
Some to Backend
Some to Database

You also have
Development
Testing
Production

You also have
Version 1
Version 2

Now imagine searching.

```
All frontend Pods
AND
Production
AND
Version 2
```

Multiple labels make this possible.
# Example Application
Suppose an e-commerce application.

```
Online Store
Frontend
Backend
Database
Cache
Monitoring
```

We can assign labels.

Frontend
```
labels:
  app: ecommerce
  tier: frontend
```

Backend
```
labels:
  app: ecommerce
  tier: backend
```

Database
```
labels:
  app: ecommerce
  tier: database
```

Monitoring
```
labels:
  app: monitoring
```

Now Kubernetes can distinguish between every workload.

# Creating Labels
Example Pod
```
apiVersion: v1
kind: Pod

metadata:
  name: web
  labels:
    app: ecommerce
    tier: frontend
    environment: production

spec:
  containers:
  - name: nginx
    image: nginx
```

Create it
```
kubectl apply -f pod.yaml
```

---

# Viewing Labels
Display labels:
```
kubectl get pods --show-labels
```

Example
```
NAME      READY   STATUS    LABELS
web       1/1     Running   app=ecommerce,tier=frontend,environment=production
```

Describe Pod
```
kubectl describe pod web
```
You'll find
```
Labels:
app=ecommerce
tier=frontend
environment=production
```

# What is a Selector?
Labels identify objects.
Selectors **find** those objects.
Think of them like SQL queries.
Label
```
app: ecommerce
```

Selector
```
Find all objects
where
app=ecommerce
```

# Simple Selector
Command
```
kubectl get pods --selector app=ecommerce
```

Equivalent logic
```
SELECT *
FROM Pods
WHERE
app=ecommerce
```

Output
```
web
frontend
shopping-cart
checkout
```
# Another Example
Suppose
```
Pod A
app=frontend
```

```
Pod B
app=backend
```

```
Pod C
app=frontend
```

Run
```
kubectl get pods --selector app=frontend
```

Output
```
Pod A

Pod C
```

Backend Pod is ignored.
# Equality-Based Selectors
The simplest selector uses equality.
```
app=frontend
```
Meaning
```
Label app
must equal
frontend
```

Another example
```
environment=production
```
# Multiple Label Selection
Suppose labels
```
labels:
  app: ecommerce
  tier: frontend
  environment: production
```

You can search using multiple labels.
```
kubectl get pods \
--selector app=ecommerce,tier=frontend
```

Meaning
```
app=ecommerce
AND
tier=frontend
```

Only Pods matching **both** labels are returned.

# ReplicaSets and Labels
One of the biggest uses of labels is in ReplicaSets.

Suppose
ReplicaSet
```
Desired Pods
3
```

How does it know which Pods belong to it?
Answer:
Selectors.

Example
```
selector:
  matchLabels:
    app: ecommerce
```

Pod Template
```
template:
  metadata:
    labels:
      app: ecommerce
```
Notice

Both are identical.

# Why Must They Match?
ReplicaSet continuously asks:
```
Show me
all Pods
whose label is
app=ecommerce
```

If only two Pods exist,
ReplicaSet creates another one.

If five Pods exist,
ReplicaSet deletes two.

This is how Kubernetes maintains the desired state.

# Important Rule
This is one of the most common interview questions.
ReplicaSet has labels.
```
metadata:
  labels:
    app: ecommerce
```

Pod Template has labels.
```
template:
  metadata:
    labels:
      app: ecommerce
```

Which labels does ReplicaSet use to identify Pods?
**Answer:**

Only
```
template.metadata.labels
```
The ReplicaSet's own metadata labels are for identifying the ReplicaSet itself, not the Pods it manages.

# Services and Labels
Suppose
Frontend Pods
```
Pod1
app=frontend
```

```
Pod2
app=frontend
```

```
Pod3
app=frontend
```

Backend Pods
```
Pod4
app=backend
```

Service
```
selector:
  app: frontend
```

Result
```
Traffic
↓
Service
↓
Pod1

Pod2

Pod3
```

Backend Pod receives no traffic.
# Deployments and Labels
Deployment creates
ReplicaSet

ReplicaSet creates
Pods

How does Deployment know which ReplicaSet belongs to it?
Labels.

How does ReplicaSet know which Pods belong to it?
Labels.

Everything is connected through labels and selectors.
```
Deployment
↓
ReplicaSet
↓
Pods
```

All coordinated using matching labels.

---

# Labels on Nodes
Labels are not limited to Pods.

Nodes also have labels.

Example
```
kubectl get nodes --show-labels
```

Example labels
```
kubernetes.io/hostname=node01
topology.kubernetes.io/zone=zone-a
node-role.kubernetes.io/control-plane=
```

Administrators can also add custom labels, such as:
```
kubectl label node worker01 disktype=ssd
```

Later, Pods can request nodes with specific labels using mechanisms like `nodeSelector` or node affinity, which we'll cover in upcoming scheduling topics.

# Label Naming Best Practices
Good labels describe stable characteristics of an object.

Examples:
```
app: ecommerce
tier: frontend
environment: production
version: v2
team: payments
```

Avoid labels that change frequently, such as timestamps or rapidly changing metrics. Those belong in annotations or external monitoring systems.
# What are Annotations?
Annotations also store metadata.
Example
```
annotations:
  build-number: "245"
  git-commit: "4baf83d"
  owner: "platform-team"
  documentation: "https://internal.example/docs"
```

Unlike labels,
Annotations are **not searchable using selectors**.
# Labels vs Annotations
Suppose you have a passport.

Important identity information:
```
Name
Nationality
Passport Number
```

These identify you.

Think of these as Labels.

Additional notes:
```
Issued By
Remarks
Visa Notes
Internal Tracking Number
```

These provide extra information but are not used to identify you.

Think of these as Annotations.

# Labels vs Selectors vs Annotations

|Feature|Labels|Selectors|Annotations|
|---|---|---|---|
|Purpose|Identify and categorize objects|Query objects using labels|Store additional metadata|
|Format|Key-value|Query expression|Key-value|
|Used for scheduling|Yes|Yes|No|
|Used by Services|Yes|Yes|No|
|Used by ReplicaSets|Yes|Yes|No|
|Used for documentation|Limited|No|Yes|

# Common Interview Questions
### Can two Pods have the same labels?
Yes.

In fact, that's the primary purpose of labels. A Service or ReplicaSet typically targets multiple Pods that share the same labels.

### Can one Pod have multiple labels?
Yes.
A Pod can have many labels describing different aspects, such as application, environment, version, team, and tier.

### Are labels unique?
No.

Label **keys** on a single object must be unique, but many different objects can share the same label values.

### Can selectors work without labels?
No.
Selectors only evaluate labels. If an object has no matching labels, it cannot be selected.

### Can annotations replace labels?
No.
Annotations are not considered during selection or scheduling. They are intended only for additional metadata.

# Key Takeaways
- **Labels** are key-value pairs that categorize Kubernetes objects.
- **Selectors** are queries that locate objects based on their labels.
- Labels form the foundation of communication between Kubernetes resources such as Services, ReplicaSets, Deployments, and Pods.
- A ReplicaSet manages Pods by matching the labels in its selector with the labels in the Pod template.
- A Service routes traffic only to Pods whose labels match its selector.
- Nodes can also have labels, enabling scheduling decisions through `nodeSelector` and node affinity.
- **Annotations** also store metadata, but they are informational only and are never used for grouping, scheduling, or selection.
- Mastering labels and selectors is essential because they are the "glue" that allows independent Kubernetes components to work together declaratively.


---


## Labs

We have deployed a number of PODs. They are labelled with `tier`, `env` and `bu`. How many PODs exist in the `dev` environment (`env`)?
kubectl get pods --selector env=dev  | wc
7

How many PODs are in the `finance` business unit (`bu`)?
controlplane ~ ➜  kubectl get pods --selector bu=finance  | wc
6

How many objects are in the `prod` environment including PODs, ReplicaSets and any other objects?
```bash
controlplane ~ ➜  kubectl get all --selector env=prod -A
NAMESPACE   NAME              READY   STATUS    RESTARTS   AGE
default     pod/app-1-zzxdf   1/1     Running   0          37m
default     pod/app-2-d4d6q   1/1     Running   0          37m
default     pod/auth          1/1     Running   0          37m
default     pod/db-2-nsxqq    1/1     Running   0          37m

NAMESPACE   NAME            TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
default     service/app-1   ClusterIP   10.43.103.56   <none>        3306/TCP   37m

NAMESPACE   NAME                    DESIRED   CURRENT   READY   AGE
default     replicaset.apps/app-2   1         1         1       37m
default     replicaset.apps/db-2    1         1         1       37m

```

Identify the POD which is part of the `prod` environment, the `finance` BU and of `frontend` tier?
✖ kubectl get pods --selector bu=finance,env=prod,tier=frontend 
NAME          READY   STATUS    RESTARTS   AGE
app-1-zzxdf   1/1     Running   0          39m


A ReplicaSet definition file is given `replicaset-definition-1.yaml`. Attempt to create the replicaset; you will encounter an issue with the file. Try to fix it.
```bash
cat replicaset-definition-1.yaml 
apiVersion: apps/v1
kind: ReplicaSet
metadata:
   name: replicaset-1
spec:
   replicas: 2
   selector:
      matchLabels:
        tier: nginx
   template:
     metadata:
       labels:
        tier: nginx
     spec:
       containers:
       - name: nginx
         image: nginx
```
