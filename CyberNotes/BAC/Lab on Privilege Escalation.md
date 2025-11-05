Step-by-step with **hands-on lab scenarios** that simulate **both Vertical and Horizontal Privilege Escalation**. These will be relevant to your CAPenX and practical security testing skills.

---
## ⚙️ **LAB 1: Vertical Privilege Escalation (Linux SUID Exploitation)**
### 🧪 **Goal**: Exploit a misconfigured SUID binary to gain root shell
### 🛠️ Setup (On a test VM like Kali or Ubuntu):
Create a fake vulnerable binary:
```
echo -e '#!/bin/bash\n/bin/bash' > /tmp/vuln
chmod +x /tmp/vuln
sudo chown root:root /tmp/vuln
sudo chmod u+s /tmp/vuln
```
### 🏃‍♂️ Run as normal user:
```
ls -l /tmp/vuln
# -rwsr-xr-x 1 root root 20 ... /tmp/vuln

/tmp/vuln
whoami
# root
```
🎯 **You escalated from normal user to root** — **Vertical Privilege Escalation**.
> 🧠 Tip: In real-world Linux systems, always check for SUID binaries:

`find / -perm -4000 -type f 2>/dev/null`

---

	## 🌐 **LAB 2: Horizontal Privilege Escalation (Web App - IDOR)**
### 🧪 **Goal**: Access another user's profile using direct object reference
### 🔧 Setup:
Assume a vulnerable Flask web app or try using DVWA (Damn Vulnerable Web App).
When logged in as user `alice`, the browser sends:
`GET /profile?id=101`

Try manually modifying:
`GET /profile?id=102`

✅ If it shows **Bob's profile**, this is **horizontal escalation**.

### 🔐 How to detect in Burp Suite:
- Intercept request    
- Modify the `id` parameter    
- Observe if response data leaks another user’s info
> 🧠 Real attack tools like **Burp Intruder** or **ffuf** can automate IDOR testing:

`ffuf -u https://target.com/profile?id=FUZZ -w users.txt -b "session=abc123"`

---
## 🧪 BONUS: CAPenX-Style Mock Challenge
### Challenge:
Target: https://mock.hackme.secops.group:8000  
Function: Domain to IP Converter
#### 🎯 Tasks:
1. Intercept form submission or API request.
2. Check for IDOR — try accessing logs of other users.
3. Check if uploaded scripts or inputs can trigger code execution (leading to root file access).
4. Access `/etc/flag`.
🧠 Hints:
- Try **vertical escalation** via command injection.
- Try **horizontal escalation** by manipulating session, user ID, or stored logs.

---

## ✅ Summary Table

|Scenario|Type|Exploit|Target|
|---|---|---|---|
|SUID bash shell|Vertical|SUID misconfiguration|Root shell|
|Web app IDOR `/profile?id=102`|Horizontal|Insecure access control|Another user|
|Web shell leads to `/etc/flag`|Vertical|Code injection → root file access|Root privilege|

---
