# Manual Scheduling
## Scheduling → Manual Scheduling
Manual scheduling means assigning a Pod to a specific node **without relying on the Kubernetes Scheduler**. This is useful in situations like:
- Testing cluster behavior when the scheduler is disabled
- Forcing a pod to run on a specific node for troubleshooting
- Demo scenarios where you want full control
Before learning manual methods, first understand **how scheduling normally works**.

---
## How Pod Scheduling Works
When you create a Pod, its manifest usually **does not include the `nodeName` field**. For example:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
    - name: nginx
      image: nginx
  nodeName:
```

Since `nodeName` is empty:
1. Kubernetes Scheduler checks which pods need scheduling.
2. It selects the best node using scheduling algorithms.
3. It creates a **Binding** object behind the scenes to attach the pod to a node.
If **the scheduler is not running**, pods stay in **Pending**:
```scss
kubectl get pods
# NAME     READY   STATUS    RESTARTS   AGE
# nginx    0/1     Pending   0          3s
```
---
# Manual Scheduling Methods
There are **two ways** to manually schedule a pod:

---
# 1. Set `nodeName` While Creating the Pod
This is the **simplest and most common** manual scheduling method.
Example:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
    - name: nginx
      image: nginx
  nodeName: node02
```

When you apply this manifest:
`kubectl apply -f nginx.yaml`

Kubernetes **immediately assigns** the pod to `node02`.  
**The scheduler is bypassed entirely.**

### Notes
- If the node does not exist → pod stays Pending
- If the node is unschedulable → pod stays Pending
---
# 2. Schedule an Existing Pod Using a Binding Object
This method is used when:
- You already created the pod
- You cannot edit or recreate the pod
The official scheduler uses this internally.
### Step 1: Create a Binding Object
`pod-binding-object.yaml`
```yaml
apiVersion: v1
kind: Binding
metadata:
  name: nginx
target:
  apiVersion: v1
  kind: Node
  name: node02
```
### Step 2: Sending POST the binding to the Kubernetes API
Kubernetes accepts Bindings **only via API calls**, not `kubectl apply`.
Example:
```zsh
curl --header "Content-Type: application/json" \
     --request POST \
     --data '{
       "apiVersion": "v1",
       "kind": "Binding",
       "metadata": { "name": "nginx" },
       "target": {
         "apiVersion": "v1",
         "kind": "Node",
         "name": "node02"
       }
     }' \
     http://$SERVER/api/v1/namespaces/default/pods/$PODNAME/binding/
```
Replace:
- `$SERVER` → API server URL
- `$PODNAME` → the pod you want to schedule
Once the binding succeeds, Kubernetes assigns that pod to the specified node.

---
# Summary

| Scenario               | Method                                 | How It Works                              |
| ---------------------- | -------------------------------------- | ----------------------------------------- |
| Pod is not created yet | Add `nodeName` in manifest             | Pod is scheduled immediately to that node |
| Pod already exists     | Create a Binding object + POST request | Manually simulates the scheduler          |
Manual scheduling is rarely used in production, but it is useful for:
- Testing scheduler dependencies
- Understanding how Kubernetes scheduling works internally
- KCNA/CKA exam practice
---
