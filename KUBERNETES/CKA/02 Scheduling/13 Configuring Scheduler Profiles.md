# Configuring Scheduler Profiles
We are going to cover:
1. Why Scheduler Profiles were introduced
2. Complete Scheduler Architecture
3. Scheduler Framework
4. Scheduling Cycle
5. Binding Cycle
6. Scheduler Extension Points
7. Scheduler Plugins
8. Default Plugins Explained
9. Scheduler Profiles
10. Plugin Configuration
11. Multiple Profiles
12. Real-world examples
13. CKA/CKS Exam Perspective

---

# Part 1 — First Understand the Problem
Imagine Kubernetes has 100 nodes.
```
Node-1
Node-2
Node-3
...
Node-100
```

Now a Pod is created.

```
kubectl apply -f pod.yaml
```

The API Server stores it inside etcd.

Notice something.

The Pod has
```
spec:
```

but
```
spec.nodeName
```

is empty.

Example
```
apiVersion: v1
kind: Pod

metadata:
  name: nginx

spec:
  containers:
  - image: nginx
```

After creation
```
API Server
Pod
Name: nginx
Node: <none>
Status: Pending
```

Nobody knows where this pod should run.

Someone has to decide.

That someone is
```
kube-scheduler
```

# Part 2 — Scheduler Workflow
The scheduler continuously watches the API Server.

```
Watch()
Pending Pods
```

Whenever it sees
```
nodeName == empty
```

it starts scheduling.

```
API Server

Pending Pod
      |
      |
      V

Scheduler
```

Scheduler then performs
```
Scheduling Cycle
```

followed by
```
Binding Cycle
```

# Part 3 — Scheduling Cycle
Scheduling Cycle answers only ONE question.

```
Which node is best?
```

Not
```
How to start container?
```

Not
```
How to pull image?
```

Only
```
Which node?
```

The scheduling cycle is roughly
```
Pending Queue
      |

Queue Sort
      |

PreFilter
      |

Filter
      |

PostFilter
      |

PreScore
      |

Score
      |

Reserve
      |

Permit
      |

Choose Best Node
```

Then comes
```
Bind
```

which is another cycle.

# Part 4 — Why So Many Phases?
Because Kubernetes wants scheduling to be modular.

Instead of writing one huge function
```
schedulePod()
```

they divided scheduling into plugins.

Each plugin performs one small task.

Like LEGO blocks.

```
+----------------+
| QueueSort      |
+----------------+

+----------------+
| Filter         |
+----------------+

+----------------+
| Score          |
+----------------+

+----------------+
| Bind           |
+----------------+
```

This architecture is called
```
Scheduler Framework
```
# Part 5 — Scheduler Framework
Internally
```
Scheduler
        |

 Scheduler Framework
        |

+----------------------+
| QueueSort Plugin     |
+----------------------+

+----------------------+
| Filter Plugin        |
+----------------------+

+----------------------+
| Score Plugin         |
+----------------------+

+----------------------+
| Bind Plugin          |
+----------------------+
```

Instead of modifying Kubernetes source code,

you simply
```
Enable Plugin
Disable Plugin
Replace Plugin
```

This is exactly why Scheduler Profiles exist.

# Part 6 — Queue Phase
Suppose these pods arrive
```
Pod A
Priority = 10

Pod B
Priority = 5000

Pod C
Priority = 100
```

Queue initially
```
A

B

C
```

PrioritySort plugin rearranges them
```
B

C

A
```

Higher priority first.

Plugin responsible

```
PrioritySort
```

---

Example
```
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass

metadata:
  name: high-priority

value: 1000000
globalDefault: false
```

Pod
```
spec:
  priorityClassName: high-priority
```

Immediately jumps ahead in queue.

# Part 7 — Filter Phase
Now suppose
```
Pod requires

CPU = 10
RAM = 8GB
```

Cluster
```
Node1
CPU Free = 4
RAM = 20GB
```
Rejected.

Node2
```
CPU Free = 16
RAM = 32GB
```
Accepted.

Node3
```
CPU Free = 12

RAM = 4GB
```

Rejected.

After filtering
Only
```
Node2
```
remains.

Plugins involved
```
NodeResourcesFit
NodeName
NodeAffinity
TaintToleration
VolumeRestrictions
etc.
```

# Part 8 — NodeResourcesFit Plugin
Probably the most important plugin.
Suppose
```
Pod
requests
CPU = 2
Memory = 4Gi
```

Node
```
Free CPU = 1
Free Memory = 16Gi
```

Filter says
```
No
CPU insufficient
```
Node removed.

Another node
```
CPU = 16
Memory = 64Gi
```
Accepted.

# Part 9 — NodeName Plugin
Suppose Pod says
```
spec:
  nodeName: worker-2
```

Scheduler immediately checks
```
worker-2
```

If worker-2 exists
Schedule there.

Otherwise
Pod remains Pending.

Normally
```
nodeName
```

bypasses scheduler decisions because you explicitly chose the node.

# Part 10 — NodeUnschedulable Plugin
Suppose
```
kubectl cordon worker1
```
or
```
kubectl drain worker1
```

Node becomes
```
Unschedulable
```

Output
```
Unschedulable: true
```

Plugin
```
NodeUnschedulable
```

filters it immediately.

Even if
```
100 CPUs free
```

scheduler ignores it.

# Part 11 — Score Phase
Suppose after filtering
```
Node1

Node2

Node3
```
all satisfy requirements.

Now scheduler asks
```
Which one is BEST?
```

This is scoring.

Example
Node1
```
CPU Left After Scheduling
2
```
Score
```
20
```


Node2
```
CPU Left
8
```
Score
```
90
```

Node3
```
CPU Left
5
```
Score
```
60
```

Scheduler chooses
```
Node2
```

Highest score wins.

# Part 12 — ImageLocality Plugin
Suppose
Node1 already has
```
nginx:1.28
```

downloaded.

Node2
does not.

Scheduling
```
Image: nginx:1.28
```

ImageLocality plugin gives Node1 a better score because it avoids downloading the image again, reducing startup latency.

# Part 13 — Reserve Phase
Scheduler temporarily reserves
```
Node2
```
for this pod.

Why?
Imagine two schedulers.

Without reservation
```
Pod A
chooses Node2
```

At exactly same time
```
Pod B
also chooses Node2
```

Reservation prevents this race.

# Part 14 — Permit Phase
A custom plugin may decide
```
Wait
before scheduling.
```

Example
```
Only schedule after external approval.
```

Permit plugin can
```
Allow
Reject
Wait
```

# Part 15 — Bind Phase
Only now does scheduler write
```
nodeName = worker2
```
into Pod object.

```
Before
nodeName: ""
```

After
```
nodeName: worker2
```

API Server updates Pod.

Now
```
Kubelet on worker2
```

sees
```
This pod belongs to me.
```

Then container creation begins.

Notice:
Scheduler **does not** start containers. It only assigns a node. The kubelet on the chosen node is responsible for pulling images, creating containers, mounting volumes, and reporting status.

# Part 16 — Why Scheduler Profiles?
Before Kubernetes 1.18
people started multiple scheduler binaries.

Example
```
default-scheduler

my-scheduler

gpu-scheduler

ml-scheduler
```

Each was a different process.

Problems
```
Higher memory
Higher maintenance
Race conditions
Separate configuration
```

Kubernetes solved this.

One scheduler process.

Many personalities.

These are
```
Scheduler Profiles
```

# Part 17 — Scheduler Profiles
One scheduler
```
kube-scheduler
```
can expose multiple logical schedulers.

Configuration
```
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration

profiles:
- schedulerName: default-scheduler

- schedulerName: gpu-scheduler

- schedulerName: batch-scheduler
```

One binary.

Three behaviours.

# Part 18 — How Pod Chooses Profile
Pod YAML
```
spec:
  schedulerName: gpu-scheduler
```

Scheduler checks
```
Which profile?
gpu-scheduler
```

Then uses
```
GPU profile plugins
```

instead of
```
Default profile plugins.
```

Another pod
```
spec:
  schedulerName: batch-scheduler
```

uses another profile.

Same scheduler process.

Different behaviour.

# Part 19 — Customising Plugins
Example
```
profiles:
- schedulerName: gpu-scheduler
  plugins:
    score:
      disabled:
      - name: TaintToleration
      enabled:
      - name: MyCustomPlugin
```

Meaning
During scoring

Do NOT use
```
TaintToleration
```

Instead
also execute
```
MyCustomPlugin
```

# Part 20 — Disable Every Plugin
Possible
```
score:

  disabled:

  - name: "*"
```

Meaning
```
Disable every scoring plugin.
```

Similarly,
```
preScore:
  disabled:
  - name: "*"
```

No PreScore plugins will run.

# Part 21 — Multiple Profiles Example
```
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration

profiles:
- schedulerName: default-scheduler
- schedulerName: high-performance
  plugins:
    score:
      disabled:
      - name: ImageLocality
- schedulerName: testing
  plugins:
    score:
      disabled:
      - name: "*"
```

Pods
```
spec:
  schedulerName: default-scheduler
```

Uses default plugins.

```
spec:
  schedulerName: high-performance
```

Uses all plugins except ImageLocality during scoring.

```
spec:
  schedulerName: testing
```

Uses no scoring plugins.

# Internal Mental Model
Always think of scheduling as a configurable pipeline:
```
Pending Pod
    |
    v
+----------------------+
| QueueSort            |
+----------------------+
    |
    v
+----------------------+
| PreFilter            |
+----------------------+
    |
    v
+----------------------+
| Filter              | --> Remove invalid nodes
+----------------------+
    |
    v
+----------------------+
| PostFilter          |
+----------------------+
    |
    v
+----------------------+
| PreScore            |
+----------------------+
    |
    v
+----------------------+
| Score               | --> Rank remaining nodes
+----------------------+
    |
    v
+----------------------+
| Reserve             |
+----------------------+
    |
    v
+----------------------+
| Permit              |
+----------------------+
    |
    v
+----------------------+
| Bind                | --> Write spec.nodeName
+----------------------+
    |
    v
Kubelet starts the Pod
```

# CKA Exam Tips
For the CKA exam, you should be able to:
- Explain the difference between filtering and scoring.
- Understand that the scheduler only assigns a node; the kubelet runs the workload.
- Use `schedulerName` in a Pod to target a specific scheduler profile or custom scheduler.
- Recognise the effects of `PriorityClass`, `cordon`, `drain`, taints, affinities, and resource requests on scheduling.
- Read and understand `KubeSchedulerConfiguration` files, especially the `profiles` and `plugins` sections.

# CKS Perspective
The CKS exam generally does not require you to implement custom scheduler plugins, but it expects you to understand how scheduling policies affect workload placement and security. For example:

- Taints and tolerations can isolate sensitive workloads.
- Node affinity can restrict workloads to trusted nodes.
- Priority classes influence which workloads are scheduled first during resource pressure.
- Scheduler profiles allow different scheduling policies without running multiple scheduler processes.

Understanding the scheduler framework also helps explain why security-sensitive workloads can be steered toward hardened nodes while less-trusted workloads are kept elsewhere.