# Daemon Sets
## What is a DaemonSet (in one line – exam perfect)
		
A **DaemonSet** ensures **exactly one pod runs on each selected node** in a Kubernetes cluster.  
When a node is added → pod is added.  
When a node is removed → pod is removed.

---
## Big Picture: Why DaemonSets exist

![https://cast.ai/wp-content/uploads/2023/11/des-618-Kubernetes-DaemonSet-png.webp?utm_source=chatgpt.com](https://cast.ai/wp-content/uploads/2023/11/des-618-Kubernetes-DaemonSet-png.webp?utm_source=chatgpt.com)

![https://devopscube.com/content/images/2025/03/daemonset-explained-1.png?utm_source=chatgpt.com](https://devopscube.com/content/images/2025/03/daemonset-explained-1.png?utm_source=chatgpt.com)

![https://zesty.co/wp-content/uploads/2025/02/DaemonSets.png?utm_source=chatgpt.com](https://zesty.co/wp-content/uploads/2025/02/DaemonSets.png?utm_source=chatgpt.com)

Some workloads are **node-scoped**, not application-scoped.  
They don’t scale by traffic, they scale by **number of nodes**.

Examples you must remember:

| Category   | Real Use                           |
| ---------- | ---------------------------------- |
| Monitoring | node-exporter, Datadog agent       |
| Logging    | Fluentd, Filebeat                  |
| Networking | kube-proxy, weave-net, calico-node |
| Storage    | CSI node plugins                   |

👉 ReplicaSet says _“run N copies”_  
👉 DaemonSet says _“run on every node”_

---
## DaemonSet vs ReplicaSet (CKA favorite)

|Feature|DaemonSet|ReplicaSet|
|---|---|---|
|Number of Pods|One per node|Fixed count|
|Scaling|By nodes|By replicas|
|Use case|Node services|App workloads|
|Scheduler|Yes (post v1.12)|Yes|
|Typical pods|Agents, proxies|Web, API, workers|

**Exam trap:**  
If they say _“one pod per node”_ → ✅ DaemonSet  
If they say _“three copies”_ → ✅ ReplicaSet / Deployment

---
## How DaemonSets REALLY work (Scheduler internals)

![https://devopscube.com/content/images/2025/03/image-4-44.png?utm_source=chatgpt.com](https://devopscube.com/content/images/2025/03/image-4-44.png?utm_source=chatgpt.com)

![https://media.geeksforgeeks.org/wp-content/uploads/20240506110659/Node-Affinity-In-Kubernetes.webp?utm_source=chatgpt.com](https://media.geeksforgeeks.org/wp-content/uploads/20240506110659/Node-Affinity-In-Kubernetes.webp?utm_source=chatgpt.com)

### Old behavior (pre-1.12)
- Used `nodeName`
- Bypassed scheduler ❌

### Current behavior (important for CKA!)
- Uses **default scheduler**
- Automatically adds **node affinity**    
- Scheduler decides placement ✅
This matters because:
- DaemonSet pods **respect taints & tolerations**
- They **can be restricted with nodeSelector / affinity**

---
## Basic DaemonSet YAML (must memorize structure)
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: monitoring-daemon
spec:
  selector:
    matchLabels:
      app: monitoring-agent   # MUST match template labels
  template:
    metadata:
      labels:
        app: monitoring-agent
    spec:
      containers:
      - name: monitoring-agent
        image: monitoring-agent:latest
```
**Critical exam rule**  
`spec.selector.matchLabels` **MUST match** `spec.template.metadata.labels`  
If not → resource will be rejected or misbehave.

---

## DaemonSet Scheduling Rules (very exam-relevant)
### 1. Runs on **all nodes by default**
Including:
- Worker nodes ✅
- Control-plane nodes ❌ (usually tainted)

---
### 2. Control-plane nodes need tolerations
Control-plane nodes have taint:
`node-role.kubernetes.io/control-plane:NoSchedule`

✅ To run on control plane, add toleration:
```yaml
spec:
  template:
    spec:
      tolerations:
      - key: "node-role.kubernetes.io/control-plane"
        operator: "Exists"
        effect: "NoSchedule"
```
⚠️ **CKA loves this**

---
### 3. Running DaemonSet on selected nodes only
#### Using `nodeSelector`
```yaml
spec:
  template:
    spec:
      nodeSelector:
        disktype: ssd
```

#### Using `nodeAffinity` (preferred)
```yaml
spec:
  template:
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: disktype
                operator: In
                values:
                - ssd
```
✅ This is **100% exam material**

---
## Updating a DaemonSet (RollingUpdate)
By default:
```yaml
spec:
  updateStrategy:
    type: RollingUpdate
```

Optional tuning:
```yaml
updateStrategy:
  rollingUpdate:
    maxUnavailable: 1
```
✅ Same logic as Deployment, but per node.

---
## DaemonSet Lifecycle Behavior

| Event             | Result                          |
| ----------------- | ------------------------------- |
| New node added    | Pod automatically created       |
| Node removed      | Pod automatically deleted       |
| Node drained      | Pod evicted (unless toleration) |
| DaemonSet deleted | All pods deleted                |

---
## Kubectl Commands You MUST know
```yaml
kubectl get daemonsets
kubectl describe daemonset <name>

kubectl get pods -o wide
kubectl get pods --all-namespaces

kubectl rollout status daemonset <name>
kubectl edit daemonset <name>
```

✅ On exam → `kubectl edit` is often faster than re-writing YAML.

---
## Common CKA / KCNA Exam Traps 🚨
### Trap 1: Expecting replicas
❌ DaemonSets don’t use `replicas`

---
### Trap 2: Pod not running on control-plane
👉 Missing **toleration**

---
### Trap 3: Pod runs on unwanted nodes
👉 Missing **nodeSelector / affinity**

---
### Trap 4: Selector mismatch
👉 Labels must match EXACTLY

---
## When SHOULD NOT use DaemonSet
❌ User-facing apps  
❌ APIs  
❌ Autoscaling workloads  
❌ Batch jobs

Use:
- Deployment    
- StatefulSet    
- Job / CronJob    
---

## One-line memory hook (helps in exams)
> **If the workload belongs to the node, use a DaemonSet.  
> If the workload belongs to users, don’t.**

---
## Quick KCNA-style summary
- DaemonSet = 1 Pod per node    
- Automatic scaling with nodes    
- Common for logging, monitoring, networking    
- Uses scheduler + node affinity    
- Works with taints & tolerations    
- No replicas field    

---