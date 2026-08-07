# Kubernetes Secrets 
Secrets are one of the most important topics for both **CKA** and especially **CKS**.

Many tutorials simply say:
> "Secrets store sensitive information."

That is correct, but it is incomplete.

The real questions are:
- Why do Secrets exist?
- How are they different from ConfigMaps?
- Are Secrets actually secure?
- How do they work internally?
- What happens when a Pod uses a Secret?
- What are the security limitations?

Let's study everything from the ground up.
# Why Do We Need Secrets?
Let's start with a simple application.
```
import mysql.connector

mysql.connector.connect(
    host="mysql",
    user="root",
    password="mypassword"
)
```

Everything is hardcoded.

Problems:
- Password is inside source code.
- Every developer can see it.
- Password changes require rebuilding the application.
- Password may accidentally be committed to GitHub.

This violates one of the most important security principles:

> **Never hardcode secrets into your application.**

Instead, developers write
```
import os

mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
```

Now the application expects Kubernetes to provide the values.

Question:
Where should Kubernetes store them?

---

# Can We Use ConfigMaps?
Technically yes.

```
apiVersion: v1
kind: ConfigMap
data:
  DB_HOST: mysql
  DB_USER: root
  DB_PASSWORD: mypassword
```

Will the application work?
Yes.

Should we do it?
No.

Why?
Because ConfigMaps are intended for **non-sensitive configuration**.

Anyone with permission to read ConfigMaps can immediately see
```
DB_PASSWORD=mypassword
```

This is a security risk.

Therefore Kubernetes provides another object.
```
ConfigMap
↓
Application Configuration
↓
Non-sensitive


Secret
↓
Passwords
Tokens
Keys
Certificates
```
# What is a Secret?
A Secret is simply another Kubernetes object.
Just like
- Pod
- Deployment
- Service
- ConfigMap

there is also
```
Secret
```
The difference is only the purpose.

ConfigMap
```
APP_COLOR=blue
LOG_LEVEL=INFO
```

Secret
```
DB_PASSWORD=mypassword
JWT_TOKEN=xxxxxxxx
TLS_KEY=...
```

# Internal Architecture
```scss
	 Secret
     DB_PASSWORD
           │
           ▼
      API Server
           │
           ▼
          etcd
           │
           ▼
        kubelet
           │
           ▼
     Container Runtime
           │
           ▼
      Environment Variable
or
Mounted File
```

Notice
A Secret is simply stored inside Kubernetes and later delivered to Pods.
# Is Secret Actually Encrypted?
This is one of the most misunderstood topics.
Most beginners think
> Secret = Encryption

Wrong.
By default
Secrets are only
```
Base64 Encoded
```

NOT
```
Encrypted
```
These are completely different.

# What is Base64?
Suppose
```
mysql
```

Encode
```
echo -n "mysql" | base64
```

Output
```
bXlzcWw=
```
Looks secure?
Not at all.
Anyone can decode it.
```
echo -n "bXlzcWw=" | base64 --decode
```
Output
```
mysql
```
Base64 is simply an encoding mechanism.
It is not cryptography.

# Encoding vs Encryption
Encoding
```
Password
↓
Base64
↓
cGFzc3dvcmQ=
```
Anyone can reverse it.

Encryption
```
Password
↓
AES Encryption
↓
Random Ciphertext
↓
Requires Encryption Key
```
Huge difference.

This distinction is very important in the CKS exam.
# Creating Secrets
There are two methods.
```
Secret
├── Imperative
└── Declarative
```
Exactly like ConfigMaps.
# Imperative Method
General syntax
```
kubectl create secret generic <secret-name> \
--from-literal=<key>=<value>
```

Example
```
kubectl create secret generic app-secret \
--from-literal=DB_HOST=mysql \
--from-literal=DB_USER=root \
--from-literal=DB_PASSWORD=paswrd
```

Verify
```
kubectl get secrets
```

Output
```
NAME          TYPE      DATA
app-secret    Opaque       3
```

Describe
```
kubectl describe secret app-secret
```

Output
```
Name: app-secret
Type: Opaque
Data
====
DB_HOST
DB_USER
DB_PASSWORD
```

Notice
The values are hidden.
Unlike ConfigMaps.

# Create from File
Suppose
```
app_secret.properties
```

contains
```
DB_HOST=mysql
DB_USER=root
DB_PASSWORD=paswrd
```

Create
```
kubectl create secret generic app-secret \
--from-file=app_secret.properties
```

# Declarative Method
Unlike ConfigMaps
Secret values must be Base64 encoded.
Example
```
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
data:
  DB_HOST: bXlzcWw=
  DB_USER: cm9vdA==
  DB_PASSWORD: cGFzd3Jk
```

Apply
```
kubectl apply -f secret.yaml
```

# Why Are Values Encoded?
Because Kubernetes API expects the `data` field to contain Base64-encoded strings.
This is a transport and storage format, **not a security feature**.
If you don't want to manually encode values, Kubernetes also supports a field named `stringData`.

Example
```
apiVersion: v1
kind: Secret

metadata:
  name: app-secret

stringData:
  DB_HOST: mysql
  DB_USER: root
  DB_PASSWORD: paswrd
```

When you run
```
kubectl apply -f secret.yaml
```

Kubernetes automatically converts `stringData` into Base64 and stores it in `data`.
**Exam Tip:** `stringData` is easier for humans to write. `data` is what Kubernetes stores internally.

# Encoding Values
Linux
```
echo -n "mysql" | base64
```

Output
```
bXlzcWw=
```

Another
```
echo -n "root" | base64
```

Output
```
cm9vdA==
```

Password
```
echo -n "paswrd" | base64
```

Output
```
cGFzd3Jk
```
# Viewing Secrets
List
```
kubectl get secrets
```

YAML
```
kubectl get secret app-secret -o yaml
```

Output
```
data:
  DB_HOST: bXlzcWw=
  DB_USER: cm9vdA==
  DB_PASSWORD: cGFzd3Jk
```
Notice
Still encoded.

Decode
```
echo -n "cGFzd3Jk" | base64 --decode
```

Output
```
paswrd
```

# Using Secrets Inside Pods
Exactly like ConfigMaps,
Secrets can be consumed in three ways.
```
Secret
↓
Single Environment Variable
↓
Entire Secret
↓
Volume
```
# Method 1
## Single Key
```
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: app-secret
      key: DB_PASSWORD
```

Application
```
os.getenv("DB_PASSWORD")
```

Output
```
paswrd
```

# Method 2
## Entire Secret
```
envFrom:
- secretRef:
    name: app-secret
```

Suppose
```
DB_HOST=mysql
DB_USER=root
DB_PASSWORD=paswrd
```

Application receives
```
DB_HOST=mysql
DB_USER=root
DB_PASSWORD=paswrd
```
automatically.
# Method 3
## Mount as Volume
```
volumes:
- name: secret-volume
  secret:
    secretName: app-secret
```
Mount
```
volumeMounts:
- name: secret-volume
  mountPath: /opt/secrets
```

Inside container
```
/opt/secrets/
DB_HOST
DB_USER
DB_PASSWORD
```

Each key becomes one file.

Example
```
cat /opt/secrets/DB_PASSWORD
```

Output
```
paswrd
```
# Environment Variables vs Volume
Environment Variable
```
DB_PASSWORD
↓
Application
↓
os.getenv()
```

Volume
```
DB_PASSWORD File
↓
Application Reads File
```
Some applications prefer files.
Examples
- TLS certificates
- SSH keys
- Private keys
- NGINX certificates
# Updating Secrets
Suppose
```
DB_PASSWORD=oldpass
```

Later
```
DB_PASSWORD=newpass
```

Question
Does the running Pod automatically see the new password?
It depends.
## Secret as Environment Variable
```
env:
envFrom:
```
No.
The application receives the value only once when the process starts.
Restart Pod.
## Secret as Volume
Mounted files are updated automatically by the kubelet (typically within about a minute).
Example
```
Old Secret
↓
Mounted File
↓
New Secret
↓
Mounted File Updated
```
However,
your application may still need to reload the file.
# ConfigMap vs Secret

|Feature|ConfigMap|Secret|
|---|---|---|
|Purpose|Non-sensitive configuration|Sensitive information|
|Stored in etcd|Yes|Yes|
|Encoded|No|Yes (Base64)|
|Encrypted by default|No|No|
|Environment Variables|Yes|Yes|
|Mounted as Volume|Yes|Yes|
|Typical Use|Colors, ports, URLs|Passwords, API keys, certificates|
# Are Kubernetes Secrets Secure?
This is where CKS goes deeper.
By default,
Secrets have several limitations.
## 1. Base64 is not encryption
Anyone with read access can decode them.
## 2. Stored in etcd
Unless you enable **Encryption at Rest**, etcd stores Secret data without true encryption.
Production clusters should enable encryption at rest.
## 3. RBAC
Only authorized users should be able to execute
```
kubectl get secrets
```
RBAC should restrict access.
Example:
- Application service account: can read only its own Secret.
- Cluster administrator: can read all Secrets.
- Regular developer: no access unless required.
## 4. Avoid Git
Never commit
```
data:
  DB_PASSWORD: cGFzc3dvcmQ=
```
or
```
stringData:
  DB_PASSWORD: mypassword
```
to a public Git repository.
Use external secret management or encrypted secret workflows instead.

---
# External Secret Managers
Many production clusters do not store long-lived secrets directly in Kubernetes.
Instead, Kubernetes retrieves them from dedicated secret management systems.
Common solutions include:
- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault
- Google Cloud Secret Manager

These provide:
- Strong encryption
- Automatic rotation
- Audit logging
- Fine-grained access control

# Complete Flow
```
Developer
      │
      ▼
Create Secret
      │
      ▼
API Server
      │
      ▼
etcd
      │
      ▼
kubelet
      │
      ▼
Container Runtime
      │
      ▼
Pod
      │
      ▼
Application
```

# Common CKA/CKS Troubleshooting Questions
### "My application cannot find DB_PASSWORD."
Check:
```
kubectl describe pod <pod-name>
```

Verify:
- Secret exists.
- Secret name is correct.
- Key name matches exactly.
- Pod references the correct Secret.

### "kubectl describe secret does not show the password."
This is expected.
Use:
```
kubectl get secret app-secret -o yaml
```

or
```
kubectl get secret app-secret -o jsonpath='{.data.DB_PASSWORD}' | base64 --decode
```

### "I updated the Secret but the application still uses the old password."

Likely causes:
- Secret is injected as environment variables. Restart the Pod or roll out the Deployment.
- If mounted as a volume, verify the application reloads the updated file instead of reading it only at startup.

---

# CKA Exam Tips
1. Know both creation methods:
    - Imperative: `kubectl create secret generic`
    - Declarative: YAML
2. Prefer `stringData` when writing Secret manifests manually. Kubernetes converts it to Base64 in the stored `data` field.
3. Learn the three consumption methods:
    - `secretKeyRef`
    - `secretRef` (`envFrom`)
    - Mounted volume
4. Remember that **Base64 encoding is not encryption**. This is one of the most frequently tested security concepts.
5. Know the security best practices:
    - Enable **Encryption at Rest** for etcd.
    - Restrict Secret access using RBAC.
    - Avoid committing Secret manifests containing sensitive values to source control.
    - Consider external secret managers for production workloads.

A useful mental model is:
```
Application
      ▲
      │
Environment Variables or Mounted Files
      ▲
      │
Secret
      ▲
      │
API Server → etcd
```

The Secret is simply Kubernetes' mechanism for delivering sensitive configuration to containers. Its security depends not just on using the `Secret` object, but also on proper RBAC, encryption at rest, secure storage practices, and, in many production environments, integration with an external secret management system.