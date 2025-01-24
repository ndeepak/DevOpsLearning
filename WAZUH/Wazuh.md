### Wazuh: Open Source Security Platform
Wazuh is an open-source platform that provides **unified security monitoring** for threat detection, compliance management, and incident response across various environments.

---
#### 1. **Components of Wazuh**
- **Wazuh Manager**: Analyzes data from agents and external devices.
- **Wazuh Agent**: Deployed on monitored endpoints to collect security data.
- **Elastic Stack**: Used for data storage, analysis, and visualization (Elasticsearch, Logstash, Kibana).
- **Filebeat**: Collects and ships logs from Wazuh to Elasticsearch.

---
#### 2. **Installing Wazuh**
##### **Step 1: System Requirements**
- **Operating System**: Ubuntu 20.04/22.04, CentOS/RHEL 8.
- **Memory**: Minimum 4GB RAM for small installations.
- **CPU**: Minimum 2 cores.
##### **Step 2: Installation Steps for All-in-One Setup**
1. **Update Packages**
    `sudo apt update && sudo apt upgrade -y`
2. **Add Wazuh Repository**
```
curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | sudo apt-key add -
echo "deb https://packages.wazuh.com/4.x/apt/ stable main" | sudo tee /etc/apt/sources.list.d/wazuh.list
sudo apt update
```
3. **Install Wazuh Manager**
    `sudo apt install wazuh-manager`
4. **Install Filebeat**
    `sudo apt install filebeat`
5. **Configure Filebeat**
    - Enable Wazuh module:
        `sudo filebeat modules enable wazuh`
    - Set the correct configuration in `/etc/filebeat/filebeat.yml`:
        `output.elasticsearch:   hosts: ["localhost:9200"]`
6. **Install and Configure Elasticsearch**
    - Download and install from [Elasticsearch official site](https://www.elastic.co/downloads/elasticsearch).
    - Start the service:        
        `sudo systemctl start elasticsearch`
7. **Install Kibana**
    `sudo apt install kibana && sudo systemctl start kibana`
8. **Connect Kibana to Elasticsearch** Edit `/etc/kibana/kibana.yml`:
    `server.port: 5601` 
    `elasticsearch.hosts: ["http://localhost:9200"]`
9. **Start Wazuh Manager**
	`sudo systemctl start wazuh-manager`
10. **Enable services on boot**
    `sudo systemctl enable wazuh-manager filebeat elasticsearch kibana`
---
#### 3. **Accessing Wazuh Dashboard**
- Navigate to `http://<your-server-ip>:5601` in your browser.
- Use the Kibana interface with Wazuh installed for security event visualization.
---
#### 4. **Adding Wazuh Agents**
1. Install the agent on the desired endpoint:
```
curl -s https://packages.wazuh.com/4.x/apt/ stable main | sudo apt-key add -
sudo apt install wazuh-agent
```   
2. **Register the Agent** with the manager by editing `/var/ossec/etc/ossec.conf` on the agent machine:
```
<client>
  <server>
    <address>YOUR_MANAGER_IP</address>
    <port>1514</port>
  </server>
</client>
```
3. **Start the agent**:
```
sudo systemctl start wazuh-agent
sudo systemctl enable wazuh-agent
```
---
#### 5. **Useful Commands**
- **Check Wazuh Manager Status**:
    `sudo systemctl status wazuh-manager`
- **Restart Wazuh Manager**:
    `sudo systemctl restart wazuh-manager`
- **Check Agent Logs**:    
    `tail -f /var/ossec/logs/ossec.log`
---
#### 6. **Using Wazuh for Security Monitoring**
- **Intrusion Detection**: Monitors system logs, file integrity, and vulnerabilities.
- **Compliance**: Automates checks for standards like PCI-DSS and GDPR.
- **Active Response**: Configurable automatic responses to threats.

---
#### 7. **Best Practices**
- Regularly update Wazuh and Elastic Stack components.
- Limit access to the Wazuh Manager and Kibana dashboards.
- Configure SSL/TLS for secure communication between agents and the manager.
Wazuh provides a robust foundation for centralized security monitoring, helping enhance visibility and automate security operations.