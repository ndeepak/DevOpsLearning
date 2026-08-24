# Autoscaling in Kubernetes
Autoscaling is an important part of **Application Lifecycle Management** and is especially relevant for CKA. The most important thing is to clearly distinguish:
1. **Scaling Pods**
2. **Scaling Nodes**
3. **Horizontal scaling**
4. **Vertical scaling**
5. **HPA**
6. **VPA**
7. **Cluster Autoscaler**

---
# 1. What Does Scaling Mean?
Imagine your application currently has:
```
Application
    |
    +-- Pod 1
```
If traffic increases, Pod 1 might become overloaded.
You have two basic choices.
## Horizontal Scaling
Add more Pods:
```
Application
    |
    +-- Pod 1
    +-- Pod 2
    +-- Pod 3
```

You increased the **number of instances**.
This is:
> Horizontal scaling = scale out/in
## Vertical Scaling
Give the existing Pod more resources:
```
Before:
Pod
CPU:    500m
Memory: 512Mi


After:
Pod
CPU:    1
Memory: 1Gi
```
You increased the resources assigned to the workload.
This is:
> Vertical scaling = scale up/down

---

# 2. Kubernetes Has Two Different Things You Can Scale
This is where beginners often get confused.
You can scale:
```scss
                    Kubernetes Cluster
                           |
             +-------------+-------------+
             |                           |
          Nodes                       Workloads
        (Infrastructure)              (Pods)
```
Therefore, there are two different scaling areas.

---

# 3. Scaling the Cluster Infrastructure
Suppose you have:
```
Cluster
Node 1
Node 2
Node 3
```

You can horizontally scale the cluster:
```
Node 1
Node 2
Node 3
Node 4
Node 5
```

You added more nodes.
This is:
> Cluster horizontal scaling

The component commonly associated with automatically adding/removing nodes is the:
> **Cluster Autoscaler**

---

# 4. Vertical Scaling of Nodes
You could also increase resources on a node.
Before:
```
Node 1
CPU:    4 cores
Memory: 16 GiB
```

After:
```
Node 1
CPU:    8 cores
Memory: 32 GiB
```

This is:
> Cluster vertical scaling

In Kubernetes environments, adding another node is often operationally preferable to modifying an existing node, depending on the infrastructure.

---

# 5. Scaling Workloads
Now consider:
```
Node 1
 |
 +-- Pod
 +-- Pod
 +-- Pod
```
You can scale the workload horizontally:
```
Before:
3 Pods

After:
6 Pods
```

This is:
> Horizontal Pod Autoscaling — HPA

Or you can increase the resource requests/limits of the Pods:
```
Pod
CPU:    500m → 1
Memory: 512Mi → 1Gi
```

This is:
> Vertical Pod Autoscaling — VPA

---

# 6. The Four Main Concepts
Memorize this table:

|Target|Horizontal|Vertical|
|---|---|---|
|Cluster|Add/remove Nodes|Increase/decrease Node resources|
|Workload|Add/remove Pods|Increase/decrease Pod resources|

Then:
```
Cluster Horizontal
        ↓
Cluster Autoscaler


Workload Horizontal
        ↓
HPA

Workload Vertical
        ↓
VPA
```

---

# 7. Manual vs Automatic Scaling
Kubernetes supports both.
## Manual
You explicitly tell Kubernetes:
```
kubectl scale ...
```

Example:
```
kubectl scale deployment web --replicas=5
```

Kubernetes changes:
```
2 Pods
  ↓
5 Pods
```

---

# 8. Check the Result
```
kubectl get deployment
```

Example:
```
NAME   READY   UP-TO-DATE   AVAILABLE
web    5/5     5            5
```

Check Pods:
```
kubectl get pods
```
You should see five Pods.

---

# 9. Scaling Back Down
```
kubectl scale deployment web --replicas=2
```

Now:
```
5 Pods
   ↓
2 Pods
```
Kubernetes terminates the excess Pods.

---

# 10. Important: HPA Does Not Create Nodes
This is an important CKA concept.

Suppose:
```
Cluster:
Node 1
Node 2

Workload:
3 Pods
```

HPA detects high CPU and decides:
```
3 Pods → 8 Pods
```

HPA creates more Pods.
It does **not** itself create additional nodes.
The scheduler tries to place the new Pods on existing nodes.

If there isn't enough capacity:
```
HPA
 ↓
More Pods
 ↓
Scheduler
 ↓
Insufficient node capacity
 ↓
Pods Pending
```

If a **Cluster Autoscaler** is configured, it can then add nodes.

Conceptually:
```scss
                High Load
                    |
                    v
                   HPA
                    |
                    v
              More Pods
                    |
                    v
                Scheduler
                    |
             +------+------+
             |             |
       Capacity exists   No capacity
             |             |
             v             v
          Schedule     Pending Pods
                           |
                           v
                   Cluster Autoscaler
                           |
                           v
                       New Node
                           |
                           v
                    Pods scheduled
```

This distinction is extremely important.

---

# 11. What Is HPA?
HPA stands for:
> **Horizontal Pod Autoscaler**

Its job is to automatically adjust the number of Pods belonging to a workload.
For example:
```
Low traffic:

Deployment
   |
   +-- Pod
   +-- Pod
```

High traffic:
```
Deployment
   |
   +-- Pod
   +-- Pod
   +-- Pod
   +-- Pod
   +-- Pod
```

Low traffic again:
```
Deployment
   |
   +-- Pod
   +-- Pod
```

HPA changes the workload's replica count.

---

# 12. HPA Works With Controllers
You normally don't attach HPA directly to an individual Pod.
Instead, HPA targets a scalable workload such as a Deployment.
Conceptually:
```
HPA
 |
 | modifies desired replicas
 v
Deployment
 |
 v
ReplicaSet
 |
 v
Pods
```

---

# 13. Basic HPA Example
Suppose we have:
```
apiVersion: apps/v1
kind: Deployment

metadata:
  name: web

spec:
  replicas: 2

  selector:
    matchLabels:
      app: web

  template:
    metadata:
      labels:
        app: web

    spec:
      containers:
        - name: web
          image: nginx

          resources:
            requests:
              cpu: "100m"
```

Then we can create an HPA.

Using the imperative command:
```
kubectl autoscale deployment web \
  --cpu-percent=70 \
  --min=2 \
  --max=10
```

This means:
```
Minimum Pods = 2
Maximum Pods = 10
Target CPU = 70%
```

Conceptually:
```
             HPA
              |
       CPU target = 70%
              |
       +------+------+
       |             |
   CPU > 70%     CPU < target
       |             |
       v             v
 Scale up         Scale down
```

---

# 14. Check HPA
```
kubectl get hpa
```

Example:
```
NAME   REFERENCE          TARGETS   MINPODS   MAXPODS   REPLICAS
web    Deployment/web     65%/70%   2         10        3
```

You can also use:
```
kubectl describe hpa web
```

This is very useful for troubleshooting.

---

# 15. HPA YAML
Instead of using:
```
kubectl autoscale deployment web \
  --cpu-percent=70 \
  --min=2 \
  --max=10
```

you can define the HPA declaratively.

A modern example:
```
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler

metadata:
  name: web-hpa

spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web

  minReplicas: 2
  maxReplicas: 10

  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

Apply:
```
kubectl apply -f hpa.yaml
```

Check:
```
kubectl get hpa
```

---

# 16. Why CPU Requests Matter for HPA
This is a very important exam concept.

Suppose:
```
resources:
  requests:
    cpu: "100m"
```

and HPA says:
```
target CPU utilization = 70%
```

Suppose a Pod is consuming:
```
70m CPU
```

Then:
```
70m / 100m × 100
=
70%
```

So the Pod is exactly at the target.

If it consumes:
```
100m
```

then:
```
100 / 100 × 100
=
100%
```

HPA sees CPU utilization above the target and may scale out.

---

# 17. Why Resource Requests Are Important
Consider:
```
containers:
  - name: web
    image: nginx
```

There is no CPU request.
Then CPU utilization-based HPA may not work as expected because utilization is calculated relative to resource requests.

Therefore, for CPU-based HPA, a common configuration is:
```
resources:
  requests:
    cpu: "100m"
```

---

# 18. Metrics Server
HPA needs metrics.
A common Kubernetes component used to provide resource metrics is:
> **Metrics Server**

Architecture:
```scss
              HPA
               |
               v
         Metrics API
               |
               v
       Metrics Server
               |
               v
            kubelet
               |
               v
        Node / Containers
```
You can inspect resource usage with:
```
kubectl top nodes
```

and:
```
kubectl top pods
```

If:
```
kubectl top pods
```

doesn't work, check whether Metrics Server is installed and functioning.

---

# 19. HPA Is Not a Monitoring System
This distinction is important.
Metrics Server provides basic resource metrics.
It is not equivalent to a complete monitoring platform such as Prometheus.

Think:
```
Metrics Server
    |
    +-- CPU
    +-- Memory
```
while Prometheus can collect much broader application and system metrics.

For CKA, know Metrics Server especially well because of:
```
kubectl top nodes
kubectl top pods
```
and HPA.

---

# 20. What Is VPA?
VPA stands for:
> **Vertical Pod Autoscaler**

Instead of changing:
```
Number of Pods
```

VPA changes:
```
CPU / Memory resources
```
associated with Pods.

Example:
```
Before:
Pod
CPU request:    100m
Memory request: 128Mi


After:
Pod
CPU request:    500m
Memory request: 512Mi
```

---

# 21. HPA vs VPA
This is one of the most important things to memorize.
### HPA
```
High CPU
   |
   v
More Pods
```

Example:
```
2 Pods → 5 Pods
```

### VPA
```
High resource usage
   |
   v
More resources per Pod
```

Example:
```
100m CPU → 500m CPU
```

Therefore:
```
HPA = More/Fewer Pods

VPA = Bigger/Smaller Pods
```

---

# 22. VPA Example
Suppose:
```
Pod:

CPU request = 100m
Memory request = 128Mi
```

The application consistently needs:
```
CPU = 500m
Memory = 512Mi
```

VPA can recommend or apply larger resource requests.

Conceptually:
```
                  VPA
                   |
           Resource analysis
                   |
          +--------+--------+
          |                 |
         CPU              Memory
          |                 |
        500m              512Mi
```

---

# 23. VPA Components
VPA is generally deployed as a set of components, including:
```
VPA Recommender
VPA Updater
VPA Admission Controller
```

Their roles are roughly:
### Recommender
Determines appropriate resource recommendations.
```
Usage data
    ↓
Recommender
    ↓
CPU/Memory recommendation
```

### Updater
Determines which Pods need to be restarted to apply new recommendations, depending on configuration.
### Admission Controller
Applies recommended resource values when Pods are admitted.

---

# 24. VPA Modes
VPA has several important modes.
## `Off`

VPA only provides recommendations.
```
Usage
  ↓
VPA
  ↓
Recommendation
```
It doesn't automatically modify Pods.
Useful for observing recommendations.

---

## `Initial`
Recommendations are applied when a Pod is initially created.
```
Pod creation
     ↓
VPA recommendation
     ↓
Pod receives resources
```

Existing Pods aren't continuously updated just because recommendations change.

---

## `Recreate`
VPA may evict/recreate Pods so that updated resource recommendations can be applied.
Conceptually:
```
Existing Pod
     ↓
VPA determines new resources
     ↓
Pod recreated
     ↓
New resource configuration
```

This can cause disruption, so workload availability considerations matter.

---

## `InPlaceOrRecreate`
In newer Kubernetes/VPA environments, VPA can use in-place resource updates when supported, otherwise recreate the Pod.
For CKA, understand the concept rather than memorizing a particular cluster's VPA implementation details.

---

# 25. HPA vs VPA Table

|Feature|HPA|VPA|
|---|---|---|
|Full name|Horizontal Pod Autoscaler|Vertical Pod Autoscaler|
|Changes|Pod count|Pod resources|
|CPU-based scaling|Yes|Yes|
|Memory-based resource adjustment|Not its primary role|Yes|
|Adds Pods|Yes|No|
|Increases CPU request|No|Yes|
|Increases memory request|No|Yes|
|Main purpose|Scale out/in|Scale up/down|

The easiest memory trick:
```
H = Horizontal = More Pods

V = Vertical = Bigger Pods
```

---

# 26. HPA and VPA Together?
This requires care.
Suppose both HPA and VPA are trying to control CPU utilization.
You can get competing behavior.

For example:
```
HPA:
"CPU is high. Add Pods."

VPA:
"CPU per Pod is high. Increase CPU request."
```

Changing CPU requests changes the denominator used for CPU utilization, which can affect HPA behavior.

Therefore, blindly using HPA and VPA together on the same CPU metric can produce undesirable interactions.

For CKA, remember:
> HPA and VPA should be designed carefully when they operate on the same resource metrics.

---

# 27. Cluster Autoscaler
Now we need to distinguish another autoscaler.
Cluster Autoscaler deals with:
```
Nodes
```
not directly with Pod replicas.
Suppose:
```
Node 1
Node 2
```
are full.

A Deployment scales:
```
3 Pods → 10 Pods
```

Some Pods cannot be scheduled:
```
Pod 7 → Pending
Pod 8 → Pending
Pod 9 → Pending
Pod 10 → Pending
```

Cluster Autoscaler can detect that the cluster needs additional capacity and add nodes when the infrastructure/provider supports it.

Architecture:
```scss
                HPA
                 |
                 v
             More Pods
                 |
                 v
             Scheduler
                 |
          +------+------+
          |             |
       Capacity       No capacity
       available          |
          |               v
          |          Pending Pods
          |               |
          |               v
          |       Cluster Autoscaler
          |               |
          |               v
          |           New Nodes
          |               |
          +-------<-------+
```

---

# 28. Three Autoscaling Components
Memorize:
```
HPA
 |
 +-- Pods


VPA
 |
 +-- Pod resources


Cluster Autoscaler
 |
 +-- Nodes
```

This is probably the most useful autoscaling diagram for CKA.

---

# 29. Manual Scaling vs Autoscaling
### Manual
```
kubectl scale deployment web --replicas=5
```

You decide:
```
replicas = 5
```

### HPA
You specify:
```
min = 2
max = 10
target CPU = 70%
```
Kubernetes determines the replica count.

---

# 30. `kubectl edit`
Manual vertical scaling can be done by modifying resource requests/limits:

```
kubectl edit deployment web
```

Find:
```
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
```

Change to:
```
resources:
  requests:
    cpu: "500m"
    memory: "512Mi"
```

However, remember that changing Pod template resources causes Pods to be recreated because the Pod template changes.

---

# 31. Important Difference: Requests vs Limits
For autoscaling, don't confuse:
```
requests
```

with:
```
limits
```

Example:
```
resources:
  requests:
    cpu: "250m"
    memory: "256Mi"

  limits:
    cpu: "500m"
    memory: "512Mi"
```

Think:
```
request = amount Kubernetes uses for scheduling/resource accounting

limit = maximum resource boundary imposed on the container
```
For CPU-utilization-based HPA, the CPU request is particularly important.

---

# 32. HPA Example From Start to Finish
Let's build a simple workload.
## Step 1: Deployment
```
apiVersion: apps/v1
kind: Deployment

metadata:
  name: web

spec:
  replicas: 2

  selector:
    matchLabels:
      app: web

  template:
    metadata:
      labels:
        app: web

    spec:
      containers:
        - name: web
          image: nginx

          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"

            limits:
              cpu: "500m"
              memory: "256Mi"
```

Apply:
```
kubectl apply -f deployment.yaml
```

Check:
```
kubectl get deployment
```

---

# 33. Step 2: Check Metrics
```
kubectl top pods
```

Example:
```
NAME                    CPU(cores)   MEMORY(bytes)
web-abc123              20m          30Mi
web-def456              25m          31Mi
```

If this command fails, investigate Metrics Server.

---

# 34. Step 3: Create HPA
```
kubectl autoscale deployment web \
  --cpu-percent=70 \
  --min=2 \
  --max=10
```

Check:
```
kubectl get hpa
```

You might see:
```
NAME   TARGETS   MINPODS   MAXPODS   REPLICAS
web    25%/70%   2         10        2
```

---

# 35. Step 4: Increased Load
Suppose CPU increases:
```
CPU = 90%
```

HPA sees:
```
90% > 70%
```
and increases replicas.

```
2 Pods
   ↓
3 Pods
   ↓
4 Pods
```
depending on the calculated desired replica count and HPA behavior.

---

# 36. Step 5: Load Decreases
Suppose CPU falls:
```
30%
```

HPA can reduce replicas toward the configured minimum, subject to its scaling behavior and stabilization rules.
```
4 Pods
   ↓
3 Pods
   ↓
2 Pods
```

---

# 37. HPA Is Controller-Based
This is a fundamental Kubernetes concept.
HPA continuously compares:
```
Current state
```

against:
```
Desired state
```

Example:
```
Desired CPU = 70%

Current CPU = 90%
```

Difference:
```
Current > Desired
```

Therefore:
```
Scale up
```

If:
```
Current CPU = 30%
Desired CPU = 70%
```

then:
```
Scale down
```

This follows the general Kubernetes reconciliation model.

---

# 38. HPA Does Not Immediately Scale Every Second
Don't think:
```
CPU = 71%
→ immediately create one Pod
```

HPA uses control-loop timing, metrics collection, stabilization, and scaling behavior.

The exact response depends on Kubernetes/HPA configuration and version.

For the exam, understand:

```
Metrics
   ↓
HPA controller
   ↓
Calculate desired replicas
   ↓
Update target workload
   ↓
Deployment/ReplicaSet
   ↓
Pods
```

---

# 39. Useful HPA Commands
Create:
```
kubectl autoscale deployment web \
  --cpu-percent=70 \
  --min=2 \
  --max=10
```

List:
```
kubectl get hpa
```

Detailed:
```
kubectl describe hpa web
```

YAML:
```
kubectl get hpa web -o yaml
```

Delete:
```
kubectl delete hpa web
```

---

# 40. Troubleshooting HPA
If HPA isn't scaling, don't immediately assume HPA is broken.

Check:
```
kubectl get hpa
```

Then:
```
kubectl describe hpa web
```

Check metrics:
```
kubectl top pods
```

Check Deployment:
```
kubectl get deployment web
```

Check Pods:
```
kubectl get pods
```

Check resource requests:
```
kubectl get deployment web -o yaml
```

Check events:
```
kubectl describe deployment web
```

You want to investigate:
```
Metrics available?
       ↓
Resource requests configured?
       ↓
HPA targeting correct workload?
       ↓
Current replicas within min/max?
       ↓
Pods healthy?
       ↓
Enough cluster capacity?
```

---

# 41. Common CKA Traps
## Trap 1
Question:
> Automatically increase the number of Pods when CPU utilization increases.

Answer:
```
HPA
```
Not VPA.

---

## Trap 2
Question:
> Automatically increase CPU and memory resources assigned to Pods.

Answer:
```
VPA
```
Not HPA.

---

## Trap 3
Question:
> Automatically add nodes when Pods cannot be scheduled because the cluster lacks capacity.

Answer:
```
Cluster Autoscaler
```

---

## Trap 4
Question:
> What command manually changes Deployment replica count?
```
kubectl scale deployment <name> --replicas=<number>
```

---

## Trap 5
Question:
> Which command displays current CPU/memory usage?
```
kubectl top pods
kubectl top nodes
```
This requires resource metrics, commonly provided by Metrics Server.

---

# 42. The Complete Picture
This is the diagram I recommend memorizing for CKA:
```scss
                         Kubernetes Cluster
                                |
                 +--------------+--------------+
                 |                             |
                 v                             v
              Nodes                         Workloads
                 |                             |
                 |                             |
       Cluster Autoscaler              +-------+-------+
                 |                      |               |
                 v                      v               v
          Add/Remove Nodes             HPA             VPA
                                        |               |
                                        v               v
                                  Pod count       Pod resources
                                        |               |
                                        v               v
                                   More/Fewer      More/Less
                                      Pods          CPU/Memory
```

---

# 43. Scaling Cheat Sheet
```
HORIZONTAL
==========
More instances.

Workload:
2 Pods → 5 Pods

Tool:
HPA
```

```
VERTICAL
========
More resources per instance.

Pod:
100m CPU → 500m CPU

Tool:
VPA
```

```
CLUSTER HORIZONTAL
==================
More nodes.

Node:
3 → 5 nodes

Tool:
Cluster Autoscaler
```

---

# 44. CKA Commands to Know
### Manual horizontal scaling
```
kubectl scale deployment nginx --replicas=5
```

### Check workloads
```
kubectl get deployments
kubectl get pods
```

### Check resource usage
```
kubectl top pods
kubectl top nodes
```

### Create HPA
```
kubectl autoscale deployment nginx \
  --cpu-percent=70 \
  --min=2 \
  --max=10
```

### Check HPA
```
kubectl get hpa
```

### Detailed HPA information
```
kubectl describe hpa nginx
```

### HPA YAML
```
kubectl get hpa nginx -o yaml
```

### Edit workload resources
```
kubectl edit deployment nginx
```

---

# 45. Final Mental Model
When you see **autoscaling**, ask one question:
> **What exactly am I trying to make bigger or smaller?**

### More Pods?
```
HPA
```

### Bigger Pods?
```
VPA
```

### More Nodes?
```
Cluster Autoscaler
```

### Manually change number of Pods?
```
kubectl scale
```

### Manually change resource requests/limits?
```
kubectl edit
```

And the overall relationship is:
```scss
                         LOAD
                           |
                           v
                    Metrics / Monitoring
                           |
                           v
              +------------+------------+
              |                         |
              v                         v
             HPA                       VPA
              |                         |
       Change replica count       Change resources
              |                         |
              v                         v
            Pods                    Pods
              |
              v
        Scheduler checks
        available capacity
              |
       +------+------+
       |             |
       v             v
   Capacity       No capacity
   available          |
       |              v
       |       Cluster Autoscaler
       |              |
       |              v
       |         New Nodes
       |              |
       +------+-------+
              |
              v
         Pods scheduled
```

For **CKA**, the highest-priority things to master are **HPA, Metrics Server, `kubectl top`, resource requests, `kubectl autoscale`, HPA YAML, `kubectl describe hpa`, manual `kubectl scale`, and the distinction between HPA, VPA, and Cluster Autoscaler**.