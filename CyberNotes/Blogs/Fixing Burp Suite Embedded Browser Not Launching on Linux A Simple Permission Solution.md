# Fixing Burp Suite Embedded Browser Not Launching on Linux: A Simple Permission Solution

Have you ever clicked **“Open Browser”** in Burp Suite on Linux, only to be met with… nothing?  
No errors, no loading screen — just silence.

You’re not alone.

Many penetration testers and security professionals encounter this frustrating issue, especially after installing Burp Suite on **modern Linux distributions.**

**The culprit?**  
A simple but critical **permissions misconfiguration** that prevents Burp Suite’s embedded Chromium browser from launching correctly.

In this article, I’ll show you exactly how to diagnose and fix the problem in minutes, whether you're on Ubuntu, Fedora, Arch, or any other Linux flavor.

Let’s dive in.


Burp Suite is one of the most widely used web security tools, and its **embedded Chromium browser** is a crucial feature for many penetration testers and security engineers. However, on certain **Linux distributions**, users frequently encounter an issue where the embedded browser simply fails to launch when clicking **“Open Browser.”**

If you’ve run into this problem, this guide will walk you through **why it happens and how to fix it** quickly.

---

## The Problem: Why Burp Suite’s Embedded Browser Won’t Start

The issue is related to **Chromium sandboxing requirements** on modern Linux systems.  
Burp Suite bundles its own version of Chromium, which relies on a critical binary called **`chrome-sandbox`** to function securely.

In many **hardened or security-focused Linux distributions** (such as Ubuntu, Debian, Fedora, Arch, and their derivatives), the system restricts binaries that attempt to execute with elevated privileges unless they are correctly owned by the `root` user and have the **setuid bit** enabled.

When these ownership and permission requirements are missing, the Chromium-based browser inside Burp Suite fails to start, often **without any clear error message**.

---
## Why Does This Happen?
The issue can occur in several scenarios:
- After **upgrading your Linux distribution**, which may reset file permissions.
- After a **fresh installation** of Burp Suite where default permissions are not correctly applied.
- On **distributions with additional security layers**, such as SELinux or AppArmor.
---

## The Solution: Adjust Chrome-Sandbox Permissions
The solution is straightforward:  
You need to **locate the `chrome-sandbox` binary** inside your Burp Suite installation and apply the correct ownership and permissions.

---
### Step 1: Find the `chrome-sandbox` File
You can locate the sandbox binary by running the following command in your terminal:
`find ~ -type f -name "chrome-sandbox"`

This will output something like:
`/home/yourusername/BurpSuitePro/burpbrowser/126.0.6478.55/chrome-sandbox`

Your path and browser version may vary.

---

### Step 2: Apply the Correct Permissions
Once you have the full path to the `chrome-sandbox` file, run these commands:
```bash
sudo chown root:root /path/to/chrome-sandbox
sudo chmod 4755 /path/to/chrome-sandbox
```

Replace `/path/to/chrome-sandbox` with your actual file path.

#### Example:
```bash
sudo chown root:root /home/cas/BurpSuitePro/burpbrowser/126.0.6478.55/chrome-sandbox
sudo chmod 4755 /home/cas/BurpSuitePro/burpbrowser/126.0.6478.55/chrome-sandbox
```

---

## What These Commands Do:
- **`sudo chown root:root`**  
    Assigns the file to the `root` user and group, which is required for sandboxed execution.
- **`sudo chmod 4755`**  
    Sets the **setuid** bit (indicated by `4`), which allows the binary to run with the effective user ID of the file owner (in this case, `root`). This is critical for Chromium’s sandbox security model.
    

Without these exact settings, many modern Linux kernels will **block the execution of Chromium-based sandboxes** for security reasons.

---

## Why This Fix Works Across Linux Distributions

While this problem is often reported on Ubuntu, it is **not exclusive to any specific Linux distribution.**

Any modern Linux system that implements strict sandboxing, kernel hardening, or file permission policies can prevent the Burp Suite browser from launching if this binary isn’t configured correctly.

The same fix applies whether you are using:
- Ubuntu    
- Debian    
- Fedora    
- Arch Linux    
- Kali Linux    
- Other Debian/RHEL-based systems

---

## Key Notes:
- **Upgrades or reinstallation of Burp Suite** may reset these permissions, so you might need to reapply this fix occasionally.
    
- If you use tools like SELinux or AppArmor, additional sandbox restrictions might still interfere, but this permission fix resolves the most common issue.
    
- Always download Burp Suite directly from the official PortSwigger website to ensure the binaries are trustworthy.
    

---

## Conclusion
Linux’s evolving security posture is a great step for protecting systems, but sometimes it can unintentionally break the behavior of tools we rely on daily.
If your Burp Suite browser isn’t launching on Linux, this is almost always a **permissions issue related to the `chrome-sandbox` binary.**  
By adjusting ownership and enabling the setuid bit, you can restore full functionality in minutes.

If you’ve encountered variations of this issue on different distributions or found other related solutions, feel free to share your experience.


References:
- Burp Suite Official Site https://portswigger.net/burp
- Linux chmod command manual https://linux.die.net/man/1/chmod
- https://www.reddit.com/r/bugbounty/comments/1db1lh5/the_default_browser_in_burp_suite_isnt_launching/



Title
**How to Fix Burp Suite’s Embedded Browser Not Launching on Linux: Chrome-Sandbox Permissions Guide**

## **Tags:**
- Burp Suite    
- Linux    
- Ubuntu    
- Penetration Testing    
- Cybersecurity    
- Chrome Sandbox
- Linux File Permissions
- Ethical Hacking
- AppSec    
- Bug Bounty

Example phrases: `Burp Suite browser not launching`, `chrome-sandbox Linux fix`, `Burp Suite embedded browser issue on Ubuntu/Linux`.


## **Hashtags:**
- #BurpSuite
- #Linux    
- #CyberSecurity    
- #EthicalHacking     
- #PenetrationTesting    
- #BugBounty    
- #InfoSec    
- #LinuxTips    
- #WebSecurity    
- #AppSec    
- #LinuxPermissions    
- #SecurityTesting     
- #RedTeam    
- #BlueTeam    
- #SecurityTools

#BurpSuite #Linux #CyberSecurity #PenetrationTesting #EthicalHacking #LinuxPermissions #WebSecurity