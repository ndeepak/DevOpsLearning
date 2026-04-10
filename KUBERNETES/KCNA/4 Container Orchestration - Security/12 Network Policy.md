# Network  Policy
# Kubernetes Network Policies (KCNA)
## What Is a Network Policy?
A **NetworkPolicy** is a Kubernetes resource that **controls network traffic between pods**.
It defines:
- **Who** can talk to a pod    
- **On which ports**    
- **In which direction** (ingress or egress)    
Network policies are a **core part of container orchestration security**.

---
## Basic Traffic Flow Example
Consider a simple 3-tier application:
### Components
- **Web server** – serves the frontend    
- **API server** – handles business logic    
- **Database server** – stores data    
### Traffic Flow
1. User → Web server on **port 80**    
2. Web server → API server on **port 5000**    
3. API server → Database server on **port 3306**    

---
## Ingress vs Egress Traffic
### Ingress
- Traffic **coming into** a pod    
- Example: User request reaching the web server    

### Egress
- Traffic **leaving** a pod    
- Example: API server querying the database    
### Important Note
When defining rules:
- Only the **initial traffic direction** is evaluated    
- **Response traffic is automatically allowed**    
This is commonly tested in exams.

---
## Traffic Requirements per Component
### Web Server
- Ingress: Allow TCP **80**    
- Egress: Allow TCP **5000** to API server    
### API Server
- Ingress: Allow TCP **5000**    
- Egress: Allow TCP **3306** to database    
### Database Server
- Ingress: Allow TCP **3306**    
- Egress: No restriction (by default)    

---
## Default Kubernetes Networking Behavior
By default, Kubernetes follows an **“all-allow” model**:
- All pods can communicate with each other    
- No traffic restrictions exist    
- Pods share a flat network across nodes    
- Communication works using:    
    - Pod IPs        
    - Pod names        
    - Services        
This default behavior is **not secure for production**.

---
## Why Network Policies Are Needed
Without network policies:
- Any pod can access any other pod    
- A compromised pod can reach sensitive services (like databases)    
With network policies:
- Traffic is **explicitly allowed**    
- Everything else is **denied by default** (once a policy applies)    

---
## What a Network Policy Does
A network policy:
- Applies to **selected pods**    
- Uses **labels and selectors**    
- Controls **ingress, egress, or both**    
- Blocks all traffic **not explicitly allowed**    
Important:
> A network policy affects **only the pods it selects**

---
## Example Scenario: Securing a Database Pod
Goal:
- Only the **API pod** should access the **database pod**    
- Web pod must NOT access the database directly    
---
## Labeling the Database Pod
```yaml
podSelector:
  matchLabels:
    role: db
```
This selects all pods with the label `role=db`.

---
## Allowing Traffic from API Pod Only
```yaml
policyTypes:
- Ingress
ingress:
- from:
  - podSelector:
      matchLabels:
        name: api-pod
  ports:
  - protocol: TCP
    port: 3306
```
This means:
- Only pods labeled `name=api-pod`    
- Can connect on TCP port **3306**    

---
## Complete Network Policy Example
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              name: api-pod
      ports:
        - protocol: TCP
          port: 3306
```
### What This Policy Does
- Applies to database pods (`role=db`)    
- Allows ingress only from API pods    
- Blocks all other ingress traffic    
- Does NOT restrict egress traffic    

---
## Ingress vs Egress Policies

|Type|Controls|
|---|---|
|Ingress|Incoming traffic|
|Egress|Outgoing traffic|
|Both|Full traffic control|
If `egress` is not defined:
- All outgoing traffic is allowed

---
## Network Policy Enforcement (Very Important)
Network policies **require a compatible CNI plugin**.
### Supported CNIs
- Calico    
- Kube-router    
- Weave Net    
- Romana
### Not Supported
- Flannel
---
## Critical Warning
Even if:
- Network policies are created correctly    
- YAML syntax is valid    
If the CNI does **not support network policies**:
- Policies are **not enforced**    
- Kubernetes shows **no error**    
This is a frequent exam trap.
---
## KCNA Exam Tips
- Network policies are **namespace-scoped**
- They use **labels**, not names
- Policies are **deny-by-default once applied**
- Response traffic is automatically allowed
- They control **pod-to-pod traffic**, not users
- They are different from:
    - RBAC (API access)
    - Security Contexts (container privileges)
---
## Common Misconceptions

|Misconception|Reality|
|---|---|
|Network policies secure nodes|They secure pods|
|Policies apply cluster-wide|Namespace-scoped|
|Policies work without CNI support|They do not|
|Policies block response traffic|Response is allowed|

---
## One-Line Summary
A **NetworkPolicy** defines which pods can communicate with each other and on which ports, providing network-level isolation inside a Kubernetes cluster.