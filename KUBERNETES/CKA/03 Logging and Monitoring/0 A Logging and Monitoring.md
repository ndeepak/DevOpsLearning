# Logging and Monitoring
Logging and Monitoring is one of the most practical topics in Kubernetes. It is  also one of the first things engineers use when troubleshooting production clusters.
Almost every Kubernetes troubleshooting scenario starts with one of these questions:
- Is the cluster healthy?
- Is the node overloaded?
- Is the pod running?
- Why is the application crashing?
- Why is scheduling failing?
- What does the application log say?
- What does the kubelet log say?

This entire topic can be divided into four major sections.
```scss
                 Kubernetes Observability

               +---------------------------+
               |   Monitoring              |
               |---------------------------|
               | CPU                       |
               | Memory                    |
               | Disk                      |
               | Network                   |
               | Pod Usage                 |
               +---------------------------+

                           +

               +---------------------------+
               | Logging                   |
               |---------------------------|
               | Application Logs          |
               | Container Logs            |
               | kubelet Logs              |
               | API Server Logs           |
               | Scheduler Logs            |
               +---------------------------+
```

Monitoring answers:
> "What is happening?"

Logging answers:
> "Why is it happening?"

---

# The Four Topics
## 1. Monitoring Cluster Components
Monitor Kubernetes infrastructure.

Examples
- CPU usage
- Memory usage
- Disk usage
- Network usage
- Number of Pods
- Number of Nodes
- Resource utilization

Typical tools
- Metrics Server
- Prometheus
- Datadog
- Dynatrace

---

## 2. Monitoring Applications
Monitor application-level metrics.
Examples
- HTTP Requests/sec
- Response Time
- Error Rate
- Active Users
- JVM Memory
- Database Connections

Usually done with
- Prometheus
- Grafana
- OpenTelemetry
- Datadog

---

## 3. Monitoring Cluster Component Logs
Cluster components generate logs.

Examples
- kube-apiserver
- kube-scheduler
- kube-controller-manager
- kubelet
- etcd

These logs help troubleshoot Kubernetes itself.

---

## 4. Application Logs
Your application also generates logs.

Example
```
Application Started

Connected to Database

Received Request

Error while processing payment

Null Pointer Exception
```

These are usually viewed using
```
kubectl logs
```

This topic appears frequently in CKA.

---

# Monitoring Cluster Components
Before learning tools, understand what Kubernetes actually monitors.

Suppose we have
```scss
            Kubernetes Cluster

      +-------------------------+
      | Node 1                  |
      | CPU                     |
      | Memory                  |
      | Pods                    |
      +-------------------------+

      +-------------------------+
      | Node 2                  |
      | CPU                     |
      | Memory                  |
      | Pods                    |
      +-------------------------+
```

Every few seconds Kubernetes collects
- CPU
- Memory
- Storage
- Network
- Running Pods

These numbers are called **metrics**.

Metrics are simply numerical measurements collected over time.

Examples
```
CPU = 35%

Memory = 5.2GB

Running Pods = 42

Network RX = 125MB/s

Disk Usage = 60%
```

Notice these are numbers.

Not logs.

---

# Metrics vs Logs
This is one of the biggest concepts.
## Metrics
Metrics answer
> How much?

Examples
```
CPU Usage = 60%

Memory = 4GB

Network = 20Mbps
```

Metrics are
- numbers
- lightweight
- collected every few seconds

---
## Logs
Logs answer
> What happened?

Example
```
10:10 User Login

10:11 API Request

10:12 Database Error

10:13 Payment Failed
```

Logs are text.

---

Comparison

|Metrics|Logs|
|---|---|
|Numbers|Text|
|Continuous|Event based|
|Small|Large|
|Fast|Detailed|
|Used for dashboards|Used for troubleshooting|

---

# Kubernetes Monitoring Solutions
There are many monitoring solutions.
```scss
                Monitoring

        +----------------------+
        | Metrics Server       |
        +----------------------+

        +----------------------+
        | Prometheus           |
        +----------------------+

        +----------------------+
        | Elastic Stack        |
        +----------------------+

        +----------------------+
        | Datadog              |
        +----------------------+

        +----------------------+
        | Dynatrace            |
        +----------------------+
```

Let's understand each one.

---

# 1. Metrics Server
This is the simplest monitoring solution.

Purpose
```
Provide basic CPU and Memory metrics.
```

It is used by
- kubectl top
- Horizontal Pod Autoscaler (HPA)

It is NOT a full monitoring solution.

It stores only recent metrics.

No historical database.

No graphs.

No dashboards.

---

Architecture
```scss
               Metrics Server

                     ^
                     |

             kubelet on every node

                     ^
                     |

                 cAdvisor

                     ^
                     |

                 Containers
```

---

# cAdvisor
Every container runs inside a runtime.
Example
```
containerd

CRI-O

Docker (older clusters)
```

Each container consumes
- CPU
- Memory
- Filesystem
- Network

Something has to measure this.

That component is
```
cAdvisor
```

Container Advisor
It collects container statistics.

Example
```
Container

CPU = 25%

Memory = 300MB

Network = 20MB/s
```

---
# kubelet
Every node runs a kubelet.
```scss
             Node

        +--------------+
        | kubelet      |
        +--------------+

              |

          cAdvisor

              |

         Container Stats
```

The kubelet exposes an API.

Metrics Server contacts kubelet.

Example
```
Metrics Server
        |
HTTPS
        |
kubelet
        |
cAdvisor
        |
Container Metrics
```

---

# Heapster vs Metrics Server
Many students get confused.
## Heapster
Old monitoring solution.
```
Heapster
↓
Collected Metrics
↓
Stored Metrics
↓
Supported HPA
```

Problems
- Too large
- Hard to maintain
- Deprecated
Heapster is completely deprecated.

Never use it in modern Kubernetes.

## Metrics Server
Replacement for Heapster.
Advantages
- Lightweight
- Fast
- Only CPU and Memory
- Supports HPA
CKA expects Metrics Server.

---

Comparison

|Heapster|Metrics Server|
|---|---|
|Deprecated|Current|
|Large|Lightweight|
|Historical|No History|
|Monitoring|Basic Metrics|

---

# Installing Metrics Server
On Minikube
```
minikube addons enable metrics-server
```

Verify
```
kubectl get pods -n kube-system
```

Expected
```
metrics-server
```

---

Manual Installation
```
git clone https://github.com/kubernetes-sigs/metrics-server.git
kubectl apply -f deploy/1.8+/
```

---

Verify
```
kubectl get deployment -n kube-system
```

```
metrics-server
```

---

# How Metrics Server Works
```
Every 15 seconds

Metrics Server
      |
Requests metrics
      |
kubelet
      |
cAdvisor
      |
Containers
```

Metrics Server stores only recent values in memory.

No database.

---

# Viewing Metrics
## Node Metrics
```
kubectl top node
```

Example
```
NAME      CPU(cores)   CPU%   MEMORY(bytes)
node01    200m         10%    850Mi
node02    350m         18%    1.5Gi
```

Explanation
```
200m

means

200 millicores

1 CPU

=

1000m

500m

=

0.5 CPU
```

---

## Pod Metrics
```
kubectl top pod
```

Example
```
NAME
frontend
CPU = 10m
Memory = 45Mi
```

---

All namespaces
```
kubectl top pod --all-namespaces
```

---

Sort
```
kubectl top pod --sort-by=cpu
kubectl top pod --sort-by=memory
```

Very useful in CKA troubleshooting.

---
# Important Exam Points
Metrics Server provides
- CPU
- Memory

It does NOT provide
- Logs
- Network metrics
- Disk metrics
- Historical graphs

---

# Monitoring Applications
Cluster metrics are different from application metrics.

Suppose a Spring Boot application exposes
```
/actuator/prometheus
```

It may return
```
http_requests_total

database_connections

jvm_memory_used

jvm_gc_pause

request_latency
```

These are application metrics.

Prometheus scrapes these metrics.

---

Architecture
```
Application
      |
Exports Metrics
      |
Prometheus
      |
Stores Metrics
      |
Grafana
      |
Dashboards
```

---

# Monitoring Cluster Component Logs
Every Kubernetes component writes logs.

Examples
```
kube-apiserver
kubelet
scheduler
controller-manager
etcd
```

Examples
View kubelet logs (systemd-based nodes):

```
journalctl -u kubelet
```

Follow logs:
```
journalctl -u kubelet -f
```

If control plane components run as static Pods (common with kubeadm):
```
kubectl get pods -n kube-system
```

Example:
```
NAME
kube-apiserver-controlplane
kube-scheduler-controlplane
kube-controller-manager-controlplane
etcd-controlplane
```

View API server logs:
```
kubectl logs -n kube-system kube-apiserver-controlplane
```

View scheduler logs:
```
kubectl logs -n kube-system kube-scheduler-controlplane
```

View controller manager logs:
```
kubectl logs -n kube-system kube-controller-manager-controlplane
```

View etcd logs:
```
kubectl logs -n kube-system etcd-controlplane
```

In managed Kubernetes services (EKS, GKE, AKS), access to control plane logs depends on the provider because the control plane is not hosted on your worker nodes.

---

# Application Logs
Application logs explain what the application is doing.

Example
```
Application Started

Connected to Database

Listening on Port 8080

User Login Success

Database Error
```

---

# Docker Logs
Foreground mode
```
docker run kodekloud/event-simulator
```

The container stays attached to the terminal.

Logs appear directly.

---

Detached mode
```
docker run -d kodekloud/event-simulator
```

Check running containers
```
docker ps
```

Example
```
CONTAINER ID
ecf234abc
```

View logs
```
docker logs ecf234abc
```

Follow logs
```
docker logs -f ecf234abc
```

---

# Kubernetes Application Logs
Create Pod
```
apiVersion: v1
kind: Pod
metadata:
  name: event-simulator-pod

spec:
  containers:
  - name: event-simulator
    image: kodekloud/event-simulator
```

Apply
```
kubectl apply -f event-simulator.yaml
```

---

View logs
```
kubectl logs event-simulator-pod
```

Follow continuously
```
kubectl logs -f event-simulator-pod
```

Show timestamps
```
kubectl logs --timestamps event-simulator-pod
```

View previous logs after a container restart (CrashLoopBackOff scenarios)
```
kubectl logs --previous event-simulator-pod
```

---

# Multiple Containers in One Pod
Example
```
apiVersion: v1
kind: Pod
metadata:
  name: event-simulator-pod

spec:
  containers:
  - name: event-simulator
    image: kodekloud/event-simulator

  - name: image-processor
    image: some-image-processor
```

Since there are multiple containers, Kubernetes requires the container name.

Container 1
```
kubectl logs event-simulator-pod -c event-simulator
```

Container 2
```
kubectl logs event-simulator-pod -c image-processor
```

Follow logs
```
kubectl logs -f event-simulator-pod -c event-simulator
```

---

# Logs from Deployments
Get Pods
```
kubectl get pods
```

Example
```
nginx-648d4f6c5d-x4jrs
```

Logs
```
kubectl logs nginx-648d4f6c5d-x4jrs
```

Or directly using the Deployment resource:
```
kubectl logs deployment/nginx
```

---

# Common CKA/CKS Troubleshooting Workflow
When an application is not working:
```
kubectl get pods
```

If the Pod is not Running:
```
kubectl describe pod <pod-name>
```

Check events for scheduling, image pull, or probe failures.

If the Pod is Running but the application still fails:
```
kubectl logs <pod-name>
```

If the container restarted:
```
kubectl logs --previous <pod-name>
```

Check resource usage:
```
kubectl top pod
kubectl top node
```

If the issue appears to be with Kubernetes itself:
```
journalctl -u kubelet
```

or inspect the control plane component logs if they run as Pods.

This sequence—`get`, `describe`, `logs`, `top`, and component logs—is one of the most common troubleshooting patterns in both the CKA and CKS exams.