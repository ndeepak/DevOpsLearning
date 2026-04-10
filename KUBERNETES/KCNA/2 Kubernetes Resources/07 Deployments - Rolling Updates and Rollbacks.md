# Deployments - Rolling Updates and Rollbacks
[[Kubernetes Deployments]]

## 1. **Understanding What a Deployment Really Is**
A **Deployment** is one of the most powerful controllers in Kubernetes. It manages **Pods** indirectly — not by creating them itself, but by creating and controlling a **ReplicaSet**, which in turn manages the Pods.

When you create a Deployment:
- Kubernetes creates a **ReplicaSet** under it.    
- That ReplicaSet creates the desired number of **Pods**.    
- The Deployment watches the ReplicaSet and ensures it matches the desired state.    

If you update the Deployment later (e.g., new image), the Deployment:
- Creates a **new ReplicaSet** for the new version.    
- Gradually **scales up** the new ReplicaSet.    
- Simultaneously **scales down** the old one.    
- Maintains zero downtime (if RollingUpdate strategy is used).    

This entire process is called a **rollout**.

---

## 2. **Rollout Process (Versioning System)**
A **rollout** is what happens when:
- A new Deployment is created, or    
- A change is made to the Deployment spec that affects the Pod template.    

Each rollout corresponds to a **new revision number**.  
Revisions are stored as **annotations** on the Deployment and ReplicaSets.

You can check rollout history using:
`kubectl rollout history deployment/myapp-deployment`

Example output:
```scss
deployment.apps/myapp-deployment
REVISION  CHANGE-CAUSE
1         kubectl apply --filename=deployment-definition.yml
2         kubectl set image deployment/myapp-deployment nginx-container=nginx:1.9.1
```
> **Note:** You can add the `--record` flag when you create or apply a deployment to store what command caused the change.

---

## 3. **Deployment Strategies**
There are **two core strategies** for handling rollouts:
### a. **Recreate Strategy**
Behavior:
- All old Pods are killed **immediately**.    
- Then new Pods are started.    
- Causes **downtime** between termination and new pod readiness.    

You can specify it like this:
```yaml
spec:
  strategy:
    type: Recreate
```

Use this when:
- You can tolerate short downtime.    
- Old and new versions **cannot run simultaneously** (e.g., incompatible DB schema changes).
    

---

### b. **RollingUpdate Strategy (Default)**
Behavior:
- Gradually replaces old Pods with new ones.    
- Keeps your app available throughout the update.    

You can control how many Pods are updated simultaneously with two parameters:
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
```

**maxUnavailable** — the max number of Pods that can be unavailable during the update.  
**maxSurge** — the max number of _extra_ Pods (beyond the desired count) allowed temporarily.

Example:  
If your Deployment has 5 replicas:
- `maxUnavailable: 1` → at least 4 pods must be running at all times.    
- `maxSurge: 1` → at most 6 pods total can run during the update.
    

---

## 4. **How Kubernetes Performs a Rolling Update Internally**
Let’s say you have this Deployment:
```yaml
spec:
  replicas: 5
  template:
    spec:
      containers:
      - name: nginx-container
        image: nginx:1.7.0
```

You update the image to `nginx:1.7.1`.
Here’s what happens internally:
1. **New ReplicaSet Created**  
    Kubernetes detects a change in the Pod template and creates a **new ReplicaSet** for the updated image.
    
2. **Scaling Up/Down**    
    - The new ReplicaSet starts creating new Pods (based on maxSurge).        
    - The old ReplicaSet starts deleting old Pods (based on maxUnavailable).
        
3. **Controller Loop**  
    The Deployment controller continuously checks both ReplicaSets until:    
    - The new one reaches the desired count.        
    - The old one scales down to 0.        
4. **Old ReplicaSet Retained (for Rollback)**  
    The old ReplicaSet is not deleted — it stays around with zero replicas so you can roll back easily.
    

You can verify this by running:
`kubectl get replicaset`

You’ll see both old and new ReplicaSets listed:
```scss
NAME                              DESIRED   CURRENT   READY   AGE
myapp-deployment-6795844b58       0         0         0       1h
myapp-deployment-7d57dbbd8d       5         5         5       2m
```

---

## 5. **Observing Rollout Progress**
To check real-time rollout progress:
`kubectl rollout status deployment/myapp-deployment`
You’ll see:
```scss
Waiting for rollout to finish: 2 of 5 updated replicas are available...
deployment "myapp-deployment" successfully rolled out
```

To see detailed rollout information (conditions, events, strategy):
`kubectl describe deployment myapp-deployment`

---

## 6. **Updating a Deployment**
There are two ways to update a deployment:
### a. **Declarative (recommended)**
Edit your YAML file and reapply:
`kubectl apply -f deployment-definition.yml`

This keeps your configuration consistent and version-controlled.
### b. **Imperative**
Quick updates without editing files:
`kubectl set image deployment/myapp-deployment nginx-container=nginx:1.9.1`

or
`kubectl scale deployment myapp-deployment --replicas=10`

Use this for temporary fixes or testing.

---

## 7. **Rollback Mechanism**
If a deployment update fails (e.g., app not working properly), you can revert to the last working revision:
`kubectl rollout undo deployment/myapp-deployment`

To rollback to a specific revision:
`kubectl rollout undo deployment/myapp-deployment --to-revision=1`

To check the rollback details:
`kubectl rollout history deployment/myapp-deployment`

---

## 8. **Pausing and Resuming Rollouts**
You can **pause** a rollout mid-way, make multiple changes, then **resume** — allowing you to batch changes safely.
Pause:
`kubectl rollout pause deployment/myapp-deployment`
Make modifications (e.g., image, replicas).
Resume:
`kubectl rollout resume deployment/myapp-deployment`

This is useful for **staged rollouts** — applying multiple updates without triggering separate rollouts for each one.

---

## 9. **Deployment Lifecycle Summary**

|Phase|Action|Description|
|---|---|---|
|1|Create Deployment|Creates initial ReplicaSet and Pods|
|2|Update Deployment|New ReplicaSet created, old one scaled down|
|3|Rollout Status|Progress monitored via Deployment controller|
|4|Rollback|Old ReplicaSet reactivated if needed|
|5|Cleanup|Old ReplicaSets optionally pruned using revision history limits|

---

## 10. **Revision History Limit**
You can configure how many old ReplicaSets to retain for rollback:
```yaml
spec:
  revisionHistoryLimit: 3
```

If you set it to 3, only the last three revisions are kept. Older ReplicaSets will be deleted automatically.

---
## 11. **Common Deployment Commands Recap**

|Command|Description|
|---|---|
|`kubectl create -f deployment.yml`|Create a new deployment|
|`kubectl get deployments`|List all deployments|
|`kubectl describe deployment <name>`|Show detailed info|
|`kubectl rollout status deployment/<name>`|Monitor rollout progress|
|`kubectl set image deployment/<name> <container>=<image>`|Update container image|
|`kubectl rollout history deployment/<name>`|View revision history|
|`kubectl rollout undo deployment/<name>`|Roll back to previous revision|
|`kubectl rollout pause/resume deployment/<name>`|Temporarily stop/resume rollouts|
|`kubectl get rs`|Show ReplicaSets created by Deployments|
|`kubectl get pods`|View Pods created by ReplicaSets|

---

## 12. **Why Rolling Updates Are Safer**

Rolling updates are preferred because they:
- Keep your service **available** (no downtime).    
- Allow **real-time health checks**.    
- Provide **fast rollback** if new Pods fail readiness probes.    
- Enable **canary-style** or **progressive** deployment approaches.
    

---
For more details, consult the official [Kubernetes Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).