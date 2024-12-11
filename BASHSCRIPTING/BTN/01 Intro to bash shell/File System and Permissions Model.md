## **File System Hierarchy**
In Linux, the file system is structured as a hierarchical tree, starting at the root directory `/`. Each directory serves a specific purpose:
```
/ 
├── /bin
├── /boot
├── /dev
├── /etc
├── /home
├── /lib
├── /media
├── /mnt
├── /opt
├── /sbin
├── /srv
├── /tmp
├── /usr
└── /proc
```

### **Important Directories and Their Functions**
1. **`/` (Root Directory):**
    - The top-level directory of the Linux file system. All files and directories are located under this.
2. **`/bin`:**
    
    - Contains essential binary executables (e.g., `ls`, `cp`, `mv`).
    - Available to all users for basic operations.
3. **`/boot`:**
    
    - Contains bootloader-related files (e.g., `vmlinuz`, `initrd`).
    - Critical for system startup.
4. **`/dev`:**
    
    - Contains device files representing hardware components (e.g., `/dev/sda` for hard drives).
5. **`/etc`:**
    
    - Configuration files for the system and applications.
    - Examples: `/etc/passwd`, `/etc/fstab`.
6. **`/home`:**
    
    - User-specific directories for storing personal files and settings.
    - Example: `/home/user1`, `/home/user2`.
7. **`/lib`:**
    
    - Essential libraries required by binaries in `/bin` and `/sbin`.
8. **`/media`:**
    
    - Temporary mount points for removable media like USB drives and CDs.
9. **`/mnt`:**
    
    - Generic mount point for manually mounted file systems.
10. **`/opt`:**
    
    - Optional software packages.
11. **`/sbin`:**
    
    - System binaries used for administrative tasks (e.g., `fsck`, `reboot`).
12. **`/srv`:**
    
    - Data served by the system, such as web or FTP servers.
13. **`/tmp`:**
    
    - Temporary files. Data here is cleared on reboot.
14. **`/usr`:**
    
    - User binaries, libraries, documentation, and source code.
    - Subdirectories:
        - `/usr/bin`: User applications.
        - `/usr/lib`: Libraries for user applications.
        - `/usr/share`: Shared resources (e.g., documentation).
15. **`/proc`:**
    
    - Virtual file system providing system information.
    - Example: `/proc/cpuinfo`, `/proc/meminfo`.

---

## **Permissions in Linux**

Permissions define how files and directories can be accessed or modified by users.

### **Permission Types**

Each file or directory has three levels of permissions for three categories of users:

- **User (u):** The owner of the file.
- **Group (g):** The group to which the file belongs.
- **Others (o):** All other users.

|**Permission**|**Symbol**|**Description**|
|---|---|---|
|Read|`r`|Allows viewing file content.|
|Write|`w`|Allows modifying file content.|
|Execute|`x`|Allows running files or accessing directories.|

---

### **File Permission Representation**

- **Symbolic Format:** `rwxr-xr--`
    
    - First character: `-` (file), `d` (directory), or `l` (link).
    - Next 9 characters: Permissions for **user**, **group**, and **others**.
        - Example: `rwxr-xr--`
            - User: `rwx` (read, write, execute).
            - Group: `r-x` (read, execute).
            - Others: `r--` (read only).
- **Numeric Format (Octal):**
    
    - Each permission is represented by a number:
        - `r=4`, `w=2`, `x=1`.
    - Combine values for each category:
        - `7` (rwx), `5` (r-x), `4` (r--).
        - Example: `chmod 754 file.txt` results in `rwxr-xr--`.

---

### **Permission Management Commands**

#### **1. `chmod` - Change File Permissions**

Used to modify permissions for a file or directory.
`chmod [options] [permissions] [file/directory]`

**Examples:**

1. Grant read, write, and execute to the user; read and execute to the group; and read to others:
    `chmod 754 file.txt`
    
2. Add execute permission for all:
    `chmod +x script.sh`
    
3. Remove write permission for others:
    `chmod o-w file.txt`
    
4. Use symbolic representation:
    `chmod u+rwx,g+rx,o+r file.txt`
    

---

#### **2. `chown` - Change Ownership**

Changes the owner of a file or directory.
`chown [options] [owner][:group] [file/directory]`

**Examples:**

1. Change the owner of a file to `user1`:
    `chown user1 file.txt`
    
2. Change both owner and group:
    `chown user1:group1 file.txt`
    
3. Change ownership recursively:
    `chown -R user1 /path/to/directory`
    

---

#### **3. `chgrp` - Change Group Ownership**
Changes the group ownership of a file or directory.
**Syntax:**
`chgrp [options] [group] [file/directory]`

**Examples:**

1. Change the group of a file to `group1`:
    `chgrp group1 file.txt`
    
2. Change group ownership recursively:
    `chgrp -R group1 /path/to/directory`
    

---
### **Practical Examples**
1. **Set file permissions:**
    `chmod 755 script.sh`
    
2. **Make a file readable and writable only by the owner:**
    `chmod 600 private.txt`
    
3. **Change ownership:**
    `chown alice project.doc`
    
4. **Change group ownership:**
    `chgrp developers code.py`
    
5. **Remove execute permission from all:**
    `chmod a-x file.sh`

---
### Summary Table of Commands

|**Command**|**Description**|
|---|---|
|`chmod`|Change file/directory permissions.|
|`chown`|Change the ownership of a file/directory.|
|`chgrp`|Change the group ownership of a file/directory.|
By understanding the Linux file system hierarchy and managing permissions effectively, users can maintain system organization, security, and efficient access control.