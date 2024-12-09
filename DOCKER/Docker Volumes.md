### **Docker Volumes Notes**
#### **Volume Management Commands:**
1. **List All Volumes:**
    `docker volume ls`
    
2. **Create a New Named Volume:**
    `docker volume create deployment_code`
    
3. **Inspect Volume Details:**
    `docker inspect deployment_code`
    
4. **Mount Volume to a Container:**
    `docker run -it -v deployment_code:/deployment_code ubuntu:16.04 /bin/bash`
    
5. **Create Read-Only Volumes:**
    `docker run -it -v deployment_code:/deployment_code:ro ubuntu:16.04 /bin/bash`
    
6. **Remove a Volume:**
    `docker volume rm deployment_code`
    
7. **Remove All Unused Volumes:**
    `docker volume prune`
    
8. **Bind Mount Example:**    
    `docker run -it --mount type=bind,source=/home/deep/Distros,target=/Distros ubuntu /bin/bash`
    
9. **List Containers Using a Specific Volume:**
    `docker ps -a --filter volume=deployment_code`

---

