# ETCD In Kubernetes
## 1. What is etcd’s Role in Kubernetes?
etcd is the **database of the Kubernetes control plane**.  
It stores _every piece of cluster state_, such as:
- Nodes registered in the cluster    
- Pods and Deployments    
- Config, ConfigMaps and Secrets    
- Account, Roles and RBAC objects (Roles, RoleBindings)    
- Custom Resource Definitions (CRDs)    

When you execute a command like:
`kubectl get pods`

The **kube-apiserver** reads data from **etcd**.  
When you run:
`kubectl create -f pod.yaml`
The API server writes new data into etcd.
### Conceptual Flow:
`kubectl → kube-apiserver → etcd → kube-controller-manager / scheduler / kubelet`

---
## 2. etcd Basics
- etcd stores key-value data under the `/registry/` directory.    
- It listens by default on port **2379** for client requests (API server communication).    
- etcd can be run **as a single instance (non-HA)** or **as a cluster (HA)**.    

---
## 3. Deployment Methods
### A. Manual Deployment (from scratch)
Useful if you’re building a Kubernetes control plane manually (e.g., for CKA practice or in a custom environment).

### B. kubeadm Deployment
Used in production-like or managed environments; kubeadm configures etcd as a **static Pod** managed by the **kubelet**.

---
## 4. Manual etcd Deployment Example
### Step 1: Download and Install etcd
```zsh
wget -q --https-only \
"https://github.com/coreos/etcd/releases/download/v3.3.9/etcd-v3.3.9-linux-amd64.tar.gz"

tar xzf etcd-v3.3.9-linux-amd64.tar.gz
sudo mv etcd-v3.3.9-linux-amd64/etcd* /usr/local/bin/
```
Verify:
`etcd --version`

---
### Step 2: Configure etcd Service (Single Node)
Example service file `/etc/systemd/system/etcd.service`:
```scss
[Unit]
Description=etcd key-value store
Documentation=https://github.com/coreos/etcd
After=network.target

[Service]
ExecStart=/usr/local/bin/etcd \
  --name controller-0 \
  --cert-file=/etc/etcd/kubernetes.pem \
  --key-file=/etc/etcd/kubernetes-key.pem \
  --trusted-ca-file=/etc/etcd/ca.pem \
  --peer-cert-file=/etc/etcd/kubernetes.pem \
  --peer-key-file=/etc/etcd/kubernetes-key.pem \
  --peer-trusted-ca-file=/etc/etcd/ca.pem \
  --peer-client-cert-auth \
  --client-cert-auth \
  --listen-peer-urls=https://127.0.0.1:2380 \
  --listen-client-urls=https://127.0.0.1:2379 \
  --advertise-client-urls=https://127.0.0.1:2379 \
  --initial-advertise-peer-urls=https://127.0.0.1:2380 \
  --initial-cluster controller-0=https://127.0.0.1:2380 \
  --initial-cluster-token etcd-cluster-0 \
  --initial-cluster-state new \
  --data-dir=/var/lib/etcd

Restart=always
RestartSec=10s

[Install]
WantedBy=multi-user.target
```

Enable and start etcd:
```zsh
sudo systemctl daemon-reload
sudo systemctl enable etcd
sudo systemctl start etcd
sudo systemctl status etcd
```

---
### Step 3: Verify etcd Operation
```zsh
export ETCDCTL_API=3
etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/etcd/ca.pem \
  --cert=/etc/etcd/kubernetes.pem \
  --key=/etc/etcd/kubernetes-key.pem endpoint health
```
Expected output:
```cpp
https://127.0.0.1:2379 is healthy
```
---
## 5. High Availability (HA) Setup
In production, you need an **etcd cluster** to avoid data loss if one node fails.
### Example Cluster (3 nodes):

|Node|IP Address|Name|
|---|---|---|
|1|10.0.0.1|controller-0|
|2|10.0.0.2|controller-1|
|3|10.0.0.3|controller-2|

Each node runs etcd with the following configuration (changing names and IPs per node):
```zsh
ExecStart=/usr/local/bin/etcd \
  --name controller-0 \
  --cert-file=/etc/etcd/kubernetes.pem \
  --key-file=/etc/etcd/kubernetes-key.pem \
  --peer-cert-file=/etc/etcd/kubernetes.pem \
  --peer-key-file=/etc/etcd/kubernetes-key.pem \
  --trusted-ca-file=/etc/etcd/ca.pem \
  --peer-trusted-ca-file=/etc/etcd/ca.pem \
  --peer-client-cert-auth \
  --client-cert-auth \
  --listen-peer-urls=https://10.0.0.1:2380 \
  --listen-client-urls=https://10.0.0.1:2379,https://127.0.0.1:2379 \
  --advertise-client-urls=https://10.0.0.1:2379 \
  --initial-advertise-peer-urls=https://10.0.0.1:2380 \
  --initial-cluster-token=etcd-cluster-0 \
  --initial-cluster controller-0=https://10.0.0.1:2380,controller-1=https://10.0.0.2:2380,controller-2=https://10.0.0.3:2380 \
  --initial-cluster-state=new \
  --data-dir=/var/lib/etcd
```
### Verify Cluster Health
From any etcd node:
```zsh
ETCDCTL_API=3 etcdctl endpoint status --write-out=table \
  --endpoints=https://10.0.0.1:2379,https://10.0.0.2:2379,https://10.0.0.3:2379 \
  --cacert=/etc/etcd/ca.pem \
  --cert=/etc/etcd/kubernetes.pem \
  --key=/etc/etcd/kubernetes-key.pem
```
---
## 6. Deploying etcd with kubeadm
When you use `kubeadm init`, it automatically configures etcd as a **static Pod** located in:
`/etc/kubernetes/manifests/etcd.yaml`
This file is managed by the kubelet directly. You can check it:
`cat /etc/kubernetes/manifests/etcd.yaml`

You’ll see parameters such as:
```yaml
command:
- etcd
- --advertise-client-urls=https://127.0.0.1:2379
- --cert-file=/etc/kubernetes/pki/etcd/server.crt
- --key-file=/etc/kubernetes/pki/etcd/server.key
- --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
- --data-dir=/var/lib/etcd
```
---
### Inspect etcd Pod
`kubectl get pods -n kube-system | grep etcd`

Typical output:
`etcd-master     1/1     Running   0     1h`

Check its logs:
`kubectl logs etcd-master -n kube-system`

---
### Explore etcd Data
You can inspect Kubernetes data directly in etcd:
`kubectl exec -it etcd-master -n kube-system -- sh`

Inside the container:
```bash
export ETCDCTL_API=3
etcdctl get / --prefix --keys-only
```
Output:
```scss
/registry/apiregistration.k8s.io/apiservices/v1
/registry/namespaces/default
/registry/pods/default/nginx
/registry/configmaps/kube-root-ca.crt
```
Every Kubernetes resource is stored under `/registry`.

---
## 7. etcd Backup and Restore (CKA-Level)
This is one of the most important exam tasks.

### Backup
```zsh
export ETCDCTL_API=3
ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.crt
ETCDCTL_CERT=/etc/kubernetes/pki/etcd/server.crt
ETCDCTL_KEY=/etc/kubernetes/pki/etcd/server.key
ETCDCTL_ENDPOINTS=https://127.0.0.1:2379

etcdctl snapshot save /opt/snapshot.db \
  --endpoints=$ETCDCTL_ENDPOINTS \
  --cacert=$ETCDCTL_CACERT \
  --cert=$ETCDCTL_CERT \
  --key=$ETCDCTL_KEY
```
### Verify Backup
`etcdctl snapshot status /opt/snapshot.db --write-out=table`

Output example:
```scss
+----------+----------+------------+-----------+
| HASH     | REVISION | TOTAL KEYS | SIZE (MB) |
+----------+----------+------------+-----------+
| 6ab4d2a4 | 1225     | 700        | 12.3      |
+----------+----------+------------+-----------+
```
---
### Restore
1. Stop kube-apiserver and etcd static pods:    
    `mv /etc/kubernetes/manifests/etcd.yaml /tmp/`    
2. Restore snapshot to a new directory:    
    `etcdctl snapshot restore /opt/snapshot.db --data-dir=/var/lib/etcd-from-backup`    
3. Edit `/etc/kubernetes/manifests/etcd.yaml` and update:    
    `- --data-dir=/var/lib/etcd-from-backup`    
4. Move manifest back:    
    `mv /tmp/etcd.yaml /etc/kubernetes/manifests/`
Kubelet restarts the etcd Pod automatically.

---
## 8. Security Considerations
- Always enable **client and peer certificate authentication**.    
- Never expose port **2379** publicly.    
- Keep snapshots secure; they contain Secrets and ConfigMaps in plaintext.    

---
## 9. Summary

|Concept|Command / File|Notes|
|---|---|---|
|etcd location in kubeadm|`/etc/kubernetes/manifests/etcd.yaml`|Static Pod|
|Default client port|2379|Used by kube-apiserver|
|etcdctl API version|`export ETCDCTL_API=3`|Required for v3 syntax|
|Backup|`etcdctl snapshot save`||
|Restore|`etcdctl snapshot restore`||
|Data storage|`/var/lib/etcd`|Contains database files|
|View keys|`etcdctl get / --prefix --keys-only`|Inside etcd Pod|

---
