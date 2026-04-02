# Kubernetes KubeConfig – Complete Guide (KCNA / CKA)
## 1. What is KubeConfig and Why It Exists
KubeConfig is a **configuration file used by kubectl and other Kubernetes clients** to:
- Authenticate to a Kubernetes cluster    
- Know **which cluster** to connect to    
- Know **which user credentials** to use    
- Know **which namespace** to operate in by default    
Without kubeconfig, every kubectl command would need full authentication details.
### Without kubeconfig (manual REST call)
```zsh
curl https://my-kube-playground:6443/api/v1/pods \
  --key admin.key \
  --cert admin.crt \
  --cacert ca.crt
```
### With kubeconfig
`kubectl get pods`
Kubeconfig **removes repetition**, **reduces errors**, and **supports multiple clusters and users**.

---
## 2. Default Location and How kubectl Uses It
kubectl looks for kubeconfig in the following order:
1. `--kubeconfig` flag (highest priority)    
2. `KUBECONFIG` environment variable    
3. Default path:    
    `~/.kube/config`    
If your kubeconfig file is placed at `~/.kube/config`, kubectl automatically uses it.
Example:
`kubectl get pods --kubeconfig my_custom_config`

---
## 3. High-Level Structure of a KubeConfig File
A kubeconfig file has **four main sections**:

| Section         | Purpose                                       |
| --------------- | --------------------------------------------- |
| clusters        | Defines Kubernetes clusters (API server + CA) |
| users           | Defines credentials (certs, tokens, keys)     |
| contexts        | Maps a user to a cluster (and namespace)      |
| current-context | The active context kubectl uses               |
Think of it as:
> **Context = User + Cluster (+ Namespace)**
---
## 4. Clusters Section (Who am I talking to?)
This section defines **where the API server is** and **how to trust it**.
Example:
```yaml
clusters:
- name: my-kube-playground
  cluster:
    server: https://my-kube-playground:6443
    certificate-authority: ca.crt
```
### Important fields
- `server`: API server endpoint
- `certificate-authority`: CA certificate used to verify the API server
- `certificate-authority-data`: Base64-encoded CA (embedded)
Only **trust** is defined here — **no user authentication**.

---
## 5. Users Section (Who am I?)
This section defines **how the client authenticates** to the API server.
Example (certificate-based authentication):
```yaml
users:
- name: my-kube-admin
  user:
    client-certificate: admin.crt
    client-key: admin.key
```
Other authentication methods you may see:
- Client certificates (most common for clusters)
- Bearer tokens
- Exec plugins (cloud providers)
This section contains **sensitive data** and must be protected.

---
## 6. Contexts Section (Who am I + Where am I working?)
Contexts link **one user** to **one cluster**, optionally with a namespace.
Example:
```yaml
contexts:
- name: my-kube-admin@my-kube-playground
  context:
    cluster: my-kube-playground
    user: my-kube-admin
    namespace: default
```
### Why contexts matter
- You can switch clusters **without changing files**
- You can switch users easily
- You can default namespaces per context

---
## 7. current-context (What kubectl uses right now)
This tells kubectl **which context is active**.
Example:
`current-context: my-kube-admin@my-kube-playground`

Switching context:
`kubectl config use-context prod-user@production`

kubectl updates `current-context` automatically.

---
## 8. Viewing and Managing KubeConfig
`kubectl config --help`
### View full config
`kubectl config view`
`kubectl config view --kubeconfig=my-custom-config`
### List contexts
`kubectl config get-contexts`
### Show current context
`kubectl config current-context`
### Switch context
`kubectl config use-context prod-user@production`

---
## 9. Namespaces in KubeConfig
You can **bind a namespace to a context**.
Example:
```yaml
contexts:
- name: admin@production
  context:
    cluster: production
    user: admin
    namespace: finance
```
Now:
`kubectl get pods`
automatically runs in the `finance` namespace.
This avoids repeatedly typing:
`-n finance`

---
## 10. Certificate Paths vs Embedded Certificate Data
### Referencing certificate files
`certificate-authority: /etc/kubernetes/pki/ca.crt`

### Embedding certificates (base64)
`certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0t`
`cat ca.crt | base64`
`echo "BASE64_CODED_CONTENTS" | base64 --decode`
### Why embedding is useful
- Portable kubeconfig    
- Works without external files    
- Common in cloud-managed clusters

Same applies to:
- `client-certificate-data`
- `client-key-data`
---
## 11. KubeConfig in Real Clusters (kubeadm)
In kubeadm clusters, the admin kubeconfig is usually created at:
`/etc/kubernetes/admin.conf`

You often copy it to:
`~/.kube/config`

Example kubeadm kubeconfig:
```yaml
apiVersion: v1
kind: config
clusters:
- cluster:
    server: https://172.17.0.5:6443
    certificate-authority-data: REDACTED
    certificate-authority: ca.crt

contexts:
- context:
    cluster: kubernetes
    user: kubernetes-admin
  name: kubernetes-admin@kubernetes

users:
- name: kubernetes-admin
  user:
    client-certificate-data: REDACTED
    client-key-data: REDACTED

current-context: kubernetes-admin@kubernetes
```
---

## 12. Security Best Practices (Very Important)
- Never commit kubeconfig to public repositories    
- Protect client keys and tokens    
- Use RBAC to limit user permissions    
- Rotate certificates regularly    
- Prefer embedded certs only when necessary

---
## 13. Summary Table (Revision Friendly)

|Component|Purpose|
|---|---|
|clusters|API server + CA trust|
|users|Authentication credentials|
|contexts|User + cluster (+ namespace)|
|current-context|Active working context|
|~/.kube/config|Default kubeconfig location|
|kubectl config|Tool to manage kubeconfig|

---
## Summary Table
Below is a table summarizing key components of a kubeconfig file and their use cases:

|Section|Purpose|Example Entry|
|---|---|---|
|Clusters|Specifies the Kubernetes cluster details|`server: https://my-kube-playground:6443`|
|Users|Contains credentials and certificate info for a user|`client-certificate: admin.crt`|
|Contexts|Maps a user to a cluster and optionally a namespace|`context: { cluster: production, user: admin, namespace: finance }`|
|Current Context|Defines the default context for kubectl commands|`current-context: prod-user@production`|

---
## 14. KCNA / CKA Exam Tips
You **must know**:
- Structure of kubeconfig    
- What context means    
- How kubectl selects kubeconfig    
- How to switch contexts    
- Difference between cluster, user, context    
- Where kubeconfig lives by default    
You **do not need to memorize** base64 values.
---
## One-Line Mental Model
> **KubeConfig tells kubectl: which cluster to talk to, who you are, and where you are working — all in one file.**

For more detailed information on managing Kubernetes clusters, consider exploring these resources:
- [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Hub](https://hub.docker.com/)
- [Terraform Registry](https://registry.terraform.io/)
---
