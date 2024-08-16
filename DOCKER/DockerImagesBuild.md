### Detailed Notes on Building Docker Images
#### Overview
Docker images are the core components of Docker containers. They contain everything needed to run an application, including code, runtime, libraries, environment variables, and configuration files. Docker images are built using two primary methods: **Docker Commit** and **Docker Build**.

### 1. Docker Commit
**Docker Commit** allows you to create a new Docker image from an existing container. This is useful when you’ve manually configured a container and want to save those changes for future use.

#### **Steps to Create an Image using Docker Commit:**
1. **Start a Container:** Begin by running a container using an existing image.   
    `docker run -it ubuntu bash`
    
    This command will start a new container from the Ubuntu image and drop you into a Bash shell.
    
2. **Make Changes Inside the Container:** Within the running container, you can install software, change configurations, or add files. For example:
```
apt-get update
apt-get install -y nginx
echo "Hello from my custom image!" > /var/www/html/index.html
```
3. **Commit the Container to an Image:** Once you’re satisfied with the changes, commit the container to a new image:
    `docker commit <container_id> my_custom_image`
    
    Replace `<container_id>` with the actual ID or name of the container. This creates an image named `my_custom_image` with all the changes made in the container.
    
4. **Verify the New Image:** You can list and verify the new image using:
    `docker images`
    
5. **Run a Container from the New Image:** To test the newly created image, run a container from it:    
    `docker run -d -p 80:80 my_custom_image`
    
    This command runs the container in the background, exposing port 80.


#### **Advantages of Docker Commit:**
- Quick and straightforward for creating images based on manual modifications.
- Ideal for prototyping and experimentation.

#### **Disadvantages of Docker Commit:**
- Not suitable for reproducible builds since the steps to create the image are not documented.
- Changes are not easily version-controlled.

### 2. Docker Build
**Docker Build** uses a Dockerfile to create images in a more structured and reproducible way. The Dockerfile is a script that contains a series of instructions to build an image.

#### **Dockerfile Basics:**
A typical Dockerfile contains the following directives:
- **FROM**: Specifies the base image.
- **RUN**: Executes commands in the container during the image build.
- **COPY/ADD**: Copies files from the host system to the container.
- **CMD**: Specifies the command to run when a container is started from the image.
- **EXPOSE**: Informs Docker that the container will listen on the specified network ports.

#### **Steps to Create an Image using Docker Build:**
1. **Create a Dockerfile:** Start by creating a `Dockerfile` in an empty directory:
```
# Use an official Ubuntu as a base image
FROM ubuntu:latest

# Update and install Nginx
RUN apt-get update && apt-get install -y nginx

# Copy custom HTML file to the Nginx web directory
COPY index.html /var/www/html/index.html

# Expose port 80 for web traffic
EXPOSE 80

# Start Nginx service
CMD ["nginx", "-g", "daemon off;"]
```
    In this example:
    
    - **FROM** specifies the base image as the latest version of Ubuntu.
    - **RUN** updates the package list and installs Nginx.
    - **COPY** copies a custom `index.html` file to the container.
    - **EXPOSE** makes port 80 accessible.
    - **CMD** runs Nginx in the foreground.
2. **Create the HTML File:** If you have the Dockerfile, create the `index.html` file in the same directory:
```
<html>
<head>
    <title>Welcome to My Custom Nginx Server!</title>
</head>
<body>
    <h1>Hello, Docker!</h1>
</body>
</html>
```
    
3. **Build the Docker Image:** Run the following command in the directory containing the Dockerfile to build the image:
    `docker build -t my_nginx_image .`
    
    This command builds an image named `my_nginx_image` using the current directory (specified by the `.`).
    
4. **Verify the Image:** List the images to ensure it was created successfully:
    `docker images`
    
5. **Run a Container from the Image:** Test the image by running a container from it:
    `docker run -d -p 80:80 my_nginx_image`
    This command starts the container and maps port 80 of the host to port 80 of the container.
    
6. **Access the Web Server:** You can now access the running Nginx server via your browser at `http://localhost`.
    

#### **Advantages of Docker Build:**
- Reproducibility: The Dockerfile provides a clear, version-controlled, and reproducible build process.
- Automation: The entire build process can be automated, making it ideal for CI/CD pipelines.

#### **Disadvantages of Docker Build:**
- Requires upfront knowledge of Dockerfile syntax.
- More complex than using Docker Commit for simple changes.

### **Conclusion**
Both Docker Commit and Docker Build have their use cases. **Docker Commit** is quick and easy for manual modifications but lacks reproducibility. **Docker Build** offers a structured, reproducible, and automated way to create images, which is ideal for production environments and continuous integration workflows.

By understanding both methods, you can choose the right approach based on your specific needs and the complexity of your Docker environment.