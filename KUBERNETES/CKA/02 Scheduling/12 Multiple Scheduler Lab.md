12 Multiple Scheduler Lab

1. What is the name of the POD that deploys the default kubernetes scheduler in this environment?
* Kube-scheduler
* etcd-master
* scheduler
* **kube-scheduler-controlplane**

2. What is the image used to deploy the kubernetes scheduler?
Inspect the kubernetes scheduler pod and identify the image

* kube-scheduler:1.23 
* **`registry.k8s.io/kube-scheduler:v1.35.0`** 
* `registry.k8s.io/kube-scheduler:v1.33.0` 
* scheduler:1.20

3. We have already created the `ServiceAccount` and `ClusterRoleBinding` that our custom scheduler will make use of.  
Checkout the following Kubernetes objects:  
  `ServiceAccount`: my-scheduler (kube-system namespace)  
`ClusterRoleBinding`: my-scheduler-as-kube-scheduler  
`ClusterRoleBinding`: my-scheduler-as-volume-scheduler  
Run the command: `kubectl get serviceaccount -n kube-system` and `kubectl get clusterrolebinding`  
**Note: -** Don't worry if you are not familiar with these resources. We will cover it later on.


4. Please create a ConfigMap that the new scheduler will utilize, implementing the concept of `ConfigMap as a volume`.  A ConfigMap definition file named `my-scheduler-configmap.yaml` has been provided at the `/root/` path. This file will be used to create a ConfigMap with the name `my-scheduler-config`, utilizing the content from the file located at `/root/my-scheduler-config.yaml`.
```
kubectl create configmap --name my-scheduler-config --from-file=/root/my-scheduler-config.yaml -n kube-system

# OR 

kubectl create -f my-scheduler-configmap.yaml

kubectl get configmaps
```

5. Deploy an additional scheduler to the cluster following the given specification.
Utilize the manifest file located at `/root/my-scheduler.yaml`. Ensure that you are using the same image as that of the default Kubernetes scheduler.
To verify the image used by the default Kubernetes scheduler, execute the following command:
```
kubectl describe pod kube-scheduler-controlplane --namespace=kube-system
```
**Note :** Deploying the new scheduler may take a few seconds to reach a running state.
`image:registry.k8s.io/kube-scheduler:v1.35.0`
Please modify the provided Pod manifest file located at `/root/nginx-pod.yaml` to specify that the Pod should be scheduled by your custom scheduler, which is named `my-scheduler`. After updating, create the Pod in the **default** namespace and verify it is scheduled by your custom scheduler.
**Note :** The pod may take a few seconds to reach a running state.



6. Please modify the provided Pod manifest file located at `/root/nginx-pod.yaml` to specify that the Pod should be scheduled by your custom scheduler, which is named `my-scheduler`.After updating, create the Pod in the **default** namespace and verify it is scheduled by your custom scheduler.**Note :** The pod may take a few seconds to reach a running state.

