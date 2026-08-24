# Horizontal Pod Autoscaler (HPA)
## 1. What problem does HPA solve?
Suppose you have:
```
                    Traffic
                       |
                       v
                +-------------+
                |   Service   |
                +-------------+
                       |
             +---------+---------+
             |         |         |
             v         v         v
           Pod 1     Pod 2     Pod 3
```
You initially have 3 Pods.

During normal traffic:
```
CPU usage = 20%
```

During heavy traffic:
```
CPU usage = 90%
```

If you manually scale:
```
kubectl scale deployment my-app --replicas=10
```
someone has to monitor the application and execute the command.

HPA automates this:
```scss
                  Metrics Server
                       |
                       v
                CPU / Memory data
                       |
                       v
                +-------------+
                |     HPA     |
                +-------------+
                       |
                 desired replicas
                       |
                       v
                +-------------+
                | Deployment  |
                +-------------+
                       |
              +--------+--------+
              |        |        |
              v        v        v
             Pods     Pods     Pods
```

So:
> **HPA automatically changes the number of Pods based on observed metrics.**

---

# 2. Horizontal vs Vertical Scaling
This is extremely important.

## Horizontal scaling
Increase/decrease the number of Pods.

```
Before:

Pod  Pod  Pod
 |    |    |
 +----+----+

3 Pods
```

After:
```
Pod Pod Pod Pod Pod Pod
 |   |   |   |   |   |

6 Pods
```

Command:
```
kubectl scale deployment my-app --replicas=6
```
HPA performs this automatically.

---

# 3. Vertical scaling
Instead of adding Pods, increase resources assigned to existing Pods.
For example:
```
resources:
  requests:
    cpu: "250m"
    memory: "256Mi"
  limits:
    cpu: "1"
    memory: "512Mi"
```

You might increase:
```
requests:
  cpu: "500m"
  memory: "512Mi"
```

The number of Pods doesn't necessarily change.
So:
```
Horizontal:
3 Pods -> 6 Pods


Vertical:
250m CPU -> 500m CPU
```

For CKA:
```
HPA = Horizontal Pod Autoscaler
    = changes replica count
```

---

# 4. What does HPA actually control?
HPA doesn't directly create Pods.
It modifies the workload's desired replica count.
For example:
```
HPA
 |
 | desiredReplicas = 5
 v
Deployment
 |
 v
ReplicaSet
 |
 v
5 Pods
```

This is an important Kubernetes architecture concept.

Suppose:
```
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 2
```

HPA might determine that 5 replicas are required.
Conceptually:
```
HPA:
"Application needs 5 Pods"
        |
        v
Deployment:
replicas = 5
        |
        v
ReplicaSet:
creates 5 Pods
```

---

# 5. HPA requires metrics
HPA needs information about application resource usage.
For example:
```
Pod 1 -> CPU 70%
Pod 2 -> CPU 80%
Pod 3 -> CPU 60%
```
Where does this information come from?
Typically:
```
kubelet
   |
   v
Metrics Server
   |
   v
Kubernetes Metrics API
   |
   v
HPA
```
Metrics Server collects resource usage from nodes and Pods.

You can inspect metrics using:
```
kubectl top nodes
```

and:
```
kubectl top pods
```

Example:
```
NAME       CPU(cores)   MEMORY(bytes)
my-app     450m         350Mi
```

If:
```
kubectl top pods
```
doesn't work, HPA may also be unable to obtain resource metrics.

Check:
```
kubectl get deployment metrics-server -n kube-system
```

and:
```
- [ ] kubectl get apiservice | gmonmmomonrep metrics
```

You can also test:
```
kubectl top pod
```

---

# 6. Very important: CPU utilization is based on requests
This is one of the most important HPA concepts for the CKA.

Consider:
```
resources:
  requests:
    cpu: "250m"

  limits:
    cpu: "500m"
```

Suppose the Pod is consuming:
```
CPU = 125m
```

CPU utilization is:
```
125m / 250m × 100
= 50%
```

Notice:
```
125m / 250m
```

not:
```
125m / 500m
```

For CPU utilization-based HPA, the utilization percentage is calculated relative to the container's **CPU request**.

So if:
```
request = 250m
usage  = 200m
```

then:
```
200 / 250 × 100 = 80%
```

If HPA target is:
```
50%
```
then the workload is above target.

---

# 7. Why CPU requests matter
Suppose:
```
resources:
  requests:
    cpu: "250m"
```

Actual usage:
```
200m
```

Utilization:
```
200 / 250 = 80%
```

Now change the request:
```
resources:
  requests:
    cpu: "500m"
```

Same actual usage:
```
200m
```

Now:
```
200 / 500 = 40%
```

Same application.

Same CPU consumption.

But HPA sees:
```
80% -> 40%
```
because the CPU request changed.

Therefore:
> For CPU-utilization HPA, CPU requests are critical.

---

# 8. Basic Deployment
Let's create a proper example.
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 1

  selector:
    matchLabels:
      app: my-app

  template:
    metadata:
      labels:
        app: my-app

    spec:
      containers:
        - name: my-app
          image: nginx

          resources:
            requests:
              cpu: "250m"
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

```
kubectl get pods
```

Check CPU:
```
kubectl top pods
```

---

# 9. Create HPA imperatively
The traditional command is:
```
kubectl autoscale deployment my-app \
  --cpu-percent=50 \
  --min=1 \
  --max=10
```

This means:
```
Target CPU utilization = 50%

Minimum Pods = 1

Maximum Pods = 10
```

Check:
```
kubectl get hpa
```

Example:
```
NAME     REFERENCE           TARGETS   MINPODS   MAXPODS   REPLICAS
my-app   Deployment/my-app   30%/50%   1         10        1
```

Interpret this as:
```
Current CPU = 30%
Target CPU  = 50%

Current replicas = 1
Min replicas     = 1
Max replicas     = 10
```

---

# 10. Declarative HPA
For modern Kubernetes, understand `autoscaling/v2`.
```
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler

metadata:
  name: my-app-hpa

spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app

  minReplicas: 1
  maxReplicas: 10

  metrics:
    - type: Resource

      resource:
        name: cpu

        target:
          type: Utilization
          averageUtilization: 50
```

Apply:
```
kubectl apply -f hpa.yaml
```

Check:
```
kubectl get hpa
```

Detailed:
```
kubectl describe hpa my-app-hpa
```

---

# 11. Understand every field
Let's break this down.
```
apiVersion: autoscaling/v2
```

HPA API version.
For current Kubernetes clusters, `autoscaling/v2` is the important version to know.
```
kind: HorizontalPodAutoscaler
```
Tells Kubernetes this object is an HPA.

---

```
scaleTargetRef:
```
This tells HPA:
> Which workload should I scale?

Example:
```
scaleTargetRef:
  apiVersion: apps/v1
  kind: Deployment
  name: my-app
```

Meaning:
```
HPA
 |
 +----> Deployment/my-app
```

```
minReplicas: 1
```

HPA will not scale below:
```
1 Pod
```

```
maxReplicas: 10
```

HPA will not scale above:
```
10 Pods
```

```
metrics:
```
Defines what HPA should monitor.
Here:
```
type: Resource
```
means Kubernetes resource metrics.

Then:
```
name: cpu
```
means CPU.

And:
```
target:
  type: Utilization
  averageUtilization: 50
```

means:
```
Maintain average CPU utilization around 50%.
```

---

# 12. How HPA calculates replicas
This is an excellent CKA concept.
A simplified formula is:
```
desired replicas =
current replicas × current metric / desired metric
```

Suppose:
```
Current replicas = 2

Current CPU = 80%

Target CPU = 50%
```

Then:
```
desired replicas
= 2 × 80 / 50
= 3.2
```

Kubernetes needs an integer number of replicas, so it will move toward:
```
4 replicas
```

Conceptually:
```
2 Pods
  |
  | CPU = 80%
  |
  v
HPA
  |
  | target = 50%
  |
  v
More Pods
  |
  v
4 Pods
```

The actual controller behavior includes rounding and stabilization behavior, so don't treat this as a promise that every situation immediately produces exactly that number.

For the exam, understand the relationship:
```
current usage > target
        |
        v
increase replicas
```

and:
```
current usage < target
        |
        v
decrease replicas
```
subject to min/max and HPA behavior.

---

# 13. Example
Suppose:
```
Deployment:

replicas = 2
```

Each Pod:
```
CPU request = 250m
```

Usage:
```
Pod 1 = 200m
Pod 2 = 200m
```

Utilization:
```
200 / 250 × 100
= 80%
```

Average:
```
80%
```

HPA target:
```
50%
```

Therefore:
```
80% > 50%
```

HPA increases replicas.

Eventually:
```
2 -> 4 -> ...
```

until the observed utilization approaches the target, subject to HPA limits and timing.

---

# 14. Scaling down
Suppose:
```
replicas = 6
```
and traffic decreases.

CPU becomes:
```
10%
```

while target is:
```
50%
```

Then:
```
10% < 50%
```
HPA can reduce replicas.

For example:
```
6
|
v
4
|
v
2
|
v
1
```
But Kubernetes does not necessarily scale down instantly. HPA has stabilization and timing behavior to prevent rapid oscillation.

This is important in real systems:
```
Traffic spikes
    |
    v
Scale up

Traffic drops for a short time
    |
    v
Don't immediately destroy Pods

Traffic remains low
    |
    v
Scale down
```

This avoids constant:
```
1 -> 10 -> 1 -> 10 -> 1
```
behavior.

---

# 15. HPA with memory
HPA can also use memory.
Example:
```
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app

  minReplicas: 2
  maxReplicas: 10

  metrics:
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 70
```
Now HPA monitors memory utilization.

---

# 16. CPU AND memory together
You can specify multiple metrics:
```
metrics:

  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50

  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 70
```

The important behavior is:
> HPA evaluates all configured metrics and chooses the highest required replica count.

For example:
```
CPU requires:    4 Pods
Memory requires: 6 Pods

HPA chooses:     6 Pods
```

Why?
Because scaling to 4 would satisfy CPU but not memory.

---

# 17. HPA with Pods
`autoscaling/v2` also supports Pods metrics.
For example:
```
metrics:
  - type: Pods
    pods:
      metric:
        name: requests_per_second

      target:
        type: AverageValue
        averageValue: "100"
```

Conceptually:
```
Pod 1 -> 120 requests/sec
Pod 2 -> 100 requests/sec
Pod 3 -> 110 requests/sec

Average = 110 requests/sec
```

Target:
```
100 requests/sec
```
HPA may increase replicas.

---

# 18. Resource vs Pods vs Object vs External
For CKA/CKS, recognize these HPA metric types:
```
Resource
Pods
Object
External
```
### Resource
CPU/memory.
```
type: Resource
```

Example:
```
name: cpu
```
### Pods
A metric associated with each Pod.
```
type: Pods
```

Examples might include:
```
requests_per_second
queue_depth_per_pod
```
### Object
A metric associated with another Kubernetes object.
```
type: Object
```

For example:
```
Ingress
Service
```
### External
Metrics outside the normal Kubernetes resource metrics.

```
type: External
```

Examples:
```
cloud queue length
external API requests
message queue depth
```

These generally require an appropriate metrics adapter/provider.

# 19. Metrics Server vs Prometheus
This distinction is important for CKA/CKS.
### Metrics Server
Primarily provides basic resource metrics:
```
CPU
Memory
```

Used by:
```
kubectl top
```

and commonly by:
```
HPA
```

Architecture:
```
kubelet
   |
   v
Metrics Server
   |
   v
Metrics API
   |
   +----> kubectl top
   |
   +----> HPA
```

### Prometheus
Prometheus is a much more comprehensive monitoring system.
It can collect application-specific metrics such as:
```
HTTP requests/sec
HTTP error rate
queue depth
latency
business metrics
```
HPA can use custom/external metrics through appropriate adapters/integrations.

For the exam, don't confuse:
```
Metrics Server
```

with:
```
Prometheus
```

---

# 20. Check whether Metrics Server works
First:
```
kubectl top nodes
```

Then:
```
kubectl top pods
```

If successful, you'll get something like:
```
NAME       CPU(cores)   MEMORY(bytes)
my-app     125m         128Mi
```

You can inspect:
```
kubectl get pods -n kube-system
```

Look for:
```
metrics-server
```

Then:
```
kubectl get apiservice
```
You should see the metrics API.

---

# 21. Important HPA commands
Know these.

Create HPA:
```
kubectl autoscale deployment my-app \
  --cpu-percent=50 \
  --min=1 \
  --max=10
```

List:
```
kubectl get hpa
```

Short form:
```
kubectl get hpa
```

Detailed:
```
kubectl describe hpa my-app
```

Watch:
```
kubectl get hpa -w
```

Delete:
```
kubectl delete hpa my-app
```

Check deployment:
```
kubectl get deployment my-app
```

Check Pods:
```
kubectl get pods
```

Check metrics:
```
kubectl top pods
```

---

# 22. Very useful troubleshooting sequence
Suppose HPA says:
```
TARGETS: <unknown>/50%
```
Don't immediately assume HPA itself is broken.

Work through the dependency chain.
### Step 1
Check HPA:
```
kubectl get hpa
```

### Step 2
Describe it:
```
kubectl describe hpa my-app
```

Look at:
```
Events
Conditions
Metrics
```

### Step 3
Check Metrics Server:
```
kubectl get pods -n kube-system
```

### Step 4
Test metrics:
```
kubectl top pods
```

### Step 5
Check resource requests.
For CPU utilization HPA:
```
resources:
  requests:
    cpu: "250m"
```
is important.

### Step 6
Check the target:
```
kubectl get hpa my-app -o yaml
```

### Step 7
Check the target workload:
```
kubectl get deployment my-app
```

---

# 23. HPA does not create nodes
This is another common exam trap.
Suppose:
```
HPA wants:
10 Pods
```

But your cluster only has enough capacity for:
```
6 Pods
```
HPA does not add nodes.
You can end up with:
```
HPA
 |
 | wants 10 Pods
 v
Deployment
 |
 v
10 Pods requested
 |
 +---- 6 Running
 |
 +---- 4 Pending
```

A separate component called:
```
Cluster Autoscaler
```
can add nodes.
So remember:
```
HPA
 |
 +---- scales Pods


Cluster Autoscaler
 |
 +---- scales Nodes
```

---

# 24. HPA vs VPA vs Cluster Autoscaler
Memorize this table.

|Component|Scales|Direction|
|---|---|---|
|HPA|Pods|Horizontal|
|VPA|Pod resources|Vertical|
|Cluster Autoscaler|Nodes|Horizontal|
|Manual `kubectl scale`|Pods|Horizontal|

Conceptually:
```scss
                 Kubernetes Cluster
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
        HPA            VPA       Cluster Autoscaler
          |             |             |
          v             v             v
       Pods count    Pod CPU/       Nodes
                     memory
```

---

# 25. HPA vs Deployment replicas
This is important.
You may have:
```
spec:
  replicas: 3
```

and HPA:
```
minReplicas: 2
maxReplicas: 10
```
The HPA controls the target's replica count.

Therefore, manually doing:
```
kubectl scale deployment my-app --replicas=5
```

while HPA is managing the Deployment can lead to confusing behavior because HPA will continue reconciling the replica count according to its metrics.

Think of it as:
```
Deployment
    ^
    |
    | controlled by
    |
   HPA
```

---

# 26. Complete CKA-style example
Create the Deployment:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 1

  selector:
    matchLabels:
      app: web

  template:
    metadata:
      labels:
        app: web

    spec:
      containers:
        - name: nginx
          image: nginx:latest

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
kubectl apply -f web.yaml
```

Check:
```
kubectl get deployment
kubectl get pods
```

Check metrics:
```
kubectl top pods
```

Create HPA:
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

  minReplicas: 1
  maxReplicas: 10

  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```

Apply:
```
kubectl apply -f hpa.yaml
```

Check:
```
kubectl get hpa
```

Then:
```
kubectl describe hpa web-hpa
```

Watch:
```
kubectl get hpa -w
```

---

# 27. What you should know for the CKA exam
If you see an HPA task, your mental checklist should be:
```
1. What workload am I scaling?
       |
       v
2. Deployment / StatefulSet / ReplicaSet?
       |
       v
3. What metric?
       |
       +---- CPU
       +---- Memory
       +---- Custom
       +---- External
       |
       v
4. What target?
       |
       v
5. Minimum replicas?
       |
       v
6. Maximum replicas?
       |
       v
7. Is Metrics Server available?
       |
       v
8. Does the workload have resource requests?
```

For a basic CPU HPA:
```
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app

  minReplicas: 2
  maxReplicas: 10

  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```
That structure is worth being able to write from memory.

---

# 28. CKA mental model
The entire topic can be reduced to this:
```scss
                    APPLICATION
                         |
                         v
                       Pods
                         |
                  CPU / Memory usage
                         |
                         v
                   Kubelet / Metrics
                         |
                         v
                  Metrics Server
                         |
                         v
                   Metrics API
                         |
                         v
                       HPA
                         |
                  calculates desired
                     replica count
                         |
                         v
                    Deployment
                         |
                         v
                     ReplicaSet
                         |
                         v
                  More / fewer Pods
```

And if those additional Pods don't fit:
```
HPA
 |
 | wants more Pods
 v
Deployment
 |
 v
Pending Pods
 |
 v
Cluster Autoscaler
 |
 v
More Nodes
```

The three most important distinctions to memorize are:
```
HPA
= more/fewer Pods

VPA
= more/fewer CPU/memory resources per Pod

Cluster Autoscaler
= more/fewer Nodes
```

And the most important HPA dependency:
```
CPU/Memory metrics
        |
        v
Metrics Server
        |
        v
HPA
```

Finally, for CPU utilization:
```
CPU utilization
    =
actual CPU usage
-----------------
CPU request
```

not CPU limit. This is one of the details I would make sure you can recall during the CKA exam.