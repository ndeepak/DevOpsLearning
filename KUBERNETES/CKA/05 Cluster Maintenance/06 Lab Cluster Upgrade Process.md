# Lab Cluster Upgrade Process
Question 1 of 13
This lab tests your skills on **upgrading a kubernetes cluster**. We have a production cluster with applications running on it. Let us explore the setup first.
What is the current version of the cluster?
`kubectl get nodes -o wide`

How many nodes are part of this cluster?
Including controlplane and worker nodes
`2`

How many nodes can host workloads in this cluster?
Inspect the applications and taints set on the nodes.
`2` no taints on both

How many applications are hosted on the cluster?
Count the number of deployments in the `default` namespace.
```
 kubectl get deployments.apps 
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
blue   5/5     5            5           5m29s
```

What nodes are the pods hosted on?
both

You are tasked to upgrade the cluster. Users accessing the applications must not be impacted, and you cannot provision new VMs. What strategy would you use to upgrade the cluster?
- Users will be impacted since there is only one worker node
- **Upgrade one node at a time while moving the workloads to the other**
- Add new nodes with newer versions while taking down existing nodes
- Upgrade all nodes at once


What is the latest version available for an upgrade with the current version of the kubeadm tool installed?
Use the `kubeadm` tool

We will be upgrading the controlplane node first. Drain the controlplane node of workloads and mark it `UnSchedulable`
`kubectl drain controlplane --ignore-daemonsets`

---

Upgrade the `controlplane` components to exact version `v1.35.0`
Upgrade the kubeadm tool (if not already), then the controlplane components, and finally the kubelet. Practice referring to the Kubernetes documentation page.
On the `controlplane` node:
Use any text editor you prefer to open the file that defines the Kubernetes apt repository.
```sh
vim /etc/apt/sources.list.d/kubernetes.list
```

Update the version in the URL to the next available minor release, i.e v1.35.

```sh
deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.35/deb/ /
```

After making changes, save the file and exit from your text editor. Proceed with the next instruction.

```sh
apt update

apt-cache madison kubeadm
```

Based on the version information displayed by `apt-cache madison`, it indicates that for Kubernetes version `1.35.0`, one of the available package versions is `1.35.0-1.1`. Therefore, to install kubeadm for Kubernetes `v1.35.0`, use the following command:

```sh
apt-get install kubeadm=1.35.0-1.1
```

Run the following command to upgrade the Kubernetes cluster.

```sh
kubeadm upgrade plan v1.35.0

kubeadm upgrade apply v1.35.0
```

> Note that the above steps can take a few minutes to complete.

Now, upgrade the `Kubelet` version. Also, mark the node (in this case, the "controlplane" node) as schedulable.

```sh
apt-get install kubelet=1.35.0-1.1
```

Run the following commands to refresh the systemd configuration and apply changes to the `Kubelet` service:

```sh
systemctl daemon-reload

systemctl restart kubelet
```

---
Mark the `controlplane` node as "Schedulable" again
`kubectl uncordon controlplane`

Next is the worker node. `Drain` the worker node of the workloads and mark it `UnSchedulable`
`kubectl drain node01 --ignore-daemonsets`


---
Upgrade the worker node to the exact version `v1.35.0`
**Note:**
- Run `kubeadm upgrade node` only once on the worker node. Re-running it may lead to errors like:
```
no flags found in file "/var/lib/kubelet/kubeadm-flags.env"
```
- In a rare case, kubelet may fail to start after upgrade. If this happens, remove the deprecated flag (--pod-infra-container-image) and restart the kubelet.
On the `node01` node, run the following commands:

> If you are on the `controlplane` node, run `ssh node01` to log in to the `node01`.

Use any text editor you prefer to open the file that defines the Kubernetes apt repository.

```sh
vim /etc/apt/sources.list.d/kubernetes.list
```

Update the version in the URL to the next available minor release, i.e v1.35.

```sh
deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.35/deb/ /
```

After making changes, save the file and exit from your text editor. Proceed with the next instruction.

```sh
apt update

apt-cache madison kubeadm
```

Based on the version information displayed by `apt-cache madison`, it indicates that for Kubernetes version `1.35.0`, the available package version is `1.35.0-1.1`. Therefore, to install kubeadm for Kubernetes `v1.35.0`, use the following command:

```sh
apt-get install kubeadm=1.35.0-1.1

# Upgrade the node 
kubeadm upgrade node
```

Now, upgrade the `Kubelet` version.

```sh
apt-get install kubelet=1.35.0-1.1
```

Run the following commands to refresh the systemd configuration and apply changes to the `Kubelet` service:

```sh
systemctl daemon-reload

systemctl restart kubelet
```

> Type `exit` or `logout` or enter `CTRL + d` to go back to the `controlplane` node.

---
Remove the restriction and mark the worker node as schedulable again.
```
kubectl uncordon node01
```

