# Pods
[[KUBERNETES/Kubernetes for Absolute Beginner/Kubernetes Pods Replicasets Deployments/Pods with YAML]]
## What Is a Pod?
A **Pod** is the **smallest deployable unit** in Kubernetes.  
It represents **one instance** of your running application and can contain **one or more containers** that share the same environment.

Think of a **Pod as a wrapper around your containers** — it handles networking, storage, and lifecycle management for them.

---
### Why Pods Exist
When you use Docker alone, you run and manage containers directly:
`docker run python-app`
If you want to scale to 5 instances, you must manually run:
`docker run python-app docker run python-app ...`

You’d then need to manage links, networks, and restarts manually — which quickly becomes unmanageable.
Kubernetes solves this by grouping containers inside Pods and managing them for you.

---
## Pod Structure and Behavior
Each **Pod**:
- Runs on a **worker node** (the actual machine in your cluster).    
- Gets its **own IP address** inside the cluster.    
- Shares **network and storage** between all containers inside it.    
- Is managed automatically by the **Kubelet** on that node.    

When you deploy an app with Kubernetes, you aren’t running containers directly — you’re deploying Pods that contain those containers.

---
## Single-Container Pods (Most Common)
In most cases, each Pod runs **one main container** — for example, a Python web app or an Nginx server.
Example:
```lua
+-------------------------+
| Pod: python-app         |
|--------------------------|
| Container: python:3.11   |
| Application: myapp.py    |
+--------------------------+
```
If traffic grows, Kubernetes doesn’t add containers to the same Pod — it **creates more Pods**:
`Pod-1  Pod-2  Pod-3  Pod-4`
Each Pod runs one instance of your app.

This makes scaling **simple** and **stateless**.

---
## Multi-Container Pods
Sometimes you _do_ want multiple containers in one Pod — when they must share resources tightly and always run together.
Example use case:
- **Main container** → web application.    
- **Helper container** → log processor or file uploader.    

They share:
- **Network (localhost)** → communicate as if on the same machine.    
- **Volumes (storage)** → share files or data.    

Diagrammatically:
```lua
+--------------------------------------------------+
| Pod: web-app                                     |
|--------------------------------------------------|
| Container 1: nginx (main app)                    |
| Container 2: sidecar (helper, logs or proxy)     |
+--------------------------------------------------+
```
These containers are scheduled, started, and stopped **together**.

---
## Pods vs Docker Containers

|Concept|Docker|Kubernetes|
|---|---|---|
|Unit of deployment|Container|Pod|
|Scaling|Run more containers manually|Create more pods automatically|
|Networking|Containers need linking|Pods get internal IPs, auto-managed|
|Storage|Manual volume setup|Volumes declared and shared in spec|
|Lifecycle|Managed manually|Managed by controllers (ReplicaSet, Deployment, etc.)|

---
## Creating a Pod
Simple example:
`kubectl run nginx --image=nginx`
What happens:
- Kubernetes creates a Pod with one container (`nginx`).    
- It downloads the image from Docker Hub.    
- The Kubelet runs it on a worker node.    

Check the pod status:
`kubectl get pods`

Example output:
```sql
NAME                   READY   STATUS    RESTARTS   AGE
nginx-7b6d5f76cf-h5r9f 1/1     Running   0          10s
```
---
## Exposing a Pod
By default, Pods are **internal** — accessible only inside the cluster.  
To make them reachable externally (by users), you must create a **Service**, such as:
- `ClusterIP` – internal access (default)    
- `NodePort` – accessible via node IP + port    
- `LoadBalancer` – cloud load balancer (for production)    

Example:
`kubectl expose pod nginx --type=NodePort --port=80`

---
## Lifecycle and Scaling
- **Scaling up** → Kubernetes creates more Pods.    
- **Scaling down** → Kubernetes removes some Pods.    
- **Pod fails** → Kubernetes automatically recreates it (via ReplicaSet).    

You never edit a running Pod directly. Instead, you define desired state (e.g., 5 replicas) and Kubernetes maintains it.

---
## Summary

|Feature|Description|
|---|---|
|**Pod**|The smallest deployable unit in Kubernetes|
|**Contains**|One or more containers sharing network/storage|
|**Scaling**|Add or remove Pods, not containers|
|**Communication**|Containers inside a Pod talk via `localhost`|
|**Deployment**|Managed by `kubectl`, Deployments, or ReplicaSets|

---
**Key takeaway:**  
Pods are to containers what containers are to processes — a higher-level abstraction that adds structure, isolation, and management capabilities.  
Kubernetes uses Pods to make scaling, deployment, and fault-tolerance automatic and predictable.