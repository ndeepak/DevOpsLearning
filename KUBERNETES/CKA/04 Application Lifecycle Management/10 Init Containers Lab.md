# Init Containers Lab

Identify the pod that has an `initContainer` configured.
```bash
kubectl get pods
kubectl describe pod <pod-name>
```

What is the image used by the `initContainer` on the `blue` pod?
`busybox`
What is the state of the `initContainer` on pod `blue`?
`Terminated`

Why is the `initContainer` terminated? What is the reason?
`Completed`

We just created a new pod named `purple`. How many `initContainers` does it have?
`kubectl describe pod purple`


What is the **lifecycle status** of the `purple` pod?
(Use the command `kubectl describe pod purple` and check the Status field.)
```bash
 kubectl get pods
NAME     READY   STATUS     RESTARTS   AGE
blue     1/1     Running    0          4m45s
green    2/2     Running    0          4m45s
purple   0/1     Init:0/2   0          92s
red      1/1     Running    0          4m45s
```

How long after the creation of the `purple` POD will the application come up and be available to users?
600+1200 seconds

Update the pod `red` to use an `initContainer` named `red-initcontainer` that uses the `busybox` image and `sleeps for 20` seconds
Delete and re-create the pod if necessary. But make sure no other configurations change.
```yaml
spec:
  initContainers:
  - image: busybox
    name: red-initcontainer
    command: ["sleep","20"]
```

A new application `orange` is deployed. There is something wrong with it. Identify and fix the issue.
Once fixed, wait for the application to run before checking solution.
sleep spelling wrong

