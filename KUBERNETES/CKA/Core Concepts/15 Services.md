# Kubernetes Services

A Kubernetes cluster is made up of many Pods. Pods are **ephemeral**, meaning they can be created, destroyed, or recreated at any time. Their IP addresses are not permanent.

Imagine you have a web application running inside a Pod.

```
Pod
--------------------
Nginx Web Server
Port: 80
IP: 10.244.0.2
```

Today the Pod IP is:

```
10.244.0.2
```

Tomorrow, after the Pod restarts, it may become:

```
10.244.0.15
```

If another application connects directly to the Pod IP, it will eventually fail because the Pod IP changes.

This is exactly why Kubernetes Services exist.

---

# What is a Kubernetes Service?

A **Service** is a stable networking object that provides a permanent endpoint for one or more Pods.

Instead of talking directly to Pods,

Applications talk to Services.

The Service automatically finds the correct Pods behind it.

Think of it like this:

```
Client
   |
   |
Service
   |
----------------------
|         |          |
Pod1      Pod2      Pod3
```

The client never knows which Pod handled the request.

The Service hides all that complexity.

---

# Why Do We Need Services?

Without Services:

```
Frontend ---> Pod IP

Frontend ---> 10.244.0.12
```

If Pod dies

```
Frontend ---> 10.244.0.12 (Dead)

Connection Failed
```

With Service

```
Frontend

     |
     |

Frontend-Service

     |

-------------------------
|           |           |
Pod1        Pod2        Pod3
```

Pods may come and go.

Service IP never changes.

---

# Real World Example

Suppose you are building an online banking application.

Components

```
Internet User

      |

Frontend

      |

Backend

      |

Database
```

Each component runs inside Kubernetes.

```
Frontend Pod
Backend Pod
Database Pod
```

Question:

How does Frontend know Backend's IP?

It doesn't.

Instead,

Frontend communicates with

```
backend-service
```

Backend Pods may change.

Service remains the same.

---

# Kubernetes Service Types

There are mainly four service types.

```
ClusterIP

NodePort

LoadBalancer

ExternalName
```

Most beginners learn these three:

```
ClusterIP

NodePort

LoadBalancer
```

---

# 1. ClusterIP

This is the default service type.

Purpose:
Allow communication inside the cluster.

Example:
```
Frontend Pod

        |

backend-service

        |

Backend Pods
```

The service gets an internal IP.

Example

```
Backend Service

IP:
10.96.12.45
```

Frontend accesses

```
http://10.96.12.45
```

or better
```
http://backend-service
```

because Kubernetes DNS resolves it.

External users cannot access it.

---

# Example
Backend Deployment
```
apiVersion: apps/v1
kind: Deployment

metadata:
  name: backend

spec:
  replicas: 3

  selector:
    matchLabels:
      app: backend

  template:
    metadata:
      labels:
        app: backend

    spec:
      containers:
      - name: backend
        image: nginx
```

Service

```
apiVersion: v1
kind: Service

metadata:
  name: backend-service

spec:
  selector:
    app: backend
  ports:
  - port: 80
    targetPort: 80
```

Notice

No type is specified.

Default becomes
```
ClusterIP
```

---

# How ClusterIP Works

Suppose

```
Pod A
10.244.1.3

Pod B
10.244.2.8

Pod C
10.244.4.10
```

Service

```
backend-service

Cluster IP

10.96.1.20
```

Traffic

```
Frontend

      |

10.96.1.20

      |

------------------------
|          |          |
PodA       PodB       PodC
```

---

# 2. NodePort
ClusterIP only works inside Kubernetes.

Suppose your laptop wants to access the application.

It cannot.

Your laptop cannot directly reach
```
10.244.x.x
```

because Pod network is private.

NodePort solves this.

---

# How NodePort Works

Suppose

```
Node IP

192.168.1.2
```

Pod

```
10.244.0.8

Port 80
```

NodePort

```
30008
```

Traffic

```
Laptop

192.168.1.10

       |

192.168.1.2:30008

       |

Service

       |

Pod:80
```

Now

```
curl http://192.168.1.2:30008
```

returns

```
Welcome to nginx
```

---

# Three Important Ports

This is the most confusing topic.

Suppose your application listens on

```
Port 80
```

There are three ports.

```
NodePort

↓

Service Port

↓

Target Port
```

Example

```
User

↓

30008

↓

80

↓

80

↓

Pod
```

Let's understand individually.

---

# TargetPort
Where application is listening inside Pod.

```
Container
Nginx

Port 80
```

So
```
targetPort: 80
```

---

# Port
Port exposed by Service.
```
Service
Port 80
```

Other Pods connect using
```
backend-service:80
```

---

# NodePort
External port.
```
30008
```
Outside users connect here.

---

# Complete Flow
```
Internet
     |
Node IP
192.168.1.2
     |

30008
     |

Service
Port 80
     |
Pod
Port 80
```

---

# NodePort YAML

```
apiVersion: v1
kind: Service
metadata:
  name: myapp-service

spec:
  type: NodePort
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30008
```

---

# Pod YAML
```
apiVersion: v1
kind: Pod
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
```

Notice

Both have
```
app: myapp
```

This is how Service discovers Pods.

---

# What is Selector?
Service never connects to Pods by name.

It connects using labels.
Example
Pod
```
labels:
  app: payment
  version: v1
```

Service

```
selector:
  app: payment
```

Result
Service automatically connects.

---

# What if Labels Don't Match?
Pod
```
labels:
  app: frontend
```

Service
```
selector:
  app: backend
```

No Pods found.

Service exists.

But requests fail.

You can verify using:

```
kubectl get endpoints
```

Output

```
NAME               ENDPOINTS 
backend-service    <none>
```

---

# Create Service

```
kubectl apply -f service.yaml
```

Check

```
kubectl get svc
```

Output

```
NAME            TYPE        CLUSTER-IP      PORT(S)

myapp-service   NodePort    10.96.20.8      80:30008/TCP
```

Describe

```
kubectl describe svc myapp-service
```

You will see

```
Selector

Ports

Endpoints

NodePort
```

---

# Endpoints

Service does not actually store Pods.

It stores endpoints.

Example

```
Service

↓

Endpoints

↓

10.244.1.3

10.244.2.8

10.244.3.5
```

Whenever Pods change,

Endpoints update automatically.

---

# Load Balancing

Suppose

```
Replica = 3
```

Pods

```
Pod1

Pod2

Pod3
```

Traffic

```
Client

      |

Service

      |

---------------------

Pod1

Pod2

Pod3
```

Requests are distributed across all healthy Pods.

You don't configure load balancing yourself.

Kubernetes does it automatically (typically using kube-proxy's networking rules, providing simple connection distribution across available endpoints).

---

# Production Example

Deployment

```
5 Backend Pods
```

```
backend-1

backend-2

backend-3

backend-4

backend-5
```

NodePort Service

```
backend-service
```

Traffic

```
1000 Users

        |

backend-service

        |

5 Pods
```

If

```
backend-2
```

dies,

Traffic automatically shifts to remaining Pods.

No configuration needed.

---

# What Happens if Pods Are on Different Nodes?

Suppose

```
Node1

PodA
```

```
Node2

PodB
```

```
Node3

PodC
```

NodePort exists on every node.

```
Node1:30008

Node2:30008

Node3:30008
```

Any request reaching any node is forwarded to one of the healthy Pods, regardless of which node that Pod is running on.

```
User

     |

Node2:30008

     |

PodA
```

or

```
PodB
```

or

```
PodC
```

---

# NodePort Limitations

NodePort is useful for:

- Learning Kubernetes
- Development environments
- Home labs
- Testing

It is generally **not** the preferred way to expose production internet-facing applications because:

- Ports are limited to the NodePort range (30000–32767 by default).
- Users must know the node IP and port.
- It does not provide cloud-native features like managed public IPs or advanced load balancing.

---

# LoadBalancer Service

In cloud providers

- AWS
- Azure
- GCP

You usually use

```
LoadBalancer
```

instead of NodePort.

Traffic

```
Internet

      |

Cloud Load Balancer

      |

Service

      |

Pods
```

The cloud provider automatically provisions an external load balancer and public IP that forwards traffic to your Service.

---

# Service Discovery Using DNS

Suppose

```
backend-service
```

exists.

Frontend connects simply using

```
http://backend-service
```

Kubernetes DNS resolves it automatically.

No IP addresses needed.

This is one of the biggest advantages of Services.

---

# Useful Commands

Create

```
kubectl apply -f service.yaml
```

List services

```
kubectl get svc
```

Detailed information

```
kubectl describe svc myapp-service
```

View endpoints

```
kubectl get endpoints
```

Delete

```
kubectl delete svc myapp-service
```

---

# Interview Questions

### 1. Why do we need a Kubernetes Service?

Because Pods are ephemeral and their IP addresses can change. A Service provides a stable endpoint and load balances traffic across matching Pods.

---

### 2. What is the difference between `port`, `targetPort`, and `nodePort`?

- **targetPort**: Port where the application listens inside the Pod.
- **port**: Port exposed by the Service inside the cluster.
- **nodePort**: External port opened on every node for outside access.

---

### 3. How does a Service find Pods?

Using **label selectors**. The Service routes traffic to Pods whose labels match its selector.

---

### 4. Can one Service route traffic to multiple Pods?

Yes. As long as the Pods have matching labels, the Service automatically includes them as endpoints and distributes traffic among them.

---

### 5. Does a Service connect to Pods by Pod name?

No. Services use label selectors and endpoint lists, not Pod names.

---

# Key Takeaways

- A Service provides a stable network endpoint for Pods.
- Pods communicate through Services instead of directly using Pod IPs.
- `ClusterIP` is for internal communication and is the default Service type.
- `NodePort` exposes an application externally by opening a port on every Kubernetes node.
- `LoadBalancer` integrates with cloud providers to create an external load balancer.
- Services discover Pods using label selectors.
- Kubernetes automatically updates Service endpoints as Pods are created, deleted, or rescheduled.
- Services distribute traffic across all healthy Pods, enabling scalability and high availability.