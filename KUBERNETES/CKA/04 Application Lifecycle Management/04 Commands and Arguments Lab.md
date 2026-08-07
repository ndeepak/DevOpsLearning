# Commands and Arguments Lab

How many PODs exist on the system?
In the current(default) namespace
```bash
controlplane ~ ➜  kubectl get pods
NAME             READY   STATUS    RESTARTS   AGE
ubuntu-sleeper   1/1     Running   0          34s
```


What is the command used to run the pod `ubuntu-sleeper`?
```bash
controlplane ~ ✖ kubectl get pod ubuntu-sleeper -o yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: "2026-08-05T06:05:20Z"
  generation: 1
  name: ubuntu-sleeper
  namespace: default
  resourceVersion: "950"
  uid: 145e290b-bf6b-41c3-a33d-44bdb37ce580
spec:
  containers:
  - command:
    - sleep
    - "4800"
```


Create a pod with the ubuntu image to run a container to sleep for 5000 seconds. Modify the file `ubuntu-sleeper-2.yaml`.
```yaml
apiVersion: v1 
kind: Pod 
metadata:
  name: ubuntu-sleeper-2 
spec:
  containers:
  - name: ubuntu
    image: ubuntu
    command:
      - "sleep"
      - "5000"
```

Create a pod using the file named `ubuntu-sleeper-3.yaml`. There is something wrong with it. Try to fix it!

```yaml
apiVersion: v1 
kind: Pod 
metadata:
  name: ubuntu-sleeper-3 
spec:
  containers:
  - name: ubuntu
    image: ubuntu
    command:
      - "sleep"
      - "1200"
```

Update pod `ubuntu-sleeper-3` to sleep for 2000 seconds.
```yaml
apiVersion: v1 
kind: Pod 
metadata:
  name: ubuntu-sleeper-3 
spec:
  containers:
  - name: ubuntu
    image: ubuntu
    command:
      - "sleep"
      - "2000"
```

A Dockerfile named `Dockerfile` is located at `/root/webapp-color`.
**Inspect it carefully and identify which command will be executed when a container is started from this image.**
```bash
 cat Dockerfile
FROM python:3.6-alpine

RUN pip install flask

COPY . /opt/

EXPOSE 8080

WORKDIR /opt

ENTRYPOINT ["python", "app.py"]
```


A Dockerfile named `Dockerfile2` is located at `/root/webapp-color`.
```bash
controlplane ~/webapp-color ➜  cat Dockerfile2 
FROM python:3.6-alpine

RUN pip install flask

COPY . /opt/

EXPOSE 8080

WORKDIR /opt

ENTRYPOINT ["python", "app.py"]

CMD ["--color", "red"]
```



You are given a directory `webapp-color-2` that contains a `Dockerfile` and a Kubernetes pod YAML file `webapp-color-pod.yaml`.
**When the Pod defined in `webapp-color-pod.yaml` starts, which command will actually run inside the container?**
```bash
 cat Dockerfile 
FROM python:3.6-alpine

RUN pip install flask

COPY . /opt/

EXPOSE 8080

WORKDIR /opt

ENTRYPOINT ["python", "app.py"]

CMD ["--color", "red"]


 cat webapp-color-pod.yaml 
apiVersion: v1 
kind: Pod 
metadata:
  name: webapp-green
  labels:
      name: webapp-green 
spec:
  containers:
  - name: simple-webapp
    image: kodekloud/webapp-color
    command: ["--color","green"]

```


You are given a directory `webapp-color-3` that contains a `Dockerfile` and a Kubernetes pod YAML file `webapp-color-pod-2.yaml`.
**When the Pod defined in `webapp-color-pod-2.yaml` starts, which command will actually run inside the container?**

```bash
 cat Dockerfile 
FROM python:3.6-alpine

RUN pip install flask

COPY . /opt/

EXPOSE 8080

WORKDIR /opt

ENTRYPOINT ["python", "app.py"]

CMD ["--color", "red"]

controlplane ~/webapp-color-3 ➜  cat webapp-color-pod-2.yaml 
apiVersion: v1 
kind: Pod 
metadata:
  name: webapp-green
  labels:
      name: webapp-green 
spec:
  containers:
  - name: simple-webapp
    image: kodekloud/webapp-color
    command: ["python", "app.py"]
    args: ["--color", "pink"]
```


---
**Task:** Create a Kubernetes Pod that runs a web application with a green background.
**Requirements:**
- **Pod Name:** `webapp-green`
- **Docker Image:** `kodekloud/webapp-color`
- The application must display a **green background** instead of the default blue.
- **Pass the command-line argument:** `--color=green` as **container arguments (args)**, not as a command.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: webapp-green
spec:
  containers:
  - name: webapp-color
    image: kodekloud/webapp-color
    args: ["--color=green"]
```