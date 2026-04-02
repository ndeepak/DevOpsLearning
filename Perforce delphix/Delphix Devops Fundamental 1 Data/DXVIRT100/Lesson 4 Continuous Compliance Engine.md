# Continuous Compliance Engine
Once data has been ingested into the Delphix Continuous Data Engine and a dSource has been linked, the Delphix Continuous Compliance Engine can be used to secure sensitive data through masking. It's important to note that masking is not dependent on virtualization—there is zero mandatory dependency—so it can be applied independently of VDBs 

The **Continuous Compliance Engine (CCE)** is Delphix’s **data security layer**.
> Its job is to **find sensitive data and secure it** (mask or tokenize it), especially in **non-production environments**.
### Key point (very exam-important):
- **Masking is NOT dependent on virtualization**
- You can mask:
    - Physical databases
    - VDBs
    - Flat files
    - Cloud data
So even without Delphix VDBs, **CCE still works**.
## **The Delphix Continuous Compliance Engine**
![[Pasted image 20251229141900.png]]
While masking data within the Delphix Continuous Compliance Engine is not a mandatory step prior to the process of provisioning and replicating VDBs, it is an extremely important step if your goal is protecting and securing sensitive data. It is legally required to mask sensitive data.

The Delphix Continuous Compliance Engine uses an automated approach to protecting non-production environments, replacing confidential information such as social security numbers, patient records, and credit card information with fictitious, yet realistic data.

The Delphix Continuous Compliance Engine identifies what data should be secured. Profiling jobs can be executed across multiple sources to provide businesses with an enterprise-wide view of sensitive data risk. The Delphix Continuous Compliance Engine identifies sensitive information and automates data masking wherever data resides—from mainframes to modern cloud platforms. 
## Why Masking Is Critical (Not Optional)
Masking is:
- **Legally required** (GDPR, HIPAA, PCI-DSS, CCPA)
- Essential for:
    - Dev        
    - QA        
    - UAT        
    - Training        
    - Outsourced teams
Without masking:  
❌ PII leakage  
❌ Audit failures  
❌ Legal penalties

## What the Compliance Engine Actually Does
The CCE performs **three major functions**:
1. **Identify sensitive data** (Profiling)
2. **Define rules** (Rule Sets)    
3. **Secure the data** (Masking / Tokenization)

![[Pasted image 20251229141912.png]]
**The Benefits**
There are several benefits to using the Delphix Continuous Compliance Engine to mask and secure sensitive data. Unlike traditional solutions which take months to implement, Delphix Continuous Compliance processes can be implemented in days. APIs can be used to automatically provision masked data, clean up, and tear down environments for DevOps and CI/CD.
Lets explore more about the benefits of using the Delphix Continuous Compliance Engine:
4. Reduces Risk: by using masked data suitable for a large number of business activities
5.  Identifies Sensitive Data:  by identifying the location of sensitive data automatically with profiling tools
6. Masks Data Quickly : with a simple to use User Interface that doesn't require coding
7. Maintains Referential Integrity: with the help of patented, repeatable, and deterministic algorithms
8. Enables Data Sharing: **by enabling sharing of masked data safely and easily**
9. Lowers Costs : by automating the entire masking process, securing only essential data, and provisioning only the data you need
Before we continue, let's take a look at some of the Key Terms used within the Delphix Continuous Compliance Engine.
## Application
An Application is a tag that is assigned to one or more environments. In order for an Environment to be created, an Application has to be created first.
Think: _Project / Business Unit_
## Environment
Environments are used to group certain sets of objects within the Delphix Continuous Compliance Engine. They can be thought of as folders/containers where a specified user can create and manage connectors, rule sets, and jobs.  An environment:
- Defines the scope of work in the Delphix Continuous Compliance Engine
- Contains multiple database and file connections
- Stores the connection information, plus masking rules
An **Environment**:
- Groups connectors, rule sets, jobs
- Defines scope and permissions
- Acts like a **folder/container**
Contains:
- Multiple connectors
- Rule sets
- Inventory
## Connector
 A connector is an object in which the Delphix Continuous Compliance Engine stores connection information. Connectors are the way users define the data sources to which the Delphix Continuous Compliance Engine should connect. Connectors are grouped within environments. Connection to data sources is required for all masking activities. The Delphix Continuous Compliance Engine allows you to create both database and file connections. Examples of these include: 
- Database Connectors such as Oracle, MS SQL Server, and SAP ASE    
- File Connectors such as Filesystem Mount Point, SFTP, NFS, CIFS FTP and others    
- Extended Connectors where customers can upload their own JDBC drivers and connect to virtually any data store and protect it    
No connector → no masking
## Classifier
A **classifier** is a detection rule the Compliance Engine uses to scan your data and determine whether a column or field contains a particular type of sensitive information—such as:
- Social Security numbers    
- Credit card numbers    
- Dates of birth    
- Email addresses    
- Names    
- Phone numbers    
- Custom company-specific identifiers    
Classifiers answer:
> “What kind of sensitive data is this?”
## Profiling
Profiling jobs use Profiler Sets to determine the set of Classifiers to use in identifying sensitive data in an Inventory
- A Delphix Continuous Compliance Engine administrator (a user with the appropriate role privileges) can create/add/update/delete Profiler Sets and Classifiers    
- The Profiler determines how we search for sensitive fields    
- Classifiers are grouped by DOMAINS. A domain is a categorization of a type of sensitive data. Each domain can be created to use basically unlimited classifiers to detect it. For instance, First Name, Last Name, Address, Credit Card, SSN, and Bank Account Number Expressions could constitute a Financial Profiler Set    
- The Continuous Compliance Engine comes with four predefined Profiler Sets: Standard, Financial and Healthcare (HIPAA) and ASDD Standard. The Engine Admin can create/add/update/delete these Profiler Sets   
- Delphix’s Automated Sensitive Data Discovery (ASDD) is a feature within Delphix Compliance Services that automates the identification and classification of sensitive data (e.g., PII, financial data) across diverse data sources using advanced classifiers (LIST, TYPE, PATH, REGEX). It supports statistical sampling, customizable profile sets, and seamless integration with platforms like Azure, Snowflake, and Databricks to ensure data privacy and compliance with regulations like GDPR, CCPA, and HIPAA.    
**Profiling** scans data to:
- Find sensitive fields
- Classify them into domains
Uses:
- Profiler Sets
- Classifiers
- Sampling & regex
Types:
- Column-level profiling
- Data-level profiling

### Profiler Sets & Domains
- Classifiers are grouped into **Domains**    
- Domains form **Profiler Sets**    
Built-in Profiler Sets:
- Standard    
- Financial    
- Healthcare (HIPAA)    
- ASDD Standard
## Rule Set
A rule set points to a collection of tables or flat files that the Delphix Continuous Compliance Engine uses for profiling and masking data. There are a number of operations that you can perform while working with a rule set. You can create a new rule set, edit an existing rule set, refresh a rule set in case of disparity with the database, copy a rule set, and delete a rule set. Delphix can use PATTERN to detect files whose names match specific regex patterns.
A **Rule Set**:
- Points to tables or files    
- Defines:    
    - What to scan        
    - What to mask        
    - How to mask        
Operations:
- Create    
- Edit    
- Refresh    
- Copy    
- Delete
## Rule Set Details
A Rule set now encompasses both the inventory and configuration details for data masking. Within a Rule set, you’ll find a listing of database tables or files—referred to as objects—which can be expanded to reveal their columns or fields. Each column or field includes metadata such as data classification and the selected masking algorithm, defining how the data will be secured.
Inside a Rule Set:
- Tables / files    
- Columns / fields    
- Data classification    
- Masking algorithm
📌 This is where **security decisions happen**.
## Masking Algorithms
Masking algorithms create a structurally similar but fictitious version of data, protecting sensitive information while generating a functional substitute that can be used for purposes such as application development and testing.
Masking algorithms:
- Replace real data    
- With realistic but fake values    
- Preserve:    
    - Format        
    - Length        
    - Relationships        
Examples:
- Name → random name    
- CC → valid-looking CC    
- Email → fake domain
---
The process of identifying and masking sensitive data with the Delphix Continuous Compliance Engine can be generalized into two main steps. 
## Identify Sensitive Data - Profiling
Questions to ask
![[Pasted image 20251229142642.png]]
## Create the Ruleset
Steps below
![[Pasted image 20251229142649.png]]

---
## **How Delphix Identifies Sensitive Data**
The Delphix Continuous Compliance Engine helps you quickly identify sensitive data. This sensitive data identification is done using two different methods, **column level profiling,** and **data level profiling:**
Column Level Profiling
![[Pasted image 20251229142740.png]]
Data Level Profiling
![[Pasted image 20251229142746.png]]
**REGEX is short form for "Regular Expressions", which are a string of text that allow you to create patterns that can be used to match data.** 
Delphix supports **two security methods**:
### Masking (Anonymization)
- Irreversible    
- Best for non-production    
- Most common    
### Tokenization (Pseudonymization)
- Reversible    
- Uses token vault    
- Useful when original data may be needed later

For both column and data level profiling, when data is identified as sensitive, Delphix recommends/assigns particular algorithms to be used when securing the data. The platform comes with several dozen pre-configured algorithms which are recommended when the profiler finds certain sensitive data.

---
****How Delphix Secures Your Sensitive Data****
Delphix strives to make available multiple methods for securing data, depending on your needs. The two secure methods Delphix currently supports are masking (anonymization) and tokenization (pseudonymization).

Masking
clickable link:  [https://help.delphix.com/cc/current/content/algorithm_frameworks.htm  
](https://help.delphix.com/cc/current/content/algorithm_frameworks.htm)
![[Pasted image 20251229142831.png]]

Tokenization
![[Pasted image 20251229142848.png]]
There are two ways to mask data in the Delphix Continuous Compliance Engine; In-Place Masking and On-The-Fly Masking.
![[Pasted image 20251229142925.png]]
## Advantages of In-Place Masking:
- Allows Delphix Continuous Compliance Engine to mask the data in the existing environment
- Masks only the columns you flag
- Lack of sensitive production data on the target database or in transit
- Requires only a production source and non-production target environment
- Use of all insert statements leads to better performance

## Advantages of On-The-Fly Masking:
- Lack of sensitive production data on the target database or in transit
- Requires only a production source and non-production target environment
- Use of all insert statements leads to better performance
- Allows Delphix Continuous Compliance Engine to mask the data in the existing environment    
- Masks only the columns you flag

Now that we have learned more about how the Delphix Continuous Compliance Engine masks sensitive data, let's take a look at the User Interface (UI).

---

**The Delphix Continuous Compliance User Interface (UI)**
## Compliance Engine UI (High-Level Flow)
1. Create **Environment**    
2. Add **Connector**    
3. Create **Rule Set**    
4. Run **Profiling**    
5. Verify results    
6. Run **Masking job**    

All available via:
- UI    
- APIs (CI/CD ready)

Environments
The Environments page is where a new environment can be added, or an existing environment can be accessed, imported or exported. The Connector, Rule Set, and Inventory tabs are accessed by clicking on the environment name.
![[Pasted image 20251229143150.png]]

Connector
The Connector tab is where the Delphix Continuous Compliance Engine stores database connection information.
![[Pasted image 20251229143200.png]]

Rule Set
The Rule Set tab is where the collection of tables or flat files that the Delphix Continuous Compliance Engine uses for profiling, masking, and certifying data are created.
![[Pasted image 20251229143212.png]]

Rule Set Details
Rule set details describe all of the data present in a particular ruleset and defines the methods which will be used to secure it. Inventories typically include the table or file name, column/field name, the data classification, and the chosen algorithm.
![[Pasted image 20251229143222.png]]

There are a few ways that many of the standard masking job tasks can be completed within the Delphix Continuous Compliance Engine. There are easy to use tabs, buttons, and menus available within the Environments page as seen above. These operations can also be completed via APIs.

![[Pasted image 20251229143247.png]]

1. In this example, a new Environment is being created.
![[Pasted image 20251229143325.png]]

2. In this example, we are choosing an Oracle Database
![[Pasted image 20251229143341.png]]

3. Define
![[Pasted image 20251229143409.png]]

4. Profile Data/Verify Results
![[Pasted image 20251229143449.png]]
The Continuous Compliance Engine comes with many predefined Profiler Sets. In this example, we also have two additional Profiler Sets. Additionally, **Automated Sensitive Data Discovery (ASDD)** enhances compliance by automatically identifying and classifying sensitive data across environments, ensuring that all Profiler Sets are accurately and efficiently applied.
5. Mask Data
In this example, we are running a masking job called "Drupal 9 Custom App Masking"
![[Pasted image 20251229143512.png]]

---
Before we move on and learn more about the Data Control Tower (DCT), let's do a quick knowledge check of some of the Key Terms we learned in this section of the course:
# Knowledge Check — Correct Answers
### Match each Key Term with the correct description
- **Connector** →  
    ✅ _Stores database connection information and defines the data source used_    
- **Profiling** →  
    ✅ _Running the job to scan and identify sensitive data within the environment_    
- **Tokenization** →  
    ✅ _A form of encryption that uses reversible algorithms to restore data to original state_    
- **Environment** →  
    ✅ _Groups certain sets of objects within the Delphix Continuous Compliance Engine_    
- **Rule Set** →  
    ✅ _Points to a collection of tables or flat files used for profiling and masking_    
- **Masking** →  
    ✅ _Replaces values with fictitious but realistic data_

---
## One-Line Summary (Remember This)
> The Delphix Continuous Compliance Engine automatically discovers sensitive data and secures it through masking or tokenization, enabling safe, compliant use of data across non-production environments without exposing real PII.