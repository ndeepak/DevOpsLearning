# Labels and Selectors

## Scheduling → Labels and Selectors
Labels and selectors are fundamental concepts in Kubernetes. They allow you to organize, group, and filter cluster resources in a flexible and scalable way.  
Think of them as tags or key-value pairs that you attach to Kubernetes objects. Selectors then allow you to find objects with matching labels.

This is similar to:
- Tagging videos on YouTube
- Using product filters on an online store
- Categorizing animals by attributes
Labels = metadata you attach  
Selectors = queries you run to find objects with certain labels

Kubernetes uses labels and selectors extensively across **Pods, ReplicaSets, Deployments, Services, Jobs**, and more.

---
# What Are Labels?
Labels are **key-value pairs** attached to Kubernetes objects.
Examples:
```yaml
app: App1
function: Front-end
environment: production
tier: backend
```
Labels help you:
- Group related resources
- Identify resources belonging to a particular application
- Target pods using a Service
- Match pods to a ReplicaSet or Deployment template
---
# Adding Labels in a Pod Manifest
Labels are added under `metadata.labels`.
Example:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp
  labels:
    app: App1
    function: Front-end
spec:
  containers:
    - name: simple-webapp
      image: simple-webapp
      ports:
        - containerPort: 8080
```
After creating the Pod:
`kubectl get pods --selector app=App1`

Output:
```scss
NAME             READY   STATUS      RESTARTS   AGE
simple-webapp    0/1     Completed   0          1d
```
The selector returns **only** pods with `app=App1`.

---
# Labels and Selectors with ReplicaSets
A ReplicaSet manages multiple pods using labels and selectors.  
It uses **matchLabels** in its selector to identify which pods it owns.

Important rule:  
**The selector must match the labels inside the Pod template exactly.**

Correct example:
```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: simple-webapp
  labels:
    app: App1
    function: Front-end
spec:
  replicas: 3
  selector:
    matchLabels:
      app: App1
  template:
    metadata:
      labels:
        app: App1
        function: Front-end
    spec:
      containers:
      - name: simple-webapp
        image: simple-webapp
```

Notes:
- Only the labels inside `template.metadata.labels` are used for pod selection.    
- Labels under `metadata` of the ReplicaSet itself are not used by the selector.    
- You can match by a single label, but use multiple if you want more precision.    

---
# Labels and Selectors with Services
A Kubernetes Service uses selectors to identify which Pods it should send traffic to.

For example:
```yaml
selector:
  app: App1
  function: Front-end
```
The Service routes traffic only to pods with matching labels.
Without labels and selectors, Kubernetes Services cannot correctly identify the backend Pods.

---
# What Are Annotations?
Annotations also store metadata, but are **not** used for selecting or grouping objects.
Use annotations for:
- Build/version details    
- Git commit info    
- Contact information    
- Tooling metadata    
- CI/CD pipeline notes    

Example with annotation:
```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: simple-webapp
  labels:
    app: App1
    function: Front-end
  annotations:
    buildversion: "1.34"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: App1
  template:
    metadata:
      labels:
        app: App1
        function: Front-end
    spec:
      containers:
      - name: simple-webapp
        image: simple-webapp
```
Annotations do not affect scheduling or selection.  
They are used purely for metadata.

---
# Summary

| Feature     | Purpose                          | Used For Scheduling/Selection? |
| ----------- | -------------------------------- | ------------------------------ |
| Labels      | Key-value metadata for grouping  | Yes                            |
| Selectors   | Query to filter objects by label | Yes                            |
| Annotations | Non-identifying metadata         | No                             |

Key points:
- Labels organize Kubernetes resources.    
- Selectors find resources based on those labels.    
- ReplicaSets, Deployments, and Services rely heavily on selectors.    
- Annotations store informational metadata without affecting behavior.   
Mastering labels and selectors is essential for understanding how Kubernetes connects Pods, Services, and workload controllers.