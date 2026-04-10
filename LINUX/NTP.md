# **NTP (Network Time Protocol) in Linux Servers – Step-by-Step Guide**
## **What is NTP?**
Network Time Protocol (NTP) is used to synchronize the system clock with an accurate time source, such as an external NTP server. In modern Linux distributions, **Chrony** is the preferred NTP implementation.

---
## **Step 1: Installing Chrony (NTP Service)**
Chrony is an implementation of NTP that is designed to keep the system time accurate, even in less stable network conditions.
### **On the NTP Server:**
Install Chrony using:
- **For Debian/Ubuntu:**
    `sudo apt update && sudo apt install chrony -y`
    
- **For RHEL/CentOS:**    
    `sudo yum install chrony -y`
### **On the NTP Client:**
Install Chrony just like on the server:
- **Debian/Ubuntu:**
    `sudo apt install chrony -y`    
- **RHEL/CentOS:**
    `sudo yum install chrony -y`
---
## **Step 2: Configure the NTP Server**
1. Open the Chrony configuration file:
    `sudo vi /etc/chrony.conf`    
2. Allow specific client machines or a whole subnet to access the NTP server:
    - To allow a single client:
        `allow 192.168.1.100`
    - To allow a whole subnet (e.g., `192.168.1.0/24`):
        `allow 192.168.1.0/24`
3. Save and exit (`:wq` in `vi`).

---
## **Step 3: Configure the NTP Client**
1. Open the Chrony configuration file:
    `sudo vi /etc/chrony.conf`
2. Comment out any default `pool` addresses by adding `#` at the beginning:
    `# pool 0.centos.pool.ntp.org iburst `
    `# pool 1.centos.pool.ntp.org iburst`
3. Add the NTP server’s IP address:
    `server 192.168.1.1 iburst`
    (Replace `192.168.1.1` with your actual NTP server's IP)
4. Save and exit (`:wq`).

---
## **Step 4: Open Firewall Ports (on both Server and Client)**
Run the following commands on **both** the server and the client:
`sudo firewall-cmd --add-service=ntp --permanent `
`sudo firewall-cmd --reload`

---
## **Step 5: Start and Enable Chrony**
Enable and start the Chrony service:
`sudo systemctl enable --now chronyd`
Check the service status:
`sudo systemctl status chronyd`

---
## **Step 6: Verify NTP Synchronization**
### **On the Server:**
1. Check if the NTP server is tracking time correctly:
    `chronyc tracking`    
    - This will show details such as the reference time source, delay, and synchronization accuracy.
2. Verify which time sources the server is using:
    `chronyc sources`
    - This will list all the upstream NTP sources.
3. Check the list of clients using the server:
    `chronyc clients`
    - This will display connected client IPs.
### **On the Client:**
1. Verify time synchronization with the server:
    `chronyc tracking`
2. Check which server the client is synchronizing with:
    `chronyc sources`
---
## **Understanding NTP Stratum**
### **What is a Stratum?**
NTP uses a hierarchical structure called **Stratum** to define the reliability of a time source:
- **Stratum 0**: High-precision clocks (e.g., atomic clocks, GPS clocks).
- **Stratum 1**: Servers directly connected to Stratum 0 devices.
- **Stratum 2**: Servers that synchronize with Stratum 1 servers.
- **Stratum 3+**: Additional levels in the hierarchy.
You can check the stratum level using:
`chronyc tracking`
- If the `Reference ID` is a public NTP server, your server is likely at **Stratum 2**.
- If your server is serving clients, it might be at **Stratum 3**.
---
## **Final Validation**
On the **client**, confirm the time is synchronized with the server:
`timedatectl`
If `System clock synchronized: yes`, your setup is working correctly.

---
## **Summary**
1. Install Chrony (`chronyd`) on both server and client.
2. Configure the **server** to allow clients (`allow x.x.x.x` in `/etc/chrony.conf`).
3. Configure the **client** to use the NTP server (`server x.x.x.x` in `/etc/chrony.conf`).
4. Open firewall ports (`firewall-cmd --add-service=ntp`).
5. Start and enable `chronyd` on both machines.
6. Verify synchronization using `chronyc tracking`, `chronyc sources`, and `chronyc clients`.
This ensures accurate timekeeping across your Linux servers. 🚀