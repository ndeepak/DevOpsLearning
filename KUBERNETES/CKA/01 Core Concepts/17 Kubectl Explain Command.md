# Kubectl Explain Command

## Introduction

When working with Kubernetes, you'll frequently create YAML manifest files for resources like Pods, Deployments, Services, ConfigMaps, Secrets, and many others. A common question is:

- What fields are available for a resource?
- Which fields are required?
- What does a particular field mean?
- What data type should a field contain?
- Where can I find the official schema for a Kubernetes object?

The `kubectl explain` command answers these questions directly from your terminal. It acts as a built-in documentation tool for Kubernetes API resources.

Instead of searching the Kubernetes documentation on the web, you can inspect the API schema interactively.

---

# What is `kubectl explain`?

`kubectl explain` displays documentation about Kubernetes resource types and their fields.

It tells you:

- Available fields
- Field descriptions
- Data types
- Whether a field is required
- Nested object structure

Think of it as the Kubernetes equivalent of the Linux `man` command.

Example:

```
man ls
```

shows documentation for the `ls` command.

Similarly,

```
kubectl explain pods
```

shows documentation for the Pod resource.

---

# Why is it Useful?

Suppose you want to create a Pod manually.

```
apiVersion: v1
kind: Pod

metadata:
  name: nginx

spec:
  containers:
```

Questions may arise:

- What comes under `spec`?
- What fields are allowed?
- Is `containers` mandatory?
- What data type is `containers`?
- Can I add `restartPolicy` here?

Instead of searching online:

```
Google
↓
Kubernetes Documentation
↓
Pod API Reference
↓
Search
```

You simply run

```
kubectl explain pods.spec
```

and Kubernetes tells you everything.

---

# Syntax

Basic syntax

```
kubectl explain RESOURCE
```

Nested field

```
kubectl explain RESOURCE.FIELD
```

Recursive documentation

```
kubectl explain RESOURCE --recursive
```

---

# Kubernetes Object Structure

Almost every Kubernetes object follows a similar structure.

```
Object

├── apiVersion
├── kind
├── metadata
├── spec
└── status
```

The `spec` section contains the desired state, while `status` is maintained by Kubernetes and represents the current state.

`kubectl explain` lets you inspect each part of this structure.

---

# Command 1

## `kubectl api-resources`

Before using `kubectl explain`, it's useful to know which resources exist in your cluster.

```
kubectl api-resources
```

Example output

```
NAME          SHORTNAMES   APIVERSION
pods          po           v1
services      svc          v1
deployments   deploy       apps/v1
configmaps    cm           v1
secrets                    v1
nodes         no           v1
namespaces    ns           v1
jobs                       batch/v1
cronjobs      cj           batch/v1
```

This command lists:

- Resource names
- Short names
- API versions
- Whether they are namespaced
- Supported operations (depending on output format)

### Use Cases

- Discover available Kubernetes resources.
- Find the correct resource name for `kubectl explain`.
- Verify Custom Resource Definitions (CRDs) installed in the cluster.

Example

```
kubectl api-resources | grep deploy
```

Output

```
deployments
```

Now you know you can use

```
kubectl explain deployments
```

---

# Command 2

## `kubectl explain pods`

Displays documentation for the Pod resource.

```
kubectl explain pods
```

Example output

```
KIND:     Pod
VERSION:  v1

DESCRIPTION:
     Pod is a collection of containers...

FIELDS:

apiVersion
kind
metadata
spec
status
```

This tells you:

- Resource type
- API version
- Description
- Top-level fields

Visualization

```
Pod

├── apiVersion
├── kind
├── metadata
├── spec
└── status
```

---

# Understanding the Output

Example

```
FIELDS:

metadata
spec
status
```

Suppose you're interested in `spec`.

You can drill down into it.

---

# Command 3

## `kubectl explain pods.spec`

This is one of the most useful forms of the command.

```
kubectl explain pods.spec
```

Example output

```
FIELDS:

containers
initContainers
volumes
dnsPolicy
nodeSelector
restartPolicy
hostNetwork
serviceAccountName
tolerations
affinity
securityContext
```

Now you know every field allowed inside `spec`.

Visualization

```
Pod
└── spec
     ├── containers
     ├── volumes
     ├── affinity
     ├── tolerations
     ├── nodeSelector
     ├── restartPolicy
     ├── hostNetwork
     └── securityContext
```

This is extremely useful when writing YAML manually.

---

# Exploring Nested Fields

Suppose you want information about containers.

```
kubectl explain pods.spec.containers
```

Example

```
DESCRIPTION:
     List of containers belonging to the pod.

TYPE:
     []Container
```

Now inspect Container itself.

```
kubectl explain pods.spec.containers.image
```

Output

```
DESCRIPTION:
     Docker image name.

TYPE:
     string
```

You can continue drilling into almost any field.

Examples

```
kubectl explain pods.metadata
```

```
kubectl explain pods.metadata.labels
```

```
kubectl explain pods.spec.volumes
```

```
kubectl explain pods.spec.restartPolicy
```

---

# Example

Suppose you're unsure where to define the container image.

You know it belongs somewhere under `spec`, but not exactly where.

Step 1

```
kubectl explain pods.spec
```

You see

```
containers
```

Step 2

```
kubectl explain pods.spec.containers
```

You see

```
image
name
ports
resources
env
volumeMounts
```

Step 3

```
kubectl explain pods.spec.containers.image
```

Output

```
TYPE:
string
```

Now you know exactly where to place the image field in your YAML.

---

# Command 4

## `kubectl explain pods --recursive`

This displays the complete schema recursively.

```
kubectl explain pods --recursive
```

Example

```
KIND: Pod
FIELDS:
apiVersion <string>
kind <string>
metadata <Object>
  annotations <map>
  labels <map>
  name <string>
spec <Object>
  containers <[]Object>
     image <string>
     name <string>
     ports <[]Object>
     env <[]Object>
  volumes <[]Object>
  restartPolicy <string>
status <Object>
  phase <string>
  podIP <string>
```

Instead of navigating field by field, recursive mode prints the entire hierarchy.

Visualization

```
Pod

├── metadata
│
│   ├── labels
│   ├── annotations
│   └── name
│
├── spec
│
│   ├── containers
│   │
│   │    ├── image
│   │    ├── name
│   │    ├── ports
│   │    ├── env
│   │    └── resources
│   │
│   ├── volumes
│   ├── affinity
│   ├── tolerations
│   └── restartPolicy
│
└── status
```

---

# Working with Other Resources

The `explain` command works for almost every Kubernetes resource.

Deployment

```
kubectl explain deployments
```

Deployment spec

```
kubectl explain deployments.spec
```

Deployment template

```
kubectl explain deployments.spec.template
```

Container image inside Deployment

```
kubectl explain deployments.spec.template.spec.containers.image
```

---

Service

```
kubectl explain services
```

Service spec

```
kubectl explain services.spec
```

Ports

```
kubectl explain services.spec.ports
```

---

ConfigMap

```
kubectl explain configmaps
```

Secret

```
kubectl explain secrets
```

Job

```
kubectl explain jobs.spec
```

CronJob

```
kubectl explain cronjobs.spec
```

---

# Understanding Data Types

One major advantage of `kubectl explain` is that it shows field types.

Example

```
kubectl explain pods.spec.restartPolicy
```

Output

```
TYPE:
string
```

Example

```
kubectl explain pods.spec.containers
```

Output

```
TYPE:
[]Container
```

Meaning:

- `string` → Text value
- `integer` → Number
- `boolean` → true/false
- `[]Object` → List
- `Object` → Nested object
- `map` → Key-value pairs

This helps prevent YAML syntax and schema errors.

---

# `kubectl explain` vs Documentation

|`kubectl explain`|Kubernetes Documentation|
|---|---|
|Built into `kubectl`|Web-based|
|Works from terminal|Requires browser|
|API schema reference|Detailed guides and tutorials|
|Fast lookup|More comprehensive explanations|
|Cluster-aware|General documentation|

Both are valuable:

- Use `kubectl explain` while writing manifests.
- Use the official documentation for concepts, examples, and best practices.

---

# Common Use Cases

### 1. Learning Kubernetes Objects

Explore the structure of Pods, Deployments, Services, ConfigMaps, Secrets, and more.

---

### 2. Writing YAML Files

Instead of guessing field names, verify them directly.

Example:

```
kubectl explain deployments.spec.strategy
```

---

### 3. Troubleshooting

If you encounter an error like:

```
unknown field "container"
```

You can inspect the schema:

```
kubectl explain pods.spec
```

and discover that the correct field is `containers`.

---

### 4. Exploring New Resources

When working with unfamiliar resources, inspect their structure before creating manifests.

Example:

```
kubectl explain cronjobs.spec
```

---

### 5. Working with Custom Resources

If a Custom Resource Definition (CRD) exposes its OpenAPI schema, you can inspect it using `kubectl explain`, making it useful for third-party operators and extensions.

---

# Best Practices

- Use `kubectl api-resources` to discover available resource types.
- Use `kubectl explain <resource>` to understand the top-level structure.
- Drill down with dot notation (`resource.field.subfield`) to inspect nested fields.
- Use `--recursive` when you want to see the complete object hierarchy at once.
- Combine `kubectl explain` with `kubectl create --dry-run=client -o yaml` to generate and understand manifests efficiently.

---

# Summary

|Command|Purpose|
|---|---|
|`kubectl api-resources`|Lists all available Kubernetes API resources.|
|`kubectl explain pods`|Displays documentation for the Pod resource.|
|`kubectl explain pods.spec`|Shows all fields available under the Pod's `spec`.|
|`kubectl explain pods.spec.containers.image`|Explains a specific nested field.|
|`kubectl explain pods --recursive`|Prints the complete schema recursively.|

In practice, `kubectl explain` is one of the most valuable commands for Kubernetes administrators and developers because it provides instant, authoritative API documentation directly from the command line, making it much easier to write correct YAML manifests and understand Kubernetes resources.