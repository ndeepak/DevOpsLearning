# Configuring Environment Variables in Applications

Environment Variables are one of the most common ways to configure applications running inside containers.

Almost every real-world application uses environment variables.

Examples:
- Database hostname
- Database username
- Database password
- API URL
- Redis host
- Logging level
- Timezone
- Feature flags
- Application mode (Development/Production)
- Port numbers

For the CKA exam, you need to know:
- How Docker passes environment variables
- How Kubernetes passes environment variables
- Different ways to define environment variables
- ConfigMaps and Secrets (next topics)
- How to verify environment variables inside Pods
- Troubleshooting environment variable issues

---

# Why Do We Need Environment Variables?
Imagine you wrote a Python application.
```
from flask import Flask
import os

app = Flask(__name__)

color = os.getenv("APP_COLOR", "blue")

@app.route("/")
def home():
    return f"Application Color: {color}"
```

Notice
```
os.getenv("APP_COLOR")
```

The application does **not** know the color.

Instead, it asks Linux:

> "What is the value of APP_COLOR?"

Linux replies
```
pink
```

or
```
blue
```

depending on what was configured.

This allows us to configure the application **without changing the source code**.

---

# Hardcoded Values (Bad Practice)
Imagine this.
```
APP_COLOR = "pink"
```

Problem?
Suppose tomorrow
Production wants
```
green
```

Testing wants
```
yellow
```

Development wants
```
blue
```

You would have to edit the source code every time.

Instead
```
APP_COLOR = os.getenv("APP_COLOR")
```

Now the application remains identical.

Only configuration changes.

This is one of the principles of the **Twelve-Factor App** methodology.

---

# What is an Environment Variable?
An environment variable is simply a
> key-value pair

Example
```
APP_COLOR = pink
APP_MODE = production
DATABASE = mysql
PORT = 8080
```

Linux stores these variables in the process environment.

Every process has its own environment.

Visualization
```
Linux Process
----------------------

APP_COLOR=pink
PORT=8080
USER=ubuntu
HOME=/root

----------------------
```

When the process starts,
these variables are already available.

---

# Viewing Environment Variables in Linux
Print all variables
```
printenv
```

or
```
env
```

Example
```
HOME=/root
HOSTNAME=node01
USER=root
PATH=/usr/local/bin
```

View a specific variable
```
echo $HOME
```

or
```
echo $PATH
```

---

# Docker Environment Variables
Suppose our application needs
```
APP_COLOR=pink
```

Docker provides
```
docker run \
-e APP_COLOR=pink \
simple-webapp
```

What does Docker do?
Internally
```
docker run
        │
        ▼

Create Container
        │
        ▼

Set Environment
APP_COLOR=pink
        │
        ▼

Start Process
```

The application sees
```
APP_COLOR=pink
```

inside the container.

---

# Multiple Environment Variables
Docker
```
docker run \
-e APP_COLOR=blue \
-e APP_MODE=production \
-e PORT=8080 \
simple-webapp
```

Process Environment
```
APP_COLOR=blue
APP_MODE=production
PORT=8080
```

---

# Verifying Docker Environment Variables
Run
```
docker exec -it container-name env
```

Example
```
APP_COLOR=blue
PORT=8080
HOSTNAME=6af92d
HOME=/root
```

---

# Kubernetes Environment Variables
Kubernetes does exactly the same thing.

Docker
```
docker run \
-e APP_COLOR=pink \
simple-webapp
```

becomes
```
env:
- name: APP_COLOR
  value: pink
```

Notice the mapping.

Docker
```
-e
↓
Environment Variable
```

Kubernetes
```
env
↓
Environment Variable
```

---

# Basic Pod Example
```
apiVersion: v1
kind: Pod

metadata:
  name: simple-webapp

spec:
  containers:
  - name: simple-webapp
    image: simple-webapp
    env:
    - name: APP_COLOR
      value: pink
```

When the Pod starts
Kubernetes sends
```
APP_COLOR=pink
```
to the container runtime.

The runtime starts the application with
```
Environment
↓
APP_COLOR=pink
```

---

# Internal Flow
```
Pod YAML
↓

API Server
↓

etcd
↓

Scheduler
↓

kubelet
↓

containerd
↓

Container Process
↓

APP_COLOR=pink
```

Notice
Kubernetes itself never reads the variable.

It simply passes it to the runtime.

---

# Environment Variables Inside the Process
Imagine
```
env:
- name: APP_COLOR
  value: pink
- name: PORT
  value: "8080"
```

The process starts like this
```
Application Process
Environment

--------------------
APP_COLOR=pink
PORT=8080
--------------------
```

Application code
Python
```
import os
print(os.getenv("APP_COLOR"))
```

Output
```
pink
```

Java
```
System.getenv("APP_COLOR");
```

Go
```
os.Getenv("APP_COLOR")
```

NodeJS
```
process.env.APP_COLOR
```

Every language reads the same environment.

---

# Why is value Quoted Sometimes?
Example
```
value: "8080"
```

instead of
```
value: 8080
```

Because
Environment variables are always strings.

Linux does not have
```
Integer Environment Variable
Boolean Environment Variable
```

Everything is text.

Even
```
value: "true"
value: "8080"
value: "500Mi"
```
are all strings.

The application converts them if necessary.

---

# Multiple Environment Variables
Example
```
env:
- name: APP_COLOR
  value: pink

- name: APP_MODE
  value: production

- name: DATABASE
  value: mysql

- name: PORT
  value: "8080"
```

Container Environment
```
APP_COLOR=pink
APP_MODE=production
DATABASE=mysql
PORT=8080
```

---

# How to Verify Environment Variables
Create Pod
```
kubectl apply -f pod.yaml
```

Execute shell
```
kubectl exec -it simple-webapp -- sh
```

Inside
```
printenv
```

or
```
env
```

Output
```
APP_COLOR=pink
PORT=8080
HOME=/root
```

Specific variable
```
echo $APP_COLOR
```

Output
```
pink
```

---

# Updating Environment Variables
Suppose
```
env:
- name: APP_COLOR
  value: blue
```

Later
```
env:
- name: APP_COLOR
  value: green
```

Run
```
kubectl apply -f pod.yaml
```

What happens?
Remember

Environment variables are inside
```
spec:
  containers:
```
Changing them changes the Pod template.

Therefore Kubernetes creates
```
New ReplicaSet
↓

New Pods
↓

Old Pods Removed
```
Exactly like changing the image.

This is because environment variables are part of the Pod specification.

---

# Can Environment Variables Change While the Pod is Running?
No.
This is a common misconception.

Once a process starts
its environment is fixed.

Example
```
APP_COLOR=pink
```
Changing YAML later does **not** modify the running process.

Instead Kubernetes creates a **new Pod**.

---

# Common Mistake
Many beginners think
```
env:
APP_COLOR=pink
```
is valid.

Wrong.

It must be
```
env:
- name: APP_COLOR
  value: pink
```

Because
`env` is a list (array).

Each environment variable is an object.
Visualization

```
env
↓

List
↓
----------------------
name=APP_COLOR
value=pink
----------------------
name=PORT
value=8080
----------------------
```

---

# Different Ways to Define Environment Variables
There are **three** primary ways to configure environment variables in Kubernetes.
## Method 1: Direct Value
```
env:
- name: APP_COLOR
  value: pink
```

The value is hardcoded in the Pod manifest.

## Method 2: ConfigMap
```
env:
- name: APP_COLOR
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: APP_COLOR
```
The value is read from a ConfigMap.
This is the preferred approach for non-sensitive configuration.
We'll study ConfigMaps in detail next.

## Method 3: Secret
```
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: db-secret
      key: password
```
The value comes from a Secret.

This is commonly used for:
- Passwords
- API keys
- Tokens
- Certificates

We'll cover Secrets in the next lesson.

---

# Environment Variables vs Command-Line Arguments
Many students confuse these.
Command-line arguments
```
sleep 10
```

The application receives
```
argv[1] = 10
```

Environment variables
```
APP_COLOR=pink
```

The application receives
```
process.env.APP_COLOR
or
os.getenv("APP_COLOR")
```

These are completely different mechanisms.

Example
```
Command
python app.py

Arguments
--port 8080

Environment
APP_MODE=production
```

The application can access both independently.

---

# Real-World Example
Imagine a web application.

Instead of hardcoding values:
```
DATABASE_HOST = "10.0.0.15"
DATABASE_PORT = "3306"
DATABASE_USER = "admin"
DATABASE_PASSWORD = "mypassword"
```

A production-ready application reads them from the environment:
```
DATABASE_HOST=db-service
DATABASE_PORT=3306
DATABASE_USER=appuser
DATABASE_PASSWORD=<from Secret>
LOG_LEVEL=INFO
APP_MODE=production
```

The same container image can now run in development, testing, staging, and production simply by changing the environment variables.

---

# CKA Exam Tips
1. `env` is a **list**, so every variable is defined with `name` and `value`.
2. Environment variables are **always strings**. Quote numeric or boolean-looking values to avoid YAML type surprises.
3. Environment variables become part of the **Pod specification**. Changing them in a Deployment triggers a new rollout because the Pod template changes.
4. Verify environment variables using:
```
kubectl exec -it <pod-name> -- printenv
```

or
```
kubectl exec -it <pod-name> -- env
```

5. For production applications:
    - Use direct `value` for simple static settings.
    - Use **ConfigMaps** for non-sensitive configuration.
    - Use **Secrets** for sensitive values such as passwords, tokens, and certificates.

Understanding how environment variables flow from the Pod manifest to the container process is essential before learning ConfigMaps and Secrets, since both ultimately inject configuration into the container using the same underlying environment variable mechanism.