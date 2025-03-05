# **📌 Log Management**

### **Why is Log Management Important?**
Security investigations depend on logs because they provide insight into system activities, potential attacks, and incidents. Effective log management ensures logs are:
1. **Centralized** – Collected in one place.
2. **Normalized** – Structured in a standard format.
3. **Filtered** – Unnecessary data is removed.
4. **Indexed** – Logs are organized for fast searching.
5. **Searchable** – Easy to query logs for security events.

### **Example: Log Management Process**
- Collect logs from multiple sources (**firewalls, web servers, authentication logs**).
- Use **Logstash/Filebeat** to filter and normalize logs.
- Store logs in **Elasticsearch** with proper indexing.
- Use **Kibana** to search logs and detect security incidents.

---

# **📌 ELK / Elastic Stack Components**
**Motto:** _"Reliably and securely take data from any source, in any format, and search, analyze, and visualize it in real-time."_
ELK is composed of three major components: **Elasticsearch, Logstash, and Kibana**. Each serves a unique purpose in log management.

---
## **1️⃣ ElasticSearch – Data Storage & Search**
### **🔹 What is ElasticSearch?**
- A **database** designed for storing **JSON documents** (log data).
- Uses **Lucene (inverted index)** for fast searching.
- Supports **full-text search, aggregations, and data transformations**.
- **Distributed and scalable** – can handle large datasets.
- Exposes **RESTful APIs** for interaction.

### **🔹 ElasticSearch in Action**
#### **Check if ElasticSearch is running**
`curl -X GET "http://localhost:9200"`

#### **Create an Index (Storage for Logs)**
`curl -X PUT "localhost:9200/security-logs"`

#### **Insert Log Data**
```
curl -X POST "localhost:9200/security-logs/_doc/1" -H 'Content-Type: application/json' -d'
{
  "timestamp": "2024-02-05T10:00:00",
  "loglevel": "ERROR",
  "message": "Unauthorized access attempt detected"
}'
```

#### **Search Logs**
`curl -X GET "localhost:9200/security-logs/_search?pretty"`

---
## **2️⃣ Logstash – Data Ingestion & Processing**
### **🔹 What is Logstash?**
- **A data processing pipeline** that collects logs from various sources.
- **Parses and normalizes** log data into a structured format.
- **Filters out unnecessary data** (e.g., debug logs).
- **Forwards processed logs** to Elasticsearch for storage.

### **🔹 Logstash Pipeline Example**
#### **Logstash Configuration File (`logstash.conf`)**
```
input {
  file {
    path => "/var/log/auth.log"
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
    index => "auth-logs"
  }
}
```

#### **Start Logstash**
`logstash -f logstash.conf`

---
## **3️⃣ Kibana – Data Visualization & Analysis**
### **🔹 What is Kibana?**
- A **web-based GUI** to interact with Elasticsearch data.
- Uses a **flexible search language** for querying logs.
- Provides **charts, graphs, and dashboards** to visualize logs.
- Helps in **security monitoring and threat detection**.

### **🔹 Kibana Dashboard Example**
1. Open **http://localhost:5601**
2. Go to **Discover** → Load `auth-logs` index.
3. Use search queries:
    `loglevel: ERROR`    
4. Create a **Pie Chart** showing failed login attempts.

---
# **📌 ELK Interaction (How ELK Works)**
1. **Logstash** collects and processes logs from different sources.
2. **Logstash** sends structured logs to **Elasticsearch** for storage.
3. **Kibana** queries and visualizes data from **Elasticsearch**.
### **🔥 Example Use Case: Security Incident Investigation**
💡 **Scenario:** You want to detect **unauthorized SSH login attempts**.

1️⃣ **Collect SSH Logs**
```
input {
  file {
    path => "/var/log/auth.log"
    start_position => "beginning"
  }
}
```

2️⃣ **Parse Failed Login Attempts**
```
filter {
  grok {
    match => { "message" => "Failed password for %{USERNAME:user} from %{IP:ip}" }
  }
}
```

3️⃣ **Store in Elasticsearch**
```
output {
  elasticsearch {
    hosts => ["http://localhost:9200"]
    index => "ssh-failures"
  }
}
```

4️⃣ **Visualize in Kibana**
- Create a **bar chart** showing login failures by IP.
- Use alerts to notify **when login failures exceed 10 per minute**.

---

# **📌 Summary**
### ✅ **Log Management**
- Logs need to be centralized, filtered, and searchable.
- ELK enables efficient log storage and analysis.

### ✅ **ElasticSearch**
- Stores log data.
- Supports full-text searching and aggregations.

### ✅ **Logstash**
- Collects logs from different sources.
- Parses and normalizes data before sending to Elasticsearch.

### ✅ **Kibana**
- Provides a web-based UI to analyze logs.
- Helps detect security threats through visualization.
---
