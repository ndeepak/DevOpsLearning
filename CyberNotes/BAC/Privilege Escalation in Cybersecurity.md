## 🔐 **Privilege Escalation in Cybersecurity**

Privilege Escalation is when a user gains **unauthorized access** to resources or performs actions beyond their intended permission level.
There are two main types:

---
## 🧱 1. **Vertical Privilege Escalation**
### 🔎 **Definition:**
Gaining **higher-level privileges** than originally assigned.  
E.g., A normal user becomes an admin or root.
### 🔧 **Example Scenario:**
Suppose you're logged in as:
`Username: user1 (Role: Basic User)`

You find a vulnerable file `/usr/bin/change_role` with **SUID bit** that lets any user run it as root.  
You exploit it to gain **root shell** access:
```
user1@server$ /usr/bin/change_role
root@server# whoami
root
```

### 🧪 **Pentest Example (Web App):**
- A normal user intercepts a request to access:
    `GET /admin/dashboard`    
    and gets a **200 OK** instead of 403.
✅ This is **Vertical Privilege Escalation** — accessing features meant only for higher roles.

---
## 🧍 2. **Horizontal Privilege Escalation**
### 🔎 **Definition:**
Gaining **access to other users’ data or actions** at the **same privilege level**.
### 🔧 **Example Scenario:**
Suppose:
- `user1` is logged in to a banking app.    
- They see their account info at:        
    `GET /account/1001`
- They manually change the ID to:
    `GET /account/1002`
- And it shows **user2's** information!

That’s horizontal escalation — accessing another user’s data without permission.

---
## 🧑‍💻 **Quick Comparison Table**

|Feature|Vertical Escalation|Horizontal Escalation|
|---|---|---|
|📈 Privilege Level Change|Yes (Low → High)|No (Same level)|
|🎯 Target|Admin/root or higher privilege features|Other users at same privilege|
|🧪 Exploit Type|Misconfigured permissions, SUID, auth bypass|IDOR, session manipulation, API weakness|
|🔐 Example|Normal user → Root|User A accesses User B's data|

---

## 🔍 Real-World Examples
### 🟡 Vertical Escalation
- Exploiting **sudo rights** or **SUID binaries**.    
- Misconfigured **setuid scripts**.    
- Exploiting a **web app role change** function.    

### 🔵 Horizontal Escalation
- **Insecure Direct Object Reference (IDOR)** vulnerabilities.
- Reusing valid session tokens (session fixation).    
- Broken access control in APIs.    

---
## 🔐 How to Prevent Privilege Escalation

|Risk|Mitigation|
|---|---|
|SUID Misuse (Linux)|Regular audits, restrict unnecessary SUID binaries|
|Broken Access Control|Implement strict role-based access (RBAC)|
|Session Hijacking|Use secure tokens, session timeouts, strong authentication|
|IDOR in Web Apps|Avoid exposing predictable object IDs, use server-side permission checks|

---

## 🧪 In Your PenTesting or Mock-Exam
When you’re exploiting:
- File permissions on Linux for `/etc/flag` or `/root/flag` → likely **vertical**.
- Accessing another user’s submitted data or logs via URL → likely **horizontal**.
---