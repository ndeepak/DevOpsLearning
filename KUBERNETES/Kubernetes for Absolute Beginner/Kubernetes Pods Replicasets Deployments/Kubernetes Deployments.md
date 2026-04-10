# Kubernetes Deployments
## 1. Background: Pods and ReplicaSets
Before we get to **Deployments**, remember:
- A **Pod** is the smallest deployable unit in Kubernetes — it runs one or more containers (usually one).    
- A **ReplicaSet** ensures a specified number of **Pods** are always running.    
    - Example: You want 3 nginx Pods; if one dies, ReplicaSet creates another.

---
## 2. What is a Deployment?
A **Deployment** in Kubernetes automates how Pods are created, scaled, and updated. It builds on **ReplicaSets** to ensure the correct number of Pods are running at all times, even during upgrades or failures.
A **Deployment** is a **controller** that manages ReplicaSets and provides higher-level features like:

| Feature             | Description                                               |
| ------------------- | --------------------------------------------------------- |
| **Rolling Updates** | Update Pods to a new version gradually (no downtime).     |
| **Rollbacks**       | Revert to an older version if something goes wrong.       |
| **Scaling**         | Easily change replica count (up or down).                 |
| **Pause/Resume**    | Temporarily stop rollout to make changes or troubleshoot. |
Key purposes:
- Automate rollout of application updates
- Ensure zero downtime (through rolling updates)
- Allow smooth rollback if a new release fails
- Scale applications up or down easily    
- Pause/resume updates when necessary
Structure:  
**Deployment → ReplicaSet → Pod**
Think of it like this:
`Deployment → manages ReplicaSet → manages Pods`

## How Deployments Work
1. **Deployment**
    - Defines the desired state (how many Pods, which image, what labels).
    - Supports advanced actions like rolling updates, rollbacks, and scaling.
2. **ReplicaSet**
    - Ensures the specified number of Pods are running.
    - Created automatically by the Deployment.
3. **Pod**
    - The running instance of your container (e.g., Nginx web server).

---
## 3. Deployment Example YAML
Here’s the example you saw:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
  labels:
    app: myapp
    type: front-end
spec:
  replicas: 3
  selector:
    matchLabels:
      type: front-end
  template:
    metadata:
      name: myapp-pod
      labels:
        app: myapp
        type: front-end
    spec:
      containers:
      - name: nginx-container
        image: nginx
```

### Breakdown:
- **apiVersion:** tells Kubernetes this uses Deployment API. Defines which API version handles this Deployment.   
- **kind:** defines the object type i.e. Deployment object.    
- **metadata:** contains the name and labels.    
- **spec.replicas:** how many Pods you want.    
- **spec.selector:** matches which Pods this Deployment will manage.    
- **spec.template:** defines the Pod’s template (same as in ReplicaSet/Pod manifest) (container image, labels,etc.).

---
## 4. Creating the Deployment
Save that YAML as `deployment-definition.yml`, then run:
`kubectl create -f deployment-definition.yml`
To verify:
```bash
kubectl get deployments
kubectl get replicaset
kubectl get pods
kubectl get all
```
### Example output:
```pgsql
NAME                DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
myapp-deployment    3         3         3            3           2m
```

Kubernetes automatically:
1. Creates a **ReplicaSet** (`myapp-deployment-<hash>`)
2. That ReplicaSet creates **3 Pods**    
3. Each Pod runs **nginx**

---
## 5. Rolling Updates
Now, imagine you want to update the nginx image to a newer version:
`kubectl set image deployment/myapp-deployment nginx-container=nginx:1.19`

Kubernetes will:
- Gradually terminate old Pods (v1)    
- Spin up new Pods (v2)    
- Maintain desired replicas throughout → **zero downtime**    

Check rollout status:
`kubectl rollout status deployment/myapp-deployment`

---

## 6. Rollback to Previous Version
If something goes wrong:
`kubectl rollout undo deployment/myapp-deployment`

You can also check previous versions:
`kubectl rollout history deployment/myapp-deployment`

---

## 7. Pause & Resume a Deployment
Pause the rollout (e.g., during config changes):
`kubectl rollout pause deployment/myapp-deployment`

Make edits, then resume:
`kubectl rollout resume deployment/myapp-deployment`

---
## 8. Scaling a Deployment
To scale replicas:
`kubectl scale deployment myapp-deployment --replicas=5`

→ Now 5 Pods will run.
Or modify directly in YAML and reapply:

`kubectl apply -f deployment-definition.yml`

---
##  9. Deleting a Deployment
When you’re done:
`kubectl delete deployment myapp-deployment`

This also deletes its ReplicaSet and Pods.

---
## 10. Summary Chart

| Kubernetes Object | Responsibility                                           |
| ----------------- | -------------------------------------------------------- |
| **Pod**           | Runs one or more containers                              |
| **ReplicaSet**    | Ensures desired number of Pods are running               |
| **Deployment**    | Manages ReplicaSets, handles updates, rollbacks, scaling |

---

## Common Commands Cheat Sheet

|Task|Command|
|---|---|
|Create deployment|`kubectl create -f deployment.yml`|
|View all|`kubectl get all`|
|View deployments|`kubectl get deployments`|
|View rollout history|`kubectl rollout history deployment/myapp-deployment`|
|Rollback|`kubectl rollout undo deployment/myapp-deployment`|
|Update image|`kubectl set image deployment/myapp-deployment nginx-container=nginx:1.19`|
|Scale replicas|`kubectl scale deployment myapp-deployment --replicas=5`|
|Pause/Resume|`kubectl rollout pause/resume deployment/myapp-deployment`|

---
