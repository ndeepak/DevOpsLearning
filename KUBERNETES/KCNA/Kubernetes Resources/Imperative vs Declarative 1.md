# Imperative vs Declarative
## 1. The Core Concept
In simple terms:

|Approach|You tell the system...|System does...|
|---|---|---|
|**Imperative**|_Exactly how to do something_|Executes each command as instructed|
|**Declarative**|_What the final state should look like_|Figures out how to reach that state|
So —
- Imperative = Step-by-step instructions (“Do this, then that”)    
- Declarative = Desired state (“Make sure I have this configuration”)
    

---

## 2. In Infrastructure as Code (IaC)
Let’s use an analogy with **server provisioning**.

### Imperative Example
You are telling the system exactly **what to do and in which order**.
```bash
1. Provision a VM named "web-server"
2. Install nginx
3. Edit the configuration file to use port 8080
4. Change web root to /var/www/nginx
5. Pull code from GIT repo X
6. Start nginx
```

This is _procedural_ — like a recipe of commands.  
If something fails midway, you may need to rerun specific steps.

**Examples of imperative tools:**
- Manual shell scripting    
- Using `bash` scripts with `ssh`    
- Running `kubectl` commands one by one manually    

---

### Declarative Example
Here you don’t describe the steps.  
You just describe the **desired state** of the system.
```scss
VM Name: web-server
Package: nginx
Port: 8080
Path: /var/www/nginx
Code: GIT Repo - xxx
```
A **declarative tool** reads this file, compares it with the current state, and takes actions automatically to make the system match it.

**Examples of declarative tools:**
- **Ansible**    
- **Terraform**    
- **Puppet**    
- **Chef**    
- **Kubernetes YAML manifests**    

---

## 3. In the Kubernetes World
Kubernetes can work both ways — **imperative** and **declarative**.  
Let’s look at both with examples.

---

### A. **Imperative Approach**
This is when you directly tell Kubernetes what to do **through specific commands**.
#### Example commands:
```sh
kubectl run nginx --image=nginx
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80
kubectl edit deployment nginx
kubectl scale deployment nginx --replicas=5
kubectl set image deployment nginx nginx=nginx:1.18
```
Each command directly changes the state of the cluster _immediately_.

---

#### Two Use Cases in Imperative Approach
1. **Creating objects:**    
    `kubectl create -f nginx.yml`    
2. **Updating objects:**  
    You can use:    
```sh
kubectl edit deployment nginx
kubectl replace -f nginx.yaml
kubectl replace --force -f nginx.yaml
```    

If you delete and recreate the object:
```bash
kubectl delete -f nginx.yml
kubectl create -f nginx.yml
```
That’s still **imperative**, because you are manually instructing each step.

---

#### Advantages:
- Quick and simple for testing or one-time changes    
- Useful for ad-hoc actions and debugging    

#### Disadvantages:
- Hard to track or version changes    
- Not easily repeatable or reusable    
- Prone to human error    
- No automatic reconciliation (Kubernetes won’t “remember” your intent)    

---

### B. **Declarative Approach**
This is the recommended, production-grade way to manage Kubernetes configurations.
You define the desired state in YAML files and let Kubernetes handle the rest.
Example command:
`kubectl apply -f nginx.yml`

If the resource doesn’t exist, it **creates** it.  
If it already exists, it **updates** it to match the YAML.

---

#### Two Use Cases in Declarative Approach
1. **Create objects**    
    `kubectl apply -f nginx.yml`
    `kubectl apply -f /path/to/config-files/`
    
2. **Update objects**    
    `kubectl apply -f nginx.yml`    

You don’t need to use separate commands for creation and modification — `kubectl apply` handles both.

---

#### Advantages
- Easy to version control (store YAML in Git)    
- Consistent and repeatable    
- Supports GitOps workflows (using tools like ArgoCD, Flux)    
- Kubernetes reconciles state automatically if something changes or fails    
- Easier collaboration among teams    

#### Disadvantages:
- Requires learning YAML and Git workflows    
- Changes are not as “immediate” — might need `kubectl diff` or similar to preview    

---
## 4. Comparison Summary

|Feature|Imperative|Declarative|
|---|---|---|
|**Style**|Step-by-step instructions|Desired final state|
|**Command Examples**|`kubectl run`, `kubectl create`, `kubectl edit`, `kubectl delete`|`kubectl apply -f <file>`|
|**Speed**|Fast for one-off changes|Better for long-term management|
|**Version Control**|Hard to track|YAML files stored in Git|
|**Repeatability**|Manual repetition|Automated, reproducible|
|**Use Case**|Testing, quick setup|Production, automation, GitOps|
|**Reconciliation**|No automatic reconciliation|Kubernetes ensures state consistency|

---
## 5. Practical Example
Let’s assume we have a Deployment YAML (`nginx.yml`):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.18
        ports:
        - containerPort: 80
```

### Using **Imperative** Commands
```sh
kubectl create -f nginx.yml
kubectl scale deployment nginx --replicas=5
kubectl set image deployment nginx nginx=nginx:1.19
kubectl delete -f nginx.yml
```

### Using **Declarative** Commands
`kubectl apply -f nginx.yml`

If you later modify `replicas: 5` and run `kubectl apply -f nginx.yml`,  
Kubernetes updates it automatically — no need for a separate scale command.

---
## 6. Summary
- **Imperative:** You say _how_ to reach the goal. (Do this, then that)
- **Declarative:** You say _what_ the goal is. (Make sure it looks like this)    
- **Imperative commands** are good for learning and quick testing.    
- **Declarative manifests** are best for automation, GitOps, and production environments.

---

