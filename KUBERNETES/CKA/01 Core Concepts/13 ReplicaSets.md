# ReplicaSets
[[Replication Controllers and ReplicaSets]]

## 1. Why ReplicaSets Exist
Imagine you deployed a single **Pod** running your web app.  
If that Pod crashes or the Node hosting it fails, your application goes down. That’s unacceptable for production environments where uptime and reliability are critical.

Kubernetes introduces **ReplicaSets** (and before them, **ReplicationControllers**) to solve this problem.

A **ReplicaSet** ensures that **a specified number of Pod replicas** are running at all times:
- If a Pod fails → it creates a new one.    
- If there are too many Pods → it deletes the extras.    
- If a Node dies → Pods are rescheduled on healthy Nodes.

In short, a ReplicaSet continuously **monitors and maintains the desired number of Pods**, giving your application **high availability** and **automatic recovery**.

---
## 2. ReplicationController vs ReplicaSet

|Feature|ReplicationController|ReplicaSet|
|---|---|---|
|**API Version**|`v1`|`apps/v1`|
|**Selector Field**|Implicit|**Explicit** (must specify `selector`)|
|**Adopts Existing Pods**|Limited|**Yes** (based on label selector)|
|**Current Usage**|Deprecated|**Preferred and modern standard**|

> The ReplicaSet is a more powerful and flexible version of the ReplicationController.  
> It adds **selectors** and forms the foundation for **Deployments** (which you’ll learn next).

---
## 3. Structure of a ReplicaSet YAML File
Every Kubernetes object definition (Pods, ReplicaSets, Deployments, etc.) follows this same structure:
```yaml
apiVersion: <API version>
kind: <Object type>
metadata:
  <Object details>
spec:
  <Desired state of object>
```

Let’s examine this in the context of a ReplicaSet:
```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myapp-replicaset
  labels:
    app: myapp
    type: front-end
spec:
  replicas: 3
  selector:
    matchLabels:
      type: front-end
  template:
    metadata:
      name: myapp-pod
      labels:
        app: myapp
        type: front-end
    spec:
      containers:
        - name: nginx-container
          image: nginx
```

Let’s break this down.

### a. `apiVersion`
Specifies which API version of Kubernetes this object uses.  
For ReplicaSets, this is **`apps/v1`**.

### b. `kind`
Defines the type of object. Here, it’s a **ReplicaSet**.

### c. `metadata`
Gives the ReplicaSet a **unique name** and **labels**.  
Labels help identify and group objects logically.

### d. `spec`
Describes the **desired state** of the ReplicaSet:
- `replicas`: Number of Pod copies you want.    
- `selector`: How Kubernetes knows which Pods belong to this ReplicaSet.    
- `template`: The blueprint for creating Pods.    

### e. `template`
This is **embedded Pod definition** (without `apiVersion` and `kind`):
- The metadata section defines the Pod’s name and labels.    
- The spec section defines containers, images, ports, etc.    

---

## 4. Relationship Between Labels and Selectors
Labels are key–value pairs attached to objects.
Selectors use those labels to “select” which Pods the ReplicaSet manages.
For example:
```yaml
selector:
  matchLabels:
    type: front-end
```
means this ReplicaSet will manage all Pods having:
```yaml
labels:
	type: front-end
```
If you manually created a Pod earlier with the same label, the ReplicaSet will **adopt** it instead of creating a new one.

This label–selector mechanism is a fundamental concept across Kubernetes.

---

## 5. Creating and Managing ReplicaSets
### a. Create a ReplicaSet
`kubectl create -f replicaset-definition.yml`
### b. List ReplicaSets
`kubectl get replicaset`

### c. List Pods Managed by the ReplicaSet
`kubectl get pods`
Pods created by the ReplicaSet will have names derived from it, such as:
```yaml
myapp-replicaset-abc12
myapp-replicaset-def34
myapp-replicaset-ghi56
```

### d. Delete a ReplicaSet
`kubectl delete replicaset myapp-replicaset`

This also deletes all Pods created by it.
### e. Replace / Update a ReplicaSet
If you edit the YAML (for example, changing the image):
`kubectl replace -f replicaset-definition.yml`

---

## 6. Scaling ReplicaSets
Scaling means adjusting the number of replicas.

### Option 1: Edit the YAML file
Change:
`replicas: 3`

to:
`replicas: 6`

and apply:
`kubectl replace -f replicaset-definition.yml`

### Option 2: Use the `scale` command
`kubectl scale --replicas=6 -f replicaset-definition.yml`

or by name:
`kubectl scale --replicas=6 replicaset/myapp-replicaset`

Note:  
Using the scale command updates only the cluster’s current state. The YAML file remains unchanged.

---

## 7. How ReplicaSets Maintain Desired State
Kubernetes continuously compares:
- **Desired state** (from your YAML)    
- **Current state** (actual running Pods)    

If any difference exists, it reconciles automatically.
For example:
- If a Pod crashes, the ReplicaSet creates a new one.    
- If someone manually deletes a Pod, a replacement is immediately launched.    
- If you increase replicas from 3 to 6, three new Pods are created.    

This reconciliation loop is what gives Kubernetes its **self-healing** nature.

---

## 8. Why ReplicaSets Matter
ReplicaSets give you:
- **High availability:** Even if some Pods fail, your app stays online.    
- **Scalability:** Easily add more replicas when demand increases.    
- **Consistency:** All Pods are identical, ensuring predictable behavior.    
- **Automation:** Manual intervention isn’t needed for restarts or rescheduling.    

However, **we rarely use ReplicaSets directly in production.**  
Instead, we use **Deployments**, which manage ReplicaSets for us, providing **versioning**, **rollback**, and **rolling updates**.

---

## 9. Summary Table of Key Commands

|Command|Description|
|---|---|
|`kubectl create -f replicaset-definition.yml`|Create a ReplicaSet|
|`kubectl get replicaset`|List ReplicaSets|
|`kubectl get pods`|List all Pods (including those managed by ReplicaSets)|
|`kubectl delete replicaset myapp-replicaset`|Delete a ReplicaSet|
|`kubectl replace -f replicaset-definition.yml`|Update a ReplicaSet|
|`kubectl scale --replicas=6 -f replicaset-definition.yml`|Scale using a file|
|`kubectl scale --replicas=6 replicaset/myapp-replicaset`|Scale by name|

---
