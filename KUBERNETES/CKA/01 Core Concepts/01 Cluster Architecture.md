# Cluster Architecture
[[KUBERNETES/KCNA/1 Kubernetes Fundamental/Kubernetes Architecture|Kubernetes Architecture]]

Analogy of Ships

Two Kinds of ships,  --> Set of nodes 
Cargo --> Worker Nodes (Host Applications as Controller)
Control Ships --> Master Nodes (Manage, Plan, Schedule and Monitor Nodes)


In control Ships,
etcd CLUSTER
Cranes --> Kube-scheduler
Controller Manager
[Node-Controllers]
[Replication-Controllers]
kube-apiserver

In Cargo Ships,
