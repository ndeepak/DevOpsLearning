# Demo: Encrypting Secret Data at Rest

# Kubernetes Encryption at Rest — Comprehensive Notes

This topic is particularly important for **CKS**, and it is also useful for CKA troubleshooting questions.
The single most important thing to understand is:
> **A Kubernetes Secret is not encrypted merely because it is a Secret. By default, Secret data is Base64-encoded, and the data stored in etcd is not protected by encryption at rest.**

The goal of encryption at rest is to ensure that if someone gains access to the underlying etcd storage, the Secret values cannot simply be read.

---

# 1. The Problem
Consider:
```
kubectl create secret generic my-secret \
  --from-literal=DB_PASSWORD=supersecret
```

Kubernetes creates:
```
Secret
    |
    | DB_PASSWORD=supersecret
    v
API Server
    |
    v
etcd
```

By default, the Secret is stored in etcd without encryption at rest.

If you retrieve it through the API:
```
kubectl get secret my-secret -o yaml
```

you might see:
```
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  DB_PASSWORD: c3VwZXJzZWNyZXQ=
```
The value appears encoded.

Decode it:
```
echo -n 'c3VwZXJzZWNyZXQ=' | base64 --decode
```

Output:
```
supersecret
```

Therefore:
```
Base64 != Encryption
```

---

# 2. Encoding vs Encryption
This distinction is critical for CKS.
## Base64 Encoding
```
supersecret
      |
      v
Base64
      |
      v
c3VwZXJzZWNyZXQ=
```

Anyone can reverse it:
```
echo -n 'c3VwZXJzZWNyZXQ=' | base64 --decode
```
Therefore Base64 provides:
- No confidentiality
- No password protection
- No cryptographic security

It is simply an encoding format.

---

## Encryption
Encryption looks conceptually like:
```
supersecret
      |
      v
Encryption algorithm + key
      |
      v
Encrypted ciphertext
```

Without the encryption key, the original value should not be practically recoverable.
Therefore:
```
Encoding
    ≠
Encryption
```

---

# 3. Where Is Kubernetes Data Stored?
Kubernetes uses **etcd** as its persistent key-value database.
Simplified architecture:
```
kubectl
   |
   v
API Server
   |
   v
etcd
```

For example, a Secret might be stored under a key similar to:
```
/registry/secrets/default/my-secret
```

The important point is:
```
Kubernetes Secret
        |
        v
    API Server
        |
        v
       etcd
```
So protecting etcd is extremely important.

---

# 4. Why Does etcd Matter?
Suppose an attacker obtains access to the etcd database or its underlying storage.
If encryption at rest is **not enabled**, Secret data can potentially be recovered.

Conceptually:
```
Attacker
   |
   v
etcd
   |
   v
Secret data
   |
   v
Base64 decode
   |
   v
Actual password
```

Therefore, CKS security is not just:
```
"Use Kubernetes Secrets"
```

It is:
```scss
Use Secrets
      +
RBAC
      +
Encryption at Rest
      +
Secure etcd
      +
Secure control plane
```

---
# 5. How Kubernetes Encryption at Rest Works
Kubernetes API Server supports an **encryption provider configuration**.
The basic flow becomes:
```scss
kubectl
   |
   v
API Server
   |
   | Encrypt
   v
etcd
   |
   | Encrypted Secret
   v
Storage
```

When a user requests the Secret:
```scss
kubectl
   |
   v
API Server
   |
   | Decrypt
   v
etcd
   |
   v
API Server
   |
   v
kubectl
```

The encryption/decryption happens at the API server boundary.

---
# 6. Before Encryption
Without encryption:
```scss
               API Server
                    |
                    v
                  etcd
                    |
                    v
             Secret data
                    |
                    v
             Base64 encoded
```

---

# 7. After Encryption
With encryption at rest:
```
               API Server
                    |
                    |
                 Encrypt
                    |
                    v
                  etcd
                    |
                    v
             Encrypted data
```

When Kubernetes needs the Secret:
```
                  etcd
                    |
                    |
                 Decrypt
                    |
                    v
               API Server
                    |
                    v
               Kubernetes
```

---
# 8. Creating a Secret
There are several ways.
## From literal
```
kubectl create secret generic my-secret \
  --from-literal=key1=supersecret \
  --from-literal=key2=topsecret
```

---

## From a file
```
kubectl create secret generic my-secret \
  --from-file=secret.txt
```

---

## From specific files
```
kubectl create secret generic my-secret \
  --from-file=ssh-privatekey=id_rsa \
  --from-file=ssh-publickey=id_rsa.pub
```

---

## From environment file
Suppose:
```
foo.env
```

contains:
```
DB_HOST=mysql
DB_USER=root
DB_PASSWORD=supersecret
```

Create:
```
kubectl create secret generic my-secret \
  --from-env-file=foo.env
```

---

# 9. Verify the Secret
```
kubectl get secret my-secret
```

Example:
```scss
NAME         TYPE     DATA   AGE
my-secret    Opaque   2      20s
```

To inspect metadata:
```
kubectl describe secret my-secret
```

To see the encoded values:
```
kubectl get secret my-secret -o yaml
```

---

# 10. Inspecting etcd
In a kubeadm-style cluster, etcd certificates are commonly located under:
```
/etc/kubernetes/pki/etcd/
```

For example:
```
ls /etc/kubernetes/pki/etcd/
```

You may see:
```
ca.crt
server.crt
server.key
```
The exact paths can differ depending on the Kubernetes distribution and installation method.

---
# 11. Using etcdctl
First check:
```
etcdctl version
```

For etcd v3:
```
export ETCDCTL_API=3
```

Then a command may look like:
```
ETCDCTL_API=3 etcdctl \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  get /registry/secrets/default/my-secret
```

You can inspect the raw output:
```
ETCDCTL_API=3 etcdctl \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  get /registry/secrets/default/my-secret | hexdump -C
```
This is primarily a **CKS-level understanding/troubleshooting exercise**.

The important thing to remember is:
```scss
Without encryption at rest:
Secret
  |
  v
API Server
  |
  v
etcd
  |
  v
Data is not encrypted at rest
```

---

# 12. EncryptionConfiguration
Kubernetes allows us to configure an encryption provider.

Example:
```
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources:
  - secrets
  providers:
  - aescbc:
      keys:
      - name: key1
        secret: <BASE64-ENCODED-32-BYTE-KEY>
  - identity: {}
```
Let's understand every section.

---

# 13. `apiVersion`
```
apiVersion: apiserver.config.k8s.io/v1
```

This is **not** the normal Kubernetes object API version such as:
```
apiVersion: v1
```

It belongs to the API server configuration API.

---

# 14. `kind`
```
kind: EncryptionConfiguration
```
This tells the API server:
> This file contains encryption configuration.

---

# 15. `resources`
```
resources:
- resources:
  - secrets
```
This says:
> Apply this encryption configuration to Secret resources.

You can configure other resource types as well, but Secrets are the most important example.

---

# 16. Encryption Provider
Example:
```
providers:
- aescbc:
```

This tells Kubernetes to use the AES-CBC encryption provider.
The important CKS concept is not memorizing every encryption algorithm, but understanding:
```scss
EncryptionConfiguration
        |
        v
Encryption Provider
        |
        v
Encryption Key
        |
        v
Encrypted data in etcd
```

---

# 17. Encryption Key
Example:
```
keys:
- name: key1
  secret: <BASE64-KEY>
```

Generate a random 32-byte key:
```
head -c 32 /dev/urandom | base64
```

Example output:
```
some-long-base64-value...
```

Put that value into:
```
secret: some-long-base64-value...
```

Important:
The key itself must be protected.

If an attacker obtains both:
```
Encrypted Secret
+
Encryption Key
```

the encryption protection is compromised.

---

# 18. Why 32 Bytes?
AES supports:
```
AES-128
AES-192
AES-256
```

A 32-byte key corresponds to:
```
32 bytes × 8 = 256 bits
```

Therefore:
```
32-byte key
    =
256-bit key
```

---

# 19. What Does `identity: {}` Mean?
This is extremely important.
Example:
```
providers:
- aescbc:
    keys:
    - name: key1
      secret: <KEY>
- identity: {}
```

`identity` means:
> Store/read the data without encryption.

It acts as a fallback/read mechanism.
This matters during migration.
Conceptually:
```
Read:
Try AES-CBC
     |
     +-- encrypted object → decrypt
If not encrypted
     |
     v
identity
     |
     v
read plaintext object
```

This allows Kubernetes to continue reading Secrets that were created before encryption was enabled.

---

# 20. Why Is `identity` After `aescbc`?
Provider order matters.
```
providers:
- aescbc:
    ...
- identity: {}
```

The first provider is used for writing new data.

Therefore:
```
New Secret
    |
    v
aescbc
    |
    v
Encrypted
```

`identity` remains available for reading older unencrypted objects.

This is important during migration.

---

# 21. Configure kube-apiserver
In a kubeadm-style control-plane node, the API server manifest is usually:
```
/etc/kubernetes/manifests/kube-apiserver.yaml
```

Place the encryption configuration somewhere secure, for example:
```
mkdir -p /etc/kubernetes/enc
```

Then:
```
/etc/kubernetes/enc/enc.yaml
```

---

# 22. Add the Encryption Provider Flag
In the kube-apiserver manifest:
```
spec:
  containers:
  - command:
    - kube-apiserver
    - --encryption-provider-config=/etc/kubernetes/enc/enc.yaml
```
This tells kube-apiserver:
> Use this file to determine how resources should be encrypted.

---

# 23. Mount the Configuration
The API server runs inside a static Pod.
Therefore the API server container needs access to the configuration file.
Add:
```
volumeMounts:
- name: enc
  mountPath: /etc/kubernetes/enc
  readOnly: true
```

And:
```
volumes:
- name: enc
  hostPath:
    path: /etc/kubernetes/enc
    type: DirectoryOrCreate
```

Conceptually:
```
Control Plane Host

/etc/kubernetes/enc/enc.yaml
             |
             | hostPath
             v
kube-apiserver container

/etc/kubernetes/enc/enc.yaml
```

---

# 24. Why Does kube-apiserver Restart?
Because kube-apiserver is usually a **static Pod**.

Its manifest is:
```
/etc/kubernetes/manifests/kube-apiserver.yaml
```

The kubelet watches this directory.

When the manifest changes:
```
Modify manifest
      |
      v
kubelet detects change
      |
      v
kube-apiserver recreated
      |
      v
New configuration loaded
```

This is a very important Kubernetes concept for the CKA.

---

# 25. Verify the Configuration
You can check the running kube-apiserver command:
```
ps aux | grep kube-apiserver
```

Look for:
```
--encryption-provider-config=/etc/kubernetes/enc/enc.yaml
```

You can also inspect the static Pod:
```
kubectl -n kube-system get pods
```

and:
```
kubectl -n kube-system describe pod kube-apiserver-<node>
```

---

# 26. Important: Existing Secrets
This is probably the most important operational detail.

Suppose before encryption:
```
Secret A
Secret B
Secret C
```
were created.

Then you enable encryption.

Are they automatically encrypted?
**No.**

The existing data is not automatically rewritten just because the encryption configuration has changed.
Think:
```
Before encryption:
Secret A → plaintext at rest
Secret B → plaintext at rest
Secret C → plaintext at rest

Enable encryption
↓
Secret D → encrypted
A/B/C → still need migration
```

---

# 27. Why Does This Happen?
Encryption configuration controls how Kubernetes **writes** resources.
Changing the configuration doesn't necessarily rewrite every existing object in etcd.
Therefore existing objects must be rewritten.

---

# 28. Re-encrypt Existing Secrets
A commonly used migration approach is:
```
kubectl get secrets --all-namespaces -o json \
  | kubectl replace -f -
```

Conceptually:
```
Existing Secrets
       |
       v
Read through API
       |
       v
API Server decrypts/reads
       |
       v
kubectl replace
       |
       v
API Server encrypts
       |
       v
etcd
       |
       v
Encrypted
```

Afterward, the existing Secrets have been rewritten using the active encryption provider.

---

# 29. Important Operational Warning
The command:
```
kubectl get secrets --all-namespaces -o json \
  | kubectl replace -f -
```

should be treated as a **migration operation**, not a casual command.

Before doing this on production:
- Take an etcd backup.
- Verify API server health.
- Verify the encryption configuration.
- Protect the encryption key.
- Test in a non-production cluster first.
- Understand your Kubernetes version and encryption configuration.
- Ensure you can recover the cluster if something goes wrong.

---

# 30. Key Rotation
CKS can go deeper than simply enabling encryption.
Suppose you currently have:
```
keys:
- name: key1
  secret: OLD_KEY
```
Eventually you want to rotate the key.

You can configure a new key as the first encryption key:
```
keys:
- name: key2
  secret: NEW_KEY
- name: key1
  secret: OLD_KEY
```

Why?
Because:
```
key2
```
is first and becomes the active write key.

Old data may still require:
```
key1
```
for decryption.

Then rewrite the existing Secrets.

Conceptually:
```
Old:

key1
 |
 v
Existing encrypted Secrets


Rotate:

key2 = write key
key1 = old read key


Rewrite Secrets

        ↓

Secrets become encrypted with key2
```

After everything has been migrated and verified, the old key can eventually be removed according to a carefully planned key-rotation procedure.

---

# 31. Complete Encryption Lifecycle
Think about the entire process this way:
```scss
               SECRET CREATED
                     |
                     v
               API SERVER
                     |
                     v
            Encryption Provider
                     |
                     v
                  AES-CBC
                     |
                     v
                    etcd
                     |
                     v
             Encrypted at Rest
```

When requested:
```scss
                  etcd
                    |
                    v
             Encrypted Secret
                    |
                    v
               API Server
                    |
                    v
                 Decrypt
                    |
                    v
                  Client
```

---

# 32. Before vs After
## Without Encryption at Rest
```scss
Secret
DB_PASSWORD=supersecret

        |
        v
Base64
        |
        v
etcd
        |
        v
Base64-encoded data
```
Base64 can easily be reversed.

---

## With Encryption at Rest
```scss
Secret
DB_PASSWORD=supersecret
        |
        v
API Server
        |
        v
Encryption Provider
        |
        v
Encrypted ciphertext
        |
        v
etcd
```
Now someone who only obtains the etcd data cannot simply Base64-decode the Secret.

---

# 33. But Encryption at Rest Does NOT Solve Everything
This is a very important CKS concept.
Encryption at rest protects data **while stored**.
It does not magically protect Secrets everywhere.
For example:
```
kubectl get secret ... -o yaml
```
can expose encoded Secret data to an authorized user.

Also:
```
kubectl exec
```
into a container may expose environment variables or mounted Secret files if the user has sufficient access.

Therefore:
```
Encryption at Rest
       +
RBAC
       +
Network Security
       +
Node Security
       +
Secure etcd
       +
Secret Management
```
are all necessary.

---

# 34. Security Layers
A good CKS mental model is:
```scss
                    Kubernetes Security

                           |
        +------------------+------------------+
        |                  |                  |
       RBAC          Encryption at Rest    Node Security
        |                  |                  |
        v                  v                  v
 API access          etcd protection     filesystem
                                         container access
```
Encryption at rest protects the storage layer.

RBAC controls who can access the Secret through Kubernetes.

---

# 35. Important CKS Distinction
Consider:
```
kubectl get secret db-secret -o yaml
```

You see:
```
data:
  password: cGFzc3dvcmQ=
```

Someone says:
> "The Secret is secure because it is Base64 encoded."

Wrong.
Correct answer:
> Base64 is encoding, not encryption. Encryption at rest must be configured if we want Secret data to be encrypted when persisted in etcd.

---

# 36. Commands You Should Know
## Create Secret
```
kubectl create secret generic my-secret \
  --from-literal=key1=supersecret
```
## List Secrets
```
kubectl get secrets
```
All namespaces:
```
kubectl get secrets -A
```
## Inspect
```
kubectl describe secret my-secret
```
## Get YAML
```
kubectl get secret my-secret -o yaml
```
## Decode
```
kubectl get secret my-secret \
  -o jsonpath='{.data.key1}' | base64 --decode
```
## Generate encryption key
```
head -c 32 /dev/urandom | base64
```
## Check kube-apiserver configuration
```
ps aux | grep kube-apiserver
```
Look for:
```
--encryption-provider-config=
```
## Inspect etcd
```
ETCDCTL_API=3 etcdctl \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  get /registry/secrets/default/my-secret
```

---

# 37. CKA/CKS Exam Cheat Sheet
```
Kubernetes Secret
        |
        +-- Base64 by default
        |
        +-- NOT encrypted by default
        |
        v
      etcd
```

Enable encryption:
```
EncryptionConfiguration
        |
        v
kube-apiserver
        |
        | --encryption-provider-config
        v
Encryption Provider
        |
        v
etcd
```

Key concepts:
```
Base64
    =
Encoding

Encryption
    =
Cryptographic protection

etcd
    =
Kubernetes persistent datastore

EncryptionConfiguration
    =
Tells kube-apiserver how to encrypt resources

aescbc
    =
Encryption provider

identity
    =
No encryption / identity provider

32 random bytes
    =
256-bit AES key

Existing Secrets
    =
Need to be rewritten to migrate them

RBAC
    =
Controls who can access Secrets

Encryption at Rest
    =
Protects Secrets stored in etcd
```

---

# 38. The Most Important Exam Scenario
If you get a question like:
> "Configure Kubernetes to encrypt Secrets stored in etcd."

Your thought process should immediately be:
```
1. Generate encryption key

2. Create EncryptionConfiguration

3. Configure provider

4. Add secrets under resources

5. Put configuration on control-plane node

6. Mount configuration into kube-apiserver

7. Add:
   --encryption-provider-config=<path>

8. kube-apiserver restarts

9. Create/update a Secret

10. Verify etcd contains encrypted data

11. Rewrite existing Secrets
    to migrate them to encrypted storage
```

---

# 39. Final Mental Model
If you remember only one diagram for the CKS exam, remember this:
```scss
                         Kubernetes

                         Secret
                           |
                           v
                      API Server
                           |
                           v
                Encryption Provider
                           |
                    +------+------+
                    |             |
                 Encrypt       Decrypt
                    |             |
                    v             ^
                   etcd ----------+
                    |
                    v
              Encrypted at Rest
```

And remember the security distinction:
```
Secret
  ≠
Encryption

Secret + Base64
  ≠
Encryption

Secret + Encryption at Rest
  =
Encrypted storage
```

Finally:
```
Encryption at Rest
        |
        v
Protects Secret data in etcd

RBAC
        |
        v
Controls who can access Secrets

External Secret Manager
        |
        v
Can provide stronger centralized
secret management, rotation and auditing
```

For **CKS**, this topic connects directly to **etcd security, RBAC, service accounts, API server security, key rotation, and Kubernetes hardening**, so understanding the complete data path is much more valuable than memorizing just the `enc.yaml` syntax.

References:
https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/

