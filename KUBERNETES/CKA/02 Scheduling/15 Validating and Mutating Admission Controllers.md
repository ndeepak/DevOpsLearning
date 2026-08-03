# Validating and Mutating Admission Controllers
This topic is heavily tested because almost every enterprise Kubernetes cluster today uses admission webhooks through products like:
- Kyverno
- OPA Gatekeeper
- Kubewarden
- Falco (partially)
- Custom internal policy engines

The biggest confusion among students is:
> "What is the difference between an Admission Controller and an Admission Webhook?"

By the end of this lesson, you'll understand the entire request flow from the API server's perspective.

---

# Chapter 1 — First Correct a Common Misunderstanding
> DefaultStorageClass is a validating admission controller.

That is **not correct**.

Think about what DefaultStorageClass does.

Suppose you create:
```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim

spec:
  accessModes:
  - ReadWriteOnce

  resources:
    requests:
      storage: 1Gi
```

Notice
```
storageClassName
```
does not exist.

After admission
```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim

spec:
  accessModes:
  - ReadWriteOnce

  storageClassName: standard

  resources:
    requests:
      storage: 1Gi
```

Question:
Who added
```
storageClassName: standard
```
?

Kubernetes.

So the object was **modified**.

That makes DefaultStorageClass a **mutating admission controller**, not a purely validating one.

This leads us to the first important concept.

---

# Chapter 2 — Two Families of Admission Controllers
There are only two kinds.
```
Admission Controllers
        |
  ---------------------
  |                   |
Mutating          Validating
```

Everything belongs to one of these.

---

## Mutating
Mutating means
```
Change the object.
```

Examples
```
Before
imagePullPolicy missing
↓
After
imagePullPolicy: Always
```

or
```
Before
No labels
↓
After
labels:
   owner: team-a
```

or
```
Before
No ServiceAccount
↓
After
serviceAccountName: default
```

The object changes.

---

## Validating
Validation means
```
Inspect.
Accept or Reject.
```

Nothing changes.

Example
```
runAsRoot?

YES

↓

Reject
```

Another
```
Image from DockerHub?

YES

↓

Reject
```

No modification.

Only decision.

---

# Chapter 3 — Why Two Different Controllers?
Imagine your company has this policy.

```
Every Pod
must have
environment label.
```

Developer writes
```
metadata:

  name: nginx
```

No labels.

There are two possible approaches.

Approach 1
Reject.
```
ERROR
Missing label.
```

Developer fixes YAML.

Approach 2
Automatically add
```
labels:
   environment: production
```
No rejection.
Pod created.


One is
```
Validation
```

One is
```
Mutation
```

---

# Chapter 4 — Why Mutation Runs First
Suppose the request is
```
metadata:
  labels: {}
```

Policy
```
Every Pod
must contain
team label.
```

If validation runs first
```
Missing label
↓
Reject
```

Developer gets error.

But suppose mutation runs first.

```
Mutation
↓

Adds

team=backend

↓

Validation

↓

Label exists

↓

Success
```

This is exactly why Kubernetes executes
```
Mutating
↓
Validating
```

in that order.

---

# Chapter 5 — Complete Request Pipeline
Let's build the complete API Server pipeline.

```
kubectl apply
        |
        ▼
Authentication
        |
        ▼
Authorization
        |
        ▼
Built-in Mutating Admission Controllers
        |
        ▼
Mutating Admission Webhooks
        |
        ▼
Built-in Validating Admission Controllers
        |
        ▼
Validating Admission Webhooks
        |
        ▼
Store into etcd
```

This is the actual order.

---

# Chapter 6 — Built-in vs External
This is another area where many students become confused.

There are two completely different things.
Built-in
```
Compiled

inside kube-apiserver.
```

Examples
```
NamespaceLifecycle

ServiceAccount

LimitRanger

DefaultStorageClass

AlwaysPullImages
```

These already exist.

You only enable or disable them.

---

External
You write your own server.

```
Python

Go

Java

NodeJS

Rust
```

API Server calls your server.

This is called
```
Admission Webhook
```

---

# Chapter 7 — Why Webhooks Exist
Suppose your company policy says

```
Every deployment

must have

owner label
```

Kubernetes has no built-in controller for that.

Or

```
Image tag

must match

release number
```

Again
No built-in controller.

Need custom logic.

Solution
```
Webhook
```

---

# Chapter 8 — API Server Calls Your Server
Normally
```
kubectl

↓

API Server

↓

etcd
```

With webhook
```
kubectl
↓

API Server
↓

Webhook Server
↓

API Server
↓

etcd
```

Notice
The API Server temporarily pauses.

It waits for your webhook.

---

# Chapter 9 — AdmissionReview
How does API Server talk to your webhook?
It sends
```
AdmissionReview
```

This is just JSON.

Think of it as
```
Question
↓
API Server
↓
Webhook
```

Example
```
{
  "request": {
    "uid":"123",
    "operation":"CREATE",
    "userInfo":{
       "name":"alice"
    },
    "object":{
       ...
    }
  }
}
```

The webhook now knows
```
Who?

What?

Operation?

Object?

Namespace?

Resource?
```

Everything.

---

# Chapter 10 — UID
Notice
```
"uid"
```

This is extremely important.

Every request gets a unique ID.

Example
```
Request

UID

ABC123
```

Webhook must return
```
Response

UID

ABC123
```

Why?
Imagine 10,000 requests.

The API Server must know which response belongs to which request.

Exactly like TCP sequence numbers or HTTP request IDs.

---

# Chapter 11 — Validating Webhook
Suppose company policy says
```
No latest tag.
```

Developer submits
```
image:

nginx:latest
```

Webhook receives
```
object:

spec:

containers
```

Webhook checks
```
EndsWith(latest)?

YES
```

Returns
```
allowed:false
```

API Server returns
```
Forbidden

latest tag prohibited
```

Pod never exists.

---

# Chapter 12 — Mutating Webhook
Developer writes
```
metadata:

labels: {}
```

Webhook adds
```
labels:

createdBy: Alice
```

Response
```
Allowed

Patch attached
```

API Server applies the patch.

Stores modified object.

---

# Chapter 13 — Why Patch?
Many beginners think the webhook sends the whole object back.

It doesn't.

Imagine a Deployment with 300 lines.

Returning the entire object would be wasteful.

Instead, the webhook returns only the changes using **JSON Patch** (RFC 6902).

Example
Original

```
labels: {}
```

Patch

```
[
 {
   "op":"add",

   "path":"/metadata/labels/team",

   "value":"backend"
 }
]
```

The API Server applies the patch internally.

Result
```
labels:

   team: backend
```

Much more efficient.

---

# Chapter 14 — Understanding JSON Patch
The Python example shows
```
patch = [
  {
      "op":"add",
      "path":"/metadata/labels/users",
      "value":user_name
  }
]
```

Let's understand each field.

### op
Operation.

Possible values
```
add

replace

remove

copy

move

test
```

Example
```
add
```

means
```
Create this field.
```

---

### path
```
Where?
```

Example
```
/metadata/labels/team
```

Means
```
metadata

↓

labels

↓

team
```

Exactly like filesystem paths.

---

### value
```
What should be inserted?
```

Example
```
backend
```

API Server inserts
```
labels:

   team: backend
```

---

# Chapter 15 — Base64 Encoding
The article encodes the patch.

```
base64.b64encode(...)
```

Question
Why?
Not for encryption.

Not for security.

The AdmissionReview API expects the patch bytes to be Base64 encoded because JSON cannot directly embed arbitrary binary data.

The API Server simply decodes it before applying the patch.

---

# Chapter 16 — Deploying the Webhook
Your webhook is just another application.
Example
```
Flask
↓

Container
↓

Deployment
↓

Service
```

Typical architecture
```
Deployment
↓

Pods
↓

Service
↓

WebhookConfiguration
```

The API Server contacts the Service, which forwards the request to one of the webhook Pods.

---

# Chapter 17 — ValidatingWebhookConfiguration
This object tells Kubernetes:
```
"When should I call this webhook?"
```

Example
```
rules:
- operations:
  - CREATE
  resources:
  - pods
```

Meaning
```
Every Pod creation
↓

Call webhook
```

Not updates.

Not deletes.

Only creates.

---

# Chapter 18 — clientConfig
One of the most important fields.
```
clientConfig:
  service:
      namespace: webhook
      name: webhook-service
```

This tells the API Server where the webhook is located.

```
API Server
↓
webhook-service
↓
Pods
```

The API Server does not know Pod IPs directly; it uses the Service abstraction.

---

# Chapter 19 — caBundle
Communication uses HTTPS.

The API Server must trust the webhook's certificate.
```
caBundle:
```

contains the CA certificate used to verify the webhook server's TLS certificate.

Without a trusted CA, the API Server will reject the TLS connection.

---

# Chapter 20 — Real Enterprise Example
Suppose a bank has these rules:
```
1. No DockerHub images.

2. No root user.

3. CPU request mandatory.

4. Every Pod must have owner label.

5. No hostPath volumes.

6. No latest tag.

7. Must use internal registry.
```

Workflow
```
Developer

↓

kubectl apply

↓

Authentication

↓

Authorization

↓

LimitRanger

↓

ServiceAccount

↓

Mutating Webhook

Adds owner label

↓

Validating Webhook

Checks image registry

Checks root user

Checks hostPath

Checks latest tag

↓

Accepted

↓

Stored in etcd
```

This is how most production Kubernetes clusters enforce security and governance.

---

# Chapter 21 — Why Kyverno and OPA Gatekeeper Are So Popular
Notice something.

Everything we've discussed is generic.

Instead of writing Python or Go yourself, tools such as **Kyverno** and **OPA Gatekeeper** provide ready-made webhook servers.

You simply define policies.

Example (conceptually):
```
Disallow latest image tag.

Disallow privileged Pods.

Require labels.

Require CPU limits.
```

The policy engine evaluates every AdmissionReview and returns either:

```
allowed = true
```

or
```
allowed = false
```

No custom application code is required.

---

# Interview Question
A common interview question is:
> Why can't RBAC stop a user from using `nginx:latest`?

Correct answer:
RBAC authorizes **API operations** (such as `create`, `update`, `delete`) on Kubernetes resources. It does **not inspect the contents** of the object being created. Checking fields like image names, tags, security contexts, labels, or capabilities requires **admission controllers** (built-in or webhook-based), which examine and optionally modify the object before it is stored in etcd.

---

# CKA vs CKS Exam Focus
## CKA
Know:
- The API request flow.
- The difference between mutating and validating admission.
- The purpose of common built-in admission controllers.
- The roles of `MutatingWebhookConfiguration` and `ValidatingWebhookConfiguration`.

## CKS
Understand in depth:
- Why mutating admission runs before validating admission.
- The structure and purpose of an `AdmissionReview` request and response.
- How JSON Patch is used to modify objects.
- How webhook servers are deployed behind a Kubernetes Service with TLS.
- How policy engines like Kyverno and OPA Gatekeeper rely on admission webhooks to enforce security policies.