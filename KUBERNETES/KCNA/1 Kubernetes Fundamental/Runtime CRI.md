# Runtime CRI

Let’s break down the **Container Runtime Interface (CRI)** step by step — from **history** to **hands-on configuration and inspection examples**, the way you’ll see it in real clusters and exams.

---

## 1. Why the Container Runtime Interface (CRI) Exists
When Kubernetes was first created (around v1.0), it worked **only with Docker**.  
As more container runtimes appeared (rkt, containerd, cri-o, Kata Containers, etc.), maintaining separate integrations became messy.

So the Kubernetes team defined a **common interface**, called **CRI (Container Runtime Interface)** — a [**gRPC-based API**](https://grpc.io/) that allows **Kubelet** to communicate with _any_ container runtime in a standardized way.

**Without CRI:**  
Kubelet → Docker (direct)

**With CRI:**  
Kubelet → CRI API → Runtime (containerd, CRI-O, etc.)

---

## 2. Core Concept
The **CRI** defines two major gRPC services:

| gRPC Service       | Purpose                                                       |
| ------------------ | ------------------------------------------------------------- |
| **RuntimeService** | Manages containers and pods (start, stop, list, exec, attach) |
| **ImageService**   | Manages images (pull, list, remove)                           |
Every runtime that implements these two APIs can plug directly into Kubernetes.

---

## 3. Kubernetes Runtime Communication Flow
```yaml
Kubelet
  |
  | (via gRPC API over Unix socket)
  ↓
CRI Plugin (e.g., containerd-shim, cri-o)
  |
  ↓
Container Runtime Engine (e.g., runc)
  |
  ↓
Containers running on the node
```

- **kubelet** interacts only with the **CRI socket**.    
- The **CRI plugin** translates Kubelet’s requests into container runtime-specific operations.    
- The **runtime engine (runc, crun)** actually spawns and manages Linux containers.    

---

## 4. What Happened to Docker?
### a. Docker Shim
Originally, Kubernetes needed a “bridge” called **dockershim** to communicate with Docker, since Docker did **not implement CRI**.
`Kubelet → Docker Shim → Docker Engine → containerd → runc`
This worked, but it was inefficient (extra translation layers).

### b. Docker Shim Deprecation
In **Kubernetes v1.24**, Docker Shim was **removed**:
- Docker no longer runs as a runtime within Kubernetes.    
- But Docker-built images still work because **Docker images follow the OCI standard**.    
- Kubernetes now works directly with **containerd**, **CRI-O**, or others.  
So, **Docker images are fine**, but **Docker runtime** is no longer used.

---

## 5. OCI and Its Importance
The **Open Container Initiative (OCI)** defines:
- **Image format specification** (how container images are structured)    
- **Runtime specification** (how to run containers)   
This ensures interoperability:  
An image built with Docker can run in containerd, CRI-O, or any OCI-compliant runtime.

---

## 6. Common Container Runtimes Today

|Runtime|Description|Used by|
|---|---|---|
|**containerd**|Lightweight runtime maintained by CNCF; runs inside Docker too|Default for most Kubernetes setups|
|**CRI-O**|Built specifically for Kubernetes, implements CRI natively|Red Hat, OpenShift|
|**gVisor**|Sandbox runtime from Google (security isolation)|GKE, secure workloads|
|**Kata Containers**|Runs lightweight VMs for strong isolation|Cloud-native secure environments|
|**Mirantis Dockershim**|Maintains Docker runtime compatibility|Legacy users migrating from older clusters|

---
## 7. Inspecting the Runtime in Your Cluster
**Step 1: Check the configured runtime**
`ps aux | grep kubelet | grep container-runtime`

Or on most systems:
`cat /var/lib/kubelet/config.yaml | grep runtime`

Typical output:
`containerRuntimeEndpoint: unix:///run/containerd/containerd.sock`

**Step 2: Verify containerd is running**
`sudo systemctl status containerd`

**Step 3: List containers via containerd CLI**
`sudo ctr containers list`

**Step 4: List pods via CRI CLI (crictl)**  
`crictl` is a direct tool to talk to CRI runtimes (useful in exams).
```bash
sudo crictl ps
sudo crictl images
sudo crictl pods
```
If you see results, it means the CRI socket is correctly configured and kubelet is communicating with the runtime.

---
## 8. Configuration Files
### a. kubelet config (runtime definition)
Path: `/var/lib/kubelet/config.yaml`
Example:
```yaml
containerRuntimeEndpoint: unix:///run/containerd/containerd.sock
imageServiceEndpoint: unix:///run/containerd/containerd.sock
```
### b. systemd unit file for kubelet
Path: `/etc/systemd/system/kubelet.service.d/10-kubeadm.conf`
Snippet:
`Environment="KUBELET_EXTRA_ARGS=--container-runtime=remote --container-runtime-endpoint=unix:///run/containerd/containerd.sock"`

Reload and restart kubelet after any change:
```bash
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

---

## 9. Scenario: Switching from Docker to containerd
Imagine you upgraded Kubernetes from v1.23 (Docker) to v1.24 (no Docker Shim).

Here’s how you’d migrate:
```bash
# Stop Docker
sudo systemctl stop docker

# Install containerd
sudo apt install containerd -y

# Configure containerd (generate default config)
sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml

# Start and enable
sudo systemctl enable --now containerd

# Point kubelet to containerd socket
sudo sed -i 's#docker.sock#containerd/containerd.sock#g' /var/lib/kubelet/config.yaml
sudo systemctl restart kubelet
```
Now your cluster uses containerd as its runtime.

---

## 10. Hands-On Test of CRI Communication
```bash
# Verify CRI socket
sudo ls /run/containerd/containerd.sock

# Test via crictl
sudo crictl --runtime-endpoint unix:///run/containerd/containerd.sock info
```

Output should show runtime info:
```json
"runtimeType": "io.containerd.runc.v2",
"version": {
    "containerd": "1.7.0",
    "runc": "1.1.5"
}
```

---

## 11. Summary Table

|Component|Purpose|Communication|
|---|---|---|
|**Kubelet**|Manages Pods and containers on node|Talks to runtime via CRI|
|**CRI Plugin**|Translates gRPC requests to container actions|Runs as socket daemon|
|**Runtime (containerd, CRI-O)**|Manages actual containers|Talks to OS & cgroups|
|**runc/crun**|Low-level container launcher|Executes OCI runtime spec|

---
## 12. Exam Notes (KCNA + CKA)

|Concept|Likely Question Type|Key Fact|
|---|---|---|
|CRI|Conceptual (KCNA)|Defines how kubelet talks to runtimes via gRPC|
|Docker Shim|Conceptual (KCNA, CKA)|Removed in v1.24|
|containerd|Practical (CKA)|Default runtime in kubeadm setups|
|crictl|Practical (CKA)|Used for debugging runtime directly|
|OCI|Conceptual (KCNA)|Ensures runtime/image compatibility|

---
## 13. Example Debugging Scenario
**Problem:** Pods stuck in `ContainerCreating` state.  
**Diagnosis:**
```bash
kubectl describe pod <podname>
# Look for message like:
# Failed to create container: connection to runtime endpoint failed
```

**Fix:**  
Check runtime socket and kubelet connection:
```bash
sudo systemctl status containerd
sudo systemctl restart kubelet
sudo crictl ps
```

If crictl works but kubelet doesn’t, the socket path may differ in kubelet config.

---

