A **PDB (Pluggable Database)** is a feature introduced in Oracle's **Multitenant Architecture**.

Think of it like this:

### Traditional Oracle (Pre-12c)

One Oracle instance = One database

```
Server └── Oracle Instance      └── Database
```

If you wanted another database, you had to create another complete database instance.

---

### Oracle Multitenant (12c, 19c, 21c, 23ai)

One Oracle instance can host multiple databases.

```
Container Database (CDB)│├── PDB$SEED├── ORCLPDB├── NEWGENPDB└── TESTPDB
```

Here:

- **CDB** = Container Database
- **PDB** = Pluggable Database

Each PDB behaves almost like an independent database.

---

## Components

### CDB (Container Database)

The top-level database.

Contains:

- Oracle background processes
- Memory structures (SGA/PGA)
- Data dictionary metadata
- One or more PDBs

### PDB$SEED

A read-only template Oracle creates automatically.

Whenever you create a new PDB, Oracle copies from PDB$SEED.

### User PDBs

Examples:

- ORCLPDB
- NEWGENPDB
- FINACLEPDB

Each can have:

- Its own schemas
- Tables
- Users
- Roles
- Application data

---

## Why Oracle Created PDBs

Imagine a bank server hosting:

- Newgen
- Finacle
- HR System
- Reporting Database

Without PDBs:

```
4 Oracle databases4 SGA allocations4 listener registrations4 sets of background processes
```

With PDBs:

```
1 Oracle instance ├── FINACLEPDB ├── NEWGENPDB ├── HRPDB └── REPORTPDB
```

Much less resource consumption.

---

## Why You Got ORA-65096

You connected as:

```
SYS AS SYSDBA
```

to:

```
CDB$ROOT
```

and tried:

```
CREATE USER TEST123 IDENTIFIED BY "Test@123";
```

Oracle thought:

> "You're in the root container, so this must be a common user."

Common users require:

```
CREATE USER C##TEST123 IDENTIFIED BY "Test@123";
```

To create a normal application schema, you should switch to a PDB:

```
ALTER SESSION SET CONTAINER=ORCLPDB;
```

then:

```
CREATE USER TEST123 IDENTIFIED BY "Test@123";
```

---

## How to Check Your PDBs

As SYS:

```
SHOW PDBS;
```

Example output:

```scss
CON_ID  CON_NAME    OPEN MODE
------  ----------  ----------
2       PDB$SEED    READ ONLY
3       ORCLPDB     READ WRITE
```

or:

```
SELECT NAME, OPEN_MODE FROM V$PDBS;
```

---

## How Applications Connect

Instead of connecting to the CDB:

```
Service Name = ORCL
```

applications usually connect directly to a PDB:

```
Service Name = ORCLPDB
```

or

```
Service Name = NEWGENPDB
```

For Newgen, Finacle, Oracle EBS, and most enterprise applications, the application schemas are typically created **inside a PDB**, not in `CDB$ROOT`.

Run:

```
SHOW PDBS;
```

