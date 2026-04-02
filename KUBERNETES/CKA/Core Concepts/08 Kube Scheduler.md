# Kube Scheduler
### 1. What Is the Kube Scheduler?
The **kube-scheduler** is one of the **control plane** components in Kubernetes.  
Its job is to **assign newly created pods** to suitable nodes in the cluster.

When you create a pod (via Deployment, ReplicaSet, or directly), it is first stored in **etcd** through the **API Server**.  
At this point, the pod has **no node assigned** — its `spec.nodeName` field is empty.  
The scheduler continuously watches the API Server for such “unscheduled” pods and attempts to assign each of them to a node.

After a scheduling decision is made:
- The scheduler **writes the decision** (which node the pod should go to) back to the API Server.
- Then the **Kubelet** on that node takes over and **creates the pod** on that node.
So:  
**Scheduler = decision maker**  
**Kubelet = executor**
## **Kube Scheduler**
### **Role**
The **Kube Scheduler** decides **which node** each **Pod** should run on.  
It **does not** create pods — that’s the **Kubelet’s** job.  
Its goal is to ensure **optimal resource use**, **fair workload distribution**, and **policy compliance** (like affinity, taints, etc.).

---
### **2. How the Scheduling Process Works**
The scheduling process consists of two major phases: **Filtering** and **Scoring (Ranking)**.
#### 1. **Filtering Phase**
- Filters out nodes that can’t run the pod due to:    
    - Insufficient CPU/memory        
    - Node taints        
    - Unsatisfied node selectors        
    - Missing labels or affinity violations        
- The remaining nodes are called **“feasible nodes.”**    
- It uses a set of **predicates** (rules) to determine which nodes can run the pod.

**Example:**  
Pod requires 10 CPUs  
→ Node1: 4 CPUs ❌  
→ Node2: 12 CPUs ✅  
→ Node3: 16 CPUs ✅  
Only Node2 and Node3 pass the filtering stage.

Other Examples of filters:
- **Node not ready:** If a node’s status is `NotReady`, it’s excluded.    
- **Insufficient resources:** Nodes without enough CPU/memory requested by the pod are removed.    
- **Taints and Tolerations:** If a node is tainted and the pod doesn’t have a matching toleration, the node is excluded.    
- **Node Selectors / Node Affinity:** If the pod requires a certain label (e.g., `disktype=ssd`), only nodes matching that label are considered.    
- **Pod affinity / anti-affinity:** Ensures certain pods are placed together or apart.    
After filtering, you get a list of **feasible node**

---
#### 2. **Ranking (Scoring) Phase**
- Scheduler ranks feasible nodes using **priority functions**.    
- Scores range from **0 to 10**.    
- Node with the **highest score** wins.    
From the feasible nodes, the scheduler must pick the **best** one.  
It applies several **scoring functions** (sometimes called priorities) to each node and gives a score between **0 and 100** (older versions used 0–10).  
Then it picks the node with the **highest total score**.

Common scoring criteria:
- **Least Requested Priority:** Prefers nodes with the most free resources (to spread workloads evenly).    
- **Balanced Resource Allocation:** Prefers nodes that use CPU and memory in balanced proportions.    
- **Node Affinity:** Adds score bonuses to nodes matching the pod’s preferred affinity rules.    
- **Image Locality:** Prefers nodes that already have the required container image cached.    

If there are multiple nodes with equal scores, Kubernetes picks one randomly.
Example:  
Node2 leaves 2 CPUs free → Score 6  
Node3 leaves 6 CPUs free → Score 10  
✅ **Pod scheduled on Node3**

---
### **3. Installing and Running Kube Scheduler**
#### Download Binary
`wget https://storage.googleapis.com/kubernetes-release/release/v1.13.0/bin/linux/amd64/kube-scheduler`
#### Example Service File
```ini
# /etc/systemd/system/kube-scheduler.service
ExecStart=/usr/local/bin/kube-scheduler \
  --config=/etc/kubernetes/config/kube-scheduler.yaml \
  --v=2
Restart=on-failure
```

Example configuration (`/etc/kubernetes/config/kube-scheduler.yaml`):
```yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
- schedulerName: default-scheduler
  plugins:
    score:
      disabled:
      - name: NodeResourcesBalancedAllocation
      enabled:
      - name: NodeResourcesLeastAllocated
```

In the above configuration:
- The default scoring plugin is replaced with a different one that prefers nodes with the most available resources.

You can also run **multiple schedulers** by giving them different names and having pods specify which scheduler to use:
`spec:   schedulerName: my-custom-scheduler`
This is rarely needed in normal environments but can appear in exam questions to test your conceptual understanding.
### 4. Scheduler in Cluster Setup
#### a. Kubeadm-Based Clusters
In clusters created using **kubeadm**, the scheduler runs as a **static Pod** managed by the kubelet on the control plane node.

Check its manifest file:
`cat /etc/kubernetes/manifests/kube-scheduler.yaml`

This YAML defines:
- The scheduler container image
- Its arguments    
- Mounted config files (if any)
You can inspect logs using:
`kubectl logs -n kube-system kube-scheduler-<node-name>`

#### b. Manual Installation
If installing manually:
- Download the binary:
    `wget https://storage.googleapis.com/kubernetes-release/release/v1.13.0/bin/linux/amd64/kube-scheduler`
    
- Create a systemd unit file:
```ini
[Service]
ExecStart=/usr/local/bin/kube-scheduler \
  --config=/etc/kubernetes/config/kube-scheduler.yaml \
  --v=2
Restart=on-failure
RestartSec=5
```    

Start and enable the service.
#### Verify Running Process
`ps -aux | grep kube-scheduler`

Example:
```scss
root  2477  0.8  1.6  48524 34044 ?  Ssl  kube-scheduler --address=127.0.0.1 --kubeconfig=/etc/kubernetes/scheduler.conf --leader-elect=true
```
---
### 5. Observing the Scheduler in Action
When a new pod is created:
1. Initially, it appears as **Pending** because it has not yet been scheduled.    
2. The scheduler examines available nodes.    
3. Once a node is selected, the scheduler updates the pod spec with the node name.    
4. The Kubelet on that node starts the pod.    

You can observe this with:
`kubectl get pods -o wide`
and look at the `NODE` column to see where each pod landed.

To view scheduling decisions and reasons:
`kubectl describe pod <pod-name>`

This often includes lines like:
```scss
Events:
  Type     Reason            Message
  ----     ------            -------
  Normal   Scheduled         Successfully assigned default/nginx to worker-node-1
```

---

### 6. Common Exam-Relevant Topics
**a. NodeSelector**  
Specify a node label for the pod to target.
```yaml
spec:
  nodeSelector:
    disktype: ssd
```

**b. Node Affinity**  
More flexible version of nodeSelector.
```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: disktype
            operator: In
            values:
            - ssd
```

**c. Pod Affinity / Anti-Affinity**  
Controls pod placement relative to other pods.
```yaml
spec:
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - frontend
        topologyKey: "kubernetes.io/hostname"
```

**d. Taints and Tolerations**  
Nodes can repel pods using taints; pods need tolerations to be scheduled on them.

Node taint:
`kubectl taint nodes node1 key=value:NoSchedule`

Pod toleration:
```yaml
tolerations:
- key: "key"
  operator: "Equal"
  value: "value"
  effect: "NoSchedule"
```

---
### 7. Key Points for KCNA / CKA

|Concept|Explanation|
|---|---|
|**Scheduler Role**|Assigns pods to nodes based on constraints and available resources|
|**Filtering Phase**|Excludes nodes that don’t satisfy the pod’s requirements|
|**Scoring Phase**|Ranks feasible nodes by scoring functions|
|**Output of Scheduler**|Updates pod’s `spec.nodeName`|
|**Kubelet Role Afterward**|Actually runs the pod on that node|
|**Custom Scheduler**|Can define a separate scheduler with its own logic|
|**Key Features**|Node affinity, taints/tolerations, resource requests/limits|
|**Logs Location (kubeadm)**|`kubectl logs -n kube-system kube-scheduler-<master>`|

---
### **Advanced Scheduling Concepts**
(You’ll explore these later)
- **NodeSelector**    
- **Node Affinity / Anti-affinity**    
- **Taints and Tolerations**    
- **Pod Priority and Preemption**    
- **Custom Schedulers**

---
### **In Short**

|Function|Description|
|---|---|
|**Component**|Master node|
|**Main Task**|Assign pods to nodes|
|**Phases**|Filtering → Scoring|
|**Decision Basis**|Resource availability, policies|
|**Runs As**|Systemd service or Pod (kubeadm)|

---
