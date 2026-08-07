# Secrets Lab

How many `Secrets` exist on the system? In the current(default) namespace.
```bash
controlplane ~ ➜  kubectl get secrets
NAME              TYPE                                  DATA   AGE
dashboard-token   kubernetes.io/service-account-token   3      2m17s
```
How many secrets (data keys) are defined in the `dashboard-token` secret?
`3`

What is the type of the `dashboard-token` secret?
`kubernetes.io/service-account-token`

Which of the following is not a secret data defined in `dashboard-token` secret?
`type`


We are going to deploy an application with the below architecture
We have already deployed the required pods and services. Check out the pods and services created. Check out the web application using the `Webapp MySQL` link above your terminal, next to the Quiz Portal Link.
![](Attachments/Pasted%20image%2020260806114957.png)

The reason the application is failed is because we have not created the secrets yet. Create a new secret named `db-secret` with the data given below.
You may follow any one of the methods discussed in lecture to create the secret.
```yaml
controlplane ~ ✦ ➜  cat secret.yaml 
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
data:
  DB_Host: c3FsMDE=
  DB_User: cm9vdA==
  DB_Password: cGFzc3dvcmQxMjM=
```

  

Configure the `webapp-pod` to load environment variables from the `db-secret` secret you created in the previous task.
**Note:**
- Use `envFrom` with `secretRef` to load ALL secret keys as environment variables
- The pod must be deleted and recreated (environment variables cannot be updated on running pods)
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: webapp-pod
  labels:
    name: webapp-pod
  namespace: default
spec:
  containers:
  - name: webapp
    image: kodekloud/simple-webapp-mysql
    imagePullPolicy: Always
    envFrom:
    - secretRef:
        name: db-secret
```

```bash
kubectl apply -f pod-definition.yaml
```

View the web application to verify it can successfully connect to the database
