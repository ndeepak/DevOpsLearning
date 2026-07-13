# Oracle RAC Lab Setup
A **practical, real RAC 19c two-node setup** using your servers:
- Node1: `orarac1`
- Node2: `orarac2`
- OS: Oracle Linux 8.5
- Goal: Install **2-node Oracle RAC 19c**

This will be a **step-by-step implementation guide** (no theory, only what you need).

---

# 1. Architecture Overview
You need:
## Nodes
- orarac1
- orarac2

## Networks
- Public network (client access)
- Private interconnect (node communication)
- Optional: Virtual IPs (VIP) + SCAN

## Storage
- Shared storage (ASM disks)

---

# 2. Prerequisites
## Minimum Requirements
### Hardware (per node)
- RAM: 8 GB minimum (16 GB recommended)
- CPU: 2+
- Disk:
    - OS disk
    - Shared disks (for ASM)

---

# 3. Network Configuration
## Define Hostnames
Edit `/etc/hosts` on both nodes:
Our:
```scss
# Public
192.168.10.230  orarac1.cas.com.np   orarac1
192.168.10.231  orarac2.cas.com.np   orarac2

# Private
192.168.35.230  orarac1-priv.cas.com.np  orarac1-priv
192.168.35.231  orarac2-priv.cas.com.np  orarac2-priv

# VIP
192.168.10.227  orarac1-vip.cas.com.np  orarac1-vip
192.168.10.228  orarac2-vip.cas.com.np  orarac2-vip

# SCAN
192.168.10.224  rac-cluster-scan.cas.com.np rac-cluster-scan
192.168.10.225  rac-cluster-scan.cas.com.np rac-cluster-scan
192.168.10.226  rac-cluster-scan.cas.com.np rac-cluster-scan
```


```
# Public IPs
192.168.1.101   orarac1
192.168.1.102   orarac2

# Private Interconnect
192.168.2.101   orarac1-priv
192.168.2.102   orarac2-priv

# Virtual IPs
192.168.1.111   orarac1-vip
192.168.1.112   orarac2-vip

# SCAN IPs (3 recommended)
192.168.1.121   rac-scan
192.168.1.122   rac-scan
192.168.1.123   rac-scan
```

---

## Verify Connectivity
Run from both nodes:

```
ping orarac2
ping orarac2-priv
ping rac-scan
```

---

# 4. Install Required Packages
On both nodes:
```
dnf install oracle-database-preinstall-19c -y
```

This automatically:

- Creates user `oracle`
- Sets kernel parameters
- Configures limits

---

# 5. Create Required Users and Groups

Verify:

```
id oracle
```

Groups should include:

- oinstall
- dba
- oper
- asmadmin
- asmdba
- asmoper

---

# 6. Configure SSH Passwordless Login
From `orarac1`:
```
su - oracle

ssh-keygen
ssh-copy-id oracle@orarac1
ssh-copy-id oracle@orarac2
```

Test:
```
ssh orarac2 hostname
```

Must not ask password.

---

# 7. Shared Storage Setup (ASM Disks)
You need shared disks (via iSCSI / SAN / VirtualBox shared disks).
## Example disks:
- /dev/sdb
- /dev/sdc
- /dev/sdd

---

## Configure ASMLib
### Install:
```
dnf install oracleasm-support oracleasmlib kmod-oracleasm -y
```

### Configure:
```
oracleasm configure -i
```

Provide:
- oracle user: oracle
- group: oinstall

---

### Create ASM disks:
```
oracleasm createdisk DATA1 /dev/sdb
oracleasm createdisk DATA2 /dev/sdc
oracleasm createdisk FRA1  /dev/sdd
```

Check:
```
oracleasm listdisks
```

---

# 8. Directory Structure

Create on both nodes:

```
mkdir -p /u01/app/19.0.0/grid
mkdir -p /u01/app/oracle/product/19.0.0/dbhome_1

chown -R oracle:oinstall /u01
chmod -R 775 /u01
```

---

# 9. Configure Environment Variables

Add to `.bash_profile` for oracle user:

```
export ORACLE_BASE=/u01/app/oracle
export GRID_HOME=/u01/app/19.0.0/grid
export DB_HOME=/u01/app/oracle/product/19.0.0/dbhome_1

export ORACLE_SID=orarac1   # change per node
export PATH=$PATH:$GRID_HOME/bin:$DB_HOME/bin
```

On node2:

```
export ORACLE_SID=orarac2
```

---

# 10. Install Grid Infrastructure (Clusterware + ASM)

On `orarac1`:

```
cd /stage/grid
./runInstaller
```

---

## Choose:
- Configure Oracle Grid Infrastructure for a Cluster
- Cluster Name: `rac-cluster`
- SCAN Name: `rac-scan`

---

## Add Nodes
Add:
```
orarac1
orarac2
```

---

## Network Selection

- Public interface: eth0 (example)
- Private: eth1

---

## ASM Configuration

- Disk Group: DATA
- Redundancy: External or Normal
- Select ASM disks created earlier

---

## Set Passwords

- ASM password
- Grid user password

---

## Run Root Scripts

After install:

```
/u01/app/19.0.0/grid/root.sh
```

Run on both nodes when prompted.

---

# 11. Install Oracle RAC Database Software

On node1:

```
cd /stage/database
./runInstaller
```

Choose:

- Install database software only
- RAC installation

Select:

- Both nodes

---

After install:

Run root scripts on both nodes.

---

# 12. Create RAC Database

Use DBCA:

```
dbca
```

---

## Choose:

- Create Database
- Advanced configuration
- RAC database

---

## Provide:

- DB Name: racdb
- Instances:
    - racdb1 (node1)
    - racdb2 (node2)

---

## Storage:

- ASM disk group: DATA

---

## Configure:

- Memory
- Character set
- EM Express optional

---

# 13. Verify Cluster

Check cluster status:

```
crsctl stat res -t
```

---

Check instances:

```
srvctl status database -d racdb
```

---

# 14. Test Failover

Stop one node:

```
shutdown -h now
```

Check database still accessible from other node.

---

# 15. Common Issues to Watch

- SSH not working
- DNS / SCAN misconfigured
- ASM disks not visible
- Incorrect kernel params
- Network latency (critical for RAC)

---

# Conclusion of Setup Phase

At this point you have:

- Fully working 2-node RAC
- Shared ASM storage
- Load-balanced database instances
- High availability cluster

---

# Next Step

If you want, next we can go deeper into:

1. Silent installation (automated RAC setup)
2. VirtualBox / VMware RAC lab setup
3. SCAN listener internals
4. RAC troubleshooting and logs
5. Performance tuning (very important for RAC)

Just tell me what you want next.