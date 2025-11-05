# Kubernetes Architecture — Complete Guide

---
## 1. Overview
Before setting up a Kubernetes cluster, it’s crucial to understand **how Kubernetes is structured** — the **components**, **their roles**, and **how they interact**.
Kubernetes architecture revolves around **two main parts**:
- **Control Plane (Master Node)** — brain of the cluster.    
- **Worker Nodes** — machines that actually run your applications (containers).    

Together, they form a **cluster**.

---

## 2. Clusters and Nodes
### Node
- A **Node** is a **physical or virtual machine** where Kubernetes runs.    
- It is a **worker** that hosts containerized applications.    
- Each node runs:    
    - `kubelet` (agent)        
    - `container runtime` (e.g., Docker, CRI-O)        
    - `kube-proxy` (networking component)        

 _Older Kubernetes documentation called nodes “minions.”_
 
---

### Cluster
- A **cluster** = multiple nodes working together.    
- Provides:    
    - **High Availability** — if one node fails, others continue running workloads.        
    - **Scalability** — workloads can be distributed or expanded across multiple nodes.        
- Workloads are **scheduled** and **balanced** across nodes by the **Control Plane**.    

---

## 3. Master Node (Control Plane)
The **master node** acts as the brain of the cluster. It manages overall cluster operations such as scheduling, monitoring, and failure handling. The master node hosts critical components that form the Kubernetes control plane.
It manages:
- The **cluster state**    
- **Scheduling** and **deployment**    
- **Monitoring** and **health checks*
   
- **Failure recovery**    

### Key Components on the Master Node

|Component|Description|
|---|---|
|**kube-apiserver**|The front-end of Kubernetes. Exposes the Kubernetes API that users, CLI (`kubectl`), and components interact with. All communication passes through it.|
|**etcd**|A distributed **key-value store** that stores the entire cluster configuration and state (like database for Kubernetes).|
|**kube-scheduler**|Detects new Pods (unscheduled workloads) and assigns them to appropriate nodes based on resource availability, taints, and affinity rules.|
|**kube-controller-manager**|Runs various controllers that continuously monitor the cluster’s desired state (e.g., node controller, replication controller, endpoint controller).|
|**cloud-controller-manager** _(optional)_|Integrates Kubernetes with cloud-specific services like load balancers or storage volumes (used in GCP, AWS, Azure).|

---

## 4. Worker Node Components
Each **worker node** runs services that actually execute and manage your application containers.

|Component|Description|
|---|---|
|**kubelet**|Node agent that ensures containers are running as expected on the node. Communicates with the API server to receive Pod specs.|
|**container runtime**|Software that actually runs containers (e.g., **Docker**, **CRI-O**, or **containerd**).|
|**kube-proxy**|Manages networking rules and handles communication between services and pods (load balancing, routing, etc.).|

---

## 5. How the Components Work Together
1. **User or DevOps Engineer** issues a command using `kubectl` → goes to `kube-apiserver`.    
2. **API Server** authenticates and validates the request.    
3. **etcd** stores or updates cluster state data.    
4. **Scheduler** checks pending Pods and finds the best node for deployment.    
5. **Controller Manager** ensures the cluster’s actual state matches the desired state.    
6. **kubelet** on the selected node receives instructions → starts containers using the container runtime.    
7. **kube-proxy** manages network routing so that services and pods communicate correctly.

Think of Kubernetes as:
> “API Server = Brain, etcd = Memory, Scheduler = Planner, Controllers = Executors, Nodes = Workers.”

---

## 6. Distribution of Components

|Role|Components|
|---|---|
|**Master Node**|kube-apiserver, etcd, scheduler, controller-manager|
|**Worker Node**|kubelet, container runtime, kube-proxy|

This separation ensures:
- **Scalability** (add more worker nodes easily)    
- **Resilience** (if one control-plane node fails, others can take over in HA setups)    

---

## 7. Key Kubernetes Component Deep Dive
### etcd (Key-Value Store)
- Stores **cluster configuration**, **state**, and **metadata**.    
- Ensures **synchronization** between masters in multi-master clusters.    
- Implements **locking mechanisms** to prevent data conflicts.    
- Without etcd → Kubernetes loses its memory of what exists.    
---

### Scheduler
- Detects new pods (unscheduled workloads).    
- Chooses the **best available node** based on:    
    - CPU/memory resources        
    - Node labels and taints        
    - Pod affinity/anti-affinity rules        

---

### Controllers
- Continuously monitor and adjust cluster state.    
- Examples:    
    - **Node Controller:** Monitors node health.        
    - **Replication Controller:** Ensures desired pod count.        
    - **Endpoint Controller:** Manages service endpoints.        

---
### Kubelet 
- Agent on every node.    
- Talks to the API Server → pulls pod definitions.    
- Starts containers using the container runtime.    
- Reports node and pod status back to the master.    

---

### Container Runtime
- Responsible for **running containers**.    
- Supported runtimes include:    
    - Docker        
    - containerd        
    - CRI-O        
- Kubernetes uses a **Container Runtime Interface (CRI)** so different runtimes can be plugged in.    

---

## 8. kubectl — The Command-Line Tool
`kubectl` is the **primary CLI tool** to manage Kubernetes clusters.
### Common Commands

|Command|Description|
|---|---|
|`kubectl run hello-minikube`|Deploys a simple application (creates a pod).|
|`kubectl cluster-info`|Displays cluster details (API server, DNS, etc.).|
|`kubectl get nodes`|Lists all nodes in the cluster.|

**Tip:**  
You’ll use `kubectl` daily — learn its options well. It’s the gateway to deploying, managing, and debugging in Kubernetes.

---

## 9. Summary

|Concept|Description|
|---|---|
|**Cluster**|Collection of master and worker nodes.|
|**Master Node (Control Plane)**|Manages and orchestrates the cluster.|
|**Worker Nodes**|Run the containers and report to the master.|
|**etcd**|Stores cluster configuration and state.|
|**kubelet**|Ensures containers run properly on each node.|
|**Scheduler**|Decides where new pods are placed.|
|**Controllers**|Maintain desired cluster state automatically.|
|**kubectl**|CLI tool to interact with the cluster.|

---
