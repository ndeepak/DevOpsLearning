### Linux Basics Commands for System Engineers

#### File and Directory Management
1. **List Files and Directories:**
    
```
    ls ls -l  # Long format 
    ls -a  # Include hidden files
```
    
2. **Change Directory:**
```
    cd /path/to/directory 
    cd ~  # Go to home directory 
    cd -  # Go to previous directory`
```
    
3. **Print Working Directory:**
    `pwd`
    
4. **Create Directory:**    
```
	mkdir new_directory 
    mkdir -p /path/to/new_directory  # Create parent directories if they don't exist`
```

5. **Remove Directory:**
```
    rmdir directory_name 
    rm -r directory_name  # Remove directory and its contents`
```
    
6. **Copy Files and Directories:**  
```
    cp source_file destination 
    cp -r source_directory destination  # Copy directory and its contents`
```
    
7. **Move/Rename Files and Directories:**
    `mv source_file destination`
    
8. **Remove Files:**
```
    rm file_name 
    rm -f file_name  # Force removal without prompt
```
#### File Viewing and Editing
1. **View File Contents:**
```
    cat file_name 
    less file_name  # View file with pagination 
    more file_name  # View file with pagination (older version of less)
```
    
2. **Edit Files:**
    `nano file_name vim file_name`
    
3. **Compare Files:**
    `diff file1 file2`
    
4. **Search for Text in Files:**
```
    grep "search_term" file_name 
    grep -r "search_term" /path/to/directory  # Recursive search
```
    

#### System Information

1. **Check System Information:**
```
    uname -a  # Kernel version and other info 
    lsb_release -a  # Linux distribution details
```
2. **Check Disk Usage:**
```
    df -h  # Human-readable format 
    du -h /path/to/directory  # Disk usage of specific directory`
```
3. **Check Memory Usage:**
    `free -h  # Human-readable format`
    
4. **Check CPU Information:**
    `lscpu`
    
5. **Check Running Processes:**
```
    ps aux  # List all running processes 
    top  # Real-time process monitoring 
    htop  # Enhanced version of top (requires installation)
```

#### User and Group Management
1. **Add New User:**
    `sudo adduser new_username`
    
2. **Delete User:**    
    `sudo deluser username`
    
3. **Add User to Group:**
    `sudo usermod -aG groupname username`
    
4. **Change User Password:**
    `sudo passwd username`
    
5. **List Users:**
    `cat /etc/passwd`
    
6. **List Groups:**
    `cat /etc/group`
#### Package Management (YUM)
1. **Update Package Index:**
    `sudo yum update`
    
2. **Install a Package:**
    `sudo yum install package_name`
    
3. **Remove a Package:**
    `sudo yum remove package_name`
    
4. **Search for a Package:**    
    `yum search package_name`
    
5. **List Installed Packages:**
    `yum list installed`
#### Networking
1. **Check Network Configuration:**
    `ifconfig  # Deprecated, use ip instead ip addr show`
    
2. **Check Network Connections:**
    `netstat -tuln  # List all listening ports`
    
3. **Ping a Host:**
    `ping hostname_or_ip`
    
4. **Traceroute:**
    `traceroute hostname_or_ip`
    
5. **Download Files:**
    `wget http://example.com/file curl -O http://example.com/file`
    
6. **SSH to Remote Host:**
    `ssh username@remote_host`
#### System Monitoring and Performance
1. **Check System Uptime:**
    `uptime`

2. **Monitor Real-Time Logs:**    
    `tail -f /var/log/syslog`
    
3. **Check Open Files:**
    `lsof`
    
4. **Measure Disk I/O:**
    `iostat`
#### Process Management
1. **Start/Stop a Service:**
```
    sudo systemctl start service_name 
    sudo systemctl stop service_name
```
2. **Enable/Disable a Service at Boot:**
```
    sudo systemctl enable service_name 
    sudo systemctl disable service_name
```
    
3. **Check Service Status:**
    `sudo systemctl status service_name`
    
4. **Kill a Process:**
    `kill process_id kill -9 process_id  # Force kill`
    
5. **Kill All Processes by Name:**
    `pkill process_name`
By mastering these basic Linux commands, a system engineer can effectively manage, monitor, and troubleshoot a Linux system.