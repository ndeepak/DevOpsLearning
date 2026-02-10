# Policies
Lesson 1 of 5
A **Policy** in the Delphix Continuous Data Engine is a **rule-based automation mechanism** that controls **when** and **how** data operations occur on datasets.

Creating **policies** is a great way to automate the management of datasets in the Delphix Engine. Whether for syncing data, taking snapshots, or refreshing virtual databases, policies ensure that data is ready when needed.
Policies ensure:
- Consistent behavior across environments
- Reduced manual intervention
- Predictable data availability
- Governance and compliance
Policies work **in conjunction with database objects** such as:
- dSources
- VDBs
- Replicated objects

There are 5 categories of policies that the Delphix Continuous Data Engine uses in conjunction with database objects. 
## SnapSync 
How often snapshots of a source database are taken for a dSource.
## VDB Snapshot
How often snapshots are taken of the VDB. 
## Retention
How long snapshots and log files are retained for dSources and VDBs.
## VDB Refresh
Automatic scheduled refreshes of VDBs. The default setting for this policy is None.
## Replica Retention
How long snapshots are retained on replicated namespaces for dSources and VDBs after they have been deleted on the replication source. 

**Note:** Retention of snapshot applies as long as the database is not deleted on the source. If the database is deleted, then the next replication update will delete the database and the retained snapshots on the replication target. 

The Delphix policies area is a way for Delphix Administrators to control and guarantee behaviors within the Delphix Engines. Here, administrators can:
- Control the SnapSync frequency for dSources (default SnapSync occurs daily)
- Control the snapshot frequency for VDBs
- Manage retention of snapshots and logs for dSources and VDBs
- Automate VDB Refreshes and determine VDB Refresh frequency

## **Delphix Policy Types**
There are three policy types offered within the Delphix Continuous Data Engine. Click on the tabs below to learn more about each type of policy and who can set them:

Template
Template policies are named policies that can be saved and applied to other database objects and to groups. These are created on the Manage > Policy screen. 
**Who can set these policies:**
Users with Delphix Admin credentials
Group and object owners 

Default
Default policies exist at the domain level and are applied across all objects in a category. You can modify the settings for a default policy in a category, but you cannot change the name default. 
**Key Rules**
- Name cannot be changed
- Settings can be modified
- Exists for every policy category
**Who can set these policies:** 
Users with Delphix Admin credentials

Custom
Custom policies can only be **applied to a specific database object**. These cannot be saved to be used with other objects. You can create custom policies for dSources during the dSource linking process, as described in the Linking and Advanced Data Management Settings topics for each database platform type. 
**Key Characteristics**
- Cannot be reused
- Cannot be saved as templates
- Often created during dSource linking
**Who can set these policies:**
Users with Delphix Admin credentials
Group and object owners


**Policies applied at the group level will affect all objects in that group. To set different policies for objects in a group, apply the policies at the group level first, then apply policies at the object level. Policies applied at the dataset level override those applied in the group level.**
## Policy Precedence (Very Important for Exams)
**Order of precedence**
1. Group-level policy
2. Dataset-level policy (overrides group-level)
**Rule**
> Policies applied at the dataset level override those applied at the group level.

We will now take a closer look at the use cases for each of the Policy Categories and Types and how to create or modify them within the Delphix Continuous Data Engine.

---
![[Pasted image 20251231110952.png]]
The Policies Screen is accessed by selecting **Policies** under the **Manage** tab located on the banner of the Delphix Continuous Data Engine.
The Policies screen shows the SnapSync policy category by default.  

You can change the policy type you are viewing by clicking on the names of each policy category respectively. The policy category selected is indicated by the blue line underneath the policy category, as well as by the name listed on the Default Policy, and the blue + button.
![[Pasted image 20251231111011.png]]
**The blue + button and pencil and garbage can icons shown above appear for each policy category respectively and function in the same ways.**

## SnapSync Policies
SnapSync policies determine how often snapshots of the source database are taken. SnapSync Policies can only be applied to dSources.

In the Default SnapSync policy, a snapshot is taken daily at 3:30 AM of the timezone your  engine was set to by the System Administrator, and will cancel if not completed within four hours. If SnapSync does not complete within this four hour period, it will restart at the next scheduled daily time until the process is complete.

**You can configure the SnapSync, VDB Snapshot, and VDB Refresh policies with the time zone in which the policy should be scheduled.**

**Key Characteristics**
- Applies **only to dSources**    
- Defines snapshot schedule    
- Controls job timeout behavior    
- Drives data currency for downstream VDBs    

**Default Behavior**
- Runs **daily at 3:30 AM**    
- Uses **engine time zone**    
- Cancels if not completed within **4 hours**    
- Automatically retries at next scheduled window    

**Operational Impact**
- Determines how fresh data is    
- Affects snapshot frequency and storage usage    
- Works together with Retention policy

---
## VDB Snapshot Policies
The VDB Snapshot Policy determines the frequency of VDB Snapshots. VDB Snapshot Policies can only be applied to VDBs.
![[Pasted image 20251231111045.png]]
**Purpose**  
Controls **how often snapshots are taken of a VDB**.
**Key Characteristics**
- Applies **only to VDBs**    
- Independent of dSource SnapSync    
- Useful for:    
    - Rollbacks        
    - Rewinds        
    - Point-in-time restores    
**Why VDB snapshots matter**
- Protects development or testing changes    
- Allows rollback within the VDB lifecycle    
- Improves recovery flexibility
## Retention Policies
A Retention Policy defines how long the Delphix Engine retains snapshots and log files, which are used to rewind or provision objects from past points in time. 

**The Retention policy – in combination with the SnapSync Policy – can have a significant impact on the performance and storage consumption of the Delphix Engine.**
![[Pasted image 20251231111148.png]]
**Purpose**  
Defines **how long snapshots and log files are retained**.
**Applies To**
- dSources    
- VDBs   
**What it controls**
- Snapshot retention duration    
- Log retention duration    
- Advanced retention rules (monthly, weekly, etc.)    
**Critical Rule**
> Snapshot retention must be **equal to or longer than log retention**
**Advanced Retention Options**
- Custom snapshot schedules    
- Monthly or yearly snapshot preservation    
- Example: Keep 3 snapshots on the 1st of every month    
**Performance and Storage Impact**  
Retention + SnapSync frequency directly affects:
- Storage consumption    
- Performance    
- Rollback depth    
**Common Use Cases**
- Regulatory compliance    
- Long-term audit requirements    
- Risk mitigation    
- Development environments    
- Fast rollback to older states

**Policy**
Retention policies can be customized to retain snapshots and logs for longer periods, enabling usage to specific points further back in time. In this example, we have named our Retention Policy 'Long Term'.

To reveal the advanced options menu as seen in this example, you would click on 'Show advanced'. Clicking the downward facing arrow next to the 'Show Advanced' button allows you to create customized retention timeframes. In this example, we have selected an advanced option to keep 3 snapshots on the 1st of every month. To hide the advanced options section, you would click the upward facing arrow in the right hand corner of the advanced options menu. When done selecting the timeframe, click on the **Next** Button
![[Pasted image 20251231111243.png]]

**Datasets**
After editing the policy, select the Group(s) or Dataset(s) to apply the policy to. Remember, policies applied at the group level apply to all objects in the group. Policies applied at the dataset level override those applied in the group level. 
Once the correct Group(s) or Dataset(s) are selected, click the 'Submit' button to apply the policy.
![[Pasted image 20251231111307.png]]
**Viewing the created Policy**
Our new policy is now visible on the Retention Policies page and we can see that we set the policy to keep 3 snapshots on the 1st of each month. Note that this policy states that it applies to 1 dataset, while the default retention policy applies to 3 groups and one dataset.

Notice the difference in color between the trashcan icons on each of our listed Retention policies. As mentioned previously, we can delete created policies, but not default policies
![[Pasted image 20251231111326.png]]

There are some benefits to setting longer retention  times. With increased retention time for snapshots and logs, a longer (older) rollback period for data is allowed. Common use cases for longer retention include:
- Regulatory compliance 
- Frequent application changes and development
- Caution and controlled progression of data
- Reduction of project risk
- Speed of rollback or restoring to older points in time

To support longer retention times, more storage may need to be allocated to the Delphix Engine. The retention time for snapshots must be equal to or longer than the retention time for logs.

---
## VDB Refresh Policies
VDB Refresh Policies can only be applied to VDBs, and are only used in cases where the user needs to re-provision VDBs from their source at regular intervals. 
![[Pasted image 20251231111411.png]]
**Purpose**  
Automates **scheduled refreshes of VDBs** from their source.
**Key Characteristics**
- Applies **only to VDBs**    
- Default setting is **None**    
- Used when VDBs must be reset regularly    
**Typical Use Cases**
- Training environments    
- QA environments    
- Automated test cycles    
- Environments that must stay aligned with production    
**Important Behavior**
- Refresh **destroys changes** made in the VDB    
- Re-provisions from the source snapshot
## Replica Retention Policies
Replica Retention policies define how long the snapshots are retained on replicated namespaces for dSources and VDBs, after they have been deleted on the replication source.
![[Pasted image 20251231111427.png]]
**Purpose**  
Extends the **lifetime of snapshots on a replication target** after they are deleted on the source.
**Key Characteristics**
- Defined **on the replication target**    
- Can apply to:    
    - Entire replica namespace        
    - Specific groups        
    - Individual datasets        
- Can **only extend**, not reduce, snapshot lifetime    
**Why this exists**  
Normally:
- Deleted snapshots on source are deleted on target    
Replica Retention allows:
- Continued access to deleted snapshots    
- Additional recovery or provisioning options    
**Limitations**
- Snapshots cannot be deleted manually    
- Removal happens only when:    
    - Policy duration expires        
    - Dataset is deleted        
    - Dependency (e.g., Oracle CDB) is removed        
**Optimization Note**  
Point-in-time provisioning may not be available to save disk space.

---

Normally, the snapshots that have been deleted on the replication source engine are also deleted on the replication target engine. 

A new retention policy is introduced to provide an extended lifetime of such snapshots on the replication target. 

The Replica Retention Policy is targeted and defined on the replication target. This policy can be applied to an entire replica namespace or could target specific groups or dSource/VDBs within the replica namespace.

The replica retention policy can only be used to extend (not to reduce) the lifetime of the replica snapshots.

Use the replica snapshots on the replication target to provision or refresh VDBs. Point-in-time provisioning may not be possible for these snapshots; this is done to optimize the disk space usage on the replication target.

The replica retention policy runs automatically on a schedule to cleanup expiring snapshots or whenever a replication receive job is executed.

Extended Replica Snapshots can be deleted in the following cases:

1.  Similar to Replicated snapshots, Extended Replica Snapshots cannot be deleted manually. They can only be removed by adjusting the policy duration so the snapshot is no longer covered.    
2.  If the entire dSource or VDB is deleted, the extended replica snapshot will be deleted on the replication target as well.    
3. Oracle virtual PDBs require their CDB to be present and, if the CDB is deleted or is not replicated, then the extended replica snapshots on both the deleted CDB as well as the dependent virtual PDB will be deleted on the replication target. This can happen in a rare scenario where an Oracle virtual PDB is migrated from one CDB to another. Once the virtual PDBs snapshots that reference the old CDB are deleted, the old CDB can also be deleted. The snapshots on the virtual PDB that depend on the old CDB will not be covered by extended replica retention on the replication target.

---
## Knowledge Check
**Policies applied at the _______ level override those applied in the group level.**
Dataset-level policies take precedence over group-level policies.

**SnapSync Policies can only be applied to _______.**
dSources
SnapSync controls snapshots of source databasesm which only exists for dSources.
Acceptable responses: Answer 1, dSources, DSources, d Sources, dsources

**The Replica Retention Policy can only be used to_______ the lifetime of the replica snapshots.**
extend (not to reduce) 
reduce (not to extend) 
_Replica Retention only extends snapshot lifetime beyond source deletion._

---
