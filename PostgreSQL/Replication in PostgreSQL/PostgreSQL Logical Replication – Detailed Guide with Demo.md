# PostgreSQL Logical Replication – Detailed Guide with Demo

## 1. What is Logical Replication?
Logical replication in PostgreSQL allows you to **replicate selected database objects (primarily tables)** by transferring **logical changes (INSERT, UPDATE, DELETE)** rather than raw binary data.
### Key characteristics:
- Replicates **specific tables**, not entire database cluster
- Works using **publications and subscriptions**
- Sends **row-level changes**
- Can replicate across different PostgreSQL versions
## 2. Architecture Overview
Logical replication consists of two main components:
### Publisher (Source)
- The database where data originates
- Defines a **publication**

### Subscriber (Target)
- The database that receives data
- Creates a **subscription** to a publication
## 3. Preconditions
Before setting up logical replication:
### On both Publisher and Subscriber:

`Ensure PostgreSQL version ≥ 10`
### On Publisher (postgresql.conf):
```
wal_level = logical  
max_replication_slots = 10  
max_wal_senders = 10  
```
Restart PostgreSQL after changes.
### Configure pg_hba.conf (on Publisher)
Allow subscriber to connect:
```
host replication all <subscriber_ip>/32 md5  
host all all <subscriber_ip>/32 md5  
```
Reload or restart PostgreSQL.
## 4. Demo Setup
Assume:
- Publisher: localhost (port 5432)
- Subscriber: localhost (port 5433)
- Database: testdb
## Step 1: Create Database and Table (Publisher)
```sql
CREATE DATABASE testdb;
\c testdb
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    city TEXT
);
INSERT INTO customers (name, city)
VALUES
('John', 'New York'),
('Alice', 'London');
```
## Step 2: Create Publication (Publisher)
```
CREATE PUBLICATION my_publication  
FOR TABLE customers;  
```
This means:
- Only the `customers` table is replicated
- Future changes will also be replicated
## Step 3: Prepare Subscriber Database
On subscriber server:
```sql
CREATE DATABASE testdb;
\c testdb
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    city TEXT
);
```
Important:
- Table structure must match publisher exactly
## Step 4: Create Subscription (Subscriber)
```sql
CREATE SUBSCRIPTION my_subscription

CONNECTION 'host=localhost port=5432 dbname=testdb user=postgres password=your_password'

PUBLICATION my_publication;
```
## What Happens Now?
- PostgreSQL copies initial data from publisher
- Then starts streaming changes
## Step 5: Test Replication

### Insert Data on Publisher:
```
INSERT INTO customers (name, city)  
VALUES ('Bob', 'Paris');  
```
### Check Subscriber:
```
SELECT * FROM customers;  
```

You should see:
```
1 | John  | New York
2 | Alice | London
3 | Bob   | Paris
```
## Step 6: Update and Delete Test
### Update on Publisher:
```
UPDATE customers  
SET city = 'Berlin'  
WHERE name = 'Alice';  
```
### Delete on Publisher:
```
DELETE FROM customers  
WHERE name = 'John';  
```
### Verify on Subscriber:
```
SELECT * FROM customers;  
```
Changes will reflect automatically.
## 5. Important Concepts
### 1. Replica Identity
For UPDATE/DELETE to work, PostgreSQL needs a way to identify rows.
Default:
- PRIMARY KEY\
If no primary key:
`ALTER TABLE customers REPLICA IDENTITY FULL;`
### 2. Initial Data Synchronization
When subscription is created:
- PostgreSQL copies existing data
- This is called **initial snapshot**
### 3. Replication Slots
Each subscription creates a **replication slot** on publisher:
- Prevents WAL deletion until subscriber consumes it
Check slots:
`SELECT * FROM pg_replication_slots;`
### 4. Monitoring Replication
#### On Publisher:
`SELECT * FROM pg_stat_replication;`
#### On Subscriber:
`SELECT * FROM pg_stat_subscription;`
## 6. Adding More Tables to Replication
### On Publisher:
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    item TEXT
);
ALTER PUBLICATION my_publication
ADD TABLE orders
```
### On Subscriber:
```
CREATE TABLE orders (  
id SERIAL PRIMARY KEY,  
item TEXT  
);  
```
Subscription will automatically pick this up (may require refresh):
`ALTER SUBSCRIPTION my_subscription REFRESH PUBLICATION;`
## 7. Stopping and Removing Replication
### Disable Subscription:
`ALTER SUBSCRIPTION my_subscription DISABLE;`
### Drop Subscription:
`DROP SUBSCRIPTION my_subscription;`
### Drop Publication:
`DROP PUBLICATION my_publication;`
## 8. Limitations of Logical Replication
- No automatic conflict handling
- DDL changes (ALTER TABLE) are not replicated automatically
- Requires primary key or replica identity
- Sequence values are not synchronized automatically
## 9. Common Use Cases
- Microservices architecture (share selective tables)
- Data migration between servers
- Reporting systems
- Multi-region replication
## 10. Summary
Logical replication in PostgreSQL:
- Uses **publication and subscription model**
- Replicates **row-level changes**
- Works at **table-level granularity**
- Is flexible but requires careful setup
## Key Takeaway
Logical replication gives PostgreSQL the ability to behave like **fine-grained data distribution system**, similar to SQL Server transactional replication, but with simpler architecture and manual conflict handling.