### **1️⃣ List all `.log` files in `/var/log` sorted by modification time**
`ls -lt /var/log/*.log`
- `-l` → Long listing format
- `-t` → Sort by modification time (newest first)
To display the oldest first:
`ls -ltr /var/log/*.log`

---
### **2️⃣ Copy only `.txt` files from `/home/user/docs` to `/tmp`**
`cp /home/user/docs/*.txt /tmp/`
- Copies only `.txt` files from `/home/user/docs` to `/tmp`.
For recursive copy (if subdirectories exist):
`find /home/user/docs -type f -name "*.txt" -exec cp {} /tmp/ \;`

---

### **3️⃣ Find all files modified in the last 7 days inside `/var/log`**
`find /var/log -type f -mtime -7`
- `-type f` → Only files
- `-mtime -7` → Modified in the last 7 days

To include directories as well:
`find /var/log -mtime -7`

---

### **4️⃣ Count the number of `.log` files in `/var/log`**
`ls /var/log/*.log | wc -l`
`find /var/log -type f -name "*.log" | wc -l`
- `wc -l` → Counts the number of lines (i.e., files found)

---
### **5️⃣ Print a message showing the current user and their home directory**
`echo "Current user: $USER, Home directory: $HOME"`

`echo "Current user: $(whoami), Home directory: $(echo $HOME)"`

---
### **6️⃣ Find the 5 largest files in `/var/log`**
`du -ah /var/log | sort -rh | head -5`
- `du -ah` → Show disk usage for all files, human-readable
- `sort -rh` → Sort by size, largest first
- `head -5` → Show the top 5

---
### **7️⃣ Display the top 10 processes consuming the most memory**
`ps aux --sort=-%mem | head -11`
- `ps aux` → Show all processes
- `--sort=-%mem` → Sort by memory usage (descending)
- `head -11` → Shows top 10 + header

Alternative:
`top -b -o +%MEM | head -17`
- `top -b` → Batch mode
- `-o +%MEM` → Sort by memory usage

---

### **8️⃣ Archive all `.log` files in `/var/log` into a `.tar.gz`**
`tar -czvf /tmp/logs_backup.tar.gz /var/log/*.log`
- `tar -czvf` → Create (`c`), compress (`z`), verbose (`v`), file (`f`)
- `/tmp/logs_backup.tar.gz` → Output file
- `/var/log/*.log` → Files to archive

To archive all logs recursively:
`tar -czvf /tmp/logs_backup.tar.gz /var/log`

---
💡