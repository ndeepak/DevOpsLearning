# Admission Controllers
Admission Controllers are the **security guards** of the Kubernetes API Server.

Most students memorize:
- Authentication
- Authorization
- Admission Controllers

But they never understand **why Kubernetes needed another layer after RBAC**.

This chapter will build that understanding from scratch.


# Chapter 1 — The Complete Journey of a kubectl Request
Let's start with something very simple.

You execute:
```
kubectl run nginx --image=nginx
```

Most people think Kubernetes immediately creates the Pod.

That is **not true**.

The request goes through many stages before anything is stored in etcd.

The complete flow is:
```
kubectl
     │
     ▼
API Server
     │
     ▼
Authentication
     │
     ▼
Authorization
     │
     ▼
Admission Controllers
     │
     ▼
Object Validation
     │
     ▼
Store into etcd
     │
     ▼
Scheduler
     │
     ▼
Kubelet
```

Notice something.

Admission Controllers happen **before the object reaches etcd**.

This is extremely important.

They can stop an object before Kubernetes ever saves it.

# Chapter 2 — Why Authentication Isn't Enough
Suppose Alice executes
```
kubectl apply -f pod.yaml
```

API Server asks
> Who are you?

Alice presents a client certificate.
```
~/.kube/config
↓
certificate-authority-data
client-certificate-data
client-key-data
```

Example
```
users:
- name: alice
  user:
    client-certificate-data: ...
    client-key-data: ...
```

Authentication succeeds.

API Server now knows
```
This request belongs to Alice.
```

Notice:
Authentication **does not ask what Alice wants to do**.

It only verifies identity.

Think of entering an airport.

Security asks:
```
Who are you?
```
Not
```
Can you fly the plane?
```

# Chapter 3 — Authorization
Now Kubernetes asks another question.
```
Is Alice allowed?
```

RBAC decides.

Example
```
kind: Role

rules:

- resources:
  - pods

  verbs:
  - create
```

Now Alice can create Pods.

So far everything looks good.

Authentication:
```
Identity verified
```
Authorization:
```
Permission granted
```
Should Kubernetes now create the Pod?.
Not yet.
Why?
# Chapter 4 — The Big Problem with RBAC
Suppose Alice creates this Pod.
```
apiVersion: v1
kind: Pod

metadata:
  name: evil
spec:
  containers:
  - image: ubuntu:latest
```

RBAC checks
```
Can Alice create Pods?
YES
```

RBAC is finished.

RBAC never checks
```
Which image?
Which tag?
Which registry?
Is it privileged?
Runs as root?
Dangerous capabilities?
Host network?
Host PID?
```

RBAC only understands
```
Resource
Verb
```
It does **not inspect object contents**.

That is a huge limitation.

# Chapter 5 — Imagine a Company Policy
Suppose your company says
```
Only images from
registry.company.com
```
Allowed.

Developer submits
```
image: docker.io/nginx
```
RBAC says
```
Allowed.

Developer can create Pods.
```
But company policy says
```
Rejected.
```

Who enforces this?
Admission Controller.
# Chapter 6 — Admission Controller
Admission Controllers inspect the object itself.
Think of them as
```
Authentication
↓
Who?

Authorization
↓
Can you create Pods?

Admission
↓
What exactly are you creating?
```
Huge difference.
# Chapter 7 — Real Life Analogy
Airport.
Authentication
```
Passport
```
Authorization
```
Valid ticket
```
Admission Controller
```
Open your suitcase.
Any dangerous items?
Liquids?
Weapons?
Explosives?
```
Exactly the same idea.
# Chapter 8 — Admission Controller Can Do Two Things
There are two types.
```
Mutating Admission
Validating Admission
```
These are extremely important.
## Mutating Admission
Mutating means
```
Modify the request.
```

Example.
Developer creates
```
apiVersion: v1
kind: Pod
metadata:
  name: nginx
```
Admission controller changes it into
```
metadata:
  name: nginx
  labels:
    owner: dev-team
```
Developer never wrote that label.
Admission Controller added it.
Another example
Developer forgets
```
imagePullPolicy
```

Admission Controller automatically adds
```
imagePullPolicy: Always
```
Object changed.
No rejection.

## Validating Admission
Validation means
```
Inspect
Accept
Reject
```

Example
Developer submits
```
image: ubuntu:latest
```
Policy
```
latest tag forbidden
```
Admission Controller returns
```
Rejected
Do not use latest.
```
Object never reaches etcd.

# Chapter 9 — Request Flow with Mutation
```
kubectl
     │
Authentication
     │
Authorization
     │
Mutating Admission
     │
Object Modified
     │
Validating Admission
     │
Accepted
     │
Stored in etcd
```

Notice
Validation always happens **after mutation**, because the final object should be validated, not the original one.

# Chapter 10 — Built-in Admission Controllers
Kubernetes ships with many built-in controllers.

Some important ones are:

|Admission Controller|Purpose|
|---|---|
|NamespaceLifecycle|Ensures namespace exists and protects system namespaces|
|LimitRanger|Applies default CPU/memory limits|
|ResourceQuota|Prevents namespace resource overuse|
|ServiceAccount|Automatically injects service accounts|
|DefaultStorageClass|Assigns default StorageClass|
|AlwaysPullImages|Always pulls images|
|NodeRestriction|Restricts kubelets from modifying other nodes|
|PodSecurity|Enforces Pod security standards|
|MutatingAdmissionWebhook|Calls external mutating webhooks|
|ValidatingAdmissionWebhook|Calls external validating webhooks|
For CKS, these are the most important.

# Chapter 11 — NamespaceLifecycle
Suppose
```
kubectl run nginx --image=nginx -n blue
```
Current namespaces
```
default
kube-system
production
```
There is no
```
blue
```
NamespaceLifecycle checks
```
Does namespace exist?
```
Answer
```
No
```

Result
```
Rejected
```
Error
```
namespaces "blue" not found
```
Another responsibility
Try deleting
```
kube-system
```

Admission Controller blocks it.

Why? 
Deleting kube-system would destroy the cluster.
NamespaceLifecycle protects critical namespaces.

# Chapter 12 — AlwaysPullImages
Normally
Node already has
```
nginx:1.29
```
Kubelet may reuse it.

Company policy says
```
Always pull latest approved image.
```

Admission Controller modifies
```
imagePullPolicy
↓
Always
```
Every Pod now downloads the image again.

Useful in shared clusters to avoid stale or poisoned cached images.

# Chapter 13 — DefaultStorageClass
PVC
```
kind: PersistentVolumeClaim
spec:
  resources:
    requests:
      storage: 10Gi
```
n
Developer forgot
```
storageClassName
```

Admission Controller changes
```
storageClassName: standard
```
Automatically.

# Chapter 14 — LimitRanger
Namespace has
```
Default CPU
500m
```

Developer writes
```
containers:
- image: nginx
```

No requests.
Admission Controller injects
```
resources:
  requests:
    cpu: 500m
```
Object modified.
# Chapter 15 — ResourceQuota
Namespace quota
```
Maximum Pods = 5
```
Already running
```
5 Pods
```
Developer creates sixth Pod.

Admission Controller checks
```
Quota exceeded.
```
Rejected.
# Chapter 16 — NodeRestriction
Very important for CKS.
Suppose kubelet on Worker-1 tries
```
Modify Worker-2
```

Without NodeRestriction
A compromised node could alter labels or taints on another node, potentially influencing scheduling.

With NodeRestriction
```
Rejected.
```
A kubelet is limited to operations on its own node and certain objects associated with it.

# Chapter 17 — PodSecurity Admission
Older Kubernetes versions used **PodSecurityPolicy (PSP)**, which has been removed.

Modern Kubernetes uses **Pod Security Admission (PSA)**.

Example
Developer submits
```
securityContext:
  privileged: true
```

Namespace policy
```
restricted
```

Admission Controller
```
Reject.
```

Another example
```
runAsUser: 0
```

Namespace
```
restricted
```
Rejected.

This is heavily tested in CKS.

# Chapter 18 — The Powerful Webhooks
Built-in controllers are useful.

But companies need custom policies.

Example
```
Every Pod
must have
department label.
```
Kubernetes has no built-in controller for that exact rule.

Solution
```
Admission Webhook
```

Request flow
```
API Server
↓
Webhook Server
↓

Approve?
↓
Yes
↓
Store object
```
Your own code decides.

This is how tools like Kyverno and OPA Gatekeeper enforce organisational policies.

# Chapter 19 — Enabling Admission Controllers
Control plane static pod manifest (kubeadm):
```
/etc/kubernetes/manifests/kube-apiserver.yaml
```

Example
```
spec:
  containers:
  - command:
    - kube-apiserver
    - --enable-admission-plugins=NodeRestriction,PodSecurity
```

Disable plugins
```
- --disable-admission-plugins=AlwaysPullImages
```

After editing the manifest, the kubelet automatically restarts the API server because it manages static Pods.

# Chapter 20 — Checking Enabled Admission Controllers
You can inspect the API server options:
```
kube-apiserver --help | grep admission
```
Or, in a kubeadm cluster, inspect the running manifest:
```
grep admission /etc/kubernetes/manifests/kube-apiserver.yaml
```

You may also inspect the running API server Pod:
```
kubectl -n kube-system get pod kube-apiserver-<control-plane-node> -o yaml
```

Look for the `--enable-admission-plugins` and `--disable-admission-plugins` command-line arguments.

# Chapter 21 — A Complete End-to-End Example
Suppose a developer submits:
```
apiVersion: v1
kind: Pod
metadata:
  name: web
spec:
  containers:
  - name: app
    image: docker.io/nginx:latest
    securityContext:
      runAsUser: 0
```
The request flows like this:
```
kubectl apply
        │
        ▼
Authentication
        │
        ▼
Alice identified
        │
        ▼
Authorization
        │
        ▼
Alice can create Pods
        │
        ▼
Mutating Admission
        │
        ├── Add labels
        ├── Add ServiceAccount
        ├── Add default resource requests
        ▼
Validating Admission
        │
        ├── Image registry allowed?
        ├── latest tag allowed?
        ├── runAsUser=0 allowed?
        ├── Pod Security policy satisfied?
        ▼
Rejected
```

The Pod never reaches etcd if validation fails.

# Authentication vs Authorization vs Admission

|Stage|Main Question|Checks|
|---|---|---|
|Authentication|Who are you?|Certificates, tokens, OIDC, service accounts|
|Authorization|Are you allowed to perform this action?|RBAC, ABAC, Node authorizer, Webhook authorizer|
|Admission|Is the object itself acceptable?|Pod spec, security context, labels, quotas, image policies, defaults|

---

# CKA and CKS Exam Notes
For **CKA**, focus on:
- Understanding the request flow through the API server.
- Knowing the purpose of common built-in admission controllers such as `NamespaceLifecycle`, `LimitRanger`, `ResourceQuota`, `ServiceAccount`, and `DefaultStorageClass`.
- Knowing where the API server manifest is located in a kubeadm cluster and how admission plugins are enabled or disabled.

For **CKS**, go deeper:
- Understand the difference between **mutating** and **validating** admission.
- Understand **Pod Security Admission** and why **PodSecurityPolicy** is deprecated and removed.
- Know why `NodeRestriction` is important for node isolation.
- Understand admission webhooks and how policy engines such as **Kyverno** and **OPA Gatekeeper** integrate with the API server.
- Be able to reason about why a Pod is rejected before it is stored in etcd.

The key mental model to remember is this:
```
kubectl
    │
    ▼
Authentication
    │
    ▼
Authorization
    │
    ▼
Mutating Admission
    │
    ▼
Validating Admission
    │
    ▼
API Object Validation
    │
    ▼
etcd
    │
    ▼
Scheduler
    │
    ▼
Kubelet
```

If you keep this pipeline in mind, almost every admission-controller question in the CKA and CKS exams becomes much easier to reason about.