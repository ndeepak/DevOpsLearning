# Deployments
[[Kubernetes Deployments]]
## 1. What Is a Deployment?
A **Deployment** is a higher-level Kubernetes object that **manages ReplicaSets**, which in turn manage **Pods**.  
It builds upon the foundation of ReplicaSets to add important production-level features like:

- **Rolling updates** (gradually replace old Pods with new ones)    
- **Rollbacks** (revert to a previous stable version if something fails)    
- **Pause and resume** (control rollout progress)    
- **Declarative updates** (apply new configurations safely)    
- **Version history** (track previous ReplicaSets)    

In short:
> **Pods** → run your containers  
> **ReplicaSets** → ensure a fixed number of Pods  
> **Deployments** → control and version your ReplicaSets

---

## 2. Why Not Use ReplicaSets Directly?
ReplicaSets guarantee that a specific number of Pods are running, but they **lack version control and update mechanisms**.
For example:
- You have 3 Pods running version `nginx:1.18`.    
- You want to update to `nginx:1.19`.    

With a ReplicaSet, you’d have to:
1. Delete the old ReplicaSet.    
2. Create a new one with the new image.    

This causes downtime and manual intervention.
A **Deployment**, however:
- Automatically creates a **new ReplicaSet** for the new version.    
- Gradually replaces Pods from the old ReplicaSet with those from the new one.    
- Keeps the old ReplicaSet until you confirm stability (allowing rollbacks).    

This makes Deployments **safer**, **automated**, and **declarative**.

---

## 3. Deployment YAML Structure
A Deployment YAML looks very similar to a ReplicaSet definition — just the `kind` field changes.
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

### Let’s break this down:

|Section|Description|
|---|---|
|**apiVersion**|For Deployments, use `apps/v1`|
|**kind**|Specifies that this object is a `Deployment`|
|**metadata**|Names and labels the Deployment|
|**spec.replicas**|How many Pod replicas to maintain|
|**spec.selector**|Determines which Pods this Deployment manages|
|**spec.template**|Blueprint for Pods (same as in ReplicaSets)|

---

## 4. Creating and Viewing a Deployment
### Create a Deployment
`kubectl create -f deployment-definition.yml`

### List Deployments
`kubectl get deployments`

Example output:
```scss
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
myapp-deployment   3/3     3            3           21s
```
### Check the ReplicaSet Created by the Deployment
`kubectl get replicaset`

You’ll see something like:
`myapp-deployment-6795844b58   3   3   3   2m`

### Check the Pods
`kubectl get pods`
```scss
myapp-deployment-6795844b58-5rbj1   1/1   Running   0   2m
myapp-deployment-6795844b58-h4w55   1/1   Running   0   2m
myapp-deployment-6795844b58-1fjhv   1/1   Running   0   2m
```
### View Together
`kubectl get all`

This shows:
- The **Deployment**    
- The **ReplicaSet** it created    
- The **Pods** managed by that ReplicaSet    

---

## 5. How Deployments Manage Updates (Rolling Updates)
A **rolling update** means new Pods are gradually rolled out while old ones are terminated — ensuring **zero downtime**.
For example, if you change the image version in your YAML:
```yaml
containers:
- name: nginx-container
  image: nginx:1.25
```

and apply the change:
`kubectl apply -f deployment-definition.yml`

Kubernetes:
1. Creates a **new ReplicaSet** for the new version.    
2. Gradually **scales up** the new ReplicaSet and **scales down** the old one.    
3. Maintains service availability throughout the process.    

You can check rollout status using:
`kubectl rollout status deployment/myapp-deployment`

If everything is fine, you’ll see:
`deployment "myapp-deployment" successfully rolled out`

---

## 6. Rollbacks (Undoing a Faulty Update)
If a new version fails or behaves incorrectly, you can easily roll back.
### Command:
`kubectl rollout undo deployment/myapp-deployment`
This immediately reverts to the previous stable ReplicaSet.
You can check rollout history:
`kubectl rollout history deployment/myapp-deployment`

Each update (revision) is recorded, allowing you to revert to specific versions if needed.

---

## 7. Pausing and Resuming Deployments
Sometimes, you might want to **pause** an ongoing rollout to inspect or modify settings.
### Pause a Deployment:
`kubectl rollout pause deployment/myapp-deployment`

Make configuration changes to your YAML (e.g., image, resource limits).
Then **resume** it:
`kubectl rollout resume deployment/myapp-deployment`

---

## 8. Scaling Deployments
Scaling a Deployment works exactly like ReplicaSets — but simpler.

### Option 1: Edit YAML
Change:
`replicas: 3`

to:
`replicas: 6`

and apply:
`kubectl apply -f deployment-definition.yml`

### Option 2: Use the scale command
`kubectl scale --replicas=6 deployment/myapp-deployment`

Kubernetes updates the underlying ReplicaSet accordingly.

---
## 9. Key Deployment Commands

|Command|Description|
|---|---|
|`kubectl create -f deployment.yml`|Create a new Deployment|
|`kubectl get deployments`|List Deployments|
|`kubectl get replicaset`|List underlying ReplicaSets|
|`kubectl get pods`|List Pods created by Deployments|
|`kubectl rollout status deployment/myapp`|Check rollout progress|
|`kubectl rollout undo deployment/myapp`|Roll back to a previous version|
|`kubectl rollout history deployment/myapp`|View version history|
|`kubectl scale --replicas=6 deployment/myapp`|Scale Deployment replicas|
|`kubectl delete deployment myapp`|Delete a Deployment and its Pods|

---

## 10. How Deployments Interact Internally

Here’s what happens inside Kubernetes when you create or update a Deployment:

1. You apply a Deployment YAML.    
2. The Deployment controller:    
    - Creates (or updates) a ReplicaSet.        
    - Ensures the ReplicaSet maintains the specified number of Pods.
        
3. During updates:    
    - It creates a **new ReplicaSet** for the new version.        
    - Gradually shifts Pods from the old to the new ReplicaSet.        
    - Monitors progress and status.
        
4. If something goes wrong:    
    - You can pause, resume, or roll back safely.        

So, a Deployment acts as the **brain** that coordinates everything — Pods, ReplicaSets, and version control.

---

## 11. Summary

|Concept|Purpose|
|---|---|
|**Pod**|Runs a single instance of your app|
|**ReplicaSet**|Maintains a fixed number of Pod replicas|
|**Deployment**|Manages ReplicaSets and enables updates, rollbacks, and scaling|

### Key Advantages of Deployments

- Rolling updates with **zero downtime**    
- Rollback capability    
- Declarative configuration    
- History tracking    
- Pause/resume rollouts    
- Simplified scaling