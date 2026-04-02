Let's go step by step to generate a **self-signed wildcard SSL certificate** for `*.deepaknagarkoti.com`, ensuring it works on multiple servers and services.

---
## **1. Install OpenSSL (if not installed)**
Before we start, ensure **OpenSSL** is installed on your machine.
`openssl version`
If OpenSSL is not installed, install it:
- **Ubuntu/Debian:**
    `sudo apt update && sudo apt install openssl -y`
- **RHEL/CentOS:**
    `sudo yum install openssl -y`
---
## **2. Generate a Private Key**
The private key is used to create the certificate.
`openssl genrsa -out wildcard.deepaknagarkoti.com.key 2048`
- This generates a **2048-bit RSA private key**.
- Store this key securely; do not share it.
---
## **3. Create a Certificate Signing Request (CSR)**
A **CSR** contains details about your domain and is required for certificate generation.
`openssl req -new -key wildcard.deepaknagarkoti.com.key -out wildcard.deepaknagarkoti.com.csr`

You will be prompted to enter details:
- **Country Name (2 letter code):** `US` (or your country code)
- **State or Province Name:** `California`
- **Locality Name (City):** `Los Angeles`
- **Organization Name:** `MyCompany`
- **Organizational Unit Name:** `IT`
- **Common Name (CN):** `*.deepaknagarkoti.com`
- **Email Address:** `admin@deepaknagarkoti.com`

👉 The **Common Name (CN) MUST be `*.deepaknagarkoti.com`** to cover all subdomains.

---
## **4. Generate a Self-Signed Wildcard SSL Certificate**
`openssl x509 -req -days 365 -in wildcard.deepaknagarkoti.com.csr -signkey wildcard.deepaknagarkoti.com.key -out wildcard.deepaknagarkoti.com.crt`
- `-days 365` → Certificate valid for **1 year** (adjust if needed).
- This creates `wildcard.deepaknagarkoti.com.crt`.
---
## **5. Verify the Certificate**
Check if the certificate was generated correctly:
`openssl x509 -in wildcard.deepaknagarkoti.com.crt -noout -text`

---
## **6. (Optional) Create a `.pem` File for Services**
Some services require certificates in `.pem` format:
`cat wildcard.deepaknagarkoti.com.crt wildcard.deepaknagarkoti.com.key > wildcard.deepaknagarkoti.com.pem`

---
## **7. Deploying the Certificate on Different Services**
### **A. Apache Web Server**
1. Move the certificate and key to `/etc/ssl/certs/`:
    `sudo cp wildcard.deepaknagarkoti.com.crt /etc/ssl/certs/ `
    `sudo cp wildcard.deepaknagarkoti.com.key /etc/ssl/private/`
2. Edit Apache SSL config file (`/etc/apache2/sites-available/default-ssl.conf` or `/etc/httpd/conf.d/ssl.conf`):
```
<VirtualHost *:443>
    ServerName deepaknagarkoti.com
    ServerAlias *.deepaknagarkoti.com
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/wildcard.deepaknagarkoti.com.crt
    SSLCertificateKeyFile /etc/ssl/private/wildcard.deepaknagarkoti.com.key
</VirtualHost>
```
    
3. Enable SSL and restart Apache:
    `sudo a2enmod ssl
    `sudo systemctl restart apache2`
---
### **B. Nginx Web Server**
1. Move the certificate and key:
```
sudo cp wildcard.deepaknagarkoti.com.crt /etc/nginx/ssl/
sudo cp wildcard.deepaknagarkoti.com.key /etc/nginx/ssl/
```
    
2. Edit the Nginx configuration file (`/etc/nginx/sites-available/deepaknagarkoti.com`):
```
server {
    listen 443 ssl;
    server_name deepaknagarkoti.com *.deepaknagarkoti.com;

    ssl_certificate /etc/nginx/ssl/wildcard.deepaknagarkoti.com.crt;
    ssl_certificate_key /etc/nginx/ssl/wildcard.deepaknagarkoti.com.key;

    location / {
        root /var/www/html;
        index index.html;
    }
}
```
    
3. Restart Nginx:    
    `sudo systemctl restart nginx`
---
### **C. Kubernetes (Ingress Controller)**
4. Create a Kubernetes secret:
    `kubectl create secret tls cas-com-tls --cert=wildcard.deepaknagarkoti.com.crt --key=wildcard.deepaknagarkoti.com.key -n default`
    
5. Configure Ingress to use this secret:
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: cas-com-ingress
spec:
  tls:
  - hosts:
    - app.deepaknagarkoti.com
    - api.deepaknagarkoti.com
    secretName: cas-com-tls
  rules:
  - host: app.deepaknagarkoti.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
```
    
6. Apply the configuration:
    `kubectl apply -f ingress.yaml`    
---
### **D. Adding Certificate to Trusted Store on Other Machines**
If other servers or clients need to trust this certificate, copy `wildcard.deepaknagarkoti.com.crt` and **add it to their trusted CA store**:
- **Ubuntu/Debian:**
    `sudo cp wildcard.deepaknagarkoti.com.crt /usr/local/share/ca-certificates/
    `sudo update-ca-certificates`
- **RHEL/CentOS:**
    `sudo cp wildcard.deepaknagarkoti.com.crt /etc/pki/ca-trust/source/anchors/ 
  - `sudo update-ca-trust`
---
## **Final Notes**
✅ This **wildcard certificate** now works for:
- `app.deepaknagarkoti.com`
- `api.deepaknagarkoti.com`
- `dev.deepaknagarkoti.com`
- **Any subdomain of `*.deepaknagarkoti.com`** across multiple servers.
🚀 You can now use it for **web servers, Kubernetes, Docker, and other services**.