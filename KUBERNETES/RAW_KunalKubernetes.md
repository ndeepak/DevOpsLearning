
Systems
Servers
Docker
Containerization


Configurations Management
Immutability, previously and now for virtual machines and containers
--> reliability, security, 

Configurations Management tools: Chef, puppet, etc
Infrastructure as a Code structure

Multiple services in one server, like different version of services required, like python3.1, 3.2 and more.
Package management
--> then comes containers

Managing Containers


Application Structures
* Monolithic Applications Architecture
	* Website: 
	1. Frontend
	2. Backend
	3. Databases
	4. Messages
	5. Networking
	* Bundle all together in one server or similar
	* Problems with monolithic applications
	* deployments issues
	* scaling issues
	* design problems

* Microservices Application Architecture
	* Deployed as individuals applications
	* Frontend as single 
	* backend as server1
	* database as server2
	* message as server3
	* networking as other
	* scaling easy
	* designs 
	* dependencies problem solutions
	* advantages

* Fault Isolations

How to manage containers?
How to communicate with each other?

**note: Services Meshes

Orchestrators --> help us in deploying and managing dynamically
* Deploy
* zero down time
* update and scale
* self healing

Cloud Native Applications... run modern business demands applications, definitions
Cloud computing vs cloud native applications



History: 
Aws offered cloud
openstack.. its down
Google container use, borg, omega,

Google made k8s, open sourced it and donated to CNCF in 2018.
OS of cloud or datacenter.


Docker VS Kubernetes

CRI, Container Runtime Interface --> containerd

Architecture of Kubernetes
Kubernetes Cluster --> control plane (master) + Nodes (worker nodes)

kubectl command --> master manages the worker nodes, 

Kubectl --> kubernetes command line tool

Declarative way --> manifest files, YAML file, commands and all
Imperative way --> 