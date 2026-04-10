To set up **Zabbix, Grafana, Prometheus, and cAdvisor** under **domain mode** (`monitor.deepaknagarkoti.com.np`) with **Cloudflare wildcard SSL certificates**, follow these steps:

---
## **1️⃣ Prerequisites**
Before proceeding, ensure: ✅ You have **Cloudflare wildcard certificates** (`*.deepaknagarkoti.com.np`).  
✅ Your domain (`monitor.deepaknagarkoti.com.np`) is **pointing to your server's public IP** in **Cloudflare DNS**.  
✅ **Port 443 (HTTPS) is open** in your firewall.

---
## **2️⃣ Create an Nginx Reverse Proxy with SSL**
Since your applications (Zabbix, Grafana, etc.) don’t have built-in HTTPS support, we'll **use Nginx as a reverse proxy**.
### **📝 Create `nginx.conf`**
```
mkdir -p ~/Zabbix_Bundle/nginx
nano ~/Zabbix_Bundle/nginx/nginx.conf
```
**Paste the following:**
```
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        server_name monitor.deepaknagarkoti.com.np;

        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen 443 ssl;
        server_name monitor.deepaknagarkoti.com.np;

        ssl_certificate /etc/nginx/certs/deepaknagarkoti.com.np.crt;
        ssl_certificate_key /etc/nginx/certs/deepaknagarkoti.com.np.key;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        location / {
            root /usr/share/nginx/html;
            index index.html;
        }

        location /zabbix/ {
            proxy_pass http://zabbix-web:8080/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /grafana/ {
            proxy_pass http://grafana:3000/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /prometheus/ {
            proxy_pass http://prometheus:9090/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /cadvisor/ {
            proxy_pass http://cadvisor:8081/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

---

## **3️⃣ Update `docker-compose.yml`**
Now, modify `docker-compose.yml` to include the **Nginx reverse proxy**.
### **📝 Edit `docker-compose.yml`**
```
version: '3.8'

networks:
  zabbix_network:
    driver: bridge

volumes:
  postgres-data:
  prometheus-data:
  grafana-data:
  nginx-certs:

services:
  postgres:
    image: postgres:16
    container_name: postgres
    restart: always
    networks:
      - zabbix_network
    environment:
      POSTGRES_USER: zabbix
      POSTGRES_PASSWORD: zabbix
      POSTGRES_DB: zabbix
    volumes:
      - postgres-data:/var/lib/postgresql/data

  zabbix-server:
    image: zabbix/zabbix-server-pgsql:7.0.10-ubuntu
    container_name: zabbix-server
    restart: always
    networks:
      - zabbix_network
    depends_on:
      - postgres
    environment:
      DB_SERVER_HOST: postgres
      POSTGRES_DB: zabbix
      POSTGRES_USER: zabbix
      POSTGRES_PASSWORD: zabbix

  zabbix-web:
    image: zabbix/zabbix-web-nginx-pgsql:7.0.10-ubuntu
    container_name: zabbix-web
    restart: always
    networks:
      - zabbix_network
    depends_on:
      - postgres
      - zabbix-server
    environment:
      ZBX_SERVER_HOST: zabbix-server
      DB_SERVER_HOST: postgres
      POSTGRES_DB: zabbix
      POSTGRES_USER: zabbix
      POSTGRES_PASSWORD: zabbix

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: always
    networks:
      - zabbix_network
    volumes:
      - ./prometheus/config:/etc/prometheus
      - ./prometheus/data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: always
    networks:
      - zabbix_network
    depends_on:
      - zabbix-web
      - prometheus
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/datasources:/etc/grafana/provisioning/datasources
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: admin
      GF_USERS_ALLOW_SIGN_UP: "false"
    entrypoint: >
      /bin/bash -c "
      grafana-cli plugins install alexanderzobnin-zabbix-datasource;
      /run.sh"

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    restart: always
    networks:
      - zabbix_network
    ports:
      - "8081:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /sys:/sys:ro
      - /var/lib/docker:/var/lib/docker:ro

  nginx:
    image: nginx:latest
    container_name: nginx
    restart: always
    networks:
      - zabbix_network
    depends_on:
      - zabbix-web
      - grafana
      - prometheus
      - cadvisor
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
```

---
## **4️⃣ Add SSL Certificates**
Move your Cloudflare SSL certificates into the `certs` directory.
```
mkdir -p ~/Zabbix_Bundle/certs
cp origin_ca_ecc_root.pem deepaknagarkoti.com.np.crt ~/Zabbix_Bundle/certs/
cp deepaknagarkoti.com.np.key deepaknagarkoti.com.np.pem ~/Zabbix_Bundle/certs/
```

---
## **5️⃣ Deploy the Containers**
Run the following:
`docker-compose down -v `
`docker-compose up -d --build`

---
## **6️⃣ Verify the Setup**
### **🔹 Test HTTPS:**
`curl -k https://monitor.deepaknagarkoti.com.np/zabbix/`
Expected response: **Zabbix Login Page HTML**.
### **🔹 Check Nginx Logs**
`docker logs nginx -f`
### **🔹 Verify SSL**
`openssl s_client -connect monitor.deepaknagarkoti.com.np:443 -servername monitor.deepaknagarkoti.com.np`
You should see a valid **SSL certificate chain**.

---
## **7️⃣ Access the Services**
✅ **Zabbix:** https://monitor.deepaknagarkoti.com.np/zabbix/  
✅ **Grafana:** https://monitor.deepaknagarkoti.com.np/grafana/  
✅ **Prometheus:** https://monitor.deepaknagarkoti.com.np/prometheus/  
✅ **cAdvisor:** https://monitor.deepaknagarkoti.com.np/cadvisor/

---
### 🎯 **Done! Now you have a fully secure domain-based monitoring setup.** 🚀🔥