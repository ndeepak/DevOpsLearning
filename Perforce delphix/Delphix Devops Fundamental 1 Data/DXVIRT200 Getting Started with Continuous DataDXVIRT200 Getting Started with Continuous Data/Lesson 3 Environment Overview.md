# Environment Overview
Lesson 3 of 7
**Environments** are individual hosts or supported Clusters that are configured to be used with Delphix. We configure the hosts in Delphix by adding them using their host names or IP addresses.
In Delphix, an **Environment** is:
> A **host or supported cluster** that Delphix connects to in order to **read, stage, or provision databases**

Think of an Environment as the **place where databases live or will live**.
**Please note that if using host names, they must be resolvable by the Delphix engine via domain, name system, or DNS**
If Delphix cannot resolve the hostname → **Environment add fails**
![[Pasted image 20251230112621.png]]
Environment Overview
There are three main types of environments: **Source, Staging** and **Target**. 
## Types of Environments (Core Concept)
There are **exactly 3 main environment types**:

|Environment Type|Purpose|
|---|---|
|**Source**|Where production/source databases run|
|**Staging**|Used for recovery and log processing|
|**Target (VDB Target)**|Where VDBs are provisioned|
![[Pasted image 20251230112633.png]]

1.  Source Environment
The Source Environment is the host or cluster on which the instances for the source database run. It contains one or more source databases that are synced with Delphix. The syncing process requires at least one full backup, followed by ongoing incremental backups.
The source environment hosts the databases containing data that we want to virtualize with Delphix, and at times,  works as the production database.
**Key idea**:
> Source = “Where the original data lives”

2.  Staging Environment
The Staging Environment hosts a database instance, using the same version as the source database. It is responsible for recovery of changes on these sources.
The Staging Environment is optional for Oracle databases, whereas it is mandatory for SQL Server and Sybase.
What is it?
- A host that runs a **database instance matching the source version**    
- Used by Delphix to **apply logs and recover changes**
Is it mandatory?

| Database       | Staging Required? |
| -------------- | ----------------- |
| **Oracle**     | ❌ Optional        |
| **SQL Server** | ✅ Mandatory       |
| **Sybase**     | ✅ Mandatory       |
**Exam favorite**:  
Oracle **can skip staging**, SQL Server **cannot**

3.  VDB Target Environment
A Target Environment is a host or cluster that will be used to provision VDBs. This is typically the server where development, testing or similar non-production databases exist. 
In windows, a VDB Target Environment is a host or cluster that will be used to provision VDBs or to act as a validated sync or proxy environment
In Linux or Unix, A VDB Target Environment is an environment to which you plan to provision VDBs.
What is it?
- Where **Virtual Databases (VDBs)** are created    
- Typically **Dev / Test / QA servers**    
OS-specific notes
- **Windows**:  
    Can be VDB target, proxy, or validated sync environment    
- **Linux/Unix**:  
    Used mainly for provisioning VDBs   
**Memory trick**:
> Target = “Where developers work”

---

Source and Target environments can be either standalone or clusters. Standalone environments consist of a single host whereas a cluster typically includes two or more hosts.
## Standalone vs Cluster Environments
Environments can be:

| Type           | Description       |
| -------------- | ----------------- |
| **Standalone** | Single host       |
| **Cluster**    | Two or more hosts |

### Examples
- **SQL Server clusters**    
    - Windows Failover Cluster        
    - Always On Availability Groups        
- **Oracle clusters**    
    - Oracle RAC (Real Application Clusters)        
**Exam trap**:  
RAC is a **cluster type**, NOT an environment type

For example, cluster environments for MS SQL Server databases use windows failover cluster and always on availability groups, while cluster environments for Oracle use Oracle Cluster with Real Application Clusters (RAC).

---
![[Pasted image 20251230112851.png]]
**To add Environments to the Delphix Continuous Data Engine:**
1. Run HostChecker to validate the Source or Target host.    
2. Navigate to the Environments Page of the Delphix Continuous Data Engine by Selecting **Environments** from the **Manage** menu located in the Delphix Engine banner.    
3.  Click on the elipses located next to **Environments** and select **Add Environment** from the drop down menu.  
Always required before adding environments
![[Pasted image 20251230112907.png]]
Host and Server
The **Host and Server** tab of the Add Environment Wizard is where users can select either Unix/Linux or Windows Hosts, and standalone servers or clusters. 
For cluster Oracle RAC environments, select **Cluster** and then enter the following information:
- Environment name
- Cluster Home
- Node Address

Environment Settings
The **Environment Settings** tab is used to enter the Environment name, IP address, SSH port, Login options, and credentials, as well as the toolkit path. **It is important to enter the toolkit path prior to validating the credentials.** Other Environment settings include:
- **Java Development Kit (Optional)** OpenJDK is included in each toolkit and is sent to all Delphix connected environments. Customers who require using Oracle Java may do so by selecting "Provide my own JDK" when adding an environment and then specifying the PATH to the alternate Java Development Kit.
- **NFS Addresses** **(Optional)**:  
    Enter one or more comma-separated IP Address/Hostname. In the case of the Oracle RAC environment, users need to ensure that the NFS Address list includes IP Addresses from all the cluster nodes.
![[Pasted image 20251230113040.png]]
### Required Fields
- Environment name    
- IP address / hostname    
- SSH port    
- Login credentials    
- **Toolkit path**    
**Critical rule**:
> Toolkit path must be entered **before validating credentials**

Summary
The **Summary** tab offers users the opportunity to review the settings chosen prior to initiating the set up the environment. Changes to the settings can be made by clicking the **Back** button. 
- Review all settings
- Go back if needed
- Click **Submit** to start setup
If satisfied with the settings, click **Submit**.
![[Pasted image 20251230113108.png]]

Actions Tab
Progress can be monitored by viewing the **Running Actions** located on the right side of the UI. If the Actions menu is not visible, Click the **Actions** button in the top right hand side of the banner.
Monitoring Progress (Actions Tab)
- View **Running Actions** on the right
- If hidden:
    - Click **Actions** button (top right)
Useful for troubleshooting environment setup issues
![[Pasted image 20251230113129.png]]

---
Knowledge Check

There are 3 main types of Environments (choose all that apply)
- Source    
- RAC    
- Staging    
- Target

## Exam Summary
- **3 environment types only**: Source, Staging, Target
- Staging:
    - Optional for Oracle
    - Mandatory for SQL Server & Sybase
- RAC = cluster, NOT environment
- Toolkit path must be set **before credential validation**
- DNS resolution is critical when using hostnames