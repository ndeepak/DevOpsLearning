### **Exit Status in Bash**
#### **1. Overview**
In Bash, every command executed returns an **exit status**, also known as the **return code** or **exit code**. The exit status is a numeric value that indicates whether a command was successful or encountered an error. It plays a crucial role in scripting and command execution, as it allows you to control the flow of the script based on the success or failure of commands.
- **Exit Status Value:**
    - **0**: The command was successful.
    - **Non-Zero**: The command encountered an error. Different non-zero values can indicate different types of errors.

#### **2. Checking Exit Status**
The exit status of the last executed command can be accessed using the special variable `$?`.
**Example:**
```
#!/bin/bash

# Run a command
ls /home/user/

# Check the exit status of the last command
if [ $? -eq 0 ]; then
    echo "The command was successful."
else
    echo "The command failed."
fi
```

**Explanation:**
- The script checks the exit status of the `ls /home/user/` command. If the exit status is `0`, it prints a success message; otherwise, it prints a failure message.

#### **3. Setting an Exit Status in a Script**
You can explicitly set the exit status of a script using the `exit` command followed by a numeric value.
**Example:**
```
#!/bin/bash

# Some operations
echo "Processing..."

# Set an explicit exit status
if [ some_condition ]; then
    echo "Success"
    exit 0
else
    echo "Error: Something went wrong."
    exit 1
fi
```

**Explanation:**
- The script uses the `exit` command to set the exit status based on the outcome of some operations. `exit 0` indicates success, while `exit 1` indicates an error.

#### **4. Using Exit Status in Conditional Statements**
Exit statuses are often used in conditional statements to determine the flow of a script.
**Example:**
```
#!/bin/bash

# Run a command
mkdir /protected_directory

# Use exit status in a conditional statement
if [ $? -ne 0 ]; then
    echo "Failed to create directory. Check permissions."
    exit 1
else
    echo "Directory created successfully."
fi
```
**Explanation:**
- The script attempts to create a directory. If the `mkdir` command fails (e.g., due to lack of permissions), the script exits with a status of `1` after printing an error message.

#### **5. Common Exit Status Codes**
Here are some commonly used exit status codes:

| **Exit Code** | **Meaning**                    | Example      |
| ------------- | ------------------------------ | ------------ |
| 0             | Success                        | pwd          |
| 1             | General error                  | cal=$((1/0)) |
| 2             | Misuse of shell built-ins      | fun(){}      |
| 126           | Command invoked cannot execute | /dev/null    |
| 127           | Command not found              | LD           |
| 128           | Invalid argument to `exit`     |              |
| 130           | Script terminated by Ctrl+C    |              |
```
                       │
root@ubuntumachine:~/LearnBash/ExitStatus# LD                       │
LD: command not found                                               │
root@ubuntumachine:~/LearnBash/ExitStatus# echo $?                  │
127                                                                 │
root@ubuntumachine:~/LearnBash/ExitStatus# fun() {}                 │
-bash: syntax error near unexpected token `{}'                      │
root@ubuntumachine:~/LearnBash/ExitStatus# echo $?                  │
2                                                                   │
root@ubuntumachine:~/LearnBash/ExitStatus# /dev/null                │
-bash: /dev/null: Permission denied                                 │
root@ubuntumachine:~/LearnBash/ExitStatus# echo $?                  │
126                                           

```
#### **6. Practical Use Case: Exit Status in Automation**
In automation scripts, exit statuses are crucial for error handling and decision-making.
**Example:**
```
#!/bin/bash

# Update system packages
sudo apt-get update
if [ $? -ne 0 ]; then
    echo "Update failed. Exiting..."
    exit 1
fi

# Install a package
sudo apt-get install -y vim
if [ $? -eq 0 ]; then
    echo "Vim installed successfully."
else
    echo "Failed to install Vim. Exiting..."
    exit 1
fi
```

**Explanation:**
- The script first updates the system packages. If the update fails, the script exits with an error status. If successful, it proceeds to install Vim, checking the exit status again.
---
### **Conclusion**
Exit statuses in Bash provide a mechanism to understand the outcome of commands and control the flow of scripts accordingly. By checking and using exit statuses, you can create more robust and reliable scripts that handle errors gracefully and execute tasks conditionally based on success or failure.