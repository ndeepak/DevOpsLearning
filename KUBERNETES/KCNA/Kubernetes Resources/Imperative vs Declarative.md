# Imperative vs Declarative

Imperative and Declarative Approaches in the kubernetes

Objects creations
Different Approaches

Imperative and Declarative approach

In Infrastructure as a Code world,
Imperative:
1. Provision a VM by the name "web-server"
2. Install NGINX on it
3. Edit Configuration file to use port "8080"
4. Edit Configuration file to web path "/var/www/nginx"
5. Load web pages to "/var/www/nginx" from GIT repo -X
6. Start NGINX Server
Example,


Declarative:
```scss
VM Name: web-server
Package: nginx
Port: 8080
Path: /var/www/nginx
Code: GIT Repo - xxx
```
Example, Ansible, Terraform, Puppet, etc.

---
In Kubernetes world,
Imperative
```zsh
kubectl run --image=nginx nginx
kubectl create deployment --image=nginx nginx
kubectl expose deployment nginx --port 80
kubectl edit deployment nginx
kubectl scale deployment nginx --replicas=5
kubectl set image deployment nginx nginx=nginx:1.18
kubectl create -f nginx.yml
kubectl replace -f nginx.yml
kubectl delete -f nginx.yml
```
Two ways:
Creating objects
```zsh
kubectl create -f nginx.yml
```
Updating objects
```zsh
kubectl edit deployment nginx

kubectl replace -f nginx.yaml

kubectl replace --force -f nginx.yaml

kubectl create -f nginx.yml
```

Declarative:
```zsh
kubectl apply -f nginx.yml
```
Two Ways:
Create Objects
```zsh
kubectl apply -f nginx.yml

kubectl apply -f /path/to/config-files
```

Update Objects
```zsh
kubectl apply -f nginx.yml
```

