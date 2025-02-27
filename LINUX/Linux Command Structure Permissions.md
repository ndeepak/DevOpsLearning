## **1️⃣ Understanding File Permissions in Linux**
Start with:
`ls -l`

Example output:
`-rw-r--r--  1 user group 1234 Feb 17 10:30 file.txt`

Explain each part:
- `-rw-r--r--` → **File permissions**
- `1` → **Hard link count**
- `user` → **File owner**
- `group` → **Group owner**
- `1234` → **File size in bytes**
- `Feb 17 10:30` → **Last modification date**
- `file.txt` → **File name**

Break down **permission types**:
```
-rw-r--r--  
 │ │  │  │
 │ │  │  └── Others: Read (r) only
 │ │  └── Group: Read (r) only
 │ └── Owner: Read (r) and Write (w)
 └── File type (- for file, d for directory)
```

---

## **2️⃣ `chmod` (Change File Permissions)**
**Syntax:**
`chmod [mode] file`

Teach them **symbolic** and **numeric** methods.
### **Symbolic Method**
```
chmod u+x file.sh   # Give execute permission to owner
chmod g-w file.txt  # Remove write permission from group
chmod o+r file.txt  # Add read permission to others

```

### **Numeric Method**
Explain permission numbers:
- `r` = 4 (read)
- `w` = 2 (write)
- `x` = 1 (execute)
`chmod 755 file.sh`
Break it down:
- `7` (Owner) → `rwx` (4+2+1)
- `5` (Group) → `r-x` (4+0+1)
- `5` (Others) → `r-x` (4+0+1)
---
## **3️⃣ `chown` (Change File Owner)**
**Syntax:**
```
chown [new_owner] file
chown [new_owner]:[new_group] file
```
Examples:
```
chown deepak file.txt        # Change owner to "deepak"
chown deepak:developers file.txt  # Change owner to "deepak" and group to "developers"
chown -R deepak /var/www     # Recursively change owner of a directory
```

---

## **4️⃣ `chgrp` (Change Group Ownership)**
**Syntax:**
`chgrp [new_group] file`
Example:
```
chgrp developers file.txt  # Change group to "developers"
chgrp -R admins /opt/data  # Change group for all files in /opt/data
```

---

## **5️⃣ Special Permissions: `SUID`, `SGID`, `Sticky Bit`**
### **SUID (Set User ID)**
When a file has **SUID**, it runs with the owner's privileges, not the user's.
`chmod u+s script.sh  # Enable SUID 
`ls -l script.sh`
Output:
`-rwsr-xr-x  1 root root 1234 Feb 17 11:00 script.sh`
- `s` in **owner’s execute bit** means SUID is set.
### **SGID (Set Group ID)**
When set on directories, new files inherit the group's ownership.
`chmod g+s /shared 
`ls -ld /shared`
Output:
`drwxr-sr-x  1 deepak developers 4096 Feb 17 11:10 /shared`
- `s` in **group’s execute bit** means SGID is set.

### **Sticky Bit**
Used on directories (`/tmp`) to prevent users from deleting others' files.
`chmod +t /tmp 
`ls -ld /tmp`
Output:
`drwxrwxrwt  10 root root 4096 Feb 17 11:15 /tmp`
- `t` in **others' execute bit** means the sticky bit is set.

---
## **6️⃣ Hands-on Exercises**
💡 **Let interns practice with these tasks:**
1. **Check permissions** of all files in their home directory:
    `ls -l ~`
    
2. **Create a file and modify its permissions:**    
    `touch myfile.txt 
    `chmod 640 myfile.txt`

3. **Change ownership of a file (if they have `sudo` access):**
    `sudo chown root:users myfile.txt`
    
4. **Enable SUID on a script and test its behavior:**
    `chmod u+s myscript.sh`
    
5. **Create a shared folder with SGID and Sticky Bit:**   
    `mkdir /tmp/shared chmod 2777 /tmp/shared`
---
## **7️⃣ Summary Table for Quick Reference**

|Command|Purpose|Example|
|---|---|---|
|`chmod`|Change file permissions|`chmod 755 file.sh`|
|`chown`|Change file owner|`chown deepak file.txt`|
|`chgrp`|Change group ownership|`chgrp developers file.txt`|
|`chmod u+s`|Set SUID (run as owner)|`chmod u+s script.sh`|
|`chmod g+s`|Set SGID (inherit group)|`chmod g+s /shared`|
|`chmod +t`|Set sticky bit (protect files)|`chmod +t /tmp`|

---
### **How to Proceed Next?**
🔹 Test their knowledge with **real-world scenarios** like managing shared folders, securing scripts, and setting up access restrictions.  
🔹 Introduce **ACLs (Access Control Lists)** for **granular permissions**:
`setfacl -m u:deepak:rwx myfile.txt getfacl myfile.txt`
 🚀