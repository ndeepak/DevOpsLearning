# Monitoring Cluster Components


Monitoring Solutions
* Metrics Server
* Prometheus
* Elastic Stack
* Datadog
* Dynatrace


Heapster VS Metrics Server
Deprecated

Metrics Server
cAdvisor
kubelet


```bash
minikube addons enable metrics-server

git clone https://github.com/kubernetes-sigs/metrics-server.git

kubectl create -f deploy/1.8+/

kubectl top node
kubectl top pod
```



