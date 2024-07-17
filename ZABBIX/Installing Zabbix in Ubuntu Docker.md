Here's a step-by-step guide to install Zabbix 7.0 LTS on an Ubuntu 24.04 Docker machine:
### Step 1: Set up an Ubuntu Docker Container

First, create and start a Docker container running Ubuntu 24.04:
`docker run -d --name zabbix-ubuntu -p 80:80 -p 10051:10051 -p 10050:10050 ubuntu:24.04`

### Step 2: Access the Container
Access the running Docker container:
`docker exec -it zabbix-ubuntu bash`

### Step 3: Update the System
Update the package list and upgrade the installed packages:
`apt update apt upgrade -y`

### Step 4: Install Zabbix Repository
Download and install the Zabbix repository package:
```
wget https://repo.zabbix.com/zabbix/7.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_7.0-2+ubuntu24.04_all.deb
dpkg -i zabbix-release_7.0-2+ubuntu24.04_all.deb
apt update

```
### Step 5: Install Zabbix Server, Frontend, and Agent
Install Zabbix server, frontend, agent, and other necessary packages:
`apt install zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-sql-scripts zabbix-agent -y`

### Step 6: Set Up the Database
Make sure you have MySQL server installed and running. Then, create the Zabbix database and user:
1. Access MySQL:
    `apt install mysql-server -y && mysql -uroot -p`
    
2. Create the database and user:
```
CREATE DATABASE zabbix CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
CREATE USER 'zabbix'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'localhost';
SET GLOBAL log_bin_trust_function_creators = 1;
quit;
```
    
3. Import the initial schema and data:    
    `zcat /usr/share/zabbix-sql-scripts/mysql/server.sql.gz | mysql --default-character-set=utf8mb4 -uzabbix -p zabbix`
    
4. Disable `log_bin_trust_function_creators` option after importing database schema:
```
mysql -uroot -p
SET GLOBAL log_bin_trust_function_creators = 0;
quit;
```
### Step 7: Configure Zabbix Server
Edit the Zabbix server configuration file to set the database password:
```
nano /etc/zabbix/zabbix_server.conf
# Set the following parameter:
DBPassword=password
```
### Step 8: Start Zabbix Services
Start Zabbix server and agent processes and enable them to start at system boot:
`systemctl restart zabbix-server zabbix-agent apache2 && systemctl enable zabbix-server zabbix-agent apache2`

### Step 9: Access Zabbix Web Interface
Open your web browser and navigate to the Zabbix UI web page:
`http://<container_ip>/zabbix`

Follow the on-screen instructions to complete the setup.
### Step 10: Clean Up and Exit
Once the installation is complete, exit the container shell:
`exit`
Your Zabbix installation should now be running and accessible from your browser.