### **If-Else Conditions in Bash (Conditional Statements)**
#### **1. Overview of If-Else Conditions**
If-else conditions in Bash are used to make decisions within scripts. These conditional statements allow the script to execute different blocks of code based on whether a given condition is true or false. The basic structure of an if-else statement in Bash is similar to other programming languages but uses specific Bash syntax.

##### **Basic Syntax:**
```
if [ condition ]; then
    # Code to execute if the condition is true
elif [ another_condition ]; then
    # Code to execute if the another_condition is true
else
    # Code to execute if none of the above conditions are true
fi
```

- **`if`**: Starts the conditional block.
- **`[` condition `]`**: The condition to be evaluated (also written as `[[ condition ]]`).
- **`then`**: If the condition is true, the code following `then` is executed.
- **`elif`**: (Optional) Checks another condition if the previous one was false.
- **`else`**: (Optional) Executes code if none of the conditions are true.
- **`fi`**: Ends the conditional block.
---
#### **2. Mathematical Comparisons**
Bash allows you to perform mathematical comparisons within if-else statements. These comparisons are commonly used to evaluate numeric expressions.
##### **Comparison Operators:**

| **Operator** | **Description**          |
| ------------ | ------------------------ |
| `-eq`        | Equal to                 |
| `-ne`        | Not equal to             |
| `-gt`        | Greater than             |
| `-lt`        | Less than                |
| `-ge`        | Greater than or equal to |
| `-le`        | Less than or equal to    |

##### **Example:**
```
#!/bin/bash

num1=10
num2=20

if [ $num1 -gt $num2 ]; then
    echo "$num1 is greater than $num2"
elif [ $num1 -lt $num2 ]; then
    echo "$num1 is less than $num2"
else
    echo "$num1 is equal to $num2"
fi
```

**Explanation:**
- The script compares two numbers, `num1` and `num2`, and prints the appropriate message based on their relationship.
---
#### **3. String Comparisons**
String comparisons are used to compare two strings in Bash. These comparisons can check if strings are equal, not equal, or if one string is lexicographically greater or smaller than the other.
##### **Comparison Operators:**

| **Operator** | **Description**                      |
| ------------ | ------------------------------------ |
| `=`          | Equal to (strings match)             |
| `!=`         | Not equal to (strings don't match)   |
| `<`          | Less than (lexicographical order)    |
| `>`          | Greater than (lexicographical order) |
| `-z`         | String is null (zero length)         |
| `-n`         | String is not null (non-zero length) |

##### **Example:**
```
#!/bin/bash

str1="apple"
str2="orange"

if [ "$str1" = "$str2" ]; then
    echo "Strings are equal"
elif [ "$str1" \< "$str2" ]; then
    echo "$str1 is less than $str2"
else
    echo "$str1 is greater than $str2"
fi
```

**Explanation:**
- The script compares two strings, `str1` and `str2`, and prints the appropriate message based on their lexicographical order.
---
#### **4. File Conditions**
Bash also provides conditions to check the status of files. These conditions can check if a file exists, is readable, writable, executable, or if it is a directory.
##### **File Test Operators:**

| **Operator** | **Description**                      |
| ------------ | ------------------------------------ |
| `-e`         | File exists                          |
| `-f`         | File exists and is a regular file    |
| `-d`         | File is a directory                  |
| `-r`         | File is readable                     |
| `-w`         | File is writable                     |
| `-x`         | File is executable                   |
| `-s`         | File is not empty                    |
| `!`          | Negates the condition (NOT operator) |

##### **Example:**
```
#!/bin/bash

file="/path/to/file.txt"

if [ -e "$file" ]; then
    if [ -r "$file" ]; then
        echo "File exists and is readable"
    else
        echo "File exists but is not readable"
    fi
else
    echo "File does not exist"
fi
```
**Explanation:**
- The script checks if a file exists and then checks if it is readable. It prints messages based on these conditions.
---
### **5. Practical Examples**
#### **Mathematical Comparison:**
```
#!/bin/bash

age=25

if [ $age -ge 18 ]; then
    echo "You are an adult."
else
    echo "You are a minor."
fi
```

**Explanation:**
- The script checks if the `age` variable is greater than or equal to 18. If true, it prints "You are an adult," otherwise "You are a minor."

#### **String Comparison:**
```
#!/bin/bash

user_input="yes"

if [ "$user_input" = "yes" ]; then
    echo "You agreed!"
else
    echo "You did not agree."
fi
```

**Explanation:**
- The script compares the user input with the string "yes". If they match, it prints "You agreed!"
#### **File Condition:**
```
#!/bin/bash

logfile="/var/log/syslog"

if [ -f "$logfile" ]; then
    echo "Log file exists."
    if [ -s "$logfile" ]; then
        echo "Log file is not empty."
    else
        echo "Log file is empty."
    fi
else
    echo "Log file does not exist."
fi
```
**Explanation:**
- The script checks if the `logfile` exists and whether it is empty or not, printing appropriate messages.
---
### **Conclusion**
Conditional statements in Bash provide powerful tools for controlling the flow of scripts based on various conditions. Whether you're performing mathematical comparisons, comparing strings, or checking file statuses, mastering if-else statements enables you to write more dynamic and robust scripts.

---

