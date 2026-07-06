# Enabling Guest Access to Samba Shares on Windows

## Overview

Modern versions of Windows (Windows 10, Windows 11, Windows Server 2019/2022) block **insecure guest logons** by default for security reasons.

If your Samba server is configured with a **public/guest share** (for example, `guest ok = yes`), Windows may display errors such as:

- **Windows cannot access \<server>\share**
- **You do not have permission to access this shared folder**
- **Access is denied**
- **Your organization's security policies block unauthenticated guest access**

This happens because Windows refuses guest (anonymous) SMB authentication unless it is explicitly enabled.


# Solution
Enable **AllowInsecureGuestAuth** in the Windows Registry.

> **Important:** Only do this if you intentionally use guest/public Samba shares in a trusted network. It is **not recommended** for production or untrusted networks because it allows unauthenticated SMB access.

---

# Method 1: Using Registry Editor
## Step 1: Open Registry Editor
Press:
```
Win + R
```

Type:
```
regedit
```

Click **OK**.

---

## Step 2: Navigate to

```scss
Computer
└── HKEY_LOCAL_MACHINE
    └── SOFTWARE
        └── Policies
            └── Microsoft
                └── Windows
```

---

## Step 3: Create a New Key

If it does not already exist:

- Right-click **Windows**
- Select **New → Key**
- Name it:

```
LanmanWorkstation
```

Your path should now be:

```
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\LanmanWorkstation
```

---

## Step 4: Create a DWORD Value

Inside the **LanmanWorkstation** key:

- Right-click → **New**
- Select **DWORD (32-bit) Value**
- Name it:

```
AllowInsecureGuestAuth
```

---

## Step 5: Set the Value

Double-click the newly created value.

Configure it as:

|Setting|Value|
|---|---|
|Base|Hexadecimal|
|Value data|**1**|

Result:

```
AllowInsecureGuestAuth = 1
```

---

## Step 6: Restart

Either:

- Restart the computer

or restart the **Workstation** service (a full restart is usually simpler).

---

# Registry Summary

|Registry Path|Value|
|---|---|
|`HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\LanmanWorkstation`||
|`AllowInsecureGuestAuth`|`1 (DWORD)`|

---

# PowerShell Method

Instead of using the Registry Editor, you can create the registry key from an elevated PowerShell session:

```powershell
New-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\LanmanWorkstation" -Force

New-ItemProperty `
-Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\LanmanWorkstation" `
-Name "AllowInsecureGuestAuth" `
-PropertyType DWord `
-Value 1 `
-Force
```

---

# Command Prompt Method

Run Command Prompt as **Administrator**:

```cmd
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\LanmanWorkstation" /v AllowInsecureGuestAuth /t REG_DWORD /d 1 /f
```

---

# Verify the Registry Value

Run:

```cmd
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows\LanmanWorkstation"
```

Expected output:

```scss
HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\LanmanWorkstation

AllowInsecureGuestAuth    REG_DWORD    0x1
```

---

# Why This Is Required

Suppose your Samba configuration contains:

```ini
[public]
path = /srv/samba/public
guest ok = yes
guest only = yes
browseable = yes
writable = yes
```

This share allows users to connect **without providing a username or password**.

Older Windows versions permitted this by default. However, newer Windows versions block guest authentication to reduce the risk of unauthorized access.

Setting:

```
AllowInsecureGuestAuth = 1
```

tells Windows that it is acceptable to connect to SMB shares using guest authentication.

---

# Security Considerations
⚠️ **Use this setting only when necessary.**

Enabling insecure guest authentication means:
- No username/password is required for the configured guest share.
- Anyone with network access may be able to read or modify files on that share, depending on your Samba configuration.
- It should only be used on trusted internal networks and for intentionally public shares.

For production environments, the recommended approach is to use authenticated Samba users (`valid users`, `smbpasswd`, etc.) instead of guest access whenever possible.

---

# Troubleshooting
If you still cannot access the share after enabling the registry value, verify the following:

- Samba service is running:    
    ```
    systemctl status smb
    ```
    
- Firewall allows Samba:    
    ```
    firewall-cmd --list-services
    ```
    
- SELinux labels are correct:    
    ```
    ls -Zd /srv/samba
    ```
    
- Samba configuration is valid:    
    ```
    testparm
    ```
    
- Guest access is enabled in `smb.conf` (if using a public share):    
    ```
    guest ok = yesguest only = yes
    ```
    
- Try accessing the share using:    
    ```
    \\<Server-IP>\<Share-Name>
    ```

For private shares, **do not** enable insecure guest authentication. Instead, create Linux and Samba users, configure `valid users` in `smb.conf`, and authenticate with a username and password.


---

Windows 11 blocks insecure SMB guest logons by default, which can prevent access to Samba shares configured with `guest ok = yes`. Microsoft recommends only enabling this in trusted environments, because guest logons weaken SMB security and do not support SMB signing or encryption.[learn.microsoft](https://learn.microsoft.com/en-us/windows-server/storage/file-server/enable-insecure-guest-logons-smb2-and-smb3)

To allow access, open **Local Group Policy Editor** and go to **Computer Configuration > Administrative Templates > Network > Lanman Workstation > Enable insecure guest logons**, then set it to **Enabled**. Microsoft says the same setting can also be enabled with PowerShell.[learn.microsoft](https://learn.microsoft.com/en-us/windows-server/storage/file-server/enable-insecure-guest-logons-smb2-and-smb3)

## PowerShell-only cheat sheet

Run PowerShell **as Administrator** and use this command:
`Set-SmbClientConfiguration -EnableInsecureGuestLogons $true -Force`

Microsoft documents this as the supported PowerShell method for allowing insecure guest logons on Windows 10, Windows 11, and supported Windows Server versions.