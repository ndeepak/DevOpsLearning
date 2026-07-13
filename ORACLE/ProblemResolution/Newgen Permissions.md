# ✅ 1. Check privileges for a user

Assume your user is `DEEPAK` (replace if needed).

## 🔹 Check system privileges

SQL

select privilege, admin_option  

from dba_sys_privs  

where grantee = 'DEEPAK';  

Show more lines

✅ This shows:

- what privileges the user has
- whether they have **ADMIN OPTION (YES/NO)**

---

# ✅ 2. Check each required privilege from your list

### Required privileges checklist:

|Privilege|Must exist?|Admin option?|
|---|---|---|
|CREATE TABLESPACE|✅|NO|
|CREATE USER|✅|NO|
|CREATE PROCEDURE|✅|✅|
|CREATE SEQUENCE|✅|✅|
|CREATE SESSION|✅|✅|
|CREATE TABLE|✅|✅|
|CREATE TRIGGER|✅|✅|
|CREATE VIEW|✅|✅|
|CREATE JOB|✅|✅|
|CREATE TYPE|✅|✅|

---

## ✅ Query to verify all at once

SQL

select privilege,  

case when admin_option = 'YES' then 'ADMIN' else 'NO ADMIN' end as admin_option  

from dba_sys_privs  

where grantee = 'DEEPAK'  

order by privilege;  



---

# ✅ 3. Check missing privileges

To quickly identify missing ones:

SQL

select p.privilege  

from (  

select 'CREATE TABLESPACE' privilege from dual union all  

select 'CREATE USER' from dual union all  

select 'CREATE PROCEDURE' from dual union all  

select 'CREATE SEQUENCE' from dual union all  

select 'CREATE SESSION' from dual union all  

select 'CREATE TABLE' from dual union all  

select 'CREATE TRIGGER' from dual union all  

select 'CREATE VIEW' from dual union all  

select 'CREATE JOB' from dual union all  

select 'CREATE TYPE' from dual  

) p  

where p.privilege not in (  

select privilege from dba_sys_privs where grantee = 'DEEPAK'  

);  



---

# ✅ 4. Grant missing privileges

Run as SYS or SYSTEM:

SQL

grant create tablespace, create user to DEEPAK;  

  

grant create procedure,  

create sequence,  

create session,  

create table,  

create trigger,  

create view,  

create job,  

create type  

to DEEPAK with admin option;  



---

# ✅ 5. CTXSYS (CTX_DDL) permission

This is special 👇

## 🔹 Check access

SQL

select *  

from dba_tab_privs  

where grantee = 'DEEPAK'  

and owner = 'CTXSYS';  



---

## ✅ Grant CTX_DDL privilege

SQL

grant execute on CTXSYS.CTX_DDL to DEEPAK with grant option;  



✅ This satisfies:

> “CTXSYS package object rights for CTX_DDL (With Grantable Yes)”

---

# ✅ 6. Optional: verify roles too

Sometimes privileges come via roles:

SQL

select * from dba_role_privs where grantee = 'DEEPAK';  



---

# ✅ 7. Important Note (very important for your use case)

- `CREATE TABLESPACE` and `CREATE USER` are **powerful privileges**
- Giving them usually means this is a **DB admin-type user**

✔ This matches your requirement (“client creates DB objects via product script”)

---

# ✅ ✅ Final validation checklist

After everything:

SQL

select privilege, admin_option  

from dba_sys_privs  

where grantee = 'DEEPAK';  



Confirm:

✔ All privileges exist  
✔ Required ones show `ADMIN_OPTION = YES`

---

# ✅ Quick Summary

- Use `DBA_SYS_PRIVS` → system privileges
- Use `DBA_TAB_PRIVS` → CTXSYS access
- Grant missing ones with `WITH ADMIN OPTION`
- Always do this inside **NEWGENPDB**