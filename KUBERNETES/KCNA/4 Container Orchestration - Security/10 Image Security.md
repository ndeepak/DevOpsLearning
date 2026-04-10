# Image Security
# Kubernetes Image Security (KCNA + CKA)

## 1. What Is a Container Image?
A **container image** is a packaged filesystem that includes:
- Application code    
- Runtime (for example, Node.js, Python, Java)    
- System libraries    
- Configuration defaults    
Kubernetes **does not build images**.  
It only **pulls and runs** images from a container registry.

---
## 2. Image Naming Convention (Very Important for Exams)
When you write:
`image: nginx`
Kubernetes interprets this as:
`docker.io/library/nginx:latest`
### Image name format
`<registry>/<account>/<image>:<tag>`

Examples:

|Short Name|Fully Qualified Image Name|
|---|---|
|nginx|docker.io/library/nginx:latest|
|redis|docker.io/library/redis:latest|
|myuser/app|docker.io/myuser/app:latest|
|gcr.io/myproj/app|gcr.io/myproj/app:latest|
|private-reg.io/team/app:v1|private-reg.io/team/app:v1|
### Defaults Kubernetes assumes

|Field|Default|
|---|---|
|Registry|docker.io|
|Account|library|
|Tag|latest|

Exam tip:
- **Always prefer explicit image names and tags**    
- Avoid `latest` in production    
---
## 3. What Is the “library” Namespace?
- `library` is a **special Docker Hub namespace**    
- It contains **official images**    
- Maintained by Docker and upstream project maintainers    

Examples:
- library/nginx    
- library/mysql    
- library/postgres    

Why this matters for security:
- Official images are regularly scanned    
- Better patching and maintenance    
- Reduced risk of malicious content    

---
## 4. Where Images Are Stored (Registries)
A **container registry** stores and distributes images.
### Common registries

|Registry|Purpose|
|---|---|
|Docker Hub (docker.io)|Default public registry|
|GCR (gcr.io)|Google Container Registry|
|ECR|AWS Elastic Container Registry|
|ACR|Azure Container Registry|
|Harbor|On-prem private registry|

---
## 5. Public vs Private Registries
### Public registry
- Anyone can pull images    
- No authentication required    
- Example: nginx from Docker Hub    
### Private registry
- Requires authentication    
- Used for:    
    - Internal apps        
    - Proprietary software        
    - Sensitive workloads        
Security rule:
> Production images should almost always live in **private registries**

---
## 6. Image Pull Process in Kubernetes
When a pod is created:
1. Kubelet checks if the image exists locally    
2. If not, it contacts the registry    
3. Registry authentication happens    
4. Image is pulled    
5. Container starts    

If authentication fails:
`ImagePullBackOff ErrImagePull`

---
## 7. Pulling Private Images with Docker (Local)
Before Kubernetes, Docker must authenticate:
`docker login private-registry.io`
This creates:
`~/.docker/config.json`
This file stores credentials (base64 encoded, not encrypted).
Kubernetes does **not** use this file directly.

---
## 8. How Kubernetes Accesses Private Registries
Kubernetes uses **Secrets** of type:
`kubernetes.io/dockerconfigjson`
These secrets store registry credentials.

---
## 9. Creating an Image Pull Secret
Command:
```bash
kubectl create secret docker-registry regcred \
  --docker-server=private-registry.io \
  --docker-username=registry-user \
  --docker-password=registry-password \
  --docker-email=registry-user@org.com
```
This creates:
- A secret named `regcred`    
- Encodes credentials in Docker config format    
Verify:
`kubectl get secrets `
`kubectl describe secret regcred`

---
## 10. Using imagePullSecrets in a Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx
    image: private-registry.io/apps/internal-app
  imagePullSecrets:
  - name: regcred
```
Important rules:
- Secret must exist in the **same namespace**    
- Name must match exactly    
- Applies only to image pulling (not API access)
---
## 11. imagePullSecrets vs Service Accounts
You can attach image pull secrets to:
- A Pod    
- A ServiceAccount    
### ServiceAccount approach (recommended)
```bash
kubectl patch serviceaccount default \
  -p '{"imagePullSecrets":[{"name":"regcred"}]}'
```
Now:
- All pods using this service account can pull private images    
- No need to repeat `imagePullSecrets` in every pod
---
## 12. ImagePullPolicy (Often Tested)
Image pull behavior is controlled by:
`imagePullPolicy: Always | IfNotPresent | Never`

Defaults:
- `latest` → Always    
- Tagged image → IfNotPresent    
Best practice:
```yaml
image: myapp:v1.2.3
imagePullPolicy: IfNotPresent
```

---
## 13. Image Security Best Practices
### Use minimal base images
- Distroless    
- Alpine    
- Scratch    
### Pin image versions
Avoid:
`image: nginx:latest`
Prefer:
`image: nginx:1.25.3`
### Scan images
- Trivy    
- Clair    
- Anchore    
### Restrict registries
- Admission controllers    
- Pod Security / OPA    
### Run as non-root
(Not image-specific, but related)

---
## 14. Common Errors and Fixes

|Error|Cause|Fix|
|---|---|---|
|ErrImagePull|Wrong credentials|Fix secret|
|ImagePullBackOff|Registry unreachable|Check DNS/network|
|unauthorized|Secret missing|Add imagePullSecrets|
|manifest unknown|Wrong image name/tag|Correct image|

---
## 15. KCNA / CKA Exam Pointers
- Kubernetes does **not** build images    
- Kubernetes pulls images at **node level**    
- imagePullSecrets ≠ service account token    
- Private registry access requires a secret    
- Default registry is docker.io    
- Default namespace for official images is library    

---
## Final Summary
- Images come from registries    
- `nginx` means `docker.io/library/nginx:latest`    
- Private registries require authentication    
- Kubernetes uses secrets to store registry credentials    
- imagePullSecrets enable private image access    
- Service accounts can carry image pull secrets    
- Image security is a critical supply-chain concern

---
