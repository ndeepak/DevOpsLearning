# Authentication

## Authentication in Kubernetes (KCNA)
Authentication in Kubernetes answers one fundamental question:
**“Who is making this request?”** 

Before Kubernetes allows _any_ operation—viewing pods, creating deployments, or modifying cluster settings—it must first **verify the identity** of the requester. This process is handled centrally and consistently by the **kube-apiserver**.

---
## 1. Who Accesses a Kubernetes Cluster?
In a real-world Kubernetes environment, multiple types of users and systems interact with the cluster:
### Human users
- **Administrators**    
    - Perform cluster setup and maintenance        
    - Configure networking, storage, and security        
- **Developers**    
    - Deploy applications        
    - Debug workloads        
    - View logs and resources 
### Automated entities
- **Bots and third-party integrations**    
    - CI/CD pipelines        
    - Monitoring tools        
    - External automation systems        
### End users
- Typically **do not** interact with Kubernetes directly    
- Their authentication is handled **inside the application**, not by Kubernetes    

---
## 2. Where Authentication Happens
### kube-apiserver is the gatekeeper
All access to the Kubernetes cluster goes through the **kube-apiserver**.
- `kubectl` commands    
- Direct REST API calls (e.g., using curl)    
- Internal cluster components    
- External automation tools    

Every request must pass through the API server, which performs authentication **before** authorization or admission checks.
Example entry points:
`kubectl get pods`
`curl https://kube-server-ip:6443/`

---
## 3. Kubernetes Authentication Model
### Kubernetes does NOT manage human users internally
This is a very important KCNA concept.
- Kubernetes **does not have**:    
    - User objects        
    - Password databases        
    - Built-in user lifecycle management        

Instead:
- Human user authentication is **delegated** to:    
    - Static files        
    - Certificates        
    - External identity providers (LDAP, Kerberos, OIDC)        
### Kubernetes DOES manage service accounts
- Service accounts are Kubernetes API objects    
- Used for **machine-to-machine** communication    
- Managed entirely by Kubernetes    
- Discussed separately in the course    

---
## 4. Supported Authentication Methods
The kube-apiserver supports **multiple authentication mechanisms at the same time**.
Common methods include:
1. Static password files    
2. Static token files    
3. Certificate-based authentication    
4. External authentication providers (LDAP, Kerberos, OIDC)    
5. Service accounts (for workloads)    

In this lesson, the focus is on **static password and token file authentication**, which are the simplest to understand.

---
## 5. Static Password File Authentication
### What it is
- A **CSV file** containing user credentials    
- Stored locally on the control plane node    
- Referenced when starting the kube-apiserver    
### CSV file format
The file contains **three mandatory columns**:
`password,username,user-id`

Example: user-details.csv
```scss
password123,user1,u0001
password123,user2,u0002
password123,user3,u0003
password123,user4,u0004
password123,user5,u0005
```
**kube-apiserver  --basic-auth-file=user-details.csv**
### Optional fourth column: groups
`password,username,user-id,group`

Example:
```scss
password123,user1,u0001,group1
password123,user2,u0002,group2
```

Groups are important later for **RBAC authorization**.

---
## 6. Configuring kube-apiserver for Password Authentication
### Using direct kube-apiserver startup flags
Add the following flag:
`--basic-auth-file=user-details.csv`

Example kube-apiserver startup snippet:
```scss
ExecStart=/usr/local/bin/kube-apiserver \
  --advertise-address=${INTERNAL_IP} \
  --authorization-mode=Node,RBAC \
  --bind-address=0.0.0.0 \
  --etcd-servers=https://127.0.0.1:2379 \
  --basic-auth-file=user-details.csv
```
After updating this:
- The kube-apiserver **must be restarted**
---
## 7. kubeadm-Based Clusters
In kubeadm setups:
- kube-apiserver runs as a **static Pod**    
- Configuration is stored in a Pod manifest (usually under `/etc/kubernetes/manifests/`)
### Example kube-apiserver Pod configuration
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - name: kube-apiserver
    image: k8s.gcr.io/kube-apiserver-amd64:v1.11.3
    command:
    - kube-apiserver
    - --authorization-mode=Node,RBAC
    - --advertise-address=172.17.0.107
    - --allow-privileged=true
    - --enable-admission-plugins=NodeRestriction
    - --enable-bootstrap-token-auth=true
```

To use password authentication:
- Add `--basic-auth-file`    
- Ensure the CSV file is **mounted into the Pod**    
- kubeadm automatically restarts the API server when the file changes
---
## 8. Using Password Authentication
Once configured, users can authenticate using **basic authentication**.
### Example API request using curl
```bash
curl -v -k https://master-node-ip:6443/api/v1/pods \
-u "user1:password123"
```
### Successful response
The API server returns the requested resource, such as:
- PodList    
- Metadata    
- Pod details    

This confirms:
- Authentication succeeded    
- Authorization was also allowed (RBAC permitting)

---
## 9. Static Token File Authentication
### What it is
- Similar to password authentication    
- Uses **tokens instead of passwords**    
- Tokens are sent as **Bearer tokens**    
### Token file format
`token,username,user-id,group`

Example:
```
KpjCvBI7rCFAHYPKByTlzRb7gulcUc4B,user10,u0010,group1
rJjncHmvtXHc6M1WQddhtvNyhgTdxSC,user11,u0011,group1
mjpOFEiFokLgtoikaRNTt59ePtczZSq,user12,u0012,group2
PG411Xhs7qjwWkmBkvG7g9lOyUqZj,user13,u0013,group2
```

---

## 10. Enabling Token Authentication
Start kube-apiserver with:
`--token-auth-file=user-details.csv`

As with password files:
- kube-apiserver must have access to the file    
- kubeadm requires proper volume mounting    

---

## 11. Using Token Authentication
### API request with Bearer token
```bash
curl -v -k https://master-node-ip:6443/api/v1/pods \
--header "Authorization: Bearer KpjCvBI7rCFAHYPKByTlzRb7gulcUc4B"
```

How this works:
- Token is sent in HTTP header    
- kube-apiserver validates token    
- Maps token to user identity    
- Authorization checks follow    

---
## 12. Security Warnings (Very Important for Exam)
### Why static authentication is discouraged
Static password and token files:
- Store credentials in **plain text**    
- Are difficult to rotate securely    
- Require API server restarts    
- Are vulnerable if node access is compromised    

### Acceptable use cases
- Learning environments    
- Lab setups    
- Testing scenarios    

### Production recommendations
- Certificate-based authentication    
- Integration with external identity providers    
- Short-lived credentials    
- Centralized identity management    

---
## 13. Final kubeadm Consideration
When using kubeadm:
- Authentication files must be:    
    - Mounted into the kube-apiserver Pod        
    - Correctly referenced by flags        
- Without volume mounts, authentication **will fail**    
- RBAC must be configured separately for permissions    

---
## 14. Key KCNA Exam Takeaways
- kube-apiserver authenticates **all requests**    
- Kubernetes does not manage human users internally    
- Static password and token authentication exist    
- Service accounts are managed by Kubernetes    
- Authentication answers **who you are**    
- Authorization (RBAC) answers **what you can do**    
- Static auth methods are not recommended for production

---
