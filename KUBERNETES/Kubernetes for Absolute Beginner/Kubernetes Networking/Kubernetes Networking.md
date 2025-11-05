# **Kubernetes Networking — Complete Guide (with Examples)**

---
## 1. What is Kubernetes Networking?
Kubernetes Networking allows:
- **Pods**, **Nodes**, and **Services** to communicate with each other.\
- Applications running inside containers to reach one another seamlessly — just like on a normal network.

Kubernetes networking model follows **four golden rules**:

| Rule | Description                                                                                     |
| ---- | ----------------------------------------------------------------------------------------------- |
| 1    | All Pods can communicate with all other Pods in the cluster **without NAT**.                    |
| 2    | All Nodes can communicate with all Pods (and vice versa) **without NAT**.                       |
| 3    | A Pod gets its **own IP address**.                                                              |
| 4    | Containers within the same Pod **share the same network namespace** (same IP, different ports). |

---
## 2. Single Node Kubernetes Cluster (Minikube Setup)
In a **single-node cluster** (like Minikube), everything — master components, kubelet, and pods — runs on **one node**.
Let’s see how it looks:
```lua
+---------------------------------------+
| Node (Minikube)                       |
|---------------------------------------|
| kube-apiserver, controller, scheduler  |  ← Master components
| kubelet, kube-proxy                    |  ← Worker agent
|---------------------------------------|
| Pod 1 (nginx) → IP: 10.244.0.2        |
| Pod 2 (redis) → IP: 10.244.0.3        |
| Pod 3 (app)   → IP: 10.244.0.4        |
+---------------------------------------+
```

Even though it’s one machine, **each Pod gets its own IP** from a virtual subnet (like `10.244.0.x`).

## Kubernetes Pod and IP Addressing
- Each pod in Kubernetes gets its own unique IP address.
- Containers in the same pod share the same network namespace, so they communicate over localhost.
- Pods can communicate to other pods directly using IP addresses without NAT (Network Address Translation).
- All nodes and pods can communicate with each other freely within the cluster networking model.

---

## 3. Pod Networking Basics
### Every Pod gets its own IP
Each Pod runs inside a network namespace. Containers inside that Pod share:
- The same IP address    
- The same network interfaces    

You can test this easily.

---

### Example: Create Two Pods
**Step 1:** Create nginx pod
`kubectl run nginx --image=nginx --restart=Never`

**Step 2:** Create busybox pod
`kubectl run busybox --image=busybox --restart=Never -it -- /bin/sh`

**Step 3:** Get Pod IPs
`kubectl get pods -o wide`

Example output:
```nginx
NAME      READY   STATUS    IP           NODE
nginx     1/1     Running   10.244.0.5   minikube
busybox   1/1     Running   10.244.0.6   minikube
```

---
### Step 4: Ping from busybox → nginx
Inside busybox shell:
`ping 10.244.0.5`
Output: You can ping directly without NAT!

That’s Kubernetes Pod-to-Pod communication in action.

---
## 4. How Does This Work Internally?
When you start Minikube, it sets up a **Container Network Interface (CNI)** plugin.  
This creates a **virtual network bridge** (like `cni0`) inside the node.
Each Pod gets an IP from a subnet allocated by that plugin.
**CNI plugins examples:**
- Flannel    
- Calico    
- Weave    
- Cilium    

Example: With Flannel
`cni0 bridge → assigns IPs like 10.244.0.x`

---

## 5. Communication Between Nodes (Multi-node Cluster Concept)
In a **multi-node cluster**, Kubernetes ensures:
- Pods on Node A can talk to Pods on Node B.    
- Every node’s Pod CIDR (like `10.244.1.0/24`, `10.244.2.0/24`) is reachable cluster-wide.
Example diagram:
```scss
[ Node 1 ]                          [ Node 2 ]
PodA(10.244.1.2)                    PodC(10.244.2.3)
PodB(10.244.1.3)                    PodD(10.244.2.4)

        ↕                                  ↕
   CNI Plugin (Flannel/Calico) connects the two nodes
```
All this routing is managed by your **CNI plugin**, not by Kubernetes itself.

---
## 6. Static IPs for Pods
Kubernetes **does not recommend assigning static IPs** to Pods, because:
- Pods are ephemeral (they can die anytime).    
- New Pods get new IPs.    

But if you want **a stable IP or endpoint**, you use a **Service**.

---

## 7. Internal Networking: Services
When Pods are created dynamically, their IPs keep changing.  
To solve this, Kubernetes introduces **Service objects** — they provide a **stable IP and DNS name** to reach your application.
Example YAML:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 80
  type: ClusterIP
```
Create it:
`kubectl apply -f service.yml `
`kubectl get svc`

Example output:
```pgsql
NAME             TYPE        CLUSTER-IP      PORT(S)
myapp-service    ClusterIP   10.96.123.45    80/TCP
```
Now all Pods can access your app via `myapp-service:80` internally — even if the Pod IP changes!

---

## 8. Kubernetes Networking Layers Overview

|Layer|Object|Purpose|
|---|---|---|
|**Pod Network**|Pod ↔ Pod|All Pods can talk directly without NAT|
|**Node Network**|Node ↔ Pod|Each Node can reach all Pods|
|**Service Network**|Stable access endpoint|ClusterIP, NodePort, LoadBalancer|
|**Ingress**|HTTP routing|Routes external HTTP(S) traffic to services|

---

## 9. Verify Cluster Networking in Minikube
You can test your networking using these commands:
```bash
# Get node IP
kubectl get nodes -o wide

# Get pod IPs
kubectl get pods -o wide

# Get cluster IPs of services
kubectl get svc -o wide
```
To debug Pod communication:
```bash
kubectl exec -it busybox -- ping nginx
kubectl exec -it busybox -- nslookup myapp-service
```

---

## 10. Summary Table

|Concept|Description|Example|
|---|---|---|
|Pod IP|Each Pod has unique IP|`10.244.0.5`|
|NAT|Not used inside cluster|Direct communication|
|CNI Plugin|Handles routing|Flannel, Calico|
|Service|Provides stable IP|`myapp-service`|
|Node|Worker machine|Minikube|
|ClusterIP|Internal service IP|Default type|
|NodePort|Exposes service on node port|External access|

---

## Bonus: Exposing App to External Network
To access your app from outside Minikube:
```bash
kubectl expose deployment nginx --type=NodePort --port=80
kubectl get svc
```
Output:
```pgsql
NAME         TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
nginx        NodePort   10.96.0.1      <none>        80:31345/TCP   2m
```

Then run:
`minikube service nginx`

This opens your nginx app in the browser!

---

## Key Takeaways
- Every **Pod** has its **own IP**.    
- All **Pods and Nodes can communicate** without NAT.    
- Use **Services** for stable IPs and internal DNS names.    
- **CNI plugins** handle routing and IP allocation.    
- In **Minikube**, everything runs on one host, but Kubernetes networking rules still apply.