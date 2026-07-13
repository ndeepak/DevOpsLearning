Awesome — you’re at the **perfect stage to learn Oracle properly**. I’ll walk you step-by-step like a real DBA training, from:

✅ Database creation → ✅ Architecture → ✅ Listener → ✅ Users → ✅ Remote access → ✅ Tools

---

# 🧠 1. Oracle Architecture (must understand first)

When you ran DBCA, Oracle created:

```
CDB (Container DB)
│
├── CDB$ROOT   → system container (admin level)
├── PDB$SEED   → template
└── NEWGENPDB  → your actual working database ✅
```

👉 Key idea:

|Component|Purpose|
|---|---|
|CDB|Holds everything|
|PDB|Where your applications & users go ✅|
|Listener|Handles remote connections|

---

# ⚙️ 2. Database Creation (what you already did)

You used:
```bash
dbca -silent -createDatabase \  
-templateName General_Purpose.dbc \  
-gdbname NEWGENDB \  
-sid NEWGENDB \  
-createAsContainerDatabase true \  
-numberOfPDBs 1 \  
-pdbName NEWGENPDB \  
-sysPassword Oracle123 \  
-systemPassword Oracle123
```


That created:

- DB name: `NEWGENDB`
- SID: `NEWGENDB`
- PDB: `NEWGENPDB`
- Port: `1521`

---

# ⚡ 3. Environment setup (VERY IMPORTANT)

Every Oracle DB uses environment variables:

Shell

export ORACLE_SID=NEWGENDB  
export ORACLE_HOME=/Oracle/app/oracle/product/19.3.0.0/dbhome_1  
export PATH=$ORACLE_HOME/bin:$PATH  



👉 Without this → errors like `ORA-12162`

---

# 🟢 4. Starting & stopping database

## ✅ Start DB

Shell

sqlplus / as sysdba  

startup;  



---

## ✅ Stop DB

SQL

shutdown immediate;  



---

## ✅ Check DB status

SQL

select status from v$instance;  


---

# 🧩 5. PDB management

## Check PDBs

SQL

show pdbs;  



---

## Open PDB

SQL

alter pluggable database all open;  



---

## Save auto-open

SQL

alter pluggable database all save state;  


---

## Switch to PDB

SQL

alter session set container=NEWGENPDB;  



---

# 👤 6. Users & Schemas

## Create user (inside PDB)

SQL

create user deepak identified by pass123;  

grant connect, resource to deepak;  


---

## Quota (important for tables)

SQL

alter user deepak quota unlimited on users;  


---

## Check users

SQL

select username from dba_users;  


---

# 📦 7. Tablespaces

## Create tablespace

SQL

create tablespace app_ts  

datafile '/Oracle/app/oracle/oradata/NEWGENDB/app_ts01.dbf'  

size 500m autoextend on;  


---

## Assign to user

SQL

alter user deepak default tablespace app_ts;  


---

# 🌐 8. Listener (Network layer)

Listener allows external connections.

---

## Check listener
lsnrctl status  

---

## Start/Stop
```
lsnrctl start  

lsnrctl stop  

```

---

## Register DB manually

SQL

```
alter system register;  
```


---

## Fix listener issue (important)

SQL

```
alter system set local_listener='(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.10.221)(PORT=1521))' scope=both;  
```

---

# 🔗 9. Connection types

## ✅ Local connection (no listener)

Shell

sqlplus / as sysdba  


---

## ✅ Remote (listener needed)

### Using Service Name (recommended)

Shell

sqlplus system/Oracle123@192.168.10.221:1521/NEWGENPDB  


---

## ✅ JDBC (DBeaver)

```
jdbc:oracle:thin:@//192.168.10.221:1521/NEWGENPDB
```

---

# 💻 10. DBeaver setup

|Field|Value|
|---|---|
|Host|192.168.10.221|
|Port|1521|
|Service|NEWGENPDB|
|User|deepak|

✅ Important:

- Choose **Service Name**
- Not SID

---

# 🔐 11. Privileges (your earlier topic)

## View privileges

SQL

select * from dba_sys_privs where grantee='DEEPAK';  


---

## Grant privileges

SQL

grant create table, create view to deepak;  


---

## With admin option

SQL

grant create table to deepak with admin option;  


---

# 📊 12. Basic operations

## Create table

SQL

create table emp (  

id number,  

name varchar2(100)  

);  


---

## Insert

SQL

insert into emp values (1, 'Deepak');  

commit;  


---

## Query

SQL

select * from emp;  


---

# 🚨 13. Common issues (you’ve already seen)

## ORA-12514

👉 Listener doesn’t know DB  
✔ Fix: `alter system register`

---

## ORA-12162

👉 ORACLE_SID not set  
✔ Fix: `export ORACLE_SID`

---

## Cannot create user without C##

👉 You're in CDB  
✔ Fix: switch to PDB

---

# 🔄 14. Full lifecycle (important)

### Start system

Shell

lsnrctl start  

sqlplus / as sysdba  

startup;  

---

### Open PDB

SQL

alter pluggable database all open;  

---

### Connect from app / DBeaver

✅ Use:

```
NEWGENPDB
```

---

# 🧠 15. Best practices

✔ Always create users in **PDB**  
✔ Always connect via **service name**  
✔ Never use SYS for applications  
✔ Use dedicated tablespaces  
✔ Save PDB state

---

# 🎯 Final mental model (VERY IMPORTANT)

```
Client (DBeaver)
      ↓
 Listener (1521)
      ↓
 Service Name (NEWGENPDB)
      ↓
 PDB (Database)
      ↓
 User (Deepak)
      ↓
 Tables
```

---

# 🚀 If you want next level training