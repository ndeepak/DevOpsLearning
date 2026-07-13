# 🚨 Problem Summary

1. ✅ Listener is running    
2. ❌ Listener shows:    
    ```
    The listener supports no services
    ```    
    → Database is **NOT registered**    
3. ❌ `sqlplus / as sysdba` fails with:    
    ```
    ORA-12162
    ```    
    → Your **ORACLE_SID is not set**    


# ✅ Fix Step-by-Step

# ✅ 1. Set ORACLE_SID (this is critical)

Your DB name is `NEWGENDB`, so run:
export ORACLE_SID=NEWGENDB  

Verify:
echo $ORACLE_SID  

👉 Should print:
```
NEWGENDB
```


# ✅ 2. Connect locally (no listener needed)
Now try:
sqlplus / as sysdba  

✅ This should work now

# ✅ 3. Start the database (if not started)
Inside SQL*Plus:
startup;  

# ✅ 4. Register DB with listener
Still inside SQL:
alter system register;  

# ✅ 5. Check listener again
lsnrctl status  
✅ Now you should see something like:

```
Service "NEWGENDB" has 1 instance(s)
Service "NEWGENPDB" has 1 instance(s)
```

# ✅ 6. Open the PDB
Inside SQL:
show pdbs;  


If not open:
alter pluggable database all open;  


Make it permanent:
alter pluggable database all save state;  

# ✅ 7. Fix listener registration permanently (important)

Set correct listener address:

alter system set local_listener='(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.10.221)(PORT=1521))' scope=both;  

Then:
alter system register;  

# ✅ 8. Clean up your tnsnames.ora (optional but better)
Your current config still has old `ORCL`. Replace/add:

```
NEWGENDB =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.10.221)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = NEWGENDB)
    )
  )

NEWGENPDB =
  (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.10.221)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = NEWGENPDB)
    )
  )
```

# ✅ 9. Test connections
## 👉 SQL*Plus
sqlplus system/Oracle123@NEWGENPDB  

or:

sqlplus system/Oracle123@192.168.10.221:1521/NEWGENPDB  

## 👉 DBeaver settings
- Host: `192.168.10.221`
- Port: `1521`
- Service name: `NEWGENPDB`
- User: `system`
- Password: `Oracle123`
# ✅ 🔍 Why this happened
You hit **two classic Oracle issues**:
### ❌ ORA-12162
→ caused by missing:
```
ORACLE_SID
```
### ❌ Listener has no services
→ database wasn’t:
- started OR
- registered
# ✅ ✅ Final expected state
After fix:
lsnrctl status  

Should show:

```
Service "NEWGENDB"
Service "NEWGENPDB"
```


# ✅ If STILL not working
Run this and send me output:
echo $ORACLE_SID  

ps -ef | grep pmon  

lsnrctl status  

I'll diagnose it instantly 👍

# ✅ Why this happens
You created your DB as:
```
-createAsContainerDatabase true
```

So:
- `NEWGENDB` = **CDB (root container)**
- `NEWGENPDB` = **Pluggable DB**


## 🔒 Oracle rule
Inside the **CDB root**, Oracle only allows **common users**, and they **must start with `C##`**

So:
create user test identified by test;  
❌ Fails

create user c##test identified by test;  

✅ Works

# ✅ Correct way (what you should do)
👉 You should **NOT create normal schemas in CDB**

Instead:
✅ Switch to the **PDB (NEWGENPDB)**  
✅ Then create your schema normally

# ✅ Step-by-step fix

## 1. Check where you are
show con_name;  

If it shows:
```
CDB$ROOT
```

👉 That’s why you're getting the error.

## 2. Switch to PDB
alter session set container=NEWGENPDB;  

## 3. Now create schema normally
create user deepak identified by pass123;  

grant connect, resource to deepak;  

✅ No `C##` required here

## 4. Verify
show con_name;  

Output should be:
```
NEWGENPDB
```

# ✅ Alternative (direct login to PDB)
Instead of switching manually, connect directly:
sqlplus system/Oracle123@NEWGENPDB  
Then create user:
create user deepak identified by pass123;  

grant connect, resource to deepak;  

# ✅ When do you use C## users?
Only if you want a **common user across ALL PDBs**

Example:

create user c##admin identified by pass123 container=all;  
✅ Quick Summary

|Location|Allowed user types|
|---|---|
|CDB (root)|Only `C##` (common users)|
|PDB|Normal users ✅|

# ✅ Best practice
✔ Always:
- Connect to **PDB**
- Create users there

❌ Avoid:
- Creating application users in CDB

# ✅ Your situation (final fix)
Just run:
alter session set container=NEWGENPDB;  

  

create user deepak identified by pass123;  

grant connect, resource to deepak;  
