# Introduction
Lesson 1 of 7
## Delphix DevOps Data Platform – Big Picture
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

It is important to understand the main concepts and use cases of the **Delphix Continuous Data Engine** before going hands-on with the Delphix DevOps Data Platform as an Administrator. 

This course will teach you the main features of, and use cases for, the Delphix Continuous Data Engine, and how the engine fits into the bigger picture of data management practices with the Delphix DevOps Data Platform.
![[Pasted image 20251230104340.png]]
**The Delphix DevOps Data Platform** includes the Delphix Continuous Data Engine, the Delphix Continuous Compliance Engine, Delphix Self-Service and Data Control Tower (DCT). The **Continuous Data Engine** is a data management engine that provides the ability to ingest, replicate, and share datasets.

The Delphix Continuous Data Engine is able to connect to several types of data sources including RDBMS databases (Oracle, Sybase ASE, Postgres, MS SQL) and flat files such as database/application binaries, content, configuration files, and more...
![[Pasted image 20251230104402.png]]
While we won't be covering the Delphix Continuous Compliance Engine in this course, it is important to note that the VDB provisioning and Replication processes we cover later on in this course are often done once the data from the initial dSource has been masked by the Delphix Administrator(s) using the Continuous Compliance Engine. 
## **Continuous Data Engine Overview**
### What the Continuous Data Engine does
The **Continuous Data Engine** is a data management engine that:
- Connects to source systems    
- Ingests data efficiently    
- Keeps data synchronized    
- Creates virtual copies for non-production use   
### Supported data sources
It can connect to:
- RDBMS databases:    
    - Oracle        
    - PostgreSQL        
    - MS SQL Server        
    - Sybase ASE        
- Flat files:    
    - Application binaries        
    - Configuration files        
    - Content files
The Delphix Continuous Data Engine connects with your source database(s) to take in a full readable, writable copy of your data. When it does this, the data is compressed (usually to about 1/3 the size). After the initial data ingestion, the Delphix Continuous Data Engine stays connected to your source environment. Each time the data from your source environment changes, the Delphix Continuous Data Engine ingests only the new data blocks rather than an entire 1:1 copy. This collection of source data blocks is referred to as a dSource.
![[Pasted image 20251230104421.png]]
Virtual copies of your database (VDBs) can then be provisioned from dSource (or VDB) snapshots, from any point in time in a timeflow. VDBs share common data blocks with their dSource timeflow, resulting in minimal capacity requirements for each provisioned VDB

 VDBs are read-write databases, and changes made to the VDB are written to new, compressed blocks in Delphix storage. 

The data within the VDB can be refreshed as needed, to any point in time along its source's timeline.

The Delphix Continuous Data Engine maintains synchronization either by using product native replication such as Dataguard, SQL Server log shipping, and Postgres replication, or via product native incremental backups. User defined policies dictate the frequency of synchronization. 

Delphix maintains a Timeflow of the source database; a record of snapshots and log changes. We will cover Policies, Snapshots, Timeflows, and Replication later on in this course. 

## **User Interface Options for working with Delphix**
Methods of connecting with Delphix Engines include:
## Graphical User Interface (preferred)
Graphical UI control panel used to configure, control, and monitor Delphix assets and objects
## Web API
- RESTful interface with PUT/GET/DELETE capabilities for Delphix assets and operations
- Useable via curl or in a programming language  
## Command Line Interface (CLI)
- Accessed via SSH to the Delphix Continuous Data Engine
- Uses a custom menu and command system to perform operations with Delphix
## DXToolkit
- Unofficial command-line primitives package **(not supported by Delphix Support)**
- Runs as .exe programs on Windows or binary scripts for Linux    
- Can be chained to build powerful Powershell or bash scripts
## Data Control Tower (DCT)
Requires Docker and Docker Compose to run. Linux versions and distributions that have been verified to work with Docker are supported.

## **Delphix Administration**
**The Delphix Administrator**
A Delphix Administrator's primary responsibilities include:
- Installation
- Configuration and management of servers, virtual machines, and applications
- Defining user roles and privileges 

Administration of the Delphix Continuous Data Engine is effected through product interfaces only. These interfaces provide for the proper configuration and testing of customer infrastructure components, such as network addresses, storage, Domain Name Service (DNS) servers, authentication servers (LDAP), etc. The interfaces also control the business logic and control of the overall platform, including how customer data is used and provisioned by the system.