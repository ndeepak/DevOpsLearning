## ⚠️ Important: Windows Registry Setting Required (First-Time Access)

When accessing the Samba server **for the first time** from a Windows machine, the following registry key must be added to allow guest authentication.
### 🔧 Registry Configuration Steps
1. Press **Win + R**, type `regedit`, and press **Enter**    
2. Navigate to the following path:    
    ```
    Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows
    ```
3. Right‑click **Windows** → **New → Key**
    - Name the key:
        ```
        LanmanWorkstation
        ```        
4. Select the **LanmanWorkstation** key    
5. Right‑click in the right pane → **New → DWORD (32‑bit) Value**
    - Name:
        ```
        AllowInsecureGuestAuth
        ```
    - Set **Value data** to:
        ```
        1
        ```
        
    - Base: **Hexadecimal**
6. Close Registry Editor
    
7. **Restart the computer**
    

---

## ✅ Registry Path (Summary)

```
HKLM\SOFTWARE\Policies\Microsoft\Windows\LanmanWorkstation
AllowInsecureGuestAuth = 1 (DWORD)
```

---

## 🔐 Security Advisory (Very Important)

- This setting **allows insecure guest access**, which is **disabled by default in Windows 10/11** for security reasons.
- **Recommended only for**:
    - Internal LAN
    - Trusted environments
    - Legacy or guest‑based Samba shares

### ✅ Better (More Secure) Alternative – Recommended

Since your Samba server already uses:

INI

valid users = sovit, bikesh, himanshu, abik, ...  

``  

Show more lines

👉 **You should NOT need guest access at all.**  
Instead:

- Ensure users authenticate with:
    
    ```
    Username: <samba username>
    Password: <smbpasswd password>
    ```
    
- Disable guest access in Samba (`guest ok = no`)

This avoids registry changes and keeps Windows secure.

---

## ✅ When is This Registry Key Actually Required?

|Scenario|Required|
|---|---|
|Guest access (no username/password)|✅ Yes|
|Authenticated Samba users (`smbpasswd`)|❌ No|
|Domain / AD-based access|❌ No|

---

## ✅ Recommendation for Your Setup

Since you already configured:

- `valid users`
- `smbpasswd`
- Read/write controls

👉 **Do NOT enable AllowInsecureGuestAuth unless absolutely necessary**