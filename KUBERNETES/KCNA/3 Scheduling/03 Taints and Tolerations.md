# Taints and Tolerations

## Scheduling → Taints and Tolerations
Taints and tolerations are Kubernetes features used to **control which pods are allowed or not allowed to run on which nodes**.  
They do not force scheduling to a specific node, but they **restrict placement**.

Taints are applied on nodes.  
Tolerations are applied on pods.

Together, they let you:
- Reserve nodes for specific workloads
- Prevent unwanted workloads from running on certain nodes
- Evict pods from a node under certain conditions
---
# Concept Overview (Analogy)
Imagine a person (node) sprays a repellent.  
A bug (pod) wants to land on them.
- The repellent = taint    
- The bug’s immunity = toleration    
- Bugs without immunity avoid the person    
- Bugs with immunity can land    

This is exactly how Kubernetes behaves:
- Taints repel pods
- Tolerations allow certain pods through 
- Only pods with matching tolerations may be scheduled on a tainted node

---
# Kubernetes Translation
- **Nodes** hold _taints_
- **Pods** carry _tolerations_
- Taints prevent scheduling of unmatched pods
- Tolerations allow scheduling but do not guarantee it

Important:  
Taints and tolerations restrict pod placement.  
For forcing placement, you use **node selectors or affinity**, not taints alone.

---
# Example Scenario
Cluster with 3 nodes: node1, node2, node3  
Pods: A, B, C, D

Scheduler normally spreads pods across all nodes.

You add a taint to node1:
`app=blue:NoSchedule`

Now:
- Pods A, B, C have no toleration → cannot run on node1
- Pod D has the matching toleration → allowed on node1
This is how you reserve a node for specific workloads.

---
# Applying a Taint
General syntax:
`kubectl taint nodes node-name key=value:effect`

Example:
`kubectl taint nodes node1 app=blue:NoSchedule`

This means:
- Node does not allow pods without a matching toleration.
- Scheduler will avoid scheduling unmatched pods on that node.
Note: The Taints defines **what happens to PODs that DO NOT TOLERATE this taint?**

---
# Taint Effects

| Effect               | Behavior                                                                                   |
| -------------------- | ------------------------------------------------------------------------------------------ |
| **NoSchedule**       | New pods without toleration will not be scheduled on the node.                             |
| **PreferNoSchedule** | Scheduler will try to avoid the node but may place pods there if needed.                   |
| **NoExecute**        | New pods without toleration are blocked, and existing pods without toleration are evicted. |

---
# Adding a Toleration to a Pod
To allow a pod to run on a tainted node, add a toleration.
Example:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: nginx-container
    image: nginx
  tolerations:
  - key: "app"
    operator: "Equal"
    value: "blue"
    effect: "NoSchedule"
```

This pod can now run on any node tainted with:
`app=blue:NoSchedule`

---
# Special Case: **NoExecute**
This effect impacts both new and existing pods.
Example scenario:
1. node1 is tainted with `app=blue:NoExecute`
2. Pod D tolerates the taint
3. Pod C does not tolerate it and is already running on node1
Result:
- C is evicted
- D stays running
- No new pods without toleration can land on node1
NoExecute is commonly used in:
- Node failures    
- Node maintenance    
- Cordoning/draining operations
---
# Important Considerations
### 1. Taints do **not** force pods to run on a node
They only restrict which nodes are allowed.
If a pod tolerates the taint, Kubernetes _may_ put it there—but is not required to.
For forcing placement, use:
- Node selectors
- Node affinity    

### 2. Master/Control-plane nodes
Control-plane nodes are typically tainted to prevent regular workloads:
Example default taint:
`node-role.kubernetes.io/control-plane:NoSchedule`

To check:
`kubectl describe node <node-name>`
`kubectl describe node kubemaster | grep Taint`
### 3. Removing a taint
Add a trailing minus `-`:
`kubectl taint nodes node1 app=blue:NoSchedule-`

---
# Summary
- **Taints** = placed on nodes; repel pods    
- **Tolerations** = placed on pods; allow them to land on tainted nodes    
- Effects control behavior:    
    - NoSchedule        
    - PreferNoSchedule        
    - NoExecute        
- Taints restrict placement; tolerations permit placement    
- They do not force scheduling.    
- Commonly used for dedicating nodes, isolating workloads, and stabilizing control-plane nodes    
Mastering taints and tolerations is essential for understanding **advanced scheduling and cluster reliability strategies**.

----