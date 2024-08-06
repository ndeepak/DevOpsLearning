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

---
commands `locate`, `find`, `chmod`, `chown`, `df`, and `du`, explaining their usage with code examples and practical use cases.

### 1. `locate` Command

The `locate` command is used to find files in a directory hierarchy quickly. It searches through a pre-built database (usually updated periodically by the `updatedb` command) and returns paths to files matching the search criteria.

#### Basic Syntax
`locate [OPTIONS] PATTERN`

#### Examples

**Example 1: Basic Usage
```
# Find all files named 'bashrc'
locate bashrc

# Output (example)
# /home/user/.bashrc
# /etc/skel/.bashrc
```

**Example 2: Find Files with a Specific Extension
```
# Find all files with the .txt extension
locate "*.txt"

# Output (example)
# /home/user/documents/notes.txt
# /home/user/todo.txt

```

### 2. `find` Command

The `find` command searches for files in a directory hierarchy based on various criteria, such as file name, type, modification time, size, etc. Unlike `locate`, `find` searches the file system in real-time.

#### Basic Syntax
`find [PATH] [OPTIONS] [EXPRESSION]`

#### Examples

**Example 1: Find Files by Name
```
# Find all files named 'example.txt' in the current directory and its subdirectories
find . -name "example.txt"

# Output (example)
# ./documents/example.txt
```

**Example 2: Find Files Modified in the Last 7 Days
```
# Find files modified in the last 7 days in the /var/log directory
find /var/log -type f -mtime -7

# Output (example)
# /var/log/syslog.1
# /var/log/auth.log
```

**Example 3: Find and Execute a Command
```
# Find and delete all .tmp files in /tmp
find /tmp -name "*.tmp" -type f -delete

```

### 3. `chmod` Command

The `chmod` command changes the file mode (permissions) of a file or directory. It can set read, write, and execute permissions for the owner, group, and others.

#### Basic Syntax
`chmod [OPTIONS] MODE FILE`

#### Examples

**Example 1: Set File Permissions Using Numeric Mode
```
# Set permissions to 755 (rwxr-xr-x) for a script.sh file
chmod 755 script.sh

# Output (example)
# -rwxr-xr-x 1 user user 1234 Aug 7 12:34 script.sh
```

**Example 2: Set File Permissions Using Symbolic Mode**
```
# Add execute permission for the user
chmod u+x script.sh

# Remove write permission for others
chmod o-w file.txt
```

### 4. `chown` Command

The `chown` command changes the owner and group of a file or directory.

#### Basic Syntax
`chown [OPTIONS] OWNER[:GROUP] FILE`

#### Examples

**Example 1: Change Owner
```
# Change the owner of file.txt to user 'john'
chown john file.txt

# Output (example)
# -rw-r--r-- 1 john user 1234 Aug 7 12:34 file.txt
```

**Example 2: Change Owner and Group
```
# Change the owner to 'john' and the group to 'developers'
chown john:developers project/

# Output (example)
# drwxr-xr-x 1 john developers 4096 Aug 7 12:34 project/
```

### 5. `df` Command

The `df` command reports file system disk space usage. It shows the amount of disk space used and available on mounted file systems.

#### Basic Syntax

`df [OPTIONS] [FILE]`

#### Examples

**Example 1: Display Disk Space Usage**

```
# Show disk space usage in human-readable format
df -h

# Output (example)
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1        50G   20G   28G  42% /
# /dev/sda2        30G   10G   18G  36% /home
```

**Example 2: Display Specific File System**
```
# Display disk space usage for /home
df -h /home

# Output (example)
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda2        30G   10G   18G  36% /home

```

### 6. `du` Command

The `du` command estimates file space usage. It can display the size of a directory and its contents, showing both the total size and the size of individual files or subdirectories.

#### Basic Syntax
`du [OPTIONS] [FILE]`

#### Examples

**Example 1: Display Directory Size**
```
# Display disk space usage for /home
df -h /home

# Output (example)
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda2        30G   10G   18G  36% /home
```

**Example 2: Display Size of Files and Subdirectories**

sh

Copy code

```
# Show the size of each file and subdirectory in the /home/user directory
du -h /home/user

# Output (example)
# 100M    /home/user/Documents
# 200M    /home/user/Downloads
# 500M    /home/user
```

These commands are essential for system administration, file management, and security. They allow you to navigate the filesystem, manage permissions, monitor disk usage, and more.