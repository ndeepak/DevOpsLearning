# Taints and Tolerations vs Node Affinity

## Scheduling → Taints and Tolerations vs Node Affinity
Kubernetes offers multiple mechanisms to control **pod placement**. Two of the most important are:
- **Taints and Tolerations** – prevent unwanted pods from landing on nodes.    
- **Node Affinity / Node Selectors** – guide pods to preferred nodes.    
Combining these ensures **exclusive node usage** and precise placement.

---
## Scenario
Imagine a Kubernetes cluster:

|Node|Label|Taint|
|---|---|---|
|Node-Blue|color=blue|color=blue:NoSchedule|
|Node-Red|color=red|color=red:NoSchedule|
|Node-Green|color=green|color=green:NoSchedule|

Pods:
- Pod-Blue    
- Pod-Red    
- Pod-Green    

Goal:
- Pod-Blue → Node-Blue    
- Pod-Red → Node-Red    
- Pod-Green → Node-Green    

Requirements:
1. No pod from other teams is scheduled on your dedicated nodes.    
2. Your pods do not land on nodes assigned to other teams.    

---
## Step 1: Using Taints and Tolerations
**Purpose:** Block any pod without a matching toleration from landing on a node.
### Apply Taints to Nodes
```zsh
kubectl taint nodes Node-Blue color=blue:NoSchedule
kubectl taint nodes Node-Red color=red:NoSchedule
kubectl taint nodes Node-Green color=green:NoSchedule
```
- This repels pods that **do not have matching tolerations**.
### Set Tolerations on Pods
Example for Pod-Blue:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-blue
spec:
  containers:
  - name: app
    image: nginx
  tolerations:
  - key: "color"
    operator: "Equal"
    value: "blue"
    effect: "NoSchedule"
```
- Pod will **only schedule** on Node-Blue    
- Other pods without this toleration cannot land on Node-Blue    

**Key Consideration:**  
Taints + tolerations **allow scheduling** but do not guarantee preferential placement. If other nodes are available and meet generic scheduling criteria, pods **might schedule elsewhere**.

---
## Step 2: Using Node Affinity
**Purpose:** Guide pods to specific nodes using labels.
### Label the Nodes
```zsh
kubectl label nodes Node-Blue color=blue
kubectl label nodes Node-Red color=red
kubectl label nodes Node-Green color=green
```
### Add Node Affinity to Pods
Example for Pod-Red:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-red
spec:
  containers:
  - name: app
    image: nginx
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: color
            operator: In
            values:
            - red
```
- Scheduler will **only place the pod on a node labeled `color=red`**
- Ensures pods land on the intended node
**Limitation:** Node affinity **does not prevent other pods** from being scheduled on the same node. Other teams’ pods could still land there.

---
## Step 3: Combining Taints, Tolerations, and Node Affinity
To fully dedicate nodes:
1. **Use Taints + Tolerations**    
    - Prevents external pods from landing on your nodes.        
2. **Use Node Affinity / Node Selector**    
    - Ensures your pods are placed on the correct nodes.
Example for Pod-Green:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-green
spec:
  containers:
  - name: app
    image: nginx
  tolerations:
  - key: "color"
    operator: "Equal"
    value: "green"
    effect: "NoSchedule"
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: color
            operator: In
            values:
            - green
```
- Pod-Green **only schedules on Node-Green**
- No other pods without the toleration can land on Node-Green
---
## Summary

|Feature|Behavior|Use Case|
|---|---|---|
|**Taints & Tolerations**|Repel pods that don’t tolerate the taint|Reserve nodes for specific pods and prevent external interference|
|**Node Affinity / Selector**|Guide pods to nodes with matching labels|Ensure pods are placed on intended nodes|
|**Combined Use**|Exclusive scheduling and placement|Dedicate nodes to workloads in multi-team clusters|

**Best Practice:**  
Use **both** when you need exclusive nodes for critical workloads in shared clusters.

---
This approach is particularly useful for:
- Dedicated GPU or high-memory nodes for AI workloads
- Reserved nodes for production-critical pods    
- Multi-tenant clusters where teams must not interfere
---
