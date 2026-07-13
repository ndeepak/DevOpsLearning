# Oracle 19c Installation to Basic DBA Notes (End-to-End Guide)

---

# 1. Overview
This document summarizes the full journey from installing Oracle Database 19c on Oracle Linux to creating users inside a Pluggable Database (PDB), and performing basic SQL operations.

---

# 2. Oracle Architecture Basics
Oracle 19c uses **Multitenant Architecture**:

## Structure
CDB (Container Database)
├── CDB$ROOT → system/admin layer
├── PDB$SEED → template database
└── PDB (ORCLPDB) → actual working database

## Key Concept
- CDB$ROOT → system-level administration only
- PDB → where applications, users, tables exist

---

# 3. Pre-install Requirements (Oracle Linux)
## Host setup
```
hostnamectl set-hostname oracle-db
```

## Install prerequisites
`dnf install -y oracle-database-preinstall-19c`

This configures:
- Oracle user
- kernel parameters
- required packages

---

# 4. Oracle Software Installation
## Create directories
```
mkdir -p /u01/app/oracle/product/19.3.0/dbhome_1
chown -R oracle:oinstall /u01
```

## Extract software
`unzip LINUX.X64_193000_db_home.zip -d $ORACLE_HOME`

## Set environment variables
```
export ORACLE_BASE=/u01/app/oracle
export ORACLE_HOME=$ORACLE_BASE/product/19.3.0/dbhome_1
export ORACLE_SID=orcl
export PATH=$ORACLE_HOME/bin:$PATH
```

---

# 5. Database Creation (runInstaller / DBCA)
During installation:
- Choose "Create and Configure Database"
- Create Single Instance Database
- Database name: orcl
- PDB created: orclpdb

Result:
- CDB created
- PDB created
- Listener configured (may need fix)

---

# 6. Listener Configuration
## Check listener
`lsnrctl status`

## Start listener
`lsnrctl start`

## listener.ora example
```
LISTENER =

(DESCRIPTION_LIST =

(DESCRIPTION =

(ADDRESS = (PROTOCOL = TCP)(HOST = 0.0.0.0)(PORT = 1521))

)

)
```

## Open firewall
```
firewall-cmd --permanent --add-port=1521/tcp
firewall-cmd --reload
```

---

# 7. Verify Database Status

`sqlplus / as sysdba`

Check:

```
SELECT name, open_mode FROM v$database;
SHOW CON_NAME;
SHOW PDBS;
```

---

# 8. Switching to PDB

Always switch before creating users:

`ALTER SESSION SET CONTAINER = orclpdb;`
`SHOW CON_NAME;`

---

# 9. User Management (Important)

## Create user

`CREATE USER deep IDENTIFIED BY System321;`

## Grant privileges

`GRANT CONNECT, RESOURCE TO deep;`

## Storage quota

`ALTER USER deep QUOTA UNLIMITED ON USERS;`

---

# 10. ORA-65096 Fix (Important Concept)
Error occurs when creating user in ROOT:

ORA-65096: invalid common user or role name

Fix:
`ALTER SESSION SET CONTAINER = orclpdb;`

---

# 11. Basic SQL Operations

## Create table

```
CREATE TABLE employees (
	id NUMBER PRIMARY KEY,
	name VARCHAR2(50)
);
```

## Insert data

`INSERT INTO employees VALUES (1, 'Ram');`

## Select data

`SELECT * FROM employees;`

## Describe table

`DESC employees;`

---

# 12. Schema Concept

A USER = SCHEMA

Example:

deep (schema)
├── employees table
├── orders table
└── indexes

---

# 13. SYS vs SYSTEM vs App Users

|User|Purpose|
|---|---|
|SYS|Super admin (don’t use for apps)|
|SYSTEM|Admin tasks|
|deep|Application user|

---

# 14. DBeaver Connection Settings

## For app user (recommended)
- Host: 192.168.10.221
- Port: 1521
- Service: orclpdb
- User: deep
- Password: System321

## For SYS (admin only)
- User: SYS
- Role: SYSDBA

---

# 15. Network Troubleshooting
## ORA-12541
- Listener not running

## Fix
`lsnrctl start`

## Check port
`netstat -tulnp | grep 1521`

---

# 16. Key Learning Summary

✔ Oracle 19c = Multitenant (CDB + PDB) ✔ Always use PDB for development ✔ Users must be created in PDB ✔ Listener enables external connections ✔ DBeaver connects using service name

---

# 17. Recommended Next Topics

- Joins (INNER, LEFT, RIGHT)
- Indexing
- Constraints (FK, UNIQUE)
- Backup (RMAN basics)
- Performance tuning basics
- PDB creation and cloning

I’ve created a complete structured notes document for you covering everything from:

- Oracle installation
- Listener setup
- CDB vs PDB architecture
- User creation
- ORA-65096 fix
- DBeaver connection
- Basic SQL operations

You can now use it as your **Oracle beginner-to-admin cheat sheet**.