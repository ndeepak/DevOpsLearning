### **The Ultimate Command-Line Challenge - Solutions**

#### **Task 1: Text Editors and Viewing**
1. **Create a file named `notes.txt` using `nano` and add content:**
    `nano Editors/notes.txt`
    
    _(Inside nano, write about your favorite Linux command, e.g., "I love the `grep` command because it allows me to search through files quickly.")_
    
2. **Edit the file using `vi`:
    `vi Editors/notes.txt`
    
    _(Add more details using `vi` editor, for example: "It helps me filter out unnecessary information and find exactly what I need.")_
    
3. **Edit the file using `jed`:**
    `jed Editors/notes.txt`
    
    _(Further edit or add to the content, e.g., "The ability to use regular expressions with `grep` makes it even more powerful.")_
    
4. **Use `cat` to display the content of `notes.txt`:**
    `cat Editors/notes.txt`
    
5. **Display the first three lines using `head`:**
    `head -n 3 Editors/notes.txt`
    
6. **Display the last three lines using `tail`:**
    `tail -n 3 Editors/notes.txt`
    

#### **Task 2: Text Processing**
1. **Create `data.txt` with random text:*
    `echo -e "Linux is great.\nI enjoy coding.\nLinux and UNIX are different.\nBash is a great shell.\nSed is useful." > DataProcessing/data.txt`
    
2. **Use `grep` to find lines containing "Linux":
    `grep "Linux" DataProcessing/data.txt`
    
3. **Use `sed` to replace "Linux" with "UNIX":**
    `sed -i 's/Linux/UNIX/g' DataProcessing/data.txt`
    
4. **Create a CSV-like file `employees.csv`:**
    `echo -e "Name,Position,Salary\nAlice,Developer,70000\nBob,Manager,90000\nCharlie,Designer,60000\nDave,Analyst,65000\nEve,Engineer,80000" > DataProcessing/employees.csv`
    
5. **Use `awk` to display "Name" and "Salary":**
    `awk -F, '{print $1, $3}' DataProcessing/employees.csv`
    
6. **Sort `employees.csv` by "Salary":**
    `sort -t, -k3 -n DataProcessing/employees.csv`
    
7. **Use `cut` to extract the "Position" column:**
    `cut -d, -f2 DataProcessing/employees.csv`
    
8. **Create `data_old.txt` and use `diff` to compare with `data.txt`:**
```
echo -e "UNIX is great.\nI enjoy coding.\nLinux and UNIX are different.\nBash is a great shell.\nSed is useful." > DataProcessing/data_old.txt
diff DataProcessing/data_old.txt DataProcessing/data.txt
```
    
9. **Use `tee` to write to a file and display it:**
    `echo "This is a test line." | tee DataProcessing/output.txt`
    

#### **Task 3: File and User Management**
1. **Use `locate` to find the `passwd` file:**
    `locate passwd`
    
2. **Use `find` to search for `.txt` files:
    `find CommandChallenge/ -name "*.txt"`
    
3. **Create `permissions_test.txt` and set permissions to `644`:**
```
touch SystemManagement/permissions_test.txt
chmod 644 SystemManagement/permissions_test.txt
```
    
4. **Change the owner of `permissions_test.txt`:**
    `sudo chown newuser SystemManagement/permissions_test.txt`
    
5. **Create a new user `testuser`:**
    `sudo useradd testuser`
    
6. **Delete the user `testuser`:**
    `sudo userdel testuser`
    
7. **Practice using `sudo` and `su`:**
    `sudo command su - otheruser`
    

#### **Task 4: System Monitoring and Management**
1. **Check disk space usage with `df`:**
    `df -h`
    
2. **Display disk usage of `CommandChallenge`:**
    `du -sh CommandChallenge/`
    
3. **Monitor processes with `top` and `htop`:**
    `top htop`
    
4. **List running processes with `ps`:**
    `ps aux`
    
5. **Display system information with `uname`:**
    `uname -a`
    
6. **Show the system's hostname:**
    `hostname`
    
7. **Measure command execution time:**
    `time ls`
    
8. **Manage services with `systemctl`:**
```
sudo systemctl start httpd
sudo systemctl status httpd
sudo systemctl stop httpd
```
    
9. **Monitor command output with `watch`:**
    `watch df -h`
    
10. **List background jobs:**
    `jobs`
    
11. **Terminate a process with `kill`:**
    `kill <PID>`
    
12. **Schedule a system shutdown:**
```
sudo shutdown -h +1
sudo shutdown -c
```
    

#### **Task 5: Networking**
1. **Check connectivity with `ping`:**
    `ping google.com`
    
2. **Download a file with `wget`:**
    `wget http://example.com/samplefile.txt`
    
3. **Fetch a webpage with `curl`:**
    `curl http://example.com`
    
4. **Securely copy files with `scp`:**
    `scp /path/to/file user@remote:/path/to/destination`
    
5. **Display network interfaces with `ifconfig`:**
    `ifconfig`
    
6. **Show network information with `netstat`:
    `netstat -tuln`
    
7. **Trace the path to a destination with `traceroute`:**    
    `traceroute google.com`
    
8. **Query DNS with `nslookup`:**
    `nslookup example.com`
    
9. **Display DNS information with `dig`:**
    `dig example.com`
    

#### **Task 6: Miscellaneous Commands**
1. **View and re-execute commands with `history`:
```
history
!42  # Re-execute command number 42
```
    
2. **Read the manual for `grep`:**
    `man grep`
    
3. **Print a message with `echo`:**
    `echo "Hello, World!" | tee hello.txt`
    
4. **Create a symbolic link with `ln`:**
    `ln -s /path/to/original /path/to/link`
    
5. **Create and remove an alias:**
```
alias ll='ls -la'
unalias ll
```
    
6. **Display the current month's calendar:**
    `cal`

### **Submission:**
1. **Create `CommandChallenge_Completion.txt`:**
    - Document the steps taken to complete each task.
    - Include challenges faced and solutions found.
    - Provide relevant outputs or screenshots where necessary.