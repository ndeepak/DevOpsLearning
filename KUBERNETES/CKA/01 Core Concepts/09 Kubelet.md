# Kubelet
# The Kubelet — Deep Dive
## 1. What Is the Kubelet?
The **Kubelet** is the **primary agent** running on every **node** (both control plane and worker nodes) in a Kubernetes cluster.  
It ensures that the containers described in **Pod manifests** are running and healthy.

You can think of it as the **node manager** — it:
- Registers the node with the **API Server**.    
- Watches for **PodSpecs** assigned to the node.    
- Communicates with the **container runtime** (e.g., containerd, CRI-O, Docker) to run containers.    
- Continuously reports the **status of the node and its pods** to the API Server.    

In short:  
**Kube-scheduler decides _where_ pods run; Kubelet ensures _how_ they actually run.**

---

## 2. Kubelet’s Role in the Kubernetes Architecture
Here’s how the Kubelet fits into the control plane–node communication loop:
1. The **Kube-scheduler** selects a node for a pod.    
2. The **API Server** updates the pod spec in etcd.    
3. The **Kubelet on that node** watches the API Server and sees a new pod assigned to it.    
4. The Kubelet:    
    - Pulls the container image.        
    - Creates and starts containers using the **Container Runtime Interface (CRI)**.        
    - Sets up networking via the **Container Network Interface (CNI)**.        
    - Mounts volumes via the **Container Storage Interface (CSI)**.        
5. It then reports **PodStatus** and **NodeStatus** back to the API Server continuously.    
This back-and-forth is the heartbeat of Kubernetes node operation.

---

## 3. Kubelet Responsibilities
Let’s break down the major responsibilities of the Kubelet:

### a. Node Registration
When a node starts, the Kubelet registers itself with the API Server.  
It reports metadata such as:
- Node name    
- CPU and memory capacity    
- OS and architecture    
- Labels (used for scheduling decisions)    

Command-line flag used:
`--register-node=true`

### b. Pod Lifecycle Management
Kubelet ensures that **the pods assigned to the node are running as desired**.

It:
- Watches for new PodSpecs from the API Server.    
- Starts containers using the runtime.    
- Restarts containers if they crash (based on the pod’s restart policy).    
- Removes containers when pods are deleted.    

Kubelet doesn’t directly create pods unless explicitly told to (for static pods or manifests).

### c. Health Checks and Monitoring
The Kubelet performs:
- **Liveness probes** — checks if the container is still running correctly.    
- **Readiness probes** — checks if the container is ready to serve traffic.    
- **Startup probes** — used to handle long startup times.   
Results of these probes are reported to the control plane and can affect service routing.

### d. Node Status Updates
The Kubelet reports node health every **10 seconds** by default.  
If a node stops reporting for a set timeout, the **Node Controller** in the control plane may mark it as **NotReady** and reschedule pods elsewhere.

---

## 4. Pod Sources — How Kubelet Knows Which Pods to Run
The Kubelet can get PodSpecs from multiple sources:
1. **API Server** — Normal scheduled pods.    
2. **Static Pods** — Local pod manifests placed in a directory like `/etc/kubernetes/manifests`.    
3. **HTTP endpoint** — Rarely used in production, but possible via configuration.    

For example, on control plane nodes:
```scss
/etc/kubernetes/manifests/
├── etcd.yaml
├── kube-apiserver.yaml
├── kube-controller-manager.yaml
└── kube-scheduler.yaml
```

Kubelet automatically creates and manages these static pods without API Server involvement.  
If you delete them using `kubectl delete pod`, they’ll immediately be recreated from the manifest file.

---

## 5. Installation and Service Configuration

### Step 1: Download the Kubelet Binary
`wget https://storage.googleapis.com/kubernetes-release/release/v1.13.0/bin/linux/amd64/kubelet chmod +x kubelet mv kubelet /usr/local/bin/`

### Step 2: Create Systemd Service
File: `/etc/systemd/system/kubelet.service`
```ini
[Service]
ExecStart=/usr/local/bin/kubelet \
  --config=/var/lib/kubelet/kubelet-config.yaml \
  --container-runtime=remote \
  --container-runtime-endpoint=unix:///var/run/containerd/containerd.sock \
  --image-pull-progress-deadline=2m \
  --kubeconfig=/var/lib/kubelet/kubeconfig \
  --network-plugin=cni \
  --register-node=true \
  --v=2
Restart=on-failure
RestartSec=5
```

### Step 3: Start and Enable the Service
```bash
systemctl daemon-reload
systemctl enable kubelet
systemctl start kubelet
systemctl status kubelet
```
---

## 6. Verifying the Kubelet Process
Check if the Kubelet is running:
`ps -aux | grep kubelet`

Example output:
```scss
root    2095  1.8  2.4 960676 98788 ?    Ssl  02:32   0:36 /usr/bin/kubelet \
--bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf \
--kubeconfig=/etc/kubernetes/kubelet.conf \
--config=/var/lib/kubelet/config.yaml \
--cni-bin-dir=/opt/cni/bin \
--cni-conf-dir=/etc/cni/net.d \
--network-plugin=cni
```
Each argument defines a key part of how the Kubelet integrates with Kubernetes networking, storage, and authentication systems.

---
## 7. Important Configuration Files

| File                                     | Description                                       |
| ---------------------------------------- | ------------------------------------------------- |
| `/etc/kubernetes/kubelet.conf`           | Main kubeconfig for Kubelet to talk to API Server |
| `/etc/kubernetes/bootstrap-kubelet.conf` | Used for TLS bootstrapping during join            |
| `/var/lib/kubelet/config.yaml`           | Main Kubelet configuration file                   |
| `/etc/cni/net.d/`                        | CNI network configuration directory               |
| `/opt/cni/bin/`                          | CNI binary directory                              |

---

## 8. TLS Bootstrapping
When a new node joins the cluster, the Kubelet initially uses a **bootstrap token** to authenticate with the API Server.  
It requests a client certificate via the **Certificate Signing Request (CSR)** API.

The control plane’s **Controller Manager** (specifically, the CSR Approving controller) then approves the request, and the Kubelet downloads its own certificate.
This allows secure, authenticated communication between Kubelet and the API Server.
You can view CSRs using:
`kubectl get csr`

---
## 9. Kubelet Logging and Troubleshooting
**Common log locations:**
- `/var/log/syslog` (Ubuntu)
- `journalctl -u kubelet`
- For static pods: check `/etc/kubernetes/manifests`
**Key troubleshooting commands:**
```bash
kubectl describe node <node-name>
kubectl get nodes
kubectl logs <pod> -n kube-system
journalctl -u kubelet -f
```

Common issues:
- Incorrect container runtime endpoint (`--container-runtime-endpoint`)
- Wrong CNI configuration (pods stuck in `ContainerCreating`)
- TLS bootstrap failure (node never joins)    
- Swap enabled (Kubelet requires swap to be disabled)
To disable swap permanently:
`swapoff -a`
Then remove swap entries from `/etc/fstab`.

---
## 10. Kubelet and CKA Exam Tips

|Topic|What You Should Know|
|---|---|
|**Node registration**|Kubelet automatically registers node with API Server|
|**Pod management**|Watches assigned pods and runs them|
|**Static pods**|Managed locally; used for control plane components|
|**TLS bootstrapping**|Handles secure certificate-based authentication|
|**Container runtime**|Communicates via CRI socket (containerd, CRI-O, Docker)|
|**Network setup**|Uses CNI plugin for pod networking|
|**Logs**|View with `journalctl -u kubelet -f`|
|**Exam tasks**|Might include debugging a failed node join or static pod issue|

---
## 11. Summary

| Component               | Description                                                    |
| ----------------------- | -------------------------------------------------------------- |
| **What it is**          | Node agent ensuring pods run as desired                        |
| **Who manages it**      | Systemd (manual setup) or kubeadm (auto-managed)               |
| **Key interactions**    | Talks to API Server, CRI, CNI, and CSI                         |
| **Configuration files** | `/var/lib/kubelet/config.yaml`, `/etc/kubernetes/kubelet.conf` |
| **Failure impact**      | Node marked `NotReady`; pods may get rescheduled               |

---


