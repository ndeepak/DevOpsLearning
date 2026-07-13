# Oracle RAC Notes
# What is Oracle RAC?

**Oracle Real Application Clusters (RAC)** is a technology that allows **multiple servers (nodes)** to run Oracle Database software and **access a single shared database simultaneously**.

In simple terms:
- Multiple machines
- One database
- Workload shared across all nodes

This provides **high availability, scalability, and fault tolerance**.

---
Oracle RAC =
> Multiple servers running Oracle together while accessing the SAME database stored on shared storage.

Think of it like:
```scss
Server 1 ----\  
				\  
Server 2  --------------> Shared Oracle Database  
				/  
Server 3 ----/
```

All nodes:
- run Oracle instance
- access same datafiles
- work together as one database system

---
# First Understand the Problem RAC Solves
Imagine a bank application running on **one Oracle server**.
If that server crashes:
- database goes down
- application stops
- users cannot transact
This is called a **Single Point of Failure (SPOF)**.
Oracle RAC removes that issue.

---
# Important Terminology

## A. Node
A physical or virtual server participating in RAC.

Example:
- racnode1
- racnode2

Each node:
- has CPU/RAM
- runs Oracle instance
- runs cluster services
## B. Instance
An Oracle instance is:
- memory structures (SGA)
- background processes (PMON, DBWR, LGWR etc.)
Each RAC node has its OWN instance.
Example:

|Node|Instance|
|---|---|
|racnode1|PROD1|
|racnode2|PROD2|

But both access SAME database files.
## C. Database
The actual datafiles:
- tables
- indexes
- redo logs
- control files

Stored on:
- SAN
- ASM disks
- shared storage

Shared by all RAC nodes.

---
# RAC Architecture
Here’s the full picture:

```scss
               CLIENTS
                   |
            SCAN / VIP
                   |
    --------------------------------
    |                              |
+-----------+              +-----------+
| NODE 1    |              | NODE 2    |
| Instance1 |              | Instance2 |
+-----------+              +-----------+
      |                           |
      |----- Private Interconnect |
                  |
         Shared Storage (ASM)
```

# Main Components of RAC
# A. Oracle Clusterware
This is the HEART of RAC.

It manages:
- node membership
- failover
- cluster health
- VIP management
- fencing
- startup/shutdown

Without Clusterware:
- RAC cannot function

Important services:
- CRS
- CSSD
- EVMD
# B. Shared Storage
All nodes must access SAME storage.

Usually:
- SAN
- iSCSI
- Fiber Channel
- ASM disks

Contains:
- datafiles
- OCR
- voting disks
- redo logs
# C. ASM (Automatic Storage Management)
ASM is Oracle’s volume manager + filesystem.

Instead of:
```
/ext4/xfs filesystems
```

Oracle uses:
```
+DATA+FRA
```

ASM handles:
- striping
- mirroring
- disk balancing

System engineer often manages:
- multipath
- udev rules
- ASM disks visibility

# D. Private Interconnect
Dedicated high-speed network between RAC nodes.

Used for:
- heartbeat
- cache fusion
- cluster communication

Usually:
- 10G/25G network
- low latency

If interconnect fails:
- cluster instability
- node eviction
- split-brain risk

# E. Public Network
Client-facing network.
Applications connect here.

Used for:
- SQL connections
- listener traffic

# 6. VIP (Virtual IP)

Each node has:

- public IP
- virtual IP (VIP)

Example:

|Node|Public IP|VIP|
|---|---|---|
|node1|192.168.1.10|192.168.1.20|
|node2|192.168.1.11|192.168.1.21|

If node1 dies:
- VIP automatically relocates
- clients reconnect faster

Without VIP:
- clients wait for TCP timeout



# 7. SCAN (Single Client Access Name)

Very important concept.

Instead of applications knowing every node:

```
db.company.com
```
SCAN resolves to multiple IPs.

Benefits:
- simplified connectivity
- load balancing
- easier node addition


# 8. How RAC Actually Works
Now the real magic.
# Scenario
Suppose:
User A connects to NODE1.
NODE1 needs a data block currently cached in NODE2 memory.

Without RAC:
- disk read required

With RAC:
- NODE2 sends block directly from memory

This is called:

# Cache Fusion
# 9. Cache Fusion
One of RAC’s core technologies.

## What it does
Transfers data blocks:

- node-to-node
- through memory
- over interconnect

Instead of disk.

Benefit:
- faster synchronization
- reduced disk I/O
# Example
```
NODE1 wants block XNODE2 already has block XNODE2 sends block directly to NODE1 RAM
```

Very fast.

# 10. Split Brain Problem
Critical clustering concept.

Occurs when:
- nodes lose communication
- both think they are master

Can corrupt database.

Oracle prevents this using:
- voting disks
- clusterware
- node eviction

# 11. Voting Disk
Used to determine:
- which nodes are alive
- cluster quorum

If node loses voting access:
- Oracle may evict it

Purpose:
- prevent split brain

# 12. OCR (Oracle Cluster Registry)
Stores cluster configuration:
- node info
- resources
- services
- VIPs

Very important cluster metadata.


# 13. Node Eviction
If a node becomes unhealthy:
- Oracle forcibly removes it

Called:
```
Node eviction
```

Usually due to:
- interconnect latency
- heartbeat failure
- CPU starvation
- storage delay

You may see:

```
reboot advisorycssd eviction
```

# 14. RAC Startup Sequence
Simplified flow:
```
OS starts   ↓Clusterware starts   ↓ASM starts   ↓Database instances start   ↓Services become available
```

# 15. Common RAC Services
Important system engineer commands:

## Check cluster
```
crsctl stat res -t
```

## Check node membership
```
olsnodes -n
```

## Check cluster health
```
crsctl check cluster
```

## ASM disks
```
asmcmd lsdg
```

# 16. RAC Networking Requirements
Oracle RAC networking is strict.

Usually requires:

|Network|Purpose|
|---|---|
|Public|Client access|
|Private Interconnect|Node communication|
|VIP|Failover|
|SCAN|Load balancing|

DNS and hostname resolution must be PERFECT.

Bad DNS causes many RAC issues.

# 17. Storage Requirements
All RAC nodes must see SAME disks.

Important for system engineers:
- multipath
- persistent naming
- udev
- permissions
- latency
# 18. What System Engineers Usually Handle
You are heavily involved in:

## OS Preparation
- kernel params
- limits.conf
- hugepages
- NTP/chrony
- packages

## Storage
- SAN zoning
- multipath
- ASM disks
- iSCSI/Fiber

## Networking
- VIPs
- bonding
- MTU
- interconnect tuning

## Cluster Troubleshooting
- node eviction
- CRS failures
- heartbeat issues
- DNS issues

## Patching
- GI patching
- rolling patching
- reboot coordination
# 19. RAC vs Standalone Oracle

|Feature|Standalone|RAC|
|---|---|---|
|Servers|1|Multiple|
|Availability|Lower|High|
|Scalability|Vertical|Horizontal|
|Failover|Limited|Automatic|
|Complexity|Simple|Complex|
|Cost|Lower|Higher|
# 20. RAC vs Active-Passive Cluster
Traditional cluster:

```
One activeOne standby
```

RAC:

```
All active simultaneously
```

This is called:

# Active-Active clustering
# 21. Real-World Example
Imagine a banking application.

100,000 users connected.

If one RAC node crashes:

- sessions failover
- other nodes continue
- database remains online

Users may only notice:

- brief delay

That’s why RAC is used in:

- banks
- telecom
- airlines
- stock exchanges
# 22. Major RAC Challenges
RAC is powerful but difficult.

Common issues:
- interconnect latency
- storage latency
- split brain
- node eviction
- DNS mismatch
- time sync problems

RAC is VERY sensitive to infrastructure quality.

# 23. RAC and Grid Infrastructure
When installing RAC, Oracle installs:

# Oracle Grid Infrastructure (GI)
GI includes:
- Clusterware
- ASM

Then:

- Oracle Database software installed separately


# 24. Important RAC Directories
Typical paths:

```
/u01/app/grid/u01/app/oracle/u01/app/19c/grid
```

Logs:
```
$GRID_HOME/log
```

Diagnostic tools:
```
adrci
```

# 25. High-Level RAC Flow

```scss
Client connects
      ↓
SCAN resolves node
      ↓
Listener accepts connection
      ↓
Instance processes request
      ↓
Cache Fusion syncs blocks if needed
      ↓
Shared storage updated
```

# 26. RAC Mental Model (Most Important)

Think of RAC as:

```
Multiple Oracle instances
behaving like
ONE database system
```

The biggest engineering challenge is:

- synchronization
- consistency
- communication

Oracle solves that using:

- Clusterware
- ASM
- Cache Fusion
- Voting disks
- OCR
- Interconnect


# 27. What You Should Learn Next
As a system engineer, next focus areas should be:

1. Oracle Grid Infrastructure
2. ASM deep dive
3. RAC networking
4. CRS architecture
5. RAC troubleshooting
6. Node eviction analysis
7. OCR/Voting disk internals
8. RAC patching
9. Interconnect tuning
10. Oracle services/listeners

# 28. Important RAC Logs
Useful locations:
```
GRID_HOME/log
```

Cluster alert logs:
```
crsd.logcssd.logevmd.log
```

Database alert log:

```
alert_PROD1.log
```

# 29. Final Understanding
RAC is essentially:

- a cluster of servers
- sharing one database
- coordinated by Clusterware
- synchronized using Cache Fusion
- protected by voting/quorum logic
- backed by shared storage

The infrastructure side is JUST as important as DBA work.

Poor:
- network
- storage
- DNS
- time sync

can completely destabilize RAC.

# 30. Core Concepts You Must Remember
## Memorize These
- Node
- Instance
- Database
- Clusterware
- ASM
- VIP
- SCAN
- Interconnect
- Cache Fusion
- OCR
- Voting Disk
- Node Eviction
- Split Brain

These are the foundations of Oracle RAC.


# What Does Oracle RAC Do?
Oracle RAC enables:
- **Load balancing** – distributes workload across nodes
- **High availability** – if one node fails, others continue
- **Scalability** – add more nodes to increase performance
- **Fault tolerance** – reduces single points of failure

---

# How Oracle RAC Works
### Core Architecture
- Multiple servers (nodes)
- Shared storage (datafiles, control files)
- Oracle Clusterware (manages cluster)
- Private interconnect (fast network for node communication)

### Data Flow
1. Client connects to any node
2. Node processes the request
3. If required data is cached on another node:
    - It uses **Cache Fusion** (memory transfer)
4. Data blocks are synchronized across nodes
5. All nodes maintain **database consistency**

---

# Key Capabilities of Oracle RAC
## 1. Cache Synchronization (Cache Fusion)
- Ensures all nodes have consistent data
- Instead of disk I/O, data blocks are shared **in-memory**
- Uses high-speed interconnect

Benefit: Faster data access & reduced disk usage

---
## 2. Smart Cluster Reconfiguration

- Automatically detects node failures or additions
- Redistributes workload dynamically
- No manual intervention required

Benefit: Minimal downtime

---
## 3. Full Stack Protection
- Protects across layers:    
    - Hardware
    - OS
    - Database
    - Network
- Integrated with Oracle Clusterware for resilience
Benefit: End-to-end fault tolerance

---

# Features of Oracle RAC
- Shared database architecture
- Horizontal scalability
- Transparent application failover
- Load balancing (dynamic)
- Rolling patching (no downtime during updates)
- Online node addition/removal
- High-speed inter-node communication

---
# Benefits of Oracle RAC
## 1. High Availability
- Node failure doesn’t impact application significantly

## 2. Scalability
- Add nodes to handle more workload

## 3. Performance Improvement
- Parallel processing across nodes

## 4. Fault Tolerance
- No single point of failure

## 5. Cost Efficiency (in some cases)
- Uses commodity hardware instead of high-end single servers

---
# Disadvantages of Oracle RAC
## 1. Complexity
- Setup and maintenance are complex
- Requires skilled DBA

## 2. High Cost
- Licensing is expensive
- Requires specialized infrastructure

## 3. Network Dependency
- Performance relies heavily on interconnect network

## 4. Cache Fusion Overhead
- Cross-node communication can add latency
- Poor configuration = performance issues

## 5. Not Ideal for All Workloads
- Best suited for OLTP systems
- Not always efficient for heavy batch or write-heavy workloads

---
#  Conclusion
Oracle RAC is a **powerful clustering solution** designed for:
✅ Mission-critical systems  
✅ High availability requirements  
✅ Scalable database workloads

However:
⚠️ It is **complex and expensive**, so organizations must evaluate whether they truly need clustering at this level.

---
