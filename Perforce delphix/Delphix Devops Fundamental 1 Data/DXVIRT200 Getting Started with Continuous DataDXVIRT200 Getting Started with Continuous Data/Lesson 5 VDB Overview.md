# VDB Overview
Lesson 5 of 7
At their core, Virtual Databases (**VDBs**) are a database provisioned from either a dSource or another VDB which is a full read/write copy of the source data. To end-users, VDBs act and perform just like a standard database.
![[Pasted image 20251230121333.png]]
Key characteristics:
- Read/write
- Appears like a normal database
- Runs on a **Target Environment**
- Shares data blocks with its parent dSource or VDB
- Uses minimal additional storage
Important distinction:
- **dSource** = virtualized representation (not usable directly)
- **VDB** = usable database for developers, testers, or applications

When you use the Delphix Continuous Data Engine to create a dSource from your source database, you are actually creating a virtualized representation of that source database. 

Because a dSource is only a **virtual representation**, you cannot:
- Connect to it
- Query it
- Modify it
To actually use the data, you must **provision a VDB**.
Delphix term to remember:
> Creating a VDB is called **VDB provisioning**

Because it is only a virtual representation of the source, you cannot work with it the same way you would the original source. Instead, you must use that dSource to create a virtual database (VDB), a process that Delphix refers to as **"VDB provisioning."**

In order to provision a VDB, you will need a linked dSource from a source host and a compatible target environment. 

Datasets Page
Provisioning  your first VDB begins by selecting the dSource on the lefthand side of the Datasets page, if it is not already highlighted by default. In this example, our dSource is named 'orcl'.
## Requirements to Provision a VDB
To provision a VDB, you need:
1. A **linked dSource**    
2. A **compatible Target Environment**    
3. A **snapshot or point in time** from the dSource (or VDB)
Provisioning creates:
- A filesystem based on the selected snapshot    
- A dependency between the VDB and the snapshot used
Important exam note:
> A snapshot used for provisioning **cannot be deleted** while the VDB depends on it.

![[Pasted image 20251230121344.png]]
Provisioning
Hovering your cursor over the snapshot the selected dSource reveals the **Provision a VDB** button, which, when clicked on, launches the **Provision VDB** Wizard.
![[Pasted image 20251230121412.png]]

Provision VDB Wizard
**Since provisioning VDBs can vary across data platforms, details on configuration requirements and settings within the VDB Wizard can be found within the Delphix documentation for each specific data platform, such as Oracle.** 
In this example, we are provisioning the VDB on an Oracle Target environment.
![[Pasted image 20251230121433.png]]
**The Virtual database's filesystem will be dependent upon the snapshot used to provision, and as such, that snapshot can not be removed until the dependency is removed.**

---
## **Refreshing Virtual Databases**
### What is a VDB Refresh?
Refreshing a VDB:
- Re-provisions the VDB from the dSource
- Reverts it to a **snapshot or specific point in time**
- Discards all current changes in the VDB
Refresh options:
- Snapshot-based
- Point-in-time (faster vs more accurate)
After refresh:
- A new snapshot is created labeled **“Refresh Point”**
- The old Timeflow still exists in Delphix and is accessible via **CLI**
- The VDB now follows a new Timeflow
Important safety feature:
> Delphix allows you to **undo a refresh** if done accidentally

![[Pasted image 20251230121547.png]]
Refreshing a VDB will re-provision it from the dSource. You can choose to refresh the VDB from a snapshot or a specific point in time. When you refresh a VDB, it will revert to its past state in the specified snapshot or point in time. When performing a VDB refresh, there is an option to choose between either the faster or more accurate point in time for that database. Once the Refresh is completed, you will see it listed as a snapshot on that VDBs Timeflow. The snapshot states "Refresh Point." The old VDB Timeflow can be accessed using the CLI, until the related snapshots are removed via Retention policy.
![[Pasted image 20251230121555.png]]

**Although the VDB no longer contains the previous contents, the previous Snapshots and TimeFlow still remain in Delphix and are accessible through the Command Line Interface (CLI).**
![[Pasted image 20251230121601.png]]
An accidental refresh of one or more virtual databases (VDBs) from a source database can remove important data. To correct this situation, users can undo VDB refresh or rewind actions. Clicking on the elipses in the top right corner of the datasets page reveals the option to undo a Refresh or a Rewind of a VDB.

## **Rewinding a VDB**
What is a VDB Rewind?
Rewinding:
- Rolls a VDB back to an earlier point in **its own Timeflow**
- Re-provisions the VDB at that point
- Removes changes after the rewind point
Key difference:
- **Refresh** → goes back to the dSource
- **Rewind** → goes back within the VDB’s Timeflow
After rewind:
- A new snapshot labeled **“Rewind Point”** is created
- Delphix creates a **new Timeflow**
- The parent snapshot and Timeflow become **dependencies**
Critical exam rule:
> Parent snapshots and Timeflows **cannot be deleted** until the VDB is refreshed

Rewinding a VDB rolls it back to a previous point in its Timeflow and re-provisions the VDB. The VDB will no longer contain changes after the rewind point, but is a useful feature which allows you to roll back data to a previous point if your data has been corrupted. 

Although the VDB no longer contains changes after the rewind point, the rolled-over Snapshots and Timeflow still remain in Delphix and are accessible through the Command Line Interface (CLI).  More information about this process can be found on the Delphix Documentation page. 

![[Pasted image 20251230121628.png]]
Hover over the Snapshot you want to use as your rewind point with your cursor and click the Rewind button.

![[Pasted image 20251230121640.png]]
Confirm the decision to rewind the VDB by clicking the **Rewind** Button.

![[Pasted image 20251230121647.png]]
A new snapshot is created, that shows the time the Snapshot was completed, and states "Rewind Point."

Delphix clones a new Timeflow from the closest Snapshot older than or equal to the rewind point. This creates a dependency between the new Timeflow and the parent Snapshot and Timeflow. The parent Snapshot and Timeflow cannot be deleted because of this dependency. **The VDB must first be refreshed before the parent Snapshot and Timeflow can be removed.**


---
## **Enabling and Disabling Virtual Databases**
Disabling a VDB is a prerequisite for procedures such as VDB migration or upgrade. Disabling a VDB removes all traces of it, including any configuration files, from the target environment to which it was provisioned. However, the VDB itself, as well as the metadata, will still exist on the engine.
### Disable VDB
- Removes database files and config from the **Target Environment**
- Metadata and data remain on the Delphix Engine
- Required for operations like:
    - Migration
    - Upgrade
### Enable VDB
- Restores configuration files to the target
- VDB resumes normal operation
Exam tip:
> Disable does **not** delete the VDB

When you later enable the VDB again, these configuration files are restored on the target environment.
![[Pasted image 20251230121756.png]]

When you are ready to enable the VDB again, you will see the word 'Enable' instead of Disable in the menu seen above. Once enabled, the VDB will continue to function as it did previously.
## **Deleting Virtual Databases**
Deleting a VDB will remove it and it's Timeflow and snapshots from the Delphix Engine entirely. This operation is non-reversible. 
Deleting a VDB:
- Permanently removes:
    - VDB
    - Its Timeflow
    - All snapshots
- Is **non-reversible**
Restrictions:
- You **cannot delete** a VDB that has dependencies
Exam wording to remember:
> Deleting a VDB is an **unrecoverable operation**

**Deleting a VDB is an unrecoverable operation. Proceed only if you want to permanently destroy the unique data that was created in the VDB.**
![[Pasted image 20251230121820.png]]

![[Pasted image 20251230121827.png]]

You cannot delete a VDB that has dependencies, as the dependencies rely on the data associated with the snapshot. 
## Common VDB Operations — Comparison Table

| Operation | What it Does                     | Reversible        |
| --------- | -------------------------------- | ----------------- |
| Refresh   | Re-provisions from dSource       | Yes (undo)        |
| Rewind    | Rolls back within VDB Timeflow   | Yes (via refresh) |
| Disable   | Removes from target only         | Yes               |
| Delete    | Permanently removes VDB and data | No                |

### Knowledge Check — Answers
### Question 1
**VDBs that have dependencies cannot be deleted**
Correct answer: **True**
## **Knowledge Check**
VDBs that have dependencies can not deleted.
True
False  

Match each VDB function with its name.
1. Rewind VDB
2. Delete VDB
3. Refresh VDB

- Will re-provision the VDB from the dSource
- Rolls a VDB back to a previous point in its Timeflow and re-provisions it.
- Will remove a VDB and it's Timeflow and snapshots from the Delphix Engine entirely
---
## One-Page Exam Summary
- VDBs are **read/write databases**
- Provisioned from a **dSource or another VDB**
- Behave like standard databases
- Share storage with parent objects
- Can be refreshed, rewound, disabled, or deleted
- Dependencies control what can be removed

---