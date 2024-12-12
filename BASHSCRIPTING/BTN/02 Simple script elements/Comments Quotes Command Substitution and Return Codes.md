 #### **1. Comments in Bash**
- Comments are used to include explanations or notes within the script and are ignored during execution.
**Single-line Comment**:
`# This is a single-line comment `
`echo "Hello, World!"  # Inline comment`
**Multi-line Comments**: Using a **Here Document**:
```
<<COMMENTS
This is a multi-line comment.
It can span multiple lines.
COMMENTS
```

Using `: '` for multi-line comments:
```
: '
This is a
multi-line comment
using a colon and single quotes.
'
```

---

#### **2. Quotes in Bash**
Quotes define how special characters within strings are interpreted.
- **Single Quotes (`'`)**:
    - Treat everything literally; no variable expansion or special character interpretation.
```
name='Deepak'
echo 'Hello $name'  # Output: Hello $name
```
    
- **Double Quotes (`"`)**:
    
    - Allow variable expansion and interpretation of special characters like `$`.
```
name="Deepak"
echo "Hello $name"  # Output: Hello Deepak
```
---
#### **3. Command Substitution**
Command substitution allows the output of a command to be used as a variable or as part of another command.
- Syntax:
    `variable=$(command)`
    
- Example:
    `current_date=$(date) `
    `echo "Today's date is $current_date"`

    **Output**:
    `Today's date is Sun Dec 11 14:25:39 UTC 2024`  

---
#### **4. Variables in Bash**
Variables are used to store data that can be referenced and manipulated.
- **Declaring a Variable**:
    `name="Deepak"`
    
- **Accessing Variables**:
    `echo $name  # Output: Deepak`
    
- **Reading Input into a Variable**:    
```
echo "Enter your name:"
read name
echo "Hello $name"
```
---
#### **5. Return Status and Exit Codes**
- **Return Status**:
    - Every command in Bash returns a status code (exit code).
    - `0` indicates success, and any non-zero value indicates failure.
- **Using `exit` to Set Exit Codes**:
    `exit 0  # Exits with a success status`
    
- **Example Script**:
```
#!/bin/bash
name=$(whoami)  # Command substitution
echo "Current user: $name"
exit $?
echo $?  # Prints the exit code of the previous command
```

**Explanation**:
1. `$(whoami)` captures the output of the `whoami` command.
2. `exit $?` exits with the status of the last executed command.
3. `$?` holds the exit status of the most recent command.

---
#### **6. Difference Between Single Quotes and Double Quotes**

|Feature|Single Quotes (`'`)|Double Quotes (`"`)|
|---|---|---|
|Variable Expansion|Not Supported|Supported|
|Command Substitution|Not Supported|Supported|
|Special Characters (`$ \`)|Treated Literally|Interpreted|

**Examples**:
```
greeting='Hello $USER'
echo $greeting   # Output: Hello $USER (literal)

greeting="Hello $USER"
echo $greeting   # Output: Hello deepak (interpreted)
```

---
#### **Summary**
This guide covers essential Bash scripting concepts including comments, quotes, variables, command substitution, and exit codes. Understanding these basics is crucial for writing efficient scripts.