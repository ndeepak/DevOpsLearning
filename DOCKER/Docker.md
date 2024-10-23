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
        $ lsb_release -a 
        $ lsb_release -cs 
        $ cat /etc/os-release
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
---
### Creating Docker Image using `docker commit` Command
#### Project-1: Creating an Nginx Docker Image with Application Code
##### Step-by-Step Process:
1. **Create a Container**
    `$ docker run -it --name nginx-container ubuntu /bin/bash`    
2. **Install Nginx**
```
    $ apt-get update 
    $ apt-get install -y nginx    
```
3. **Deploy Application Code**    
    - Place the following content into `/var/www/html/index.html` within the container: 
`<html>`
    `<body>`
        `<h1 style="color:red;">Ndeepak</h1>`
    `</body>`
`</html>`

4. **Create Docker Image from Container**
    `$ docker commit nginx-container username/nginx-img`    
    - Syntax:
    `$ docker commit <container-name> <image-name>`
5. **Verify Image Creation**
    `$ docker image ls`    
6. **Push Image to Docker Hub**
    - Login to Docker Hub (if not logged in):        
        `$ docker login`
    - Push the newly created image:
        `$ docker push username/nginx-img`        
7. **Test the Image**    
    - Run a container using the pushed image to verify functionality:
        `$ docker run -it username/nginx-img /bin/bash`        
    - Access the application at: `http://172.17.0.2:80`
##### Additional Notes:
- **Manage Nginx Server**:   
```
    $ sudo service nginx start 
    $ sudo service nginx stop 
    $ sudo service nginx restart 
    $ sudo service nginx status
```
- **Uninstall Nginx**:
        `$ sudo apt-get purge nginx nginx-common`
### Container Status: Create and Pause
---
- **Create a Container**: The `docker run` command creates and starts a new container instance based on a Docker image.
- **Pause a Container**: The `docker pause` command suspends all processes in a running container.
    Example:
    `$ docker pause <container-name>`
---
PROJECT-2:
=============
DAY-6:
# Creating docker image using "docker build" command
=================
	- mkdir gamutgurus
	- cd gamutgurus
	- touch Dockerfile

	--> 'gamutgurus' directory is called "context" or "build context".
		It contains the code, files or other data that you want to include in the 
		image.
	
	- Write Dokckerfile:
		FROM ubuntu:16.04
		MAINTAINER "info@gamutgurus.com"
		RUN apt-get update
		RUN apt-get install -y nginx
		COPY index.html /var/www/html
		ENTRYPOINT service nginx start && bash

index.html:
=======
<html>
   <body style="background-color:powderblue;">
     <h1 style="color:red;">Gamug Gurus Online Training Portal</h1>
	</body> 
</html>
 	
# Building docker image:
	$ cd gamutgurus
	$ docker build -t "nageshvkn/nginx-img" .

Note: Building the image if 'Dockerfile' has different name.
	  Use "-f <YourDockerfileName>" option.
	  Example: $ docker build -f MyDockerfile -t="nageshvkn/nginx-img" .

# Listing docker image
	$ docker image ls

# Create an account in docker hub

# Pushing custom images to docker repository
	$ docker login
	$ docker push nageshvkn/nginx-image

#
Testing Image
1. Remove the local image so that it will be downloaded from Docker Hub.
	$ docker rmi nageshvkn/nginx-image (OR)
	$ docker image rm nageshvkn/nginx-image
 
2. Creating a new container from our image
	$ docker run -it --name nginx-container nageshvkn/nginx-img /bin/bash

Note: start the nginx server manually as it's not fixed yet. It will be fixed in the next topic.

3. Verify if nginx is running from the container.
	$ http://172.17.0.2:80
	
#
User Images Syntax:
	nageshvkn/nginx-img (username/imagename)

Official Images Syntax:
	ubuntu

# Specifying Image via tags
	- ubuntu:16.04
	  ubuntu- is image name
	  16.04 - is called tag


# Deleting an Image
	- docker rmi gamut/nginx

# Deleting all Images
	- docker rmi $(docker images -q)


# Container creation process - Deep dive
  How contaner is created:
		
		Writable Layer		
		-		
		Gamutkart application		
		Apache image
		nginx image
		-		
		Ubuntu Base Image(rootfs)
		-
		Bootfs:
		    cgroups, namespace, lxc, devicemapper/aufs/overlay..etc.
		Kernel


Volumes:
===============
# List all volumes available in host machine
	$ docker volume ls
 
# Create a new Named Volume
	$ docker volume create deployment_code

# Check Mount point directory
	$ docker inspect deployment_code

# Mount Volume(deployment_code) to a new container
	$ docker run -it -v deployment_code:/deployment_code ubuntu:16.04 /bin/bash

# Create 'Read-only' Volumes
	$ docker run -it -v deployment_code:/deployment_code:ro ubuntu:16.04 /bin/bash

# Removing a Volume
	$ docker volume rm deployment_code

# Remove all unused Volumes
	$ docker volume prune

# Note:
Creating host Volume with your own directory in host machine (OR)
Creating host Volume with existing directory in the host machine
	$ docker run -it -v /home/gamut/Distros:/Distros ubuntu /bin/bash

# bind mount
$ docker run -it --mount type=bind,source=/home/gamut/Distros,target=/Distros ubuntu /bin/bash

# List down all containers which are using a particular volume
	$ docker ps -a --filter volume=deployment_code


DAY-8:
Gamutkart Real-time application
============================
Agenda:
How do you containerize or dockerize your application?
Can you explain how you have implememnted Docker for your application?


1. Clone the source code from Git or any other V.C.S
	$ git clone https://github.com/nageshvkn/gamutkart2.git
 
2. Build the code using your favourate build tool Maven/ANT
	$ mvn install

3. Create docker image for the application(gamutkart2) with
   war file, tomcat,jdk...etc using below Dockerfile.
	Dockerfile:
	-------------
	FROM ubuntu:16.04 
	MAINTAINER "info@gamutgurus.com"
	RUN apt-get update
	RUN apt-get install -y openjdk-8-jdk
	ENV JAVA_HOME /usr
	ADD apache-tomcat-8.5.38.tar.gz /root
	COPY target/gamutkart.war /root/apache-tomcat-8.5.38/webapps
	ENTRYPOINT /root/apache-tomcat-8.5.38/bin/startup.sh && bash

4. Build the Image using below command
	$ docker build -t "nageshvkn/gamutkart-img" .
	
4A. Push the image to docker hub.
        $ docker push nageshvkn/gamutkart-img

5. Run below shell script to create an environment with give no. containers
	$ ./create-env.sh 10

6. Observer all containers created using above script ($ docker ps)

7. Launch the gamutkart application from all containers.
	$ http://IP:8080/gamutkart

---

7pm-daily-batch

#
Docker and Jenkins Integration
1. Create a new Free style project in Jenkins
2. Configure Git, Maven, Docker Image creation & Environment creation using below.
        - Configure Git URL under "Source code Management"
        - Provide Maven's 'install' command under build section
        - Open 'Execute shell' and type below commands for creating Image and Environment
                - docker build -t "nageshvkn/gamutkart-img" . (Note: don't forget "." at the                                                                                      end)
                - ./create-env.sh 10


1. How to download image from private repo
2. 


