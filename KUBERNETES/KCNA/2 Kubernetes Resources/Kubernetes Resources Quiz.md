# Kubernetes Resources Quiz

What are the two strategies for making deployments in Kubernetes?
• Scale and replace strategies
• Replicate and update strategies
**• Recreate and rolling update strategies**
• Update and upgrade strategies


Why is the use of a replication controller important in Kubernetes?
**• All of the options are correct |**
• It manages the replication of pods for load balancing purposes.
• It ensures that multiple instances of a pod are running to provide high availability.
• It helps to automatically recover and replace failed pods.

What is the default deployment strategy in Kubernetes where the application never goes down during the update?
• Replace strategy
**• Rolling update strategy**
• Scale strategy
• Recreate strategy

Which of the following fields are required in a Kubernetes definition file?
• image, ports, volumes, annotations
**• apiVersion, kind, metadata, spec**
• version, type, description, configuration
• name, containers, labels, replicas

Which command is used to view the list of pods in a Kubernetes cluster?
• kubecti show pods
**• kubecti get pods**
• kubectl list pods
• kubectl view pods

How can you view pods in all namespaces in Kubernetes?
**• Use the kubectl get pods -all-namespaces command.**
• Use the kubectl get pods -global command.
• Use the kubectl get pods -all command.
• Use the kubectl get pods -namespace=all command.

To view all the objects created after a deployment, which command can you use?
**• kubectl get all**
• kubectl get replicasets
• kubectl get pods
• kubecti get deployments

What is the recommended approach for expanding the physical capacity of a Kubernetes cluster when the current node lacks sufficient capacity?
• Add more resources to the existing node to increase its capacity.
**• Deploy additional pods on a new node in the cluster to expand the cluster's physical capacity.**
• Adjust the resource limits of the existing pods to optimize their performance.
• Spin up additional pods on the same node to handle the increased load

Which approach is used to specify what actions should be performed in Kubernetes without specifying how they should be executed?
• Reactive approach
• Proactive approach
• Imperative approach
**• Declarative approach**


Which approach is used to specify specific actions and how should they be performed in Kubernetes?
**• Imperative approach**
• Declarative approach
• Proactive approach
• Reactive approach


How can you view the history and revisions of a deployment rollout in Kubernetes?
• Use the command kubectl get revisions [deployment-name].
**• Use the command kubectl rollout history [deployment-name].**
• Use the command kubectl describe rollout [deployment-name].
• Use the command kubectl get history [deployment-name].

In Kubernetes, which namespace is automatically created by Kubernetes when the cluster is first set up?
• Custom Namespace
**• default Namespace**
• Primary Namespace
**• kube-system Namespace**


What parameter is used with the "kubect run" command to specify the
application image when deploying a Docker container as a pod?
• -container
• -pod-image
**• -image**
• -app-image


By default, when a Docker container is deployed within a pod, how can users
access the application?
• Internally, from the node where the pod is running
**• Only through direct SSH access to the container**
• Externally, using the pod's IP address
• Externally, from any node in the cluster


Which namespace in Kubernetes is created at cluster startup and contains
internal services required for networking and DNS?
**• kube-system Namespace**
• Custom Namespace.
• kube-public Namespace
• default Namespace


Is the "selector" field a required field in a ReplicationController?
• Yes, the selector field is a required field in a ReplicationController.
**• No, the selector field is not a required field in a ReplicationController.**
• The selector field is only required if the ReplicationController manages existing pods.
• The requirement for the selector field depends on the Kubernetes version.

Why are deployment rollouts and revisions important in Kubernetes?
• They ensure high availability of the application.
• They provide security for the application.
**• They allow for tracking changes made to the deployment.**
• They help in scaling up the pods.


When a new deployment is created, what is the result of the rollout process?
• Scaling up of the pods
• Deletion of the previous deployment revision
**• Creation of a new deployment revision**
**• Creation of a new replica set**


When using the kubectl apply command to create an object in Kubernetes, what
happens to the YAML version of the local object config file?
• It is discarded and not used for further operations.
• It is stored as the live configuration on the Kubernetes cluster.
**• It is converted to a JSON format and stored as the last applied configuration.**
• It is used as the primary reference for object creation.


How can you rollback a Kubernetes deployment to a previous revision?
• kubecti rollout update deployment/my-deployment
• kubecti undo deployment my-deployment.
• kubectl rollback deployment my-deployment
**• kubectl rollout undo deployment/my-deployment**

In which Kubernetes namespace are the resources created that should be made
available to all users?
• Tuber System Namespace
• Custom Namespace
• default Namespace
**• kube-public**


What is the smallest object that can be created in Kubernetes?
• Node
• Service
**• Pod**
• Container


What is the advantage of having multiple containers within the same pod in Kubernetes?
• It provides a backup container in case the main application container fails.
• It ensures that all containers within the pod have the same resource limits.
**• It enables the containers to share the same network namespace and storage volumes.**
• It allows for scaling the application more efficiently.


What is the recommended approach for expanding the physical capacity of a Kubernetes cluster when the current node lacks sufficient capacity?
• Add more resources to the existing node to increase its capacity.
• Spin up additional pods on the same node to handle the increased load.
• Adjust the resource limits of the existing pods to optimize their performance.
**• Deploy additional pods on a new node in the cluster to expand the cluster's physical capacity.**


Which command is used to view the list of pods in a Kubernetes cluster?
• kubectl view pods
• kubectl get pods
• kubectl list pods
• kubectl show pods


Which of the following fields are required in a Kubernetes definition file?
• image, ports, volumes, annotations
• version, type, description, configuration
• name, containers, labels, replicas
**• apiVersion, kind, metadata, spec**


What is the purpose of assigning quotas to Kubernetes namespaces?
• To control the network bandwidth available to pods within a namespace
• To limit the number of pods that can be created within a namespace
• To define access controls and permissions for different user groups within a namespace
**• To restrict the amount of CPU and memory resources that can be utilized by objects within a namespace**


In a Kubernetes definition file, why is the "containers" property within the "spec" section defined as a list or an array?
• It allows for specifying multiple versions of the container image.
• It enables easy scaling of the containers within the pod.
• It ensures the containers have unique names within the pod.
**• It supports the deployment of multiple containers within the pod**


Why would you create separate namespaces for dev and production environments in Kubernetes?
• To simplify the management of Kubernetes objects
**• To isolate resources and prevent accidental modifications in one environment affecting the other**
• To improve resource utilization within the cluster
• To facilitate communication and collaboration between dev and production teams

