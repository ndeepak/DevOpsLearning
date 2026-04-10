# Kubernetes Architecture
[[KUBERNETES/Kubernetes for Absolute Beginner/Kubernetes Overview/Kubernetes Architecture|Kubernetes Architecture]]
## 1. Overview: What Is Kubernetes?
Kubernetes (K8s) is an **open-source container orchestration system** for automating:
- Deployment of containers    
- Scaling applications    
- Managing container lifecycles    
- Handling networking between containers
You can think of it as an **operating system for your cluster** — it abstracts the underlying infrastructure and exposes APIs to manage workloads declaratively.

## 2. Kubernetes Cluster Architecture
A **Kubernetes Cluster** = **Control Plane (Master)** + **Worker Nodes**.
```pgsql
                    +-----------------------------------+
                    |         Control Plane Node         |
                    |-----------------------------------|
                    | API Server     | etcd              |
                    | Controller Mgr | Scheduler         |
                    +-----------------------------------+
                                 |
                    +-------------------------+
                    | Communication via API   |
                    +-------------------------+
                                 |
      --------------------------------------------------------
      |                         |                            |
+--------------+         +--------------+            +--------------+
| Worker Node1 |         | Worker Node2 |            | Worker Node3 |
|--------------|         |--------------|            |--------------|
| Kubelet      |         | Kubelet      |            | Kubelet      |
| Kube-proxy   |         | Kube-proxy   |            | Kube-proxy   |
| Container R. |         | Container R. |            | Container R. |
+--------------+         +--------------+            +--------------+

```

---

## 3. Control Plane Components (Master Node)
The **Control Plane** manages the state of the entire cluster.
### a. kube-apiserver
- The _front door_ to your cluster.
- Accepts REST requests (via `kubectl`, dashboards, CI/CD pipelines).
- Validates requests and updates the cluster state in **etcd**.
**Scenario Example:**
`kubectl get pods`
This command sends a REST call to the kube-apiserver. The API server authenticates you, queries etcd for pod info, and returns results.


### b. etcd
- A **distributed key-value store** holding the _source of truth_ for your cluster.
- Stores:    
    - Cluster state        
    - ConfigMaps
    - Secrets        
    - Pod specs
    - Service definitions

You can inspect etcd directly (not usually needed in practice, but important in the exam).
**Example command:**
```bash
ETCDCTL_API=3 etcdctl get / --prefix --keys-only
```

(Used only when etcdctl is configured on the control plane.)

---

### c. kube-scheduler
- Assigns Pods to nodes.    
- Watches for unscheduled Pods in the API server.    
- Chooses the **best node** based on:   
    - CPU/memory availability        
    - Taints/Tolerations        
    - Node affinity        
    - Pod affinity/anti-affinity        

**Scenario Example:**  
If you deploy a Pod with:
```yaml
spec:
  nodeSelector:
    disktype: ssd
```

The scheduler ensures this Pod lands on a node labeled `disktype=ssd`.

---

### d. kube-controller-manager
- Runs **controllers** that continuously reconcile the cluster’s _desired state_ vs _current state_.    
- Examples:    
    - **Node controller**: reacts if a node goes offline        
    - **Replication controller**: ensures desired number of Pod replicas        
    - **Endpoint controller**: updates service endpoints        

**Scenario:**  
If a Pod crashes unexpectedly, the controller-manager will detect the mismatch (desired replicas = 3, actual = 2) and recreate one Pod automatically.

---

## 4. Worker Node Components
Worker nodes run the **application workloads** (your Pods and containers).
### a. kubelet
- Node-level agent that communicates with the control plane.    
- Ensures containers defined in PodSpecs are running and healthy.    
- Reports node and Pod status to the API server.    

**Example:**  
If kubelet notices a container crash, it restarts it according to the Pod’s restartPolicy.

---

### b. kube-proxy
- Handles **network routing** for Pods and Services.    
- Maintains network rules (using iptables or IPVS).    
- Forwards traffic to the correct Pod IPs.    

**Scenario:**  
If a Service exposes 3 Pod replicas, kube-proxy ensures incoming requests are load-balanced among them.

---

### c. Container Runtime Engine
- The engine that actually **runs the containers**.    
- Examples:    
    - `containerd`        
    - `CRI-O`        
    - `Docker` (deprecated as runtime but can still be used with containerd under the hood)        

**Verify runtime:**
`ps aux | grep containerd`

---

## 5. Communication Flow Example
Let’s walk through what happens when you deploy a Pod:
1. You run:    
    `kubectl apply -f nginx-pod.yaml`    
2. **kubectl** sends the request → **kube-apiserver**    
3. **API server** validates and stores PodSpec → **etcd**    
4. **Scheduler** detects unscheduled Pod → chooses a node    
5. **kubelet** on that node pulls the container image → starts container via **container runtime**    
6. **Controller-manager** monitors state → keeps desired replicas running    

---

## 6. Practice: Minimal Cluster Commands
```bash
# Get overall cluster info
kubectl cluster-info

# List control plane components
kubectl get componentstatuses  # (deprecated, replaced by...)
kubectl get --raw '/healthz?verbose'

# View all nodes
kubectl get nodes -o wide

# Check node details
kubectl describe node <node-name>

# List pods running in kube-system namespace (control plane)
kubectl get pods -n kube-system -o wide
```

---

## 7. Example Scenario: Cluster Health Verification
After initializing your cluster using `kubeadm init`, verify all system Pods:
`kubectl get pods -n kube-system`
Expected output:
```yaml
NAME                                 READY   STATUS    RESTARTS   AGE
coredns-64897985d-vkzv5              1/1     Running   0          2m
etcd-master                          1/1     Running   0          2m
kube-apiserver-master                1/1     Running   0          2m
kube-controller-manager-master       1/1     Running   0          2m
kube-scheduler-master                1/1     Running   0          2m
kube-proxy-5xkhn                     1/1     Running   0          2m
```
---

## 8. YAML Example – Deploying an Application
**nginx-pod.yaml**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-demo
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 80
```

**Commands:**
```bash
kubectl apply -f nginx-pod.yaml
kubectl get pods
kubectl describe pod nginx-demo
kubectl logs nginx-demo
```

---

## 9. Key Takeaways

|Component|Plane|Role|
|---|---|---|
|**kube-apiserver**|Control|Cluster gateway (all communication passes through it)|
|**etcd**|Control|Persistent cluster state storage|
|**kube-scheduler**|Control|Assigns Pods to nodes|
|**controller-manager**|Control|Maintains desired state|
|**kubelet**|Worker|Ensures Pods run as defined|
|**kube-proxy**|Worker|Handles network routing|
|**Container runtime**|Worker|Runs containers|

---



Nodes
Machines, physical or virtual
Minions
what if it fails?
application fails down
more than one node
Cluster (set of nodes)
Load balancer

Cluster:
Who is responsible, monitor, work load
Master Node
Actual Orchestration

Components:
API Server
	frontend for kubernetes
	user management devices, api services interacts with kubernetes cluster
	
	

ETCD Key value store
	distributed reliable key value store which used to manage the cluster
	when you have multiple nodes in the cluster, it stores all that information on all nodes in the cluster in a distributed manner
	implementing logs within the cluster, to ensure no conflicts between the masters

Scheduler
	distributing work or containers across the nodes
	it looks for newly created containers and assign them nodes

Controller
	brain behind the orchestration
	responsible for noticing and responding when nodes, containers, or endpoints go down.
	it makes decision in such cases

Container Runtime
	it is the underlying software that is used to run containers
	example, docker, containerd
	

Kubelet
	agent
	containers are running in nodes as expected.


---
Master VS Worker Nodes
Master
	kube-api server
	etcd
	controller
	scheduler
	

Worker
	worker nodes
	container runtime
	kubelet

---
Kubectl
	kubectl run hello-minikube
	kubectl cluster info
	kubectl get nodes
	