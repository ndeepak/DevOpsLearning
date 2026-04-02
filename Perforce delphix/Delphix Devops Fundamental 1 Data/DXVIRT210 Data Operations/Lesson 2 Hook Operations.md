# Hook Operations
Lesson 2 of 5

**Hook operations** allow you to execute custom operations at select points during linking sources and managing virtual datasets. For example, you may want to prevent your monitoring systems from triggering during VDB startup and shutdown. In this case, you would leverage pre- and post-hooks to run required scripts for VDB start/stop operations.
**Hook Operations** allow Delphix administrators to **run custom scripts or commands at specific points** during dataset lifecycle events such as:
- Linking a dSource
- Taking a snapshot
- Provisioning a VDB
- Refreshing or rewinding a VDB    
- Starting or stopping a VDB

Hooks extend Delphix’s built-in automation by allowing **environment-specific or application-specific logic** to be executed at precise moments.

You can construct hook operation lists through the Delphix Management application or the Command Line Interface (CLI). You can either define the hooks as part of the provisioning process or edit them on virtual datasets that already exist. Unix-based operating systems will execute hook scripts in **bash**, while Windows operating systems will execute using **PowerShell**. Below are the available Hook Operations for dSources, VDBs, and Staging Hosts: 
## Hook Operations Scope
Hooks are available for:
- dSources    
- VDBs    
- Staging Servers (limited platforms)   
Hooks can be:
- Defined during provisioning or linking    
- Added or modified later on existing datasets    
- Managed through UI or CLI
## dSource Hooks
dSource hooks are tied to **SnapSync operations**.
## Pre Sync
**When it runs**
- Before SnapSync starts    
**Purpose**
- Prepare the source database for a clean snapshot    
**Common Use Cases**
- Quiesce database    
- Pause application writes    
- Stop interfering processes    
**Failure Behavior**
- If Pre Sync fails, SnapSync may fail or be prevented
## Post Sync
**When it runs**
- After SnapSync completes    
**Important Behavior**
- Runs **regardless of SnapSync success or Pre Sync failure**   
**Purpose**
- Restore environment to normal state    
**Common Use Cases**
- Resume application writes    
- Restart services stopped in Pre Sync    
- Cleanup temporary changes
## **VDB Hooks**
VDB hooks are more extensive because VDBs have a full lifecycle.
## Configure Clone
- Operations performed after initial provision or after a refresh.
- This hook will run after the virtual dataset has been started.
- During a refresh, this hook will run before the Post Refresh hook.
## Pre Refresh
- Operations performed before a refresh.
- This hook will run before the virtual dataset has been stopped.
- These operations can cache data from the virtual dataset to be restored after the refresh completes.

## Post Refresh
- Operations performed after a refresh.
- This hook will run after the virtual dataset has been started and after the Configure Clone hook.
- This hook will not run if the refresh or Pre Refresh hook operations fail.
- These operations can restore cached data after the refresh completes.

## Pre Rollback
- Operations performed before a rollback, also known as rewind.
- This hook will run before the virtual dataset has been stopped. 
- These operations can cache data from the virtual dataset to be restored after the rewind completes.

## Post Rollback
- Operations performed after a rollback, also known as rewind. 
- This hook will not run if the rewind or Pre Rewind hook operations fail. 
- This hook will run after the virtual dataset has been started. 
- This hook will not run if the rewind or Pre Rewind hook operations fail. 
- These operations can restore cached data after the rewind completes.

## Pre Snapshot
- Operations performed before a snapshot.
- These operations can quiesce data to be captured during the snapshot, or stop processes that may interfere with the snapshot.

## Post Snapshot
- Operations performed after a snapshot.
- This hook will run regardless of the success of the snapshot or Pre Snapshot hook operations.
- These operations can undo any changes made by the Pre Snapshot hook.

## Pre Start
- Operations performed before the startup of a VDB or vFile.
- These operations can be used to initialize configuration files or stop processes that might interfere with the virtual dataset.

## Post Start
- Operations performed after the startup of a VDB of vFile.
- These operations can be used to clean up any temporary files, or restart processes that may have been stopped by a Pre-Start hook, or log notifications.

## Pre Stop
- Operations performed before the shutdown of a VDB or vFile.
- These operations can quiesce data or processes prior to the virtual dataset shutdown.

## Post Stop
- Operations performed after the shutdown of a VDB or vFile.
- These operations can be used to log notifications, clean up any temporary files, or stop/restart related processes.

## Staging Server Hooks
Staging Server hooks are currently applicable to SAP ASE and staged plugins (Db2, HANA, and PostgreSQL) environments, and execute on the configured staging server.
1. Pre Validated Sync    
    - Operations performed on a staging server before validated sync.
    - This hook will run before the validated sync operation whenever the validated sync run is triggered.
    
2. Post Validated Sync       
    - Operations performed on staging server after validated sync.
    - This hook will run after the validated sync operation whenever the validated sync run is triggered.  
![[Pasted image 20251231114154.png]]
**Setting Hook Operations**
Hook operations can be created in the Hooks tab of both the Add dSource or Add VDB wizards. The scrollable list of Hook Points can can be seen here. To add a new Hook Point or to link in a Hook Template, click on the plus sign.   

To edit Hook operations on a dataset, navigate to the **Datasets** page and select the dataset you would like to edit from the left hand menu. Click on the **Configuration** tab and then the **Hooks** Tab.  As with the dSource and VDB Wizards, a scrollable list of Hook Points is visible. To create a new Hook Point or create one from a template, click on the plus sign. 
![[Pasted image 20251231114219.png]]
**Hook Templates**
Each Delphix object will have its own set of hooks you can create. To easily manage hooks across multiple datasets, you can create Hook Templates to apply the same hook to many objects. You can use Hook Templates to store commonly used operations, which allows you to avoid repeated work when an operation is applicable to more than a single virtual dataset. You manage templates through the Delphix UI by Clicking on the Manage tab in the Delphix Continuous Data Engine UI banner, and selecting Hook Templates. 

To create a new Hook Template, click on the plus next to **Hook Templates.** The Template Menu seen below will pop up.
![[Pasted image 20251231114239.png]]
![[Pasted image 20251231114247.png]]
The **New Template** wizard provides a place to name the template, select the type, add a description, set up credential environment variables (by clicking the plus sign), and add a script to the Content section. Once filled in, clicking create will create and save the template.

Once created, your Hook Templates will be listed on the Hook Template Page and can be accessed via the dSource and VDB Wizards, as well as the Hook tab on the Datasets page.  The template components can be edited by clicking on the pencil icons located next to the template name and components. 
![[Pasted image 20251231114501.png]]
## **Importing and Exporting a Hook Template**
It is possible to both import and export Hook templates. Click on the boxes below to see the steps for each of these operations: 
## Importing a Hook Template
1. In the Datasets panel, select a dataset.
2. Click the Configuration tab.
3. Within the Configuration tab, click the Hooks tab. 
4. Select the hook you wish to edit.
5.  Click the Plus icon to add a new operation. 
6.  Click Import.
7. Select the template to import.
8. Click Import.
9. When you have set all hook operations, click Check to save the changes.

## Exporting a Hook Template
1. In the Datasets panel, select a dataset.
2. Click the Configuration tab.
3. Within the Configuration tab, click the Hooks tab.
4. Select the hook to edit.
5. Click the Plus icon to add a new operation.
6. Select the type of operation.
7. Click the text area and edit the contents of the operation.
8. Click Export.
9. Enter a Name for the template.
10. Enter a Description detailing what the operation does or how to use it.
11. Click Export.

**For Information on how to set up Hook operations via the Command Line Interface (****CLI), visit the Delphix Documentation Page:** 
# **Knowledge Check**
Staging Server hooks are currently applicable to SAP ASE and staged plugins (Db2, HANA, and PostgreSQL) environments only.
True
False