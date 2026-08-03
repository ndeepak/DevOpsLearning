# 14 Lab - Admission Controllers
The `ImagePolicyWebhook` admission controller intercepts pod creation requests and consults an external webhook service to determine whether the container images specified in the pod spec should be allowed or denied.

In this lab, you will configure an `ImagePolicyWebhook` admission controller to work with a container image scanner.

A functional container image scanner is already deployed with the HTTPS endpoint:  
`https://image-checker-webhook.default.svc:1323/image_policy`

An incomplete configuration exists at `/etc/kubernetes/imgvalidation`.


---

What is the primary purpose of the `ImagePolicyWebhook` admission controller?
* Automatically scan images for vulnerabilities after pods are deployed
* Encrypt container images at rest in the container registry
* **Validate container images against an external webhook before allowing pod creation**
* Authenticate users trying to pull container images

The `ImagePolicyWebhook` admission controller is a **validating** admission controller. It sends image information from pod specs to an external backend (webhook) for validation before the pod is persisted. It can approve or deny pod creation based on the images used.

The `ImagePolicyWebhook` admission controller intercepts pod creation and update requests, extracts the container images, and sends them to an external webhook for validation. Based on the webhook's response, it either allows or denies the pod creation.
It does **not** perform authentication, post-deployment scanning, or image encryption.

---

Examine the incomplete configuration at `/etc/kubernetes/imgvalidation`.
This directory contains the following files:
- `admission-configuration.yaml` — The `AdmissionConfiguration` resource that references the ImagePolicyWebhook config
- `imagepolicy-conf.yaml` — The ImagePolicyWebhook plugin configuration (**incomplete**)
- `kubeconf.yaml` — The kubeconfig file used by the API server to connect to the webhook (**incomplete**)
- `webhook.crt` — The TLS certificate for the webhook server

Run the following commands to examine the files:

```bash
ls -la /etc/kubernetes/imgvalidation/
cat /etc/kubernetes/imgvalidation/admission-configuration.yaml
cat /etc/kubernetes/imgvalidation/imagepolicy-conf.yaml
cat /etc/kubernetes/imgvalidation/kubeconf.yaml
```

Notice that:

1. `imagepolicy-conf.yaml` has `defaultAllow: true` — this means images are **allowed** when the webhook backend is unavailable (fail-open).
2. `kubeconf.yaml` has a placeholder server endpoint (`https://placeholder.example.com`) instead of the real webhook URL.

---


In the `ImagePolicyWebhook` configuration, the `defaultAllow` field is currently set to `true`. What does this mean when the webhook backend is unavailable?
- **All pod creation requests are allowed (fail-open)**
- All pod creation requests are denied (fail-closed)
- Only pods in the default namespace are allowed
- The API server retries indefinitely until the backend responds

Hint:
The `defaultAllow` field in the ImagePolicyWebhook configuration determines the behavior when the webhook backend cannot be reached.
- When set to `true`, it operates in **fail-open** mode.
- When set to `false`, it operates in **fail-closed** mode.

When `defaultAllow` is set to `true`, the ImagePolicyWebhook operates in **fail-open** mode. This means:
- If the webhook backend is unreachable or returns an error, pod creation requests are **allowed** by default.
- This is less secure because images bypass validation when the backend is down.
To enforce **fail-closed** behavior (deny pods when the backend is unavailable), set `defaultAllow: false`.

---

Reconfigure the `ImagePolicyWebhook` to **reject** images when the webhook backend is unavailable (fail-closed).
```bash
controlplane /etc/kubernetes/imgvalidation ➜  cat  imagepolicy-conf.yaml 
imagePolicy:
  kubeConfigFile: /etc/kubernetes/imgvalidation/kubeconf.yaml
  allowTTL: 50
  denyTTL: 50
  retryBackoff: 500
  defaultAllow: false
```
Edit the file `/etc/kubernetes/imgvalidation/imagepolicy-conf.yaml` and set `defaultAllow` to `false`.

```bash
vi /etc/kubernetes/imgvalidation/imagepolicy-conf.yaml
```

```yaml
imagePolicy:
  kubeConfigFile: /etc/kubernetes/imgvalidation/kubeconf.yaml
  allowTTL: 50
  denyTTL: 50
  retryBackoff: 500
  defaultAllow: false
```

**Note:** Setting `defaultAllow: false` enforces a fail-closed policy — if the webhook backend is unavailable, all image pull requests will be denied. This is the recommended security posture for production environments.

---

The kubeconfig file at `/etc/kubernetes/imgvalidation/kubeconf.yaml` is missing the correct webhook server endpoint.
Update the `server` field under `clusters[0].cluster` to point to the image scanner webhook:
`https://image-checker-webhook.default.svc:1323/image_policy`
**Note:** The kubeconfig file is used by the API server to communicate with the external image policy webhook. The `server` field must contain the full URL of the webhook endpoint.
Webhook server endpoint configured in kubeconf.yaml?

Edit `/etc/kubernetes/imgvalidation/kubeconf.yaml`:
```bash
vi /etc/kubernetes/imgvalidation/kubeconf.yaml
```

Update the `server` field to the correct webhook endpoint:
```yaml
apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority: /etc/kubernetes/imgvalidation/webhook.crt
    server: https://image-checker-webhook.default.svc:1323/image_policy
  name: checker_webhook
contexts:
- context:
    cluster: checker_webhook
    user: api-server
  name: checker_validator
current-context: checker_validator
preferences: {}
users:
- name: api-server
  user:
    client-certificate: /etc/kubernetes/pki/front-proxy-client.crt
    client-key: /etc/kubernetes/pki/front-proxy-client.key
```


---
Reconfigure the API server to enable the ImagePolicywebhook admission
plugin and ensure it can access the configuration files.
• ImagePolicyWebhook admission plugin enabled on kube-apiserver?
• admission-control-config-file flag set on kube-apiserver?
• imgvalidation volume mounted in kube-apiserver?

Edit `/etc/kubernetes/manifests/kube-apiserver.yaml`:
```bash
cp /etc/kubernetes/manifests/kube-apiserver.yaml /opt/kube-apiserver.yaml.bak
vi /etc/kubernetes/manifests/kube-apiserver.yaml
```

**1. Enable the admission plugin:**
```yaml
    - --enable-admission-plugins=NodeRestriction,ImagePolicyWebhook
```
**2. Add the admission control config file:**
```yaml
    - --admission-control-config-file=/etc/kubernetes/imgvalidation/admission-configuration.yaml
```
**3. Mount the imgvalidation directory:**
Add to `volumes`:
```yaml
    - name: imgvalidation
      hostPath:
        path: /etc/kubernetes/imgvalidation
        type: Directory
```
Add to `volumeMounts`:
```yaml
    - name: imgvalidation
      mountPath: /etc/kubernetes/imgvalidation
      readOnly: true
```

**4. Verify the API server is running:**
```bash
kubectl get pods -n kube-system
```

```bash
controlplane /etc/kubernetes/imgvalidation ➜  cat /etc/kubernetes/manifests/kube-apiserver.yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    kubeadm.kubernetes.io/kube-apiserver.advertise-address.endpoint: 10.244.96.38:6443
  labels:
    component: kube-apiserver
    tier: control-plane
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
    - --advertise-address=10.244.96.38
    - --allow-privileged=true
    - --authorization-mode=Node,RBAC
    - --client-ca-file=/etc/kubernetes/pki/ca.crt
    - --enable-admission-plugins=NodeRestriction,ImagePolicyWebhook
    - --admission-control-config-file=/etc/kubernetes/imgvalidation/admission-configuration.yaml
    - --enable-bootstrap-token-auth=true
    - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
    - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
    - --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
    - --etcd-servers=https://127.0.0.1:2379
    - --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt
    - --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key
    - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
    - --proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.crt
    - --proxy-client-key-file=/etc/kubernetes/pki/front-proxy-client.key
    - --requestheader-allowed-names=front-proxy-client
    - --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
    - --requestheader-extra-headers-prefix=X-Remote-Extra-
    - --requestheader-group-headers=X-Remote-Group
    - --requestheader-username-headers=X-Remote-User
    - --secure-port=6443
    - --service-account-issuer=https://kubernetes.default.svc.cluster.local
    - --service-account-key-file=/etc/kubernetes/pki/sa.pub
    - --service-account-signing-key-file=/etc/kubernetes/pki/sa.key
    - --service-cluster-ip-range=172.20.0.0/16
    - --tls-cert-file=/etc/kubernetes/pki/apiserver.crt
    - --tls-private-key-file=/etc/kubernetes/pki/apiserver.key
    image: registry.k8s.io/kube-apiserver:v1.35.0
    imagePullPolicy: IfNotPresent
    livenessProbe:
      failureThreshold: 8
      httpGet:
        host: 10.244.96.38
        path: /livez
        port: probe-port
        scheme: HTTPS
      initialDelaySeconds: 10
      periodSeconds: 10
      timeoutSeconds: 15
    name: kube-apiserver
    ports:
    - containerPort: 6443
      name: probe-port
      protocol: TCP
    readinessProbe:
      failureThreshold: 3
      httpGet:
        host: 10.244.96.38
        path: /readyz
        port: probe-port
        scheme: HTTPS
      periodSeconds: 1
      timeoutSeconds: 15
    resources:
      requests:
        cpu: 250m
    startupProbe:
      failureThreshold: 24
      httpGet:
        host: 10.244.96.38
        path: /livez
        port: probe-port
        scheme: HTTPS
      initialDelaySeconds: 10
      periodSeconds: 10
      timeoutSeconds: 15
    volumeMounts:
    - mountPath: /etc/ssl/certs
      name: ca-certs
      readOnly: true
    - mountPath: /etc/ca-certificates
      name: etc-ca-certificates
      readOnly: true
    - mountPath: /etc/kubernetes/pki
      name: k8s-certs
      readOnly: true
    - mountPath: /usr/local/share/ca-certificates
      name: usr-local-share-ca-certificates
      readOnly: true
    - mountPath: /usr/share/ca-certificates
      name: usr-share-ca-certificates
      readOnly: true
    - name: imgvalidation
      mountPath: /etc/kubernetes/imgvalidation
      readOnly: true
  hostNetwork: true
  priority: 2000001000
  priorityClassName: system-node-critical
  securityContext:
    seccompProfile:
      type: RuntimeDefault
  volumes:
  - hostPath:
      path: /etc/ssl/certs
      type: DirectoryOrCreate
    name: ca-certs
  - hostPath:
      path: /etc/ca-certificates
      type: DirectoryOrCreate
    name: etc-ca-certificates
  - hostPath:
      path: /etc/kubernetes/pki
      type: DirectoryOrCreate
    name: k8s-certs
  - hostPath:
      path: /usr/local/share/ca-certificates
      type: DirectoryOrCreate
    name: usr-local-share-ca-certificates
  - hostPath:
      path: /usr/share/ca-certificates
      type: DirectoryOrCreate
    name: usr-share-ca-certificates
  - hostPath:
      path: /etc/kubernetes/imgvalidation
      type: Directory
    name: imgvalidation

status: {}
```