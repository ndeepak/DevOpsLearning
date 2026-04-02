# Node Affinity

## Scheduling → Node Affinity
Node affinity is an advanced Kubernetes feature that allows you to **control pod placement** on nodes using rules and expressions. It builds on the simpler **node selector**, providing more flexibility with operators, multiple conditions, and preferences.

---
## Why Node Affinity?
Imagine a cluster with three nodes:

|Node|CPU|Memory|Label|
|---|---|---|---|
|Node-1|16|64GB|size=Large|
|Node-2|8|32GB|size=Medium|
|Node-3|4|16GB|size=Small|

You have a pod that processes large datasets. You want it to run only on powerful nodes.
- **Node selectors** can schedule it only on nodes labeled `size=Large`    
- **Node affinity** allows scheduling on multiple nodes (`size=Large` or `size=Medium`) and supports more complex rules like inclusion, exclusion, or existence checks.    

---
## Node Selector Recap (Simple Affinity)
A pod with a node selector:
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
- Only schedules on nodes with `size=Large`    
- Simple equality match, no flexibility    

---
## Node Affinity Syntax
Node affinity is specified under the pod spec using an `affinity` block:
```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: size
                operator: In
                values:
                  - Large
```

**Explanation:**
- `affinity` → defines scheduling constraints
- `nodeAffinity` → affinity rules related to nodes    
- `requiredDuringSchedulingIgnoredDuringExecution` → mandatory rule for scheduling; ignored during execution
- `nodeSelectorTerms` → list of terms (ORed together)    
- `matchExpressions` → key/operator/values conditions (ANDed together)
---
## Node Affinity Operators
1. **In** – schedule pod if node label is in the specified values
```yaml
operator: In
values: [Large, Medium]
```
2. **NotIn** – schedule pod if node label is **not** in specified values
```yaml
operator: NotIn
values: [Small]
```
3. **Exists** – schedule pod on nodes where the label exists
`operator: Exists`
4. **DoesNotExist** – schedule pod on nodes where label is missing
`operator: DoesNotExist`
5. **Gt / Lt** – numeric comparisons (e.g., memory or CPU labels)
---
## Required vs Preferred Node Affinity

|Affinity Type|Behavior|Use Case|
|---|---|---|
|**requiredDuringSchedulingIgnoredDuringExecution**|Pod **must** be scheduled on matching node. Unschedulable if none available.|Critical workloads that cannot run on other nodes|
|**preferredDuringSchedulingIgnoredDuringExecution**|Scheduler **prefers** matching nodes but can schedule on others if unavailable.|Flexible workloads that benefit from certain nodes but are not strict|
> Future Kubernetes releases may introduce:
> - requiredDuringSchedulingRequiredDuringExecution
> - preferredDuringSchedulingRequiredDuringExecution  
>     Which enforce rules even after the pod is running.
---

## Real-world Scenarios
### Scenario 1: Resource-heavy workload
- Pod requires 16 CPU cores    
- Node labels: `size=Large`    
- Use required node affinity to ensure scheduling only on `Large` nodes
### Scenario 2: Flexible workloads
- Pod can run on `Large` or `Medium` nodes    
- Use `In` operator with both values under required or preferred affinity
### Scenario 3: Avoid small nodes
- Pod should **never** run on `Small` nodes    
- Use `NotIn: [Small]`
### Scenario 4: Generic affinity
- Pod can run anywhere nodes have a `size` label defined
- Use `Exists` operator
---

## Lifecycle Considerations
- **Scheduling phase:** affinity rules are evaluated to determine suitable nodes    
- **Execution phase:** current affinity types (`IgnoredDuringExecution`) do not evict pods if node labels change    
- Future types (`RequiredDuringExecution`) may evict pods if node no longer satisfies affinity rules
Example:
1. Pod scheduled on node labeled `size=Large`    
2. Admin removes `size=Large` label from the node    
3. With current affinity → pod continues to run    
4. With `RequiredDuringExecution` → pod may be evicted
---
## Comparison: Node Selector vs Node Affinity

|Feature|Node Selector|Node Affinity|
|---|---|---|
|Expression types|Exact match only|In, NotIn, Exists, DoesNotExist, Gt, Lt|
|Multiple values|❌|✅|
|Required / Preferred|❌|✅|
|Flexibility|Low|High|

---
## Best Practices
1. Label nodes accurately based on resource type, availability, or workload suitability.    
2. Use **preferred affinity** for workloads that are flexible but benefit from specific nodes.    
3. Use **required affinity** for critical workloads that cannot tolerate incorrect node placement.    
4. Combine node affinity with **taints and tolerations** to isolate workloads.    
5. Monitor nodes for label changes if using `requiredDuringSchedulingIgnoredDuringExecution`.
---

## Example: Full Node Affinity Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: analytics-pod
spec:
  containers:
    - name: analytics
      image: analytics-app
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: size
                operator: In
                values: [Large, Medium]
              - key: gpu
                operator: Exists
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 1
          preference:
            matchExpressions:
              - key: region
                operator: In
                values: [us-east-1]
```

**Interpretation:**
- Pod **must** run on nodes with `size=Large` or `Medium` **and** have `gpu` label
- Scheduler **prefers** nodes in `us-east-1` if available
---
## Summary
- Node affinity provides **flexible pod scheduling based on node labels**    
- Operators: In, NotIn, Exists, DoesNotExist, Gt, Lt    
- Types: Required vs Preferred    
- Works during **scheduling**, not typically during **execution**    
- Enables efficient cluster utilization, workload isolation, and targeted placement

---
