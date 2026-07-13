Here is the step-by-step procedure using **port 1338** as an example.

1. Update the httpd Configuration File
Open the primary configuration file with a text editor like `vi` or `nano`: [[1]

```
sudo vi /etc/httpd/conf/httpd.conf
```

Use code with caution.
Locate the `Listen` directive (typically around line 45) and change it from the default port `80` to your desired port number
```
# Change this line
Listen 1338
```

Use code with caution.

If you use Virtual Hosts, ensure you also update the port inside your `<VirtualHost * :8080>` blocks located in `/etc/httpd/conf.d/` or the main file. Save and close the file.

2. Configure SELinux Policies 
RHEL enforces [SELinux](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/using_selinux/index) by default. If you do not register the new port with SELinux, the `httpd` service will fail to restart. 

Run the following `semanage` command to append your new custom port to the valid HTTP port list:

```
sudo semanage port -a -t http_port_t -p tcp 1338
```

Use code with caution.

_(Note: If the port is already defined by another service, use `-m` instead of `-a` to modify it)._ 

3. Update the Firewall Rules
Allow network traffic to reach the new port through `firewalld`: 
```
sudo firewall-cmd --permanent --add-port=1338/tcp
sudo firewall-cmd --reload
```

Use code with caution.

You can safely remove the old HTTP service entry (`port 80`) if it is no longer required:
```
sudo firewall-cmd --permanent --remove-service=http
sudo firewall-cmd --reload
```

Use code with caution.

4. Restart and Verify the Service

Test the configuration file syntax to ensure there are no formatting errors: 
```
sudo apachectl configtest
```

Use code with caution.

If it returns `Syntax OK`, restart the `httpd` daemon to apply all changes:
```
sudo systemctl restart httpd
```

Use code with caution.

Verify that the service is successfully listening on your newly assigned port:
```
sudo ss -tlpn | grep httpd
```

Use code with caution.

If you need help configuring a **secure TLS setup (HTTPS)** on a different port or troubleshooting an **SELinux permission error**, please let me know!