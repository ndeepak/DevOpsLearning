### Wazuh Deployment Using Docker
#### Introduction
Wazuh is an open-source security platform that provides unified SIEM (Security Information and Event Management) and XDR (Extended Detection and Response) capabilities. Deploying Wazuh using Docker simplifies the setup process, supports single-node or multi-node configurations, and ensures secure communication between components.

---
### Deployment Options
1. **Single-node Deployment:**
    - One Wazuh manager, indexer, and dashboard.
    - Suitable for small environments.
2. **Multi-node Deployment:**    
    - Two Wazuh manager nodes (master and worker), three indexer nodes, and one dashboard.
    - Provides high availability and scalability.

---
### Single-Node Deployment Steps
1. **Clone the Wazuh Docker Repository:**
```
git clone https://github.com/wazuh/wazuh-docker.git -b v4.10.1
cd wazuh-docker/single-node
```
2. **Generate Certiftes (Self-signed or Custom):**  
    To secure communication between nodes, certificates are required.  
    Use Wazuh's cert generator image:
```
# generate-indexer-certs.yml
version: '3'
services:
  generator:
    image: wazuh/wazuh-certs-generator:0.0.2
    hostname: wazuh-certs-generator
    volumes:
      - ./config/wazuh_indexer_ssl_certs/:/certificates/
      - ./config/certs.yml:/config/certs.yml
```        
**Run Command to Generate Certificates:**
    `docker-compose -f generate-indexer-certs.yml run --rm generator`
3. **Place Certificates:**
    - For indexer: `config/wazuh_indexer_ssl_certs/`
    - For manager: `config/wazuh_indexer_ssl_certs/root-ca-manager.pem`
    - For dashboard: `config/wazuh_indexer_ssl_certs/root-ca.pem`
4. **Start the Deployment:**
    - Foreground:
        `docker-compose up`        
    - Background:        
        `docker-compose up -d`        
5. **Access Wazuh Dashboard:**
    - URL: `https://<your-ip>`
    - Default credentials:  
        Username: `admin`  
        Password: `SecretPassword`

---
### Multi-Node Deployment
1. **Clone and Change Directory:**
    `git clone https://github.com/wazuh/wazuh-docker.git -b v4.10.1 cd wazuh-docker/multi-node`
2. **Generate Certificates:** Repeat the process in single-node deployment for multi-node configuration, ensuring correct file placement.
3. **Run Deployment:**
    `docker-compose up -d`

---
### Managing Wazuh Users
#### Change Password for Indexer Users
1. **Generate Password Hash:**
    `docker run --rm -ti wazuh/wazuh-indexer:4.10.1 bash /usr/share/wazuh-indexer/plugins/opensearch-security/tools/hash.sh`
    Copy the generated hash.    
2. **Update Configuration:**
    - Modify `config/wazuh_indexer/internal_users.yml` with the new hash.
    - Update `docker-compose.yml` with the new password for each service.
3. **Restart Deployment:**    
    `docker-compose down docker-compose up -d`

---
### Notes
- Monitor logs for “Failed to connect to Wazuh indexer port 9200” until the indexer is ready.
- Avoid using special characters like `$` or `&` in passwords to prevent deployment issues.
This guide ensures a secure and scalable Wazuh deployment, enhancing system monitoring and threat detection.