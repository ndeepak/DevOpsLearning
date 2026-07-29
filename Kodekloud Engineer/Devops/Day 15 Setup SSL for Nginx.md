Day 15: Setup SSL for Nginx

The system admins team of `xFusionCorp Industries` needs to deploy a new application on `App Server 2` in `Stratos Datacenter`. They have some pre-requites to get ready that server for application deployment. Prepare the server as per requirements shared below:  
  

  

1. Install and configure `nginx` on `App Server 3`.   
2. On `App Server 3 there is a self signed SSL certificate and key present at location `/tmp/nautilus.crt` and `/tmp/nautilus.key`. Move them to some appropriate location and deploy the same in Nginx.    
3. Create an `index.html` file with content `Welcome!` under Nginx document root.  
4. For final testing try to access the `App Server 3` link (via hostname) from `jump host` using curl command. For example: `curl -Ik https://<app-server-name>/`.

---
- SSH to App Server 2
- Install and configure **NGINX** on a remote server.
- Deploy a **self-signed SSL certificate** and key for secure access.
- Set up a secure server block to serve a simple HTML page.
- Validate HTTPS access from a **jump host**.
```
Dynamic|stapp03|banner|BigGr33n|Hosts Nautilus 
```


```bash
sudo yum install -y nginx  
sudo systemctl enable --now nginx


sudo mkdir -p /etc/nginx/ssl  
sudo mv /tmp/nautilus.crt /etc/nginx/ssl/  
sudo mv /tmp/nautilus.key /etc/nginx/ssl/
```

```bash
sudo tee /etc/nginx/conf.d/nautilus.conf << 'EOF'  
server {  
listen 443 ssl;  
server_name _;  
ssl_certificate /etc/nginx/ssl/nautilus.crt;  
ssl_certificate_key /etc/nginx/ssl/nautilus.key;  
root /usr/share/nginx/html;  
index index.html;  
}  
EOF
```

```bash
echo 'Welcome!' | sudo tee /usr/share/nginx/html/index.html
```

```bash
sudo nginx -t  
sudo systemctl reload nginx
```

```
curl -Ik https://stapp03/
```