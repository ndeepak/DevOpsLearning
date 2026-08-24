# HPA Lab

### HPA Introduction Sample Lab

**Objectives**
- **HPA** with **Imperative commands**
- **Requirements** for **HPA to work**
- What happens when **resources.limit** is **not mentioned**

**Create a Deployment**
- Using the `/root/deployment.yml` manifest file provided , create a Kubernetes deployment for the nginx application.
Click on **Skooner** to access the monitoring tool and view the resources in the Kubernetes cluster.
**Token** for the **Skooner** can be found in `/root/skooner-sa-token.txt`

We have a manifest file to create **autoscaling** for the **Nginx deployment** located at `/root/autoscale.yml`. Review the manifest file and identify the **current replicas** and **desired replicas**?
**A**. Current replicas= 7  
    Desired replicas= 3
**B**. Current replicas= 3  
    Desired replicas= 7
**C**. Current replicas= 7  
    Desired replicas= 1
**D**. **Current replicas= 0**  
    **Desired replicas= 0**


Create an **autoscaler** for the **nginx-deployment** with a maximum of `3` replicas and a CPU utilization target of `80%`.
```
kubectl create -f autoscale.yml 
horizontalpodautoscaler.autoscaling/nginx-deployment created
```

What is the **primary purpose** of the **Horizontal Pod Autoscaler (HPA)** in Kubernetes?
to automate the creation of services
to automate the deployment of new applications
o automate the scaling of cluster nodes
**To automate the scaling of pods based on observed CPU utilization or other select metrics**



What **component** in a Kubernetes cluster is responsible for providing **metrics** to the **HPA**?
`metrics server`

What is the **current replica count** of **nginx-deployment** after deploying the **autoscaler**?
`3`

What is the **status** of **HPA** target?
`**<unknown>/80%**`
47%/80%
80%/80%
0%/80%
`kubectl get hpa`


The **HPA status** shows **/80** for the **CPU target**. what could be a possible reason?
**The deployment does not have any resource fields defined**
The metrics server is not available or not functioning properly.
The nodes are out of capacity
The Kubernetes cluster is not using namespaces



Since the **HPA** was failing due to the **resource field** missing in the **nginx-deployment**, the **resource field** has been updated in `/root/deployment.yml`. Update the **nginx-deployment** using this manifest. **Watch** the changes made to the **nginx-deployment** by the **HPA** after upgrading by using the `kubectl get hpa --watch` command.

What does the event `ScalingReplicaSet` in the **nginx-deployment** HPA indicate?
**The HPA is scaling the number of pods up or down.**
The HPA is setting memory limits for pods.
The HPA is restarting all pods.

What is the cause of the `FailedGetResourceMetric` event in the **nginx-deployment** HPA?
**CPU or memory requests are missing for a container.**
the node has reached its process limit
The HPA is unable to scale.
Memory on the node is insufficient