# Lesson 3 Provisioning and Replication
The next step is to make a virtual copy of the dSource within the Delphix Continuous Data Engine that can then be used to make as many Virtual Databases (VDBs) as needed. 
## **Virtual Database (VDB)**
When you use the Delphix Continuous Data Engine to create a dSource from your source database, you are actually creating a virtualized representation of that source database. 

Because it is only a virtual representation of the source, you cannot work with it the same way you would the original source. Instead, you must use that dSource to create a virtual database (VDB), a process that Delphix refers to as "VDB provisioning."

At their core, VDBs are fully functional copies of data sources that can be created and managed at a fraction of the storage and time that is typically required. To end-users, VDBs act and perform just like a standard database.
![[Pasted image 20251229115113.png]]

Mental Model:
```scss
dSource (read-only)
   ↓ provision
VDB (read-write, usable)
```
## **The Benefits of VDBs**
## Lightweight
Virtual databases take up very little storage space. The amount of space consumed is directly proportional to the amount of data changed, through executing DML queries against the database or other actions that result in changes to the virtual database.
Example:
- 1 TB prod DB
- 20 VDBs
- Actual storage ≈ 1.2 TB (not 20 TB)
## Flexible
VDBs support a variety of operations such as taking snapshots, provisioning copies of VDBs, refreshing the data within a VDB, or migration to a physical repository. Such tasks are known to be cumbersome with physical databases. VDBs can be ephemeral and can be administered with simple API automation.
Perfect for:
- CI/CD pipelines
- Short-lived test environments
- Automation via APIs
## Simple
While the database can be managed through the use of native database tools, Delphix will handle management of VDBs including provisioning, teardown, start and stop, migration to a different host, and more, through the Delphix DataControl Tower(DCT).
Admins & DevOps teams use:
- **Delphix UI**
- **DCT APIs**
![[Pasted image 20251229115157.png]]
A VDB is created within the Delphix Continuous Data Engine from the Timeline History of a dSource or VDB. Virtual databases are provisioned to a particular installation contained within a host or cluster, and Delphix handles the configuration and management of the externally visible database.

Let's learn about another important capability of the Delphix Continuous Data Engine: 
Replication.
Replication recreates objects from the Source Engine onto the Target Engine in a replica, also known as a namespace, that preserves object relationships and naming on the Target Engine without interfering with its active objects.
**Delphix Replication**
![[Pasted image 20251229115224.png]]
Replication allows you to move Delphix objects such as dSources and Virtual Databases (VDBs) between Delphix Engines. Replication allows you to not just migrate data, but take the important step of backing up your data. Important note: Replication supports Delphix Engine recovery and DR scenarios - not production source recovery

As virtual appliances, it is possible to backup, restore, replicate, and migrate data objects between Delphix Engines using features of hypervisor and the underlying storage infrastructure. Data objects include:
- Groups    
- dSources,    
- VDBs    

```
Non-Data objects refer to:
- Delphix users, roles, permissions, and authorizations
- Policies
These objects will not be presented as selectable objects when creating a replication spec, but will instead be passively included by association, the same way environments are. 

If the entire engine is replicated, all non-data objects will be included. If specific data objects are replicated, all associated non-data objects will be included.
```

## Disaster Recovery:
In the event of a disaster, you may need to failover your engine. Delphix replication enables you to configure a failover Delphix Engine to preserve the data and Delphix objects from the source engine for disaster recovery
## Geographically Distributed Development:
Often, development teams access data from all over the world. In this scenario, you may want to replicate data to be local to the developers who require access. With Delphix replication, you can provide developers with local access to Delphix datasets.
## Data Migration:
Delphix supports simple migration of data and resources between Delphix Engines. With replication, you can easily migrate data, automatically if desired, from one datacenter or network to another
## Replicating to the Public Cloud:
With Delphix replication you can send data from engines deployed on-premise to the public cloud. In this case, you may have a Delphix engine in the production zone to ingest data securely with replication set up to the public cloud for development access and rapid, on-demand testing.
## Selective Data Distribution (SDD):
The ability to utilize SDD enables you to securely replicate masked data without compromising sensitive data from the source engine.


---
**The Delphix Ecosystem with Replication**
Delphix Replication provides asynchronous updates to a remote site, which can be another Delphix Engine in the local datacenter, in a remote datacenter, or in the Cloud. As a solution, this provides both backup and disaster recovery in a single technology and adds several important features:
- Capability to use VDBs on the replicated side
-  Compression, encryption, and bandwidth throttling en route
-   Ability to replicate multiple source Delphix Engines to a single target Delphix Engine
- Flexibility of selecting granular objects to be replicated (Group-level, dSource only, VDBs)
- Selective Data Distribution (SDD) permits the distribution of masked data between Delphix Engines
![[Pasted image 20251229140743.png]]
Configuring Replication is as simple as having a second Delphix Engine that is reachable over the network.

**Selective Data Distribution (SDD)**
As mentioned above, Selective Data Distribution permits the distribution of masked data between Delphix Engines. The sources received on a target Delphix Engine do not include the original parent source, thereby making the original source inaccessible from the target.  
SDD is **one of Delphix’s strongest security features**.
What SDD Does:
- Replicates **only masked VDBs**
- Original unmasked source:  
    ❌ Never replicated  
    ❌ Never accessible on target
📌 Golden rule:
> **Only masked VDBs can be used with SDD**

Selective data distribution is configured on the source Delphix Engine or in the Data Control Tower. It first copies a subset of masked VDBs to a target Delphix Engine, then sends incremental updates either manually or according to a schedule.

The Masking Engine provisions a VDB from the dSource and applies the masking rules to that VDB. In parallel, the DxFS (Delphix File System uses Selective Data Distribution (SDD) to redact the sensitive data from the replication stream, ensuring that only masked or permitted data is replicated to the Non-Production datacenter. With SDD, sensitive data from the dSource never leaves the Production engine, providing protection at both the VDB and replication layers.

**Only masked VDBs can be added to a Selective Data Distribution spec. and replicated to another engine outside the production zone (dev/test on premise or in the cloud).**
![[Pasted image 20251229140812.png]]
In order to utilize SDD for Replication, you need to make sure that the VDB you want to replicate is masked during the Provisioning process.

---
In addition to the replication capabilities provided by the above infrastructure, native Delphix Engine replication provides further capabilities, such as the ability to:
- Replicate a subset of objects
- Replicating  multiple sources to a single Target
- Provision VDBs from replicated dSources and VDBs without affecting ongoing updates
![[Pasted image 20251229140933.png]]

**Replicating to the Public Cloud**
With Delphix replication you can send data from engines deployed on-premise to the public cloud. In this case, you may have a Delphix engine in the production zone to ingest data securely with replication set up to the public cloud for development access and rapid, on-demand testing.

Now that we have learned about how Delphix Engines are used to replicate data, let's take a look at what the Delphix Continuous Data Engine User Interface (UI) looks like during the Replication process. Click on the tabs below: 

The Replication Profile
In the Delphix DCT, the replication is accessed by selecting Data, Policies and then Replication on the left navbar. The Replication Policy allows the user to determine which types of objects are being replicated, and is where the address for the Target Engine is entered. 
![[Pasted image 20251229141028.png]]
There are some considerations to keep in mind when performing Replication tasks, to ensure that the Replication process is successful.

---
Replication In Progress
On the Replication page, once Replication is taking place, a bar showing the progress of the Replication process appears. In this example, our Replication is named DR Replica. Progress can also be monitored via the Running Actions Tab. 
![[Pasted image 20251229141356.png]]

Running Actions
While the Replication process is taking place, Running actions are visible on both the Source and Target Engines. 
![[Pasted image 20251229141439.png]]

## Failover and Conflict Resolution
Certain objects may require changes to resolve conflicts prior to completing a replication failover. Names of replicated objects should be unique for failover to complete successfully.
## Enabling Databases and Environments
Replicated objects may refer to states (IP addresses, mount paths, etc.) that differ between the Source and Target Engines. Because of this, all databases and objects within a replica are automatically disabled after a failover. This allows the administrator to alter configuration prior to enabling databases and environments.