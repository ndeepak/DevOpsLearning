### **The Ultimate Command-Line Challenge**
Welcome to "The Ultimate Command-Line Challenge," an interactive assignment that will take you through a series of exercises to deepen your understanding of essential command-line tools in Linux, particularly for RPM-based systems like RHEL. This challenge covers a variety of commands related to text editing, file manipulation, system monitoring, networking, and more. Each task will help you master these tools and commands in a practical and fun way.

#### **Instructions:**
1. **Setup the Environment**:
    - Create a main directory called `CommandChallenge`.
    - Inside `CommandChallenge`, create subdirectories named `Editors`, `DataProcessing`, `SystemManagement`, and `Networking`.
2. **Tasks Overview**:
    - Each task will focus on a specific set of commands or tools.
    - Follow the instructions for each task and provide the necessary outputs or documentation.
    - Feel free to explore the man pages (`man command_name`) and other resources for help.

### **Tasks:**

#### **Task 1: Text Editors and Viewing**
- **Objective**: Familiarize yourself with text editors and basic file viewing commands.
- **Commands**: `nano`, `vi`, `jed`, `cat`, `head`, `tail`
- **Instructions**:
    1. Create a file named `notes.txt` in the `Editors` directory using `nano`. Write a short note about your favorite Linux command.
    2. Edit the same file using `vi` and `jed`, adding more details about why you like that command.
    3. Use `cat` to display the entire content of `notes.txt`.
    4. Use `head` to display the first three lines and `tail` to display the last three lines of the file.

#### **Task 2: Text Processing**
- **Objective**: Learn how to search, manipulate, and format text data.
- **Commands**: `grep`, `sed`, `awk`, `sort`, `cut`, `diff`, `tee`
- **Instructions**:
    1. Create a file named `data.txt` in the `DataProcessing` directory with at least five lines of random text.
    2. Use `grep` to find all lines containing the word "Linux" in `data.txt`.
    3. Use `sed` to replace the word "Linux" with "UNIX" in `data.txt`.
    4. Create a CSV-like file `employees.csv` with columns "Name,Position,Salary" and at least five rows.
    5. Use `awk` to display the "Name" and "Salary" columns.
    6. Use `sort` to sort `employees.csv` by "Salary".
    7. Use `cut` to extract the "Position" column.
    8. Create another text file `data_old.txt` and use `diff` to compare it with `data.txt`.
    9. Use `tee` to write "This is a test line." to a file named `output.txt` while displaying it in the terminal.

#### **Task 3: File and User Management**
- **Objective**: Manage files, permissions, and users.
- **Commands**: `locate`, `find`, `chmod`, `chown`, `useradd`, `userdel`, `sudo`, `su`
- **Instructions**:
    1. Use `locate` to find a file named `passwd`.
    2. Use `find` to search for all `.txt` files in the `CommandChallenge` directory.
    3. Create a file named `permissions_test.txt` and set its permissions to `644` using `chmod`.
    4. Change the owner of `permissions_test.txt` to a different user using `chown`.
    5. Create a new user named `testuser` using `useradd`.
    6. Delete the user `testuser` using `userdel`.
    7. Practice using `sudo` and `su` commands to run administrative tasks.

#### **Task 4: System Monitoring and Management**
- **Objective**: Monitor system resources and manage services.
- **Commands**: `df`, `du`, `top`, `htop`, `ps`, `uname`, `hostname`, `time`, `systemctl`, `watch`, `jobs`, `kill`, `shutdown`
- **Instructions**:
    1. Use `df` to check the disk space usage of all mounted filesystems.
    2. Use `du` to display the disk usage of the `CommandChallenge` directory.
    3. Use `top` and `htop` to monitor system processes.
    4. Use `ps` to list all running processes.
    5. Use `uname -a` to display system information.
    6. Use `hostname` to show the system's hostname.
    7. Use `time` to measure the execution time of a simple command (e.g., `ls`).
    8. Use `systemctl` to start, stop, and check the status of a service.
    9. Use `watch` to monitor the output of a command (e.g., `df -h`) in real-time.
    10. Use `jobs` to list all jobs running in the background.
    11. Use `kill` to terminate a specific process.
    12. Schedule a system shutdown in one minute and then cancel it using `shutdown` and `shutdown -c`.

#### **Task 5: Networking**
- **Objective**: Explore basic networking tools and commands.
- **Commands**: `ping`, `wget`, `curl`, `scp`, `ifconfig`, `netstat`, `traceroute`, `nslookup`, `dig`
- **Instructions**:
    1. Use `ping` to check the connectivity to `google.com`.
    2. Use `wget` to download a file from the internet.
    3. Use `curl` to fetch and display the contents of a webpage.
    4. Use `scp` to securely copy a file to another machine.
    5. Use `ifconfig` to display network interfaces and their configurations.
    6. Use `netstat` to display network connections, routing tables, and interface statistics.
    7. Use `traceroute` to trace the path packets take to a specific destination.
    8. Use `nslookup` to query DNS servers for the IP address of a domain.
    9. Use `dig` to display DNS information, including record types.

#### **Task 6: Miscellaneous Commands**
- **Objective**: Learn additional useful commands.
- **Commands**: `history`, `man`, `echo`, `ln`, `alias`, `unalias`, `cal`
- **Instructions**:
    1. Use `history` to view your recent commands and re-execute one using `!<number>`.
    2. Use `man` to read the manual for the `grep` command.
    3. Use `echo` to print a message to the terminal and write it to a file.
    4. Create a symbolic link to a file using `ln -s`.
    5. Create an alias for a frequently used command and then remove it using `unalias`.
    6. Use `cal` to display the current month's calendar.

### **Submission:**
1. Create a text file named `CommandChallenge_Completion.txt` in the `CommandChallenge` directory.
2. Document the steps you took to complete each task.
3. Include any challenges you faced and how you overcame them.
4. Provide any relevant outputs or screenshots.

### **Note:**
This assignment is designed to help you practice and understand the various commands and their use cases. Feel free to experiment and explore further. Have fun, and happy learning!