# In-Place Pod Resizing
This is an important topic for modern Kubernetes because it connects three areas you have already studied:
1. Pod resource requests and limits
2. Vertical scaling
3. Vertical Pod Autoscaler (VPA)

The biggest thing to understand is:
> **In-place Pod Resize allows Kubernetes to change CPU and memory resources of a running Pod without necessarily deleting and recreating the Pod.**

And there is an important **2026 update** to the material you pasted: **container-level In-Place Pod Resize became stable (GA) in Kubernetes v1.35**. It was alpha in v1.27 and beta in v1.33. So older course material describing it as an alpha/beta experimental feature is now outdated.

---

# 1. First understand the problem
Suppose we have:
```
apiVersion: v1
kind: Pod
metadata:
  name: web
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      requests:
        cpu: "250m"
        memory: "256Mi"
      limits:
        cpu: "500m"
        memory: "512Mi"
```

Initially:
```
CPU request = 250m
CPU limit   = 500m

Memory request = 256Mi
Memory limit   = 512Mi
```

Now imagine the application needs more CPU.

We want:
```
CPU request = 1 CPU
CPU limit   = 2 CPU
```

Historically, changing Pod resources meant:
```
Delete old Pod
      |
      v
Create new Pod
      |
      v
Start container
```
That can be disruptive.

In-place resizing changes the model to:
```
Running Pod
    |
    | change CPU/memory
    v
Kubelet adjusts container resources
    |
    v
Same Pod continues running
```

This is especially useful for applications where restarting the Pod is expensive or disruptive.

Kubernetes now documents container-level in-place CPU/memory resizing as **stable in v1.35 and enabled by default**.

---

# 2. Traditional Pod resource change
Consider:
```
resources:
  requests:
    cpu: "250m"
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

You change it to:
```
resources:
  requests:
    cpu: "1"
    memory: "512Mi"
  limits:
    cpu: "2"
    memory: "1Gi"
```

With the traditional Deployment behavior, changing the Pod template causes a new ReplicaSet and new Pods.

Conceptually:
```
Deployment
     |
     +---- Old ReplicaSet
     |       |
     |       +---- Pod A
     |       +---- Pod B
     |
     +---- New ReplicaSet
             |
             +---- New Pod
             +---- New Pod
```

The old Pods eventually disappear.

With in-place resizing, the resource allocation of an existing running Pod can be changed instead.

---

# 3. What exactly is being resized?
Only two resource types are relevant here:
```
CPU
Memory
```

For example:
```
resources:
  requests:
    cpu: "500m"
    memory: "512Mi"
  limits:
    cpu: "1"
    memory: "1Gi"
```

You can resize:
```
500m CPU -> 1 CPU
512Mi    -> 1Gi
```

But you cannot use this mechanism to dynamically change things such as:
```
container image
ports
environment variables
volumes
securityContext
```
Those are different types of Pod changes.

The official documentation specifically defines the mutable container resources as CPU and memory.

---

# 4. Requests vs limits
You need to understand this very clearly for CKA.

Suppose:
```
resources:
  requests:
    cpu: "500m"
    memory: "512Mi"

  limits:
    cpu: "1"
    memory: "1Gi"
```

Think:

```
REQUEST
=======
What Kubernetes uses when scheduling the Pod.

LIMIT
=====
The maximum resource boundary enforced for the container.
```

For example:
```
Node has:
CPU = 4 CPU
Memory = 8Gi
```

Pod:
```
CPU request = 1 CPU
Memory request = 2Gi
```

The scheduler considers those requests when deciding whether the Pod can fit on the node.

Therefore, when resizing resources upward, node capacity matters.

---

# 5. Desired vs actual resources
This is one of the most important concepts in modern in-place resizing.
There are effectively multiple resource states.
## Desired resources
Defined in:
```
spec.containers[*].resources
```

This represents what you want.
For example:
```
resources:
  requests:
    cpu: "1"
    memory: "512Mi"
```

means:
```
Desired CPU = 1
Desired Memory = 512Mi
```

---

## Actual resources
Kubernetes reports the resources currently configured for the running container in:
```
status.containerStatuses[*].resources
```

So you could conceptually have:
```
spec:
    desired CPU = 1

status:
    current CPU = 500m
```

This means:
```
Desired != Actual
```

The kubelet works to make the actual resources match the desired resources.

---

# 6. Allocated resources
You may also encounter:
```
status.containerStatuses[*].allocatedResources
```
This is an advanced field.

It represents resources that the kubelet has allocated/confirmed for the container and is particularly relevant to scheduling and resize processing.

For CKA, remember the basic distinction:
```
spec.resources
        |
        v
Desired

status.containerStatuses[*].resources
        |
        v
Current/actual

status.containerStatuses[*].allocatedResources
        |
        v
Resources allocated by kubelet
```

The official documentation recommends focusing primarily on `status.containerStatuses[*].resources` for normal monitoring and validation.

---

# 7. How does the resize actually happen?
The architecture is roughly:
```
kubectl
   |
   v
API Server
   |
   v
Pod spec updated
   |
   v
Scheduler / resource accounting
   |
   v
Kubelet
   |
   v
Container Runtime
   |
   v
cgroups
   |
   v
CPU / Memory allocation changes
```
The kubelet is the component that ultimately works with the container runtime to apply the resource changes.

The container runtime must support the required resource-update functionality.

---

# 8. Resize subresource
Modern Kubernetes provides a resize subresource.

Conceptually:
```
Pod
 |
 +-- main resource
 |
 +-- resize subresource
```

This allows resource changes to be handled separately from ordinary Pod updates.

The official documentation states that resizing can be requested using operations such as:

```
kubectl patch
kubectl apply
kubectl edit
```

targeting the Pod's `resize` subresource. A kubectl client of at least v1.32 is required for the `--subresource=resize` option.

---

# 9. Example: CPU resize without restart
Let's create a Pod:
```
apiVersion: v1
kind: Pod
metadata:
  name: cpu-demo
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      requests:
        cpu: "250m"
      limits:
        cpu: "500m"
```

Create:
```
kubectl apply -f cpu-demo.yaml
```

Check:
```
kubectl get pod cpu-demo
```

Now suppose we want:
```
250m -> 1 CPU
500m -> 2 CPU
```

You can update the Pod's resource configuration using the resize mechanism.

For example:
```
kubectl patch pod cpu-demo \
  --subresource=resize \
  --type='merge' \
  -p '{"spec":{"containers":[{"name":"nginx","resources":{"requests":{"cpu":"1"},"limits":{"cpu":"2"}}}]}}'
```

The important part is:
```
--subresource=resize
```

This tells Kubernetes that we are requesting a resource resize rather than an ordinary Pod mutation.

---

# 10. Verify the resize
Check the Pod:
```
kubectl get pod cpu-demo -o yaml
```

Look at:
```
spec:
  containers:
  - name: nginx
    resources:
```

Then look at:
```
status:
  containerStatuses:
```

You may find:
```
resources:
  requests:
    cpu: "1"
  limits:
    cpu: "2"
```
The status tells you what has actually been applied.

---

# 11. Why CPU is easier than memory
This is a very important concept.

CPU allocation can generally be adjusted dynamically.
For example:
```
500m CPU
    |
    v
1 CPU
```
The running process can continue.

Memory is more complicated.

Suppose:
```
Current memory usage = 700Mi
```

and you request:
```
memory limit = 500Mi
```

That is problematic because:
```
700Mi currently being used
       >
500Mi requested limit
```
The new limit cannot safely be applied in the same way.

Therefore, memory resize behavior can involve a container restart depending on the resize policy and runtime/application characteristics.

---

# 12. ResizePolicy
Kubernetes provides:
```
resizePolicy:
```

This lets you specify whether changing a particular resource requires a container restart.

Example:
```
resizePolicy:
- resourceName: cpu
  restartPolicy: NotRequired
```

Meaning:
```
CPU changes
     |
     v
Do NOT restart container
```

You can also specify:
```
resizePolicy:
- resourceName: memory
  restartPolicy: RestartContainer
```

Meaning:
```
Memory change
     |
     v
Restart container
```

So a complete example could look like:
```
apiVersion: v1
kind: Pod
metadata:
  name: resize-demo
spec:
  containers:
  - name: nginx
    image: nginx

    resizePolicy:
    - resourceName: cpu
      restartPolicy: NotRequired

    - resourceName: memory
      restartPolicy: RestartContainer

    resources:
      requests:
        cpu: "250m"
        memory: "256Mi"
      limits:
        cpu: "500m"
        memory: "512Mi"
```

The idea is:
```
CPU resize
    |
    +---- no restart

Memory resize
    |
    +---- restart allowed/required
```

The exact behavior also depends on the container runtime and workload characteristics.

---

# 13. CPU resize example
Initial:
```
resources:
  requests:
    cpu: "250m"
  limits:
    cpu: "500m"
```

Resize:
```
resources:
  requests:
    cpu: "1"
  limits:
    cpu: "2"
```

With:
```
resizePolicy:
- resourceName: cpu
  restartPolicy: NotRequired
```

The goal is:
```
Pod
 |
 | CPU resize
 v
same Pod
same container
same process
```

rather than:
```
Pod deleted
   |
   v
new Pod
   |
   v
new process
```

---

# 14. Memory resize example
Suppose:
```
Memory request = 256Mi
Memory limit   = 512Mi
```

We want:
```
Memory request = 512Mi
Memory limit   = 1Gi
```

Increasing memory is generally easier:
```
512Mi
  |
  v
1Gi
```

But memory changes can require a restart depending on the resize policy/runtime.

For example:
```
resizePolicy:
- resourceName: memory
  restartPolicy: RestartContainer
```
This means Kubernetes can restart the container to apply the memory resize.

Important distinction:
```
Pod restart
    !=
Pod recreation
```

A container may restart while the Pod itself remains the same Pod object.

---

# 15. Pod recreation vs container restart
This distinction is extremely important.
## Pod recreation
```
Old Pod
  X
  |
  v
Deleted

New Pod
  |
  v
Created
```
Pod UID changes.

---

## Container restart
```
Same Pod
   |
   +---- container stops
   |
   +---- container starts again
```

The Pod remains the same object.
For example:
```
kubectl get pod resize-demo -o jsonpath='{.metadata.uid}'
```

If only the container restarts, the Pod UID remains the same.

---

# 16. Infeasible resize
This is another important exam concept.
Suppose a node has:
```
Total CPU = 4 CPU
Currently available = 500m
```

Your Pod requests:
```
CPU = 2 CPU
```
The node doesn't have enough available capacity.

The resize may become:
```
InProgress
```

or otherwise remain pending/deferred until the request can be satisfied.

Conceptually:
```
Requested:
2 CPU

Available:
500m

       |
       v

Cannot resize immediately
       |
       v
Deferred / retry
```

Kubernetes has mechanisms for retrying resize operations.

---

# 17. Memory infeasible resize
Consider:
```
Current memory usage = 800Mi
```

You request:
```
Memory limit = 512Mi
```

That is impossible to satisfy safely at that moment.

The resize can remain in progress until the desired memory limit becomes feasible.

However, there is an important **2026 correction** to the material you pasted.

Your notes say:
> A container's memory limit can't be set below its current usage.

That was an important limitation in earlier versions.

With Kubernetes **v1.35**, memory-limit decreases were changed: Kubernetes now permits decreasing memory limits, while the kubelet makes a best-effort check to avoid OOM conditions.

So for current Kubernetes:
```
v1.33/v1.34-era material
        |
        v
memory decrease had stricter restrictions

v1.35+
        |
        v
memory limit decrease permitted
        |
        v
kubelet attempts to avoid unsafe/OOM conditions
```

For your **2026 CKA preparation**, use the current Kubernetes documentation rather than memorizing the older restriction as universally true.

---

# 18. What happens if the node doesn't have capacity?
This is an important conceptual question.
Suppose:
```
Node capacity = 4 CPU

Existing allocation = 3.5 CPU

Available = 500m
```

You ask for:
```
+1 CPU
```

Kubernetes cannot simply pretend that the node has another 500m.

The resize can be deferred.

Conceptually:
```
Resize request
      |
      v
Can node satisfy it?
      |
   +--+--+
   |     |
  YES    NO
   |     |
   v     v
Apply   Defer
         |
         v
       Retry
```

The current Kubernetes implementation includes retry behavior for deferred resizes. Kubernetes 1.35 also introduced prioritization for deferred resize requests.

---

# 19. QoS Class
Your notes mention:
> Pod QoS Class cannot change

This is an important concept.
Kubernetes QoS classes include:
```
Guaranteed
Burstable
BestEffort
```

For example, a container with matching CPU and memory requests/limits can contribute toward a Guaranteed Pod.

Do not think of in-place resizing as a way to arbitrarily redesign the Pod's QoS configuration.

The important exam takeaway is:
```
In-place resize
        |
        +---- CPU
        +---- Memory
        |
        X
        +---- arbitrary Pod configuration changes
```

---

# 20. Init containers
In-place resizing is for normal application containers.

You should remember:
```
Application containers
    |
    +---- can be resized

Init containers
    |
    +---- cannot be resized
```

Why?
Because init containers have a different lifecycle:
```
Init container
      |
      v
Runs
      |
      v
Completes
      |
      v
Application container starts
```

There is normally no continuously running init container to resize.

---

# 21. Ephemeral containers
Ephemeral containers are primarily used for debugging.

Example:
```
kubectl debug
```

They also aren't targets for normal in-place resource resizing.

For exam memory:
```
CPU + Memory
   |
   +---- normal containers: YES
   |
   +---- init containers: NO
   |
   +---- ephemeral containers: NO
```

---

# 22. Windows
The material you pasted also mentions Windows limitations.

For CKA, most of the in-place resize knowledge you need is around Linux Kubernetes nodes.

Do not assume that every Kubernetes platform/runtime combination supports every resize capability identically.

---

# 23. Kubernetes version timeline
This is worth memorizing because your course material mixes different Kubernetes versions.
```
Kubernetes 1.27
       |
       v
In-place Pod Vertical Scaling
ALPHA

Kubernetes 1.33
       |
       v
BETA

Kubernetes 1.35
       |
       v
GA / STABLE
```
This is the current timeline documented by Kubernetes.

So if your notes say:
```
"alpha"
"experimental"
"enable FEATURE_GATES"
```

that may be describing an older Kubernetes version.
For **Kubernetes 1.35+**, container-level in-place resizing is stable and enabled by default.

---

# 24. Feature gate
Older documentation may show:
```
FEATURE_GATES=InPlacePodVerticalScaling=true
```

That was relevant when the feature was not yet stable.
In current Kubernetes 1.35+, the container-level feature is GA and enabled by default.

So don't blindly execute:
```
FEATURE_GATES=InPlacePodVerticalScaling=true
```

on a modern cluster and assume that is how you enable the feature.

Instead, first check:
```
kubectl version
```
and determine which Kubernetes version your lab is actually running.

---

# 25. CKA exam perspective
For CKA, understand the difference between:

### Horizontal scaling
Change:
```
number of Pods
```

Example:
```
1 Pod
   |
   v
5 Pods
```

Command:
```
kubectl scale deployment myapp --replicas=5
```

---

### Vertical scaling
Change:
```
resources allocated to Pod/container
```

Example:
```
250m CPU
   |
   v
1 CPU
```

Historically:
```
Pod recreated
```

Modern in-place resizing:
```
Pod can remain
while CPU/memory allocation changes
```

---

# 26. HPA vs VPA vs In-Place Resize
You have studied HPA already, so connect the topics.

## HPA
Changes:
```
NUMBER OF PODS
```

Example:
```
2 Pods
  |
  | high CPU
  v
5 Pods
```

---

## VPA
Changes:
```
CPU / MEMORY RESOURCES
```

Example:
```
250m CPU
   |
   v
750m CPU
```

VPA can use recommendations and update modes to manage resources. Current VPA documentation includes `InPlaceOrRecreate`, which attempts in-place resource updates and can fall back to Pod eviction when necessary.

---

## In-Place Pod Resize
This is the underlying Kubernetes capability that allows:
```
CPU / memory
     |
     v
change resources of running Pod
```
without necessarily recreating the Pod.

Think:
```
                  Scaling
                     |
          +----------+----------+
          |                     |
       Horizontal            Vertical
          |                     |
          v                     v
        HPA                    VPA
          |                     |
          v                     v
   More/fewer Pods      More/fewer resources
                                |
                                v
                       In-place Pod Resize
```

---

# 27. HPA + VPA comparison

|Feature|HPA|VPA|
|---|---|---|
|Scaling direction|Horizontal|Vertical|
|Changes|Pod count|CPU/memory|
|Example|2 → 5 Pods|500m → 1 CPU|
|Main resource|Replicas|Requests/limits|
|Typical metric|CPU/memory/custom|Historical resource usage|
|Pod recreation|Usually no, scales replicas|Depends on update mode|
|In-place resize|Not the primary mechanism|Can leverage it|

---

# 28. Very important: In-place resize is not HPA
Do not confuse:
```
kubectl scale
```

with:
```
Pod resize
```

This:
```
kubectl scale deployment nginx --replicas=5
```

changes:
```
Pod count
```

This:
```
CPU: 250m -> 1
```

changes:
```
resource allocation
```

Therefore:
```
HPA
=
How many Pods?

VPA
=
How much CPU/memory per Pod?

In-place resize
=
Can those CPU/memory resources be changed while the Pod remains?
```

---

# 29. In-place resize and Deployment
There is a subtle point here.
A Deployment manages Pods using a Pod template.

For example:
```
spec:
  template:
    spec:
      containers:
      - name: nginx
        image: nginx
        resources:
          requests:
            cpu: 250m
```

If you modify the Deployment's Pod template, that is still a Deployment rollout concern.

In-place resizing is fundamentally a **Pod resource resize operation**.

Therefore, don't assume:
```
kubectl edit deployment
```

automatically means:
```
existing Pods will be resized in-place
```

The workload controller's behavior and the Pod resize mechanism are separate concepts.

---

# 30. Practical lab
Create:
```
apiVersion: v1
kind: Pod
metadata:
  name: resize-demo
spec:
  containers:
  - name: nginx
    image: nginx
    resizePolicy:
    - resourceName: cpu
      restartPolicy: NotRequired
    - resourceName: memory
      restartPolicy: RestartContainer
    resources:
      requests:
        cpu: "250m"
        memory: "256Mi"
      limits:
        cpu: "500m"
        memory: "512Mi"
```

Apply:
```
kubectl apply -f resize-demo.yaml
```

Check:
```
kubectl get pod resize-demo
```

Inspect resources:
```
kubectl get pod resize-demo -o yaml
```

You can specifically inspect container status:
```
kubectl get pod resize-demo \
  -o jsonpath='{.status.containerStatuses[0].resources}'
```

Inspect the Pod UID:
```
kubectl get pod resize-demo \
  -o jsonpath='{.metadata.uid}'
```

Then resize CPU using the resize subresource:
```
kubectl patch pod resize-demo \
  --subresource=resize \
  --type='merge' \
  -p '{"spec":{"containers":[{"name":"nginx","resources":{"requests":{"cpu":"1"},"limits":{"cpu":"2"}}}]}}'
```

Check:
```
kubectl get pod resize-demo -o yaml
```

Look at:
```
spec.containers[].resources
```

and:
```
status.containerStatuses[].resources
```

---

# 31. Troubleshooting
If resize doesn't happen immediately, investigate:
```
kubectl describe pod resize-demo
```

Look at:
```
Events
```

Then:
```
kubectl get pod resize-demo -o yaml
```

Check:
```
status
```

You may encounter conditions associated with resize processing.

Also inspect:
```
kubectl get nodes
```

and:
```
kubectl describe node <node-name>
```

Check whether sufficient CPU/memory is available.

---

# 32. The mental model you should memorize
Think about the entire process like this:

```scss
                    POD
                     |
             +-------+-------+
             |               |
          CPU             Memory
             |               |
             +-------+-------+
                     |
              Resource Resize
                     |
                     v
                 API Server
                     |
                     v
                  Kubelet
                     |
                     v
             Container Runtime
                     |
                     v
                  cgroups
                     |
                     v
             New allocation
```

The critical distinction is:
```scss
OLD MODEL

Resource change
      |
      v
Pod recreation
      |
      v
New Pod
```

versus:
```scss
MODERN MODEL

CPU/Memory resource change
      |
      v
Resize request
      |
      v
Kubelet
      |
      v
Container resources updated
      |
      v
Same Pod can continue
```

---

# 33. CKA high-value facts
Memorize these:
```
In-place Pod Resize
        |
        +---- CPU
        +---- Memory
```

```
Kubernetes 1.27
        |
        +---- Alpha
```

```
Kubernetes 1.33
        |
        +---- Beta
```

```
Kubernetes 1.35
        |
        +---- GA / Stable
        +---- Enabled by default
```

Important limitations/concepts:
```
CPU                  YES
Memory               YES

Init containers      NO
Ephemeral containers NO

Other resources      NO
```

And:
```
spec.containers[].resources
        =
desired resources
```

while:
```
status.containerStatuses[].resources
        =
resources currently configured
```

Also:
```
HPA
  -> changes number of Pods

VPA
  -> changes resource requirements

In-place resize
  -> mechanism for changing CPU/memory of a running Pod
```

---
As of Kubernetes 1.35:
```
In-Place Pod Resize = Stable
```

and it is enabled by default for container-level CPU/memory resizing.
**Pod-level resources** are a separate capability. In Kubernetes 1.36, in-place vertical scaling of Pod-level resources is beta and enabled by default, with additional requirements such as cgroup v2 and appropriate runtime support.

So for your CKA notes, keep these two concepts separate:
```
Container-level In-Place Resize
Kubernetes 1.35
Stable / GA
```

versus:
```
Pod-level In-Place Resource Resize
Kubernetes 1.36
Beta
```

[Official Kubernetes: Resize CPU and Memory Resources assigned to Containers](https://kubernetes.io/docs/tasks/configure-pod-container/resize-container-resources/?utm_source=chatgpt.com)

This version distinction is particularly important because CKA labs may run a specific Kubernetes version, so **always check `kubectl version` before applying version-specific instructions**.