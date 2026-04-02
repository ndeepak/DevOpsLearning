# DXVIRT100 Perforce Delphix DevOps Data Platform Overview

Delphix DevOps Data Platform
A suite of products that allows you to ingest, secure, and manage copies of your data:
- **Delphix Continuous Data Engine** – Connects to your source data and creates compressed virtual copies of your database that can be used just like a physical copy of a database and can also be easily replicated to other environments.
- **Delphix Continuous Compliance Engine**- Secures your sensitive data in non-production environments and replaces sensitive data with fictitious but realistic data
- **Data Control Tower (DCT)**-A user interface and API Gateway that provides a central control point for automating, managing, and monitoring multiple Delphix Continuous Data and Compliance Engines simultaneously
---
![[Pasted image 20251225122547.png]]
1. Making a Copy of source data
The Delphix Continuous Data Engine connects with your source database(s) to take in a full copy of your data. When it does this, the data is compressed (usually to about 1/3 the size). 
The compressed copy of your data is now housed in the Delphix Continuous Data Engine.

2. Masking your data with the Continuous Compliance Engine
The Delphix Continuous Compliance Engine can then be used to mask all or some of your data, depending on your needs. The data is masked consistently across all your data tables.

3. Creating copies of your Virtual Database (VDB)
Once you have created a secure copy of your data, you can make as many copies of your Virtual Database (VDB) as you need. Delphix Replication allows you to copy objects from one Engine (referred to as a source Engine) to another Engine (referred to as a target Engine) or to use Selective Data Distribution to distribute masked data between Delphix Engines without bringing over the unmasked parent source.

4. dSources and VDBs
The Delphix Continuous Data Engine stays connected to your Source Environment. Each time the data from your source environment changes, the Delphix Continuous Data Engine ingests only the new data blocks rather than an entire 1:1 copy. The collection of these data blocks of your source data are what is referred to as a dSource.
The dSource is then used to create virtual copies of your database (VDBs)

5. Using your VDBs for development and testing
You can assign these VDBs to your testers and developers through Delphix Self-Service. This allows the data to be tested without impacting the data within the production environment.

6. Managing multiple Delphix Engines
DCT enables API-driven DevOps workflows that allow automation and management across multiple Delphix Engines at once.


---
Environments
Hosts or clusters configured within Delphix as Sources or Targets
- Source – An Environment that contains one or more source databases
- Target - An Environment that will be used for provisioning Virtual Databases (VDBs)

---
Databases
The data files, control files, transaction logs, and archive logs making up a Database that are accessible by a database instance.
- Source – A database that is synced with a Delphix dSource
- dSource– A copy of the source database stored in the Delphix Continuous Data Engine, along with all incremental updates, and used to make virtual copies of your data
- Virtual Database (VDB)–  Fully functional copies of data sources. To end users, VDBs act and perform just like a standard database
![](https://cdn5.dcbstatic.com/files/p/u/puppet_docebosaas_com/1766656800/7W6fXlVVsOZ23t_HHV1h3w/scorm/96309a497477bcaa18ed5ad00ab57647bc9d0108d6d51d84e57b0f5b428331f8/scormcontent/assets/datasources.jpg)


