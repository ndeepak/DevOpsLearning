# Cluster Roles
# What Is a ClusterRole in Kubernetes?
A **ClusterRole** is an RBAC object that defines **permissions at the cluster scope**.

It is used when:
- You want to control access to **cluster-scoped resources**    
- OR you want to grant **the same permissions across all namespaces**    
---
## One-Line Exam Definition
> A ClusterRole defines permissions for cluster-scoped resources or namespace-scoped resources across all namespaces.

---
# Why Do We Need ClusterRoles?
Regular **Roles** are:
- Namespace-scoped    
- Limited to one namespace only    

But some resources:
- Do **not belong to any namespace**    
- Exist **once per cluster**    

Examples:
- Nodes    
- PersistentVolumes    
- Namespaces    
- CertificateSigningRequests    

You **cannot manage these using a Role**.
That is why Kubernetes introduced:
- **ClusterRole**    
- **ClusterRoleBinding**    

---
# Namespaced vs Cluster-Scoped Resources (Critical Concept)
## Namespaced Resources
These live **inside a namespace**:
- Pods    
- replicasets
- jobs
- Services    
- Deployments    
- ConfigMaps    
- Secrets    
- Roles    
- RoleBindings    
- configmaps
- PVC
## Cluster-Scoped Resources
These exist **at cluster level**:
- Nodes    
- PersistentVolumes    
- Namespaces    
- ClusterRoles    
- ClusterRoleBindings    
- CSRs (CertificateSigningRequests)    

Commands to verify:
```bash
kubectl api-resources --namespaced=true
kubectl api-resources --namespaced=false
```

---
# Key Difference: Role vs ClusterRole

| Feature            | Role             | ClusterRole    |
| ------------------ | ---------------- | -------------- |
| Scope              | Single namespace | Entire cluster |
| Used for nodes     | No               | Yes            |
| Used for PVs       | No               | Yes            |
| Can manage pods    | Yes              | Yes            |
| Namespace required | Yes              | No             |

---
# Creating a ClusterRole
A ClusterRole:
- Has **no namespace**    
- Uses the same rule structure as a Role    

### Example: Cluster Administrator Role
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-administrator
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["list", "get", "create", "delete"]
```

This role allows:
- Listing nodes    
- Viewing node details    
- Creating and deleting nodes
---
# Binding a ClusterRole
ClusterRoles **do nothing on their own**.  
They must be bound to users or groups.
There are **two ways to bind** a ClusterRole.

---
## 1. ClusterRoleBinding (Cluster-Wide Access)
### What it does
- Grants permissions **across the entire cluster**    
- Applies to **all namespaces**    
### Example
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-role-binding
subjects:
- kind: User
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-administrator
  apiGroup: rbac.authorization.k8s.io
```
Result:
- `cluster-admin` can manage nodes **cluster-wide**    

---
## 2. RoleBinding (Namespace-Limited Access)
This is the **most misunderstood concept**.
You can bind a **ClusterRole using a RoleBinding**.
### What happens?
- Permissions apply **only inside that namespace**    
- But rules still come from ClusterRole
### Example
```yaml
kind: RoleBinding
metadata:
  name: dev-view-binding
  namespace: dev
roleRef:
  kind: ClusterRole
  name: view
subjects:
- kind: User
  name: dev-user
```
Result:
- `dev-user` can view resources    
- Only inside `dev` namespace
---
# Important Rule (Exam Favorite)

|Binding Type|Scope|
|---|---|
|Role + RoleBinding|One namespace|
|ClusterRole + RoleBinding|One namespace|
|ClusterRole + ClusterRoleBinding|Entire cluster|

---
# Why Use ClusterRoles for Namespaced Resources?
Reasons:
1. Avoid duplication    
2. Consistent permissions across namespaces    
3. Easier administration
Instead of:
- Creating the same Role in 10 namespaces
You:
- Create one ClusterRole    
- Bind it selectively    

---
# Default ClusterRoles in Kubernetes
Kubernetes ships with **predefined ClusterRoles**.
Common ones:

|ClusterRole|Purpose|
|---|---|
|cluster-admin|Full access to everything|
|admin|Namespace admin|
|edit|Modify most objects|
|view|Read-only access|

Example:
`kubectl get clusterroles`
These are often used with:
- RoleBindings for namespace access    
- ClusterRoleBindings for global access    

---
# Security Best Practices
- Never give `cluster-admin` casually    
- Prefer RoleBinding over ClusterRoleBinding    
- Scope permissions to namespaces when possible    
- Follow least privilege principle    

---
# Common Mistakes (Very Important)
- Using Role to manage nodes    
- Expecting Role to work across namespaces    
- Using ClusterRoleBinding when RoleBinding was enough    
- Forgetting ClusterRoles are cluster-wide by default    

---
# Real-World Use Cases

|Scenario|Correct Choice|
|---|---|
|Developer access to pods in dev|Role + RoleBinding|
|Read-only access across cluster|ClusterRole + ClusterRoleBinding|
|Admin access to nodes|ClusterRole|
|Same permissions in all namespaces|ClusterRole|
|CI tool managing deployments everywhere|ClusterRoleBinding|

---
# Quick Mental Model
```scss
Role           → namespace only
ClusterRole    → cluster-wide rules

RoleBinding        → namespace scope
ClusterRoleBinding → cluster scope
```


---
# Final Summary
- ClusterRoles manage cluster-scoped resources    
- They can also manage namespaced resources across namespaces    
- Binding type determines actual scope    
- ClusterRoles are essential for node, PV, and admin access    
- Mastering this is critical for KCNA and CKA
---
