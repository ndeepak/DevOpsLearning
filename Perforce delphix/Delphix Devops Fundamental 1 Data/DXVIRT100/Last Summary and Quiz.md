# Summary and Quiz
In this Overview of the Delphix DevOps Data Platform course, we learned:
-  What the Delphix DevOps Data Platform is and its benefits
- How the Delphix Continuous Data Engine ingests source data and creates a virtual copy of that data 
- How the Delphix Continuous Compliance Engine is used to mask sensitive data 
- How masked VDBs can be replicated, and how those replicated VDBs can be shared with developers and testers through Delphix Self-Service  
- How Data Users easily work with and test data in Delphix Self-Service without disruptions or downtime to production
- What Data Control Tower is and some of its use cases

There is so much more to learn about the Delphix Suite of Products. We invite you to take a look at our course offerings to get a more comprehensive view of how to use the Delphix DevOps Data Platform. Delphix offers a number of courses to help you learn more about Delphix best practices, Delphix Continuous Data Engine and Continuous Compliance Engine Administration, Delphix Self-Service, and Test Data Management. 
The following questions will reinforce the key components we covered in the Delphix DevOps Data Platform Overview Course:
# Question01/09
Which options allow you to bring your data into the Delphix DevOps Data Platform (select all that apply)
- **User Interface**    
- Direct Link    
- **API Calls**    
- **Administrative Interface**    
- **Data Control Tower**
# Question02/09
 _____________ allows you to provision VDBs from any point in time down to the second or transaction boundary.
An environment
**Timeflow**
A dSource

Explanation (from Data Control Tower and Delphix fundamentals)
- **Timeflow** represents the complete timeline of changes for a dataset (dSource or VDB) inside the Delphix Continuous Data Engine.
- It contains snapshots, logs, and change history that allow you to provision or rewind a VDB to **any specific point in time**, down to the **second or even transaction boundary**.
Why the others are incorrect
- **An environment**  
    An environment is simply the host or cluster where databases run. It does not track historical data states.
- **A dSource**  
    A dSource stores compressed source data and incremental changes, but the **ability to select a precise point in time** comes from the **Timeflow**, not the dSource itself.
# Question03/09
True or False:  A dSource is a virtualized representation of a physical or logical source database, which cannot be accessed using database tools. 
True
False

Explanation
A **dSource** is a **virtualized, compressed copy** of a physical or logical source database stored inside the Delphix Continuous Data Engine.
- It **cannot be accessed, queried, or managed using database tools**
- It exists only as a Delphix-managed object    
- To interact with the data, you must first provision a **VDB (Virtual Database)** from a dSource snapshot
This design ensures data efficiency, consistency, and fast provisioning.
# Question04/09
True or False:  Virtual Databases or VDBs are created from the dSource through a process called VDB Provisioning
True
False

Explanation
**Virtual Databases (VDBs)** are created from a **dSource** using a process called **VDB Provisioning**.
- The **dSource** holds the compressed, read-only copy of the source data
- **Provisioning** selects a snapshot or point in time from the dSource    
- A **VDB** is then created as a **fully functional, writable database**    
- VDBs behave just like physical databases for developers and testers
# Question05/09
In order to utilize Selective Data Distribution (SDD) for Replication, you need to make sure that the VDB you want to replicate is masked during the Provisioning process. 
True
False

Explanation
**Selective Data Distribution (SDD)** allows you to replicate **only masked data** from a source Delphix Engine to a target engine.
- This ensures that **sensitive data never leaves the production environment**.
- Only VDBs that are **masked during provisioning** can be included in an SDD replication.
- Unmasked VDBs or dSources **cannot** be replicated via SDD to non-production or external environments


# Question06/09
In Delphix Self-Service, these control decisions about how resources such as VDBs and vFiles are allocated and shared.
The Delphix Self-Service Users
The Delphix Administrators

Explanation
In **Delphix Self-Service (now replaced by DCT Self-Service)**:
- **Delphix Administrators** control governance, including:
    - Allocation of VDBs and vFiles
    - Sharing permissions
    - Access rights and resource constraints
- **Delphix Users** (or Data Users) can consume and manage data **within the permissions assigned by administrators**, but they **cannot control global allocation or sharing rules**.

Here’s the correct matching for Question 07/09:

|**Term**|**Function / Goal**|
|---|---|
|**Self-Service**|Creates a clear separation of IT infrastructure and data management|
|**Virtual Database (VDB)**|An instantly provisioned, space-efficient virtual clone of a dSource managed by Delphix|
|**Replication**|Move Delphix objects between Delphix Engines or replicate Delphix Engines|
|**Masking**|Creates a structurally similar but fictitious version of data|
# Question08/09
The Timeline History in the DCT allows you to restore a ______to different point in time.
dSources
VDBs

Explanation
- **Timeline History** in DCT tracks the lifecycle of a **VDB** including provisioning, refreshes, bookmarks, and snapshots.    
- It allows developers or administrators to **restore a VDB to any previous point in time**, down to the second or transaction boundary.    
- **dSources** are read-only, compressed representations of source data and cannot be restored or manipulated directly.


# Question09/09
The two ways to mask data in the Delphix Continuous Compliance Engine are:
- On- The- Fly Masking    
- End-Point Masking    
- In-Place Masking

Explanation
Delphix Continuous Compliance Engine supports two primary methods for masking sensitive data:
1. **In-Place Masking**
    - Masks data directly in the existing environment (source or target)        
    - Only affects the columns you flag        
    - Ensures no sensitive data leaves the production system        
2. **On-The-Fly Masking**    
    - Masks data during the provisioning process        
    - Creates a masked VDB without exposing sensitive production data        
    - Ideal for non-production environments like development or testing        
**End-Point Masking** is not a supported method in Delphix.

---
