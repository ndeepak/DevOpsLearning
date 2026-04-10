# Service Accounts
# Kubernetes Service Accounts (KCNA + CKA)

## 1. What Is a Service Account?
A **Service Account (SA)** is an identity used by **applications and system components** running **inside a Kubernetes cluster** to authenticate with the Kubernetes API server.
### Two account types in Kubernetes

|Account Type|Used By|Purpose|
|---|---|---|
|User Account|Humans (admins, developers)|kubectl, dashboards|
|Service Account|Machines / applications|Pods, controllers, CI/CD, monitoring|
**Key rule:**  
Service Accounts are for **machine-to-machine authentication**, not humans.

---
## 2. Why Service Accounts Exist
Applications running inside pods may need to:
- List pods
- Watch services    
- Read ConfigMaps    
- Update resources (CI/CD tools)    
They must do this **securely**, without embedding admin credentials.

Service Accounts provide:
- Identity    
- Authentication (token-based)    
- Authorization (via RBAC)    

---
## 3. Default Service Account
Every namespace automatically has a service account named:
 `default` 
If a pod **does not specify** a service account:
- Kubernetes assigns the **default service account**    
- A token is automatically mounted into the pod    

`kubectl get serviceaccounts`
Example output:
```scss
NAME       SECRETS   AGE
default    1         218d
```

---
## 4. Creating a Service Account
`kubectl create serviceaccount dashboard-sa`
This creates:
- A ServiceAccount object    
- (Pre-1.24) A secret with a token    
- (1.24+) No secret by default    

Verify:
`kubectl get serviceaccounts`

```scss
NAME           SECRETS   AGE
default        1         218d
dashboard-sa   1         4d   (pre-1.24)
```

---
## 5. Service Account Token (Authentication)
### Purpose of the Token
The token is a **JWT bearer token** used to authenticate to the API server.

Example API call:
```bash
curl https://<api-server>:6443/api \
  --header "Authorization: Bearer <token>"
```

---

## 6. Automatic Token Mounting in Pods
When a pod runs:
- Kubernetes **automatically mounts** the service account token
- The token is mounted as a **read-only volume**
Default mount path:
`/var/run/secrets/kubernetes.io/serviceaccount`

Files inside:
```text
ca.crt
namespace
token
```

Verify inside pod:
`kubectl exec -it pod-name -- ls /var/run/secrets/kubernetes.io/serviceaccount`

---
## 7. Using a Custom Service Account in a Pod
By default, pods use the `default` service account.
To use a custom one:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-dashboard
spec:
  serviceAccountName: dashboard-sa
  containers:
  - name: app
    image: my-dashboard
```
Important rules:
- Service account **cannot be changed after pod creation**    
- Pod must be **deleted and recreated**    
- Deployments require a rollout
---
## 8. Disabling Automatic Token Mounting
If your application **does not need** API access:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: no-api-access
spec:
  automountServiceAccountToken: false
  containers:
  - name: app
    image: nginx
```

Security best practice:
- Disable token mounting when not required
---
## 9. Service Accounts and RBAC
Service accounts **have no permissions by default**.
Permissions are granted via:
- Role + RoleBinding    
- ClusterRole + ClusterRoleBinding
Example:
```yaml
subjects:
- kind: ServiceAccount
  name: dashboard-sa
  namespace: default
```
Without RBAC:
- Token authentication succeeds    
- Authorization fails (403 Forbidden)
---
## 10. Service Account Token Evolution (Very Important for Exams)

---
## Kubernetes < 1.22 (Legacy Behavior)
- Every service account:    
    - Automatically created a **secret**        
    - Token was **non-expiring**        
    - Token stored in etcd        
    - Mounted into pods        
Problems:
- Tokens never expired
- Security risk    
- Difficult rotation    
- Scalability issues    

---
## Kubernetes 1.22 – TokenRequest API (KEP-1205)
Introduced:
- **Bound Service Account Tokens**    

Features:
- Time-bound (expires)    
- Audience-bound    
- Pod-bound    
- Automatically rotated    
- Mounted via **projected volumes**    

Example projected volume:
```yaml
projected:
  sources:
  - serviceAccountToken:
      expirationSeconds: 3600
      path: token
```
This is now the **recommended approach**.

---
## Kubernetes 1.24 – No Auto-Created Secrets (KEP-2799)
Major change:
- Service accounts **no longer auto-create secrets**    
- Tokens are created **on demand**    

Create token manually:
`kubectl create token dashboard-sa`

Output:
`<JWT token with expiry>`

Token properties:
- Short-lived (default ~1 hour)    
- Secure    
- Recommended    
---
## 11. Creating a Non-Expiring Token (Not Recommended)
If absolutely required:
```yaml
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
  name: dashboard-sa-token
  annotations:
    kubernetes.io/service-account.name: dashboard-sa
```
Warnings:
- Static token    
- Security risk    
- Not recommended for production    
---
## 12. kubectl proxy vs Service Account

|Feature|kubectl proxy|Service Account|
|---|---|---|
|Used by|Humans|Pods|
|Auth source|kubeconfig|JWT token|
|Scope|Local|Cluster|
|Use case|Debugging|Applications|

---
## 13. Common Exam Traps
- Default service account has **no permissions**    
- Tokens ≠ permissions    
- Service accounts are **namespace-scoped**    
- Pods always authenticate as their service account   
- Tokens are mounted automatically unless disabled    
- Kubernetes 1.24 does NOT auto-create secrets    

---
## 14. Real-World Use Cases

|Application|Needs Service Account|
|---|---|
|Prometheus|Yes|
|Jenkins|Yes|
|Ingress Controller|Yes|
|CoreDNS|Yes|
|Application reading ConfigMaps|Yes|
|Static website|No|

## 15. One-Page Mental Model
```scss
Pod
 └── Service Account
       └── Token (JWT)
             └── Authentication
                   └── RBAC Authorization
```
---
## Final Summary
- Service Accounts are **identities for pods**    
- They authenticate using **JWT tokens**    
- Authorization is controlled via **RBAC**    
- Default SA exists in every namespace    
- Token handling changed significantly in 1.22 and 1.24    
- TokenRequest API is now standard    
- Static tokens should be avoided    

---