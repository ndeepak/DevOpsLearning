# Scheduling Quiz

Which of the following is a suitable use case for deploying a DaemonSet in Kubernetes?
**• Deploying a monitoring agent or log collector on each node in the cluster**
• Deploying a database service on a specific subset of nodes in the cluster
• Deploying a job that runs periodically on a single node in the cluster
• Deploying a stateless web application on each node in the cluster


What does the taint effect determine for pods that do not tolerate the taint in
Kubernetes?
**• The scheduling behavior of the pods**
• The networking behavior of the pods
• The logging behavior of the pods
• The resource allocation behavior of the pods


What are the two types of node affinity available in Kubernetes?
• Primary affinity and secondary affinity
• Absolute affinity and conditional affinity
**• requiredDuringSchedulingIgnoredDuringExecution, preferredDuringSchedulingIgnoredDuringExecution**
• High affinity and low affinity


What is the key distinction between a DaemonSet and a ReplicaSet?
• A DaemonSet manages long-running services, while a ReplicaSet manages short-lived batch jobs.
A DaemonSet scales pods horizontally based on CPU utilization, while a ReplicaSet scales pods verticall
based on memory consumption.
* **A DaemonSet ensures that a copy of a pod runs on every node in a Kubernetes cluster, While a ReplicaSet**
maintains a specified number of pod replicas across the cluster.
• A DaemonSet is used for stateless applications, while a ReplicaSet is used for stateful applications.


Where are the labels defined for the pods in a ReplicaSet?
• Labels are not used for pods in a Replicaset.
• Under the template section of the Replicaset definition file.
• In both the template section and at the top of the Replicaset definition file.
• At the top of the Replicaset definition file.

What does the type of node affinity in Kubernetes define?
**• The behavior of the scheduler in relation to node affinity and the stages of the pod lifecycle.**
• The priority of pods in relation to node placement.
• The labels assigned to the nodes in the cluster.
• The types of workloads that can be deployed on a specific node.

The Kubernetes API server is aware of the static pods created by the kubelet.
TRUE

What limitation exists when using NodeSelectors in Kubernetes?
• NodeSelectors cannot be used to restrict pod placement.
• NodeSelectors can only be used to select a single node at a time.
**• NodeSelectors can only handle simple queries and cannot handle complex queries like OR or NOT.**
• NodeSelectors cannot be used to select nodes based on labels.


What is the term used for the pods that are created by the kubelet independently, without any involvement from the API server or other Kubernetes cluster components?
* Autonomous Pods
* Managed Pods
* Static Pods
* Dynamic Pods

What does the taint effect "NoSchedule" indicate in Kubernetes?
• Pods will be scheduled with a lower priority on the node.
• Pods will be scheduled with a higher priority on the node.
• Pods will be evicted immediately from the node.
**• Pods will not be scheduled on the node.**


How can you ensure complete dedication of nodes for specific pods in Kubernetes?
* **By using a combination of taints, tolerations, and node affinity rules** 
* By using only taints and tolerations 
* By using only node affinity rules 
* By using pod anti-affinity rules


Which statement accurately describes the behavior of a static pod in a Kubernetes cluster?
• Static pods do not require a mirror object in the Kube API server as they are independent entities.
• Static pods are not visible in the Kube API server and cannot be managed.
• Static pods are fully manageable from the Kube API server, allowing editing and deletion like regular pods.
• When a kubelet creates a static pod, it also creates a read-only mirror object in the Kube API server.


How can you limit a pod to run on a specific node in Kubernetes? 
•Specify the node name in the pod's metadata section under the field "node". 
• Use the nodeGroup field in the pod's spec section. 
**• Add a label to the node and use nodeSelector in the pod's spec section.** 
• Use taints and tolerations on the pod and node to restrict pod placement.


What does the type of node affinity in Kubernetes define? 
• The priority of pods in relation to node placement. 
• The types of workloads that can be deployed on a specific node. 
• The labels assigned to the nodes in the cluster. 
**• The behavior of the scheduler in relation to node affinity and the stages of the pod lifecycle.**

What does the taint effect "PreferNoSchedule" indicate in Kubernetes?
• Pods will not be scheduled on the node.
**• System will try to avoid placing a pod on the node, but it is not guaranteed.**
• Pods will be evicted immediately from the node.
• Pods will be scheduled with a higher priority on the node.


What are the key distinctions between static pods and DaemonSets in
Kubernetes?
• Both static pods and DaemonSets are ignored by the kube-scheduler.
**• All of the above statements are true.**
• Static pods are created using kubelet, while DaemonSets utilize kubeapi-server.
• Static pods can be used to deploy control plane nodes, while DaemonSets are suitable for deploying
monitoring or logging agents on each node.


How can you select pods based on labels using the kubectl command?
• Use the kubectl pods command followed by the label name.
**• Use the kubectl get pods -selector command followed by the label key-value pair.**
• Use the kubectl get pods -filter command followed by the label name.
• Use the kubectl describe pods command followed by the label key-value pair.


Where are the labels defined for the pods in a ReplicaSet?
• Labels are not used for pods in a Replicaset.
**• Under the template section of the Replicaset definition file.**
• In both the template section and at the top of the Replicaset definition file.
• At the top of the Replicaset definition file.

What is a potential use case for static pods in a Kubernetes cluster?
• Scaling worker nodes dynamically based on resource utilization
**• Deploying control plane components as pods on the master nodes**
• Managing networking configurations for the cluster
• Running user applications that require high availability


What do the labels at the top of a Replicaset definition file represent?
• Labels of the service associated with the Replicaset.
• Labels used for networking purposes.
• Labels of the pods in the Replicaset.
**• Labels of the Replicaset itself.**


Which command should be used to obtain detailed information about a
specific DaemonSet in Kubernetes?
• kubectl describe pods < -namel >
• kubectl describe deployments ‹daemon-name\>
• kubecti describe services «daemon-namel>
**• kubectl describe daemonsets ‹ daemon-name\>**



What approach can be used to specify the path for static pod definition files
when not directly specifying it in the kubelet.service file?
• Defining the path in the kubeconfig file
• Modifying the container runtime directory
**• Creating a separate config file and defining the directory path as 'staticPodPath'**
• Using the -pod-manifest-path parameter in the kubelet. service file


What can be done to manually schedule a pod to a specific node in Kubernetes when there is no
scheduler monitoring and scheduling the nodes?
• Use the kubecti assign command to assign the pod to a specific node.
**• Set the NodeName field in the pod manifest to the desired node name.**
• Create a custom binding object to associate the pod with the desired node.
• Modify the pod's namespace to match the desired node's namespace.


The Kubernetes API server is aware of the static pods created by the kubelet.
True


How do you specify labels in a Kubernetes pod definition file?
• Use the "selectors" field under the "metadata section and provide labels in a key-value format.
**• Use the "labels" field under the "metadata" section and provide labels in a key-value format.**
• Use the "annotations" field under the "metadata" section and provide labels in a key-value format.
• Use the "tags" field under the "metadata section and provide labels in a key-value format.


Which of the following is a suitable use case for deploying a DaemonSet in Kubernetes?
• Deploying a database service on a specific subset of nodes in the cluster
• Deploying a job that runs periodically on a single node in the cluster
• Deploying a stateless web application on each node in the cluster
**• Deploying a monitoring agent or log collector on each node in the cluster**



What is the difference between "Gigabyte (GB)" and "Gibibyte (GiB)" in terms of their size?
• Gigabyte (GB) and Gibibyte (GIB) are interchangeable units with the same size.
**) Gigabyte (GB) refers to 1000 Megabytes, while Gibibyte (GIB) refers to 1024 Mebibytes.**
• Gigabyte (GB) refers to 1000 Megabytes, while Gibibyte (GiB) refers to 1000 Megabytes.
• Gigabyte (GB) refers to 1024 Megabytes, while Gibibyte (GiB) refers to 1000 Megabytes.


Where is the location specified for the kubelet to look for static pod definition files?
• The container runtime directory
• The kubelet configuration file
**• The -pod-manifest-path parameter in the kubelet service file**
• The kubeconfig file

Which statement accurately describes the behavior of a static pod in a Kubernetes cluster?
**• When a kubelet creates a static pod, it also creates a read-only mirror object in the Kube API server.**
• Static pods do not require a mirror object in the Kube API server as they are independent entities.
• Static pods are not visible in the Kube API server and cannot be managed.
• Static pods are fully manageable from the Kube API server, allowing editing and deletion like regular pods.

What is the minimum value that can be set for CPU resource requests in Kubernetes?
• 100m CPU
**• 1m CPU**
• 0.5 CPU
O 1 CPU

What is the purpose of using taints and tolerations in Kubernetes?
• To record additional details or metadata for informational purposes
• To group and select pods based on their characteristics
• To define labels for pods and nodes
**• To set restrictions on which pods can be scheduled on specific nodes**


Which of the following is a taint effect in Kubernetes?
• **NoSchedule**
• PreferredSchedule
• RestrictedSchedule
• LimitedSchedule


To connect a ReplicaSet to the desired pods, which field in the ReplicaSet specification is used to
match the labels defined on the pod?
• replicas
• **selector**
• metadata
• template


What are the two types of node affinity available in Kubernetes?
• Absolute affinity and conditional affinity
**• requiredDuring SchedulingIgnoredDuringExecution, preferredDuringSchedulingIgnoredDuring Execution**
• High affinity and low affinity
• Primary affinity and secondary affinity

What capability does the node affinity feature provide in Kubernetes?
• It allows selecting multiple nodes based on a single label using the OR operator.
• It allows selecting nodes based on their resource utilization.
• It enables complex queries like OR, IN, NOT, and EXISTS for limiting pod placement on specific nodes.
• It provides a way to restrict pod placement only on the master node.