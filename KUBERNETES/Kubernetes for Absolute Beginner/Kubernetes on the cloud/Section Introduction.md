# Kubernetes on the cloud
Kubernetes on the cloud lets you deploy, manage, and scale containerized applications effortlessly by leveraging managed solutions offered by major cloud providers: Google Cloud Platform (GKE), Amazon Web Services (EKS), and Microsoft Azure (AKS). These platforms abstract much of the infrastructure management, making Kubernetes clusters easier to create, scale, and maintain.
1. Google Cloud Platform
2. Amazon Web Services
3. Microsoft Azure

Kubernetes on the cloud

| Self-Hosted/Turnkey Solutions                    | Hosted Solutions (Managed Solutions)   |
| ------------------------------------------------ | -------------------------------------- |
| You provision VMs                                | Kubernetes as a Service                |
| You configure VMs                                | Provider provision VMs                 |
| You use scripts to deploy cluster                | Provider installs Kubernetes           |
| You maintain VMs yourself                        | Provider maintains VMs                 |
| Example: Kubernetes of AWS using kops or KubeOne | Example: Google Container Engine (GKE) |

**Hosted Solutions**
Google Kubernetes Engine (GKE)
Azure Kubernetes Service (AKS)
Amazon Elastic Kubernetes Service (EKS)


---

## Google Kubernetes Engine (GKE)
GKE is Google’s fully-managed Kubernetes offering, designed for easy deployment and management of containerized apps on Google Cloud.

Prerequisites:
1. Google Cloud Free Tier
2. Creating Kubernetes Cluster
	1. Naming
	2. Location Type and Zones
	3. Master Version
	4. Working Nodes Configurations
3. Managing Kubernetes Cluster
4. Connecting to the Cluster using Cloud Shell
```
gcloud container clusters get-credentials example-voting-app --zone us-central1-c --project example-voting-app-283506

kubectl get nodes
kubectl get pods

git clone https://github.com/kodekloudhub/example-voting-app.git

cd example-voting-app
kubectl create -f voting-app-deploy.yaml
kubectl create -f voting-app-service.yaml
kubectl create -f redis-deploy.yaml
kubectl create -f redis-service.yaml
kubectl create -f postgres-deploy.yaml
kubectl create -f postgres-service.yaml
kubectl create -f worker-app-deploy.yaml
kubectl create -f result-app-deploy.yaml
kubectl create -f result-app-service.yaml

OR
kubectl create -f .

kubectl get deployments, svc
kubectl get all
```

5. Services and Ingress in GCP dashboard

Features include autoscaling, built-in security, integrated monitoring, high availability, rolling updates, rollbacks, and seamless connections with other GCP services.

---
## Amazon Elastic Kubernetes Service (EKS)
Amazon EKS provides a managed Kubernetes environment on AWS, supporting both native AWS integrations and open-source features.
Prerequisities:
1. AWS Account: https://aws.amazon.com/free
2. Installing Kubectl CLI
3. EKS Cluster Role
4. IAM Role for Node Group
5. VPC
6. EC2 Key Pair which can be used to SSH to the worker nodes
7. AWS Basics

**How it works:**
- **Managed Control Plane:** AWS provisions and manages the cluster control plane and worker nodes.
- **Self-Managed Option:** Set up Kubernetes clusters on EC2 instances using tools like kops or KubeOne.
- **Cluster Components:** Control plane, worker nodes (EC2), monitoring with CloudWatch, and autoscaling for dynamic resource allocation.
- **Monitoring & Security:** Built-in log management, extensive integration with AWS security, and scaling tools.

EKS
1. Search for EKS
2. Create EKS Cluster
	1. Name it
	2. Kubernetes Version
	3. Cluster Service Role
	4. VPC
	5. Subnets
	6. Cluster Endpoint access
	7. Review and Create
3. Add node group to the Cluster from Compute Option
	1. Name it
	2. NODE IAM Role
	3. EKSNodeRole
	4. Sunets
	5. SSH Key Pair
	6. Set compute configurations
	7. Set Scaling Configurations
	8. Review and create
4. Check status of node group
5. Installation in the AWS CLI
6. Installation of the kubectl
7. Kubeconfig installation
8. kubectl get nodes

Application Deployment
```bash
git clone https://github.com/kodekloudhub/example-voting-app.git

cd example-voting-app
cd k8s-specifications

kubectl create -f .
kubectl get deployments, svc
kubectl get all
```
---

## Azure Kubernetes Service (AKS)
AKS is Microsoft’s managed Kubernetes offering, allowing teams to run scalable, cloud-native apps with deep Azure integration.

Prerequisities	
1. Azure Account: https:///azure.microsoft.com/en-us/free/free-account-faq
2. Active Subscription
3. Azure Basics

**Key Features:**
- **Managed Infrastructure:** Automated cluster creation, upgrades, and autoscaling.
- **Integration with Azure Services:** AKS works natively with Azure Monitor, Active Directory (for RBAC), Cosmos DB, and Azure Container Registry.
- **DevOps & CI/CD:** GitHub Actions and other DevOps tools integrate directly for streamlined deployment.
- **Security & Compliance:** Multi-layered security, private endpoints for management, and policy enforcement.    
- **Observability:** Azure Monitor provides cluster telemetry and integrates with Prometheus and Grafana for visualization.
AKS supports both Linux and Windows containers, lets you scale quickly across availability zones, and offers advanced networking, security, and monitoring capabilities.
Creating Kubernetes Cluster
1. Naming the cluster
2. In the authentication tab, create a service principal to new.
3. Review and create
4. 
## Summary Table: Hosted Kubernetes Solutions

|Provider|Managed Solution|Key Features|Example CLI Actions|
|---|---|---|---|
|Google Cloud|GKE|Autoscaling, easy upgrades, GCP tools|`kubectl`, `gcloud`|
|AWS|EKS|AWS IAM, EC2 integration, CloudWatch|`kubectl`, AWS CLI|
|Azure|AKS|Azure AD, Monitor, Registry integration|`kubectl`, az CLI|

These cloud solutions make deploying Kubernetes more accessible by handling much of the complexity and letting you focus on your applications and workloads.cloud.google+2​
[references](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview)


Conclusion:
1. Kubernetes Overview
2. Containers Docker
3. Container Orchestration
4. Demo- Setup Kubernetes
5. Kubernetes Concepts  (Pods | ReplicaSets | Deployment | Services)
6. Networking in Kubernetes
7. Kubernetes Management - Kubectl
8. Kubernetes Definition Files - YAML
9. Kubernetes on Cloud - AWS/GCP/Azure


