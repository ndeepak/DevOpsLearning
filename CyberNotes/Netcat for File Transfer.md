### 📖 **Netcat (nc) for File Transfer**
Netcat (often called **nc**) is a simple, powerful command-line tool used for reading, writing, and transferring data over networks using TCP or UDP. It's often referred to as a "Swiss Army knife" for networking.
✅ **Key Use Case**:
- File Transfer (Linux ↔ Linux / Linux ↔ Windows / Windows ↔ Windows)
- Quick File Sharing Without Setup
- Network Troubleshooting
---
## 🛠 **Netcat Installation**
- **On Linux (Ubuntu/Debian)**
`sudo apt install netcat`
- **On Linux (RHEL/CentOS)**
`sudo yum install nc`
- **On Windows**
- Download Netcat (`nc.exe`) from trusted sources like **nmap.org**.
- Place it in `C:\Windows\System32` for easy access from `cmd`.
---
## 🔎 **Example 1: Sending a File from Source to Destination**
### 🖥️ **On the Destination (Receiving Side)**
1. Open a terminal and run Netcat to listen on a port.
2. Save the incoming file using the `>` operator.
`nc -l 12345 > receivedfile.txt`
- `-l` → Listen mode
- `12345` → Arbitrary port number (Choose an unused port)
- `> receivedfile.txt` → File where data will be saved

---
### 🖥️ **On the Source (Sending Side)**
1. Open a terminal.
2. Use Netcat to send the file using `<` operator.
`nc <Receiver_IP> 12345 < myfile.txt`
- `<Receiver_IP>` → IP address of the receiving machine
- `12345` → Must match the listening port
- `myfile.txt` → File you want to transfer
**Example:**
`nc 192.168.1.5 12345 < data.txt`
- This will send `data.txt` from the source to `receivedfile.txt` on the destination.
---
## 🔎 **Example 2: Sending a File from Destination to Source**
You can reverse the process if needed.
### 🖥️ **On the Source (Now Receiving)**
`nc -l 54321 > newfile.txt`
- `-l 54321` → Listen on port 54321
- `newfile.txt` → File to store the incoming data

### 🖥️ **On the Destination (Now Sending)**
`nc <Source_IP> 54321 < filetosend.txt`
- `filetosend.txt` → File that you want to send
---
## 🔎 **Example 3: Verify File Transfer**
After the transfer, check if the file was received correctly using the `md5sum` command:
`md5sum myfile.txt 
`md5sum receivedfile.txt`
- If the checksums match, the file transfer was successful.
---
## 🚀 **Additional Tips for Using Netcat**
1. **File Compression** (For faster transfer):
`tar -czf - myfile.txt | nc <Receiver_IP> 12345`
- On the receiver:
`nc -l 12345 | tar -xzf -`

2. **Multiple Files Transfer**  
    You can zip multiple files and transfer:
```
tar -czvf files.tar.gz file1.txt file2.txt file3.txt
nc <Receiver_IP> 12345 < files.tar.gz
```
- On the receiver:
`nc -l 12345 > files.tar.gz tar -xzvf files.tar.gz`
---
## 🧑‍💻 **Troubleshooting Tips**
- Ensure the firewall on both systems allows traffic on the specified port (`12345` or any other you choose).
`sudo ufw allow 12345`
- If the file is empty on the receiver, confirm the port and IP address are correct.
- Use `netstat` or `ss` to check listening ports:
`sudo netstat -tuln | grep 12345`

---
## ✅ **Conclusion**
- **Netcat** is a lightweight and efficient tool for file transfers in local or remote networks.
- No additional configuration or server setup is needed.
- Suitable for quick one-time file transfers, especially when other options like SCP or FTP aren't available.