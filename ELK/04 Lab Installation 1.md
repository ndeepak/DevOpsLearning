# **ELK Stack Lab Setup on Ubuntu Server**
This guide provides a **step-by-step setup** for deploying the **ELK (Elasticsearch, Logstash, Kibana) stack** on **Ubuntu Server**.

---

## **🔹 Lab Architecture**

| Component        | Specification                    |
| ---------------- | -------------------------------- |
| **OS**           | Ubuntu Server                    |
| **Installation** | Native or Virtual Machine        |
| **RAM**          | 4GB                              |
| **Disk Space**   | 40GB                             |
| **Access**       | Kibana Web Interface via Browser |
### **🛠️ Tools**
1. **Elasticsearch** – Stores and indexes logs.
2. **Logstash** – Collects, processes, and forwards logs.
3. **Kibana** – Visualizes and analyzes logs.
https://www.elastic.co/downloads/
---
## **🔹 Prerequisites**
Before installing ELK, ensure you have **Java Runtime Environment (JRE)** installed.
bash
`sudo apt update 
`sudo apt install openjdk-8-jre -y 
`java -version`

Expected Output:
`openjdk version "1.8.0_xxx"`

---
# **🔹 Installing and Configuring ELK Stack**
## **1️⃣ Installing Elasticsearch**
📌 **Download and Install Elasticsearch**
```
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.17.1-amd64.deb
sudo dpkg -i elasticsearch-8.17.1-amd64.deb
```

📌 **Enable and Start Elasticsearch**
```
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
```
📌 **Verify Elasticsearch is Running**
`ps aux | grep elastic 
`curl -X GET "localhost:9200"`

Expected Output:
```
{
  "name" : "your-server-name",
  "cluster_name" : "elasticsearch",
  "version" : {
    "number" : "8.17.1",
    "build_flavor" : "default",
    "build_type" : "deb"
  },
  ...
}
```

---

## **2️⃣ Installing Logstash**
📌 **Download and Install Logstash**
```
wget https://artifacts.elastic.co/downloads/logstash/logstash-8.17.1-amd64.deb
sudo dpkg -i logstash-8.17.1-amd64.deb
```
📌 **Enable and Start Logstash**
```
sudo systemctl daemon-reload
sudo systemctl enable logstash.service
sudo systemctl start logstash.service
```

📌 **Verify Logstash is Running**
`ps aux | grep logstash`

📌 **Test Logstash Connectivity**
`curl -X GET "localhost:9600"`

### **🔧 Logstash Configuration Changes**
📌 **Edit Logstash Configuration**
`sudo nano /etc/logstash/logstash.yml`

Set the following:
`config.reload.automatic: true 
`config.reload.interval: 3`

📌 **Restart Logstash**
`sudo systemctl restart logstash.service`

---
## **3️⃣ Installing Kibana**
📌 **Download and Install Kibana**
```
wget https://artifacts.elastic.co/downloads/kibana/kibana-8.17.1-amd64.deb
sudo dpkg -i kibana-8.17.1-amd64.deb
```
📌 **Enable and Start Kibana**
```
sudo systemctl daemon-reload
sudo systemctl enable kibana.service
sudo systemctl start kibana.service
```

📌 **Verify Kibana is Running**
`ps aux | grep kibana`

### **🔧 Kibana Configuration Changes**
📌 **Edit Kibana Configuration**
`sudo nano /etc/kibana/kibana.yml`

Update the file:
```
elasticsearch.url: "http://localhost:9200"
server.port: 5601
server.host: "192.168.10.250"
```

📌 **Restart Kibana**
`sudo systemctl restart kibana.service`

---

# **🔹 Accessing Kibana**
1. Open your browser.
2. Go to **[http://localhost:5601](http://localhost:5601)** or **http://192.168.10.250:5601**.
3. You should see the Kibana dashboard.

---
## **🔹 Testing Connectivity to Elasticsearch**
📌 **In Kibana DevTools**
1. Go to **DevTools**.
2. Run the command:
    `GET /`
3. Click **Run**.
4. You should see Elasticsearch details.

---
# **✅ Summary**

|Step|Task|
|---|---|
|✅ **Step 1**|Install Java Runtime|
|✅ **Step 2**|Install Elasticsearch and verify connectivity|
|✅ **Step 3**|Install Logstash, configure, and restart|
|✅ **Step 4**|Install Kibana, configure, and restart|
|✅ **Step 5**|Access Kibana Web UI at **[http://localhost:5601](http://localhost:5601)**|
|✅ **Step 6**|Test Elasticsearch in Kibana DevTools|

---
🚀 **You now have a working ELK stack running on Ubuntu Server!** 🚀