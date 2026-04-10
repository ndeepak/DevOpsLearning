# Lab-Linux Challenge 3

![](LINUX/Linux%20Challenges%20Kodekloud/Attachments/Pasted%20image%2020260409150428.png)

Some new developers have joined our team, so we need to create some `users/groups` and further need to setup some `permissions` and `access rights` for them.  
Inspect the requirements in detail by clicking on the icons of the interactive architecture diagram on the right and complete the tasks. Once done click on the `Check` button to validate your work.
`sudo su -`

---
## admins and sudo
Create a group called "admins"
Make sure all users under "admins" group can run all commands with "sudo" and without entering any password.
```bash
groupadd admins

echo '%admins ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers 
```

---

## David
Create a user called "david" , change his login shell to "/bin/zsh" and set "D3vUd3raaw" password for this user.
Make user "david" a member of "admins" group.
```bash
useradd -s /bin/zsh david
echo "D3vUd3raaw" | passwd --stdin david
```

```bash
usermod -aG admins david
```

---

## natasha
Create a user called "natasha" , change her login shell to "/bin/zsh" and set "DwfawUd113" password for this user.
```bash
useradd -s /bin/zsh natasha
echo "DwfawUd113" | passwd --stdin natasha
```
Make user "natasha" a member of "admins" group.
```bash
usermod -aG admins natasha
```

---

## devs
Create a group called "devs"
```bash
groupadd devs
```

---

## ray
Create a user called "ray" , change his login shell to "/bin/sh" and set "D3vU3r321" password for this user.
```bash
useradd -s /bin/sh ray
echo "D3vU3r321" | passwd --stdin ray
```
Make user "ray" a member of "devs" group.
```bash
usermod -aG devs ray
```

## lisa
Create a user called "lisa", change her login shell to "/bin/sh" and set "D3vUd3r123" password for this user.
```bash
useradd -s /bin/sh lisa
echo "D3vUd3r123" | passwd --stdin lisa
```
Make user "lisa" a member of "devs" group.
```bash
usermod -aG devs lisa
```

---
## /data
Make sure "/data" directory is owned by user "bob" and group "devs" and "user/group" owner has "full" permissions but "other" should not have any permissions.
```bash
chown bob:devs /data
chmod 770 /data
```

## access-control
Give some additional permissions to "admins" group on "/data" directory so that any user who is the member the "admins" group has "full permissions" on this directory.
```bash
setfacl -m g:admins:rwx /data
```



## sudo (dnf)
Make sure all users under "devs" group can only run the "dnf" command with "sudo" and without entering any password.
```bash
echo '%devs ALL=(ALL) NOPASSWD:/usr/bin/dnf' >> /etc/sudoers
```

## limits
Configure a "resource limit" for the "devs" group so that this group (members of the group) can not run more than "30 processes" in their session. This should be both a "hard limit" and a "soft limit", written in a single line.
```bash
echo '@devs            -       nproc           30' >> /etc/security/limits.conf
```

## quota
Edit the disk quota for the group called "devs". Limit the amount of storage space it can use (not inodes). Set a "soft" limit of "100MB" and a "hard" limit of "500MB" on "/data" partition.
```bash
setquota -g devs 100M 500M 0 0 /dev/vdb1
```