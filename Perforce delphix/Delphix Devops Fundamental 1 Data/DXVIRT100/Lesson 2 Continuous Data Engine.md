# Continuous Data Engine
Ingesting data into the DevOps Data Platform can be done using API calls, or using the Perforce Delphix DevOps Data Platform User Interface (UI). For the purposes of this overview course, we will be focusing on UI experience.
In this section, we will take a closer look at how the Delphix Continuous Data Engine ingests data from the data sources within your Source Environment(s), and creates dSources.

The Delphix Continuous Data Engine is able to connect to several types of data sources including RDBMS databases (Oracle, Sybase ASE, Postgres, MS SQL) and flat files such as database/application binaries, content, configuration files, and more...

**Data Sources**
A Source Environment is either a single instance host or cluster of hosts that run database software. 
For example, you might have a Linux system running Postgres. An Environment may either be an individual instance, or a cluster like Oracle RAC.
Once an environment has been added, the Delphix Continuous Data Engine will automatically discover any data sources on the host. 
The Delphix Continuous Data Engine stays connected to your Source Environment(s). Each time data is ingested from your Source Environment(s), its data blocks are compressed and stored in the Delphix Continuous Data Engine. When new source data is discovered, rather than ingesting a 1:1 copy of the data, the Continuous Data Engine only ingests and compresses blocks of the new data.  A collection of data blocks are what is referred to as a dSource.
## **Traditional Data Ingestion vs. Data Ingestion with the Delphix Continuous Data Engine**

![[Pasted image 20251229113221.png]]

In a traditional cloning operation, Data files consisting of blocks are copied in full, from one system to another, using some form of backup and recovery.
With the Delphix Continuous Data Engine, the data already exists in compressed form as a dSource. 
Data blocks in the dSource are selected, filtered, and mapped to create a set of Virtual Data Files that are presented to the Target Environment via ICSI or NFS.
No data blocks are actually copied, allowing for near-instant cloning.

**dSources**
A dSource is a compressed copy of the source database stored in the Delphix Continuous Data Engine, along with all incremental updates so that it is kept up to date over time. 
A Linked dSource within the Delphix Continuous Data Engine will ingest data from the Source Environment(s) and create a dSource object on the Delphix Continuous Data Engine. As a virtualized representation of your source data, it cannot be managed, manipulated, or examined by database tools.

**In order to use dSource snapshots, you must create a virtual database (VDB), an independent, writable copy of a dSource snapshot**
Once a dSource is added to the Delphix Continuous Data Engine, a Timeline History for that dSource gets created. A Timeline History for a dSource is the history of changes to a data source maintained within the Delphix Continuous Data Engine. 
Each dSource and VDB has its own record that is represented in the Timeline History, which is made up of snapshots taken at different points in time. Snapshots represent the state of a dataset at a specific moment in time. Snapshots are created from policies or are generated on demand. Snapshots allow you to choose a point in time from which to provision, refresh, or rewind your data. The Timeline History allows you to provision VDBs from any point in time down to the second or transaction boundary.
![[Pasted image 20251229113240.png]]
In this example, we can see that there are three Snapshots in the Timeline History, and that one of the Snapshots was created by refreshing the dataset.

---

## The Delphix Continuous Data Engine UI
Step 1
![[Pasted image 20251229114618.png]]
The Dashboard provides important information about Performance, Storage Capacity, and any Actions or Faults that need to be addressed. The banner houses the Manage, Resources, System, and Help tabs. The Manage tab houses the links to the Environments and Datasets pages. These pages are where we configure our Source and Target Environments and link our dSources.

Step 2
![[Pasted image 20251229114642.png]]
The Environments page is the place where Source and Target Environments are configured to the Delphix Continuous Data Engine. In this example, you can see that a Source Environment is linked to the engine.

Step 3
![[Pasted image 20251229114709.png]]
The Datasets page is where dSources are linked and Virtual Databases (VDBs) are provisioned.
When the dSource is selected, you can see the Timeflow for that dSource. In this example, you can see that there is one snapshot associated with this dSource.
In order to use dSource snapshots, you must create a VDB, an independent, writable copy of a dSource snapshot.

---
