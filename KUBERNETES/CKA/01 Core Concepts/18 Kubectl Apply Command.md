# Kubectl Apply Command

## Introduction

One of the most important commands in Kubernetes is:

```
kubectl apply
```

Almost every production Kubernetes environment uses this command.

Unlike imperative commands (`kubectl create`, `kubectl edit`, `kubectl replace`), `kubectl apply` follows the **Declarative** model.

Instead of telling Kubernetes **how** to perform operations, you tell it **what the desired state should be**, and Kubernetes makes the necessary changes to reach that state.

---

# What is `kubectl apply`?

`kubectl apply` is a command used to **create** or **update** Kubernetes objects using YAML manifest files.

Basic syntax:

```
kubectl apply -f <file.yaml>
```

Example:

```
kubectl apply -f nginx.yaml
```

You can also apply multiple manifests at once:

```
kubectl apply -f ./k8s/
```

or

```
kubectl apply -f /path/to/config-files
```

Every YAML file inside the directory is processed.

---

# Why use `kubectl apply`?

Suppose you have a Pod definition.

```
apiVersion: v1
kind: Pod

metadata:
  name: myapp-pod
spec:
  containers:
  - name: nginx
    image: nginx:1.18
```

When you execute
```
kubectl apply -f nginx.yaml
```

Kubernetes checks:
- Does the object already exist?
- If not, create it.
- If yes, compare it with the desired configuration.
- Update only the changed fields.

This makes `kubectl apply` both a **create** and **update** command.

---

# Example 1: Creating a New Object

Suppose your cluster is empty.

Local YAML

```
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: nginx-container
    image: nginx:1.18
```

Run

```
kubectl apply -f nginx.yaml
```

Output

```
pod/myapp-pod created
```

Internally

```
Local YAML
        │
        ▼
Object Exists?
        │
   No
        │
        ▼
Create Object
        │
        ▼
Store Last Applied Configuration
        │
        ▼
Running Pod
```

---

# Example 2: Updating an Existing Object
Suppose the Pod already exists.

Current image
```
nginx:1.18
```

Now modify the YAML.

```
containers:
- image: nginx:1.19
```

Run
```
kubectl apply -f nginx.yaml
```

Output
```
pod/myapp-pod configured
```

The Pod configuration changes from

```
Image
↓
nginx:1.18
↓
nginx:1.19
```

Only the changed field is updated.

---

# What Happens Internally?
This is the most important part of understanding `kubectl apply`.

When you execute
```
kubectl apply -f nginx.yaml
```

Kubernetes compares **three configurations**.
## 1. Local Configuration
This is your YAML file.
Example
```
spec:
  containers:
  - image: nginx:1.19
```

This represents your desired state.

## 2. Live Configuration
This is the object currently running in Kubernetes.
Example
```
Pod
Image
nginx:1.18
```

This is the actual state in the cluster.

You can view it with:
```
kubectl get pod myapp-pod -o yaml
```

## 3. Last Applied Configuration
This is the configuration previously applied using `kubectl apply`.

It is stored as an annotation on the object.
Example
```
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration
```

This stores the previous version of your manifest.

# Three-Way Merge

Unlike `kubectl replace`, which overwrites the object, `kubectl apply` performs a **three-way merge**.

It compares:
```
                Local YAML
                    │
                    │
                    ▼
        Desired Configuration
                    │
                    │
                    ▼
Current Live Object ◄────────► Last Applied Configuration
                    │
                    │
                    ▼
           Calculate Differences
                    │
                    ▼
          Update Only Changed Fields
```

This intelligent comparison allows Kubernetes to modify only what has changed while preserving other fields.

# Why Three Configurations?
Consider the following scenario.
Last applied YAML
```
labels:
  app: myapp
  type: front-end
```

Live object
```
labels:
  app: myapp
  type: front-end
```

Local YAML
```
labels:
  app: myapp
```

Notice:
The `type` label has been removed.

Without knowing the previous configuration, Kubernetes would not know whether:
- The label should remain.
- The label was intentionally removed.

The last applied configuration provides that history.
# Removing Fields
Suppose your original YAML was
```
metadata:
  labels:
    app: myapp
    type: front-end
```

Later you modify it.
```
metadata:
  labels:
    app: myapp
```

Run
```
kubectl apply -f nginx.yaml
```

Kubernetes compares
```
Last Applied
↓
app

type
Current YAML
↓
app
```

Difference
```
"type" removed
```

Live object becomes
```
labels:
  app: myapp
```

The removed field is deleted automatically.

This is one of the biggest advantages of `kubectl apply`.

---

# Last Applied Configuration Annotation
When `kubectl apply` creates an object for the first time, it stores your YAML inside the object itself.

Example
```
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration:
```

The value looks like
```
{
 "apiVersion":"v1",
 "kind":"Pod",
 "metadata":{
   "name":"myapp-pod"
 }
}
```

It is stored as JSON.

You can view it using
```
kubectl get pod myapp-pod -o yaml
```

Look under
```
metadata:
  annotations:
```

You will find
```
kubectl.kubernetes.io/last-applied-configuration
```

# Why Store This Annotation?

Without it,
Kubernetes only knows
```
Current Cluster
↓
Current YAML
```

It does **not** know what the previous desired state was.

The annotation provides that missing information.

# Internal Workflow

## First Apply

```
Local YAML
        │
        ▼
Object Exists?
        │
      No
        │
        ▼
Create Object
        │
        ▼
Store Annotation
        │
        ▼
Running Object
```

## Second Apply

```
Local YAML
        │
        ▼
Read Live Object
        │
        ▼
Read Annotation
        │
        ▼
Three-way Comparison
        │
        ▼
Patch Object
        │
        ▼
Update Annotation
```

# What If Nothing Changes?
Suppose
Current YAML
```
image: nginx:1.19
```

Live object
```
image: nginx:1.19
```

Run
```
kubectl apply -f nginx.yaml
```

Output
```
pod/myapp-pod unchanged
```

No API update occurs because the desired state already matches the current state.

# Applying Multiple Files
Example directory

```
k8s/
├── deployment.yaml
├── service.yaml
├── configmap.yaml
├── ingress.yaml
```

Run
```
kubectl apply -f k8s/
```

Every manifest is processed.

If
```
Deployment exists
```
↓
Updated

If
```
Service doesn't exist
```
↓
Created

Everything happens with a single command.

---

# `kubectl create` vs `kubectl apply`

## `kubectl create`

```
kubectl create -f nginx.yaml
```

Behavior
```
Object exists?
↓
Yes
↓
AlreadyExists Error
```

It only creates resources and never updates them.

---

## `kubectl apply`

```
kubectl apply -f nginx.yaml
```

Behavior
```
Object exists?
↓
No
↓

Create

Object exists?
↓
Yes
↓
Update
```

A single command handles both creation and updates.

---

# `kubectl replace` vs `kubectl apply`

`replace`
```
kubectl replace -f nginx.yaml
```

Behavior
- Replaces the entire object.
- Fields omitted from the manifest may be removed.
- Does not perform a three-way merge.

`apply`
```
kubectl apply -f nginx.yaml
```

Behavior
- Compares the desired state with the live state.
- Updates only the changed fields.
- Preserves unrelated fields when appropriate.
- Uses the last applied configuration to determine what has changed.

---

# Why Mixing Imperative and Declarative is Dangerous
Suppose you create a Pod using
```
kubectl create -f nginx.yaml
```

or
```
kubectl run nginx --image=nginx
```

These commands do **not** create the `kubectl.kubernetes.io/last-applied-configuration` annotation.

Later you run
```
kubectl apply -f nginx.yaml
```

`kubectl` will warn that the resource was not created with `apply` and may automatically add the annotation. However, because there is no previous declarative history, future merges may not behave as expected if imperative changes continue to be made.

For this reason, avoid alternating between imperative edits (`kubectl edit`, `kubectl set image`, `kubectl replace`, etc.) and declarative management for the same resources in production.

---

# Real Production Workflow

```
Developer
      │
Updates deployment.yaml
      │
      ▼
Git Repository
      │
      ▼
CI/CD Pipeline
      │
      ▼
kubectl apply -f manifests/
      │
      ▼
Kubernetes Cluster
      │
      ▼
Three-way Merge
      │
      ▼
Desired State Achieved
```

This workflow forms the basis of GitOps tools such as Argo CD and Flux.

---

# Best Practices
1. Store all Kubernetes manifests in a Git repository.
2. Use `kubectl apply` for managing resources declaratively.
3. Group related manifests into directories and apply them together.
4. Avoid using `kubectl edit` or `kubectl replace` on production resources managed declaratively.
5. Let CI/CD pipelines or GitOps tools apply changes instead of making manual modifications.

---

# Summary

|Command|Purpose|
|---|---|
|`kubectl apply -f file.yaml`|Create or update a resource declaratively.|
|`kubectl apply -f directory/`|Apply all manifests in a directory.|
|First execution|Creates the object and stores the last applied configuration annotation.|
|Subsequent executions|Performs a three-way merge (Local YAML + Live Object + Last Applied Configuration).|
|If fields are added|Only the new fields are applied.|
|If fields are modified|Only the modified fields are updated.|
|If fields are removed|Kubernetes removes them from the live object based on the last applied configuration.|
|If nothing changed|Reports the resource as `unchanged`.|
|Recommended for|Production deployments, Infrastructure as Code (IaC), CI/CD pipelines, and GitOps workflows.|

## Key Takeaways

- `kubectl apply` is the **standard declarative command** for managing Kubernetes resources.
- It works with **YAML manifests** and automatically **creates or updates** resources.
- It performs a **three-way merge** by comparing the **local manifest**, the **live object**, and the **last applied configuration**.
- The **`kubectl.kubernetes.io/last-applied-configuration`** annotation enables Kubernetes to detect additions, modifications, and removals accurately.
- For long-term management, keep your manifests in Git and use `kubectl apply` consistently instead of mixing imperative and declarative approaches.