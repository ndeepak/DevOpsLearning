# ETCD for beginners

# What is etcd?
- **etcd** is a **distributed, consistent key-value store** and **Reliable**
- It stores _all cluster data_ — such as Nodes, Pods, ConfigMaps, Secrets, etc.
- Think of it as the **"database" of your Kubernetes cluster**.
- It is simple, secure and fast.

In a Kubernetes control plane:
```scss
+----------------------+
| kube-apiserver       | --> Reads/Writes cluster data from/to etcd
+----------------------+
          |
          v
+----------------------+
| etcd (key-value DB)  |
+----------------------+
```
---
### Comparing Various types of storing mechanisms

| **Name**            | **Relational DB** | **Document Store** | **Key-Value Store** |
| ------------------- | ----------------- | ------------------ | ------------------- |
| **Schema**          | Yes               | No                 | No                  |
| **Complex Queries** | Yes (SQL)         | Limited (No joins) | No                  |
| **Performance**     | Good              | Good               | Super Fast          |
| **Flexibility**     | Rigid             | Flexible           | Very Flexible       |
| **Best for**        | Structured Data   | Un/Semi-Structured | Simple Fast Lookup  |

# 1. Understanding Key-Value Stores
A **key-value store** is like a simple dictionary:
`key: value`
Examples:

| Key    | Value       |
| ------ | ----------- |
| "name" | "Deepak"    |
| "city" | "Kathmandu" |
Unlike SQL databases, there are:
- **No tables or relations**    
- **No schema**    
- Very **fast and flexible**

---

# 2. Installing etcd (standalone mode)
You can try this in a Linux VM or even inside a Kubernetes master node (carefully).
```bash
# Download etcd binaries (example version)
curl -L https://github.com/etcd-io/etcd/releases/download/v3.5.13/etcd-v3.5.13-linux-amd64.tar.gz -o etcd.tar.gz

# Extract
tar xzf etcd.tar.gz
cd etcd-v3.5.13-linux-amd64

# Start etcd (foreground)
./etcd
```
* Default port for etcd: **2379**

It will start and print logs like:
```nginx
serving insecure client requests on 127.0.0.1:2379
```
---

# 3. etcdctl – the command-line client
`etcdctl` is the CLI tool used to interact with etcd.
Let’s check version first:
`./etcdctl version`
`,.etcdctl`

---

# 4. etcd API Versions (v2 vs v3)
Older etcd versions used **API v2**; newer ones use **v3** (which Kubernetes uses internally).
### Set API Version
`# Use API v3 `
`export ETCDCTL_API=3`

Confirm:
`./etcdctl version`

Output:
```scss
etcdctl version: 3.5.13
API version: 3.0
```

---

# 5. Basic etcdctl Operations (API v3)
### Put (Create Key)
`./etcdctl put mykey "Hello etcd"`

Output:
`OK`

### Get (Read Key)
`./etcdctl get mykey`

Output:
`mykey `
`Hello etcd`
### Update Key
`./etcdctl put mykey "Updated value"`
### Delete Key
`./etcdctl del mykey`
### List All Keys
`./etcdctl get "" --prefix --keys-only`

---
# 6. Watching Changes (Real-time Monitoring)
etcd supports _watching_ a key for changes.
Open **two terminals**:

**Terminal 1:**
`./etcdctl watch /app/config`

**Terminal 2:**
```bash
./etcdctl put /app/config "version1"
./etcdctl put /app/config "version2"
```

Terminal 1 will show:
```scss
PUT
/app/config
version1

PUT
/app/config
version2
```

This is how Kubernetes controllers react to changes in etcd!

---
# 7. Backup and Restore (VERY IMPORTANT for CKA!)
etcd backups are **critical** because they preserve the entire cluster state.
### Backup (snapshot)
`ETCDCTL_API=3 ./etcdctl snapshot save snapshot.db`

Output:
`Snapshot saved at snapshot.db`

### Verify Backup
`ETCDCTL_API=3 ./etcdctl snapshot status snapshot.db`

Output example:
```scss
Hash: d54a44f
Revision: 12345
Total keys: 700
```

### Restore from Snapshot
`ETCDCTL_API=3 ./etcdctl snapshot restore snapshot.db --data-dir=/var/lib/etcd-from-backup`
This restores etcd data into `/var/lib/etcd-from-backup`.

---
# 8. etcd in Kubernetes
In Kubernetes, etcd runs as a **Pod** (Static Pod) on the control-plane node.

Check it:
`kubectl get pods -n kube-system`

You’ll see something like:
`etcd-k8s-master`

Check configuration:
`cat /etc/kubernetes/manifests/etcd.yaml`

You’ll find:
```scss
command:
- etcd
- --advertise-client-urls=https://127.0.0.1:2379
- --data-dir=/var/lib/etcd
- --cert-file=/etc/kubernetes/pki/etcd/server.crt
```

---

# 9. etcd in HA (High Availability)
For production-grade clusters, etcd runs in **cluster mode** (3 or 5 nodes).
Each node:
- Has its own data directory    
- Communicates using the **Raft consensus algorithm**    

### Example HA Cluster:

|Node|Name|Peer URL|Client URL|
|---|---|---|---|
|etcd1|infra0|https://10.0.0.1:2380|https://10.0.0.1:2379|
|etcd2|infra1|https://10.0.0.2:2380|https://10.0.0.2:2379|
|etcd3|infra2|https://10.0.0.3:2380|https://10.0.0.3:2379|

They use **Raft** to maintain consistency — only one leader at a time, others are followers.

You can check cluster health:
`ETCDCTL_API=3 ./etcdctl endpoint status --write-out=table`

Output:
```scss
+------------------+---------+-----------+------------+-----------+
|     ENDPOINT     | HEALTH  |   DB SIZE |  LEADER ID | IS LEADER |
+------------------+---------+-----------+------------+-----------+
| 127.0.0.1:2379   | healthy |  10 MB    |  8e9e05c521 | true      |
+------------------+---------+-----------+------------+-----------+
```

---

# 10. etcd in CKA / KCNA Exams
### KCNA (Fundamentals)
You should know:
- etcd stores cluster state.    
- It’s key-value based.    
- kube-apiserver interacts with etcd.    

### CKA (Practical)
You should know how to:
- Backup etcd.    
- Restore from snapshot.    
- Check etcd health.    
- Locate etcd manifest.    

Sample CKA-style task:
> Take an etcd backup and store it in `/opt/snapshot.db`.

Solution:
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

---

# Summary

|Concept|Command / Note|
|---|---|
|Check version|`etcdctl version`|
|Set API|`export ETCDCTL_API=3`|
|Add key|`etcdctl put key value`|
|Get key|`etcdctl get key`|
|Backup|`etcdctl snapshot save snapshot.db`|
|Restore|`etcdctl snapshot restore snapshot.db`|
|Cluster status|`etcdctl endpoint status --write-out=table`|

---

