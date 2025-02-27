a **step-by-step guide** to setting up a **Jump Server (Bastion Host)** on **Linux (Ubuntu/RHEL)** to securely manage access to sensitive servers.

---
## **Step 1: Set Up the Jump Server**
### **1.1 Choose a Secure Machine**
- Deploy a **dedicated server (VM/physical)** in a **DMZ or secure subnet**.
- Ensure **minimal installed packages** to reduce attack surface.

### **1.2 Harden the OS**
- **Update the system**    
    `sudo apt update && sudo apt upgrade -y  # Ubuntu `
    `sudo yum update -y                      # RHEL`
- **Disable root login & enforce sudo usage**    
    `sudo sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config`
- **Create a dedicated admin user**
```
sudo adduser jumpadmin
sudo usermod -aG sudo jumpadmin  # For Ubuntu
sudo usermod -aG wheel jumpadmin # For RHEL
```
- **Enforce strong passwords**
```
sudo apt install libpam-pwquality  # Ubuntu
sudo yum install pam_pwquality     # RHEL
```
---
## **Step 2: Configure SSH for Secure Access**
### **2.1 Modify SSH Configuration**
Edit `/etc/ssh/sshd_config` and apply the following settings:
`sudo nano /etc/ssh/sshd_config`
Update/Add these lines:
```
Protocol 2
PermitRootLogin no
PasswordAuthentication no
AllowUsers jumpadmin
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
AllowTcpForwarding no
X11Forwarding no
```

**Restart SSH service:**
`sudo systemctl restart sshd`

---
## **Step 3: Implement Key-Based Authentication**
### **3.1 Generate SSH Keys (on Client Machine)**
Run the following command on your **local system (admin machine):**
`ssh-keygen -t rsa -b 4096`
Copy the public key to the jump server:
`ssh-copy-id jumpadmin@<jump-server-IP>`

**OR manually:**
`cat ~/.ssh/id_rsa.pub | ssh jumpadmin@<jump-server-IP> "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"`
### **3.2 Disable Password-Based SSH Login**
Edit `/etc/ssh/sshd_config` again and set:
`PasswordAuthentication no`
Restart SSH:
`sudo systemctl restart sshd`

---
## **Step 4: Set Up Controlled Access to Internal Servers**
### **4.1 Allow Only Jump Server to Access Secure Servers**
On **target secure servers**, edit the SSH config:
`sudo nano /etc/ssh/sshd_config`
Add:
`AllowUsers jumpadmin@<jump-server-IP>`

Restart SSH:
`sudo systemctl restart sshd`
### **4.2 Configure SSH ProxyJump on Admin's Machine**
To connect from **admin machine → jump server → secure server**, add this to `~/.ssh/config`:
```
Host secure-server
  HostName <secure-server-IP>
  User jumpadmin
  ProxyJump jumpadmin@<jump-server-IP>
```
Now, you can SSH directly:
`ssh secure-server`

---
## **Step 5: Monitor and Audit Activity**
### **5.1 Enable Logging for SSH Sessions**
```
sudo mkdir /var/log/jumpserver
sudo nano /etc/rsyslog.d/jumpserver.conf
```
Add:
`auth.*  /var/log/jumpserver/auth.log`
Restart rsyslog:
`sudo systemctl restart rsyslog`
### **5.2 Record Sessions Using TTY Logging**
Enable session logging for audit:
`sudo nano /etc/profile`
Add:
```
export HISTFILE=/var/log/jumpserver/history_$(whoami)_$(date +%F).log
exec script -q /var/log/jumpserver/session_$(whoami)_$(date +%F-%T).log
```
---
## **Step 6: Implement Multi-Factor Authentication (Optional)**
For added security, set up **Google Authenticator** for MFA:
```
sudo apt install libpam-google-authenticator  # Ubuntu
sudo yum install google-authenticator         # RHEL
```
Run:
`google-authenticator`
Follow the on-screen steps and configure `/etc/pam.d/sshd` to enforce MFA.

---
## **Step 7: Restrict Outbound Internet Access**
Ensure **jump server can only access internal secure servers**, not the open internet:
```
sudo iptables -A OUTPUT -p tcp --dport 22 -d <internal-network> -j ACCEPT
sudo iptables -A OUTPUT -p tcp --dport 80 -j DROP
sudo iptables -A OUTPUT -p tcp --dport 443 -j DROP
```
---

## **Step 8: Periodic Security Check**

1. **Review logs regularly**
    ```
    tail -f /var/log/auth.log  # Ubuntu
	tail -f /var/log/secure    # RHEL
    ```
2. **Monitor active SSH sessions**   
    `w && who && last`
3. **Check running processes**
    `ps aux | grep ssh`
---
### **Final Setup Overview**

|Component|Configuration|
|---|---|
|**Jump Server**|Dedicated access control machine|
|**SSH Hardening**|Key-based authentication, no root login, firewall rules|
|**Logging & Auditing**|Centralized logs, session recording|
|**MFA (Optional)**|Google Authenticator for extra security|
|**Network Restriction**|No direct access to internal systems from outside|

---
### **Conclusion**
A **jump server (bastion host)** adds a **critical security layer** by **controlling, monitoring, and restricting** access to secure servers. This ensures that **interns, external users, and even internal admins follow strict access policies** while reducing exposure to threats.
🚀