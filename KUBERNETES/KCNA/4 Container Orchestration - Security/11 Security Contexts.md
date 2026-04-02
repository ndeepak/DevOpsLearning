# Security Contexts

# Kubernetes Security Contexts (KCNA)
## What Is a Security Context?
A **security context** defines **privilege and access control settings** for a pod or a container.
It answers questions like:
- Which user runs the process inside the container?    
- What Linux capabilities are allowed or denied?    
- Can the container escalate privileges?    
- Is the root filesystem writable?    
Security contexts are a **core part of container orchestration security**.

---
## Why Security Contexts Matter
By default:
- Containers may run as **root**    
- Containers may have **more Linux privileges than needed**    

Security contexts help:
- Enforce **least privilege**    
- Reduce **container breakout risk**    
- Align with **security compliance requirements**    
- Limit impact if a container is compromised    

---
## Security Contexts in Docker (Background)
Before Kubernetes, Docker allowed security configuration at runtime.
Examples:
`docker run --user=1001 ubuntu sleep 3600`
Runs the container process as user ID `1001`.

`docker run --cap-add MAC_ADMIN ubuntu`
Adds a Linux capability (`MAC_ADMIN`) to the container.

Kubernetes extends these same ideas, but applies them using **YAML configuration**.

---
## Security Contexts in Kubernetes
In Kubernetes, security contexts can be applied at **two levels**:
### 1. Pod-Level Security Context
- Applies to **all containers** in the pod    
- Acts as a **default**    
### 2. Container-Level Security Context
- Applies to **one specific container**    
- **Overrides pod-level settings** if both are defined    

---
## Precedence Rule (Very Important)
> **Container-level security context always overrides pod-level security context**

This is commonly tested in KCNA and CKA exams.

---
## Common Security Context Settings
### User and Group IDs
- `runAsUser`    
- `runAsGroup`    
- `fsGroup`    
### Privilege Controls
- `privileged`    
- `allowPrivilegeEscalation`    
- `readOnlyRootFilesystem`    
### Linux Capabilities
- `add`    
- `drop`    
---
## Example: Container-Level Security Context
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
spec:
  containers:
  - name: ubuntu
    image: ubuntu
    command: ["sleep", "3600"]
    securityContext:
      runAsUser: 1000
      capabilities:
        add: ["MAC_ADMIN"]
```
### What This Configuration Does
- The container runs as **user ID 1000**    
- The container is granted the **MAC_ADMIN Linux capability**    
- Only this container is affected    

---
## Pod-Level vs Container-Level (Comparison)

|Feature|Pod-Level|Container-Level|
|---|---|---|
|Scope|All containers|Single container|
|Override behavior|Can be overridden|Takes precedence|
|Best for|Defaults|Fine-grained control|

---
## Linux Capabilities (Quick Explanation)
Linux capabilities split root privileges into smaller units.
Examples:
- `NET_ADMIN` – Network configuration    
- `SYS_TIME` – Modify system time    
- `MAC_ADMIN` – Mandatory access control    

Best practice:
- **Drop all capabilities**    
- Add only what is required    

Example:
```yaml
capabilities:
  drop: ["ALL"]
  add: ["NET_BIND_SERVICE"]
```

---
## KCNA Exam Tips
- Security contexts control **runtime security**, not API access
- They are **different from RBAC**    
- They apply at **pod and container level**    
- Container-level overrides pod-level    
- Kubernetes uses **Linux kernel features** for enforcement    
- Security contexts do not manage image security or secrets
---
## Common Misconceptions

|Misconception|Reality|
|---|---|
|Security context controls permissions to Kubernetes API|RBAC does that|
|Security context is only for pods|Can be pod or container|
|Running as root is required|Often unnecessary|
|Capabilities are Kubernetes-specific|They are Linux features|

---
## One-Line Summary

A **security context** defines how a container runs at the OS level—user IDs, privileges, and capabilities—helping enforce least privilege and improve cluster security.