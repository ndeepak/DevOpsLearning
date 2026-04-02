 # Static Pods: kubelet.service & kubelet config (Simple + Exam-Ready)

This section answers **two common questions** in CKA/KCNA:
1. **How does kubelet know where static pod YAML files are?**    
2. **What are `kubelet.service`, `kubeconfig`, and `kubelet config` actually doing?**
---
## 1️⃣ `kubelet.service` — the starting point
The **kubelet.service** file is a **systemd unit file**.  
It defines **how kubelet starts** and **which files it uses**.

You don’t edit static pods here, but you **look here to FIND static pods**.
### How to view it
`systemctl cat kubelet # or systemctl status kubelet`

---
## 2️⃣ Two ways kubelet is told about Static Pods
### ✅ Method 1: Direct flag (older / simpler)
`--pod-manifest-path=/etc/kubernetes/manifests`

✅ Meaning:
- kubelet watches this directory    
- any pod YAML here becomes a **static pod**
    

✅ Exam hint:
`Static Pod Path → /etc/kubernetes/manifests`

---
### ✅ Method 2 (Preferred): kubelet config file
Instead of many flags, kubelet uses **one config file**.

In `kubelet.service`:
`--config=/var/lib/kubelet/config.yaml`

Inside that file:
`staticPodPath: /etc/kubernetes/manifests`

✅ This is what **kubeadm clusters use**  
✅ Cleaner, more scalable

---
## 3️⃣ kubelet config file (`config.yaml`) — what it is
This is called **KubeletConfiguration** (NOT kubeconfig).
📌 Purpose:  
Controls **kubelet behavior**
### Minimal example (important parts only)
```yaml
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1

staticPodPath: /etc/kubernetes/manifests

clusterDomain: cluster.local
clusterDNS:
  - 10.96.0.10
```

### What to remember for exams

|Field|Meaning|
|---|---|
|`staticPodPath`|Where static pod YAML files live|
|`clusterDNS`|DNS given to pods|
|`clusterDomain`|Cluster domain|
**Static pods are controlled HERE**, not in API server.

---
## 4️⃣ kubeconfig file — DIFFERENT thing (very important)
⚠️ **Common confusion alert**

|File|Purpose|
|---|---|
|**kubelet config**|Controls kubelet behavior|
|**kubeconfig**|Gives kubelet API server access|

---
### kubeconfig = authentication file
Path usually used:
`--kubeconfig=/var/lib/kubelet/kubeconfig`

📌 This allows kubelet to:
- Talk to API server    
- Create **mirror pods**    
- Register the node    

---
### Minimal kubeconfig example (conceptual)
```yaml
apiVersion: v1
kind: Config

clusters:
- name: kubernetes
  cluster:
    server: https://10.0.0.1:6443
    certificate-authority: ca.crt

users:
- name: kubelet-node
  user:
    client-certificate: kubelet.crt
    client-key: kubelet.key
```

✅ If API server is **down**, kubelet:
- Still runs static pods
- Just cannot create mirror pods
---
## 5️⃣ How Static Pods actually get created
### Step-by-step (MEMORIZE THIS FLOW)
1. kubelet starts (`kubelet.service`)    
2. kubelet reads:    
    - `--pod-manifest-path` **OR**        
    - `staticPodPath` from config file        
3. kubelet scans directory:    
    `/etc/kubernetes/manifests`    
4. kubelet finds `.yaml` file    
5. kubelet creates pod directly (NO scheduler)    
6. If API server is reachable → mirror pod appears
---
## 6️⃣ Where control plane static pods live (CKA GOLD)
On control-plane nodes:
`/etc/kubernetes/manifests/`
Files you’ll see:
- `kube-apiserver.yaml`
- `etcd.yaml`
- `kube-scheduler.yaml`
- `kube-controller-manager.yaml`
These are **static pods** ✅
---
## 7️⃣ Key exam truths (short & sharp)
✅ Static pods are:
- Managed by **kubelet**
- Defined by **local YAML files**
- Independent of scheduler
- Removed ONLY by deleting the file

❌ You CANNOT:
- Scale static pods
- Use Deployment/ReplicaSet
- Delete them via kubectl
---
## 8️⃣ One-look comparison (EXAM FAVORITE)

|Item|Static Pods|DaemonSet|
|---|---|---|
|Created by|kubelet|Controller|
|Config location|Node filesystem|API server|
|Scheduler|❌|✅|
|Control plane use|✅|❌|
|Delete method|Delete file|kubectl|

---
## 9️⃣ Memory line (helps under pressure)
> **Static Pods live on disk,  
> are watched by kubelet,  
> and ignore the scheduler.**

---
## ✅ Final takeaway (KCNA friendly)
- `kubelet.service` → starts kubelet
- `--pod-manifest-path` OR `staticPodPath` → static pods location
- `kubelet config` → behavior settings
- `kubeconfig` → API server access
- Static pods → used for control plane bootstrapping

---
