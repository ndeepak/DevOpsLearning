# Kubernetes Namespaces

## 1. What is a Namespace in Kubernetes?

In simple terms:
> **A Namespace is a logical partition inside a Kubernetes cluster.**

It helps **organize, isolate, and manage** multiple environments or teams **within the same cluster**.

Think of it like folders on your computer:
- You might have `/Documents`, `/Pictures`, `/Music` — all on the same hard drive.    
- Each folder can contain files with the same name (e.g., `notes.txt`), but they won’t clash because they’re in different folders.    

Similarly:
- In Kubernetes, each namespace can contain Pods, Services, and Deployments with the **same names**, but they’re **isolated** from each other.
    

---
## Real-World Analogy
Imagine two kids both named **Mark**:
- In their own homes, each family can just call them “Mark.”    
- But outside, you must specify full names: “Mark Smith” and “Mark Williams.”    

→ In Kubernetes:
- Inside a namespace, a resource name (e.g., `myapp-pod`) must be **unique within that namespace only**.    
- But you can have another `myapp-pod` in another namespace without conflict.
    

---
## 2. Default and System Namespaces
When Kubernetes starts, it automatically creates a few namespaces:

|Namespace|Purpose|
|---|---|
|**default**|Where your resources go if no namespace is specified.|
|**kube-system**|Contains system components (like `kube-dns`, `kube-proxy`, networking plugins). You should not modify resources here.|
|**kube-public**|Contains resources meant to be publicly accessible (like cluster info).|
|**kube-node-lease**|Used for node heartbeat tracking (to monitor node health).|

You can check all namespaces with:
`kubectl get namespaces`

Example output:
```scss
NAME              STATUS   AGE
default           Active   7d
kube-system       Active   7d
kube-public       Active   7d
kube-node-lease   Active   7d
```

---
## 3. Why Namespaces Matter
Namespaces are crucial in production because they:
1. **Isolate environments** – dev, staging, and production can live in one cluster.    
2. **Enforce policies** – like Network Policies and Role-Based Access Control (RBAC).    
3. **Limit resource usage** – using **ResourceQuotas**.    
4. **Simplify management** – teams can manage their own namespaces independently.    

---

## 4. DNS Service Discovery and Namespace Awareness
Kubernetes has an internal DNS naming structure that uses namespaces.
**Within the same namespace:**
- Pods can communicate with a Service using just its name.    

Example:
`db-service`

**Across namespaces:**
- Use the _fully qualified domain name (FQDN)_:    

`db-service.dev.svc.cluster.local`

Breaking this down:
- `db-service` → service name    
- `dev` → namespace    
- `svc` → service subdomain    
- `cluster.local` → default cluster domain    

So if a Pod in the **default** namespace wants to access a service named `db-service` in **dev**, it must use:
`mysql.connect("db-service.dev.svc.cluster.local")`

---

## 5. Working with Namespaces using kubectl
### View all namespaces
`kubectl get namespaces`

### View Pods in the current namespace (default)
`kubectl get pods`

### View Pods in another namespace
`kubectl get pods --namespace=kube-system`

Example output:
```scss
NAME                                 READY   STATUS    RESTARTS   AGE
coredns-78fcd6894-92d52              1/1     Running   7          7d
kube-apiserver-master                1/1     Running   7          7d
kube-scheduler-master                1/1     Running   7          7d
```
### View Pods across all namespaces
`kubectl get pods --all-namespaces`

---
## 6. Creating Pods in Specific Namespaces
### Option 1: Default namespace
If your Pod YAML does **not** specify a namespace, it goes into the **default** namespace.

Example:
```yaml
# pod-definition.yml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: nginx-container
    image: nginx
```
Create it:
`kubectl create -f pod-definition.yml`

→ This goes to the **default** namespace.

---

### Option 2: Specify namespace in command line
`kubectl create -f pod-definition.yml --namespace=dev`

---

### Option 3: Specify namespace inside YAML
```yaml
# pod-definition.yml (namespace specified)
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  namespace: dev
  labels:
    app: myapp
spec:
  containers:
  - name: nginx-container
    image: nginx
```

Then simply:
`kubectl create -f pod-definition.yml`

---

## 7. Creating a Namespace
### YAML method
```yaml
# namespace-dev.yml
apiVersion: v1
kind: Namespace
metadata:
  name: dev
```
Apply it:
`kubectl create -f namespace-dev.yml`

Output:
`namespace/dev created`

### Command-line method
`kubectl create namespace dev`

Check:
`kubectl get namespaces`

---

## 8. Switching the Active Namespace
By default, `kubectl` commands use the **default namespace**.
To permanently switch the current context’s namespace:
`kubectl config set-context $(kubectl config current-context) --namespace=dev`

Now, running:
`kubectl get pods`

will show Pods in the **dev** namespace by default.

---

## 9. Setting Resource Quotas per Namespace
Namespaces can have **quotas** to prevent one environment or team from consuming all cluster resources.
Example quota definition:
```yaml
# compute-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: dev
spec:
  hard:
    pods: "10"
    requests.cpu: "4"
    requests.memory: 5Gi
    limits.cpu: "10"
    limits.memory: 10Gi
```

Apply it:

`kubectl create -f compute-quota.yaml`

This means:
- The `dev` namespace can have **up to 10 Pods**.    
- The total CPU requested by Pods ≤ 4 cores.    
- The total memory requested ≤ 5Gi.    
- Hard limits are 10 CPU cores and 10Gi memory.    

---
## 10. Common Namespace Commands Recap

|Task|Command|
|---|---|
|List namespaces|`kubectl get namespaces`|
|Create a namespace|`kubectl create namespace dev`|
|Delete a namespace|`kubectl delete namespace dev`|
|View resources in a namespace|`kubectl get all -n dev`|
|Switch active namespace|`kubectl config set-context $(kubectl config current-context) --namespace=dev`|
|List Pods in all namespaces|`kubectl get pods --all-namespaces`|

---
## 11. Key Takeaways

- **Namespace = logical isolation** within the same Kubernetes cluster.    
- Use **different namespaces** for different environments (dev, test, prod).    
- System components live in **kube-system**.    
- Use `--namespace` flag or specify namespace in YAML.    
- Use **ResourceQuota** to control usage.    
- DNS inside Kubernetes respects namespaces (`service.namespace.svc.cluster.local`).    

---

