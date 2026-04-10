# Authorization

## 1. Authentication vs Authorization (Exam Foundation)
Before authorization, always remember the flow:
1. **Authentication** – Who are you?    
    - Certificates        
    - Tokens        
    - ServiceAccounts        
2. **Authorization** – What are you allowed to do?    
3. **Admission Control** – Should this request be allowed to proceed?    
This lesson is strictly about **step 2: Authorization**.

---
## 2. What Authorization Means in Kubernetes
Authorization answers questions like:
- Can this user list pods?    
- Can this service delete nodes?    
- Can this application create deployments in a namespace?    
Example:
An **admin user** can:
- List pods    
- List nodes    
- Delete nodes    

A **developer** might:
- Create pods    
- Create deployments    
- Not touch nodes or cluster-wide resources    

A **CI/CD bot (Jenkins)** might:
- Deploy applications    
- Read services    
- Not delete anything    
Authorization ensures **least privilege access**.

---
## 3. Where Authorization Happens
All requests go through the **Kubernetes API Server**.
Examples:
`kubectl get pods `
`kubectl delete node worker-2`
Even internal components (kubelet, scheduler, controller-manager) talk to the API server and are **authorized**.

---
## 4. Kubernetes Authorization Modes (Very Important)
Kubernetes supports **multiple authorization mechanisms**, configured on the API server using:
`--authorization-mode=`
### Supported Authorization Modes
1. Node Authorization    
2. ABAC (Attribute-Based Access Control)    
3. RBAC (Role-Based Access Control)    
4. Webhook Authorization    
5. AlwaysAllow    
6. AlwaysDeny    
For **CKA and KCNA**, you must clearly understand **Node, ABAC, RBAC, Webhook**, and how **multiple modes work together**.
---
## 5. Node Authorization
### Purpose
Designed **only for kubelets (nodes)**.
Kubelets must:
- Read pods scheduled to them    
- Update pod status    
- Read services and endpoints    
- Report node status    
### How It Works
- Kubelets authenticate using **certificates**    
- Their identity:    
    - Username: `system:node:<node-name>`        
    - Group: `system:nodes`        
- The **Node Authorizer**:    
    - Verifies the certificate        
    - Grants permissions only for:        
        - Pods bound to that node            
        - Node status updates            
        - Services/endpoints read access            
### Key Points for Exams
- Node Authorizer is **not for humans**    
- Automatically used for kubelets    
- Very restrictive and safe    
- Prevents nodes from accessing other nodes’ data    

---
## 6. ABAC (Attribute-Based Access Control)
### What Is ABAC?
ABAC uses **JSON policy files** to define permissions.
Example policy:
```json
{
  "kind": "Policy",
  "spec": {
    "user": "dev-user",
    "namespace": "*",
    "resource": "pods",
    "apiGroup": "*"
  }
}
```
### Characteristics
- Permissions are tied to:    
    - User        
    - Group        
    - Namespace        
    - Resource        
    - API group        
- Policies are **static files**    
- Requires **API server restart** on changes    
### Drawbacks (Exam Favorite)
- Not dynamic    
- Hard to manage    
- Poor scalability    
- Rarely used in production today    
### Exam Tip
If asked:
> “Which authorization method requires API server restart?”

Answer: **ABAC**

---
## 7. RBAC (Role-Based Access Control)
### This Is the MOST IMPORTANT Authorization Method
RBAC is:
- Default in modern clusters    
- Required knowledge for **CKA**    
- Strongly tested in exams    
### Core RBAC Objects

|Object|Purpose|
|---|---|
|Role|Permissions inside a namespace|
|ClusterRole|Permissions across the cluster|
|RoleBinding|Assign Role to user/group/serviceaccount|
|ClusterRoleBinding|Assign ClusterRole|
### Example Concept
- Create a `developer` Role:    
    - Can create pods        
    - Can list services        
- Bind Role to user `dev-user`    
### Key Benefits
- Easy to manage    
- Dynamic (no restart)    
- Supports namespaces    
- Fine-grained permissions    

### Exam Tip
RBAC answers questions like:
- Who can do what?    
- Where (namespace or cluster)?    
- On which resource?    

---
## 8. Webhook Authorization
### What Is Webhook Authorization?
Delegates authorization decisions to an **external service**.
Example:
- Open Policy Agent (OPA)    
- Custom authorization server    
### How It Works
1. API server receives request    
2. Sends request details to webhook    
3. Webhook responds:    
    - Allow        
    - Deny        
### Use Cases
- Enterprise policy engines    
- Complex compliance rules    
- External governance systems    
### Exam Relevance
- Mostly conceptual for KCNA    
- Rarely configured manually in CKA labs

---
## 9. AlwaysAllow and AlwaysDeny
### AlwaysAllow
- Grants **all requests**    
- No authorization checks    
### AlwaysDeny
- Denies **all requests**    
#### Default Behavior
If no `--authorization-mode` is specified:
- **AlwaysAllow** is used    
#### Exam Tip
Never use AlwaysAllow in production.

---
## 10. Multiple Authorization Modes (Critical Concept)
You can enable **multiple authorization modes**:
`--authorization-mode=Node,RBAC,Webhook`
### How Kubernetes Evaluates Requests
1. Request goes to **first authorizer**    
2. If it **denies**, move to next    
3. If **any authorizer allows**, request is approved    
4. Evaluation stops at first success    
### Example Flow
- Node Authorizer → Deny    
- RBAC → Allow    
- Final result → Allowed    
### Exam Tip
Authorization is **OR-based**, not AND-based.

---
## 11. Authorization and Namespaces
Namespaces help **scope permissions**.
Example:
- Developer has access only to:    
    - `dev` namespace        
- Cannot:    
    - Access `kube-system`        
    - Manage nodes       
RBAC uses namespaces extensively.

---
## 12. Common Exam Scenarios
If you see this error:
`Error from server (Forbidden)`
It means:
- Authentication succeeded    
- Authorization failed    

Troubleshooting steps:
1. Check Role / ClusterRole    
2. Check RoleBinding / ClusterRoleBinding    
3. Check namespace    
4. Check authorization mode    

---

## 13. Summary Table (Quick Revision)

|Authorization Method|Used For|Restart Needed|Exam Importance|
|---|---|---|---|
|Node|Kubelets|No|High|
|ABAC|Legacy|Yes|Medium|
|RBAC|Users & apps|No|Very High|
|Webhook|External policy|No|Medium|
|AlwaysAllow|Testing only|No|Low|
|AlwaysDeny|Blocking|No|Low|

---
## 14. One-Line Exam Memory Aids
- **Node** → kubelets only    
- **ABAC** → JSON + restart    
- **RBAC** → Roles + Bindings    
- **Webhook** → external decision    
- **Multiple modes** → first allow wins    

---
