# dSource Overview
Lesson 4 of 7
A **dSource** is a copy of the source database that is compressed and stored in the Delphix Engine, along with all incremental updates, and is used to make virtual copies of your data. 
A **dSource** is:
> A **compressed, continuously updated copy of a source database** stored inside the **Delphix Continuous Data Engine**


![[Pasted image 20251230115050.png]]
**The dSource can then be used to create virtual copies of your database (VDBs). Once VDBs have been provisioned from a dSource, those VDBs can also be used to make virtual copies of a VDB.** 
It contains:
- An **initial full copy** of the source database
- **All incremental updates** (logs / changes)
- A complete **timeflow** of data
**Exam definition to remember**
> A dSource is **not a database you log into** — it is a **virtualized representation** of the source data.

```scss
Source DB
   ↓
 dSource
   ↓
  VDBs
   ↓
 VDBs from VDBs
```
### Key capabilities:
- Used to **create VDBs**
- Allows **point-in-time provisioning**
- Enables **space-efficient sharing**    
- Enables **replication**
 **Exam trap**:  
You **cannot create a VDB without a dSource** (or another VDB)
## Compression & Storage
- Data is **compressed** (typically ~⅓ of original size)
- Only **new blocks** are stored after initial ingestion
- Multiple VDBs **share the same blocks**
This is why Delphix saves **huge storage space**

## dSource vs Source Database (Very Important)

|Feature|Source Database|dSource|
|---|---|---|
|Lives on|Source Environment|Delphix Engine|
|Read/write|Yes|No|
|Can be accessed with DB tools|Yes|❌ No|
|Used for production|Often|❌ Never|
|Used to create VDBs|Indirectly|✅ Yes|
**Exam line**:
> A dSource **cannot be managed, manipulated, or examined using database tools**
## **Linking dSources**
### What does “Linking” mean?
**Linking** is the process of:
- Connecting Delphix to a **source database**
- Ingesting the data
- Creating a **dSource object** inside Delphix
Once linked:
- Delphix keeps the dSource **continuously synchronized**
- A **timeflow** is created
**Linking ≠ Provisioning**

| Action       | Purpose        |
| ------------ | -------------- |
| Linking      | Create dSource |
| Provisioning | Create VDB     |
A Linked dSource within the Delphix Continuous Data Engine will ingest data from the Source Environment(s) and create a dSource object on the Delphix Continuous Data Engine. As a virtualized representation of your source data, it cannot be managed, manipulated, or examined by database tools. 

![[Pasted image 20251230115108.png]]
## Linked dSource Characteristics
A linked dSource:
- Ingests data from the **Source Environment**
- Exists **only inside Delphix**
- Is **not accessible** by DB clients
- Serves as the **golden master** copy
 **Common mistake**:  
Trying to connect SQL*Plus / SSMS to a dSource ❌
## Creating VDBs from dSource
- VDBs can be created from:
    - dSource snapshots        
    - Any point in time in the timeflow
- VDBs are:
    - **Read-write**
    - Refreshable
    - Rollback-capable
Even more powerful:
> A **VDB can also be used to create another VDB**

This allows:
- Dev → QA → UAT chains
- Branching data copies

**Adding a dSource**
From the **Datasets** page, click on the plus sign next to **Datasets** and select **Add dSource.** This opens the **dSource Wizard.** The video below demonstrates how to navigate the dSource Wizard:
### Navigation
**Datasets → + (plus sign) → Add dSource**
This launches the **dSource Wizard**
## **Demo - Linking a dSource**
[[DXVIRT200 Getting Started with Continuous Data - DXVIRT200 Getti.mp4]]

### What the dSource Wizard does (High-level)
- Selects:
    - Source environment
    - Database
- Configures:
    - Staging (if required)
    - Credentials
    - Policies (snapshots, retention)
- Starts:
    - Initial full ingestion        
    - Ongoing sync
 You do **not** need to memorize wizard screens for the exam, just the **conceptual flow**
## Mental Model (Very Helpful)
Think of Delphix like **Git for Databases**:

| Git Concept | Delphix Concept  |
| ----------- | ---------------- |
| Repository  | dSource          |
| Commits     | Snapshots / logs |
| Branch      | VDB              |
| Checkout    | Provision        |
## Exam & Knowledge Check Tips
You will often see questions like:
- “Which object is required before provisioning a VDB?”
- “Which object stores compressed source data?”
- “Which object cannot be accessed with database tools?”
Correct answer in all cases → **dSource**
## One-line Exam Summary
- dSource = **compressed, continuously synced copy of source data**
- Created by **linking**
- Lives **inside Delphix**
- Cannot be queried directly
- Used to create **VDBs**
- VDBs can also create other VDBs

---
## **Enabling and Disabling dSources**
Some operations, such as dSource upgrade, are not available unless the dSource is disabled. Disabling a dSource turns off communication between the Delphix Engine and the source database, but it does not remove the configuration. When a disabled dSource is later enabled, it will resume communication and incremental data updates from the source database according to the original policies and data management configurations.

Disabling a dSource is also a prerequisite for several other operations, such as: 
- Database migration
- Upgrading the dSource metadata after the upgrade of the associated data source
- Restoring the source database from a backup
Disabling a dSource will stop further operations on the Delphix Engine related to the dSource.

