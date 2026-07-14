# Kube API Server

## 1. **What is the Kube API Server?**
The **Kube API Server** (`kube-apiserver`) is the **central management plane** of Kubernetes — it’s the **entry point** for _all_ cluster interactions.  
Every command, automation, controller action, or dashboard click eventually goes through it.

Think of it as:
> The “brain’s messenger” that receives requests, verifies them, updates the cluster state in etcd, and then informs other components.

It’s the **only component that directly talks to etcd**, ensuring a consistent and validated cluster state.

---
## 2. **Role in the Kubernetes Architecture**
The API server sits at the **core of the control plane** and interacts with:

|Component|Purpose|Interaction with API Server|
|---|---|---|
|`kubectl` / users|Send requests (like creating pods, viewing nodes, scaling deployments)|API Server authenticates and processes|
|`etcd`|Stores all cluster state data|API Server reads/writes data here|
|`controller-manager`|Watches for changes and ensures the desired state is met|Pulls updates from the API Server|
|`scheduler`|Assigns pods to nodes|Watches API Server for unassigned pods|
|`kubelet`|Runs on worker nodes|Reports pod and node status back to API Server|

---
## 3. **Lifecycle of a Request**
Let’s take a simple example:  
When you run `kubectl create -f pod.yaml`, the flow looks like this:
1. **Request sent** → `kubectl` sends a REST API call to `https://<apiserver-ip>:6443`.    
2. **Authentication** → The API server checks your credentials (certificates, tokens, etc.).    
3. **Authorization** → It checks your permissions (RBAC rules).    
4. **Admission Control** → Plugins may modify or validate the request (e.g., LimitRange, ResourceQuota).    
5. **Validation & Persistence** → If valid, the object (Pod, Deployment, etc.) is stored in `etcd`.    
6. **Response** → You get a success message.    
7. **Other components act**:    
    - Scheduler sees the new pod → assigns a node.        
    - Kubelet on that node → pulls the image and runs the container.        
    - Kubelet reports status → API Server updates `etcd`.        

So, all cluster actions _start and end_ at the API server.

---

## 4. **Key Parameters in Configuration**
The `kube-apiserver` binary is usually started as a systemd service or as a static pod (with kubeadm).  
It’s heavily configured using command-line flags. Let’s examine some important ones:

|Flag|Description|
|---|---|
|`--advertise-address`|IP on which the API server advertises itself to other components.|
|`--authorization-mode=Node,RBAC`|Defines authorization modes (who can do what).|
|`--etcd-servers`|URL(s) to the etcd server(s).|
|`--client-ca-file`|The CA cert to verify client requests.|
|`--service-account-key-file`|Used for signing service account tokens.|
|`--enable-admission-plugins`|Enables admission controllers that modify or reject API requests.|
|`--service-cluster-ip-range`|Defines the IP range for internal Kubernetes services.|
|`--tls-cert-file`, `--tls-private-key-file`|Used to secure HTTPS connections.|

These settings enforce _security_, _authorization_, and _communication_ between Kubernetes components.

---
## 5. **Communication Security (TLS/SSL)**
Every connection to the API Server happens over **HTTPS (port 6443)**.  
TLS certificates are used for:
- Authenticating Kubernetes components (API server, kubelet, controller, etc.)    
- Encrypting communication between them    
- Verifying client identity   

Certificates are usually stored under:
`/etc/kubernetes/pki/`

Files you might see:
- `ca.crt` — Root CA certificate    
- `apiserver.crt`, `apiserver.key` — API Server certs    
- `apiserver-kubelet-client.crt` — API Server’s cert for talking to Kubelet    
- `front-proxy-client.crt` — For aggregated API requests (like metrics-server)
    

---

## 6. **How kubeadm Handles the API Server**
When you create a cluster with `kubeadm`, you don’t manually configure the API server.  
Instead:
- kubeadm deploys it as a **static pod** (manifest file at `/etc/kubernetes/manifests/kube-apiserver.yaml`)    
- kubelet on the master node automatically creates the pod    
- The pod runs in the `kube-system` namespace    

You can check it with:
`kubectl get pods -n kube-system | grep apiserver`

and view its configuration:
`cat /etc/kubernetes/manifests/kube-apiserver.yaml`

---

## 7. **Interacting with etcd**
- The API Server is the **only** component that directly communicates with etcd.    
- It keeps the cluster’s desired state (what’s declared) and current state (what’s happening) in sync.    
- Communication uses **TLS certificates** defined by:    
```scss
--etcd-cafile
--etcd-certfile
--etcd-keyfile
--etcd-servers
```
- etcd usually listens on port **2379**.    

---

## 8. **High Availability (HA) Setup**
For production-grade clusters:
- You may have **multiple API server instances** across control-plane nodes.    
- They all connect to a **shared etcd cluster**.    
- A **load balancer** sits in front, distributing traffic on port **6443**.
Example:
```scss
Users / kubectl
        |
   [ Load Balancer ]
        |
   +----------------------+
   |  Control Pane Nodes |
   +----------------------+
     | kube-apiserver 1
     | kube-apiserver 2
     | kube-apiserver 3
```


This prevents downtime if one control plane node fails.

---

## 9. **How to Inspect and Debug**
You can interact with or inspect the API Server in several ways:
```bash
# Check if the pod is running
kubectl get pod -n kube-system -l component=kube-apiserver

# Describe the pod
kubectl describe pod kube-apiserver-master -n kube-system

# View the configuration file (kubeadm setup)
cat /etc/kubernetes/manifests/kube-apiserver.yaml

# View logs
kubectl logs -n kube-system kube-apiserver-master
```

If the API server is down, the whole cluster becomes unresponsive, since all kubectl and component requests depend on it.

---

## 10. **Summary**

|Concept|Description|
|---|---|
|**Main Role**|Acts as the front door and brain of Kubernetes.|
|**Core Functions**|Authenticate, authorize, validate, store state, respond to requests.|
|**Key Port**|6443|
|**Talks to**|etcd (for storage), scheduler, controller, kubelets, kubectl.|
|**Runs as**|Systemd service or static pod (`/etc/kubernetes/manifests/`).|
|**Secured via**|TLS/SSL certificates.|
|**Failure Impact**|Cluster cannot be managed if API server is down.|

---

