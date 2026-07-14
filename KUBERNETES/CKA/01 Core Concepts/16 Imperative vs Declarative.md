# Imperative VS Declarative

[08 Imperative vs Declarative](KUBERNETES/KCNA/2%20Kubernetes%20Resources/08%20Imperative%20vs%20Declarative.md)


# Imperative vs Declarative in Kubernetes

## Introduction

One of the most important concepts in Kubernetes is **how you manage cluster resources**.

There are two approaches:

1. **Imperative**
2. **Declarative**

These are not Kubernetes-specific concepts. They originated from software engineering and Infrastructure as Code (IaC), and Kubernetes adopted both methods.

Understanding these approaches is essential because every Kubernetes administrator, DevOps engineer, or platform engineer uses them daily.

---

# What is Imperative?

An **Imperative approach** tells the system **exactly how to perform every step**.

Think of it as giving instructions one by one.

You are responsible for telling Kubernetes:

- What to create
- When to create it
- How to update it
- What to delete

In simple words:

> "Do this, then do that, then change this."

The system simply follows your commands.

---

## Real World Example

Imagine you ask someone to make tea.

Imperative instructions would be:

```
1. Boil water
2. Add tea leaves
3. Add sugar
4. Add milk
5. Boil for 3 minutes
6. Pour into cup
```

Every step is specified.

---

## Infrastructure as Code Example

Suppose you want a web server.

Imperative approach:

```
1. Create a VM called web-server
2. Install nginx
3. Edit nginx.conf
4. Change port to 8080
5. Change web root to /var/www/nginx
6. Clone website from Git
7. Start nginx
8. Enable nginx service
```

Every action is executed manually or through commands/scripts.

Example shell script:

```
#!/bin/bash

apt install nginx -y

sed -i 's/80/8080/g' /etc/nginx/sites-enabled/default

mkdir -p /var/www/nginx

git clone https://github.com/example/project.git /var/www/nginx

systemctl restart nginx

systemctl enable nginx
```

The script explains _how_ everything should happen.

---

# Declarative Approach
Declarative means:
You describe the **desired final state**, not the steps.

Instead of saying:
```
Install nginx
Change port
Start service
```

You simply declare:
```
VM Name: web-server
Software: nginx
Port: 8080
Path: /var/www/nginx
Website: Git Repository X
```

The automation tool determines the necessary actions.

---

## Real World Example
Instead of explaining every step, you simply say:

```
I want one cup of tea with:
- Milk
- Sugar
- Medium strength
```

You don't care how the tea is made.

You only care about the final result.

---

## Infrastructure as Code Example
Example Ansible Playbook
```
---
- hosts: webservers

  tasks:

    - name: Install nginx
      apt:
        name: nginx
        state: present

    - name: Copy configuration
      template:
        src: nginx.conf
        dest: /etc/nginx/nginx.conf

    - name: Clone website
      git:
        repo: https://github.com/example/project.git
        dest: /var/www/nginx

    - name: Start nginx
      service:
        name: nginx
        state: started
```

Notice there is no shell script describing every command.

You only declare the desired state.

Ansible decides what actions are required.

---

# Imperative vs Declarative Comparison

|Imperative|Declarative|
|---|---|
|Describes steps|Describes desired state|
|User controls execution|System controls execution|
|Manual commands|Configuration files|
|Good for quick tasks|Good for production|
|Difficult to maintain|Easy to maintain|
|Easy to make mistakes|Less error-prone|
|Hard to reproduce|Easily reproducible|
|Not version friendly|Git friendly|

---

# Why Kubernetes Supports Both
Kubernetes is designed to be flexible.
Sometimes you need quick testing.
Sometimes you need production-grade deployments.
Therefore Kubernetes provides both methods.

---

# Imperative Kubernetes
Imperative Kubernetes means:
You interact directly with the Kubernetes API using commands.

Examples:
```
kubectl run
kubectl create
kubectl expose
kubectl scale
kubectl edit
kubectl delete
```

Every command immediately changes the cluster.

---

# Example 1
Create an nginx Pod
```
kubectl run nginx --image=nginx
```

What happens?
```
User
   │
   ▼
kubectl
   │
   ▼
API Server
   │
   ▼
Pod Created
```

No YAML file exists.

The cluster changes immediately.

---

# Example 2
Create a Deployment
```
kubectl create deployment nginx --image=nginx
```

Deployment created.
No YAML file.

---

# Example 3
Expose Deployment
```
kubectl expose deployment nginx --port=80
```

Service gets created.

---

# Example 4
Scale Deployment
```
kubectl scale deployment nginx --replicas=5
```

Current replicas:
```
1
```
After command:

```
5
```
---

# Example 5
Change Image
Old image
```
nginx:1.19
```

Upgrade
```
kubectl set image deployment nginx nginx=nginx:1.25
```

Deployment performs a rolling update.

---

# Example 6
Edit Deployment
```
kubectl edit deployment nginx
```

Kubernetes opens the object in your editor.

You edit fields directly.
When saved:
```
Editor
    │
    ▼
API Server Updated
```

No YAML file is stored locally.

---

# Example 7
Delete Deployment
```
kubectl delete deployment nginx
```

Deployment disappears immediately.

---

# Problems with Imperative Approach
Suppose your cluster contains:
```
Deployment
Service
ConfigMap
Secret
Ingress
Persistent Volume
```

Everything was created using commands.
A month later someone asks:
"How was this cluster created?"

You have no record.
No YAML.
No Git history.
No rollback.
This is one of the biggest disadvantages.

---

# Creating Objects Imperatively from YAML
Imperative does not always mean "without YAML."
You can still use YAML.

Example:
```
kubectl create -f nginx.yaml
```

Creates resources defined inside the file.

Example YAML
```
apiVersion: apps/v1

kind: Deployment

metadata:
  name: nginx

spec:
  replicas: 2

  selector:
    matchLabels:
      app: nginx

  template:

    metadata:
      labels:
        app: nginx

    spec:

      containers:

      - name: nginx

        image: nginx
```

Create:
```
kubectl create -f nginx.yaml
```

Output
```
deployment.apps/nginx created
```

---

# Updating Objects Imperatively
There are several methods.
## Method 1
Edit directly
```
kubectl edit deployment nginx
```

---

## Method 2
Replace
Modify YAML
Then
```
kubectl replace -f nginx.yaml
```

The API server replaces the object.

---

## Method 3
Force Replace
```
kubectl replace --force -f nginx.yaml
```

This does:
```
Delete object
↓
Create new object
```

Equivalent to
```
kubectl delete
kubectl create
```

Because the object is recreated:
- UID changes
- Pod names change
- Temporary downtime may occur

This is generally not recommended for Deployments in production.

---

# Difference Between create and replace
Suppose Deployment already exists.
```
kubectl create -f nginx.yaml
```

Output
```
AlreadyExists
```

It fails.

---

Replace
```
kubectl replace -f nginx.yaml
```

Existing object is replaced.

---

# Declarative Kubernetes
Declarative Kubernetes revolves around one command:
```
kubectl apply -f
```
You never tell Kubernetes:
```
Create this
Update this
Delete this
```

Instead you say:
```
This file represents the desired state.
Make the cluster match it.
```

Kubernetes determines whether to create or update the object.

---

# Example
File
```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
```

Apply
```
kubectl apply -f nginx.yaml
```

If deployment does not exist
```
Created
```

If deployment exists
```
Updated
```

Same command.

---

# Why apply is Powerful
Suppose your file changes.

Old
```
replicas: 2
```

New
```
replicas: 5
```

Run
```
kubectl apply -f nginx.yaml
```

Kubernetes notices:
```
Current
Replicas = 2
Desired
Replicas = 5
```

Only that field is updated.

Nothing else changes.

---

# Applying Multiple Files
Instead of one file:
```
deployment.yaml
service.yaml
configmap.yaml
secret.yaml
```

Run
```
kubectl apply -f .
```

or
```
kubectl apply -f ./k8s
```

Every YAML file inside the directory is applied.

---

# How apply Works Internally
Suppose current Deployment:
```
Replicas = 2

Image = nginx:1.19
```

Desired YAML

```
Replicas = 5

Image = nginx:1.25
```

When you run

```
kubectl apply -f deployment.yaml
```

Kubernetes compares:
```
Current Cluster
↓
Desired YAML
↓
Difference
↓
Patch
↓
Update Only Changed Fields
```

This process is called a **three-way merge** in client-side apply (historically) or uses **Server-Side Apply** (SSA) in modern Kubernetes when invoked with `--server-side`. In both cases, Kubernetes determines the differences and updates only the necessary fields instead of recreating the object.

---

# Why Declarative is Preferred
Because everything exists as code.
Example project
```
kubernetes/
    deployment.yaml
    service.yaml
    ingress.yaml
    configmap.yaml
    secret.yaml
```

Store this in Git.

Benefits
- Version control
- Rollback
- Code review
- Auditing
- CI/CD integration
- Team collaboration
- Easy disaster recovery

If the cluster is destroyed:
```
kubectl apply -f kubernetes/
```

Everything is recreated.

---

# Real Production Workflow
Developer updates
```
deployment.yaml
```

Commits
```
git commit
```

Pushes
```
Git Repository
```

CI/CD pipeline
```
GitHub Actions
GitLab CI
Jenkins
ArgoCD
FluxCD
```

Pipeline executes
```
kubectl apply -f kubernetes/
```

Cluster reaches desired state.

Nobody manually logs into the cluster.

---

# Imperative vs Declarative Commands

## Creating a Pod
Imperative
```
kubectl run nginx --image=nginx
```

Declarative
```
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx
```

```
kubectl apply -f pod.yaml
```

---

## Creating Deployment
Imperative
```
kubectl create deployment nginx --image=nginx
```

Declarative
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
```

```
kubectl apply -f deployment.yaml
```

---

## Scaling
Imperative
```
kubectl scale deployment nginx --replicas=10
```

Declarative
Modify
```
replicas: 10
```

Apply
```
kubectl apply -f deployment.yaml
```

---

## Image Upgrade
Imperative
```
kubectl set image deployment nginx nginx=nginx:1.26
```

Declarative
Modify
```
image: nginx:1.26
```

Apply
```
kubectl apply -f deployment.yaml
```

---

# When Should You Use Imperative?
Imperative commands are best suited for:
- Learning Kubernetes concepts.
- Quickly testing an application.
- Debugging resources.
- Performing temporary administrative tasks.
- Verifying behavior in a development cluster.
- Generating an initial YAML file using commands like `kubectl create deployment ... --dry-run=client -o yaml`.

Example:
```
kubectl run test --image=busybox -- sleep 3600
```

This quickly creates a temporary Pod for troubleshooting.

---

# When Should You Use Declarative?
Declarative management is the recommended approach for:
- Production environments.
- CI/CD pipelines.
- GitOps workflows.
- Infrastructure as Code.
- Team collaboration.
- Long-term maintenance.
- Disaster recovery.
- Auditing and version control.

Most modern Kubernetes platforms (such as Argo CD and Flux) continuously compare the cluster's actual state with the desired state stored in Git and automatically reconcile any differences. This model is only practical with declarative configuration.

---

# Best Practices
1. Use imperative commands for experimentation, learning, and quick troubleshooting.
2. Store all production resources as YAML files in a version-controlled repository.
3. Use `kubectl apply` (or Server-Side Apply where appropriate) for managing declarative resources.
4. Avoid manually editing production resources with `kubectl edit`, as those changes are difficult to track and can be overwritten.
5. Organize related manifests (Deployments, Services, ConfigMaps, Secrets, Ingresses, etc.) into a structured directory hierarchy.
6. Treat Kubernetes manifests as source code and review changes through pull requests before applying them.

---

# Summary

|Feature|Imperative|Declarative|
|---|---|---|
|Philosophy|Specify the steps to perform|Specify the desired final state|
|Resource Definition|CLI commands or one-off operations|YAML manifests|
|Primary Commands|`kubectl run`, `create`, `edit`, `scale`, `set image`, `delete`, `replace`|`kubectl apply`|
|State Tracking|Manual|Stored in YAML and typically version-controlled|
|Reproducibility|Limited|High|
|Git Integration|Poor|Excellent|
|Automation|Difficult|Ideal for CI/CD and GitOps|
|Production Suitability|Mainly for testing and administration|Strongly recommended|
|Collaboration|Limited|Excellent|
|Disaster Recovery|Manual recreation|Reapply manifests from Git|
|Learning Curve|Simple to start|Requires understanding Kubernetes object manifests|
|Common Use Cases|Quick tests, debugging, temporary resources|Production deployments, Infrastructure as Code, GitOps, long-term operations|

The key idea is simple:

- **Imperative** means **you tell Kubernetes what actions to perform**.
- **Declarative** means **you tell Kubernetes what the final state should be, and Kubernetes figures out how to achieve and maintain that state**.