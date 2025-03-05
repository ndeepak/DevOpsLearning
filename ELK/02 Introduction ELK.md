Structure:
1. ElasticSearch
2. Logstash
3. Kibana
4. Data Pipelines

- Elasticsearch: How data is stored and indexed. Working with JSON documents.
- Logstash: How to collect and manipulate structured and unstructured data.
- Kibana: Techniques for searching data and building useful visualizations and dashboards.
- Beats: Use the agent to ship data from endpoints and servers to your ELK systems.
* Building Data Pipelines: Handling various security logs (HTTP proxy, Windows Events, NetFlow, IDS alerts, etc.).


# Network Security Monitoring (NSM)
* is the collection, detection and analysis of security data.
NSM Cycle
## Collection
* Quantify Risk
* Deploy Sensors 
* Setup Logging

## Detection
* Signature IDS
* Anomaly IDS
* Hunting

## Analysis
* Host Forensics
* Network Forensics
* Malware Analysis

## Applied Collection Framework
1. Define Threats
* A threat is a party with the capabilities and intentions to exploit a vulnerability in an asset.
* What is your worst fear?
	* Online Retainer?
		* Downtime
	* Lawyer?
		* Stolen Client Data
	* Utility? (Business/Electricity/Water/Fire/Powergrid/Plant/)
		* Data Integrity
		* Downtime
* Translate business threats to technical threats
	* What devices interact with sensitive data?
	* How does sensitive data traverse the network?
	* What users interact with sensitive data?
	* What paths are available to access the data?
	* What types of threat actors would be interested in attacking my network?
* Threats (Pharma Company)
	* Web Server Defacement
	* Research File Server Compromise
	* Research Database Server Compromise
	* Data Exfil by a Disgruntled Employee

2. Quantify Risks
* How much risk does each threat represent?
* Impact (I) * Probability (P) = Risk (R)
![[impactrisk.png]]


3. Identify Evidence Sources
* If the threat manifests, where would you find the evidence of an attack?
	* Network Based
		* File Server VLAN - FPC Data
		* File Server VLN - Session Data
		* Edge Router - Firewall logs
	* Host-based
		* Server Authentication Logs
		* Antivirus Alert data
		* Windows Process Execution Logs

4. Narrow Focus
* How can i optimize what i'm collecting?
	* PCAP
		* Filter out encrypted traffic
		* Offset FPC collection with bro metadata
	* NIDS
		* Rules focused on protocols in use
		* Rule tunings
	* Windows Logs
		* Focus on useful events IDs
		* Sysmon tuning *whitelist/blacklist*

Summary
* Defensive Security is centered around the tasks of collection, detection and analysis.
* Everything begins with data collection.
* The applied collection framework can be used to figure out what you should be collecting.
* Collection is never finished.






