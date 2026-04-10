# Node Selectors

## Scheduling → Node Selectors
Node selectors allow you to **restrict pod scheduling to specific nodes** based on labels. They are a simple way to control where pods run in your cluster.

---
## Why Node Selectors?
Imagine a cluster with three nodes:
- Node-1 → Large resources    
- Node-2 → Medium resources    
- Node-3 → Small resources
By default, Kubernetes schedules pods on **any available node**.  
If you deploy a resource-intensive pod, it might land on a small node, causing performance issues.

**Solution:** Use **node selectors** to ensure pods only run on nodes that meet specific criteria.

---
## Using Node Selectors in Pod Definitions
To schedule a pod on nodes labeled `size=Large`, add a `nodeSelector` field to the pod spec.

Example:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: data-processor
    image: data-processor
  nodeSelector:
    size: Large
```
- The pod will only be scheduled on nodes where the label `size=Large` exists.
- If no node has this label, the pod remains in **Pending** state.    

---
## Labels and Node Selectors
Node selectors work by **matching a pod's nodeSelector to the node's labels**.  
It is essential to label your nodes correctly before using node selectors.

---

### Labeling a Node
Use the `kubectl label` command:
`kubectl label nodes <node-name> <label-key>=<label-value>`

Example:
`kubectl label nodes node-1 size=Large`

Now, any pod with `nodeSelector: size=Large` will only be scheduled on `node-1`.

---
## Deploying a Pod with Node Selector
1. Label the node(s) correctly.
2. Create a pod manifest with a nodeSelector.
3. Deploy the pod:
`kubectl create -f pod-definition.yml`
Kubernetes schedules the pod on a node where the labels **match exactly**.

---
## Limitations of Node Selectors
- Node selectors only support **exact match** with a single label.
- You cannot specify multiple options, ranges, or conditions.
    - Example: "schedule on Large or Medium nodes" → not supported with simple node selectors.
- For more advanced requirements, use **node affinity** or **anti-affinity**.
Node selectors are ideal for **simple, straightforward scheduling rules**.

---
## Summary

| Feature       | Description                                            |
| ------------- | ------------------------------------------------------ |
| Node Selector | Restricts pod scheduling to nodes with matching labels |
| Labels        | Key-value pairs assigned to nodes                      |
| Limitation    | Cannot express complex rules; only exact matches       |

**Key Commands:**
- Label node:
`kubectl label nodes node-1 size=Large`
- Deploy pod with node selector:
`kubectl create -f pod-definition.yml`
Node selectors are **easy and effective** for basic node-based pod scheduling.