# Docker vs ContainerD
## 1. Background: How Docker Started the Container Era
Before Containerd or CRI existed, Docker provided everything you needed:
- CLI (`docker run`, `docker build`, `docker ps`)    
- Image build and push system    
- Networking, volumes, logging    
- A daemon (`dockerd`) managing containers    
- The **runtime** layer (`runc`) that actually creates Linux containers using namespaces and cgroups    

Kubernetes initially orchestrated **Docker containers directly**, making Docker appear synonymous with “containers”.
However, Docker is **not just a runtime** — it’s a full platform.  
Kubernetes only needs the _runtime part_, not the builder, volume plugins, or registry features.

---

## 2. The Docker → Containerd Split
Docker internally used **Containerd** to manage containers.
Here’s how a container ran inside Docker:
```scss
docker CLI
  ↓
dockerd (Docker daemon)
  ↓
containerd (manages container lifecycle)
  ↓
runc (spawns the container process)
```

So, **Containerd** was already the part of Docker responsible for actually starting containers — it just wasn’t exposed directly to users.

In 2017, Docker donated Containerd to the **Cloud Native Computing Foundation (CNCF)** as a separate, open runtime project.  
Containerd then became the **primary runtime** for Kubernetes clusters.

---

## 3. The Role of CRI (Container Runtime Interface)
Kubernetes uses **kubelet → CRI → container runtime** to abstract away runtime differences.
- CRI defines a **gRPC interface** for image pulling, container start/stop, and pod sandboxing.    
- Docker did **not** support CRI, so Kubernetes used **Dockershim** as a translation layer.    
- Containerd **does** support CRI directly (via the built-in `cri` plugin).    

When **Dockershim was removed in Kubernetes v1.24**, Docker was effectively replaced by CRI-compatible runtimes like Containerd and CRI-O.

---
## 4. Docker vs Containerd Architecture Comparison

|Feature|**Docker**|**Containerd**|
|---|---|---|
|Architecture|Multi-component (dockerd, containerd, runc)|Simpler (containerd, runc)|
|CRI Support|No (required dockershim)|Yes (native CRI plugin)|
|Image Management|Full-featured (build, push, auth)|Basic pull/push|
|CLI|`docker`|`ctr` / `nerdctl`|
|Resource Usage|Heavier (extra daemon + shim layer)|Lightweight|
|Kubernetes Support|Deprecated (since v1.24)|Default runtime in most clusters|
|Maintainer|Docker Inc.|CNCF (graduated project)|
|Use Case|Developer-focused, building and running locally|Production runtime for Kubernetes|

---
## 5. Docker Shim Removal
In Kubernetes ≤1.23:
`kubelet → Dockershim → dockerd → containerd → runc`

In Kubernetes ≥1.24:
`kubelet → CRI (gRPC) → containerd → runc`

Docker was replaced by **Containerd directly**, eliminating a layer and simplifying performance and maintainability.

---
## 6. Tools Overview: ctr, nerdctl, crictl
Let’s examine these three tools and how they map to your workflow.
### A. `ctr` — Containerd’s native CLI
- Comes by default with Containerd.    
- Designed mainly for **debugging**, not day-to-day usage.    
- Requires `sudo`.    
- Verbose and low-level.    

**Examples:**
```bash
# List namespaces (Containerd isolates workloads via namespaces)
sudo ctr namespaces list

# Pull an image
sudo ctr images pull docker.io/library/redis:alpine

# List images
sudo ctr images list

# Run a container
sudo ctr run --rm -t docker.io/library/redis:alpine redis
```

Output looks raw and lacks Docker’s developer-friendly UX.

---

### B. `nerdctl` — Docker-like CLI for Containerd
- Developed by the Containerd team.    
- Replicates Docker’s CLI style (almost identical syntax).    
- Uses Containerd under the hood (no dockerd).    
- Supports advanced features:    
    - Rootless containers        
    - Encrypted images        
    - Lazy pulling        
    - P2P distribution        

**Examples:**
```bash
# Pull and run a container (Docker-style)
nerdctl run -d -p 8080:80 nginx

# View containers
nerdctl ps

# Build image (just like Docker)
nerdctl build -t myapp:1.0 .

# Stop and remove
nerdctl stop <id>
nerdctl rm <id>
```
If you know Docker, you already know nerdctl.

---

### C. `crictl` — Kubernetes CRI Tool
- Maintained by Kubernetes community.    
- Talks directly to any **CRI-compatible runtime** (Containerd, CRI-O).    
- Used for **debugging Pods/containers** from kubelet’s perspective.    
- Does not create containers directly like Docker or nerdctl.    

**Examples:**
```bash
# Set runtime endpoint (if not auto-detected)
sudo crictl --runtime-endpoint unix:///run/containerd/containerd.sock ps

# List all pods
sudo crictl pods

# List all containers
sudo crictl ps -a

# View images
sudo crictl images

# Get container logs
sudo crictl logs <container_id>
```
**In exams**, `crictl` is invaluable for debugging container runtime issues.

---

## 7. Example Scenario: Kubernetes Node Runtime Verification
You’re asked to confirm which runtime your node is using.
**Step 1: Check kubelet config**
`cat /var/lib/kubelet/config.yaml | grep runtime`
Output:
`containerRuntimeEndpoint: unix:///run/containerd/containerd.sock`

**Step 2: Test CRI connection**
`sudo crictl info`
Shows details about Containerd and runtime versions.

**Step 3: List running containers**
`sudo crictl ps`

If output lists your Pods’ containers, kubelet–runtime integration is healthy.

---
## 8. Common Endpoints (sockets)

|Runtime|Socket Path|
|---|---|
|containerd|`/run/containerd/containerd.sock`|
|CRI-O|`/var/run/crio/crio.sock`|
|Docker (via Mirantis cri-dockerd)|`/var/run/cri-dockerd.sock`|

You can verify the active runtime socket with:
`sudo ls /run/containerd/containerd.sock`

Or switch it:
`export CONTAINER_RUNTIME_ENDPOINT=unix:///run/containerd/containerd.sock`

---
## 9. Practical Command Comparison

|Operation|Docker|nerdctl|ctr|crictl|
|---|---|---|---|---|
|List containers|`docker ps`|`nerdctl ps`|`ctr containers list`|`crictl ps`|
|Run container|`docker run nginx`|`nerdctl run nginx`|`ctr run nginx`|N/A|
|View logs|`docker logs id`|`nerdctl logs id`|N/A|`crictl logs id`|
|Inspect|`docker inspect id`|`nerdctl inspect id`|N/A|`crictl inspect id`|
|Remove container|`docker rm id`|`nerdctl rm id`|`ctr tasks delete id`|N/A|
|Pull image|`docker pull image`|`nerdctl pull image`|`ctr images pull image`|`crictl pull image`|
|Focus|Developer use|Developer/sysadmin|Low-level debug|K8s runtime debug|

---
## 10. Real Cluster Example: Debugging Pods Using `crictl`
Let’s say a Pod is stuck in `ContainerCreating`.
`kubectl describe pod myapp`
Shows:
`Failed to create container: error connecting to container runtime`

Now check runtime layer:
```bash
sudo crictl ps
sudo crictl pods
sudo systemctl status containerd
sudo crictl logs <container_id>
```

If containerd isn’t responding, restart it:
`sudo systemctl restart containerd && sudo systemctl restart kubelet`

---
## 11. Containerd Namespaces (Important Concept)
Containerd uses **namespaces** to isolate contexts:
- Docker uses `moby`    
- Kubernetes uses `k8s.io`    

List namespaces:
`sudo ctr namespaces list`
Switch namespace:
`sudo ctr -n k8s.io containers list`

You’ll see Kubernetes-managed containers here (Pods).

---

## 12. Summary Table

|Aspect|Docker|Containerd|
|---|---|---|
|Introduced|2013|2017|
|Maintainer|Docker Inc.|CNCF|
|API Type|REST API|gRPC (CRI)|
|Runtime|containerd + runc (internally)|containerd + runc|
|Use in Kubernetes|Deprecated|Default|
|CLI|docker|ctr, nerdctl, crictl|
|OCI Compliance|Partial (pre-CRI)|Full|
|Best For|Developers, CI/CD builds|Production Kubernetes runtime|

---

## 13. KCNA / CKA Exam Notes

|Topic|Focus|Key Point|
|---|---|---|
|Docker Shim|Theory|Removed in v1.24|
|containerd|Theory + Practical|Default runtime for kubeadm|
|CRI|Theory|Allows kubelet–runtime communication|
|nerdctl|Practical|Docker-like CLI for containerd|
|crictl|Practical|CRI debugging tool|
|ctr|Practical|Low-level debug CLI for containerd|

---

