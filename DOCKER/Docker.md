### Docker - The Container Virtualization Tool
---
### 1. Difference between Physical Server, Virtual Machine, and Docker Container
#### Physical Server
- **Dedicated Hardware**: A physical machine with dedicated hardware resources (CPU, memory, storage).
- **Direct OS Installation**: The operating system is installed directly on the hardware.
- **Isolation**: Full isolation with complete resource allocation.
- **Performance**: No virtualization overhead, leading to optimal performance.
- **Usage**: Traditional data centers, critical performance-oriented applications.
#### Virtual Machine (VM)
- **Virtualization Layer**: Runs on a hypervisor that abstracts hardware resources.
- **Guest OS**: Each VM has its own guest operating system.
- **Isolation**: Strong isolation between VMs, but with higher resource overhead.
- **Performance**: Some overhead due to the hypervisor.
- **Usage**: Server consolidation, multiple OS environments, development, and testing.
#### Docker Container
- **Container Engine**: Runs on a container engine (e.g., Docker Engine) which utilizes the host OS kernel.
- **Shared OS Kernel**: Containers share the host OS kernel, leading to lightweight resource usage.
- **Isolation**: Process-level isolation with namespace and cgroups.
- **Performance**: Near-native performance with minimal overhead.
- **Usage**: Microservices, continuous deployment, scalable applications, DevOps.
### 2. Usage of VM and Docker in DevOps
- **VMs**: Useful for running multiple isolated environments with different OSes, good for complete environment replication.
- **Docker**: Ideal for running lightweight, isolated applications quickly, enabling rapid development, testing, and deployment cycles.
### 3. What is Docker? Why Docker?
- **Docker**: An open-source platform designed to automate the deployment, scaling, and management of applications in lightweight containers.
- **Why Docker?**
    - **Consistency**: Ensures the application runs the same regardless of where it is deployed.
    - **Isolation**: Provides isolated environments for applications, reducing conflicts.
    - **Efficiency**: Containers are lightweight and share the host OS kernel, leading to efficient resource usage.
    - **Portability**: Docker containers can run on any system that supports Docker, making it easy to move applications across environments.
### 4. Supported Platforms
#### Docker is supported on:
- **Linux Platforms**:
    - Ubuntu
    - RHEL (Red Hat Enterprise Linux)
    - CentOS
- **Windows**
- **OS X**
#### Cloud Platforms:
- Amazon EC2
- Rackspace Cloud
- Google Compute Engine
- Microsoft Azure
### Note:
- **Linux Containers on Windows and OS X**:
    - Docker installers for Windows and Mac include a tiny Linux virtual machine.
    - Docker creates Linux containers on top of this tiny Linux VM.
### 5. Requirements for Docker
- **Architecture**: 64-bit
- **Kernel Versions**: Linux kernel 3.8 or later
### 6. Requirements Check
- **Check Kernel Version**:
    `$ uname -a` 
    `$ uname -r`
- **Check OS Name**:
```
lsb_release -a 
lsb_release -cs 
cat /etc/os-release
```
### Installation Steps
---
#### To Install Docker on Ubuntu:
Reference: [Docker Documentation - Install on Ubuntu](https://docs.docker.com/engine/install/ubuntu)
1. **Download Docker Installation Script:**
    `$ curl -fsSL https://get.docker.com -o get-docker.sh`    
2. **Run Docker Installation Script:**
    `$ sudo sh get-docker.sh`
#### Installation Check
Verify Docker installation:
`$ sudo docker --version`
#### Adding User to Docker Group (Optional for non-root usage)
Add your user to the "docker" group:
`$ sudo usermod -aG docker <your-user>`
Check if the user is added to the group:
`$ cat /etc/group | grep docker`
**Note:** Restart the machine after adding a user to the Docker group.
#### Uninstall Docker
To completely uninstall Docker:
`$ sudo apt-get purge docker-ce docker-ce-cli containerd.io `
`$ sudo rm -rf /var/lib/docker`
This removes all Docker containers and images.
### Managing Docker Containers
---
#### Creating a New Docker Container
Create a new container using an Ubuntu base image:
`$ docker run -it ubuntu /bin/bash`
- **Explanation**:
    - `docker run`: Command to launch Docker containers.
    - `-i`: Keep STDIN open even if not attached.
    - `-t`: Allocate a pseudo-TTY for terminal interaction.
    - `-it`: Combine interactive mode with a TTY shell.
    - `ubuntu`: Docker image name (base image from Docker Hub).
    - `/bin/bash`: Launches a Bash shell inside the container.
#### Inspecting the New Container
After creating the container, explore its environment:
1. **Check Hostname:**
    `$ hostname` 
2. **View `/etc/hosts`:**
        `$ cat /etc/hosts`
3. **Check IP Address:**
        `$ hostname -i`
4. **List Running Processes:**
        `$ ps -ef`
5. **Navigate Filesystem:**
    `$ cd / && pwd && ls`
    This shows the root directory contents inside the container.
---
### SSH Setup for Docker Containers
---
#### 1. Create a New Container
Start a new Docker container with an Ubuntu base image:
`$ docker run -it ubuntu /bin/bash`
- **Note**: SSH is not installed by default in Docker containers.
### 2. Install SSH in the Container
Update package lists and install SSH server:
	`$ apt-get update` 
	`$ apt-get install -y ssh`
- **Explanation**:
    - `apt-get update`: Updates the package index.
    - `apt-get install -y ssh`: Installs SSH client and server packages.
#### 3. Start SSH Server in the Container
Start, stop, or restart the SSH service:
```
$ service ssh start 
$ service ssh stop 
$ service ssh restart 
$ service ssh status
```
#### 4. Create a User and Set Password
Create a new user and set up a password for SSH access:
```
$ useradd -m -d /home/username -s /bin/bash username 
$ passwd username`
```
#### 5. Connect to the Container via SSH
From the host machine, connect to the container using SSH:
`$ ssh username@172.17.0.3`
- Replace `172.17.0.3` with the actual IP address of your container.
---
#### Additional Docker Container Operations
##### Shutdown a Container
Exit the container to stop it:
`$ exit`
##### Login to a Stopped Container
Start and attach to a stopped container:
```
$ docker start <container-id> 
$ docker attach <container-id> 
$ docker start -ai <container-id>

```
- **Note**: Use `docker ps -a` to find the `<container-id>` of the stopped container.
---
### Docker Container Management
---
#### List Containers
- List all containers (both stopped and running):
        `$ docker container ls -a` 
        `$ docker ps -a`    
- List a specific number of containers (e.g., last 1):
    `$ docker ps -n 1`
- List running containers only:
    `$ docker container ls` 
    `$ docker ps`
- List stopped containers only:
    `$ docker container ls -f status=exited`
#### Container Details from `docker ps -a` Output
The `docker ps -a` command output includes:
- Image name
- Container ID
- Status (Up / Exited)
- Container name
#### Show Last Created Container
Show details of the last created container (stopped or running):
`$ docker container ls -l`
#### Naming and Renaming Containers
- Create a container with a specified name:
    `$ docker run --name container_name -it ubuntu /bin/bash`
    **Note**: Container names must be unique.
- Rename a container:
    `$ docker rename db-server3 db-server-name3`
#### Deleting Containers
- Delete a container by ID or name:
    `$ docker rm <container-ID-or-name>`
- Delete all containers (running or stopped):
    `$ docker rm -f $(docker container ls -a -q)`
- Delete running containers only:
    `$ docker rm -f $(docker container ls -q)`  
#### Starting, Stopping, and Restarting Containers
- Start a stopped container:
    `$ docker start container_name`    
- Stop a running container:
    `$ docker stop <container-name>`    
- Restart a container:
    `$ docker restart container_name`  

	`docker stop container (gracefully stop the container)`
	`docker kill container (forcibly stop the container)`
	
#### Attaching and Executing Commands in Containers
- Attach to a running container:
```
    $ docker attach container_name 
    $ docker attach <container_id> 
```
- Execute a command in a running container:
    `$ docker exec -it tomcat-server ps -ef`   
- Get an independent terminal session in a container:
    `$ docker exec -it tomcat-server /bin/bash`   
#### Shortcut Keys
- Detach a running container and leave it running:
    `Ctrl + p + q`    
- Stop a container:
    `Ctrl + d`   
#### Run a Container in Background (Detached Mode)
Create a container in the background without terminal access:
`$ docker run -it -d ubuntu /bin/bash`

---
### Docker Statistics and Resource Management
---
#### Display Container Usage Statistics
- Display real-time usage statistics of a container:
    `$ docker stats <container-name>`
- Display container statistics without streaming updates:
    `$ docker stats --no-stream <container-name>`
- Display statistics for all containers without streaming updates:
    `$ docker stats --no-stream --all`
- Display specific container resource usage formatted (e.g., memory usage):
    `$ docker stats --no-stream --format "{{.MemUsage}}" <container-name>`
- Display specific container CPU usage formatted:   
    `$ docker stats --no-stream --format "{{.CPUPerc}}" <container-name>`
#### Memory Allocation
- Allocate memory for a new container (e.g., allocate 1GB RAM):
    `$ docker run -it --name tomcat-server -m 1g ubuntu /bin/bash`   
- Allocate memory for a new container with 512MB RAM:
    `$ docker run -it --name tomcat-server -m 512m ubuntu /bin/bash`    
- Update memory allocation of an existing container (e.g., update to 2024MB):
    `$ docker update -m 2024m tomcat-server`   
#### CPU Allocation
- Allocate CPUs for a new container (e.g., allocate 2 CPUs):
    `$ docker run -it --cpus="2" --name jenkins-server ubuntu /bin/bash`    
- Update CPU allocation of an existing container (e.g., update to 2 CPUs):
    `$ docker update --cpus="2" jenkins-server`   

---
### Docker Images
#### Overview and Advantages
- Docker images are used as templates for creating containers.
- Advantages of Docker images include:
    - Solving the "Works on my machine" problem
    - Rapid setup of local development environments
    - Easy troubleshooting by replacing problematic instances
    - Efficient auto-scaling and disposable environments
    - Utilization of local machine resources for testing and development
#### Listing Docker Images
- List all Docker images:
    `$ docker image ls`    
- Docker images are stored in `/var/lib/docker/image/overlay2/imagedb/content/sha256`.
#### Building Docker Images
- Two methods to create Docker images:
    1. **Docker Commit**: Create an image from a container.
    2. **Docker Build**: Use a Dockerfile to specify image contents and build steps.
---
