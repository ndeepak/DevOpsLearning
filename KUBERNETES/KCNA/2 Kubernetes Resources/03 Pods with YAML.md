# Pods with YAML
[[KUBERNETES/Kubernetes for Absolute Beginner/Kubernetes Pods Replicasets Deployments/Pods with YAML]]
## 1. Kubernetes YAML Basics
Every Kubernetes manifest file follows a **common structure** of **four main fields**:
```yaml
apiVersion: <string>
kind: <string>
metadata:
  ...{Dictionary}
spec:
  ... {List or Array}
```

Each part serves a specific purpose:

|Field|Purpose|
|---|---|
|**apiVersion**|Defines which version of the Kubernetes API to use for that object.|
|**kind**|Tells Kubernetes what object type this is (Pod, Deployment, Service, etc.).|
|**metadata**|Stores identifying information like name, namespace, and labels.|
|**spec**|Contains the actual configuration details — how the object behaves.|

---

## 2. Example: Minimal Pod Definition
Here is a **basic pod YAML** running an **nginx container**:
```yaml
apiVersion: v1
kind: Pod
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

### Explanation:
- **apiVersion: v1**  
    Pods belong to the **core API group**, so we use `v1`.
    
- **kind: Pod**  
    Tells Kubernetes we’re defining a Pod.
    
- **metadata:**    
    - `name`: Unique name within the namespace.        
    - `labels`: Key-value pairs used for identification, grouping, and selection (very important for Services and ReplicaSets).
        
- **spec:**  
    Defines the configuration of the containers inside the Pod.    
    - The **containers** list must have at least one entry.        
    - Each container defines:        
        - `name`            
        - `image`            
        - (optionally) `ports`, `env`, `resources`, etc.            

---

## 3. Creating the Pod
Save the above file as **pod-definition.yml**, then run:
`kubectl create -f pod-definition.yml`
Check if the Pod is created:
`kubectl get pods`

Output (example):
```lua
NAME        READY   STATUS    RESTARTS   AGE
myapp-pod   1/1     Running   0          20s
```

To see full details:
`kubectl describe pod myapp-pod`

You’ll see sections like:
- Node assignment (which node it’s running on)    
- Labels and annotations    
- Container details    
- Events (image pulling, container start, etc.)    

---

## 4. Enhanced Pod Definition Example
You can add more configuration such as ports, environment variables, and volume mounts.
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: webserver-pod
  labels:
    app: webserver
spec:
  containers:
    - name: nginx-container
      image: nginx:latest
      ports:
        - containerPort: 80
      env:
        - name: ENVIRONMENT
          value: production
```

This pod runs Nginx on port 80 and has an environment variable set.  
To apply:
`kubectl apply -f webserver-pod.yml`

---

## 5. Multi-Container Pod Example
Pods can run multiple containers that share networking and storage.
Example:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
  labels:
    app: log-demo
spec:
  containers:
    - name: web-container
      image: nginx
      ports:
        - containerPort: 80
    - name: log-agent
      image: busybox
      command: ["sh", "-c", "while true; do echo 'logging...'; sleep 5; done"]
```

**Key points:**
- Both containers share the same network namespace.    
- They can communicate using `localhost`.    
- They share Pod lifecycle (start, stop, restart together).    

---

## 6. Debugging and Inspection Commands
You should know these commands for the CKA exam:

|Command|Purpose|
|---|---|
|`kubectl get pods`|List pods|
|`kubectl get pods -o wide`|Show pods with node/IP info|
|`kubectl describe pod <pod-name>`|Detailed info|
|`kubectl logs <pod-name>`|Show container logs|
|`kubectl exec -it <pod-name> -- /bin/sh`|Access container shell|
|`kubectl delete pod <pod-name>`|Delete pod|
|`kubectl apply -f file.yml`|Create or update an object|

---

## 7. Useful Tips for Exam and Real Use
- Indentation in YAML **must be exact** (two spaces per level).    
- Always check `apiVersion` — different objects use different API groups.    
- Labels are critical — they link Pods to higher-level controllers like Deployments and Services.    
- Use `kubectl explain <object>` to view YAML field documentation:    
    `kubectl explain pod.spec.containers`    
---
## 8. Summary Table

|Section|Description|
|---|---|
|**apiVersion**|API group and version for the object (Pods use `v1`)|
|**kind**|Type of Kubernetes object (`Pod`, `Deployment`, etc.)|
|**metadata**|Identifiers like `name`, `namespace`, and `labels`|
|**spec**|Actual configuration (containers, ports, env vars, etc.)|
|**Command**|`kubectl create -f file.yml` or `kubectl apply -f file.yml`|
|**Verification**|`kubectl get pods`, `kubectl describe pod <name>`|

---

