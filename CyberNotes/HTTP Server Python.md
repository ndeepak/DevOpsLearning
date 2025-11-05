## ✅ **What Are We Trying to Do?**
We are trying to run a simple web server using Python on your machine. A web server serves files to your browser using HTTP (Hypertext Transfer Protocol).
The goal is to:
1. Start a Python HTTP server using the `http.server` module.
2. Access the files in a directory using a web browser.
3. Understand the commands and troubleshoot any issues.

---
## 🛠 **Prerequisites**
Before we start, make sure:
1. **Python 3** is installed on your system.
2. You have a basic understanding of opening a terminal and running commands.
3. You have some files (like `.html`, `.txt`, `.jpg`) to test with.

---
### **Step 1: Check If Python Is Installed**
1. Open your terminal.
2. Run this command to check if Python 3 is installed:
    `python3 --version`    
    - If Python is installed, it will return something like:
        `Python 3.x.x`        
    - If you get an error like `Command 'python3' not found`, install Python using:
        `sudo apt update sudo apt install python3`
3. Confirm installation using:    
    `python3 --version`

---
### **Step 2: Navigate to the Correct Directory**
- Python’s HTTP server will serve the files from your **current directory**.
- Navigate to the directory you want to serve using `cd` (change directory):
    `cd /path/to/your/files`    
- Example:
    `cd ~/Downloads`
- You can check the contents using:
    `ls`
---
### **Step 3: Start the Python HTTP Server**
Once you're in the directory, run this command:
`python3 -m http.server 91919`
**Explanation:**
- `python3` → Run Python 3
- `-m` → Use the module named `http.server`
- `http.server` → The built-in module that acts as a basic HTTP server
- `91919` → The port number where the server will listen for connections (You can use any port above **1024**)
---
### **Step 4: Access Your Server**
1. Once the server starts, you’ll see a message like:
    `Serving HTTP on 0.0.0.0 port 91919 ...`    
    - This means your server is running and waiting for requests.
2. Open your web browser and enter:    
    `http://localhost:91919`    
    - `localhost` means your own computer.
    - `91919` is the port you specified.
3. You’ll see the files from your current directory listed like this:
    `Index of / - file1.html - image.png - document.txt`   

---
### **Step 5: Understanding Ports**
- **What is a Port?**
    - A port is like a virtual door that allows data to come in and go out from your computer.
    - HTTP (web traffic) typically uses **port 80** for websites.
    - HTTPS (secure web traffic) uses **port 443**.
    - You’re using **port 91919** as a non-standard, user-defined port for testing.
- **How to Check If a Port is in Use**  
    Sometimes the port might already be used by another application. You can check using:    `sudo lsof -i :91919`
    If something is using it, you’ll see a process listed. You can kill it using:    
    `sudo kill <PID>`   
---
### **Step 6: Stopping the Server**
To stop the server, press:
`Ctrl + C`
This will terminate the Python process.

---
## 🛡️ **Troubleshooting Tips**
- **Error: Port Already in Use**
    - Change to a different port:        
        `python3 -m http.server 91920`
- **Error: Python Not Found**
    - Install Python using:        
        `sudo apt update sudo apt install python3`
- **Cannot Connect in Browser**
    - Ensure firewall rules are not blocking the port:
        `sudo ufw allow 91919`        
    - Then retry `http://localhost:91919`.

---
## 🚀 **Bonus Features**
- **Serve a Specific Directory** If you want to serve a particular directory instead of the current one: 
    `python3 -m http.server 91919 --directory /path/to/directory`
- **Bind to a Specific IP Address** If you want to allow other devices on the network to access your server:
    `python3 -m http.server 91919 --bind 0.0.0.0`
    - `0.0.0.0` means it will accept requests from any device on your network.
- **Log Requests** The server will print all HTTP requests to the terminal, useful for debugging.
---
## 🧑‍💻 **Final Thoughts**
- Python's HTTP server is great for quickly sharing files or testing your website.
- It’s not meant for production use. For actual web hosting, consider using servers like **Nginx** or **Apache**.
- Experiment by creating simple `.html` files and viewing them in your browser using the server.
