# Lab - Modifying CPU resources in VPA
VPA CPU Optimization Lab
In this lab, you will deploy a sample application on Kubernetes, monitor its CPU resource usage, and utilize a Vertical Pod Autoscaler (VPA) to manage and adjust the resource allocation for the pods. The goal is to observe how the VPA automatically recommends and adjusts memory resource limits, particularly when the application experiences increased load.

### **Objectives:**

1. **Deploy a sample application** and verify that the pods are running correctly.
2. **Monitor pod resource usage** using the `kubectl top` command to assess CPU and memory consumption.
3. **Deploy a Vertical Pod Autoscaler (VPA)** to observe how it adjusts CPU and memory resource recommendations based on the application’s current usage.
4. **Introduce load** to the application and monitor how VPA dynamically updates its recommendations in response to increased demand.
5. **Interpret VPA recommendations** by understanding key parameters like `lowerBound`, `upperBound`, and `uncappedTarget` for resource management.

By the end of this lab, you will have a clear understanding of how VPA optimizes CPU resource usage in a Kubernetes environment, improving application performance and efficiency under varying workloads.

---
### VPA CPU Optimization Lab
A file named **`vpa-cpu-testing.yml`** has been prepared and is located in the **`/root`** directory. Proceed to **deploy** this file.
Have you deployed the specified file?
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app-4
  labels:
    app: flask-app-4
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-app-4
  template:
    metadata:
      labels:
        app: flask-app-4
    spec:
      containers:
      - name: flask-app-4
        image:  kodekloud/flask-session-app:1 
        ports:
        - name: http
          containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: flask-app-4-service
  labels:
    app: flask-app-4
spec:
  type: NodePort
  selector:
    app: flask-app-4
  ports:
  - name: http
    protocol: TCP
    port: 80
    targetPort: 8080
    nodePort: 30080
```



---
### Monitoring Pod Resource Usage
To check the current resource usage (CPU and memory) of all running pods in your Kubernetes cluster, use the `kubectl top pod` command. This command retrieves and displays resource metrics directly from the cluster's resource metrics API. It is particularly useful for tracking how efficiently your workloads are consuming cluster resources.

To view the resource consumption of the pods, run the following command:
```bash
kubectl top pod
```

The output will display a table with each pod's name, namespace, CPU usage (in millicores), and memory usage (in mebibytes), allowing you to monitor resource usage in real time.

For example, the output may look like this:
```
NAME                           CPU(cores)   MEMORY(bytes)   
flask-app-4-5cfb5d78c4-p9l2m   1m           19Mi            
flask-app-4-5cfb5d78c4-t229n   1m           19Mi            
```

This output provides an overview of how much CPU and memory each pod is currently consuming.
**Note: The metrics server may take some time to collect metrics from newly deployed pods.**

---
A file named `vpa-cpu.yml` has been created in the `/root` directory. Proceed to deploy this file.
Once deployed, check the cpu consumption by running the below command:
```
kubectl get vpa
```
Is the vpa-cpu.yml deployed?
```yaml
apiVersion: "autoscaling.k8s.io/v1"
kind: VerticalPodAutoscaler
metadata:
  name: flask-app
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind: Deployment
    name: flask-app-4
  updatePolicy:
    updateMode: "Off"  # You can set this to "Auto" if you want automatic updates
  resourcePolicy:
    containerPolicies:
      - containerName: '*'
        minAllowed:
          cpu: 100m
        maxAllowed:
          cpu: 1000m
        controlledResources: ["cpu"]
```

Output:
```bash
controlplane ~ ➜  kubectl get vpa
NAME        MODE   CPU   MEM   PROVIDED   AGE
flask-app   Off                           6s
```

---

**Initiate** the **load** on the **flask-app-4** **deployment** by executing the **script** located at `/root/load.sh`.
**Note:**
- The `/root/load.sh` script initiates continuous background load on the `flask-app-4` deployment.
- Please `do not terminate or interrupt` the load process, as Task 6 depends on the VPA having enough usage data to generate a `target` CPU recommendation.
Has the load been introduced?

```bash
# cat load.sh
#!/bin/bash

echo "Load initiated in the background. Please do not terminate this process."

timeout 1000s bash -c 'for i in {1..10}; do (while true; do curl -s http://controlplane:30080 > /dev/null; done) & done; wait'
```
---

Capture the **recommended `target CPU value`** from the **flask-app VPA** and store it in `/root/target`.
**Note:**
- If you `do not see a command prompt` after running the load script, it means the terminal is still busy running the script in the foreground.
- In that case, `please open a new terminal tab` to complete this task without interrupting the load.
Is the target CPU value recorded?
```bash
 kubectl get vpa
NAME        MODE   CPU    MEM   PROVIDED   AGE
flask-app   Off    143m         True       3m55s
controlplane ~ ➜  echo 143m > /root/target
```