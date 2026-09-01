# Demo Cluster Upgrade
https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/

Important notice regarding package and repository:
https://kubernetes.io/blog/2023/08/15/pkgs-k8s-io-introduction/


```bash
```shell
sudo apt update
sudo apt-cache madison kubeadm
```

```shell
sudo apt-mark unhold kubeadm && \
sudo apt-get update && sudo apt-get install -y kubeadm='1.36.x-*' && \
sudo apt-mark hold kubeadm
```

```shell
kubeadm version
```

```shell
sudo kubeadm upgrade plan
```

```shell
sudo kubeadm upgrade apply v1.36.x
```

```shell
kubectl get node
```

# Upgrading node
```shell
sudo kubeadm upgrade node
```

```shell
sudo kubeadm upgrade apply
```

```shell
kubectl drain <node-to-drain> --ignore-daemonsets
```


## Upgrading kubelet and kubectl
```shell
# replace x in 1.36.x-* with the latest patch version
sudo apt-mark unhold kubelet kubectl && \
sudo apt-get update && sudo apt-get install -y kubelet='1.36.x-*' kubectl='1.36.x-*' && \
sudo apt-mark hold kubelet kubectl
```

```shell
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

```shell
kubectl get nodes
```