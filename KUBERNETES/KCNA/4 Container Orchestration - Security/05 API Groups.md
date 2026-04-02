# API Groups

## Kubernetes API Groups (KCNA – Container Orchestration Security)
### 1. Why API Groups Matter
The **Kubernetes API** is the single entry point for **all operations** in a cluster.
- `kubectl`    
- Controllers    
- Schedulers    
- Kubelets    
- External tools (Terraform, Helm, CI/CD)    

All of them **talk to the API server**.
Understanding API groups is essential because:
- **RBAC permissions** are defined using API groups    
- **Authorization decisions** depend on group + resource + verb    
- **Security** controls who can do what in the cluster
---
## 2. Kubernetes API Server Endpoints
The Kubernetes API server exposes multiple HTTP endpoints.
Common ones include:

| Endpoint   | Purpose                                                                                     |
| ---------- | ------------------------------------------------------------------------------------------- |
| `/version` | Cluster version info                                                                        |
| `/healthz` | Health checks                                                                               |
| `/metrics` | Metrics for monitoring                                                                      |
| `/logs`    | Logging integration (third party logging applications)                                      |
| `/api`     | Core API group (core functionality, like namespaces, pods, etc.)                            |
| `/apis`    | Named API groups (apps, extensions, networkign, storage, authentication, certificates etc.) |
For listing all API groups:
`curl http://localhost:6443 -k`
`curl https://localhost:6443/apis -k | grep "name" `

Example:
`curl https://kube-master:6443/version`

This returns cluster metadata like:
- Kubernetes version    
- Git commit    
- Build info    
- Platform    

---
## 3. Core API Group (Legacy / Core Group)
### Key Characteristics
- **No group name**    
- Accessed via `/api/v1`    
- Version is always `v1`    

Example:
`curl https://kube-master:6443/api/v1/pods`

### Core API Resources
These are **fundamental building blocks** of Kubernetes:

| Resource               |
| ---------------------- |
| Pods                   |
| Namespaces             |
| Nodes                  |
| Services               |
| Endpoints              |
| ConfigMaps             |
| Secrets                |
| PersistentVolumes      |
| PersistentVolumeClaims |
| Events                 |
| ReplicationControllers |
| Bindings               |
Example response metadata:
`"apiVersion": "v1"`

This means:
- Resource belongs to **core API group**    
- Version is **v1**    

---

## 4. Named API Groups
As Kubernetes evolved, new features were grouped logically into **named API groups**.

These are accessed via:
`/apis/<group>/<version>`

Example:
`/apis/apps/v1`

---
### Common Named API Groups

|API Group|Purpose|
|---|---|
|`apps`|Deployments, ReplicaSets, StatefulSets|
|`batch`|Jobs, CronJobs|
|`networking.k8s.io`|NetworkPolicies, Ingress|
|`rbac.authorization.k8s.io`|Roles, RoleBindings|
|`authentication.k8s.io`|Auth mechanisms|
|`authorization.k8s.io`|Authorization|
|`storage.k8s.io`|Storage classes|
|`autoscaling`|HPA|
|`certificates.k8s.io`|CSRs|
|`scheduling.k8s.io`|PriorityClasses|
|`policy`|PodSecurityPolicies (legacy)|

Example:
`"apiVersion": "apps/v1"`
This tells you:
- Group: `apps`    
- Version: `v1`    
---
## 5. Listing API Groups from the Cluster
### List All API Endpoints
`curl http://localhost:6443 -k`

Output:
```json
{
  "paths": [
    "/api",
    "/api/v1",
    "/apis",
    "/healthz",
    "/metrics"
  ]
}
```
### List Named API Groups
`curl http://localhost:6443/apis -k | grep "name"`

Example output:
```text
"apps"
"batch"
"networking.k8s.io"
"rbac.authorization.k8s.io"
"scheduling.k8s.io"
```

---
## 6. Resources, Versions, and Verbs
Every Kubernetes resource is defined by **three things**:
### 1. API Group
Example:
- core    
- apps    
- networking.k8s.io    

### 2. Version
Examples:
- v1    
- v1beta1    
- v1alpha1    
### 3. Resource Name
Examples:
- pods    
- deployments    
- services    
---
### Verbs (Actions)
These define **what you can do** with a resource:

|Verb|
|---|
|get|
|list|
|create|
|delete|
|update|
|patch|
|watch|
Example RBAC rule:
```yaml
apiGroups: ["apps"]
resources: ["deployments"]
verbs: ["get", "list", "create"]
```

This means:
- Group: `apps`
- Resource: `deployments`
- Allowed actions: get, list, create
---
## 7. Authentication and Access Control
If you access the API **without authentication**, you get:
`"Forbidden: User \"system:anonymous\" cannot get path \"/\""`
Kubernetes **never allows anonymous access** by default.

---
## 8. kubectl proxy (Important for KCNA)
### What kubectl proxy Does
- Starts a **local HTTP proxy**    
- Uses **your kubeconfig credentials**    
- Avoids manual cert handling    

Command:
`kubectl proxy`
```scss
Starting to serve on 127.0.0.1:8001
```
Access API via:
`curl http://localhost:8001 -k`
This is **secure and authenticated**.

---
## 9. kubectl proxy vs kube-proxy (Exam Favorite)

| Component       | Purpose                   |
| --------------- | ------------------------- |
| `kubectl proxy` | Client-side API proxy     |
| `kube-proxy`    | Pod-to-Service networking |
Important:
- **kubectl proxy** is for users
- **kube-proxy** is for cluster networking    

---
## 10. How API Groups Relate to Security (Very Important)
- **RBAC rules reference API groups**    
- **Authorization checks group + resource + verb**    
- **Admission controllers use API group metadata**    
- **Custom resources register their own API groups**    

Example:
```yaml
apiGroups: ["networking.k8s.io"]
resources: ["networkpolicies"]
verbs: ["create"]
```

---
## 11. KCNA Exam Tips
You should remember:
- Core API group has **no name**
- Core APIs use `/api/v1`
- Named APIs use `/apis/<group>/<version>`
- RBAC always references **apiGroups**
- `kubectl proxy` ≠ `kube-proxy`
- Pods are **core/v1**
- Deployments are **apps/v1**

---
## Final Summary
- Kubernetes API is the control center of the cluster    
- APIs are divided into:    
    - **Core API Group** (`/api/v1`)        
    - **Named API Groups** (`/apis/...`)        
- Every resource is defined by:    
    - API Group        
    - Version        
    - Resource        
- Verbs define allowed actions    
- API groups are foundational to **security, RBAC, and authorization**    

This knowledge directly supports:
- RBAC    
- Authentication    
- Authorization    
- Admission control    
- Secure cluster operations

---
