# 11 Configuring Kubernetes Scheduler Profiles

# Configuring Kubernetes Scheduler Profiles (KCNA)
## 1. Why Scheduler Profiles Exist
The Kubernetes scheduler decides **which Pod goes to which Node**.
Originally, Kubernetes had:
- One scheduler binary
- One fixed scheduling behavior (default scheduler)
From **Kubernetes v1.18**, the scheduler gained a **Scheduling Framework** that allows:
- Multiple **scheduler profiles**
- Each profile behaving like an **independent scheduler**
- All profiles running inside **one scheduler binary**
This avoids:
- Running multiple scheduler processes
- Race conditions
- Extra operational overhead
---
## 2. Pod Scheduling Example (Problem Setup)
### Pod Definition
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
spec:
  priorityClassName: high-priority
  containers:
    - name: simple-webapp-color
      image: simple-webapp-color
      resources:
        requests:
          memory: "1Gi"
          cpu: 10
```
### Key Observations
- Pod requests **10 CPU units**
- Pod has **high priority**
- Scheduler must find a node with **≥ 10 CPU available**

---
## 3. PriorityClass and Scheduling Queue
### PriorityClass Definition
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
globalDefault: false
description: "This priority class should be used for XYZ service pods only."
```
### What Priority Does
- Pods enter the **scheduling queue**    
- Pods are **sorted by priority**    
- Higher priority Pods are scheduled first    
- Lower priority Pods may be:    
    - Delayed        
    - Preempted (CKA level concept)        
### Important Term
- **queueSort plugin** handles priority ordering
---
## 4. The Three Scheduling Phases (Very Important)
Every Pod scheduling attempt goes through **three phases**.

---
### Phase 1: Filter Phase
Purpose:
- Remove nodes that **cannot run the Pod**    

Examples of filtering:
- Not enough CPU    
- Node is unschedulable    
- Node taints not tolerated    

In our case:
- Nodes with < 10 CPU are filtered out
### Key Plugin
- **NodeResourcesFit**    
- **NodeUnschedulable**    

---
### Phase 2: Scoring Phase
Purpose:
- Rank remaining nodes    
- Choose the “best” node    

Example:
- Node A: 2 CPU left after scheduling    
- Node B: 6 CPU left after scheduling    
- Node B gets higher score    

Scoring is **relative**, not absolute.
### Key Plugins
- **NodeResourcesFit** (scoring logic)    
- **ImageLocality**    

---
### Phase 3: Binding Phase
Purpose:
- Bind the Pod to the chosen node    
- Write binding decision to the API server    
### Key Plugin
- **DefaultBinder**    

Once binding is complete:
- Kubelet on that node creates the Pod    

---
## 5. Node Unschedulable Example
If a node is marked unschedulable:
`kubectl describe node controlplane`

Output:
```scss
Taints: node.kubernetes.io/unschedulable:NoSchedule
Unschedulable: true
```

Effect:
- **NodeUnschedulable plugin** filters this node out
- Pod will never be scheduled there

---
## 6. Scheduler Plugins and Extension Points
The scheduler is **plugin-based**.
Each scheduling stage has **extension points**:

| Stage     | Extension Point                                                                  |
| --------- | -------------------------------------------------------------------------------- |
| Queue     | queueSort                                                                        |
| Filtering | preFilter, filter, postFilter, NodeResourcesFit, **NodeName, NodeUnschedulable** |
| Scoring   | preScore, score, reserve, **NodeResourcesFit, ImageLocality**                    |
| Binding   | reserve, preBind, bind, postBind                                                 |
Plugins can be:
- Enabled    
- Disabled    
- Replaced    
- Custom-written    
This design enables **scheduler profiles**.
---
## 7. What Is a Scheduler Profile?
A **scheduler profile** is:
- A named scheduling behavior    
- Defined inside the scheduler configuration    
- Selected using `schedulerName` in Pod spec    
Each profile:
- Uses its own plugin configuration    
- Acts like a separate scheduler    
- Runs inside the same binary    
---
## 8. Multiple Scheduler Profiles Example
### Default Scheduler Profile
```yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
- schedulerName: default-scheduler
```
### Custom Scheduler Profiles
```yaml
profiles:
- schedulerName: my-scheduler
- schedulerName: my-scheduler-2
```
Pods choose a profile using:
`schedulerName: my-scheduler`

---
## 9. Customizing Plugins Per Profile
### Disable One Plugin, Enable Custom Ones
```yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
- schedulerName: my-scheduler-2
  plugins:
    score:
      disabled:
        - name: TaintToleration
      enabled:
        - name: MyCustomPluginA
        - name: MyCustomPluginB
```
Meaning:
- TaintToleration scoring is disabled
- Custom scoring logic is used
---
### Disable All Scoring Plugins
```yaml
profiles:
- schedulerName: my-scheduler-3
  plugins:
    preScore:
      disabled:
        - name: "*"
    score:
      disabled:
        - name: "*"
```

Meaning:
- Scheduler performs filtering    
- No scoring logic    
- First acceptable node may be chosen    

---
### Default Behavior Profile
```yaml
profiles:
- schedulerName: my-scheduler-4
```

Meaning:
- Uses all default plugins
- Same logic as default scheduler
- Different name only

---
## 10. Why Scheduler Profiles Matter (Exam Perspective)
### Advantages
- No need to run multiple scheduler binaries    
- Safer and cleaner than multiple schedulers    
- Fine-grained control over scheduling logic    
- Preferred modern approach    

### KCNA Focus
- Understand:    
    - Scheduling phases        
    - Plugin roles        
    - Purpose of scheduler profiles        
- Do NOT need to write custom plugins
### CKA Focus
- Troubleshooting scheduling    
- Understanding plugin behavior    
- Choosing correct schedulerName    

---
## 11. Key Comparison Summary

|Feature|Multiple Schedulers|Scheduler Profiles|
|---|---|---|
|Binary|Multiple|Single|
|Configuration|Separate|Unified|
|Risk|Higher|Lower|
|Introduced|Older|Kubernetes 1.18+|
|Preferred|No|Yes|

---
## 12. One-Page Mental Revision
- Scheduler sorts Pods using **priority**    
- Filters nodes using **resource and taint checks**    
- Scores remaining nodes    
- Binds Pod using **DefaultBinder**    
- Plugins define scheduler behavior    
- Scheduler profiles allow multiple behaviors in one scheduler    
- Pods select scheduler using `schedulerName`
---