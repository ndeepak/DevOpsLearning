# Lab-Linux Challenge 1

The database server called `centos-host` is running short on space! You have been asked to add an LVM volume for the Database team using some of the existing disks on this server.
Inspect the requirements in detail by clicking on the icons of the interactive architecture diagram on the right and complete the tasks. Once done click on the `Check` button to validate your work.
![](LINUX/Linux%20Challenges%20Kodekloud/Attachments/Pasted%20image%2020260409140931.png)
The database server called `centos-host` is running short on space! You have been asked to add an LVM volume for the Database team using some of the existing disks on this server.  
Inspect the requirements in detail by clicking on the icons of the interactive architecture diagram on the right and complete the tasks. Once done click on the `Check` button to validate your work.

Tasks:
1. Create a Physical Volume for "/dev/vdd"
```bash
sudo yum install -y lvm2
lsblk 
lsblk /dev/vdd

pvcreate /dev/vdd
pvs
pvdisplay /dev/vdd
```


2. Create a Physical Volume for "/dev/vde"

```bash
lsblk
lsblk /dev/vde

NAME MAJ:MIN RM SIZE RO TYPE MOUNTPOINTS
vde  252:64   0   1G  0 disk 

pvcreate /dev/vde
pvs
pvdisplay /dev/vde
```

3. Create a volume group called "dba_storage" using the physical volumes "/dev/vdd" and "/dev/vde"
```bash
pvcreate /

vgcreate dba_storage /dev/vdd /dev/vde

Volume group "dba_storage" successfully created

vgs
VG          #PV #LV #SN Attr   VSize VFree
dba_storage   2   0   0 wz--n- 1.99g 1.99g
vgdisplay dba_storage
```

4. Create an "lvm" called "volume_1" from the volume group called "dba_storage". Make use of the entire space available in the volume group.
```bash
# creating logical volume
lvcreate -n volume_1 -l 100%FREE dba_storage
  Logical volume "volume_1" created.vs

# - `-n volume_1` → names the logical volume
# - `-l 100%FREE` → uses **all free extents** in the volume group
# - `dba_storage` → the volume group name

lvs
lvdisplay /dev/dba_storage/volume_1

lsblk
```

```
root@centos-host ~ ➜  lvdisplay
  --- Logical volume ---
  LV Path                /dev/dba_storage/volume_1
  LV Name                volume_1
  VG Name                dba_storage
  LV UUID                KUsoLC-tTs3-W8YR-gHjC-u9bv-AX31-AMp21w
  LV Write Access        read/write
  LV Creation host, time centos-host, 2026-04-09 02:44:56 -0400
  LV Status              available
  # open                 0
  LV Size                1.99 GiB
  Current LE             510
  Segments               2
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0
   

root@centos-host ~ ➜  lsblk
NAME                   MAJ:MIN RM SIZE RO TYPE MOUNTPOINTS
vda                    252:0    0  10G  0 disk 
└─vda1                 252:1    0  10G  0 part /
vdb                    252:16   0   1M  0 disk /mnt/app-config
vdc                    252:32   0   1M  0 disk 
vdd                    252:48   0   1G  0 disk 
└─dba_storage-volume_1 253:0    0   2G  0 lvm  
vde                    252:64   0   1G  0 disk 
└─dba_storage-volume_1 253:0    0   2G  0 lvm  
vdf                    252:80   0   1G  0 disk 
vdg                    252:96   0   1G  0 disk 

```

5. Format the lvm volume "volume_1" as an "XFS" filesystem

Logical Path:
````
/dev/dba_storage/volume_1
````

```bash
mkfs.xfs /dev/dba_storage/volume_1
meta-data=/dev/dba_storage/volume_1 isize=512    agcount=4, agsize=130560 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=1, sparse=1, rmapbt=0
         =                       reflink=1    bigtime=1 inobtcount=1 nrext64=0
data     =                       bsize=4096   blocks=522240, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0, ftype=1
log      =internal log           bsize=4096   blocks=16384, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
Discarding blocks...Done.
```
Mount the filesystem at the path "/mnt/dba_storage".
```bash
mkdir -p /mnt/dba_storage

# Mount the XFS Filesystem
mount /dev/dba_storage/volume_1 /mnt/dba_storage

# Verify
df -h | grep dba_storage

/dev/mapper/dba_storage-volume_1  2.0G   47M  1.9G   3% /mnt/dba_storage

# verify filesystem
mount | grep dba_storage

/dev/mapper/dba_storage-volume_1 on /mnt/dba_storage type xfs (rw,relatime,seclabel,attr2,inode64,logbufs=8,logbsize=32k,noquota)
```

Make sure that this mount point is persistent across reboots with the correct default options.

```bash
# Get the UUID
blkid /dev/mapper/dba_storage-volume_1
/dev/mapper/dba_storage-volume_1: UUID="8324ef88-37f8-43ce-9d18-107b6ef79657" TYPE="xfs"

vi /etc/fstab
UUID=8324ef88-37f8-43ce-9d18-107b6ef79657  /mnt/dba_storage  xfs  defaults  0  0

# - `defaults` → correct default mount options
# - `0 0` → standard values for XFS

# OR
#/dev/mapper/dba_storage-volume_1 /mnt/dba_storage xfs defaults 0 0
```

Before Rebooting:
```bash
umount /mnt/dba_storage

mount -a
df -h
lsblk
```

6. Create a group called "dba_users" and add the user called 'bob' to this group
```bash
getent group dba_users
groupadd dba_users

```

8. Ensure that the mountpoint "/mnt/dba_storage" has the group ownership set to the "dba_users" group
```bash
chown :dba_users /mnt/dba_storage
ls -ld /mnt
```
Ensure that the mount point "/mnt/dba_storage" has "read/write" and execute permissions for the owner and group and no permissions for anyone else.
```bash
chmod 770 /mnt/dba_storage
ls -ld /mnt/d

# extra
chmod 2770 /mnt/dba_storage
```