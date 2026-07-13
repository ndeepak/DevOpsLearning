# Exam Tips
Here’s a tip!

As you might have seen already, creating and editing YAML files is a bit difficult, especially in the CLI. During the exam, you might find it difficult to copy and paste YAML files from the browser to the terminal. Using the `kubectl run` command can help in generating a YAML template. And sometimes, you can even get away with just the `kubectl run` command without having to create a YAML file at all. For example, if you were asked to create a pod or deployment with a specific name and image, you can simply run the `kubectl run` command.

Use the below set of commands and try the previous practice tests again, but this time, try to use the below commands instead of YAML files. Try to use these as much as you can going forward in all exercises.

Reference (Bookmark this page for the exam. It will be very handy):

[https://kubernetes.io/docs/reference/kubectl/conventions/](https://kubernetes.io/docs/reference/kubectl/conventions/)

Create an NGINX Pod

```
kubectl run nginx --image=nginx
```

Generate POD Manifest YAML file (-o yaml). Don’t create it(–dry-run)

```
kubectl run nginx --image=nginx --dry-run=client -o yaml
```

Create a deployment

```
kubectl create deployment --image=nginx nginx
```

Generate Deployment YAML file (-o yaml). Don’t create it(–dry-run)

```
kubectl create deployment --image=nginx nginx --dry-run=client -o yaml
```

Generate Deployment YAML file (-o yaml). Don’t create it(–dry-run) and save it to a file.

```
kubectl create deployment --image=nginx nginx --dry-run=client -o yaml > nginx-deployment.yaml
```

Make necessary changes to the file (for example, adding more replicas) and then create the deployment.

```
kubectl create -f nginx-deployment.yaml
```

OR

In k8s version 1.19+, we can specify the –replicas option to create a deployment with 4 replicas.

```
kubectl create deployment --image=nginx nginx --replicas=4 --dry-run=client -o yaml > nginx-deployment.yaml
```

---


# Quick Summary

Although **Declarative (`kubectl apply`)** is the recommended approach for Kubernetes, **Imperative commands** are extremely useful for quick tasks, troubleshooting, and especially during CKA/CKAD exams.

## Useful Options

### `--dry-run=client`

- Validates the command without creating the resource.
- Useful for testing commands.

```
kubectl run nginx --image=nginx --dry-run=client
```

### `-o yaml`

- Prints the resource definition in YAML format instead of creating it.

```
kubectl run nginx --image=nginx --dry-run=client -o yaml
```

### Best Practice

Use both options together to quickly generate YAML manifests instead of writing them manually.

```
kubectl <command> --dry-run=client -o yaml > resource.yaml
```

Edit the YAML if needed, then create/apply it.

```
kubectl apply -f resource.yaml
```

---

# Common Commands

## Pod

Create Pod

```
kubectl run nginx --image=nginx
```

Generate Pod YAML

```
kubectl run nginx --image=nginx --dry-run=client -o yaml
```

---

## Deployment

Create Deployment

```
kubectl create deployment nginx --image=nginx
```

Generate Deployment YAML

```
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml
```

Create with Replicas

```
kubectl create deployment nginx --image=nginx --replicas=4
```

Scale Existing Deployment

```
kubectl scale deployment nginx --replicas=4
```

Generate YAML to File

```
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml > deployment.yaml
```

---

## Service

### ClusterIP

Generate YAML

```
kubectl expose pod redis --port=6379 --name=redis-service --dry-run=client -o yaml
```

or

```
kubectl create service clusterip redis --tcp=6379:6379 --dry-run=client -o yaml
```

**Recommendation:** Prefer `kubectl expose` because it automatically uses the Pod's labels as selectors.

---

### NodePort

Generate YAML

```
kubectl expose pod nginx --type=NodePort --port=80 --name=nginx-service --dry-run=client -o yaml
```

or

```
kubectl create service nodeport nginx --tcp=80:80 --node-port=30080 --dry-run=client -o yaml
```

**Recommendation:** Use `kubectl expose`, then manually add the `nodePort` field to the generated YAML before applying it.

---

# Key Takeaways

- Use **Declarative (`kubectl apply`)** for production.
- Use **Imperative commands** for quick tasks and exams.
- Use **`--dry-run=client -o yaml`** to generate YAML templates quickly.
- Modify the generated YAML as needed, then create resources using:

```
kubectl apply -f <file>.yaml
```

This approach saves time and avoids writing manifests from scratch.