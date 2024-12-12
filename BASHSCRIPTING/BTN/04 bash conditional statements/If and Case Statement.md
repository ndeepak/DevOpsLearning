###  Notes on `if` and `if-else` Statements in Bash**
---
#### **1. Conditional Statements in Bash**
Conditional statements allow scripts to make decisions and execute different sets of commands based on the outcome of a condition.
- **Conditions**:
    - Expressions that evaluate to **true** or **false**.
    - Based on the result, the script takes different actions.
---
#### **2. Basic Syntax**
```
if [ condition ]; then
    # commands to execute if the condition is true
fi
```

- The condition is enclosed in square brackets `[ ]`.
- Commands after `then` are executed only if the condition evaluates to true.
---
#### **3. Example: Single `if` Condition**
```
#!/bin/bash
echo "Enter your password:"
read pass

if [ $pass == "secret" ]; then
    echo "Login Successful"
fi
```

**Explanation**:
- The script prompts the user for a password.
- If the entered password matches `"secret"`, the script prints `"Login Successful"`.

---
#### **4. `if-else` Statement**
```
if [ condition ]; then
    # commands if condition is true
else
    # commands if condition is false
fi
```

**Example**:
```
#!/bin/bash
echo "Enter your password:"
read pass

if [ $pass == "secret" ]; then
    echo "Login Successful"
else
    echo "Login Failed"
fi
```

**Explanation**:
- If the password matches `"secret"`, the script prints `"Login Successful"`.
- Otherwise, it prints `"Login Failed"`.

---

#### **5. `if-elif-else` Statement**
```
if [ condition1 ]; then
    # commands if condition1 is true
elif [ condition2 ]; then
    # commands if condition2 is true
else
    # commands if none of the conditions are true
fi
```

**Example**:
```
#!/bin/bash
echo "Please enter a number:"
read num

if [ $num -gt 0 ]; then
    echo "$num is positive"
elif [ $num -lt 0 ]; then
    echo "$num is negative"
else
    echo "$num is zero"
fi
```

**Explanation**:
- The script checks if the number is positive, negative, or zero.
- Executes the appropriate block based on the condition.

---

#### **6. Logical Operators**
Logical operators allow combining multiple conditions:
- **AND (`-a`)**: Both conditions must be true.
- **OR (`-o`)**: At least one condition must be true.

**Example**:
```
if [ $a -gt 60 -a $b -lt 100 ]; then
    echo "Both conditions are true"
fi
```

---

#### **7. Comparison Operators**
- **Numeric Comparisons**:
    - `-eq`: Equal to
    - `-ne`: Not equal to
    - `-gt`: Greater than
    - `-lt`: Less than
    - `-ge`: Greater than or equal to
    - `-le`: Less than or equal to
- **String Comparisons**:
    - `==`: Strings are equal
    - `!=`: Strings are not equal
    - `-z`: String is null/empty
    - `-n`: String is not null/empty
---
#### **8. Nested `if` Statements**
```
if [ condition1 ]; then
    if [ condition2 ]; then
        # commands if both conditions are true
    fi
fi
```

**Example**:
```
if [ $age -ge 18 ]; then
    if [ $age -lt 60 ]; then
        echo "Eligible for voting"
    fi
fi
```

---

#### **9. Advanced Examples**
- **Age Validation**:
```
#!/bin/bash
echo "Enter your age:"
read age

if [ $age -lt 18 ]; then
    echo "Underage"
elif [ $age -le 60 ]; then
    echo "Age Valid"
else
    echo "Senior Citizen"
fi
```
    
- **Range Check with AND Operator**:
```
if [ $int -le 100 ] && [ $int -gt 90 ]; then
    echo "Age Valid"
else
    echo "Age Non-Valid"
fi
```
---
#### **10. Return Status and Exit Codes**
- Every command in Bash returns an **exit status**:
    - `0`: Successful execution.
    - Non-zero: Error occurred.
**Example**:
```
#!/bin/bash
name=$(whoami)
if [ $? -eq 0 ]; then
    echo "Command executed successfully"
else
    echo "Command failed"
fi
```
---
#### **Summary Table**

| **Type**          | **Syntax**                                            | **Use Case**                                |
| ----------------- | ----------------------------------------------------- | ------------------------------------------- |
| `if`              | `if [ condition ]; then commands fi`                  | Executes commands if the condition is true. |
| `if-else`         | `if [ condition ]; then commands else commands fi`    | Provides an alternative action if false.    |
| `if-elif-else`    | `if [ cond1 ]; then elif [ cond2 ]; else commands fi` | Handles multiple conditions.                |
| Logical Operators | `[ cond1 -a cond2 ]` or `[ cond1 -o cond2 ]`          | Combine multiple conditions.                |


---
### **Notes on `case` Statements in Bash**
---
#### **1. What Are `case` Statements?**
`case` statements in Bash are used to match an input expression against a list of patterns and execute the corresponding block of code for the first matching pattern.

---
#### **2. Syntax of a `case` Statement**
```
case expression in
    pattern1)
        # commands to execute if expression matches pattern1
        ;;
    pattern2)
        # commands to execute if expression matches pattern2
        ;;
    *)
        # commands to execute if no pattern matches
        ;;
esac
```

- **`expression`**: The value being evaluated.
- **`pattern1`, `pattern2`, etc.**: Patterns to compare against.
- **`*`**: The default case, executed when no pattern matches.
- **`;;`**: Terminates each block of code for a pattern.

---
#### **3. Example: Fruit Identification**
```
#!/bin/bash
fruit="apple"

case $fruit in
    "apple")
        echo "This is a red fruit."
        ;;
    "banana")
        echo "This is a yellow fruit."
        ;;
    "orange")
        echo "This is an orange fruit."
        ;;
    *)
        echo "Unknown fruit."
        ;;
esac
```
**Explanation**:
- If `fruit="apple"`, the script matches the `"apple"` pattern and outputs `"This is a red fruit."`.
- If the value of `fruit` does not match any of the specified patterns, the `*` pattern outputs `"Unknown fruit."`.

---
#### **4. Use Cases for `case` Statements**
- Menu-based scripting.
- Checking input values.
- Executing commands based on system states or parameters.

---
#### **5. Example: Menu Selection**
```
#!/bin/bash

echo "Choose an option:"
echo "1. Display date"
echo "2. Display uptime"
echo "3. Exit"
read choice

case $choice in
    1)
        echo "Current date and time: $(date)"
        ;;
    2)
        echo "System uptime: $(uptime)"
        ;;
    3)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid option!"
        ;;
esac
```

**Explanation**:
- Users select an option by entering a number.
- The script matches the input and executes the corresponding block.
- If an invalid option is entered, the `*` case outputs `"Invalid option!"`.

---
#### **6. Patterns in `case` Statements**
- **Exact Matches**:
    - Patterns can be exact strings, like `"apple"`.
- **Multiple Patterns**:
    - Combine patterns using the `|` operator.
    - Example:
```
case $color in
    "red"|"blue"|"green")
        echo "Primary color."
        ;;
    *)
        echo "Unknown color."
        ;;
esac
```
        
- **Wildcard Matches**:
    - Use `*` to match any value.
    - Example:
```
case $file in
    *.txt)
        echo "This is a text file."
        ;;
    *.jpg|*.png)
        echo "This is an image file."
        ;;
    *)
        echo "Unknown file type."
        ;;
esac
```
---
#### **7. Advanced Example: File Type Detection**
```
#!/bin/bash

echo "Enter the file name:"
read file

case $file in
    *.txt)
        echo "This is a text file."
        ;;
    *.jpg|*.png)
        echo "This is an image file."
        ;;
    *.sh)
        echo "This is a shell script."
        ;;
    *)
        echo "Unknown file type."
        ;;
esac
```

**Explanation**:
- Matches the file extension to determine its type.
- Patterns like `*.txt` or `*.jpg|*.png` match specific file types.
- The default case handles files with unknown extensions.

---
#### **8. Nested `case` Statements**
`case` statements can be nested for more complex logic:
```
case $os in
    "Linux")
        case $distro in
            "Ubuntu")
                echo "You are using Ubuntu on Linux."
                ;;
            "CentOS")
                echo "You are using CentOS on Linux."
                ;;
            *)
                echo "Unknown Linux distribution."
                ;;
        esac
        ;;
    "Windows")
        echo "You are using Windows."
        ;;
    *)
        echo "Unknown operating system."
        ;;
esac
```

---
#### **9. Advantages of `case` Over `if-else`**

|Feature|`case` Statement|`if-else` Statement|
|---|---|---|
|Readability|Easier to read and maintain for multi-pattern cases.|Becomes complex with multiple conditions.|
|Pattern Matching|Supports wildcard (`*`, `?`) and multiple patterns.|Limited to logical and arithmetic comparisons.|
|Efficiency|Stops after the first match.|Evaluates all conditions in sequence.|

---

#### **10. Summary Table**

|**Keyword**|**Description**|
|---|---|
|`case`|Starts the `case` statement.|
|`expression`|The value to be matched.|
|`pattern`|A specific value or wildcard to match against the expression.|
|`;;`|Ends the block of code for each pattern.|
|`*`|The default pattern, executed if no other pattern matches.|
|`esac`|Ends the `case` statement.|

