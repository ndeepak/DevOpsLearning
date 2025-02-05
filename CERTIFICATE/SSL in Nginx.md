# **🔹Setup SSL in Nginx**
### **Step 1: Copy the Certificates to Nginx Directory**
```
sudo mkdir -p /etc/nginx/ssl
sudo cp server.crt /etc/nginx/ssl/
sudo cp server.key /etc/nginx/ssl/
sudo cp rootCA.crt /etc/nginx/ssl/
```

### **Step 2: Configure Nginx SSL**
Edit your Nginx configuration file (`/etc/nginx/conf.d/default.conf` or `/etc/nginx/sites-available/default`):
```
server {
    listen 443 ssl;
    server_name deepaknagarkoti.com *.deepaknagarkoti.com;

    ssl_certificate /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;
    ssl_trusted_certificate /etc/nginx/ssl/rootCA.crt;

    location / {
        root /usr/share/nginx/html;
        index index.html;
    }

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
}
```

### **Step 3: Restart Nginx**
```
sudo nginx -t  # Check for syntax errors
sudo systemctl restart nginx
```
✅ **Nginx SSL is now configured!** 🚀

---
### **🔹 Test Your SSL Configuration**

Run the following command to verify the SSL setup:
`openssl s_client -connect cas.com:443 -CAfile /etc/nginx/ssl/rootCA.crt`
If everything is set up correctly, you’ll see certificate details without errors.
🔹 Open **[https://deepaknagarkoti.com](https://deepaknagarkoti.com.np)** in your browser, and accept the security warning if the CA is not globally trusted.
✅ **You now have SSL enabled for Apache and Nginx using your own CA!** Let me know if you need further adjustments. 🎯