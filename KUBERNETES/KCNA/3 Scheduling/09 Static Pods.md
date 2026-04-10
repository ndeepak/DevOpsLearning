# Static Pods
# Static Pods in Kubernetes (CKA + KCNA Complete Guide)
## One-liner (perfect for exams)
A **Static Pod** is a pod **directly managed by the kubelet**, created from a **local manifest file**, **without the Kubernetes control plane**.

---
## Why Static Pods Exist (Core Idea)

![https://miro.medium.com/v2/resize%3Afit%3A1064/1%2AiCFd-rMhmvF6ALH24WIAXQ.png?utm_source=chatgpt.com](https://miro.medium.com/v2/resize%3Afit%3A1064/1%2AiCFd-rMhmvF6ALH24WIAXQ.png?utm_source=chatgpt.com)

![https://kodekloud.com/kk-media/image/upload/v1752880709/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Static-Pods/frame_430.jpg?utm_source=chatgpt.com](https://kodekloud.com/kk-media/image/upload/v1752880709/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Static-Pods/frame_430.jpg?utm_source=chatgpt.com)

![https://kodekloud.com/kk-media/image/upload/v1752880707/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Static-Pods/frame_340.jpg?utm_source=chatgpt.com](https://kodekloud.com/kk-media/image/upload/v1752880707/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Static-Pods/frame_340.jpg?utm_source=chatgpt.com)

Normally:
- API Server stores pod specs in **etcd**    
- Scheduler assigns node    
- Kubelet pulls instructions from API Server    

But what if:
- API Server is down?    
- etcd is unavailable?    
- Control plane is not bootstrapped yet?    
✅ **Static Pods** solve this bootstrap problem.

---
## Static Pod Definition (Concept)
A **static pod** is created when:
1. Pod YAML file is placed in a **local directory**
2. kubelet:    
    - Watches that directory        
    - Creates the pod        
    - Restarts it if it crashes        
    - Deletes it if file is removed        
✅ **No scheduler**  
✅ **No controller**  
✅ **No API server needed**

---
## What Static Pods CAN and CANNOT do

|Feature|Static Pod|
|---|---|
|Created by|kubelet|
|Needs API Server|❌|
|Needs Scheduler|❌|
|Objects supported|**Pod only**|
|Deployment / RS|❌|
|Manual scaling|❌|
|Auto restart|✅ kubelet|
|Used for control plane|✅|
**EXAM MUST-REMEMBER:**  
Static pods support **ONLY Pod objects** — nothing else.

---
## How kubelet knows where Static Pods live

![https://miro.medium.com/v2/resize%3Afit%3A1400/1%2A0GsemMDQTGd4F5CoxyifiA.png?utm_source=chatgpt.com](https://miro.medium.com/v2/resize%3Afit%3A1400/1%2A0GsemMDQTGd4F5CoxyifiA.png?utm_source=chatgpt.com)

![https://cdn.hashnode.com/res/hashnode/image/upload/v1681888104325/f801850d-bde9-459c-86bd-142e75cecf5b.png?utm_source=chatgpt.com](https://cdn.hashnode.com/res/hashnode/image/upload/v1681888104325/f801850d-bde9-459c-86bd-142e75cecf5b.png?utm_source=chatgpt.com)

### Option 1: Via kubelet flag
`--pod-manifest-path=/etc/kubernetes/manifests`

### Option 2: Via kubelet config file
`staticPodPath: /etc/kubernetes/manifests`

✅ kubeadm-based clusters use:
`/etc/kubernetes/manifests`

**CKA FAVORITE PATH**
`/etc/kubernetes/manifests`

---
## Example Static Pod YAML
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: static-web
spec:
  containers:
  - name: web
    image: nginx
```
 Save this file as:
`/etc/kubernetes/manifests/static-web.yaml`
➡ kubelet creates it automatically  
➡ Delete file → pod disappears

---
## How Static Pods appear in a CLUSTER
This is super important.

![https://kifarunix.com/wp-content/uploads/2024/06/kubernetes-static-vs-mirror-vs-daemonsets.png?utm_source=chatgpt.com](https://kifarunix.com/wp-content/uploads/2024/06/kubernetes-static-vs-mirror-vs-daemonsets.png?utm_source=chatgpt.com)

![https://miro.medium.com/v2/resize%3Afit%3A1400/1%2AiCFd-rMhmvF6ALH24WIAXQ.png?utm_source=chatgpt.com](https://miro.medium.com/v2/resize%3Afit%3A1400/1%2AiCFd-rMhmvF6ALH24WIAXQ.png?utm_source=chatgpt.com)
When API Server **IS available**:
- kubelet creates the static pod locally    
- kubelet also creates a **Mirror Pod** in API Server    

👉 Mirror pod properties:
- Read-only    
- Cannot be deleted via kubectl    
- Exists only for visibility    

`kubectl get pods`

You WILL see:
`static-web-node01`

 **EXAM CHECKPOINT**
- You **cannot edit/delete** a static pod via kubectl    
- You must edit the **manifest file**    

---
## Why pod names include node name
Static pod created on node `node01`:
`static-web-node01`
✅ Helps distinguish static pod origin  
✅ Mirror pod feature

---

## Control Plane Components = Static Pods

![https://miro.medium.com/v2/resize%3Afit%3A1064/1%2AiCFd-rMhmvF6ALH24WIAXQ.png?utm_source=chatgpt.com](https://miro.medium.com/v2/resize%3Afit%3A1064/1%2AiCFd-rMhmvF6ALH24WIAXQ.png?utm_source=chatgpt.com)

![https://kubernetes.io/images/docs/components-of-kubernetes.svg?utm_source=chatgpt.com](https://kubernetes.io/images/docs/components-of-kubernetes.svg?utm_source=chatgpt.com)

In kubeadm clusters, these are **static pods**:

|Component|
|---|
|kube-apiserver|
|etcd|
|kube-controller-manager|
|kube-scheduler|

Check:
`kubectl get pods -n kube-system`

Files live at:
`/etc/kubernetes/manifests/`

🔖 **VERY COMMON CKA QUESTION**
> “Where are the API server pod manifests stored?”
✅ `/etc/kubernetes/manifests`

---

## Static Pods on Standalone Node (No API Server)

![https://kodekloud.com/kk-media/image/upload/v1752880709/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Static-Pods/frame_430.jpg?utm_source=chatgpt.com](https://kodekloud.com/kk-media/image/upload/v1752880709/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Static-Pods/frame_430.jpg?utm_source=chatgpt.com)

![https://kubernetes.io/images/docs/components-of-kubernetes.svg?utm_source=chatgpt.com](https://kubernetes.io/images/docs/components-of-kubernetes.svg?utm_source=chatgpt.com)

If node has:
- kubelet ✅    
- container runtime ✅    
- NO API server ❌
    

Then:
- kubectl won’t work    
- docker / crictl will show containers    
`docker ps # or crictl ps`

---
## Static Pods vs DaemonSets (EXAM FAVORITE)

![https://kifarunix.com/wp-content/uploads/2024/06/kubernetes-static-vs-mirror-vs-daemonsets.png?utm_source=chatgpt.com](https://kifarunix.com/wp-content/uploads/2024/06/kubernetes-static-vs-mirror-vs-daemonsets.png?utm_source=chatgpt.com)

![https://media.licdn.com/dms/image/v2/D5622AQHi8Z3yg7cCmg/feedshare-shrink_800/B56ZpPYq1iHYAg-/0/1762268459223?e=2147483647&t=d0MvXtN8Eon3hTReV0TFKxHZ2SQa7cbIKE_gK_fZ0PQ&v=beta&utm_source=chatgpt.com](https://images.openai.com/thumbnails/url/AkP_s3icu5mZUVJSUGylr5-al1xUWVCSmqJbkpRnoJdeXJJYkpmsl5yfq5-Zm5ieWmxfaAuUsXL0S7F0Tw5yKfAz083ITTc2cTLXtQxOTzcu1E0JLHX3MEoy8_EJrvKLDC6qdDM0CvWxtAyvLAhVKwYAMIckzw?utm_source=chatgpt.com)

|Feature|Static Pod|DaemonSet|
|---|---|---|
|Created by|kubelet|Controller|
|Uses API Server|❌|✅|
|Uses Scheduler|❌|✅|
|Scale per node|Manual|Automatic|
|Delete method|Remove file|kubectl|
|Typical use|Control plane|Node agents|

🔖 **TRICK QUESTION**
> “Which one bypasses the scheduler?”

✅ **Static Pods**  
✅ **DaemonSet (older exam explanations) BUT NOW → scheduler is used**

➡ Static Pods **always bypass scheduler**

---

## Key Differences (One-liners for exam)
- Static Pod = **kubelet-managed**    
- DaemonSet = **API-server-managed**    
- Static Pod is **node-specific**    
- DaemonSet is **cluster-wide**    

---
## Static Pod Lifecycle Summary

|Action|Result|
|---|---|
|Modify YAML|Pod recreates|
|Delete YAML|Pod removed|
|Pod crashes|kubelet restarts|
|Node down|Pod gone|
|API server down|Pod still runs|

---
## Debugging Static Pods (CKA gold)
### Find manifest path
`ps -ef | grep kubelet`

or
`systemctl cat kubelet`

### Look for:
- `--pod-manifest-path`    
- `staticPodPath`    

---
## Common Exam Traps
### Trap 1
❌ Trying to delete static pod using kubectl  
✅ Must edit/remove manifest

---

### Trap 2
❌ Expecting Deployment / RS features  
✅ Static pods support pod only

---
### Trap 3
❌ Thinking scheduler places static pods  
✅ kubelet places them directly

---
## Memory Hook (Very Useful)
> **Static Pods are born on disk,  
> live by kubelet,  
> and die by file removal.**

---
## Final KCNA-Style Summary
- Static pods are managed by kubelet    
- Defined by local manifest files    
- No scheduler, no controller, no etcd needed    
- Used for control plane bootstrapping    
- Visible as mirror pods in API Server    
- Edited only via manifest file    

---