# Resource Limits

## Scheduling → Resource Requests, Limits, LimitRanges, and ResourceQuotas
Kubernetes allows you to manage **CPU and memory resources** for pods to ensure predictable performance and cluster stability.
Resource management is one of the most important concepts in Kubernetes. Understanding **resource requests**, **limits**, **LimitRanges**, and **ResourceQuotas** is essential both for the KCNA exam and for real-world cluster efficiency.

---
## 1. Resource Requests and Limits
**Definitions:**
- **Request** – Minimum resources a pod is guaranteed to receive.
- **Limit** – Maximum resources a pod can consume.
The relationship between requests and limits impacts scheduling and runtime behavior.

---
### CPU Scenarios

| Configuration           | Behavior                                                                                   |
| ----------------------- | ------------------------------------------------------------------------------------------ |
| **No request or limit** | Pod can consume all available CPU, may affect other pods.                                  |
| **Limit only**          | Request = Limit. Pod is guaranteed the CPU limit (e.g., 3 vCPUs).                          |
| **Request and Limit**   | Pod guaranteed request (e.g., 1 vCPU), can scale up to limit (e.g., 3 vCPUs) if available. |
| **Request only**        | Pod guaranteed requested CPU (e.g., 1 vCPU), can use unutilized CPU cycles on node.        |
**Key:** Always specify requests to prevent overconsumption and maintain fair scheduling.

---
### Memory Scenarios

| Configuration           | Behavior                                                                                    |
| ----------------------- | ------------------------------------------------------------------------------------------- |
| **No request or limit** | Pod can consume all memory, may cause instability or OOM kills.                             |
| **Limit only**          | Request = Limit (e.g., 3 GB), pod guaranteed memory equal to limit.                         |
| **Request and Limit**   | Guaranteed request (e.g., 1 GB), can grow up to limit (e.g., 3 GB).                         |
| **Request only**        | Pod guaranteed request; exceeding memory may cause pod termination if system memory is low. |
**Warning:** Memory is stricter than CPU—overconsumption can terminate pods.

---
## 2. LimitRanges
Pods without explicit resource definitions may consume unbounded resources.  
**LimitRange** objects at the **namespace level** enforce default requests and limits for all pods created in that namespace.
### Example: CPU LimitRange
- Any container created without explicit CPU request/limit will get **500m CPU** by default.    
- Maximum allowed CPU per container = 1 CPU    
- Minimum allowed CPU per container = 100m    

### Example: Memory LimitRange
- Containers get default memory = 1 Gi if unspecified.
- Enforces min/max memory boundaries.
**Note:** Changes to LimitRange apply **only to new pods** created after the update.

---
## 3. ResourceQuotas
**Purpose:** Limit the **total resources consumed in a namespace**, useful in multi-tenant clusters or shared labs.
### Example:
- Limit total requested CPU: 4 vCPUs
- Limit total requested memory: 4 GB
- Maximum allowed across all pods: 10 vCPUs, 10 GB memory
This ensures no single team or workload can **starve the cluster** or other pods.

---
## 4. Use-Case Scenarios
### Scenario 1: Production Workload
- Pod requires 2 vCPUs and 4 GB RAM.
- LimitRange ensures default requests if missing.
- ResourceQuota ensures team cannot exceed cluster allocation.
### Scenario 2: Lab Environment
- Multiple students deploying pods without specifying resources.
- LimitRange prevents pods from over-consuming CPU/memory.
- ResourceQuota caps total resources per namespace to maintain fairness.
### Scenario 3: Burstable Pod
- Pod with request 1 vCPU, limit 3 vCPUs
- Guarantees 1 vCPU, but can use extra CPU if node has spare cycles.
---
## 5. Best Practices
1. **Always define resource requests** for predictable scheduling.
2. Use **limits** for CPU to prevent a pod from starving others.
3. Use **limits** for memory to avoid OOM kills.
4. Implement **LimitRanges** at namespace level to enforce defaults.
5. Apply **ResourceQuotas** for multi-tenant clusters.
6. Monitor pod and node metrics to adjust requests and limits as workloads change.
---
**References for further reading:**
- [Kubernetes Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [LimitRange Documentation](https://kubernetes.io/docs/concepts/policy/limit-range/)
- [ResourceQuota Documentation](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
---
