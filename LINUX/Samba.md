# Notes on Samba User Management and File Sharing (RHEL 8/9)

## 1. What is Samba?
**Samba** is an open-source implementation of Microsoft's **SMB (Server Message Block)** protocol.

It allows a Linux server to:
- Share files with Windows computers
- Share printers
- Join an Active Directory domain
- Authenticate Windows users
- Act as a file server for mixed Windows/Linux environments

Typical architecture:
```scss
              Windows PC
                    │
               SMB Protocol
                    │
        ┌────────────────────┐
        │    Samba Server    │
        │       (RHEL)        │
        └────────────────────┘
                    │
             Linux Filesystem
```

# 2. Samba Architecture
There are two important daemons.
## smb

Provides
- File sharing
- Authentication
- Printer sharing

Check it:
```
systemctl status smb
```

## nmb (Older NetBIOS service)

Provides
- NetBIOS name resolution
- Network browsing

Modern environments often don't require it.

# 3. Linux User vs Samba User
This confuses many beginners.
Linux and Samba have **separate authentication databases**.

Suppose you create
```
john
```

using
```
useradd john
```

Linux knows about the user.

But Samba **does not**.

You must register that user inside Samba.

```scss
Linux User
      │
      ▼
useradd john
      │
      ▼
Samba Password Database
      │
      ▼
smbpasswd -a john
```

Therefore every Samba user must first exist as a Linux user.

# 4. Creating a Linux User
Create user
```
sudo useradd -m john
```

Options
```
-m
```

creates
```
/home/john
```

Verify
```
cat /etc/passwd
```

Example
```
john:x:1005:1005:John:/home/john:/bin/bash
```

Meaning
```
usernamepassword placeholderUIDGIDdescriptionhome directoryshell
```

# 5. Set Linux Password
```
sudo passwd john
```

This password is used for
- SSH
- Login
- sudo (if configured)

It is **not** used by Samba.

# 6. Add User to Samba
Register user
```
sudo smbpasswd -a john
```

You'll be prompted for a Samba password.

Enable user
```
sudo smbpasswd -e john
```

Now Samba knows the user.

# 7. Where Does Samba Store Passwords?
Linux
```
/etc/shadow
```

Samba
```
/var/lib/samba/private/passdb.tdb
```

You normally never edit this file manually.

# 8. List Samba Users
```
sudo pdbedit -L
```

Example
```
john:1001:deepak:1002:
```

Detailed information
```
sudo pdbedit -Lv john
```

# 9. Create a Shared Directory
Example
```
sudo mkdir -p /srv/samba/john
```

Why `/srv/samba`?
Linux follows the Filesystem Hierarchy Standard (FHS), where `/srv` is intended for data served by network services. While not mandatory, it's a common best practice for Samba shares.


# 10. Linux Ownership
Assign ownership

```
sudo chown john:john /srv/samba/john
```

Meaning
```
Owner  -> johnGroup  -> john
```

Check
```
ls -ld /srv/samba/john
```

Example
```
drwxrwx--- john john
```

# 11. Linux Permissions
Example
```
chmod 770 /srv/samba/john
```

Meaning
```
Owner -> rwxGroup -> rwxOthers -> ---
```

Numeric permission table

|Value|Permission|
|---|---|
|7|rwx|
|6|rw-|
|5|r-x|
|4|r--|
|0|---|


# 12. SELinux
Even with correct Linux permissions, SELinux can still deny Samba access.

Check SELinux
```
getenforce
```

Example
```
Enforcing
```

Label directory
```
sudo semanage fcontext -a -t samba_share_t "/srv/samba(/.*)?"
```

Apply label
```
sudo restorecon -Rv /srv/samba
```

Check label
```
ls -Zd /srv/samba
```

Expected
```
system_u:object_r:samba_share_t
```


# 13. Samba Configuration
Configuration file

```
/etc/samba/smb.conf
```

Example

```ini
[global]

workgroup = WORKGROUP

security = user

map to guest = Bad User

log file = /var/log/samba/%m.log

max log size = 1000

[documents]

path = /srv/samba/documents

browseable = yes

writable = yes

valid users = john

guest ok = no

create mask = 0664

directory mask = 0775
```

# 14. Understanding Each Parameter
## path
Actual Linux directory
```
path=/srv/samba/documents
```

## browseable
```
browseable = yes
```
Visible in Windows Explorer.

## writable

```
writable = yes
```

Users can write files.

## guest ok

```
guest ok = no
```

No anonymous access.

## valid users
```
valid users = john
```

Only John may access.

Multiple users
```
valid users = john deepak admin
```

or
```
valid users = @developers
```

for a Linux group.

## create mask
Permissions for new files
```
0664
```

Meaning
```
rw-rw-r--
```

## directory mask
Permissions for new directories

```
0775
```

Meaning

```
rwxrwxr-x
```

# 15. Validate Configuration
```
testparm
```

Never restart Samba before running this. It checks for syntax errors in `smb.conf`.

# 16. Restart Samba

```
sudo systemctl restart smb
```

Enable at boot

```
sudo systemctl enable smb
```

# 17. Firewall
Allow Samba
```
sudo firewall-cmd --permanent --add-service=samba
```

Reload
```
sudo firewall-cmd --reload
```

Verify
```
firewall-cmd --list-services
```

# 18. Connecting from Windows
Open File Explorer
```
\\192.168.1.20\documents
```

Windows prompts
```
UsernamePassword
```

Enter
```
john********
```

# 19. Common Samba Commands
Check configuration
```
testparm
```

List shares
```
smbclient -L localhost -U john
```

Connect locally
```
smbclient //localhost/documents -U john
```

Restart
```
systemctl restart smb
```

Check service
```
systemctl status smb
```

List users
```
pdbedit -L
```

Delete Samba user
```
smbpasswd -x john
```

# 20. Troubleshooting
If you see **Access denied**:
1. Check the user exists:    
    ```
    id john
    ```
    
2. Verify the Samba user:    
    ```
    pdbedit -L
    ```
    
3. Check Linux permissions:    
    ```
    ls -ld /srv/samba/documents
    ```
    
4. Check SELinux labels:    
    ```
    ls -Zd /srv/samba/documents
    ```
    
5. Validate the configuration:    
    ```
    testparm
    ```
    
6. Review logs:    
    ```
    journalctl -u smbtail -f /var/log/samba/log.smbd
    ```

# 21. Best Practices
- Create a dedicated directory (such as `/srv/samba`) for network shares.
- Use Linux groups to manage access instead of listing individual users where possible.
- Keep `guest ok = no` unless anonymous access is intentionally required.
- Validate configuration with `testparm` before restarting the service.
- Keep SELinux enabled and configure the proper contexts rather than disabling it.
- Back up `smb.conf` before making significant changes.

---

# Summary Workflow
```scss
Create Linux User
        │
        ▼
Set Linux Password
        │
        ▼
Create Samba Password
        │
        ▼
Create Share Directory
        │
        ▼
Set Ownership (chown)
        │
        ▼
Set Permissions (chmod)
        │
        ▼
Configure SELinux Context
        │
        ▼
Configure /etc/samba/smb.conf
        │
        ▼
Validate (testparm)
        │
        ▼
Restart smb Service
        │
        ▼
Allow Samba in Firewall
        │
        ▼
Connect from Windows
```

These notes cover the core concepts you'll use in most production environments. As you become more comfortable, you can build on this by exploring **group-based shares, Access Control Lists (ACLs), integration with Active Directory, Samba as a Domain Controller, SMB protocol versions (SMB2/SMB3), and performance tuning** for enterprise deployments.