# **Docker Environment Variables - A Detailed Guide**

## **Introduction**
Environment variables in Docker allow you to configure and customize containerized applications without modifying the container image itself. These variables are used to pass configuration settings, secrets, database credentials, and other runtime parameters to the container.
Docker provides multiple ways to define and use environment variables.

---
## **1. Setting Environment Variables using `-e` Option**
The `-e` (or `--env`) flag allows you to pass environment variables when running a container.
### **Example 1: Passing a Single Environment Variable**
`docker run -d --name mycontainer -e MY_VAR="HelloWorld" ubuntu`
- `-e MY_VAR="HelloWorld"` → Sets the environment variable `MY_VAR` inside the container.
To check the variable inside the container:
`docker exec -it mycontainer bash `
`echo $MY_VAR`

---
## **2. Passing Multiple Environment Variables**
You can pass multiple variables using multiple `-e` options.
### **Example 2: Multiple Environment Variables**
`docker run -d --name mydb -e MYSQL_ROOT_PASSWORD=rootpass -e MYSQL_USER=myuser -e MYSQL_PASSWORD=mypassword mysql`
- `MYSQL_ROOT_PASSWORD=rootpass` → Sets root password for MySQL.
- `MYSQL_USER=myuser` → Creates a MySQL user.
- `MYSQL_PASSWORD=mypassword` → Sets password for the user.
Check variables inside the container:
`docker exec -it mydb env`

---
## **3. Using `--env-file` to Pass Environment Variables**
Instead of specifying environment variables in the command, you can store them in a file and pass them using the `--env-file` option.
### **Example 3: Using an Environment File**
1. **Create a file** named `env.list`:
```
MY_VAR=HelloWorld
MYSQL_ROOT_PASSWORD=rootpass
MYSQL_USER=myuser
MYSQL_PASSWORD=mypassword
```

2. **Run the container using the file:**
`docker run -d --name mycontainer --env-file env.list ubuntu`

1. **Verify inside the container:**
`docker exec -it mycontainer env`

---
## **4. Using `ENV` in a Dockerfile**
If you want to bake environment variables into an image, you can define them in a `Dockerfile` using the `ENV` instruction.
### **Example 4: Defining `ENV` in Dockerfile**
Create a `Dockerfile`:
```
FROM ubuntu
ENV MY_VAR="Hello World"
CMD ["bash", "-c", "echo $MY_VAR"]
```

Build and run the container:
```
docker build -t myimage .
docker run myimage
```
Output:
`Hello World`

---
## **5. Using `ARG` vs `ENV` in a Dockerfile**
- `ARG` → Used during build time, not available at runtime.
- `ENV` → Available during runtime.
### **Example 5: Using `ARG` and `ENV`**
```
FROM ubuntu
ARG BUILD_VERSION
ENV APP_VERSION=$BUILD_VERSION
CMD echo "App version is $APP_VERSION"
```

**Build and run:**
```
docker build --build-arg BUILD_VERSION=1.0 -t myimage .
docker run myimage
```
Output:
`App version is 1.0`

---
## **6. Using `docker-compose.yml` to Set Environment Variables**
You can also set environment variables in a `docker-compose.yml` file.
### **Example 6: Using `environment` in `docker-compose.yml`**
```
version: '3'
services:
  webapp:
    image: kodekloud/simple-webapp
    environment:
      - APP_ENV=production
      - DB_USER=admin
      - DB_PASSWORD=secret
```

Start the container:
`docker-compose up -d`

Check variables inside the container:
`docker exec -it <container_id> env`

---
## **7. Using `.env` File in ffDocker Compose**
Instead of defining variables in `docker-compose.yml`, you can store them in a `.env` file.
### **Example 7: Using `.env` File**
1. **Create a `.env` file:**
```
APP_ENV=production
DB_USER=admin
DB_PASSWORD=secret
```

2. **Modify `docker-compose.yml`:**
```
version: '3'
services:
  webapp:
    image: kodekloud/simple-webapp
    env_file:
      - .env
```

3. **Run the container:**
`docker-compose up -d`
---
## **8. Overriding Environment Variables**
When the same variable is defined in multiple places, the order of precedence is:
1. **Command-line `-e` option** (highest priority)
2. **`.env` file** (for `docker-compose.yml`)
3. **`env_file` in `docker-compose.yml`**
4. **`environment` in `docker-compose.yml`**
5. **`ENV` in `Dockerfile`** (lowest priority)

### **Example 8: Overriding Variables**
```
version: '3'
services:
  webapp:
    image: kodekloud/simple-webapp
    environment:
      - APP_ENV=staging
```
Run:
`docker run -e APP_ENV=production kodekloud/simple-webapp`
`APP_ENV` will be `production` since `-e` has the highest priority.

---
## **9. Removing or Unsetting Environment Variables**
You cannot remove an environment variable inside a running container, but you can unset it when starting the container.
### **Example 9: Unsetting a Variable**
`docker run -d -e MY_VAR=HelloWorld --env MY_VAR= ubuntu`
The second `--env MY_VAR=` unsets the variable.

---
## **10. Viewing Environment Variables in a Running Container**
To list all environment variables in a running container:
`docker exec -it <container_id> env`
or
`docker inspect <container_id> | grep -i env`

---
## **11. Using Environment Variables in `ENTRYPOINT` or `CMD`**
If you want to use environment variables inside an `ENTRYPOINT` script, use the following approach.
### **Example 11: Using `ENTRYPOINT`**
Create a script `entrypoint.sh`:
```
#!/bin/bash
echo "Welcome to $APP_NAME"
exec "$@"
```

Modify `Dockerfile`:
```
FROM ubuntu
ENV APP_NAME="MyApp"
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```
Build and run:
```
docker build -t myapp .
docker run myapp
```
Output:
`Welcome to MyApp`

---
## **Summary Table of Methods**

| Method               | Command Example                        |
| -------------------- | -------------------------------------- |
| `-e` Option          | `docker run -e VAR=value image`        |
| `--env-file`         | `docker run --env-file env.list image` |
| `ENV` in Dockerfile  | `ENV VAR=value`                        |
| `ARG` in Dockerfile  | `ARG VAR=value`                        |
| `docker-compose.yml` | `environment:` section                 |
| `.env` File          | `env_file:` section                    |

---
## **Conclusion**
Environment variables are a powerful way to configure Docker containers dynamically. Understanding the different ways to pass and manage them will help in designing efficient and scalable containerized applications. 🚀