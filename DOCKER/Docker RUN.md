## `docker run` Command - Detailed Explanation

The `docker run` command is used to create and start a container from a specified Docker image. It is one of the most fundamental commands in Docker.
### **Basic Syntax**
`docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`
- `[OPTIONS]` → Additional parameters to customize the container's behavior
- `IMAGE` → The image from which the container is created
- `[COMMAND]` → The command to run inside the container
- `[ARG...]` → Arguments passed to the command
---
## **1. Running a Basic Container**
### **Example 1: Running an Ubuntu Container**
`docker run ubuntu`
- Downloads (pulls) the `ubuntu` image from Docker Hub if not already available
- Runs a container using the `ubuntu` image
- The container starts but immediately exits because no interactive session or command is provided
---
## **2. Running a Container Interactively**
### **Example 2: Running Ubuntu with an Interactive Shell**
`docker run -it ubuntu /bin/bash`
- `-i` → Interactive mode (keeps STDIN open)
- `-t` → Allocates a pseudo-TTY (terminal)
- `/bin/bash` → Runs Bash shell inside the container
- The user gets a shell prompt inside the container
To exit:
`exit`

---
## **3. Running a Container in Detached Mode**
### **Example 3: Running a Background Container**
`docker run -d nginx`
- `-d` → Runs container in detached mode (background)
- `nginx` → Runs the `nginx` web server in a container
To check running containers:
`docker ps`
To stop the container:
`docker stop <container_id>`

---
## **4. Running a Container with Port Mapping**
### **Example 4: Exposing a Port for a Web Server**
`docker run -d -p 8080:80 nginx`
- `-p 8080:80` → Maps port `8080` on the host to port `80` in the container
- Access Nginx via `http://localhost:8080`
---

## **5. Running a Container with a Custom Name**
### **Example 5: Assigning a Name to the Container**
`docker run -d --name mynginx -p 8080:80 nginx`
- `--name mynginx` → Assigns the name `mynginx` to the container
Check container status:
`docker ps`
Stop the container:
`docker stop mynginx`

---
## **6. Running a Container with Volume Mounting**
### **Example 6: Mounting a Local Directory**
`docker run -d -v /mydata:/usr/share/nginx/html -p 8080:80 nginx`
- `-v /mydata:/usr/share/nginx/html` → Mounts `/mydata` on the host to `/usr/share/nginx/html` in the container
---
## **7. Running a Container with Environment Variables**
### **Example 7: Passing Environment Variables**
`docker run -d -e MYSQL_ROOT_PASSWORD=my-secret-pass mysql`
- `-e MYSQL_ROOT_PASSWORD=my-secret-pass` → Sets the environment variable `MYSQL_ROOT_PASSWORD`
---
## **8. Running a Container with Resource Limits**
### **Example 8: Limiting CPU and Memory Usage**
`docker run -d --memory=512m --cpus=1 nginx`
- `--memory=512m` → Limits container memory to 512MB
- `--cpus=1` → Limits CPU usage to 1 core
---
## **9. Automatically Removing Containers After Exit**
### **Example 9: Using `--rm`**
`docker run --rm ubuntu echo "Hello, Docker!"`
- `--rm` → Automatically removes the container after it exits
---
## **10. Running a Container in the Background and Attaching Later**
### **Example 10: Running and Attaching**
`docker run -dit --name testcontainer ubuntu`
- Runs an interactive Ubuntu container in the background  
    Attach to the running container:
`docker attach testcontainer`
Detach without stopping:
- Press `Ctrl + P` then `Ctrl + Q`
---
## **11. Running a Container in a Specific Network**
### **Example 11: Connecting to a Custom Network**
`docker network create mynetwork `
`docker run -d --name webserver --network mynetwork nginx`
- `docker network create mynetwork` → Creates a custom network
- `--network mynetwork` → Connects the container to `mynetwork`
---
## **12. Running a Container with Restart Policy**
### **Example 12: Ensuring a Container Restarts Automatically**
`docker run -d --restart=always nginx`
- `--restart=always` → Restarts the container automatically if it stops
Other policies:
- `no` (default) → Does not restart
- `always` → Always restarts
- `unless-stopped` → Restarts unless manually stopped
- `on-failure` → Restarts only if it exits with a non-zero status
---
## **Summary of Common Options**

|Option|Description|
|---|---|
|`-d`|Runs container in detached mode|
|`-it`|Runs container interactively with TTY|
|`-p HOST:CONTAINER`|Maps host port to container port|
|`--name NAME`|Assigns a name to the container|
|`-e ENV_VAR=VALUE`|Sets environment variables|
|`-v HOST:CONTAINER`|Mounts a volume|
|`--rm`|Removes the container after exit|
|`--memory`|Limits memory usage|
|`--cpus`|Limits CPU usage|
|`--network`|Connects to a custom network|
|`--restart`|Defines a restart policy|

---
## **Conclusion**
The `docker run` command is a powerful tool that allows you to create, manage, and customize containers. It is crucial to understand its various options for efficient container management in different scenarios. 🚀