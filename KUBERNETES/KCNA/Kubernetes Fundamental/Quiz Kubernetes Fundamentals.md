# Quiz Kubernetes Fundamentals

Why do Docker images continue to work seamlessly in Kubernetes even after the removal of Docker support?
**• Because Docker images adhere to the Open Container Initiative (OCI) standard** 
• Because Kubernetes still supports dockershim
• Because Kubernetes has developed a new container runtime specifically for Docker images
• Because Kubernetes now uses containerd as its default container runtime

Which component in Kubernetes is responsible for making decisions to bring up new containers in response to node, container, or endpoint failures?
• API server.
• Etcd service
• Kubelet service 
**• Controllers**

Which command is used with the CTR command line tool to run a container by specifying the image address?
• ctr execute ‹image address\»›
• ctr start <image address\>
• ctr create <image address\>
**• ctr run <image address\>**


Which of the following is not a benefit of cloud computing?
**• Increased reliance on physical infrastructure**
• Cost-effectiveness _
• Scalability
• Increased flexibility

What is the primary purpose of Docker, distinguishing it from hypervisors?
• Emulating hardware to create virtualized environments
****• Containerizing applications for shipping and running
• Providing a hypervisor-like environment for running multiple VMs
• Virtualizing and running different operating systems

Which of the following is NOT mentioned as a container orchestration technology?
• Kubernetes
**• Containerd |**
• Docker Swarm
• Mesos

What is the benefit of using container runtimes that support the CRI?
**• It provides better compatibility and standardization across container runtimes**
• It enables container runtimes to be developed independently of Kubernetes
• It allows for direct communication between containers
• It enables automatic scaling of container instances

How would you use the CTR command line tool to pull a Redis image?
• ctr images push «address of the redis image>
• ctr images remove «address of the redis image>
**• ctr images pull < address of the redis image\>**
• ctr images build < address of the redis image>

How can you specify a specific runtime endpoint when using the CRI Control tool?
**• Setting the CONTAINER RUNTIME_ENDPOINT environment variable**
• All of the options are correct
**_ Using the -runtime-endpoint command line option**
• Using the -endpoint-runtime command line option

Which of the following is an essential element of cloud native?
• Physical infrastructure
**• Microservices |**
• Monolithic applications
• Manual deployment

Which command can be used to run an instance of MongoDB using Docker?
• docker pull
• docker build
• docker exec
**• docker run**

What is the primary function of a node(Minion) in a Kubernetes cluster?
• Managing container networking within the cluster
• Providing load balancing services to containerized applications
• Running control plane components of Kubernetes
**• Acting as a worker machine where containers are launched**

Who maintains and develops the CRI Control command line utility?
• Red Hat Inc.
• Docker Inc.
**• Kubernetes community _**
• Cloud Native Computing Foundation (CNCF)

What is DevOps?
• A project management methodology that focuses on sequential development and strict timelines
**• A set of practices that promotes collaboration between development and operations teams to manage and scale microservices effectively**
• A development methodology that exclusively focuses on infrastructure management without considering application development
• A modern approach to building and deploying applications that leverages the benefits of cloud computing
• A methodology that views operations as a separate and isolated phase after development is complete

What is the relationship between a container image and a container in containerization?
• A container image is an isolated environment for running containers.
• A container image is a running instance of a container.
**• A container image is a package or template used to create one or more containers.**
• A container image is a set of processes that run within a container.

What is the role of etcd in a Kubernetes cluster?
• It stores all the data used to manage the cluster.
**• All of the options are correct**
• It ensures distributed storage of information across all nodes in the cluster.
• It implements locks to prevent conflicts between the masters.

What is the role of the master node in a Kubernetes cluster?
• Providing load balancing services to containerized applications
**• Orchestrating containers on the worker nodes and overseeing the cluster**
• Managing container networking within the cluster
• Running the containers and executing the workload

What is the role of the Kubelet in a Kubernetes cluster?
• It ensures distributed storage of information across all nodes in the cluster.
**• It is the agent responsible for managing and monitoring containers on each node.**
• It stores all the data used to manage the cluster.
• It acts as the entry point for interacting with the cluster.

Where can you find containerized versions of applications readily available for use?
• Kubernetes Marketplace
• Google Registry
**• Docker Hub**
• GitHub Container Registry

What is the primary role of Kubernetes in containerized environments?
**• Orchestrating the deployment and management of containers in a clustered environment**
• Managing networking configurations for containers
• Providing security measures for containerized applications
• Optimizing resource allocation for individual containers

Which container orchestration technology is known for being a bit difficult to set up and get started, but provides several features to customize the deployment?
• Mesos
**• Kubernetes |**
• Docker Swarm
• None of the options are correct

Which component serves as the entry point for interacting with a Kubernetes cluster?
• Container runtime
• Controllers and schedulers
**• API server |**
• Kubelet service


Which option is used with NerdCTL to specify port mappings and expose ports when running a container?
* -n
* -d
* -d
* **-p**

Which of the following statements) are true?
• Docker containers are lightweight than VMs.
• Docker containers boot up faster than virtual machines.
**• All the answers are correct.**
• Virtual machines consume higher disk space than in containers.

What is containerization?
• Running an application on the cloud
**• Running microservices in their own container**
• Having a separate workspace for each tool
• A set of practices that allows developers to continuously integrate, test, and deploy changes

Which command is used to view information about the Kubernetes cluster?
**• kubectl cluster-info**
• kubectl delete nodes
• kubectl get nodes
• kubectl describe nodes

What is the purpose of dockershim in Kubernetes?
• To provide automatic scaling of Docker containers in Kubernetes
• To allow for direct communication between Docker containers
• To manage container images, containers, and networking in Docker
**• To allow Docker to communicate with Kubernetes without using the CRI**

How do containers differ from virtual machines (VMs) with respect to their operating system (OS) kernel?
^ Containers and VMs do not rely on an OS kernel.
**• Containers share the same OS kernel as the host system, but VMs have their own separate OS kernel.**
/ Containers and VMs both have their own independent OS kernels
**• Containers use the same OS kernel as the host system, while VMs have their own independent OS kernel.**

What is the purpose of the kubectl tool in Kubernetes?
• It is responsible for distributing work or containers across multiple nodes.
• It is used to manage the container runtime on worker nodes.
**• It is used to deploy and manage applications on a Kubernetes cluster.**
• It is used for storing and retrieving data in the etcd store.

Which command is used with NerdCTL to run a container with the name "red" using the "alpine" image?
• nerdctl create --name red alpine
• nerdctl execute --name red alpine
**• nerdctl run --name red alpine**
• nerdctl start --name red alpine

Which of the following features are supported by NerdCTL but are not available in Docker?
• Lazy pulling of images
• P2P image distribution
**• All of the options are correct**
• Encrypted container images

What are containers?
• Virtual machines that emulate entire operating systems
**• Completely isolated and portable environments for running applications**
• Tools used for securely transporting software across networks
• Large storage units used for organizing data

Why was dockershim removed from Kubernetes version 1.24?
• To increase vendor lock-in for Docker users
**• To encourage the use of container runtimes that support the CRI**
• To provide better backwards compatibility with older versions of Kubernetes and Docker
• To reduce compatibility and standardization across container runtimes

Which of the following statements is true about Containerd?
• Containerd is a deprecated technology and no longer used in modern container environments.
**• Containerd is a separate project and a member of Cloud Native Computing Foundation (CNCF).**
• Containerd is a part of Docker and is not a separate project.
• Containerd is a part of Kubernetes and is responsible for container orchestration.

In the context of Kubernetes, what is a cluster?
• A group of containers deployed together
• A collection of control plane components
**• A set of nodes grouped together**
• A network of interconnected nodes

Which container technology does Docker primarily utilize for its containers?
• None of the options are correct
• LXD
**• LXC**
• LXCFS

Which of the following components are typically found on a Kubernetes master node?
**• kube-apiserver, etcd store, controllers, and scheduler**
• Docker, CRI-O, and rkt
• Kubelet and container runtime
• All of the options are correct

Which command is commonly used with kubectl to deploy an application on a Kubernetes cluster?
• kubectl delete
• kubectl get 
**• kubecti run**
• kubectl describe

What is the term used to describe the automated process of deploying and managing containers, including managing connectivity and scaling based on workload?
• Containerization
**• Container orchestration**
• Container virtualization
• Container networking

What is Cloud Native?
**• A modern approach to application development and deployment that embraces the advantages of cloud computing, harnessing its distributed computing capabilities to build and run applications effectively**
• A model that requires users to have their own physical infrastructure or resources
• A model that involves hosting applications on public clouds exclusively, without considering private or hybrid cloud options
• A legacy approach to building and deploying applications that relies on on-premises infrastructure

What is the purpose of the CTR command line tool that comes with ContainerD?
**• It is solely made for debugging containerD and supports a limited set of features.**
• It is used for deploying and managing containers on a Kubernetes cluster.
• It is a specialized tool designed for container introspection and analysis, providing advanced performance profiling and resource utilization metrics.
• It is a user-friendly tool for debugging containerD and supports a wide range of features.

Which of the following statements accurately describes the purpose of the crictl tool?
• It is a graphical user interface tool for container management.
**• It is primarily used for inspecting and debugging container runtimes.**
• It is built specifically for ContainerD.
• It is used to create and manage containers across different container runtimes.

Which component in Kubernetes is responsible for distributing containers across multiple nodes?
• Kubelet service
**• Scheduler**
• API server
• Etcd service 

Which of the following components are installed when setting up Kubernetes on a system?
• Container runtime
• Kubelet service
• API server and etcd service
**• All of the options are correct**


Which statement accurately describes the container runtime used with Kubernetes?
• The container runtime is always Docker.
• The container runtime can only be Docker or Podman.
**• The container runtime used with Kuberetes can vary, with Docker being a common option.**
• The container runtime is determined by the operating system and cannot be changed.

What is the Container Runtime Interface (CRI) in Kubernetes?
**• A plugin interface that enables any container vendor to work as a container runtime for Kubernetes**
• A container runtime developed by Kubernetes for Docker containers only |
• A Kubernetes feature that allows for direct communication between containers
• A Kubernetes feature that enables automatic scaling of container instances

When using Docker on an Ubuntu operating system, based on which of the following distributions can you run a container?
* **All of the options are correct**
* Debian
* Fedora
* CentOS

