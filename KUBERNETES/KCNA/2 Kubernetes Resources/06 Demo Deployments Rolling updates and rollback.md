# Demo Deployments Rolling updates and rollback

This covers everything you would _do_ in the terminal to perform, monitor, and manage rolling updates and rollbacks for a Kubernetes deployment.

---
### 1. Deployment Definition
Here’s the deployment YAML file (`deployment.yaml`):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
  labels:
    tier: frontend
spec:
  selector:
    matchLabels:
      app: myapp
  replicas: 6
  template:
    metadata:
      name: nginx-2
      labels:
        app: myapp
    spec:
      containers:
        - name: nginx
          image: nginx
```

This configuration tells Kubernetes to create a Deployment named `myapp-deployment`, which runs 6 replicas (Pods) of the `nginx` image.

---

### 2. Creating the Deployment
First, check that there are no existing deployments:
`kubectl get deployments`

Then create the deployment:
`kubectl create -f deployment.yaml`

Monitor its rollout:
`kubectl rollout status deployment.apps/myapp-deployment`

You’ll see messages such as:
`deployment "myapp-deployment" successfully rolled out`

If you check the rollout status immediately after creation, you may see progress updates like `1 of 6 updated replicas`.

---

### 3. Demonstrating the Rollout Process
To visualize how rollout works, delete and recreate the deployment quickly:
```zsh
kubectl delete deployment myapp-deployment
kubectl create -f deployment.yaml
kubectl rollout status deployment.apps/myapp-deployment
```

You might see:
`Waiting for deployment "myapp-deployment" rollout to finish: 3 of 6 updated replicas are available...`

This shows Kubernetes gradually updating and waiting until all pods are ready before marking the rollout complete.

---

### 4. Checking Rollout History
After the deployment is up:
`kubectl rollout history deployment.apps/myapp-deployment`

Output:
```scss
REVISION  CHANGE-CAUSE
1         <none>
```

Since no change cause was recorded, the `CHANGE-CAUSE` field is empty.

---
### 5. Recording Change Causes
To record change causes, recreate the deployment using the `--record` flag:
```zsh
kubectl delete deployment myapp-deployment
kubectl create -f deployment.yaml --record
kubectl rollout status deployment.apps/myapp-deployment
```

Then check the history again:
`kubectl rollout history deployment.apps/myapp-deployment`

Output:
```scss
REVISION  CHANGE-CAUSE
1         kubectl create --filename=deployment.yaml --record=true
```

---

### 6. Updating the Deployment with `kubectl edit`
View current deployment details:
`kubectl describe deployment myapp-deployment`

Now update the container image interactively:
`kubectl edit deployment myapp-deployment --record`

Change the image line to:
`image: nginx:1.18`

Save and exit the editor. Kubernetes will begin a **rolling update**, replacing old pods with new ones that use `nginx:1.18`.

Monitor progress:
`kubectl rollout status deployment.apps/myapp-deployment`

Then verify the rollout history:
`kubectl rollout history deployment.apps/myapp-deployment`

You’ll see something like:
```scss
REVISION  CHANGE-CAUSE
1         kubectl create --filename=deployment.yaml --record=true
2         kubectl edit deployment myapp-deployment --record=true
```

---

### 7. Updating the Deployment with `kubectl set image`

Another way to update the image:
`kubectl set image deployment myapp-deployment nginx=nginx:1.18-perl --record`

Check rollout progress:
`kubectl rollout status deployment/myapp-deployment`

Then confirm the new revision:
`kubectl rollout history deployment/myapp-deployment`

Expected result:
```scss
REVISION  CHANGE-CAUSE
1         kubectl create ...
2         kubectl edit deployment myapp-deployment --record=true
3         kubectl set image deployment myapp-deployment nginx=nginx:1.18-perl --record=true
```
---

### 8. Rolling Back to a Previous Revision
If the new image causes issues, roll back to the previous version:
`kubectl rollout undo deployment/myapp-deployment`

Monitor rollback:
`kubectl rollout status deployment/myapp-deployment`

Check the current state:
`kubectl describe deployment myapp-deployment`

You’ll see that the image has reverted to the previous stable version.

---

### 9. Simulating a Failed Rollout
To simulate failure, edit the deployment again and set an invalid image name:

`kubectl edit deployment myapp-deployment --record`

Change to:
`image: nginx:1.18-does-n`

Save and exit.

Check rollout status:
`kubectl rollout status deployment/myapp-deployment`

Check pods:
`kubectl get pods`

Output might show:
```scss
ErrImagePull
ImagePullBackOff
```

Kubernetes will continue running the old pods that are still healthy, keeping the application available even though some pods failed to update.

---

### 10. Rolling Back the Failed Deployment
To restore stability, roll back again:
`kubectl rollout undo deployment/myapp-deployment`

Monitor:
`kubectl rollout status deployment/myapp-deployment`

Verify that all pods are running properly:
`kubectl get pods`

Output should show all pods running a valid image version:


View rollout history:
`kubectl rollout history deployment/myapp-deployment`

You’ll see all recorded revisions with their change causes.

---

### 11. Summary of Commands Used

|Action|Command|
|---|---|
|Create deployment|`kubectl create -f deployment.yaml`|
|Check rollout status|`kubectl rollout status deployment/myapp-deployment`|
|View rollout history|`kubectl rollout history deployment/myapp-deployment`|
|Record changes|Add `--record` flag to create/edit/set commands|
|Update interactively|`kubectl edit deployment myapp-deployment --record`|
|Update via CLI|`kubectl set image deployment myapp-deployment nginx=<new-image> --record`|
|Roll back|`kubectl rollout undo deployment/myapp-deployment`|
|Check pods|`kubectl get pods`|
|Simulate failure|Set invalid image, e.g. `nginx:does-not-exist`|

---

