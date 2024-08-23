### Commands

1. **Pull Jenkins Docker Image:**
        `docker pull jenkins/jenkins:lts`
    
2. **Run Jenkins Container:**
    `docker run -d --name jenkins-container -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts`
    
3. **Retrieve Initial Admin Password:**
    `docker exec jenkins-container cat /var/jenkins_home/secrets/initialAdminPassword`
    
4. **Access Jenkins Web Interface:**
    Navigate to `http://your_server_ip:8080` in your web browser.
    

By following these steps, you will have a Jenkins instance running in a Docker container, accessible through the specified ports.