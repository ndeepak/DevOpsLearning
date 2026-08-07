# ConfigMaps in Kubernetes
ConfigMaps are one of the most important Kubernetes objects and are frequently tested in the CKA exam.
Most tutorials simply say:
> "ConfigMaps store configuration."

That is true, but it doesn't explain **why ConfigMaps exist**.

Let's build the concept from scratch.

---

# Why Do We Need ConfigMaps?
Imagine you have a web application.
```
DATABASE_HOST = "mysql"
DATABASE_PORT = "3306"
APP_COLOR = "blue"
LOG_LEVEL = "INFO"
APP_MODE = "production"
```

Everything is hardcoded.

What happens if tomorrow you deploy the same application to another environment?

Development
```
DATABASE_HOST=dev-mysql
```

Testing
```
DATABASE_HOST=test-mysql
```

Production
```
DATABASE_HOST=prod-mysql
```

You would have to edit the source code every time.

This is bad practice.

---

A better approach is

```
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
APP_COLOR = os.getenv("APP_COLOR")
```

Now configuration comes from outside the application.

But then another question appears.

Where should Kubernetes store these values?

Answer
```
ConfigMap
```

---

# What is a ConfigMap?
A ConfigMap is simply a Kubernetes object that stores

> Non-sensitive configuration as key-value pairs.

Think of it as a dictionary.

```
ConfigMap
------------------------

APP_COLOR = blue
APP_MODE = production
DB_HOST = mysql
PORT = 8080

------------------------
```

Notice
These are exactly the same environment variables we manually wrote before.

Instead of storing them inside the Pod YAML,

we store them separately.

---

# Why Not Put Everything Inside the Pod?
Without ConfigMap
```
env:
- name: APP_COLOR
  value: blue

- name: DB_HOST
  value: mysql

- name: APP_MODE
  value: production

- name: LOG_LEVEL
  value: INFO

- name: PORT
  value: "8080"
```

Imagine 50 Pods.

You would repeat this configuration 50 times.

Problems

- Duplicate configuration
- Difficult maintenance
- Error-prone
- Hard to update

---

Instead

```
                 ConfigMap

      APP_COLOR = blue

      APP_MODE = production

      DB_HOST = mysql

      PORT = 8080

            ▲
            │
   ┌────────┼─────────┐
   │        │         │
   ▼        ▼         ▼

 Pod A    Pod B     Pod C
```

One ConfigMap

Many Pods

---

# ConfigMap vs Environment Variables

Previously we wrote

```
env:
- name: APP_COLOR
  value: blue
```

Now

```
env:

- name: APP_COLOR

  valueFrom:

    configMapKeyRef:
      name: app-config
      key: APP_COLOR
```

Notice

The environment variable still exists.

Only the source changed.

Instead of

```
Pod YAML

↓

APP_COLOR=blue
```

we now have

```
ConfigMap

↓

APP_COLOR=blue

↓

Pod

↓

Application
```

---

# ConfigMap Architecture

```
                ConfigMap

      APP_COLOR=blue

      DB_HOST=mysql

      PORT=8080

             │

             ▼

      Kubernetes API Server

             │

             ▼

           kubelet

             │

             ▼

        Container Runtime

             │

             ▼

Application Process

APP_COLOR=blue
```

Notice

The application still receives environment variables.

ConfigMap is simply where Kubernetes stores those values.

---

# Ways to Create ConfigMaps

There are two methods.

```
ConfigMap

├── Imperative

└── Declarative
```

You must know both for the CKA exam.

---

# Method 1

## Imperative Approach

Imperative means

> Create it directly from the command line.

General syntax

```
kubectl create configmap <config-name> \
--from-literal=<key>=<value>
```

Example

```
kubectl create configmap app-config \
--from-literal=APP_COLOR=blue \
--from-literal=APP_MODE=prod
```

Notice

Every variable becomes a key.

Result

```
ConfigMap
APP_COLOR

↓
blue

APP_MODE

↓

prod
```

---

Verify

```
kubectl get configmaps
```

Example

```
NAME

app-config
```

or

```
kubectl get cm
```

`cm` is the short name.

---

View details

```
kubectl describe configmap app-config
```

Example

```
Name: app-config

Data

====

APP_COLOR:

blue

APP_MODE:

prod
```

Notice

Only data is stored.

---

# Creating from Multiple Literals

Example

```
kubectl create configmap app-config \
--from-literal=APP_COLOR=blue \
--from-literal=APP_MODE=production \
--from-literal=DB_HOST=mysql \
--from-literal=DB_PORT=3306
```

Result

```
ConfigMap

APP_COLOR

APP_MODE

DB_HOST

DB_PORT
```

---

# Creating from a File
Suppose you already have
```
app_config.properties
```

Contents
```
APP_COLOR=blue
APP_MODE=production
DB_HOST=mysql
DB_PORT=3306
```

Create
```
kubectl create configmap app-config \
--from-file=app_config.properties
```

Kubernetes reads the file.

---

Important
If the file looks like
```
APP_COLOR=blue

APP_MODE=production
```

Kubernetes creates
```
APP_COLOR
↓
blue

APP_MODE
↓
production
```

---

You can also create from an entire directory.
Example
```
kubectl create configmap app-config \
--from-file=./config/
```

Each file becomes one key.
Suppose
```
config/

database.conf

app.conf

nginx.conf
```

Result
```
ConfigMap

database.conf

app.conf

nginx.conf
```

The file contents become the values.

---

# Method 2
## Declarative Approach
Instead of CLI
Create YAML.

```
apiVersion: v1

kind: ConfigMap

metadata:

  name: app-config

data:

  APP_COLOR: blue

  APP_MODE: production

  DB_HOST: mysql

  DB_PORT: "3306"
```

Apply
```
kubectl apply -f configmap.yaml
```

Verify
```
kubectl get cm
```

Describe
```
kubectl describe cm app-config
```

---

# Why Declarative is Preferred
Suppose your ConfigMap contains 100 variables.
Would you like to type
```
kubectl create configmap ...
```
with 100 literals?
No.

Instead
```
data:
  APP_COLOR: blue
  APP_MODE: production
  DB_HOST: mysql
```

can be stored in Git.

Version controlled.

Reviewed.

Updated.

Re-applied.

This is the GitOps approach.

---

# Using ConfigMaps Inside Pods

Now comes the important part.

Creating a ConfigMap alone does nothing.

Pods must consume it.

There are three primary methods.

```
ConfigMap
↓

Environment Variables
↓

Single Variable
↓

Volume
```

We'll study each.

# Method 1
## Import One Key
ConfigMap
```
APP_COLOR=blue
APP_MODE=production
```

Pod
```
apiVersion: v1
kind: Pod
metadata:
  name: webapp

spec:
  containers:
  - name: webapp
    image: simple-webapp
    env:
    - name: APP_COLOR
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: APP_COLOR
```

Flow

```
ConfigMap
APP_COLOR=blue
↓
Pod
↓
APP_COLOR=blue
↓
Application
```

Only one key is imported.

---

# Method 2
## Import Entire ConfigMap

Instead of listing every variable.

```
envFrom:

- configMapRef:

    name: app-config
```

Suppose

ConfigMap

```
APP_COLOR=blue

APP_MODE=production

DB_HOST=mysql

PORT=8080
```

The application receives

```
APP_COLOR=blue

APP_MODE=production

DB_HOST=mysql

PORT=8080
```

Automatically.

Visualization

```
ConfigMap

↓

All Keys

↓

Pod Environment

↓

Application
```

This is the most common method.

---

# Method 3

## Mount ConfigMap as a Volume

Instead of environment variables.

Create files.

```
volumes:

- name: app-config-volume

  configMap:

    name: app-config
```

Mount

```
volumeMounts:

- name: app-config-volume

  mountPath: /etc/config
```

Suppose

ConfigMap

```
APP_COLOR=blue

DB_HOST=mysql
```

Inside the container

```
/etc/config/

APP_COLOR

DB_HOST
```

Each key becomes a file.

Contents

```
$ cat /etc/config/APP_COLOR

blue
```

This approach is common for applications like NGINX, Apache, and Prometheus that expect configuration files rather than environment variables.

---

# Complete Flow

```
Developer

      │

      ▼

ConfigMap

      │

      ▼

API Server

      │

      ▼

Pod

      │

      ▼

Environment Variables

      │

      ▼

Application
```

---

# Updating a ConfigMap

Suppose

```
APP_COLOR=blue
```

Later

```
APP_COLOR=green
```

Run

```
kubectl apply -f configmap.yaml
```

Does the running Pod immediately see the new value?

It depends on **how the ConfigMap is consumed**.

### If used as Environment Variables

```
env:
```

or

```
envFrom:
```

**No.**

The running Pod does **not** get updated.

Why?

Because environment variables are read **only when the process starts**.

You must restart the Pod (or perform a Deployment rollout).

---

### If Mounted as a Volume

The mounted files are updated automatically (typically within about a minute, depending on the kubelet sync period).

Example

```
ConfigMap Updated

↓

Mounted File Updated

↓

Application can read new file
```

However, many applications read configuration only during startup, so they may still require a reload or restart to use the new values.

---

# ConfigMap vs Secret

This is a common CKA interview question.

|ConfigMap|Secret|
|---|---|
|Stores non-sensitive data|Stores sensitive data|
|Plain text in the API|Base64-encoded in the API (not encryption by itself)|
|App configuration|Passwords, API keys, certificates|
|Example: APP_COLOR|Example: DB_PASSWORD|

Remember:

**Secrets are not encrypted by default simply because they are Base64 encoded.** Base64 is an encoding format, not a security mechanism. Real protection comes from enabling encryption at rest and proper RBAC.

---

# Imperative vs Declarative

## Imperative

Quick.

Useful during exams.

```
kubectl create configmap app-config \
--from-literal=APP_COLOR=blue
```

---

## Declarative

Best for production.

```
apiVersion: v1
kind: ConfigMap

metadata:

  name: app-config

data:

  APP_COLOR: blue
```

```
kubectl apply -f configmap.yaml
```

---

# CKA Exam Tips

1. `ConfigMap` stores **non-sensitive** configuration only.
2. Learn the three ways to create a ConfigMap:
    - `--from-literal`
    - `--from-file`
    - Declarative YAML
3. Learn the three ways to consume a ConfigMap:
    - `env` with `configMapKeyRef` (single key)
    - `envFrom` with `configMapRef` (all keys)
    - As a mounted volume (files)
4. Updating a ConfigMap **does not update environment variables** in running Pods. A Pod restart or rollout is required.
5. Mounted ConfigMap volumes are updated automatically by the kubelet, but your application may still need to reload the changed files.
6. Useful commands to remember:

```
# Create from literals
kubectl create configmap app-config \
  --from-literal=APP_COLOR=blue \
  --from-literal=APP_MODE=production

# Create from a file
kubectl create configmap app-config \
  --from-file=app_config.properties

# View ConfigMaps
kubectl get configmaps
kubectl get cm

# Describe a ConfigMap
kubectl describe configmap app-config

# Export YAML
kubectl get configmap app-config -o yaml

# Delete
kubectl delete configmap app-config
```

A solid mental model is:

```
Application
      ▲
      │
Environment Variables or Files
      ▲
      │
ConfigMap
      ▲
      │
Kubernetes API
```

The ConfigMap is simply a centralized configuration store. Kubernetes injects its data into your Pods as environment variables or files, and the application consumes those values at runtime.