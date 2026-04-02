# **🔹Setup SSL in Apache**
### **Step 1: Copy the Certificates to Apache Directory**
Move your generated **server.crt**, **server.key**, and **rootCA.crt** to Apache’s SSL directory:
```
sudo cp server.crt /etc/pki/tls/certs/
sudo cp server.key /etc/pki/tls/private/
sudo cp rootCA.crt /etc/pki/ca-trust/source/anchors/
sudo update-ca-trust
```
### **Step 2: Configure Apache SSL Virtual Host**
Edit your Apache SSL configuration file (usually in `/etc/httpd/conf.d/ssl.conf` or `/etc/apache2/sites-available/default-ssl.conf`):
```
<VirtualHost *:443>
    ServerAdmin admin@deepaknagarkoti.com
    ServerName deepaknagarkoti.com
    ServerAlias *.deepaknagarkoti.com

    SSLEngine on
    SSLCertificateFile /etc/pki/tls/certs/server.crt
    SSLCertificateKeyFile /etc/pki/tls/private/server.key
    SSLCACertificateFile /etc/pki/ca-trust/source/anchors/rootCA.crt

    DocumentRoot /var/www/html
    <Directory "/var/www/html">
        Require all granted
    </Directory>

    ErrorLog logs/ssl_error_log
    CustomLog logs/ssl_access_log combined
</VirtualHost>
```

### **Step 3: Enable SSL and Restart Apache**
```
sudo a2enmod ssl  # For Debian/Ubuntu
sudo systemctl restart apache2  # Ubuntu/Debian
sudo systemctl restart httpd    # RHEL/CentOS
```
✅ **Apache SSL is now configured!** 🚀

---
### **🔹 Test Your SSL Configuration**

Run the following command to verify the SSL setup:
`openssl s_client -connect cas.com:443 -CAfile /etc/nginx/ssl/rootCA.crt`
If everything is set up correctly, you’ll see certificate details without errors.
🔹 Open **[https://deepaknagarkoti.com](https://deepaknagarkoti.com.np)** in your browser, and accept the security warning if the CA is not globally trusted.
✅ **You now have SSL enabled for Apache and Nginx using your own CA!** Let me know if you need further adjustments. 🎯

---
