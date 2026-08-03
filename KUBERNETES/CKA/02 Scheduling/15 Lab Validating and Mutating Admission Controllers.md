Lab 15 Validating and Mutating Admission Controllers

Which of the below combination is correct for Mutating and validating
admission controllers ?
NamespaceAutoProvision- Mutating, NamespaceExists - Mutating
NamespaceAutoProvision- Validating, NamespaceExists - Validating
**NamespaceAutoProvision- Mutating, NamespaceExists - Validating**
NamespaceAutoProvision- Validating, NamespaceExists - Mutating

Why this combination is correct:

- **NamespaceAutoProvision (Mutating)**: This controller checks if a resource is being deployed into a namespace that does not exist. If it's missing, it **mutates** the state by automatically creating that namespace. 
- **NamespaceExists (Validating)**: This controller strictly **validates** the existence of a namespace. If a request tries to deploy a resource into a namespace that is missing, it will immediately reject the request with an error instead of trying to fix it. []

❌ Why the other options are incorrect:

- **NamespaceAutoProvision - Validating, NamespaceExists - Validating**: Incorrect because `NamespaceAutoProvision` modifies/creates resources, making it a mutating controller. 

- **NamespaceAutoProvision - Mutating, NamespaceExists - Mutating**: Incorrect because `NamespaceExists` only checks for presence and never alters the incoming object or creates a namespace. [[

- **NamespaceAutoProvision - Validating, NamespaceExists - Mutating**: Incorrect because it completely reverses the operational nature of both controllers. 
---
What is the flow of invocation of admission controllers?
Mutating and Validating at same time
**First Mutating then Validating**
Mutating and Validating can run in any order
First Validating then Mutating

---

Create namespace `webhook-demo` where we will deploy webhook components
webhook-demo namespace created?

```
kubectl create namespace webhook-demo
```

---

Create a **TLS secret** named `webhook-server-tls` in the `webhook-demo` namespace.
This secret will be used by the admission webhook server for secure communication over HTTPS.


We have already created below cert and key for webhook server which should be used to create secret.
Certificate : `/root/keys/webhook-server-tls.crt`
Key : `/root/keys/webhook-server-tls.key`
Is the webhook-server-tls of the tls secret type created correctly?

```
kubectl -n webhook-demo create secret tls webhook-server-tls \
    --cert "/root/keys/webhook-server-tls.crt" \
    --key "/root/keys/webhook-server-tls.key"
```

---

Create the webhook deployment that will run the admission webhook server.
We have already provided the deployment manifest at:
```
/root/webhook-deployment.yaml
```
Create the deployement using this definition.
webhook-server deployed?
```
kubectl create -f /root/webhook-deployment.yaml
```


---
Create a service that exposes the webhook server so that the admission controller can communicate with it. 
We have already provided the service manifest at:
```
/root/webhook-service.yaml
```
Create the service using this definition.

```
kubectl create -f /root/webhook-service.yaml
```

---

We have added the MutatingkebhookConfiguration under /root/webhook-
configuration.yaml. Upon applying this configuration, which resources and
actions will it impact?
Deployment with DELETE operations
**Pod with CREATE operations**
Pod with DELETE operations
Deployment with CREATE operations

---

Now lets deploy `MutatingWebhookConfiguration` in `/root/webhook-configuration.yaml`
```
kubectl create -f /root/webhook-configuration.yamls
```


---

In the previous steps, you have set up and deployed a demo webhook with the following behaviors:

- **Denies** all requests for pods to run as root in a container **if no `securityContext` is provided.**
- **Defaults**: If `runAsNonRoot` is not set, the webhook **automatically adds `runAsNonRoot: true`** and sets the user ID to `1234`.
- **Explicit root access**: The webhook **allows containers to run as root only if you explicitly set `runAsNonRoot: false`** in the pod's `securityContext`.

In the next steps, you will find pod definition files for each scenario. Please deploy these pods using the provided definition files and validate the behavior of our webhook.


---
Deploy a pod that does not explicitly define a `securityContext`.
This will help verify that the webhook applies **default values**.
We have already provided the manifest:
```
/root/pod-with-defaults.yaml
```


Solution:
```
kubectl apply -f /root/pod-with-defaults.yaml
```

---

Check the securitycontext of the pod created in the previous step (pod-
with-defaults).
Even though we did not specify any values in the pod definition, the mutation
webhook should have injected default values.
runAsNonRoot: true, runAsUser: 0
**runAsNonRoot: true, runAsUser: 1234**
runAsNonRoot: false, runAsUser: 0
runAsNonRoot: false, runAsUser: 1234


```
kubectl get pod pod-with-defaults -o yaml | grep -A2 "securityContext:"
```

---

Deploy pod with a securityContext explicitly allowing it to run as root 
We have added pod definition file under
```
/root/pod-with-override.yaml
```
Validate securityContext after you deploy this pod

Run command:

```
kubectl apply -f /root/pod-with-override.yaml
```

then validate `securityContext` using the following command:

```
kubectl get po pod-with-override -o yaml | grep -A2 " securityContext:"
```


---
Deploy a pod that specifies a conflicting `securityContext`.
- The pod requests to run with `runAsUser: 0` (root).
- But it does not explicitly set `runAsNonRoot: false`.
According to our webhook rules, this request should be **denied**.
We have already provided the manifest at:
```
/root/pod-with-conflict.yaml
```

```
kubectl apply -f /root/pod-with-conflict.yaml
```