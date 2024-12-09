### **Creating Docker Images using `docker commit` (Not Recommended)**

#### **Project 1: Creating an Nginx Docker Image with Application Code**
##### **Step-by-Step Process:**
1. **Create a Container:**   
    `docker run -it --name nginx-container ubuntu /bin/bash`
    
2. **Install Nginx:**
    `apt-get update apt-get install -y nginx`
    
3. **Deploy Application Code:**  
    Create and edit the `/var/www/html/index.html` file:
```
<html>
  <body>
    <h1 style="color:red;">Ndeepak</h1>
  </body>
</html>
```
    
4. **Create Docker Image from the Container:**
    `docker commit nginx-container username/nginx-img`
    - Syntax: `docker commit <container-name> <image-name>`
5. **Verify Image Creation:**
    `docker image ls`
    
6. **Push Image to Docker Hub:**
    - Log in to Docker Hub (if not logged in):
        `docker login`
        
    - Push the newly created image:
        `docker push username/nginx-img`
        
7. **Test the Image:**   
    `docker run -it username/nginx-img /bin/bash`
    - Access the application at `http://<container-ip>:80`

##### **Additional Nginx Commands:**
```
sudo service nginx start
sudo service nginx stop
sudo service nginx restart
sudo service nginx status
```

##### **Uninstall Nginx:**
`sudo apt-get purge nginx nginx-common`

---
### **Creating Docker Images using `docker build` (referred Method)**
#### **Project 2: Creating an Nginx Docker Image with `Dockerfile`**
1. **Setup Project Directory:**
```
mkdir ndeepak
cd ndeepak
touch Dockerfile
```
    ndeepak is called context or build context, it contains the code, files or other data that you want to include in the image.
2. **Write Dockerfile:** [[DockerfilesIntro]]
```
FROM ubuntu:16.04
MAINTAINER "deepak.nagarkoti@cas.com.np"
RUN apt-get update
RUN apt-get install -y nginx
COPY index.html /var/www/html
ENTRYPOINT service nginx start && bash
```
    
3. **Create `index.html`:**
```
<html>
  <body style="background-color:powderblue;">
    <h1 style="color:red;">Deepak Nagarkoti Security Engineer</h1>
  </body> 
</html>
```
    
4. **Build the Docker Image:**
    `docker build -t "ndeepak0x/nginx-img" .`
    
5. **Verify the Image:**
    `docker image ls`
    
6. **Push Image to Docker Hub:**
```
docker login
docker push ndeepak0x/nginx-img
```

7. **Test the Image:**
    `docker run -it --name nginx-container ndeepak0x/nginx-img /bin/bash`
---
