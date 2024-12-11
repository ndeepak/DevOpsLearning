# Bash Shell and Command Line Essentials

## Introduction to Bash
- **Bash** is a Unix shell and command language written by **Brian Fox** for the GNU Project as a free software replacement for the Bourne Shell.
- A **shell program** is typically an executable binary that interprets and executes the commands typed by the user.
- Bash typically runs in a **text-based terminal**, where users can execute commands to perform various tasks.
- Most modern Linux and Unix distributions provide a **Bash shell** by default.

---

## Terminal
- A **terminal** is a piece of equipment or software interface through which you interact with a computer.
- Modern terminals are software representations of old physical terminals, often integrated into GUI environments.
- The terminal transmits user commands to the shell for processing.

---

## Shell
- The **shell** is a command interpreter whose primary purpose is to run other programs.
- It converts user commands into a format understandable by the **kernel** and passes them for execution.
- The **terminal** passes typed commands to the shell, which processes and instructs the kernel.

---

## Features of Bash
1. **Compatibility**:
    - Bash is **sh-compatible** and incorporates features from **Korn Shell (ksh)** and **C Shell (csh)** like directory manipulation, job control, and aliases.
2. **Command Line Options**:
    - Supports **single-character** options: `-a`, `-b`, `-c`, etc.
    - Also supports **multi-character** options: `--help`, `--login`, etc.
3. **Startup Files**:    
    - Bash reads and executes **startup scripts** during initialization:
        - `~/.bashrc`, `~/.bash_profile`, and `~/.profile`.
4. **Key Bindings**:
    - Allows **customized key sequences** for editing commands.
5. **Arrays**:
    - Bash supports **one-dimensional arrays** for referencing and manipulating lists of data.
6. **Control Structures**:
    - Includes structures like `select`, used for menu generation.
7. **Directory Stack**:
    - Tracks recently visited directories:
        - `pushd`: Add directory to stack.
        - `popd`: Remove directory from stack.
        - `dirs`: Display stack contents.
8. **Restricted Mode**:
    - For enhanced security, Bash operates in **restricted mode** with options like `bash --restricted` or the alias `rbash`.

---

## Setting Up Bash Scripting Environment
1. **Install Git Bash**:
    - Download from [git-scm.com](https://git-scm.com/).
2. **Install Ubuntu**:
    - Download and set up Ubuntu to access Bash natively.

---
## Understanding the Prompt
The command prompt specifies the **user**, **host**, and **current working directory**:
`user@hostname:~$`

- **user**: The current logged-in user.
- **hostname**: The machine's name.
- `~`: Represents the home directory.

---

## Command Line Basics
### System Information Commands
1. `hostname`: Display the system hostname.
2. `pwd`: Print the current working directory.
3. `echo $HOME`: Print the path to the home directory.
4. `echo $SHELL`: Display the current shell in use.
5. `echo $PATH`: Show the system's PATH environment variable.

### Directory and File Management
1. `ls`, `ls -a`, `ls -la`: List directory contents.
2. `mkdir dir1 dir2`: Create directories.
3. `touch file1.txt`: Create empty files.
4. `rm file1.txt`: Delete files.
5. `rm -rf dir1`: Remove directories recursively.

### Searching Files and Paths
1. `find / -name filename`: Search for files.
2. `locate filename`: Find files quickly using a database.

### Viewing and Editing Files
1. `cat file1.txt`: View file contents.
2. `nano`, `vi`, `vim`: Edit files interactively.

### System Utilities
1. `df -h`: Check disk usage.
2. `lsblk`: List block devices.
3. `free -h`: Display memory usage.

### Date and Time
1. `date`: Show current date and time.
2. `date +%d/%m/%Y`: Custom date format.
3. `timedatectl`: Manage system time settings.
4. `timedatectl set-timezone "Asia/Kathmandu"`: Set timezone.

### Process Management
1. `ps -aux`: List running processes.
2. `kill -9 PID`: Terminate a process by PID.
3. `jobs`: List background jobs.
4. `fg`: Bring a background job to the foreground.

### History and Help

1. `history`: View command history.
2. `!!`: Re-run the last command.
3. `whatis command`: Brief description of a command.
4. `tldr command`: Simplified manual pages.
5. `man command`: Full manual for a command.

---
## Additional Notes

- Use `apt` for package management:
    - `apt install package`: Install a package.
    - `apt remove package`: Uninstall a package.
- Manage user privileges with `sudo` and `su` commands.
- Explore startup files (`~/.bashrc`, `~/.profile`) to customize your environment.