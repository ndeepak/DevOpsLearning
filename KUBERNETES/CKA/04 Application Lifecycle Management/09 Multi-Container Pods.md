# Multi-Container Pods
Multi-container Pods are an important Kubernetes concept because they test whether you understand the difference between a **Pod**, a **container**, and an **application/service**.
The most important rule is:
> **A Pod is the smallest deployable unit in Kubernetes, and a Pod can contain one or multiple containers.**

For CKA/CKS, you should understand not only how to write a multi-container Pod, but also **why containers belong in the same Pod, how they communicate, how they share storage, and when you should NOT put them together.**

---
# 1. Start With the Pod Concept
Normally, you might have:
```
Pod
 |
 +-- Container
```

Example:
```
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
    - name: nginx
      image: nginx
```

This Pod contains:
```
nginx-pod
   |
   +-- nginx container
```

But Kubernetes also allows:
```
Pod
 |
 +-- Container A
 |
 +-- Container B
```
This is a **multi-container Pod**.

---
# 2. Basic Multi-Container Pod
Example:
```
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp
spec:
  containers:
    - name: simple-webapp
      image: simple-webapp

    - name: log-agent
      image: log-agent
```

The important part is:
```
containers:
  - name: simple-webapp
    image: simple-webapp

  - name: log-agent
    image: log-agent
```
`containers` is an **array/list**.

Therefore you can have:
```
containers:
  - ...
  - ...
  - ...
```

---

# 3. Why Put Multiple Containers in One Pod?
The key question is:
> Why not simply create two Pods?

Suppose we have:
```
Web Application
       +
Logging Agent
```

The logging agent is specifically associated with that application instance.

You might want:
```
Pod 1
 ├── Web App
 └── Log Agent

Pod 2
 ├── Web App
 └── Log Agent

Pod 3
 ├── Web App
 └── Log Agent
```

When the application scales:
```
1 replica
    ↓
2 replicas
    ↓
3 replicas
```

the logging agent scales with it automatically.

---

# 4. Same Pod = Same Lifecycle
Containers inside a Pod are managed together.
Conceptually:
```
Pod
 |
 +-- Container A
 |
 +-- Container B
```

The Pod is the unit Kubernetes schedules onto a node.

Therefore Kubernetes does not schedule:
```
Container A → Node 1
Container B → Node 2
```
when they belong to the same Pod.
Instead:
```
Node
 |
 +-- Pod
      |
      +-- Container A
      |
      +-- Container B
```

Both containers run on the **same node**.
This is one of the biggest differences between:
```
Two containers in one Pod
```

and:
```
Two containers in two Pods
```

---

# 5. Pod Networking
Containers inside the same Pod share the **network namespace**.

This means they share:
- IP address
- network interface
- network namespace
- port space

For example:
```
Pod IP = 10.244.1.20

        Pod
         |
   +-----+-----+
   |           |
 Web App    Log Agent
```

Both containers use:
```
10.244.1.20
```
as the Pod's network identity.

---

# 6. Containers Communicate Using localhost
This is extremely important.
Suppose:
```
Web application
listens on port 8080
```
and another container needs to access it.

Because they share the network namespace:
```
log-agent → localhost:8080
```
works.

Example:
```
curl http://localhost:8080
```
from the second container can reach the first container's application.
You do **not** need:
```
Pod IP → 8080
```
for communication between containers in the same Pod.
You can use:
```
localhost:8080
```

---

# 7. Important Port Conflict
Because containers share the same network namespace, they also share the same network port space.
Therefore this is problematic:
```
Container A → port 8080
Container B → port 8080
```
Both cannot independently bind the same IP/port combination.
For example:
```
Pod
 |
 +-- nginx → 8080
 |
 +-- app   → 8080
```
Both attempting to listen on:
```
0.0.0.0:8080
```
would cause a conflict.
Instead:
```
nginx → 8080
app   → 8081
```
could work.
This is a common exam/troubleshooting concept.

---
# 8. Pod IP vs Container IP
In Kubernetes networking, think of the Pod as having the network identity.
Example:
```
Pod IP:
10.244.1.20

Pod
 |
 +-- container A
 |
 +-- container B
```
Both containers communicate through the same network namespace.
Therefore:
```
Container A
   |
   | localhost
   v
Container B
```
works.

---

# 9. Shared Storage
Containers inside a Pod can also share volumes.
This is one of the main reasons for using multi-container Pods.
Example:
```
Pod
 |
 +-- Application
 |
 +-- Log Agent
 |
 +-- Shared Volume
```

The application writes:
```
/app/logs/application.log
```

The logging agent reads:
```
/logs/application.log
```
using the same shared volume.

---
# 10. Example: Shared `emptyDir`
```
apiVersion: v1
kind: Pod
metadata:
  name: logging-pod

spec:
  containers:
    - name: app
      image: busybox
      command:
        - sh
        - -c
        - |
          while true; do
            date >> /var/log/app.log
            sleep 5
          done

      volumeMounts:
        - name: shared-logs
          mountPath: /var/log

    - name: log-agent
      image: busybox
      command:
        - sh
        - -c
        - |
          while true; do
            cat /var/log/app.log
            sleep 10
          done

      volumeMounts:
        - name: shared-logs
          mountPath: /var/log

  volumes:
    - name: shared-logs
      emptyDir: {}
```

The architecture becomes:
```
                    Pod
                     |
          +----------+----------+
          |                     |
          v                     v
       App Container       Log Agent
          |                     |
          |                     |
          +----------+----------+
                     |
                emptyDir
                     |
              shared filesystem
```

---

# 11. Why `emptyDir`?
`emptyDir` creates temporary storage associated with the Pod.
Example:
```
volumes:
  - name: shared-logs
    emptyDir: {}
```

When the Pod starts:
```
emptyDir
    ↓
created
```
Containers can mount it.
When the Pod is removed:
```
Pod deleted
    ↓
emptyDir deleted
```
Therefore `emptyDir` is useful for temporary shared data.
It is **not persistent storage**.

---

# 12. Multi-Container Pod With Shared Volume
A more realistic example:
```
apiVersion: v1
kind: Pod

metadata:
  name: web-logging

spec:

  containers:

    - name: web
      image: nginx

      volumeMounts:
        - name: logs
          mountPath: /var/log/nginx

    - name: log-agent
      image: fluentd

      volumeMounts:
        - name: logs
          mountPath: /var/log/nginx

  volumes:

    - name: logs
      emptyDir: {}
```

Now:
```
Pod
 |
 +--------------------------+
 |                          |
 | nginx                fluentd
 |   |                      |
 |   +----------+-----------+
 |              |
 |          shared volume
 |              |
 +--------------+
```

The logging agent can read the logs generated by nginx.

---

# 13. The Sidecar Pattern
This is a very important Kubernetes design pattern.
The most common example of multi-container Pods is the **sidecar pattern**.
Architecture:
```
Pod
 |
 +-- Main Application
 |
 +-- Sidecar
```

The sidecar provides additional functionality to the main application.

Examples:
```
Application + Logging Agent

Application + Proxy

Application + Monitoring Agent

Application + Configuration Agent
```
The sidecar is usually not the primary application.

---
# 14. Example: Application + Log Sidecar
Suppose:
```
Application
    |
    | writes
    v
/app/log/application.log
```

The sidecar:
```
Log Agent
    |
    | reads
    v
/app/log/application.log
```

Using:
```
shared volume
```

we get:
```
                 Pod
                  |
        +---------+---------+
        |                   |
        v                   v
    Application          Log Agent
        |                   |
        |                   |
        +--------+----------+
                 |
           Shared Volume
```
This is a classic **sidecar container**.

---
# 15. Why Not Use Two Pods?
Suppose you create:
```
Pod A
 |
 +-- Application
```

and:
```
Pod B
 |
 +-- Logging Agent
```

Now you have to deal with:
```
Pod networking
Pod discovery
Volume sharing
Lifecycle coordination
Scaling
```
For tightly coupled containers, putting them into one Pod simplifies this.

With a multi-container Pod:
```
Application
    +
Sidecar
```

automatically gets:
```
Same node
Same network namespace
Same Pod lifecycle
Shared volumes
```

---
# 16. But Don't Put Everything in One Pod
This is extremely important.
A common beginner mistake is:
> "If containers need to communicate, put them in the same Pod."

That is not always correct.

Containers should generally be in the same Pod when they are **tightly coupled** and need to share resources/lifecycle.

For example:
```
Application
+
Its sidecar
```
is reasonable.

But:
```
Frontend
+
Backend
```
should normally be separate Pods.

And:
```
Frontend
+
Database
```
should normally be separate Pods.

---

# 17. Separate Applications Usually Mean Separate Pods
Consider:
```
Frontend
Backend
Database
```

Better architecture:
```
Frontend Deployment
        |
      Pods

Backend Deployment
        |
      Pods

Database StatefulSet
        |
      Pods
```

rather than:
```
Pod
 |
 +-- Frontend
 +-- Backend
 +-- Database
```

Why?
Because they have different:
- Scaling requirements
- Lifecycles
- Resource requirements
- Deployment schedules
- Failure domains

---

# 18. Scaling Difference
Suppose:
```
Frontend requires 10 replicas
Backend requires 3 replicas
```

Separate Pods:
```
Frontend
  └── 10 Pods

Backend
  └── 3 Pods
```
Perfect.

But if frontend and backend are in the same Pod:

```
Frontend + Backend
```

then scaling the Pod gives:
```
10 Pods

Each Pod:
  ├── Frontend
  └── Backend
```

You automatically get:
```
10 frontend containers
10 backend containers
```
which may be wasteful.

---

# 19. Resource Management
Containers in a Pod can have their own resource requests and limits.
Example:
```
containers:

  - name: app
    image: my-app
    resources:
      requests:
        cpu: "500m"
        memory: "256Mi"
      limits:
        cpu: "1"
        memory: "512Mi"

  - name: sidecar
    image: log-agent
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
      limits:
        cpu: "200m"
        memory: "256Mi"
```

The Pod's scheduling requirements take the containers' resource requests into account.

Conceptually:
```
Pod request:

CPU
  =
app CPU request
+
sidecar CPU request

Memory
  =
app memory request
+
sidecar memory request
```

So multi-container Pods affect scheduling.

---

# 20. How Kubernetes Starts Containers
When you create:
```
apiVersion: v1
kind: Pod
metadata:
  name: multi-container
spec:
  containers:
    - name: app
      image: nginx
    - name: sidecar
      image: busybox
```
Kubernetes schedules the Pod onto a node.

Then the kubelet manages the containers.

Conceptually:
```
API Server
    |
    v
Scheduler
    |
    v
Node
    |
    v
Kubelet
    |
    +-- Container runtime
          |
          +-- app
          |
          +-- sidecar
```

---

# 21. Container Failure
This is important for understanding Pod behavior.
Suppose:
```
Pod
 |
 +-- App
 |
 +-- Sidecar
```
The app crashes.

The sidecar doesn't necessarily crash automatically.

Kubernetes manages containers according to their individual states and restart behavior, while the Pod remains the scheduling unit.

For a normal Pod:
```
restartPolicy: Always
```
is the default.

Therefore Kubernetes may restart the failed container.

---
# 22. `restartPolicy`
Pod-level field:
```
spec:
  restartPolicy: Always
```

Possible values:
```
Always
OnFailure
Never
```
For ordinary application Pods, `Always` is the default.

Example:
```
apiVersion: v1
kind: Pod

metadata:
  name: test

spec:
  restartPolicy: Always

  containers:
    - name: app
      image: nginx
```

---

# 23. Important CKA Point: Init Containers vs Sidecars
This is a very important distinction.

There are two concepts:
```
Init Containers
Sidecar Containers
```
They are not the same.

---

# 24. Init Container
An init container runs **before** the normal application containers.
Example:
```
spec:
  initContainers:
    - name: init
      image: busybox
      command:
        - sh
        - -c
        - echo "Initializing..."
  containers:
    - name: app
      image: nginx
```

Lifecycle:
```
Pod starts
    |
    v
Init container
    |
    v
Completes successfully
    |
    v
Application container starts
```

---

# 25. Sidecar
A sidecar runs alongside the application.
```
Pod starts
    |
    +----------------+
    |                |
    v                v
Application       Sidecar
```

Example:
```
spec:

  containers:

    - name: app
      image: nginx

    - name: sidecar
      image: log-agent
```

So:
```
Init Container
    =
Preparation

Sidecar
    =
Runs alongside application
```

---

# 26. Multi-Container Pod vs Init Container
Remember:
```
spec:
  initContainers:
```

is different from:
```
spec:
  containers:
```

Example:
```
spec:

  initContainers:
    - name: init
      image: busybox

  containers:
    - name: app
      image: nginx

    - name: sidecar
      image: fluentd
```

Lifecycle:
```
             Pod
              |
              v
        Init Container
              |
              v
          completes
              |
       +------+------+
       |             |
       v             v
     App          Sidecar
```

---

# 27. Useful Commands
Create:
```
kubectl apply -f pod.yaml
```

Check Pods:
```
kubectl get pods
```

More detailed:
```
kubectl get pod multi-container -o wide
```

Describe:
```
kubectl describe pod multi-container
```

---

# 28. Viewing Containers
Suppose:
```
multi-container
 |
 +-- app
 +-- sidecar
```

Run:
```
kubectl get pod multi-container
```

You might see:
```
NAME              READY   STATUS
multi-container   2/2     Running
```

The important part:
```
2/2
```

means:
```
2 containers are ready
2 containers exist
```

If you see:
```
1/2
```
it means one of the two containers isn't Ready.

---

# 29. Logs From Multi-Container Pods
This is extremely important for CKA troubleshooting.
If the Pod contains only one container:
```
kubectl logs multi-container
```
works.

But if there are multiple containers:
```
Pod
 |
 +-- app
 +-- sidecar
```
you should specify the container.
```
kubectl logs multi-container -c app
```
or:
```
kubectl logs multi-container -c sidecar
```
Follow logs:
```
kubectl logs -f multi-container -c app
```
Sidecar:
```
kubectl logs -f multi-container -c sidecar
```

---
# 30. Previous Container Logs
If a container crashed and restarted:
```
kubectl logs multi-container -c app --previous
```
This is extremely useful during CKA troubleshooting.
Example:
```
kubectl logs pod-name -c container-name --previous
```

Think:
```
Current container logs
        |
        v
kubectl logs

Previous crashed container
        |
        v
kubectl logs --previous
```

---

# 31. Executing Commands
Suppose the Pod contains:
```
app
sidecar
```

You need to enter the app container.
Use:
```
kubectl exec -it multi-container -c app -- /bin/sh
```

For sidecar:
```
kubectl exec -it multi-container -c sidecar -- /bin/sh
```
The `-c` option identifies the container.

This is a very common CKA command.

---

# 32. Example Complete Multi-Container Pod
Here is a good practice example:
```
apiVersion: v1
kind: Pod
metadata:
  name: web-with-sidecar
spec:
  containers:
    - name: web
      image: nginx
      ports:
        - containerPort: 80
      volumeMounts:
        - name: shared-data
          mountPath: /usr/share/nginx/html
    - name: sidecar
      image: busybox
      command:
        - sh
        - -c
        - |
          while true; do
            date > /shared/index.html
            sleep 5
          done
      volumeMounts:
        - name: shared-data
          mountPath: /shared
  volumes:
    - name: shared-data
      emptyDir: {}
```

Architecture:
```scss
                     Pod
                      |
             +--------+--------+
             |                 |
             v                 v
           nginx            sidecar
             |                 |
             |                 |
             +-------+---------+
                     |
                emptyDir
                     |
                shared data
```

The sidecar writes:
```
/shared/index.html
```
The nginx container sees the same file through:
```
/usr/share/nginx/html/index.html
```

Because both paths point to the same volume.

---

# 33. Testing the Example
Create:
```
kubectl apply -f pod.yaml
```

Check:
```
kubectl get pod web-with-sidecar
```

Expected:
```
NAME               READY   STATUS
web-with-sidecar   2/2     Running
```

Check nginx:
```
kubectl exec -it web-with-sidecar -c web -- cat /usr/share/nginx/html/index.html
```

Check sidecar:
```
kubectl logs web-with-sidecar -c sidecar
```

---

# 34. Shared Network + Shared Storage
The two major shared resources to remember are:
```
Same Pod
   |
   +-- Shared Network Namespace
   |
   +-- Shared Volumes
```

Therefore:
```
Container A
     |
     +---- localhost ----+
     |                   |
     |                   v
     |              Container B
     |
     +---- Shared Volume ----+
                             |
                             v
                       Container B
```

---

# 35. What Containers Do NOT Automatically Share
Do not assume containers share everything.
They do **not** automatically share:
```
Filesystem
Processes
Environment variables
Container image
Working directory
Root filesystem
```
Each container has its own filesystem.

Example:
```
Container A
   |
   +-- /app

Container B
   |
   +-- /app
```

These are separate filesystems unless a shared volume is mounted.

---

# 36. Process Namespace
By default, containers have isolated process namespaces.
Therefore Container A does not automatically see all processes of Container B.

However, Kubernetes supports configurations such as:
```
shareProcessNamespace: true
```

Example:
```
apiVersion: v1
kind: Pod

metadata:
  name: shared-process

spec:
  shareProcessNamespace: true

  containers:
    - name: app
      image: nginx

    - name: debug
      image: busybox
      command:
        - sh
        - -c
        - sleep 3600
```
With process namespace sharing enabled, containers can see each other's processes.

This is more advanced, but useful for CKS.

---

# 37. Multi-Container Pod Design Rules
A good rule is:
Put containers together when they need

```
Same lifecycle
+
Same network
+
Shared storage
+
Tight coupling
```
Examples:
```
Application + logging sidecar
Application + proxy sidecar
Application + monitoring helper
Application + configuration helper
```

Keep them separate when they need:
```
Independent scaling
Independent deployment
Independent lifecycle
Independent resource management
```

Examples:
```
Frontend + Backend
Backend + Database
Web + Database
```
usually belong in separate Pods.

---

# 38. CKA/CKS Troubleshooting Checklist
If you see:
```
READY 1/2
```

start thinking:
```
Pod has 2 containers.
One is not Ready.
```

Then:
```
kubectl describe pod <pod>
```
Check logs:
```
kubectl logs <pod> -c <container>
```
Previous crash:
```
kubectl logs <pod> -c <container> --previous
```

Enter container:
```
kubectl exec -it <pod> -c <container> -- /bin/sh
```

Check Pod:
```
kubectl get pod <pod> -o wide
```

Check events:
```
kubectl describe pod <pod>
```

---

# 39. Commands to Memorize

For a multi-container Pod:
```
kubectl get pods
```

```
kubectl describe pod <pod>
```

```
kubectl logs <pod> -c <container>
```

```
kubectl logs -f <pod> -c <container>
```

```
kubectl logs <pod> -c <container> --previous
```

```
kubectl exec -it <pod> -c <container> -- /bin/sh
```

```
kubectl get pod <pod> -o yaml
```

The most important syntax:
```
kubectl logs POD -c CONTAINER
kubectl exec POD -c CONTAINER
```

---

# 40. CKA/CKS Quick Revision
```
Multi-container Pod
        |
        +-- Multiple containers
        |
        +-- Same Pod
        |
        +-- Same Node
        |
        +-- Same Network Namespace
        |
        +-- Same Pod IP
        |
        +-- localhost communication
        |
        +-- Can share volumes
        |
        +-- Shared lifecycle
```

### Sidecar
```
Main Application
       +
Sidecar
```

Used for:
```
Logging
Proxying
Monitoring
Configuration
```

### Init Container
```
Init Container
      |
      v
Completes
      |
      v
Application Containers
```

### Logs
```
kubectl logs pod -c container
```

### Execute
```
kubectl exec -it pod -c container -- /bin/sh
```

### Previous logs
```
kubectl logs pod -c container --previous
```

### Shared storage
```
volumes:
  - name: shared
    emptyDir: {}
```

Mount into both:
```
volumeMounts:
  - name: shared
    mountPath: /some/path
```

---

# 41. One Diagram to Remember
For the CKA/CKS exam, keep this mental picture:
```scss
                         POD
                          |
             +------------+------------+
             |                         |
             v                         v
       Main Container            Sidecar Container
             |                         |
             |                         |
             +-----------+-------------+
                         |
                    Shared Volume
                         |
                  +------+------+
                  |             |
                  v             v
                Files         Files


                    Shared Network
                         |
             +-----------+-----------+
             |                       |
             v                       v
        localhost:8080         localhost:9090
```

The key idea is:
> **Containers in the same Pod are tightly coupled execution environments. They share the Pod's network namespace and can share storage, while each container still has its own filesystem and container-level configuration.**