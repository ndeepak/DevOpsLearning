# Data Control Tower (DCT)
**Data Control Tower (DCT)**  provides new approaches to general Delphix workflows, delivering a more streamlined developer experience. We will look at the key concepts and features of DCT in this lesson.
A **Data User** is typically a developer, tester, or data engineer who consumes data for non-production workloads.

**Data Control Tower (DCT)**
Data Control Tower (DCT) drives data for DevOps by delivering an integration layer for a broad Delphix deployment. No matter how many applications and data sources Delphix supports, finding and acting upon that data is made easier with DCT. This is achieved by delivering a complete set of Delphix operations available via API calls or Delphix-built integration, creating a central "pane of glass" for central administration, or a modern User Interface for end-user workloads.

**In short:**  
A Data User focuses on **using and manipulating data safely and quickly**, without needing DBA or infrastructure involvement.
![[Pasted image 20251229150517.png]]

![[Pasted image 20251229150614.png]]
DCT is a persistent, container-based application that serves as both an API gateway and orchestrator for Delphix workloads, making it ideal for bulk operations across multiple Delphix engines. It can be deployed as a containerized application or as an **OVA installation**, providing flexibility for different infrastructure environments.  
  
Without DCT, users traditionally relied on working directly with Continuous Data and Continuous Compliance Engine APIs or scripting with the **dxToolkit** and **dxmToolkit**, which are now considered legacy and primarily used in transitional environments. Organizations are encouraged to migrate to the **DCT Toolkit** for streamlined, future-proof automation.

This reliance on engine-specific APIs or legacy toolkits can become especially challenging when managing multiple Delphix engines for complex operations. In such cases, users must know exactly which engine to target in order to identify and act upon a specific Delphix object—a process that DCT simplifies by providing a centralized orchestration layer and unified API gateway.

With Data Control Tower, Delphix objects and actions such as dSources, VDBs, environments, masking jobs, and other object-to-engine relationships are mapped, persisted, and continuously updated in DCT, making automation across multiple engines easier.
```
DCT inherits and relies on existing Continuous Data & Compliance engine constructs. For example dSources and VDBs reside on the Continuous Data engine, and DCT operations must respect those engine relationships.
```
In addition to APIs, developer libraries, and CLI, Data Control Tower has plug-and-play integrations with a number of common DevOps applications such as Terraform and ServiceNow.

Terraform
The Delphix Terraform Provider enables the configuration of Delphix-sourced data to be sourced into ephemeral infrastructure as part of the Terraform build process.
![[Pasted image 20251229150802.png]]

ServiceNow
The Delphix ServiceNow Spoke enables a catalog of all Delphix operations that are currently instrumented into DCT. This includes common operations such as provisioning, refreshing, rewinding, and bookmarking. 
With ServiceNow, administrators are able to configure custom workflows that leverage Delphix operations for a strong alignment to enterprise workflow standards such as inserting approver steps or leveraging notification integrations with applications like slack.
![[Pasted image 20251229150830.png]]

---
**Central Management with DCT**
DCT offers a central management platform for Delphix Administrators to globally monitor system statuses and reports, perform common Delphix operations from a central User Interface, and enforce, integrate, and automate with enterprise authentication and authorization standards.
![[Pasted image 20251229151023.png]]


DCT provides the single "pane of glass" experience for Delphix administrators, firstly by delivering a global reporting experience. From the DCT User Interface, finding and acting upon objects such as VDBs, dSources, Engines and Environments can be done by entering a description in a search bar.

![[Pasted image 20251229151009.png]]

**Data Tags**
In addition to a number of stock reports such as VDB inventory, ingestion source sizing, and storage capacity management, DCT also serves as the Delphix metadata layer with DCT tags. This capability enables the association of any and all business metadata with common Delphix objects. One can assign an application team tag to a number of VDBs for easy curation of consumption reporting or designate a primary and secondary owner for an environment to add accountability.

 DCT also enables the mapping of group attributes from an enterprise directory service to automate and align group membership and access to constrain what users can see and do within DCT APIs and UI. 

![[Pasted image 20251229151003.png]]

---
**The Developer Experience**
DCT delivers a converged developer experience. Whether a developer wants to use DCT APIs, a UI from enterprise standards like ServiceNow, or a Delphix-built UI , DCT provides multiple paths to easily access data. 

With DCT’s Access Control system, developers retain full access to all familiar service functions—including provision, refresh, bookmark, bookmark sharing, and more. These operations are now surfaced directly after selecting the **Refresh** option, ensuring that all legacy developer-oriented capabilities remain available within the new interface. Thanks to DCT’s centralized architecture, developers can perform these actions without being tied to a specific engine.

![[Pasted image 20251229151053.png]]


In the next section, we will dive into the DCT Self-Service features, exploring how they empower teams to accelerate development and testing without waiting on traditional data provisioning cycles. We’ll look at how these capabilities enable developers, testers, and data engineers to instantly access, refresh, and manage data environments on demand—while maintaining compliance and security.

This section will highlight practical scenarios where self-service dramatically reduces bottlenecks and supports agile, AI-driven workflows across multiple brands.

---
# DCT Self-Service Features
```
**RESTRICTION:**  End of life update

Delphix CDE and CCE Self-Service has been deprecated and will reach its end of life in **2025**. Visit our [community blog(opens in a new tab)](https://community.delphix.com/blogs/nicholas-mathison/2024/02/08/delphix-end-of-support-for-delphix-self-service) for more information and guidance on transitioning to Data Control Tower’s improved developer experience.
```

```
**RESTRICTION:**  Delphix CDE and CCE Self-Service unavailable in new installations

As we approach the end of support for Delphix Self-Service (JetStream), we have blocked its usage in new installations to prevent continued rollout. UI, APIs, and CLIs will not work in fresh installs. Engine upgrades to versions released between now and the September end of support date will be unaffected. Please contact your Delphix Account team if your organization does not have a plan to migrate to DCT.
```

The goal of Delphix Data Control Tower self-service is to provide development and testing teams with the ability to manage database administration functions (ie provisioning, snap-shot, rewind) in non-prod environments.  DCT also provides infrastructure teams the ability to granularly govern the delegation of those functions.

In this section, we will learn how DCT Self-Service interacts with the Delphix Continuous Data Engine and how test data flows downstream to assigned data users. 

**Self-Service Data Flow**
Next, let's look at some of the benefits of using  DCT Self-Service in testing.

---
**The DCT Self-Service User Interface (UI)**
Lets learn more about the Overview page, the VDB page, and the Timeline History Workspace: 
Overview
The DCT UI opens to the **Connection Library**, where all external data connections discovered through infrastructure connections are listed. Each entry displays its **status**, **name**, **type**, and **platform**, allowing you to quickly understand the available data sources. From here, you can search or filter to locate specific connections. Selecting a connection lets you access and work with the associated data. In this example, the library contains multiple active connections across several platforms such as Unstructured Files, MSSQL, POSTGRES, and more.
![[Pasted image 20251229154938.png]]
VDBs
You can view details and manage an individual VDB by selecting it from the list. The VDBs page displays all virtual databases in the environment, along with their status, type, platform, engine, compliance state, and last refresh time. Choosing any VDB opens its detailed view and management tools. In this example, numerous VDBs are available across multiple engines and platforms.
![[Pasted image 20251229155005.png]]

The Timeline History Workspace
The screenshot shows the **Timeline History** view for the virtual database (VDB) named **flaskapp_dev.** This view helps administrators track VDB lifecycle events such as **provisioning**, **refreshes**, and **rollbacks**, along with associated timestamps and source relationships.
![[Pasted image 20251229155016.png]]


Let's take a closer look at some of the other features housed within the Timeline History Workspace. 
![[Pasted image 20251229155022.png]]

Lets learn more about each action on the Action dropdown:
1. Create Bookmark : Bookmarks are a way to mark and name a particular moment of data on a timeline. The data represented by a bookmark is protected and will not be deleted until the bookmark is deleted.
2. Refresh : Rebuild the VDB from a chosen point in the parent source’s timeline without creating a new VDB
3. Enable/Disable : Disable = Temporarily remove the VDB from the target environment without deleting its data on Delphix.  Enable = Restore the VDB to the target environment so it can run again.
4. Start/Stop : Start= Brings the VDB **online** so it can accept connections and be used by applications.  
Stop= Shuts down the VDB instance gracefully, making it **offline**.
5. Lock/Unlock : **Lock** prevents actions like refresh or delete, and **Unlock** restores normal access.
6. Delete : Deletes the VDB.
---
**The Timeline History**
The DCT **Timeline History** view gives developers a clear, chronological record of every refresh, snapshot, and parent-source event associated with a VDB. Each entry—such as the refresh operations shown from _AppFS_master_—captures the exact activation time, lineage, and available snapshots.

Timeline History is **readable and actionable** — users can directly restore or refresh from a specific moment shown in the timeline.

**In short:**  
Timeline History is the **source of truth for what happened to a VDB over time**.

By expanding any point on the timeline, users can see the specific snapshot or refresh event they want to return to and initiate a restore directly from that moment. This makes it easy to return a VDB to a precise state in time, ensuring rapid recovery, reproducible testing, and consistent development workflows.:
![[Pasted image 20251229155223.png]]

---
Before we move on, let's do a quick knowledge check of some of the Self-Service Key Terms we learned in this section of the course:

|**Key Term**|**Correct Description**|
|---|---|
|**Data User**|Are able to set, bookmark, and share data points in their container with other data users|
|**Data Administrator**|Control decisions about how resources such as VDBs and vFiles are allocated and shared|
|**Timeline History**|Shows the history of each bookmark and branch|
|**Bookmark**|Mark a moment of data and provide an easy way to share data with other users|
## One-Line Exam-Ready Summary
- **Data User:** Uses and manages data within assigned permissions
- **Data Administrator:** Governs access, resources, and policies
- **Timeline History:** Full lifecycle view of VDB events
- **Bookmark:** Named, protected point in time for reuse and sharing
### Quick intuition to remember
- **Bookmark** = _save & share a moment in time_
- **Timeline History** = _everything that happened to the VDB over time_
- **Data User** = _uses and manages data within allowed boundaries_
- **Data Administrator** = _governs access, resources, and rules_
In conclusion, let's look at some additional resources available to you as a Delphix practitioner.


---
# Additional Resources
**Delphix offers a number of helpful resources to further your knowledge about the Delphix Suite of Products:**
Delphix Documentation [Documentation](https://documentation.delphix.com/)
**Delphix Support Portal** [Support](https://portal.perforce.com/s/product/a3gPA000000A90PYAS/delphix)
**Delphix Community** [Community](https://portal.perforce.com/s/group/0F9PA00000007zB0AQ/delphix-product-discussion)
**Delphix Training** [Training](https://training.delphix.com/)

---
