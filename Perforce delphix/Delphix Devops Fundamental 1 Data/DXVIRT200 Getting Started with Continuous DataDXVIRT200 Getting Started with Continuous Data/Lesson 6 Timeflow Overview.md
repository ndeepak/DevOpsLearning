# Timeflow Overview
Lesson 6 of 7
**Timeflow** is essentially a history of changes to a data source or virtual database that is maintained by the Delphix Continuous Data Engine and is comprised of a series of **Snapshots**.

A **Timeflow** is:
> A chronological history of changes to a **dSource or VDB**, maintained by the Delphix Continuous Data Engine, and composed of **snapshots plus log data**.

Snapshots represent the state of a dataset at a specific moment in time. Incremental changes in the data source are ingested over time into the dSource or VDB, building a record of changes to the data over time referred to in the Continuous Data Engine as a **Timeflow**. 

Both dSources and VDBs have Timeflows. This Timeflow data serves as the basis for all Virtual Database storage within Delphix. 
1. Timeflow: uses two mechanisms to provide point in time provisioning:
    - Periodic snapshots of the dSource or VDB        
    - Transactions Log collection for all time between backups
2.  **Snapshots** are created either via a schedule policy or generated on demand. Snapshots allow you to choose a point in time from which to provision, refresh, or rollback. 
3.  Provisioning:  can be provisioned from any snapshot in a dSource or VDB Timeflow. The Timeflow allows you to provision VDBs from any point in time down to the second and the transaction point.

Key points to remember:
- Both **dSources and VDBs have Timeflows**
- Timeflow is the **foundation of Delphix virtualization**
- Enables **point-in-time provisioning, refresh, and rollback**
In simple terms:
- **Snapshots** = fixed points in time
- **Logs** = changes between snapshots
- **Timeflow** = snapshots + logs over time

## **Important notes about Timeflows:**
The duration of the Timeflow window for both dSources and VDBs depends on how long snapshots and log files are retained. The duration is configured via Retention Policies which can be specified by the Delphix Admin. We will learn more about Policies later on in this course. The database log collection provides point in time provisioning for all the points between backups. Other important notes to consider include: 
- VDB snapshots and dSource snapshots are completely independent of one another.
- A VDB's datafile file system is cloned from, and therefore dependent upon, only one parent snapshot.
- The VDB's snapshots are only dependent upon the VDB's filesystem.
- Any dSource snapshots, before or after the one that the VDB was cloned from, are not necessary and will be removed by Policy Retention unless they have other dependencies (e.g. Were used to Provision other VDBs, or represent a bookmark)
- As long as the VDB Timeflow exists, the dSource snapshot that was used to create that Timeflow cannot be removed by policy or manually.
## How Timeflow Enables Point-in-Time Operations
Timeflow uses **two mechanisms**:
1. **Periodic snapshots**
    - Taken on a schedule or on demand
    - Represent the dataset at a specific moment
2. **Transaction log collection**
    - Captures changes between snapshots
    - Enables precision down to the **second or transaction boundary**
Because of this:
- You can provision a VDB from **any snapshot**
- You can provision a VDB from **any point in time between snapshots** (if LogSync is enabled)
This is a common exam question:
> **Timeflow allows provisioning down to the second or transaction boundary**

## Snapshots Explained
A **snapshot**:
- Represents the **state of a dataset at a specific moment**
- Contains **only changed blocks**, not a full copy
- Is used as a base for:
    - Provision
    - Refresh
    - Rewind (rollback)
Snapshots are created by:
- **Policies (scheduled)**
- **Manual/on-demand actions**
Important distinction:
- dSource snapshots and VDB snapshots are **independent**
- They belong to **different Timeflows**

## Retention and Timeflow Duration
The **length of a Timeflow** depends on:
- Snapshot retention
- Log retention
Both are controlled by **Retention Policies**, defined by the Delphix Administrator.
Key rule:
> If data is removed by retention policy, it is no longer available for provisioning or rollback.


## Critical Timeflow Dependency Rules (Very Important)
These rules frequently appear in exams:
- dSource snapshots and VDB snapshots are **completely independent**
- A VDB’s filesystem is cloned from **one specific parent snapshot**
- VDB snapshots depend **only on the VDB filesystem**
- dSource snapshots not used by any VDB may be deleted by retention policy
- **The dSource snapshot used to create a VDB Timeflow cannot be deleted** as long as that VDB Timeflow exists
In short:
> Dependencies prevent deletion
## How Timeflow Appears in the UI
In the Delphix UI:
- Timeflow is shown **vertically**
- Each row represents a **snapshot**
- Logs exist between snapshot rows (not always visually shown)
Snapshot size represents:
> Only the blocks that are unique to that snapshot
## **Anatomy of a Timeflow**
![[Pasted image 20251230124443.png]]
**In the Delphix Continuous Data Engine UI, a Timeflow is represented vertically with a series of individual snapshots as rows.**
**The size of a snapshot is defined to be the size of changes that are unique to that Snapshot. i.e. changed data blocks that are only associated with a particular snapshot.** 
- ### Initial dSource Snapshot 
    The initial dSource Snapshot creates a snapshot timestamp in the dSource Timeflow.
    - The initial data load when creating a dSource is comprised of data blocks from a backup of the source, which are captured, compressed and stored within the Delphix Continuous Data engine. 
    - Because empty datafile blocks are compressed, the size of the dSource is much smaller than the source database. 
Important concept: Empty blocks are compressed and consume little or no space

- ### Data Blocks  and Block Sharing
    If there are datafile blocks which have never been written to (empty blocks) those blocks are compressed and do not consume space on the Delphix filesystem.        
    When performing a write, if the block being written is the same as the block already on disk, then no write is actually performed. Only changed blocks are written to disk.
    - There is block sharing between a dataset and its descendant child datasets (e.g. A dSource and its child VDB)
    - A block can be shared by multiple Snapshots, if the block has not changed between the creation of those snapshots. 
    - Any blocks that are shared amongst multiple Snapshots are accounted for in the shared Snapshot Space total on the Capacity Management screen.
```
Delphix uses **block-level storage efficiency**:
- Only changed blocks are written
- Identical blocks are not rewritten
- Blocks can be shared by:
    - Multiple snapshots
    - dSources and child VDBs
Shared blocks:
- Are counted under **Shared Snapshot Space**
- Reduce overall storage usage
```

- ### Initial VDB Snapshot
    The initial VDB Snapshot creates a Snapshot timestamp in the VDBs Timeflow
    - A VDBs filesystem is cloned from a Source Snapshot. If the VDB were identical to the Source Snapshot then the initial VDB Snapshot would have a zero size. In most cases, there will  be a small number of changes associated with the VDBs first Snapshot because there are blocks that are changed during provisioning (the VDB's name, maybe the number of tempfiles, etc.) Also logs that were applied during provisioning could have a number of changes that were not in the Source snapshot. The result is that the Initial VDB Snapshot's size is usually near zero, but not actually zero for most dataservices.     
    - Why it’s not zero:
		- Metadata changes
		- Tempfiles
		- Logs applied during provisioning
- ### Subsequent Snapshots
    Subsequent Snapshots capture the state of a dataset at a specific moment in time.     
    - dSources - As changes are made to the source database or unstructured files, they are ingested by the Delphix Continuous Data Engine and brought into the dSource through incremental backups. Each subsequent dSource snapshot will capture changes made to the source database and a Snapshot timestamp will be added to the dSource Timeflow
    - VDBs - As changes are made to the VDB that differ from the initial dSource Snapshot, they will be written to the VDBs subsequent Snapshots. Because there may be fewer and fewer shared blocks between the dSource and VDB over time, the VDB can grow quite large. Refreshing the VDB will reset its size to zero, but changes made to the VDB will be lost.   
    - Important exam fact: > Refreshing a VDB resets its size to near zero but discards VDB changes
## **SnapSync and LogSync and VDB Snapshot**
![[Pasted image 20251230124554.png]]

Timeflow is maintained through the use of **SnapSync,** **LogSync** and **VDB Snapshot** depending on whether the object is a dSource or a VDB.

For dSources, the dSource snapshots are taken via the Delphix SnapSync service and database logs are collected via the Delphix LogSync service.

For VDBs, snapshots are taken via the Delphix VDB snapshot service. Database logs are automatically collected if database logging is enabled on VDBs.

```md
Timeflow is maintained differently for dSources and VDBs.
### For dSources
- **SnapSync** → snapshots
- **LogSync** → database logs
### For VDBs
- **VDB Snapshot service** → snapshots
- Logs collected automatically if logging is enabled
```
## SnapSync
The standard process for importing data from a source into the Delphix Continuous Data Engine. An initial SnapSync is performed to create a dSource on the Delphix Continuous Data Engine. Incremental SnapSyncs are performed to provide additional points in time to the dSource on the Delphix Continuous Data Engine.
- SnapSync will pull over the complete data set during the initial load using standard database protocols.
- Subsequent SnapSync operations will pull only the incremental changes and store them with optimal storage efficiency. At the end of each SnapSync operation, a snapshot is created that serves as the base point for provisioning operations.
- When provisioning a VDB, the closer the origin point is to a snapshot created via SnapSync, the sooner the provisioning operation will complete.

SnapSync is responsible for:
- Creating dSource snapshots
How it works:
- Initial SnapSync pulls a full dataset
- Subsequent SnapSyncs pull only incremental changes
- Each SnapSync ends with a snapshot
Exam-relevant note:
> Provisioning is faster when the provisioning point is closer to a SnapSync snapshot
## LogSync
This feature enables the ingestion and retention of more granular (log-based) source change data. This more granular change data allows for VDB point-in-time provision, refresh, or rollback.

- If you have LogSync enabled, you can provision, refresh, or rollback from a point in time between the snapshots endpoints. Point in time provisioning is also dependent on log retention.
- With LogSync is enabled, you will be able to to select the exact time from which you want to provision a VDB. 
- LogSync will periodically connect to the host(s) running the source database via standard protocols and pull over any log files associated with the database. These log files are stored separately from the SnapSync data and are used to provision from points in between SnapSync snapshots.
LogSync enables **fine-grained point-in-time control**.
Key points:
- Collects database log files
- Enables provisioning between snapshots
- Depends on log retention
With LogSync enabled:
- You can select an exact timestamp    
- You can refresh or rewind to precise points
Without LogSync:
- You are limited to snapshot boundaries

## VDB Snapshot
VDB Snapshots represent the state of a dataset at a specific moment in time. Snapshots are created via scheduled policies or are generated on demand. VDB Snapshots store any changed blocks that differ from those found in the dSource. As more and more changes are saved, the VDB will grow in size. 
VDB snapshots:
- Capture VDB state at a moment in time
- Store only changed blocks
- Can be created:
    - By policy
    - Manually
Important:
> VDBs can be provisioned from **dSource snapshots or VDB snapshots**

**VDBs can be provisioned from any dSource or VDB Snapshot within a Timeflow.**

## **Demo - Modifying LogSync and SnapSync**
![[Modifying LogSync and SnapSync.mp4]]

## One-Page Exam Summary
- Timeflow = snapshots + logs over time    
- Both dSources and VDBs have Timeflows    
- Snapshots store only changed blocks    
- LogSync enables second-level precision    
- Dependencies prevent snapshot deletion    
- Refresh resets VDB size    
- Rewind creates a new Timeflow    
---
## 13. Typical Knowledge Check Style Questions
You should now be able to answer:
- What enables point-in-time provisioning?    
- Why can’t certain snapshots be deleted?    
- Difference between SnapSync and LogSync    
- Why VDB size grows over time    
- How Timeflow differs for dSources vs VDBs

---