# `kubectl apply` Command
### Purpose
`kubectl apply` is the **declarative** command used to create or modify Kubernetes resources (like Pods, Deployments, Services, etc.) from a YAML or JSON file.

It tells Kubernetes:
> “Ensure that the cluster’s actual state matches this desired state I’ve defined in my YAML file.”

---
### Syntax
`kubectl apply -f <filename.yaml>`
**Examples:**
```bash
kubectl apply -f nginx.yml
kubectl apply -f /path/to/directory/
kubectl apply -f https://k8s.io/examples/controllers/nginx-deployment.yaml
```
You can even apply all YAMLs in a directory at once.

---
### What Happens Internally
When you run:
`kubectl apply -f nginx.yml`

Here’s what happens:
1. **kubectl reads the YAML file** — for example, `nginx.yml` defines a Deployment.    
2. It checks if that object already exists in the cluster.    
3. If it **doesn’t exist** → it **creates** it.    
4. If it **exists** → it **updates** only the parts that changed.    
5. Kubernetes **reconciles** the current state to match the new desired state.

---
### Why `kubectl apply` is Preferred
- You don’t need to remember whether to use `create` or `replace`.
- It allows **incremental updates** — you can keep applying changes safely.    
- Works great with **GitOps**, where your YAML files are version-controlled.    
- It tracks configuration history in an **annotation** (`kubectl.kubernetes.io/last-applied-configuration`), which helps it compare differences for the next apply.    

### Examples
#### 1. Create a Deployment
`kubectl apply -f nginx-deployment.yaml`

#### 2. Modify replicas
Change this part in your YAML:
`spec:   replicas: 3`

→ to
`spec:   replicas: 5`

Then re-apply:
`kubectl apply -f nginx-deployment.yaml`

Kubernetes will **scale up** automatically.

#### 3. Apply multiple files
`kubectl apply -f deployment.yaml -f service.yaml`

#### 4. Apply all YAMLs in a folder
`kubectl apply -f ./configs/`

---
### Related Useful Options

|Flag|Description|
|---|---|
|`-f`|Specify file or directory|
|`--dry-run=client`|Check what would happen without applying|
|`--record`|Record the command in the object’s annotation|
|`--prune`|Delete resources not defined in the given files|
|`--recursive`|Process directories recursively|

Example:
`kubectl apply -f ./k8s-configs/ --recursive --prune`

---
### Summary

|Action|Command|Effect|
|---|---|---|
|Create new resource|`kubectl apply -f nginx.yml`|Creates if not found|
|Update resource|`kubectl apply -f nginx.yml`|Patches differences|
|Safe and declarative|Yes|Automatically reconciles state|

---
