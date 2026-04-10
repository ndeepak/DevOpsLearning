# TLS In Kubernetes

## TLS in Kubernetes – Certificate Creation (KCNA + CKA)
Kubernetes relies on **mutual TLS (mTLS)** for almost all internal and external communication. This means:
- **Clients authenticate servers**    
- **Servers authenticate clients**    
- **All traffic is encrypted**    
- **Trust is established through a shared Certificate Authority (CA)**    

This guide explains how certificates are created manually using **OpenSSL**, which is critical knowledge for **CKA**, even though tools like `kubeadm` automate most of this in practice.

---
## 1. Why TLS Is Mandatory in Kubernetes
Kubernetes is a **distributed system** with many components:
- kube-apiserver    
- etcd    
- kubelet    
- scheduler    
- controller-manager    
- kube-proxy    
- nodes and pods    

Without TLS:
- Credentials could be stolen    
- API requests could be tampered with    
- Nodes could impersonate each other    
- Cluster compromise would be trivial    

Therefore:
- **Every component uses certificates**    
- **Every component trusts a common CA**    

---
## 2. Certificate Authority (CA)
### What the CA does
The **Certificate Authority** is the root of trust.
- It signs all certificates    
- Any certificate signed by the CA is trusted    
- All Kubernetes components must trust the CA    

Kubernetes usually has **multiple CAs**:
- Cluster CA (API server, users, kubelets)    
- etcd CA (etcd server and peers)    
- Front-proxy CA (aggregation layer)    
For learning clarity, we start with **one CA**.

---
## 3. Creating the CA Certificate
### Step 1: Generate CA private key
`openssl genrsa -out ca.key 2048`
- `ca.key` is **highly sensitive**    
- If compromised, the entire cluster is compromised    
- Must be protected with strict permissions    
---
### Step 2: Create a Certificate Signing Request (CSR)
`openssl req -new -key ca.key -subj "/CN=KUBERNETES-CA" -out ca.csr`
- `CN` identifies the CA
- Kubernetes does not enforce a fixed CA name
- The CN is informational

---
### Step 3: Self-sign the CA certificate
`openssl x509 -req -in ca.csr -signkey ca.key -out ca.crt`
Results:
- `ca.key` → private key
- `ca.crt` → public certificate
This CA is now ready to sign **all other certificates**.

---
## 4. Client Certificates (Human and System Users)
Client certificates are used when:
- A user talks to the API server    
- A component authenticates itself    
---
## 5. Admin User Certificate
### Why admin needs a certificate
- Kubernetes does not store users    
- Admin access must be authenticated externally    
- Certificates are the strongest option    
---
### Step 1: Generate admin private key
`openssl genrsa -out admin.key 2048`

---
### Step 2: Create admin CSR
`openssl req -new -key admin.key -subj "/CN=kube-admin" -out admin.csr`
- `CN` becomes the **username** inside Kubernetes
---
### Step 3: Sign admin certificate with CA
`openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -out admin.crt`
This certificate can now authenticate to the API server.

---
## 6. Admin Privileges via Groups (Very Important for CKA)
### Why groups matter
Kubernetes authorization (RBAC) often uses **groups**, not individual users.
The group `system:masters`:
- Has **cluster-admin** privileges by default    
- Bypasses most authorization restrictions    
---
### Create admin CSR with group
```bash
openssl req -new -key admin.key \
-subj "/CN=kube-admin/O=system:masters" \
-out admin.csr
```

Then sign it again:
`openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -out admin.crt`

Key concept:
- `CN` → username    
- `O` → group membership    

---
## 7. Other Client Certificates (System Components)
* Generate Keys
* Certificate Signing Request
* Sign Certificates
The same process is used for:
- kube-scheduler    
	- scheduler.key
	- scheduler.csr
		- system:kube_scheduler
	- scheduler.crt
- kube-controller-manager    
	- controller-manager.key
	- controller-manager.csr
		- system:kube_container_manager
	- controller-manager.crt
- kube-proxy    
	- kube-proxy.key
	- kube-proxy.csr
		- system:kube_proxy
	- kube-proxy.crt

Naming conventions:
- Usually start with `system:`    
- Example CNs:    
    - `system:kube-scheduler`        
    - `system:kube-controller-manager`        

These names are important because:
- RBAC rules depend on them    
- API server recognizes them as system identities    

---
## 8. Using Certificates to Access the API Server
### Direct REST API access
```bash
curl https://kube-apiserver:6443/api/v1/pods \
  --key admin.key \
  --cert admin.crt \
  --cacert ca.crt
```
What happens:
1. API server presents its certificate
2. Client verifies it using `ca.crt`
3. Client presents its certificate
4. API server verifies it using `ca.crt`
5. Authentication succeeds
6. Authorization (RBAC) is checked

How to use client certificates for clients?
```bash
curl https://kube-apiserver:6443/api/v1/pods \
 --key admin.key --cert admin.crt
 --cacert ca.crt
```

Output:
```scss
{
	"kind": "PodList",
	"apiVersion": "v1",
	"metadata": {
	....
	}...
}
```

---
## 9. kubeconfig File (Preferred Method)
Instead of passing certs every time, use a **kubeconfig**.
```yaml
apiVersion: v1
kind: Config
clusters:
- name: kubernetes
  cluster:
    certificate-authority: ca.crt
    server: https://kube-apiserver:6443

users:
- name: kubernetes-admin
  user:
    client-certificate: admin.crt
    client-key: admin.key
```
This is how:
- kubectl works
- automation tools authenticate

---
## 10. Server-Side Certificates (Mutual TLS)
### Mutual TLS means:
- Servers also authenticate themselves
- Clients trust servers using CA certificates
---
## 11. etcd Server Certificates
* etcdserver.crt
* etcdserver.key
### Why etcd needs TLS
- etcd stores:
    - Secrets
    - ConfigMaps        
    - Cluster state        
- etcd compromise = cluster compromise

---
### etcd certificate usage
- `--cert-file` → server certificate
- `--key-file` → server private key
- `--trusted-ca-file` → CA used to verify clients
- `--client-cert-auth=true` → enforce client certs

Example etcd flags:
```scss
--cert-file=/path-to-certs/etcdserver.crt
--key-file=/path-to-certs/etcdserver.key
--trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
--client-cert-auth=true
```
### Peer certificates
- Used for etcd cluster member communication
- Prevent rogue nodes from joining etcd   

---
## 12. Kube API Server Certificate
* apiserver.crt
* apiserver.key
* kube-api-server
* kubernetes.default
* kubernetes.default.svc.local
* IP address running the kube api server

Generating Certs
Key
```bash
openssl genrsa -out apiserver.key 2048
apiserver.key
```

CSR
```bash
openssl req -new -key apiserver.key -subj \
	"CN=kube-apiserver" -out apiserver.csr

apiserver.csr 
```

Specifying ALTNames
**openssl.cnf**
```ini
[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation,
subjectAltName = @alt_names
[alt_names]
DNS.1 = kubernetes
DNS.2 = kubernetes.default
DNS.3 = kubernetes.default.svc
DNS.4 = kubernetes.default.svc.cluster.local
IP.1 = 10.96.0.1
IP.2 = 172.17.0.87
```

Sign the certificate
```bash
openssl x509 -req -in apiserver.csr -CA ca.crt -CAKey ca.key -CAcreateserial -out apiserver.crt -extensions v3_req -extfile openssl.cnf -days 10000

apiserver.crt
```


### Why API server certificate is special
The API server:
- Is accessed via **many DNS names**    
- Is accessed via **IP addresses**    
- Must support **all of them**    

---
### Required Subject Alternative Names (SANs)
Common DNS names:
- kubernetes    
- kubernetes.default    
- kubernetes.default.svc    
- kubernetes.default.svc.cluster.local    

IP addresses:
- Service IP (e.g., 10.96.0.1)    
- Node or Pod IP    

---
### Create API server key and CSR
```bash
openssl genrsa -out apiserver.key 2048
openssl req -new -key apiserver.key \
-subj "/CN=kube-apiserver" \
-out apiserver.csr
```

---

### OpenSSL config for SANs
```ini
[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name

[v3_req]
basicConstraints = CA:FALSE
keyUsage = digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = kubernetes
DNS.2 = kubernetes.default
DNS.3 = kubernetes.default.svc
DNS.4 = kubernetes.default.svc.cluster.local
IP.1 = 10.96.0.1
IP.2 = 172.17.0.87
```
---
### Sign API server certificate
```bash
openssl x509 -req -in apiserver.csr \
-CA ca.crt -CAkey ca.key \
-out apiserver.crt \
-extensions v3_req \
-extfile openssl.cnf
```

---
## 13. API Server TLS Configuration
Key flags:
```scss
--tls-cert-file=/var/lib/kubernetes/apiserver.crt
--tls-private-key-file=/var/lib/kubernetes/apiserver.key
--client-ca-file=/var/lib/kubernetes/ca.pem
```

Purpose:
- Server presents its cert
- Server validates client certs    

---
## 14. Kubelet Certificates (Node Identity – CKA Critical)
### Why kubelet certificates are special
- Nodes must authenticate to the API server    
- Each node has **unique permissions**    
- Node identity is enforced by naming    

### Naming convention
`CN=system:node:<nodeName>`

Example:
`system:node:node01`

This allows:
- Node Authorizer    
- NodeRestriction admission plugin    
- Fine-grained permissions per node    

---

### Where kubelet certs are used
- kubelet → API server    
- API server → kubelet (metrics, logs, exec)    

Certificates are referenced in:
- kubelet kubeconfig    
- API server flags    

---
## 15. Certificate Distribution via kubeconfig
Each component has its own kubeconfig:
- admin.conf    
- scheduler.conf    
- controller-manager.conf    
- kubelet.conf    

Each kubeconfig includes:
- CA certificate    
- Client certificate    
- Client private key    

---
## 16. Summary (KCNA + CKA)
Key points you must know:
- Kubernetes uses **mutual TLS everywhere**    
- A **CA signs all certificates**    
- `CN` maps to username    
- `O` maps to group    
- `system:masters` = admin    
- API server certificate requires **SANs**    
- etcd must always be encrypted    
- kubelet identity follows `system:node:<nodeName>`    
- kubeadm automates this, but **CKA expects you to understand it**

---
