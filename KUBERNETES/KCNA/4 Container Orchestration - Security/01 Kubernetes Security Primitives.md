# 01 Kubernetes Security Primitives

# Container Orchestration Security
## Kubernetes Security Primitives (KCNA + CKA)
Kubernetes security is **layered**. No single feature makes a cluster secure; instead, multiple security primitives work together. These can be grouped into:
1. Securing the underlying hosts    
2. Securing the Kubernetes control plane    
3. Authentication (Who can access?)    
4. Authorization (What can they do?)    
5. Secure communication (TLS everywhere)    
6. Network isolation (Network Policies)    

---
## 1. Securing the Underlying Hosts
Before Kubernetes even starts, **the host machines must be secured**. Kubernetes **does not protect you** if the node itself is compromised.
### Why this matters
If an attacker gains root access to a node:
- They can access container filesystems    
- They can steal Kubernetes credentials    
- They can control workloads running on that node    
- They may compromise the entire cluster    
### Host-level security best practices
#### Disable root login
- Prevent direct root login over SSH    
- Use a normal user + `sudo`    
#### Disable password-based authentication
- Passwords are vulnerable to brute-force attacks    
- Even strong passwords can be leaked    
#### Enforce SSH key-based authentication
- Use public/private key pairs    
- Keys are significantly harder to brute-force    
- Supports key rotation and revocation    
#### Additional host security measures
- Regular OS patching    
- Firewall rules (iptables, firewalld)    
- Minimal OS installations    
- Disable unused services    
- File integrity monitoring    
- Node hardening (CIS benchmarks)    

**Exam focus**
- KCNA: Understand _why_ host security is critical    
- CKA: Be aware that Kubernetes assumes secure hosts    

---
## 2. Kubernetes-Specific Security Measures
Once hosts are secured, focus shifts to Kubernetes itself.
### Central component: kube-apiserver
The **kube-apiserver** is:
- The front door of the cluster    
- The only component that talks to etcd    
- The component used by:    
    - `kubectl`        
    - Controllers        
    - Scheduler        
    - External tools        
If the API server is compromised, **the cluster is compromised**.
### Two core security questions Kubernetes must answer
1. **Who can access the cluster?**  
    → Authentication    
2. **What are they allowed to do?**  
    → Authorization
These are enforced at the API server.

---
## 3. Authentication (Who Can Access?)
Authentication verifies the **identity** of a user or component.
### Authentication methods in Kubernetes
#### 1. Static username and password files
- Simple but not recommended for production    
- Hard to rotate credentials    
- Mostly legacy or learning use    
#### 2. Tokens
- Bearer tokens    
- Common for automation and service access    
- Can be revoked or rotated    
#### 3. Certificates
- X.509 client certificates    
- Strong and secure    
- Common for admin access and component-to-component auth    
#### 4. External authentication providers
- LDAP    
- OAuth    
- OpenID Connect (OIDC)    
- Used in enterprise environments    
#### 5. Service Accounts (Machine-to-Machine)
- Used by Pods to talk to the API server    
- Automatically created in namespaces    
- Mounted into Pods as tokens    
- Essential for controllers and workloads    
### Key points to remember
- Authentication only answers **“Who are you?”**    
- It does NOT decide permissions    
- Multiple authentication methods can be enabled simultaneously    

**Exam focus**
- KCNA: Understand available authentication mechanisms    
- CKA: Understand service accounts and certificates conceptually    

---
## 4. Authorization (What Can They Do?)
Once authenticated, Kubernetes decides **what actions are allowed**.
### Role-Based Access Control (RBAC)
RBAC is the **primary and default authorization mechanism**.
#### Core RBAC objects
- **Role**    
    - Permissions within a namespace        
- **ClusterRole**    
    - Permissions across the entire cluster        
- **RoleBinding**    
    - Binds a Role to a user/group/service account        
- **ClusterRoleBinding**    
    - Binds a ClusterRole cluster-wide        

#### RBAC example logic
- A Role defines permissions like:    
    - get, list, create Pods        
- A RoleBinding assigns those permissions to:    
    - A user        
    - A group        
    - A service account        
### Other authorization methods
#### Attribute-Based Access Control (ABAC)
- Uses policies based on attributes    
- Harder to manage    
- Mostly deprecated    

#### Webhook authorization
- Delegates authorization to an external service    
- Useful for custom enterprise logic    

### Key principle
- Follow **least privilege**    
- Grant only the permissions that are required    

**Exam focus**
- KCNA: Understand RBAC conceptually    
- CKA: Must understand RBAC objects and relationships    

---
## 5. Secure Communication Within the Cluster
Kubernetes enforces **secure communication between all core components**.
### Why encryption is required
- Prevents man-in-the-middle attacks    
- Protects secrets and credentials    
- Ensures integrity of cluster operations    
### Components communicating securely
- kube-apiserver ↔ etcd    
- kube-apiserver ↔ kubelet    
- kube-controller-manager ↔ kube-apiserver    
- kube-scheduler ↔ kube-apiserver    
- Nodes ↔ control plane   
All of these communications use **TLS encryption**.

---
## 6. TLS Encryption in Kubernetes
TLS is used everywhere in a production cluster.
### What TLS protects
- Confidentiality (data is encrypted)    
- Integrity (data is not altered)    
- Authentication (identity verification)    
### Components secured with TLS
- kube-apiserver    
- etcd cluster    
- kubelet    
- controller-manager    
- scheduler    
### Certificates
- Kubernetes uses X.509 certificates    
- Certificates have:    
    - Subject        
    - Expiry        
    - Key usage        
- Certificates must be rotated periodically    

Kubernetes documentation has an entire section dedicated to:
- Generating certificates    
- Configuring TLS    
- Managing certificate rotation    

**Exam focus**
- KCNA: Know TLS is used everywhere    
- CKA: Understand certificate usage conceptually (no deep PKI ops required)    

---

## 7. Network Policies
### Default behavior
- All Pods can communicate with all other Pods    
- No network isolation by default    

This is **not secure** for production workloads.
### What Network Policies do
- Control **Pod-to-Pod** communication    
- Restrict traffic based on:    
    - Namespace        
    - Pod labels        
    - Ports        
    - Protocols        
    - Ingress and egress rules        

### Important notes
- Network Policies are enforced by the **CNI plugin**    
- If the CNI does not support them, policies do nothing    
- Policies are **deny-by-default once applied**    

### Security benefit
- Limits blast radius    
- Prevents lateral movement    
- Enforces zero-trust networking    

**Exam focus**
- KCNA: Understand purpose and concept    
- CKA: Understand behavior and enforcement    

---
## 8. Summary: Kubernetes Security Primitives
Kubernetes security is built on multiple layers:
1. Secure the hosts first    
2. Protect the kube-apiserver    
3. Authenticate every user and component    
4. Authorize actions using RBAC    
5. Encrypt all internal communication using TLS    
6. Restrict pod networking using Network Policies    

This layered approach ensures:
- Defense in depth    
- Reduced attack surface    
- Secure multi-tenant environments
---