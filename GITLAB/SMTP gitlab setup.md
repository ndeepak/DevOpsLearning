# Setting Up SMTP in a Dockerized GitLab Server
## Objective
Configure SMTP for a GitLab server deployed in Docker on an RHEL host system to send emails.
## Prerequisites
1. A running GitLab instance in a Docker container.
2. SMTP server details (example):    
    - **SMTP Server**: smtp.example.com        
    - **Port**: 25        
    - **Sender Email**: gitlab@example.com        
3. Ensure the SMTP server allows unauthenticated connections or verify authentication details.    
4. Test SMTP connectivity with `telnet`. 
---
## Step 1: Verify SMTP Connection
Use `telnet` to ensure the SMTP server is reachable and functional:
```
telnet smtp.example.com 25
HELO smtp.example.com
MAIL FROM: gitlab@example.com
RCPT TO: nagarkoti981681@gmail.com
DATA
Subject: Test Email
This is a test email sent manually using Telnet.
.
QUIT
```
- If the server responds positively, it is ready for configuration.    
---
## Step 2: Access GitLab Configuration
1. Enter the GitLab container:    
    ```
    docker exec -it <container_name> bash
    ```
     Replace `<container_name>` with the name of your GitLab container.    
2. Open the `gitlab.rb` file:    
    ```
    nano /etc/gitlab/gitlab.rb
    ```
---
## Step 3: Configure SMTP in `gitlab.rb`
Update the following SMTP settings:
```
gitlab_rails['smtp_enable'] = true
gitlab_rails['smtp_address'] = "smtp.example.com"
gitlab_rails['smtp_port'] = 25
gitlab_rails['smtp_user_name'] = nil  # Leave nil if no authentication is required
gitlab_rails['smtp_password'] = nil  # Leave nil if no authentication is required
gitlab_rails['smtp_domain'] = "example.com"
gitlab_rails['smtp_authentication'] = "plain"  # Use "login" if authentication is required
gitlab_rails['smtp_enable_starttls_auto'] = false
gitlab_rails['smtp_tls'] = false
gitlab_rails['smtp_openssl_verify_mode'] = 'none'
gitlab_rails['gitlab_email_from'] = "gitlab@example.com"
gitlab_rails['gitlab_email_reply_to'] = "noreply@example.com"  # Optional
```

---
## Step 4: Apply Changes
1. Exit the container and apply the changes:    
    ```
    docker exec -it <container_name> gitlab-ctl reconfigure
    ```
2. Restart the container for good measure:    
    ```
    docker restart <container_name>
    ```    
---
## Step 5: Test the SMTP Configuration
1. Log in to the GitLab instance.    
2. Navigate to **Admin Area** > **Settings** > **Notifications**.    
3. Send a test email to verify the configuration.   

---
## Step 6: Troubleshooting
- **Connection Issues**: Test the SMTP server from the host system using `telnet` or `tcpdump`:    
    ```
    tcpdump -i eth0 port 25
    ```    
- **Log Errors**: Check GitLab logs for errors:    
    ```
    docker logs <container_name>
    ```    
---
## Notes on Authentication
- **Unauthenticated Access**: Some SMTP servers allow unauthenticated connections due to IP whitelisting or open relay configuration.    
- If authentication is required, update the following:    
    ```
    gitlab_rails['smtp_user_name'] = "your_username"
    gitlab_rails['smtp_password'] = "your_password"
    ```    
- Always confirm with the SMTP server administrator whether authentication is needed.    

---
By following these steps, you can successfully configure SMTP for your Dockerized GitLab instance.