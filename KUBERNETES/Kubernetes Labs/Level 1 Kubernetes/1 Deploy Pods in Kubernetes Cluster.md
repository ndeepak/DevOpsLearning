The Nautilus DevOps team is diving into Kubernetes for application management. One team member has a task to create a pod according to the details below:
1. Create a pod named `pod-nginx` using the `nginx` image with the `latest` tag. Ensure to specify the tag as `nginx:latest`.
2. Set the `app` label to `nginx_app`, and name the container as `nginx-container`.
`Note`: The `kubectl` utility on `jump_host` is configured to operate with the Kubernetes cluster.


```bash
kubectl run pod-nginx \
  --image=nginx:latest \
  --labels="app=nginx_app" \
  --container-name=nginx-container
  
# one line
kubectl run pod-nginx --image=nginx:latest --labels="app=nginx_app"  --container-name=nginx-container
```

### **YAML Method**
Create a YAML file:
`kubectl run pod-nginx --image=nginx:latest --labels="app=nginx_app" --dry-run=client -o yaml > pod.yaml`
Then edit `pod.yaml` and modify:
```yaml
containers:
- name: nginx-container
  image: nginx:latest
```
Apply it:
`kubectl apply -f pod.yaml`

---
