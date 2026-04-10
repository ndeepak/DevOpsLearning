# Lab-Linux Challenge 2

![](LINUX/Linux%20Challenges%20Kodekloud/Attachments/Pasted%20image%2020260409141902.png)
The app server called `centos-host` is running a `Go app` on the `8081` port. You have been asked to troubleshoot some issues with `yum/dnf` on this system, Install `Nginx` server, configure Nginx as a `reverse proxy` for this Go app, install `firewalld` package and then configure some `firewall rules`.

Inspect the requirements in detail by clicking on the icons of the interactive architecture diagram on the right and complete the tasks. Once done click on the `Check` button to validate your work.


# To execute the task, you need to be root. Switch to root user
sudo su -


# Tasks:
1.   Troubleshoot the issues with "yum/dnf" and make sure you are able to install the packages on "centos-host"
 Fix yum DNS errors by inserting google nameserver
`echo "nameserver 8.8.8.8" >> /etc/resolv.conf`


2.   Install "nginx" package.  and Install "firewalld" package.
```bash
yum install firewalld -y
yum install nginx -y
```

3. Start and Enable "firewalld" service.
`yum install -y nginx firewalld`

Start and Enable "firewalld" service.
```
systemctl enable firewalld
systemctl start firewalld
```

Add firewall rules to allow only incoming port "22", "80" and "8081".
```bash
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --zone=public --add-port=8081/tcp --permanent
firewall-cmd --zone=public --add-port=22/tcp --permanent
firewall-cmd --reload
```

4. Start GoApp by running the "nohup go run main.go &" command from "/home/bob/go-app/" directory, it can take few seconds to start.
```
cd /home/bob/go-app
nohup go run main.go &
```

5. Configure Nginx as a reverse proxy for the GoApp so that we can access the GoApp on port "80". Start and Enable "nginx" service.
In /etc/ngin/nginx.conf,
Find this default block:
```conf
server {  
	listen 80 default_server;  
	listen [::]:80 default_server;  
	server_name _;  
	root /usr/share/nginx/html;  
}  
```

Replace it with this reverse‑proxy configuration
```conf
server {  
	listen 80;  
	server_name _;  	
	location / {  
		proxy_pass http://127.0.0.1:8081;  		
		proxy_set_header Host $host;  		
		proxy_set_header X-Real-IP $remote_addr;  		
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; 		proxy_set_header X-Forwarded-Proto $scheme;  
	}  
}  
```
This forwards **all HTTP traffic** from port 80 to the Go app.
Then
```bash
systemctl enable nginx
systemctl start nginx
systemctl status nginx
```

6. bob is able to login into GoApp using username "test" and password "test"