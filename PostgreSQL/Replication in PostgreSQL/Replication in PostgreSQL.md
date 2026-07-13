# Replication in PostgreSQL


Replication in PostgreSQL is the process of **copying and maintaining database objects and data across multiple PostgreSQL servers** to ensure consistency, high availability, and scalability.

Unlike SQL Server, PostgreSQL replication is more **system-level (database/cluster level)** rather than fine-grained object-level replication.

## Is PostgreSQL Replication DB Level or Object Level?
👉 PostgreSQL replication is primarily **database-level (or cluster-level)**.
- You generally replicate:
    - Entire database cluster (all databases)
    - Specific database (logical replication)
- It does **NOT natively support article-level replication** (like individual tables grouped into publications—though logical replication gets close)

⚠️ Important:
- **Physical replication → full database cluster**
- **Logical replication → selective tables**

## Key Components (Equivalent Mapping)

|SQL Server|PostgreSQL|
|---|---|
|Publisher|Primary Server|
|Subscriber|Standby / Replica|
|Distributor|Not separate (built-in WAL system)|
|Article|Table (in logical replication)|
|Publication|Publication (same concept in logical replication)|
|Subscription|Subscription|


## Types of Replication in PostgreSQL
PostgreSQL mainly supports **two core types** of replication:
## 1. Physical Replication (Streaming Replication)
### Overview
- Replicates **entire database cluster at binary level**
- Uses **WAL (Write-Ahead Log)**
### How it works:
1. Primary server writes changes to WAL
2. Standby server continuously reads WAL
3. Applies changes in real time
### Features
- Exact copy of primary
- High availability
- Read-only standby supported
- Low latency
### Limitations
- Cannot replicate specific tables
- Standby is read-only (no writes)
### Use Cases
- Disaster recovery
- Failover systems
- Read scaling
## 2. Logical Replication
### Overview
- Replicates **selected database objects (tables)**
- Works at **logical level (rows/changes)** rather than physical bytes
### Key Concepts
- **Publication**    
    - Defines which tables to replicate
- **Subscription**    
    - Target server subscribes to publication
Example:
```sql
CREATE PUBLICATION my_pub FOR TABLE customers, orders;  
```

```sql
CREATE SUBSCRIPTION my_sub  
CONNECTION 'host=server1 dbname=mydb user=replicator password=pass'  
PUBLICATION my_pub;  
```

### Features
- Replicate **specific tables**
- Allows **cross-version replication**
- Supports **bi-directional setups (with care)**
### Limitations
- Requires primary key on tables
- No automatic conflict resolution
- Slightly more complex setup
### Use Cases
- Microservices architecture
- Data migration
- Selective data sharing

## PostgreSQL Replication Concepts
### WAL (Write-Ahead Logging)
- Core mechanism for replication
- Stores every change before applying it
- Used by both backup and replication
### Synchronous vs Asynchronous Replication
#### Asynchronous (default)
- Primary does NOT wait for replica
- Faster
- Possible data loss on crash
Using asynchronous multimaster replication, each server works independently, and periodically communicates with the other servers to identify conflicting transactions.
####  Synchronous
- Primary waits for replica confirmation
- Strong consistency
- Slight performance overhead
Synchronous multimaster replication is best for mostly read workloads, though its big advantage is that any server can accept write requests — there is no need to partition workloads between primary and standby servers, and because the data changes are sent from one server to another, there is no problem with non-deterministic functions like `random()`.
### Replication Slots
- Ensure WAL files are retained until replicas consume them
- Prevent data loss when replica is slow



## Push vs Pull in PostgreSQL?
PostgreSQL doesn’t explicitly use push/pull terminology like SQL Server. Instead:
- **Streaming replication → push-like**
- **Logical replication → subscriber initiates (pull-like)**

---

## Comparison: SQL Server vs PostgreSQL Replication

|Feature|SQL Server|PostgreSQL|
|---|---|---|
|Granularity|Object-level|DB / Table-level|
|Distributor|Separate component|Not required|
|Types|Transactional, Snapshot, Merge, Peer|Physical, Logical|
|Conflict Handling|Built-in (Merge)|Manual|
|Real-time support|Yes|Yes (Streaming)|
|Bi-directional|Supported|Limited (custom setup)|

## Pros & Cons of PostgreSQL Replication
### Advantages
- Built-in (no separate distributor)
- Strong support for **high availability**
- **Streaming replication is fast and efficient**
- Logical replication gives flexibility
- Open-source and customizable
### Disadvantages
- No native **automatic conflict resolution**
- Physical replication lacks granularity
- Logical replication setup can be complex
- Limited compared to SQL Server Merge replication
##  When to Use What?

|Scenario|Recommended Replication|
|---|---|
|Disaster recovery|Physical replication|
|Read scaling|Streaming replication|
|Selective tables|Logical replication|
|Data migration|Logical replication|
|Multi-region scaling|Logical + custom setup|

## Conclusion
PostgreSQL replication is **simpler in architecture but powerful in capability**. It focuses heavily on **reliability and performance**, especially through WAL-based physical replication.

- Use **Physical replication** for full-copy/high availability systems
- Use **Logical replication** when you need flexibility and control
