### How to Install Zabbix on RHEL 8

#### Step 1: Update the System
`sudo dnf update -y && sudo dnf install epel-release -y`

#### Step 2: Install Apache, MariaDB, and PHP
`sudo dnf install httpd mariadb-server mariadb php php-mysqlnd php-gd php-xml php-bcmath php-mbstring -y`

#### Step 3: Start and Enable Apache and MariaDB
```
sudo systemctl start httpd 
sudo systemctl enable httpd 
sudo systemctl start mariadb 
sudo systemctl enable mariadb
```
#### Step 4: Secure MariaDB
`sudo mysql_secure_installation`
Follow the prompts to set the root password and secure the installation.
#### Step 5: Create a Database for Zabbix
`sudo mysql -u root -p`

Run the following commands in the MySQL shell:
```
CREATE DATABASE zabbix CHARACTER SET utf8 COLLATE utf8_bin;
CREATE USER 'zabbix'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'localhost';
FLUSH PRIVILEGES;
EXIT;

```
#### Step 6: Install Zabbix Repository
```
rpm -Uvh https://repo.zabbix.com/zabbix/7.0/rhel/8/x86_64/zabbix-release-7.0-4.el8.noarch.rpm
dnf clean all
```

#### Step 7: Install Zabbix Server, Frontend, and Agent
`sudo dnf install zabbix-server-mysql zabbix-web-mysql zabbix-agent -y`

#### Step 8: Import Initial Schema and Data
`sudo zcat /usr/share/doc/zabbix-server-mysql*/create.sql.gz | mysql -uzabbix -p zabbix`

#### Step 9: Configure Zabbix Server
Edit the configuration file `/etc/zabbix/zabbix_server.conf` and set the database password:
`sudo vi /etc/zabbix/zabbix_server.conf`
Find and set:
`DBPassword=password`

#### Step 10: Configure PHP for Zabbix Frontend
Edit the configuration file `/etc/php-fpm.d/zabbix.conf`:
`sudo vi /etc/php-fpm.d/zabbix.conf`

Set the time zone:
`php_value[date.timezone] = Asia/Kathmandu`

#### Step 11: Start and Enable Zabbix Server and Agent
```
sudo systemctl restart zabbix-server zabbix-agent httpd php-fpm
sudo systemctl enable zabbix-server zabbix-agent httpd php-fpm
```

#### Step 12: Configure Firewall
Open the required ports:
```
sudo firewall-cmd --permanent --add-port=10051/tcp
sudo firewall-cmd --permanent --add-port=10050/tcp
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
```

#### Step 13: Set Up Zabbix Frontend

1. Open a web browser and navigate to `http://<your_server_ip>/zabbix`
2. Follow the installation wizard and provide the necessary database and server details.

#### Step 14: Complete the Installation

- Log in with the default credentials:
    - **Username**: Admin
    - **Password**: zabbix
- Change the default password after logging in for the first time.
---