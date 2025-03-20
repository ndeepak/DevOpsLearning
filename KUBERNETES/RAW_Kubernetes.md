What is kubernetes?
Kubernetes is an orchestrator for containerized applications
kubernetes is a data Centre OS.


History of Kubernetes
* Kubernetes came out of Google. It was open sourced on 2014 and handed over to "Cloud Native Computing Foundation (CNCF)".'
* Google has been running many of it's systems on containers for years even before Docker came along.
* Google goes through billions of containers per week for applications like Gmail, Google Search, GFS (Google File System) .. etc. Lots of containers huh??
* Kubernetes is written in Go (Golang)
* Logo - Meaning "the person who steers the ship"
* Kubernetes short name as K8S.
* Borg(Proprietary) --> Omega(Proprietary) --> Kubernetes



Container World Challenges
Application Deployment & Operational Challenges:
* Fail over if one or more nodes experience on outage
* Scale-up and Scale-down: ability to add or remove containers based on application demand
* Zero downtime releases (ZDR)
* Application updates & rollbacks
* Health checks & self healing systems
	* Networking after scaling and self healing, logs, alerting, etc.
* Traffic routing and Load Balancing (LB), and more.


What is an Orchestrator?
* Orchestrator is a system that performs below without you having to supervise.
	* Deploy the application
	* Scale it up and down
	* Performs rolling updates
	* Rollbacks

Kubernetes advantage:
* All these we can achieve with declarative configurations.
* Declare desired state of the system rather than executing a series of instruction.
*Example*
* Declare how many containers, replicas are required for your application (replicas = 3)
* It's not about just creating replicas, but it will continuously monitor to ensure the desired state.

#### Orchestrator Analogy
![[orchestrator_analogy.png]]

Football team is made of individuals
* No two are same
* Each has different role to play in the team
* Some defend, some attack, some are great at passing
* Some are great at shooting
* LW/RW-wingers, LB/RB-backs, AM-attacking mid fielder

- Coach gives everyone a position and organizes them into a team with purpose
- Coach makes sure that team maintain the formation and stick to the plan

In the sports world, we call this coaching. In the application world, we call it orchestration.


In application world,
* some server web pages
* some do authentication
* some do searches
* some do store data
Kubernetes comes along a bit like the coach in the football analogy, and organizes everything into a useful app and keeps things running smoothly.


Kubernetes Cluster
* The cluster is made up of one or more Masters, and a bunch of nodes.
* You might have K8S cluster with 10 nodes to run your production application.
* Behind the scenes each node is running docker as its's container runtime.
* This means, that Docker is the low-level technology that starts, stop containers, etc.
* and k8s looks after big picture things like.. deciding when to scale up or down, update, rollback, etc.

* Kubernetes abstracts the runtime
* container runtime can be 'docker' or containerD'
* ContainerD is overtaking docker
* ContainerD is stripped-down version of docker.
* Abstraction: facilitated by container runtime interface using which you can integrate 3rd party container runtime. thanks cri


Kubernetes VS Docker Swarm
* Orchestrator
	* Docker swam
	* Mesosphere's DCOS
	* Kubernetes
* During 2016 and 2017 Orchestrator wars, kubernetes WON with active deployment and market share.

What is an Data Centre OS?
* Sometimes we call K8s as Data Centre OS
* In modern Data Centre architectures, we are abandoning traditional view of data centre as collection of computers. Insteadm
* we are viewing it as a single large computers. What does that mean?

To understand that in better way, look at this example.
* A typical computer is a collection of CPU, RAM, Storage and Networking.
* Having OS, for example, its's rare for a developer to take care which CPU core or exact memory address their application uses.
* We let the OS decide all of that! Means it abstracts away all of the CPU, Memory details.

* Now, apply this same abstraction to data center resources.
* A typical data center is collection of computers. In modern data center architecture, we view the data center as just a pool of compute, network and storage.
* This means we no longer need to care about which server or LUN our containers are running on just leave this up to the data center OS.
* Gone are the days of taking your app and saying "run this part of the app on this node, with this ip, on this specific LUN.."
* In the cloud native kubernetes world, we are more about saying 'hey kubernetes, i have got this app and it consists of these parts. just run it for me please/'
* kubernetes then goes off and does all the hard scheduling and orchestration works.

Analogy
* think about the process of sending goods via courier services:
	* You need to only package and put a label on it.
	* rest of the complex logistics like which plane, truck, drivers will be taking care by the courier service providers.
	* kubernetes just does the same in data center.

Conclusion
* you develop your application with docker and then use k8s to run/orchestrate it.
* use k8s to run your containerized app in test or production with orchestrator capabilities such as deploy, scale up, down, updates and roll back without much supervision.
* k8s and docker are complimentary technologies
* we integrate docker and k8s to package the application code with dependencies and run the application on production or test.
* k8s is a data center os (os for dev & k8s for dc.)
