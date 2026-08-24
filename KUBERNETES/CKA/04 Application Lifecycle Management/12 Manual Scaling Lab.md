# Manual Scaling Lab

### Manual Scaling of a Kubernetes Deployment
Objectives
- Understand the concept of scaling in Kubernetes
- Manually scale a deployment up and down
- Observe the effects of scaling on the application and resources


**Create a Deployment**
- Using the `/root/deployment.yml` manifest file provided , create a Kubernetes deployment for the Flask application.
**Discovery**
- Use `kubectl get deployments` to observe the deployment status.
- Use `kubectl get pods` to see the running pods.

`kubectl create -f deployments.yml`

What is the primary purpose of the `kubectl scale` command?
To create a new namespace
**To adjust the number of replicas in a deployment or replicaset**
to delete a kubernetes object
To update the image of a running container


Can the `kubectl scale` command be used to scale down a statefulset in Kubernetes?
No. statefulsets cannot be scaled down.
**Yes, it can scale both deployments and statefulsets.**
Yes, but only if the -scale-down flag is used.
No, it only works with deployments and replicasets.


**Manual Scale**
Manually scale the deployment named **flask-web-app** to have **3** replicas.
**Observation**
Observe the changes with kubectl get deployments and kubectl get pods.  
To view the application, click on the **Ingress** button at the top of the terminal, or click on **Skooner** to access the monitoring tool and view the resources in the Kubernetes cluster.
**Token** for the **Skooner** can be found in `/root/skooner-sa-token.txt`
```bash
controlplane ~ ➜  kubectl get deploy
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
flask-web-app   2/2     2            2           4m43s

controlplane ~ ➜  kubectl scale deployment flask-web-app --replicas=3
deployment.apps/flask-web-app scaled

controlplane ~ ➜  kubectl get deploy
NAME            READY   UP-TO-DATE   AVAILABLE   AGE
flask-web-app   3/3     3            3           5m54s

```

If you scale a deployment using `kubectl scale` to a higher number of replicas, but the cluster has insufficient resources to accommodate all new replicas, what will happen?
* **Some replicas will be created up to the limit of available resources, and the deployment will remain in a pending state for the remaining replicas.**
* Kubernetes will scale the deployment down automatically to fit the available resources
* The command will succeed, but Kubernetes will automatically remove resources from other workloads.
* The command will fail, and no replicas will be created.


