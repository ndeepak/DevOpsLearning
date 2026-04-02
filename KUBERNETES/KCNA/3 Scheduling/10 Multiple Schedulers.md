# Multiple Schedulers

# Multiple Schedulers in Kubernetes (KCNA + CKA aligned)
## 1. What is a Scheduler (quick recap)
The **scheduler** is the control-plane component that:
- Watches for **Pending pods**    
- Selects a suitable **node**    
- Writes the decision (`nodeName`) back to the API server
The default scheduler is named:
`default-scheduler`
Every pod that does **not** specify a scheduler uses this by default.

---
## 2. Why Multiple Schedulers Exist
Kubernetes allows **more than one scheduler** to run in the same cluster.
Why this is useful:
- You may want **special scheduling rules** for certain workloads
- Examples:    
    - Batch jobs        
    - GPU-heavy workloads        
    - High-priority system tasks        
    - Custom placement logic
Important:
- The **default scheduler still exists**
- Custom schedulers run **side-by-side**, not as replacements
---
## 3. Core Idea (Exam Definition)
> A Kubernetes cluster can run **multiple schedulers**, each identified by a **unique name**, and pods can choose which scheduler should schedule them using the `schedulerName` field.

This single line answers many KCNA questions.

---
## 4. How Kubernetes Knows Which Scheduler to Use
Every Pod spec has an optional field:
`schedulerName: my-scheduler`
If:
- `schedulerName` is **not specified** → `default-scheduler` 
- `schedulerName` **is specified** → that scheduler is responsible
If the named scheduler is:
- Not running
- Misconfigured
Then:
- Pod stays in **Pending** state   

---
## 5. High-Level Architecture

![https://kubernetes.io/images/docs/kubernetes-cluster-architecture.svg?utm_source=chatgpt.com](https://kubernetes.io/images/docs/kubernetes-cluster-architecture.svg?utm_source=chatgpt.com)

![https://kubernetes.io/images/docs/components-of-kubernetes.svg?utm_source=chatgpt.com](https://kubernetes.io/images/docs/components-of-kubernetes.svg?utm_source=chatgpt.com)

What happens internally:
1. Pod is created
2. Pod is Pending
3. Each scheduler watches the API server
4. Only the scheduler whose name matches:
    `spec.schedulerName`
    attempts to schedule the pod
Schedulers **do not compete** for the same pod.

---
## 6. Default Scheduler Configuration (Concept)
The default scheduler **does not need** a config file, but it _can_ have one.
Minimal configuration example:
```yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
- schedulerName: default-scheduler
```
Purpose:
- Documentation
- Customizing plugins, scoring, filtering (advanced, CKA level)
KCNA takeaway:
- Default scheduler name is **default-scheduler**
---
## 7. Creating a Custom Scheduler (Concept-Level)
A custom scheduler is usually:
- The same `kube-scheduler` binary    
- Started with a **different config file**    
- Uses a **unique schedulerName**

Example config:
```yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
- schedulerName: my-scheduler
```
Key rule:
- **Scheduler names must be unique**
---
## 8. Ways to Deploy an Additional Scheduler
You should know the **methods**, not memorize all YAML.
### 1. As a system service
- Separate `kube-scheduler` process    
- Different config file    
- Mostly older or manual setups    
### 2. As a Pod (common)
- Scheduler runs as a pod in `kube-system`    
- Similar to control plane components    
### 3. As a Deployment (most flexible)
- Managed like any workload    
- Can use ConfigMaps    
- Supports scaling and upgrades    

KCNA focus:
- Schedulers usually run in **kube-system**    
- Often deployed as **pods**    

---
## 9. Leader Election (High Availability)
When:
- Multiple replicas of the **same scheduler** run    
Problem:
- Multiple schedulers might try to schedule the same pod
Solution:
- **Leader election**    
Key points:
- Only the **leader** schedules pods    
- Uses Kubernetes Lease objects    
- Configured in scheduler config    

Example concept:
```yaml
leaderElection:   
	leaderElect: true
```
KCNA takeaway:
- Leader election prevents scheduling conflicts    
- Required for HA scheduler setups    

---
## 10. RBAC Requirements (Concept Only)
Schedulers need permission to:
- Watch pods    
- Bind pods to nodes    
- Read nodes and leases    

Therefore:
- Scheduler runs with a **ServiceAccount**    
- Bound to roles like:    
    - `system:kube-scheduler`        
    - `system:volume-scheduler`        

KCNA level:
- Know **RBAC is required**    
- Do not memorize full RBAC YAML    

---
## 11. Using a Custom Scheduler in a Pod
This is **very important for exams**.
Pod example:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  schedulerName: my-scheduler
  containers:
  - name: nginx
    image: nginx
```
Outcome:
- `my-scheduler` schedules this pod    
- Default scheduler ignores it
---

## 12. How to Verify Scheduling
Commands you should know:
`kubectl describe pod nginx`
`kubectl get events -o wide`

In Events, look for:
`Source: my-scheduler`

This confirms:
- Which scheduler placed the pod
---
## 13. Troubleshooting Basics
If pod is Pending:
1. Check `schedulerName`
2. Verify scheduler pod is running
3. Check scheduler logs
4. Check RBAC permissions

Command:
`kubectl logs my-scheduler -n kube-system`

---
## 14. Multiple Schedulers vs Other Concepts

| Feature           | Multiple Schedulers     | DaemonSet        | Static Pods   |
| ----------------- | ----------------------- | ---------------- | ------------- |
| Purpose           | Custom scheduling logic | One pod per node | Bootstrapping |
| Uses API server   | Yes                     | Yes              | No            |
| Uses scheduler    | Yes (custom)            | Yes              | No            |
| Per-pod selection | Yes (`schedulerName`)   | No               | No            |

---
## 15. KCNA Exam Summary (Must Remember)
- Kubernetes supports **multiple schedulers**    
- Default scheduler name: `default-scheduler`    
- Custom schedulers need **unique names**    
- Pod selects scheduler using `schedulerName`    
- If scheduler not found → pod remains Pending    
- Leader election ensures HA scheduling    

---
## 16. One-line Memory Hook
A pod is scheduled by:
> **The scheduler whose name matches `spec.schedulerName`.**