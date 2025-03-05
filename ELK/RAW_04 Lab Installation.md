Lab Architecture
* OS: Ubuntu 16 Server
* Virtual Machine or Native Installation
* RAM: 4GB
* Disk: 40GB
* Everything Installed Natively
* Accessing Kibana Web Interface via browser

Tools
* Elasticsearch
* Logstash
* Kibana

Tasks
* Install each tool
* Test Each tool
* Configure them to launch automatically

Prerequisites
* Java runtime environment
	* sudo apt install openjdk-8-jre
---
### Installing Elasticsearch
https://www.elastic.co/downloads/elasticsearch
```
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.17.1-amd64.deb
sudo dpkg -i elasticsearch-8.17.1-amd64.deb
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service
ps aux | grep elastic

curl -XGET localhost:9200
``` 

---
### Installing Logstash
```
wget https://artifacts.elastic.co/downloads/logstash/logstash-8.17.1-amd64.deb
sudo dpkg -i logstash-8.17.1-amd64.deb
sudo systemctl daemon-reload
sudo systemctl enable logstash.service
sudo systemctl start logstash.service


ps aux | grep logstash

curl -XGET localhost:
```
Configurations changes:
ls /etc/logstash/
sudo nano /etc/logstash/logstash.yml
`config.reload.automatic: true`
`config.reload.interval: 3`

`sudo systemctl restart logstash.service


---
### Installing Kibana
```
wget https://artifacts.elastic.co/downloads/kibana/kibana-8.17.1-amd64.deb
sudo dpkg -i kibana-8.17.1-amd64.deb

sudo systemctl daemon-reload
sudo systemctl enable kibana.service
sudo systemctl start kibana.service

ps aux | grep kibana
```

Configurations changes:
sudo nano /etc/kibana/kibana.yml
```
elasticsearch.url: "http://localhost:9200"
server.port: 5601
server.host: "192.168.10.250"
```

`sudo systemctl restart kibana.service`

Surf the kibana to http://localhost:5601
Test connectivity to elastic search:
* go to DevTools
* Run the default script
* GET /
* Run
---


