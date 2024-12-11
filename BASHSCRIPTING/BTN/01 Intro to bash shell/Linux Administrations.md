## **1. `uname` Command**
The `uname` command provides information about the system.
### **Common Options**
- **`uname -a`**: Displays all available system information.
    `uname -a`
    **Output Example**:
    `Linux hostname 5.15.0-50-generic #56~20.04.1-Ubuntu SMP Fri Oct 14 17:20:00 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux`
    
    **Explanation**:
    - `Linux`: Kernel name
    - `hostname`: System hostname
    - `5.15.0-50-generic`: Kernel version
    - `x86_64`: Machine hardware architecture
    - `GNU/Linux`: Operating system name
- **`uname -r`**: Displays only the kernel version.
    `uname -r`
    
    **Output Example**:
    `5.15.0-50-generic`

---
## **2. `who` Command**
The `who` command shows information about users currently logged into the system.
### **Common Options**
- **`who`**: Displays logged-in users along with terminal, login time, and IP address (if applicable).
    `who`
    
    **Output Example**:
    `user1    tty1        2024-12-11 10:30`
    
- **`who -a`**: Displays detailed information about all users, including system-level processes and dead processes.
    `who -a`
    **Output Example**:
    `system boot    2024-12-11 10:00 `
    `user1    tty1  2024-12-11 10:30`

---
## **3. `whoami` Command**
Displays the username of the current logged-in user.
`whoami`

**Output Example**:
`user1`

---
## **4. `id` Command**
The `id` command displays information about a user’s UID, GID, and group memberships.
### **Usage Examples**
- **`id`**: Displays information for the current user.
    `id`
    
    **Output Example**:
    `uid=1000(user1) gid=1000(user1) groups=1000(user1),27(sudo)`
    
- **`id username`**: Displays information for a specific user.
    `id user2`
    
    **Output Example**:
    `uid=1001(user2) gid=1001(user2) groups=1001(user2)`

---
## **5. `passwd` Command**
The `passwd` command is used to change the password of a user.
### **Usage Examples**
- **Change your own password**:
    `passwd`
    
- **Change another user's password (requires root privileges)**:
    `passwd user1`
---

## **6. `adduser` Command**
The `adduser` command is used to create a new user.
### **Usage Examples**
- **Add a new user**:
    `adduser user1`
    - Prompts for the password and additional user details (e.g., full name).
- **Add a user to a group**:
    `adduser user2 -aG root`
    
    - Adds `user2` to the `root` group.
---

## **7. `su` Command**
The `su` command allows switching to another user.
### **Usage Examples**
- **Switch to `user1`**:
    `su user1`
    - Prompts for `user1`'s password.

### **Shell Prompt Differences**
- **Root User (`#`)**:  
    A `#` at the prompt indicates the root user.
- **Regular User (`$`)**:  
    A `$` at the prompt indicates a non-root user.

---

## **8. `/etc/passwd` and `/etc/shadow` Files**
### **`/etc/passwd`**
- Stores user account information.
- Format:
    `username:x:UID:GID:Full Name:Home Directory:Shell`
    
- **Example**:
    `user1:x:1000:1000:User One:/home/user1:/bin/bash`
    

### **`/etc/shadow`**
- Stores hashed passwords and account expiration details.
- Only accessible by the root user.
- **Example**:
    `user1:$6$hashedpassword$saltsalt:19234:0:99999:7:::`

### **Permissions**
- View `/etc/shadow` file permissions:    
    `ls -la /etc/shadow`
    
    **Output Example**:
    `-r-------- 1 root root 1420 Dec 11 10:30 /etc/shadow`
---
## **9. `usermod` Command**
The `usermod` command modifies user accounts.
### **Usage Examples**
- **Add a user to a group**:
    `usermod -aG sudo user1`
    
- **Change a user’s home directory**:
    `usermod -d /new/home user1`
    
- **Change a user’s login name**:
    `usermod -l newuser user1`
---

## **10. `userdel` Command**
The `userdel` command deletes a user account.
### **Usage Examples**
- **Delete a user**:
    `userdel user1`
- **Delete a user and their home directory**:
    `userdel -r user1`
---
### **Practical Workflow**
1. Create a new user:
    `adduser user1`
    
2. Add the user to the `sudo` group:
    `usermod -aG sudo user1`
    
3. Verify the user's details:
    `id user1`
    
4. Switch to the new user:
    `su user1`
    
5. Check user account details:
    `cat /etc/passwd`
    
6. Remove the user (if needed):
    `userdel -r user1`