# Lab-Linux Challenge 5

![](LINUX/Linux%20Challenges%20Kodekloud/Attachments/Pasted%20image%2020260410113609.png)

We got a couple of tasks that need to be done on `centos-host` server. Most of these tasks are dependent on each other but not all of them.
Inspect the requirements in detail by clicking on the icons of the interactive architecture diagram on the right and complete the tasks. Once done click on the `Check` button to validate your work.

---

## network
Add an extra IP to "eth0" interface on this system: 10.0.0.50/24
```bash
ip address add 10.0.0.50/24 dev eth0
```
## dns
Add a local DNS entry for the database hostname "mydb.kodekloud.com" so that it can resolve to "10.0.0.50" IP address.
```bash
sudo su -
vi /etc/hosts
10.0.0.50    mydb.kodekloud.com
```



## database
Install "mariadb" database server on this server and "start/enable" its service.
```bash
yum install mariadb-server -y
systemctl enable mariadb --now
systemctl status mariadb
```
## security
Set a password for mysql root user to "S3cure#321"
```bash
mysqladmin -u root password 'S3cure#321'
```

## root
The "root" account is currently locked on "centos-host", please unlock it.
Make user "root" a member of "wheel" group
```bash
 usermod -U root
 usermod -aG wheel root
```


## docker-image and docker-container
Create and run a new Docker container based on the "nginx" image. The container should be named as "myapp" and the port "80" on the host should be mapped to the port "80" on the container.
```bash
docker ps
docker pull nginx
docker run -d -p 80:80 --name myapp nginx
docker ps
```
## container start and stop
Create a bash script called "container-start.sh" under "/home/bob/" which should be able to "start" the "myapp" container. It should also display a message "myapp container started!"
```bash
echo -e '#!/bin/bash \ndocker start myapp \necho "myapp container started!"' > /home/bob/container-start.sh
chmod +x /home/bob/container-start.sh
```

Create a bash script called "container-stop.sh" under "/home/bob/" which should be able to stop the "myapp" container. It should also display a message "myapp container stopped!"
```bash
echo  -e '#!/bin/bash \ndocker stop myapp \necho "myapp container stopped!"' > /home/bob/container-stop.sh
chmod +x /home/bob/container-stop.sh
```

## cron
Add a cron job for the "root" user which should run "container-stop.sh" script at "12am" everyday.
Add a cron job for the "root" user which should run "container-start.sh" script at "8am" everyday.
```bash
crontab -l

crontab -e
0 0 * * * /home/bob/container-stop.sh
0 8 * * * /home/bob/container-start.sh
```

## pam
Edit the PAM configuration file for the "su" utility so that this utility only accepts the requests from the users that are part of the "wheel" group and the requests from the users should be accepted immediately, without asking for any password.
```bash
vi /etc/pam.d/su

```



![](LINUX/Linux%20Challenges%20Kodekloud/Attachments/Pasted%20image%2020260410120316.png)