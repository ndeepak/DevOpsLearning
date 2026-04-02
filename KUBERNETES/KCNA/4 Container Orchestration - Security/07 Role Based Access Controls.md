# Kubernetes RBAC (Role-Based Access Control)
RBAC is the **primary authorization mechanism** used in Kubernetes today.  
It answers the question:
> “What is this user / service account allowed to do in the cluster?”

RBAC works by **defining permissions (Roles)** and **assigning them to subjects (users, groups, service accounts)** using **Bindings**.

---
## Big Picture: How RBAC Works
RBAC is based on **four core objects**:
1. **Role** – Defines permissions within a namespace    
2. **ClusterRole** – Defines permissions cluster-wide    
3. **RoleBinding** – Assigns a Role to a subject within a namespace    
4. **ClusterRoleBinding** – Assigns a ClusterRole cluster-wide    
RBAC does **not grant permissions by default**. Everything is denied unless explicitly allowed.

---
## Roles (Namespace-scoped permissions)
### What is a Role?
A **Role** defines **what actions are allowed** on **which resources** inside **one namespace**.
Key properties:
- Namespace-scoped    
- Cannot grant access outside its namespace    
- Used for application users, developers, namespace admins    

---
### Role YAML Breakdown
Example Role: `developer`
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list", "get", "create", "update", "delete"]
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["create"]
```
### Explanation of Fields
**apiGroups**
- `""` → Core API group (pods, services, configmaps, secrets)    
- `apps` → deployments, replicasets    
- `batch` → jobs, cronjobs    
**resources**
- Kubernetes objects (pods, services, deployments)
**verbs**
- Allowed actions:    
    - get        
    - list        
    - watch        
    - create        
    - update        
    - patch        
    - delete        
---
### Important Exam Note (CKA & KCNA)
- Pods, Services, ConfigMaps → apiGroups: `""`    
- Deployments, ReplicaSets → apiGroups: `apps`    
This is a very common exam trap.

---
## RoleBindings (Assigning Roles to Users)
### What is a RoleBinding?
A **RoleBinding connects a Role to a subject** (user, group, or service account) **inside a namespace**.
Without a binding, a Role does nothing.

---
### RoleBinding YAML Breakdown
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: devuser-developer-binding
subjects:
- kind: User
  name: dev-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
```
### Key Sections Explained
**subjects**
- Who gets the permissions    
- Types:    
    - User        
    - Group        
    - ServiceAccount        
**roleRef**
- Which role is being assigned    
- Must match Role name exactly    

---
### Namespace Behavior (Very Important)
- Role + RoleBinding → **namespace-scoped**    
- Binding must exist in the **same namespace as the Role**    
- Permissions do not cross namespaces    

---
## Viewing RBAC Objects
### List Roles
`kubectl get roles`
### Describe a Role
`kubectl describe role developer`
### List RoleBindings
`kubectl get rolebindings`
### Describe a RoleBinding
`kubectl describe rolebinding devuser-developer-binding`

---
## Verifying Permissions (Critical for Exams)
### kubectl auth can-i
This command checks **authorization**, not authentication.
```bash
kubectl auth can-i create pods
kubectl auth can-i delete nodes
```
Expected output:
- `yes`    
- `no`    
---
### Check Permissions for Another User
`kubectl auth can-i create pods --as dev-user`
With namespace:
`kubectl auth can-i create pods --as dev-user -n default`
This is extremely useful in real clusters and exams.

---
## Restricting Access to Specific Resources
Sometimes users should access **only specific resource instances**, not all.
### Example: Only specific pods
```yaml
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "update"]
  resourceNames:
    - blue
    - orange
```
This means:
- User cannot touch any pod except `blue` and `orange`
---
## Role vs ClusterRole (Must Know)

|Feature|Role|ClusterRole|
|---|---|---|
|Scope|Namespace|Cluster-wide|
|Used for|App users|Admins, nodes, controllers|
|Can access nodes|No|Yes|
|Can be bound to namespace|Yes|Yes|
|Can be bound cluster-wide|No|Yes|

Important:
- A **ClusterRole can be bound using a RoleBinding**, limiting it to a namespace    
- A **Role cannot be used cluster-wide**    

---
## Common Built-in Roles
Kubernetes ships with predefined ClusterRoles:
- `cluster-admin` – full access    
- `admin` – namespace admin    
- `edit` – modify most objects    
- `view` – read-only access    

Example binding:
```bash
kubectl create rolebinding dev-view \
  --clusterrole=view \
  --user=dev-user \
  --namespace=default
```
---
## RBAC Authorization Flow (Exam Concept)
1. User authenticates (certificate, token, kubeconfig)    
2. API Server receives request    
3. RBAC authorizer checks:    
    - Who is the user?        
    - What verb?        
    - Which resource?        
    - Which namespace?        
4. If any RoleBinding or ClusterRoleBinding allows it → access granted    
5. Otherwise → forbidden    

---
## Common Mistakes (Exam Traps)
- Using `Role` instead of `ClusterRole` for nodes    
- Forgetting apiGroups field    
- Creating Role but forgetting RoleBinding    
- Binding Role in wrong namespace    
- Expecting Role permissions to apply cluster-wide    

---
## Quick Exam Checklist
- Pods, Services → apiGroups: `""`    
- Deployments → apiGroups: `apps`    
- Role = namespace    
- ClusterRole = cluster-wide    
- RoleBinding connects subject to Role    
- Use `kubectl auth can-i` to debug    
- Permissions are deny by default
---
## Final Summary
RBAC is Kubernetes’ primary authorization system.  
It enforces **least privilege**, ensures **secure multi-tenancy**, and is heavily tested in **KCNA and CKA exams**.
You should be comfortable:
- Writing Role and RoleBinding YAML    
- Understanding apiGroups    
- Debugging permissions    
- Knowing when to use Role vs ClusterRole

---