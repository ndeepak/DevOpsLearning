# Pods
[01 Pods](KUBERNETES/KCNA/2%20Kubernetes%20Resources/01%20Pods.md)

# Pods (CKA Level)
## What Is a Pod?
A **Pod** is the **smallest deployable and schedulable unit** in Kubernetes.
It represents:
- A **group of one or more containers**
- Running on the **same node**
- Sharing:
    - Network namespace (IP, ports)
    - Storage (volumes)

A Pod is **ephemeral by design** — it is **not meant to be persistent**.

---

## Why Pods Exist (Architectural Reasoning)

Kubernetes does **not manage containers directly**.

Instead, it introduces Pods to:

- Provide a **stable abstraction layer**
- Enable **co-located containers** (sidecar pattern)
- Handle **networking and storage consistently**
- Allow **controllers** to manage workloads declaratively

Without Pods:

- No shared localhost communication
- No unified lifecycle
- No grouping of tightly coupled processes

---

## Pod Internals (Important for CKA)

### 1. Pod Sandbox (Pause Container)

Every Pod has an **infrastructure container** (pause container):

- Holds the **network namespace**
- Provides the Pod’s **IP address**
- Keeps the Pod alive even if containers restart

Other containers join this namespace.

---

### 2. Shared Networking

All containers in a Pod:

- Share the **same IP**
- Communicate via:  
    `localhost:<port>`

Example:

- App container → `localhost:8080`
- Sidecar → `localhost:8080`

No service discovery needed inside the Pod.

---

### 3. Shared Storage

Defined via **Volumes** in Pod spec.

Example:

- `/var/log/app` shared between:
    - Main container (writes logs)
    - Sidecar (ships logs)

---

### 4. Lifecycle Management

Pod lifecycle is managed by:

- **Kubelet** (node-level agent)
- **Container Runtime** (containerd / CRI-O)

Phases:

- Pending
- Running
- Succeeded
- Failed
- Unknown

---

## Pod YAML (CKA Critical)

Minimal Pod:

```yaml
apiVersion: v1  
kind: Pod  
metadata:  
  name: nginx  
  labels:  
    app: web  
spec:  
  containers:  
  - name: nginx  
    image: nginx:1.25  
    ports:  
    - containerPort: 80
```

---

## Multi-Container Pods (Design Patterns)

### 1. Sidecar Pattern

Adds supporting functionality.

Example:

- App container
- Log forwarder (Fluentd)

---

### 2. Ambassador Pattern

Acts as proxy to external services.

Example:

- App → localhost
- Ambassador → external DB

---

### 3. Adapter Pattern

Transforms output format.

Example:

- App logs → adapter → monitoring system format

---

## Pod Lifecycle (Deep Dive)

### Creation Flow

1. User applies YAML (`kubectl apply`)
2. API Server stores desired state (etcd)
3. Scheduler assigns node
4. Kubelet:
    - Pulls image
    - Creates containers
    - Starts Pod

---

### Restart Behavior

Controlled by:

`restartPolicy: Always | OnFailure | Never`

- `Always` (default): for Deployments
- `OnFailure`: batch jobs
- `Never`: debugging

---

### Container States

Inside Pod:

- Waiting
- Running
- Terminated

---

## Probes (VERY IMPORTANT FOR CKA)

### Liveness Probe

- Detects if app is **dead**
- Restarts container

### Readiness Probe

- Determines if Pod is **ready to receive traffic**
- Controls Service endpoints

### Startup Probe

- For slow-starting apps

Example:

livenessProbe:  
```
  httpGet:  
    path: /  
    port: 80  
```
  initialDelaySeconds: 10  
  periodSeconds: 5

---

## Init Containers

Run **before main containers**.

Use cases:

- Wait for DB
- Download config
- Perform setup

Example:

initContainers:  
- name: init-db  
  image: busybox  
  command: ['sh', '-c', 'sleep 10']

---

## Pod Networking (CKA Core Concept)

- Each Pod gets a **unique IP**
- No NAT between Pods
- Flat network model

Requirements:

- Pod → Pod communication across nodes
- Implemented via **CNI plugins**:
    - Calico
    - Flannel
    - Cilium

---

## Static Pods (High Priority Topic)

Managed directly by **Kubelet**, not API Server.

Location:

`/etc/kubernetes/manifests`

Use cases:

- Control plane components:
    - API Server
    - Scheduler
    - Controller Manager

Check:

kubectl get pods -n kube-system

Mirror Pods appear in API Server.

---

## Pod Resource Management

Define CPU & memory:

```yaml
resources:  
  requests:  
    memory: "64Mi"  
    cpu: "250m"  
  limits:  
    memory: "128Mi"  
    cpu: "500m"
```

- **Requests** → scheduling decision
- **Limits** → enforced by runtime

---

## Pod Troubleshooting (CKA MUST KNOW)

### Common Commands

Check pods:

`kubectl get pods -o wide`

Describe:

`kubectl describe pod <name>`

Logs:

```
kubectl logs <pod>  
kubectl logs <pod> -c <container>
```

Exec:

`kubectl exec -it <pod> -- /bin/sh`

---

### Debugging Failures

#### ImagePullBackOff

- Wrong image name
- Registry issue

#### CrashLoopBackOff

- App crashes repeatedly
- Check logs

#### Pending

- No resources
- Scheduling issues

---

## Imperative Commands (Exam Speed)

Create Pod:

`kubectl run nginx --image=nginx --restart=Never`

Dry-run YAML:

`kubectl run nginx --image=nginx --dry-run=client -o yaml`

---

## Pods and Controllers (IMPORTANT DISTINCTION)

You **should not create Pods directly** in production.

Use:

- Deployment → stateless apps
- StatefulSet → stateful apps
- DaemonSet → one per node
- Job/CronJob → batch workloads

Reason:  
Pods are **not self-healing by themselves**.

---

## Key CKA Concepts Summary

|Concept|Key Point|
|---|---|
|Pod|Smallest deployable unit|
|IP|One IP per Pod|
|Containers|Share network & storage|
|Lifecycle|Ephemeral|
|Scaling|Done via controllers|
|Debugging|kubectl logs/describe/exec|
|Static Pods|Managed by Kubelet|
|Probes|Health & readiness control|

---

## Final Takeaway

- A Pod is **not just a container wrapper** — it is a **networked, scheduled, and managed unit**.
- Understanding **Pod internals + lifecycle + troubleshooting** is critical for CKA.
- In the exam, speed comes from:
    - Writing YAML fast
    - Using `kubectl` efficiently
    - Debugging failures quickly