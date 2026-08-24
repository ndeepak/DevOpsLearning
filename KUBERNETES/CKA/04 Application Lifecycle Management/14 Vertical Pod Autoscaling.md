# Vertical Pod Autoscaler (VPA)
## 1. What Problem Does VPA Solve?
Suppose you deploy an application with:
```yaml
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
            limits:
              cpu: "500m"
````

You are telling Kubernetes:
```
CPU request = 250m
CPU limit   = 500m
```

Think of this as:
```
             CPU
              |
              |---- maximum allowed = 500m
              |
              |---- requested/reserved = 250m
              |
              0
```

But what happens if the application actually needs:
```
CPU usage = 800m
```

The CPU limit is only:
```
500m
```
Therefore, the container cannot use more than that CPU limit.

On the other hand, suppose you configure:
```
resources:
  requests:
    cpu: "2"
  limits:
    cpu: "4"
```

but the application normally uses only:
```
100m
```
Now you may have allocated far more CPU than necessary.

This creates two opposite problems:
```
Too little resource
        |
        v
Performance problems
        |
        v
CPU throttling / OOM risk


Too much resource
        |
        v
Wasted cluster capacity
        |
        v
Higher infrastructure cost
```
VPA attempts to find a better resource allocation automatically.

---

# 2. What Does "Vertical" Mean?
There are two fundamental ways to scale workloads.
## Vertical Scaling
Make an existing Pod/container bigger.
```
Before:
Pod
CPU request = 250m
Memory      = 256Mi


After:
Pod
CPU request = 1 CPU
Memory      = 1Gi
```

The number of Pods stays the same.
```
1 Pod
  |
  +-- more CPU
  +-- more memory
```
This is **Vertical Pod Autoscaling**.

---

## Horizontal Scaling
Create more Pods.
```
Before:
Pod 1


After:
Pod 1
Pod 2
Pod 3
Pod 4
```

The individual Pods don't necessarily become larger.
This is **Horizontal Pod Autoscaling**.

---

# 3. Easiest Way to Remember VPA vs HPA
Think about a restaurant.
## HPA
One waiter is overloaded.
Instead of giving that waiter more capability:
```
1 waiter
   |
   v
4 waiters
```
You add more workers.
That's horizontal scaling.
## VPA
Instead, you make the existing worker capable of handling more:
```
small worker
     |
     v
more capable worker
```
That's vertical scaling.

In Kubernetes:
```
HPA → more Pods
VPA → more CPU/memory per Pod
```

---

# 4. Why Does VPA Care About Requests?
This is extremely important.
VPA primarily recommends and manages **resource requests**.

For example:
```
resources:
  requests:
    cpu: 250m
    memory: 256Mi
```

The Kubernetes scheduler uses resource requests when deciding where a Pod can run.

For example:
```
Node A
Capacity = 4 CPU

Already allocated:
3.8 CPU

New Pod requests:
1 CPU
```

The scheduler sees:
```
3.8 + 1 = 4.8 CPU
```

Therefore:
```
Pod cannot fit
```

VPA can help by determining whether the workload actually needs:
```
1 CPU
```

or perhaps:
```
300m
```
and recommend a more appropriate value.

---

# 5. CPU Units
You need to understand Kubernetes CPU notation.
```
1 CPU = 1000m
```

Therefore:
```
100m  = 0.1 CPU
250m  = 0.25 CPU
500m  = 0.5 CPU
750m  = 0.75 CPU
1000m = 1 CPU
2000m = 2 CPU
```

So:
```
requests:
  cpu: "250m"
```

means:
```
0.25 CPU
```

And:
```
maxAllowed:
  cpu: "2"
```

means:
```
2 CPUs
```

---

# 6. Memory Units
You should also understand Kubernetes memory notation.
Example:
```
memory: "256Mi"
```

Common values:
```
128Mi
256Mi
512Mi
1Gi
2Gi
4Gi
```

VPA can adjust both:
```
CPU
Memory
```

For example:
```
resources:
  requests:
    cpu: 250m
    memory: 256Mi
```

VPA might eventually recommend:
```
resources:
  requests:
    cpu: 500m
    memory: 512Mi
```

---

# 7. How Does VPA Know What the Application Needs?
This is where the **VPA Recommender** comes in.
The overall architecture looks like:
```
                  Kubernetes API
                        |
                        |
                 +------v------+
                 | VPA         |
                 | Recommender |
                 +------+------+
                        |
                resource usage
                        |
                        v
               recommendation
                        |
          +-------------+-------------+
          |                           |
          v                           v
 VPA Admission Controller       VPA Updater
          |                           |
          v                           v
   New Pod gets                 Existing Pod
   recommended                  may be evicted
   resources                    and recreated
```

There are three major VPA components:
```
1. Recommender
2. Updater
3. Admission Controller
```

---

# 8. VPA Recommender
The Recommender answers:
> How much CPU and memory should this Pod have?

It observes resource consumption over time and generates recommendations.
For example:
```
Current request:
CPU = 250m
Memory = 256Mi


Observed usage:
CPU:
200m
350m
450m
600m
500m


Memory:
300Mi
350Mi
400Mi
450Mi
```

The Recommender might conclude:
```
Recommended CPU = 750m
Recommended Memory = 512Mi
```

Conceptually:
```
                    VPA Recommender
                           |
             +-------------+-------------+
             |                           |
             v                           v
       CPU recommendation        Memory recommendation
             |                           |
             v                           v
           750m                         512Mi
```

---

# 9. Where Does the Usage Information Come From?
VPA uses Kubernetes resource usage information through the Kubernetes metrics infrastructure.

You may already know:
```
kubectl top pods
```

For example:
```
kubectl top pod
```

Output:
```
NAME       CPU(cores)   MEMORY(bytes)
my-app     450m         350Mi
```
This gives you current usage information.
VPA is more sophisticated than simply looking at one instantaneous number.

It considers resource usage over time and builds recommendations.
Think:
```
Current usage
      +
Historical usage
      +
Usage patterns
      |
      v
VPA recommendation
```

---

# 10. Recommender Does Not Directly Modify Your Pod
This distinction is important.
The Recommender says:
```
"I recommend 750m CPU."
```

It does not necessarily go and modify the running Pod itself.
Another VPA component is responsible for the actual Pod lifecycle changes.

That component is:
# VPA Updater
# 11. VPA Updater
The Updater asks:
> Are there existing Pods whose resource allocation is significantly different from the recommendation?

Suppose:
```
Current:
CPU request = 250m


VPA recommendation:
CPU request = 750m
```

The Updater can determine that the Pod needs updating.

In traditional VPA update behavior:
```
Old Pod
   |
   | VPA Updater
   v
Eviction
   |
   v
Pod terminated
   |
   v
Deployment creates replacement
   |
   v
New Pod
   |
   v
New resource request
```

For example:
```
Old Pod:
CPU request = 250m


New Pod:
CPU request = 750m
```

---

# 12. Why Does VPA Need to Restart Pods?
This is one of the most important VPA concepts.
Historically, a running Pod's container resource configuration could not simply be changed in place.

So:
```
Running Pod
    |
    | change CPU/memory
    X
```

Instead:
```
Running Pod
    |
    v
Evict
    |
    v
Create replacement Pod
    |
    v
Apply new resources
```

That's why VPA can cause disruption.

However, modern Kubernetes has in-place Pod resource resize capabilities.

Therefore, the old blanket statement:
> VPA always has to recreate Pods

is outdated.

The exact behavior depends on:
- Kubernetes version
- VPA version
- In-place resource resize support
- Workload configuration
- VPA configuration

For exam purposes, remember the traditional VPA behavior, but understand the newer in-place resize direction.

---

# 13. VPA Admission Controller
Suppose the VPA Recommender says:
```
Recommended:
CPU = 750m
Memory = 512Mi
```
A new Pod is being created.
The **Admission Controller** intercepts the Pod creation request and can modify the Pod's resource configuration before it is admitted.

Conceptually:
```
Deployment
    |
    v
Create Pod
    |
    v
Admission Controller
    |
    | "VPA recommends 750m CPU"
    |
    v
Modified Pod
    |
    v
Kubernetes API
    |
    v
Scheduler
```

So:
```
Recommender
     |
     | recommendation
     v
Admission Controller
     |
     | mutate new Pod
     v
New Pod with recommended resources
```

---

# 14. The Three Components

|Component|Main Job|
|---|---|
|**Recommender**|Determines appropriate CPU/memory|
|**Updater**|Identifies Pods needing resource updates|
|**Admission Controller**|Applies recommendations to newly created Pods|

Easy way to remember:
```
RECOMMENDER
    ↓
"What should the resources be?"

UPDATER
    ↓
"Which existing Pods need updating?"

ADMISSION CONTROLLER
    ↓
"Apply the recommendation when creating a Pod."
```

---

# 15. Installing VPA
The VPA project provides installation manifests.
Example:
```
kubectl apply -f https://github.com/kubernetes/autoscaler/releases/latest/download/vertical-pod-autoscaler.yaml
```

After installation:
```
kubectl get pods -n kube-system | grep vpa
```

You should see components corresponding to:
```
vpa-recommender
vpa-updater
vpa-admission-controller
```

Depending on the VPA release, exact Pod names and deployment details may differ.

---

# 16. Creating a VPA Object
Example:
```
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler

metadata:
  name: my-app-vpa

spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app

  updatePolicy:
    updateMode: "Auto"

  resourcePolicy:
    containerPolicies:
      - containerName: "my-app"
        minAllowed:
          cpu: "250m"
        maxAllowed:
          cpu: "2"
        controlledResources:
          - cpu
```
Let's break this down.

---

# 17. `apiVersion`
```
apiVersion: autoscaling.k8s.io/v1
```

This tells Kubernetes which API version is being used for the VPA resource.

---

# 18. `kind`
```
kind: VerticalPodAutoscaler
```
You're creating a VPA object.

Similar to:
```
kind: Deployment
```

or:
```
kind: Service
```

---

# 19. `targetRef`
```
targetRef:
  apiVersion: apps/v1
  kind: Deployment
  name: my-app
```

This tells VPA which workload it should manage.

Conceptually:
```
Deployment
    |
    v
my-app
    |
    v
Pods
```

---

# 20. `updatePolicy`
```
updatePolicy:
  updateMode: "Auto"
```

This is one of the most important VPA fields.
It determines whether VPA merely recommends resources or actually changes them.
There are four modes:  `off`, `auto`, `initial` and `recreate`


---

# 21. VPA `Off`
```
updatePolicy:
  updateMode: "Off"
```

Meaning:
```
VPA observes workload
        |
        v
VPA generates recommendation
        |
        X
Does NOT automatically update Pods
```
This is excellent for testing.

You can inspect:
```
kubectl describe vpa my-app-vpa
```

Think:
```
Off = Recommendation only
```

---

# 22. VPA `Initial`
```
updatePolicy:
  updateMode: "Initial"
```
VPA applies recommendations when Pods are initially created.

Conceptually:
```
New Pod
   |
   v
VPA recommendation
   |
   v
Apply resources
```

Existing running Pods aren't automatically updated simply because VPA has a new recommendation.

Remember:
```
Initial = only at Pod creation
```

---

# 23. VPA `Recreate`
```
updatePolicy:
  updateMode: "Recreate"
```

VPA can evict/recreate existing Pods when their resource recommendations change.

Conceptually:
```
Existing Pod
     |
     v
VPA recommendation changes
     |
     v
Pod needs update
     |
     v
Eviction/recreation
     |
     v
New resources
```

---

# 24. VPA `Auto`
```
updatePolicy:
  updateMode: "Auto"
```

Historically this meant VPA could automatically update Pods, including eviction/recreation behavior.

For modern VPA/Kubernetes versions, the exact implementation can also take advantage of supported in-place Pod resource resizing.

For CKA/CKS preparation:
```
Off
    ↓
Recommendation only

Initial
    ↓
Apply recommendation to newly created Pods

Recreate
    ↓
Update by recreating Pods

Auto
    ↓
Automatically manage updates
```

Always check the VPA/Kubernetes version when working on a real production cluster because behavior evolves.

---

# 25. `resourcePolicy`
Example:
```
resourcePolicy:
  containerPolicies:
```

This allows you to control how VPA treats containers.

For example:
```
containerPolicies:
  - containerName: "my-app"
```

This says:
```
Apply this policy to container "my-app"
```

---

# 26. `minAllowed`
```
minAllowed:
  cpu: "250m"
```
This establishes a lower boundary.

Conceptually:
```
VPA recommendation
        |
        v
Must not go below 250m
```

For example:
```
Recommendation = 100m
Minimum = 250m
```

The resulting recommendation cannot simply be below your configured minimum.

---

# 27. `maxAllowed`
```
maxAllowed:
  cpu: "2"
```

This establishes an upper boundary.

Therefore:
```
250m ≤ CPU recommendation ≤ 2 CPU
```

Think:
```
             2 CPU
               |
               | MAX
               |
          VPA recommendation
               |
               | MIN
               |
             250m
```

---

# 28. Why Are Min/Max Boundaries Important?
Imagine VPA sees an unusual workload spike:
```
Normal usage:
300m

Temporary spike:
8 CPU
```

Without appropriate constraints, you may not want resource recommendations to grow beyond what your infrastructure can reasonably support.
So:
```
minAllowed:
  cpu: "250m"

maxAllowed:
  cpu: "2"
```
creates a safety boundary.

---

# 29. `controlledResources`
The example says:
```
controlledResources:
  - cpu
```

This means VPA is controlling CPU.
If you want both CPU and memory:
```
controlledResources:
  - cpu
  - memory
```

Then VPA can manage both resources, subject to the configured policies.

---
# 30. Viewing VPA Recommendations
Use:
```
kubectl describe vpa my-app-vpa
```

You might see:
```
Recommendation:
  Target:
    Cpu: 1.5
```

This means VPA thinks approximately:
```
CPU request ≈ 1.5 CPU
```
is appropriate according to its recommendation.

Do not confuse:
```
Target
```

with:
```
Current request
```
They are different concepts.

---

# 31. VPA Recommendation Values
VPA recommendations commonly include values such as:
```
Lower Bound
Target
Upper Bound
Uncapped Target
```

Conceptually:
```
             Upper Bound
                  |
                  |
                Target
                  |
                  |
             Lower Bound
```
The exact values depend on VPA's recommendation calculations.

The important idea:
```
Target
  ↓
Preferred resource amount

Lower Bound
  ↓
Lower reasonable range

Upper Bound
  ↓
Upper reasonable range
```
This becomes important when understanding why the VPA Updater decides whether a Pod needs updating.

---

# 32. Important Correction: VPA Is Not Simply Threshold Based
An article might say:
> If CPU consumption reaches a predefined threshold, increase CPU.

This is somewhat misleading.
VPA isn't simply:
```
if CPU > 80%:
    increase CPU
```

A better mental model is:
```
Resource usage history
        +
Current observations
        +
VPA recommendation algorithm
        |
        v
Recommended resources
```
VPA analyzes resource usage over time to produce recommendations.

---

# 33. Important Correction: Requests Cannot Exceed Limits
A common incorrect example is:
```
resources:
  requests:
    cpu: "1"

  limits:
    cpu: "500m"
```

This is problematic because:
```
request > limit
```

For the same resource, the normal relationship is:
```
request ≤ limit
```

A valid example would be:
```
resources:
  requests:
    cpu: "500m"

  limits:
    cpu: "1"
```

This is an important Kubernetes detail to understand rather than blindly memorizing examples.

---

# 34. VPA and HPA Together
You can potentially use:
```
HPA + VPA
```

but you must be careful about what each controller manages.

HPA:
```
Changes number of Pods
```

VPA:
```
Changes resources per Pod
```

Conceptually:
```scss
                 Application
                      |
            +---------+---------+
            |                   |
            v                   v
           HPA                 VPA
            |                   |
            v                   v
     Number of Pods       CPU/Memory
                          per Pod
```

This can work when carefully designed, but careless configurations can create competing feedback loops.

---

# 35. Example: HPA + VPA
Imagine:
```
Deployment
replicas = 2
```

Each Pod currently has:
```
CPU request = 250m
```

Application traffic increases.
HPA sees:
```
CPU utilization high
```
and scales:
```
2 Pods
   ↓
4 Pods
```
Meanwhile VPA observes that each Pod needs more resources.

It may recommend:
```
250m
  ↓
500m
```

So you have two independent dimensions:
```
HPA:
2 Pods → 4 Pods

VPA:
250m → 500m per Pod
```

---

# 36. HPA vs VPA

|Feature|HPA|VPA|
|---|---|---|
|Scaling dimension|Number of Pods|Resources per Pod|
|CPU requests|Usually used as input for utilization|Can be adjusted|
|Memory requests|Can be used as metric depending on configuration|Can be adjusted|
|Adds Pods|Yes|No|
|Removes Pods|Yes|No|
|Changes CPU/memory requests|No|Yes|
|Pod restart traditionally required|No|Often yes|
|Good for traffic scaling|Yes|Not primarily|
|Good for resource right-sizing|No|Yes|

The simplest exam answer:
```
HPA = Scale OUT / IN
VPA = Scale UP / DOWN
```

---

# 37. VPA Architecture to Memorize
For CKA/CKS, remember:
```scss
                    Kubernetes API
                          |
             +------------+------------+
             |                         |
             v                         v
       VPA Recommender          VPA Admission
             |                  Controller
             |                         |
             v                         v
       Recommendations          Mutate new Pods
             |
             v
         VPA Updater
             |
             v
      Existing Pods
             |
             v
       Update / Eviction
             |
             v
       New configuration
```

And the three components:
```
RECOMMENDER
    ↓
calculates recommendation

UPDATER
    ↓
updates existing workload Pods

ADMISSION CONTROLLER
    ↓
applies recommendation during Pod admission
```

---

# 38. Complete VPA Lifecycle
Suppose your application starts with:
```
resources:
  requests:
    cpu: 250m
    memory: 256Mi
```

## Step 1 — Application Runs
```
Pod
 |
 +-- CPU = 600m
 +-- Memory = 500Mi
```

## Step 2 — VPA Observes
```
       Usage
         |
         v
VPA Recommender
```

## Step 3 — VPA Calculates
```
Recommended:
CPU    = 750m
Memory = 512Mi
```

## Step 4 — Existing Pod
If update policy permits automatic updates:
```
Old Pod
CPU request = 250m
```

may need updating.
## Step 5 — Updater
```
Updater
   |
   v
Pod update/eviction mechanism
```

## Step 6 — Replacement/In-Place Update
Depending on supported mechanisms:
```
New Pod
CPU request = 750m
Memory = 512Mi
```

or an appropriate in-place resize where supported.

## Step 7 — Future Observation
VPA keeps observing:
```
Observe
   ↓
Recommend
   ↓
Update
   ↓
Observe again
```

VPA is essentially a continuous feedback loop.

---

# 39. Important VPA Commands
## Check VPA objects
```
kubectl get vpa
```

## Detailed information
```
kubectl describe vpa my-app-vpa
```

## View YAML
```
kubectl get vpa my-app-vpa -o yaml
```

## Check VPA components
```
kubectl get pods -n kube-system | grep vpa
```

## Check resource usage
```
kubectl top pods
```

and:
```
kubectl top nodes
```

---

# 40. What You Should Know for CKA/CKS
Don't try to memorize every implementation detail.
Focus on these.
## Core Concept
```
VPA adjusts CPU/memory resources of Pods.
```

## HPA Distinction
```
HPA → number of Pods
VPA → resources per Pod
```

## Components
```
Recommender
Updater
Admission Controller
```

## API
```
apiVersion: autoscaling.k8s.io/v1
```

## Kind
```
kind: VerticalPodAutoscaler
```

## Target
```
targetRef:
```

## Update Modes
```
Off
Initial
Recreate
Auto
```

## Resource Boundaries
```
minAllowed:
maxAllowed:
```

## Controlled Resources
```
controlledResources:
  - cpu
  - memory
```

## Inspect Recommendation
```
kubectl describe vpa <name>
```

---

# 41. Final Mental Model
If you remember only one thing, remember this:
```
                    WORKLOAD
                       |
                       v
              +------------------+
              | Resource Usage   |
              +--------+---------+
                       |
                       v
              +------------------+
              | VPA Recommender  |
              +--------+---------+
                       |
                       v
              "You should use
               750m CPU"
                       |
             +---------+---------+
             |                   |
             v                   v
       New Pod              Existing Pod
             |                   |
             v                   v
 Admission Controller       VPA Updater
             |                   |
             v                   v
   Recommended resources    Update/eviction
```

Compare this with HPA:
```
                  WORKLOAD
                     |
                     v
                    HPA
                     |
          +----------+----------+
          |                     |
          v                     v
      1 Pod                  5 Pods
```

The fundamental distinction:
```
VPA:
"What size should each Pod be?"

HPA:
"How many Pods should I have?"
```

That is the foundation of Vertical Pod Autoscaling



| Feature                 | VPA (Vertical Scaling)                                           | HPA (Horizontal Scaling)                                         |
| ----------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| Scaling Method          | Increases CPU and memory of existing Pods                        | Adds/Removes Pods based on load                                  |
| Pod Behavior            | Restarts Pods to apply new resource values                       | Keeps existing Pods running                                      |
| Handles Traffic Spikes? | * No, because scaling requires a Pod restart                     | Yes, instantly adds more Pods                                    |
| Optimizes Costs?        | Prevents over-provisioning of CPU/memory                         | Avoids unnecessary idle Pods                                     |
| Best For                | Stateful workloads, CPU/memory-heavy apps<br>(DBs, ML workloads) | Web apps, microservices, stateless services                      |
| Example Use Cases       | Databases (MYSQL, PostgreSQL), JVM-based apps, AI/ML Workloads   | Web Servers (Nginx, API Services), message queues, microservices |

---



