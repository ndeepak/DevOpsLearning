# **ELK for Security Analysis - Notes**
## **1. Introduction to ELK Stack**
### **What is ELK?**
The ELK Stack consists of:
- **Elasticsearch** – A distributed search and analytics engine.
- **Logstash** – A data processing pipeline that ingests logs and sends them to Elasticsearch.
- **Kibana** – A visualization and analytics tool for Elasticsearch data.

### **Use Case in Security**
- **Centralized Logging**: Collect logs from multiple sources.
- **Real-Time Threat Detection**: Identify anomalies using security event logs.
- **SIEM (Security Information and Event Management) Integration**: Analyze logs for intrusion detection.

---
## **2. ELK Installation & Lab Setup**
### **Lab Configuration**
- Use **Linux (Ubuntu 22.04, CentOS 8, or Security Onion)** for installation.
- Allocate **4GB+ RAM** for smooth operation.
### **Installing ELK 8 (Latest Version)**
#### **Step 1: Install Elasticsearch**
```
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.x-linux-x86_64.tar.gz
tar -xzf elasticsearch-8.x-linux-x86_64.tar.gz
cd elasticsearch-8.x
./bin/elasticsearch
```
- Default port: `9200`
- Verify:
`curl -X GET "http://localhost:9200"`

#### **Step 2: Install Logstash**
```
wget https://artifacts.elastic.co/downloads/logstash/logstash-8.x-linux-x86_64.tar.gz
tar -xzf logstash-8.x-linux-x86_64.tar.gz
cd logstash-8.x
./bin/logstash -f /path/to/config.conf
```
- Example **Logstash Config (`logstash.conf`)**:
```
input {
  file {
    path => "/var/log/syslog"
    start_position => "beginning"
  }
}
filter {
  grok {
    match => { "message" => "%{SYSLOGTIMESTAMP:timestamp} %{WORD:loglevel} %{GREEDYDATA:message}" }
  }
}
output {
  elasticsearch {
    hosts => ["http://localhost:9200"]
    index => "syslog-logs"
  }
}
```

#### **Step 3: Install Kibana**
```
wget https://artifacts.elastic.co/downloads/kibana/kibana-8.x-linux-x86_64.tar.gz
tar -xzf kibana-8.x-linux-x86_64.tar.gz
cd kibana-8.x
./bin/kibana
```
- Default port: `5601`
- Open `http://localhost:5601` in a browser.
---
## **3. Working with Elasticsearch**
### **Basic CRUD Operations**
#### **Create an Index**
`curl -X PUT "localhost:9200/security-logs"`
#### **Insert Data**
```
curl -X POST "localhost:9200/security-logs/_doc/1" -H 'Content-Type: application/json' -d'
{
  "timestamp": "2024-02-05T10:00:00",
  "loglevel": "ERROR",
  "message": "Unauthorized access attempt detected"
}'
```

#### **Search Data**
`curl -X GET "localhost:9200/security-logs/_search?pretty"`

---
## **4. Processing Logs with Logstash**
### **Common Logstash Pipelines**
- **Syslog Logs**
- **Firewall Logs (UFW, iptables)**
- **IDS/IPS Logs (Suricata, Zeek)**
- **Windows Event Logs**

Example: **Parsing Firewall Logs**
```
input {
  file {
    path => "/var/log/ufw.log"
    start_position => "beginning"
  }
}
filter {
  grok {
    match => { "message" => "%{SYSLOGTIMESTAMP:timestamp} %{WORD:action} %{IP:src_ip} -> %{IP:dest_ip}" }
  }
}
output {
  elasticsearch {
    hosts => ["http://localhost:9200"]
    index => "firewall-logs"
  }
}
```

---
## **5. Searching and Visualizing in Kibana**
### **Basic Kibana Features**
- **Discover Page**: View raw logs.
- **Search Logs**: Use `loglevel: ERROR` to filter.
- **Create Dashboards**: Combine multiple visualizations.

### **Building a Security Dashboard**
1. Create a **Data Table** for failed login attempts.
2. Use **Pie Charts** for log categories.
3. Build a **Line Chart** for attack trends.

---
## **6. Security Data Pipelines**
### **Firewall Logs (UFW, iptables)**
- Track blocked connections.
- Identify brute-force attempts.
### **Zeek Logs (Network Traffic Analysis)**
- Monitor HTTP, DNS, SSH traffic.
- Detect anomalies.
### **Suricata IDS Alerts**
- Capture **intrusion detection alerts**.
- Generate threat intelligence dashboards.

---

## **7. Additional Security Enhancements**
### **Integrating Security Tools**
- **Security Onion**: Pre-configured ELK stack for security monitoring.
- **Wazuh**: SIEM integration for endpoint security.
- **Auditbeat & Filebeat**: Lightweight agents for log collection.

### **Best Practices**
- **Enable SSL/TLS** for secure communication.
- **Use Role-Based Access Control (RBAC)** for user management.
- **Set up Alerting** for real-time notifications.

---

## **8. Conclusion**
### **Next Steps**
- Deploy ELK in a **production** security environment.
- Automate log analysis with **machine learning**.
- Explore **SIEM solutions** for advanced threat detection.