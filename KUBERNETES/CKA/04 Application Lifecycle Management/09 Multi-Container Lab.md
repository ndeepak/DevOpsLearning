# Multi-Container Lab

Identify the number of containers created in the `red` pod.
```bash
controlplane ~ ➜  kubectl get pods
NAME        READY   STATUS    RESTARTS   AGE
app         1/1     Running   0          2m31s
fluent-ui   1/1     Running   0          2m31s
red         3/3     Running   0          2m16s
```
`3`

Identify the name of the containers running in the `blue` pod.
` kubectl describe pod blue`
`teal and navy`


Create a multi-container pod named `yellow` that includes `2` containers as specified below:
1. **Container 1**    
    - Name: `lemon`
    - Image: `busybox`
2. **Container 2**    
    - Name: `gold`
    - Image: `redis`
If the pod encounters a `crashloopbackoff` status, modify the `lemon` container to include the command `sleep 1000`.
Is the pod named yellow created?
Is Container 1 named lemon?
Does Container 1 utilize the busybox image?
Is Container 2 named gold?
Does Container 2 utilize the redis image?

```yaml 
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: pod
  name: yellow
spec:
  containers:
    - image: busybox
      name: lemon
      command: ["sleep", "1000"]

    - image: redis
      name: gold
  dnsPolicy: ClusterFirst
  restartPolicy: Always
```


We have deployed an application logging stack in the `elastic-stack` namespace. Inspect it.
Before proceeding with the next set of questions, please wait for all the pods in the `elastic-stack` namespace to be ready. This can take a few minutes.

Once the pod is in a ready state, inspect the Kibana UI using the link above your terminal. There shouldn't be any logs for now.
We will configure a sidecar container for the application to send logs to Elastic Search.   
NOTE: It can take a couple of minutes for the `Kibana` UI to be ready after the `Kibana` pod is ready.
You can inspect the `Kibana` logs by running:  
`kubectl -n elastic-stack logs kibana`




Inspect the `app` pod and identify the number of containers in it.
It is deployed in the `elastic-stack` namespace.
```bash
 kubectl get pods -n elastic-stack 
NAME             READY   STATUS    RESTARTS   AGE
app              1/1     Running   0          17m
elastic-search   1/1     Running   0          17m
kibana           1/1     Running   0          17m
```


The application outputs logs to the file `/log/app.log`. View the logs and try to identify the user having issues with Login.
Inspect the log file located inside the pod by utilizing the kubectl exec command.
```bash
kubectl exec app -- tail -f /log/app.log
[2026-08-10 06:35:52,962] INFO in event-simulator: USER4 logged in
[2026-08-10 06:35:53,312] INFO in event-simulator: USER4 logged in
[2026-08-10 06:35:53,963] WARNING in event-simulator: USER7 Order failed as the item is OUT OF STOCK.
[2026-08-10 06:35:53,964] INFO in event-simulator: USER1 logged in
[2026-08-10 06:35:54,313] INFO in event-simulator: USER2 logged in
[2026-08-10 06:35:54,965] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2026-08-10 06:35:54,965] INFO in event-simulator: USER2 is viewing page1
[2026-08-10 06:35:55,314] INFO in event-simulator: USER1 logged out
[2026-08-10 06:35:55,966] INFO in event-simulator: USER2 logged in
[2026-08-10 06:35:56,315] INFO in event-simulator: USER2 is viewing page3
[2026-08-10 06:35:56,967] INFO in event-simulator: USER4 logged out
[2026-08-10 06:35:57,317] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2026-08-10 06:35:57,317] INFO in event-simulator: USER3 is viewing page3
```
`USER5`



The `app` pod in the `elastic-stack` namespace currently writes logs to `/log/app.log`.  
Your task is to add a sidecar container that will ship these logs to Elasticsearch.
**Requirements:**
1. **Add a sidecar container** named `sidecar` to the existing `app` pod.
2. **Use the image:** `kodekloud/filebeat-configured`.
3. **Mount the log volume:** The existing `log-volume` must be mounted to the sidecar container at `/var/log/event-simulator/`.
4. **Implementation:** Define the sidecar as a Kubernetes native sidecar container using `initContainers`, and set the `restartPolicy` to `Always`.
**Important Notes:**
- You will need to **delete and re-create** the pod to add the sidecar container.
- Do not modify the existing app container or volume configuration.
- The sidecar should be defined as an `initContainer` and must run continuously alongside the main application container
- Refer to the diagram below for your configuration.
**Reference Documentation:**
- Sidecar Containers: [https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/)
**Note:** State persistence concepts are discussed in detail later in this course. For now, follow the pattern shown in the reference documentation.
```bash

controlplane ~/elastic-search ➜  cat app.yaml 
apiVersion: v1
kind: Pod
metadata:
  name: app
  namespace: elastic-stack
  labels:
    name: app
spec:
  initContainers:
    - name: sidecar
      image: kodekloud/filebeat-configured
      restartPolicy: Always
      volumeMounts:
        - name: log-volume
          mountPath: /var/log/event-simulator
  containers:
  - name: app
    image: kodekloud/event-simulator
    volumeMounts:
    - mountPath: /log
      name: log-volume

  volumes:
  - name: log-volume
    hostPath:
      path: /var/log/webapp
      type: DirectoryOrCreate
```

