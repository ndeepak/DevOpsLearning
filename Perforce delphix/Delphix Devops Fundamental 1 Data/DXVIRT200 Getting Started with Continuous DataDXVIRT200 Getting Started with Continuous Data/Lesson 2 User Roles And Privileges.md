# User Roles And Privileges
Lesson 2 of 7
In this lesson, we will focus on the types of Delphix Users including the **System Administrator**, the **Delphix User or Admin**, and the **Self-Service** only data user. Also, the User Roles for Delphix Objects are covered, specifically: Provisioner, Owner, Data Operator and Reader.
## User Roles and Privileges (Delphix)
This lesson answers **three key questions**:
1. **Who manages the Delphix Engine itself?**
2. **Who manages data and environments inside Delphix?**
3. **What exactly can each role do?**
## Types of Delphix Users (Big Picture)
There are **three major user categories** in Delphix:

| User Type                           | Manages What?            | Key Scope                      |
| ----------------------------------- | ------------------------ | ------------------------------ |
| **System Administrator (SysAdmin)** | Delphix Engine           | Platform-level (OS-like tasks) |
| **Delphix User / Delphix Admin**    | Data & environments      | dSources, VDBs, users, groups  |
| **Self-Service Users**              | Data via Self-Service UI | Dev/Test playground            |
**Golden rule**:  
**SysAdmin ≠ Delphix Admin**  
They have **different responsibilities**.
## System Administrator
System Administrators manage the **Delphix Engine itself**, **not data objects**.
The Delphix System Administrator users are responsible for managing the Delphix Engine itself, but not the objects (Environments, dSources, VDBs) within the server. For example, a system administrator is responsible for setting the time on the Delphix Engine and its network address, restarting it, creating new system administrator users (but not Delphix users), and other similar tasks.
![[Pasted image 20251230104819.png]]
A user called sysadmin is the default system administrator user. While this user can be suspended, it may not be deleted. When the Delphix Management application first launches, this user can log in using the username sysadmin and password sysadmin.
**Exam tip**:
> SysAdmin users **cannot be deleted**
## **The Delphix Administrator (Admin)**
The Delphix Administrator can assign privileges to different users.
Delphix users are responsible for managing the environments and datasets within Delphix, such as dSources, virtual databases (VDBs), users, groups, and related policies and resources.
### Special Privileges of Delphix Admins (Very Important)
Delphix Admins have **three unique powers**:
1. Manage other Delphix users
2. Implicit **Owner** privileges on **all objects**
3. Create **new groups and environments**
**Exam trap**:
> SysAdmins manage the engine,  
> Delphix Admins manage the **data and users**

Delphix Admin users **cannot be deleted**

Delphix Admin users can further create **five** **types** of user roles and assign privileges to them**: Owner, Provisioner, Data Operator, Reader, and Self-Service only.**

These privileges apply both to objects, such as dSources and Virtual Databases (VDBs), and to groups, which are containers that hold those objects.

The Delphix Administrator user can assign privileges to groups, dSources, and VDBs. **Privileges are inherited**, meaning that privileges assigned to a group are effective for the dSources and VDBs contained in that group.

_If a user does not have a privilege in relation to an object or group, then he or she has no visibility into that object or group._

## Role-Based Privileges (Core Exam Topic)
Delphix Admins can assign **5 role types**:

|Role|Think of Them As|
|---|---|
|**Owner**|Full control|
|**Provisioner**|Create VDBs|
|**Data Operator**|Refresh & snapshot|
|**Reader**|View-only|
|**Self-Service Only**|Dev/test UI actions|

These roles apply to:
- **Objects** (dSources, VDBs)    
- **Groups** (containers)    

### Privilege Inheritance (Very Important)
**Privileges assigned to a group automatically apply to all objects inside it**
If a user has **no privilege**, they have:
- No access    
- No visibility    
---
## 5. Role Comparison Table (EXAM GOLD)
### Object-Level Privileges

|Action|Owner|Provisioner|Data Operator|Reader|
|---|---|---|---|---|
|Provision VDBs|✅|✅|❌|❌|
|Refresh / Rollback|✅|❌|✅|❌|
|Snapshot|✅|❌|✅|❌|
|V2P (Virtual to Physical)|✅|❌|❌|❌|
|Start/Stop VDB|✅|❌|❌|❌|
|View statistics|✅|✅|✅|✅|

---
### Group-Level Privileges

|Action|Owner|Provisioner|Data Operator|Reader|
|---|---|---|---|---|
|Provision from group|✅|✅|❌|❌|
|Refresh/Rollback VDBs|✅|❌|✅|❌|
|Snapshot all objects|✅|❌|✅|❌|
|Assign Owner privileges|✅|❌|❌|❌|
|View statistics|✅|✅|✅|✅|

## Owners
**Object Privileges** 
- Can provision VDBs from owned dSources and VDBs
- Can perform Virtual to Physical (V2P) from owned dSources and VDBs
- Can access statistics on the dSource, VDB, or snapshot such as usage, history, and space consumption
- Can refresh or rollback VDBs
- Can snapshot dSources and VDBs
- Can start, stop, or re-start VDBs

**Group Privileges**
- Can provision VDBs from all dSources and VDBs in the group
- Can refresh or rollback all VDBs in the group
- Can snapshot all dSources and VDBs in the group
- Can perform Virtual to Physical (V2P) from owned dSources and VDBs
- Can view Templates for policies.
- Can not create, edit, or delete a policy template from the policy page.
- Can assign Owner privileges for dSources and VDBs
- Can access the same statistics as a Provisioner, Data Operator, or Reader
- Can start, stop, or re-start VDBs

## Provisioners
**Object Privileges** 
- Can access statistics on the dSource, VDB, or snapshot such as usage, history, and space consumption
- Can provision VDBs from dSources and VDBs

**Group Privileges**
- Can access statistics on all dSources, VDBs, or snapshots in the group such as usage, history, and space consumption
- Can provision VDBs from all dSources and VDBs in the group

## Data Operators
**Object Privileges** 
- Can access statistics on the dSource, VDB, or snapshot such as usage, history, and space consumption
- Can refresh or rollback VDBs
- Can snapshot dSources and VDBs

**Group Privileges**
- Can access statistics on all dSources, VDBs, or snapshots in the group such as usage, history, and space consumption
- Can refresh or rollback all VDBs in the group
- Can snapshot all dSources and VDBs in the group

## Readers
**Object Privileges**
- Can access statistics on the dSource, VDB, or snapshot such as usage, history, and space consumption

**Group Privileges**
- Can access statistics on all dSources, VDBs, or snapshots in the group such as usage, history, and space consumption

## Self-Service Only
**Object Privileges**
- In the Delphix Self Service UI this user can:
    - Refresh
    - Restore
    - Bookmark
    - Reset
    - Branch
    - Stop/Activate
    - Share

**Group Privileges**
- None
**If a user does not have a privilege in relation to an object or group, then they have no visibility into that object or group. All commands are limited by the privilege level of the user who is executing them. For example, a user with Reader privileges cannot execute the Virtual to Physical (V2P) command.**

**No group privileges**  
**No access to core Delphix UI**
Think of them as **developers working in a sandbox**
## **Self-Service Users**
![[Pasted image 20251230104932.png]]
Delphix Self-Service has two types of users: the admin user and the data user.
Admin users have full access to all report data and can configure Delphix Self-Service, additionally, they can:
- Use the Delphix Engine to add/delete users
- Change tunable settings
- Add/delete tags
- Create and assign data templates and containers
Data users have access to production data provided in a data container. The data container provides these users with a playground in which to work with data using the Self-Service Toolbar.

## **Adding Users**
![[Pasted image 20251230104949.png]]

Adding or Editing a User
The Users page lists all of the current users. You can see the Usernames, email ,and the type of user.
Here you can:
- Add new system administrators with the plus sign
- Change system administrator passwords with the pencil icon
- Delete system administrators with the trashcan icon
- Suspend system administrators with the pause button
- Reinstate system administrators with the play button
![[Pasted image 20251230105225.png]]


User 
When adding a User, you first must determine the User Type.
![[Pasted image 20251230105251.png]]

Assigning Privileges
Privileges can be assigned for each Source and Target.
![[Pasted image 20251230105301.png]]

**The Users page can be accessed by clicking on the Manage tab in the Continuous Data Engine banner and selecting**

## Adding Users (Where & How)
### Where to Manage Users
**Continuous Data Engine → Manage tab → Users**
### User Management Actions
- Add users    
- Edit users    
- Suspend users    
- Reinstate users    
- Assign privileges per source/target    
**Important**:  
You must choose the **User Type first**, then assign privileges.

---
## 9. Key Exam Memory Tricks
- **SysAdmin = Server**    
- **Delphix Admin = Data**    
- **Owner = Everything**    
- **Provisioner = Create**    
- **Data Operator = Refresh**    
- **Reader = See**    
- **Self-Service = Dev playground**    

---
## 10. Exam-Style Quick Checks
✔ Who controls engine settings? → **SysAdmin**  
✔ Who creates environments? → **Delphix Admin**  
✔ Who can run V2P? → **Owner only**  
✔ No privilege means? → **No visibility**


---
**Knowledge Check**
Privileges assigned to a group are effective for dSources and VDBs contained in that group.
**True**
False

Which user type primarily sets up other users with certain roles and privileges
System Administrator
Self-Service User
**Delphix Administrator**
Data Operator