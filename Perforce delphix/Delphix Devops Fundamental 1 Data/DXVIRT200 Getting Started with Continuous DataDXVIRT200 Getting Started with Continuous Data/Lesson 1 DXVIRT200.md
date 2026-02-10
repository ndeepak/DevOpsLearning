# Lesson 1
## 1. What this course is about (DXVIRT200)
This course is designed to help you understand **how the Delphix Continuous Data Engine works**, why it exists, and how it fits into the **Delphix DevOps Data Platform**.
Before doing hands-on administration, you must understand:
- Core concepts (dSource, VDB, Timeflow)    
- How data is ingested, stored, and shared    
- How Delphix supports DevOps and data management    
This lesson sets the **foundation** for everything that comes later.

---

## 2. Delphix DevOps Data Platform – Big Picture
The **Delphix DevOps Data Platform** consists of four main components:
1. **Continuous Data Engine (CDE)**    
    - Core engine for ingesting, virtualizing, replicating, and sharing data        
2. **Continuous Compliance Engine (CCE)**    
    - Used for masking and securing sensitive data (PII, PCI, PHI)        
3. **Delphix Self-Service**    
    - Allows developers and testers to manage data themselves (being deprecated)        
4. **Data Control Tower (DCT)**    
    - Central orchestration, automation, and governance layer for multiple engines       
In this course, the **main focus is the Continuous Data Engine**.
---
## 3. What the Continuous Data Engine does
The **Continuous Data Engine** is a data management engine that:
- Connects to source systems    
- Ingests data efficiently    
- Keeps data synchronized    
- Creates virtual copies for non-production use   
### Supported data sources
It can connect to
- RDBMS databases:    
    - Oracle        
    - PostgreSQL        
    - MS SQL Server        
    - Sybase ASE        
- Flat files:    
    - Application binaries        
    - Configuration files        
    - Content files        
---
## 4. Data ingestion: How Delphix stores data
### Initial ingestion
- Delphix takes a **full readable and writable copy** of the source database    
- Data is **compressed**, usually to about **1/3 of its original size*
### Ongoing synchronization
- After initial ingestion:    
    - Delphix stays connected to the source        
    - Only **changed data blocks** are ingested        
    - No repeated full copies        
### dSource
- This continuously updated collection of data blocks is called a **dSource**    
- A dSource represents the **source database inside Delphix**    

---
## 5. Virtual Databases (VDBs)
### What is a VDB?
A **Virtual Database (VDB)** is:
- A read-write virtual clone of a dSource (or another VDB)    
- Provisioned instantly    
- Extremely space-efficient    
### How VDBs work
- VDBs share data blocks with the dSource    
- Only **new changes** are written as new compressed blocks    
- This dramatically reduces storage usage    
### Key VDB capabilities
- Provisioned from:    
    - Any snapshot        
    - Any point in time        
- Can be:    
    - Refreshed        
    - Rewound        
    - Recreated        
- Used for:    
    - Development        
    - Testing        
    - QA        
    - Reporting        

---
## 6. Timeflow (very important concept)
- Delphix maintains a **Timeflow**    
- A Timeflow is a **timeline of the database**    
    - Snapshots        
    - Log changes        
- It allows you to provision or refresh VDBs:    
    - To **any point in time**        
    - Even down to a transaction boundary        

This is one of Delphix’s most powerful features.

---
## 7. Synchronization methods
Delphix keeps data in sync using:
- Native database replication:    
    - Oracle Data Guard        
    - SQL Server log shipping        
    - PostgreSQL replication        
- Or incremental backups    

Synchronization frequency is controlled by **user-defined policies**.

---
## 8. Masking and Compliance (context only)
Although this course does not deep-dive into the **Continuous Compliance Engine**, it is important to know:
- In real environments:    
    - Data is often **masked first**        
    - Then VDBs are provisioned or replicated        
- Masking protects sensitive production data before it reaches non-production
---
## 9. User Interface options for Delphix
You can interact with the Continuous Data Engine using several interfaces:
### 1. Graphical User Interface (GUI) – Preferred
- Web-based UI    
- Used for:    
    - Configuration        
    - Monitoring        
    - Daily administration        
### 2. Web API
- REST-based (GET, PUT, DELETE)    
- Used for:    
    - Automation        
    - CI/CD pipelines        
    - Custom integrations
### 3. Command Line Interface (CLI)
- Accessed via SSH    
- Menu-driven    
- Used mainly by experienced admins    
### 4. dxToolkit
- Legacy scripting tools    
- Not officially supported    
- Mostly replaced by DCT    
### 5. Data Control Tower (DCT)
- Container-based (Docker / Docker Compose)    
- Central API gateway and orchestration layer    
- Preferred for modern automation and multi-engine management    

---
## 10. Delphix Administration role
### Who is a Delphix Administrator?
A Delphix Administrator is responsible for:
- Installing Delphix engines    
- Configuring infrastructure    
- Managing environments and data sources    
- Defining users, roles, and privileges    

### Important rule
Delphix administration is done **only through Delphix interfaces**  
Direct OS-level changes are not supported.
These interfaces control:
- Networking    
- Storage    
- Authentication (LDAP, DNS)    
- Data provisioning logic    
- Business rules    

---
## 11. Key takeaways from Lesson 1
- Delphix virtualizes data, not infrastructure    
- dSource = continuously updated source copy    
- VDB = instant, writable virtual clone    
- Timeflow enables point-in-time data access    
- Continuous Data Engine is the foundation of the platform    
- Administrators manage everything through Delphix interfaces