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




































