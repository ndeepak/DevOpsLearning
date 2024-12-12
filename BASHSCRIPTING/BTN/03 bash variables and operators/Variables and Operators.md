#### **1. Variables in Bash**
- **Definition**:
    - Variables in Bash are used to store values (numbers, strings, commands, etc.).
    - Bash is an **untyped language**, so variables don't require explicit data types.
- **Assigning Values**:
    `name="Deepak" `
    `numbers=$(seq 1 5)`
- **Accessing Variables**: Use the `$` symbol to access the value.
```
echo $name         # Output: Deepak
echo $numbers      # Output: 1 2 3 4 5
```

---
#### **2. System Predefined and Environment Variables**
- **Common Environment Variables**:
    - `$HOME` - User's home directory.
    - `$PATH` - Directories Bash looks into to find commands.
    - `$USER` - Logged-in user.
    - `$SHELL` - Current shell.
- **Display All Environment Variables**:
    `printenv`    
- **Example**:    
    `echo $PATH   # Prints the PATH environment variable`
---
#### **3. Rules for Naming Variables**
1. Variable names should start with a **letter** or an **underscore (`_`)**.
2. Variable names can contain **letters, numbers, and underscores**.
3. Variable names are **case-sensitive**.
4. Avoid using reserved keywords (e.g., `if`, `while`, `do`).

**Valid Examples**:
```
my_variable="Hello"
_variable123="World"
```

**Invalid Examples**:
```
123variable="Error"   # Starts with a number
my-variable="Error"   # Contains a hyphen
```
---
#### **4. Data Types in Bash**
- Bash variables are **untyped**, meaning they are treated as strings unless explicitly used in arithmetic operations.
- Example:
```
number=42
echo $number        # Output: 42
```
---
#### **5. Arithmetic Operations in Bash**
- **Using `expr`**:
```
num1=123
num2=233
result=`expr $num1 + $num2`
echo $result         # Output: 356
```
- **Using `let`**:
```
let result=num1+num2
echo $result         # Output: 356
```
- **Using Double Parentheses**:
```
result=$((num1 + num2))
echo $result         # Output: 356
```
---
#### **6. Command Line Inputs to Variables**
- **Accessing Inputs**: Use `$1`, `$2`, ..., `$n` to access positional parameters.
```
echo $1  # First argument
echo $2  # Second argument
```
- **Example**:
	echo "First argument: $1" 
	echo "Second argument: $2" 
	echo "All arguments: $@"
    
    Run the script:
    `./hello.sh 1234 5678`
    **Output**:
    First argument: 1234
    Second argument: 5678 
    All arguments: 1234 5678`
---
#### **7. Output Concatenation**
- **Using Variable Expansion**:
```
NAME="Deepak"
echo "${NAME}ISHERO"   # Output: DeepakISHERO
```
---
#### **8. Sourcing vs. Executing Scripts**
- **Sourcing a Script**:
    - Use `source <filename>` or `. <filename>`.
    - Runs in the **current shell** and affects the current environment.
    `source myscript.sh`
    
- **Executing a Script**:
    - Run the script using `./<filename>`.
    - Runs in a **new shell** and does not affect the current environment.
    `./myscript.sh`
    
- **Example**:    
    `my_var="Hello from script"`
    **Sourcing**:    
    `source myscript.sh `
    `echo $my_var   # Output: Hello from script`
    **Executing**:    
    `./myscript.sh `
    `echo $my_var   # Output: (nothing, as it does not affect the current shell)`
---
#### **9. Summary**
- **Variables**:
    - Store and access data using `$variable`.
    - Follow naming conventions to avoid errors.
- **Arithmetic Operations**:
    - Use `expr`, `let`, or `$(( ))` for calculations.
- **Command Line Arguments**:
    - Use `$1`, `$2`, ..., `$n` to access inputs.
- **Output Concatenation**:
    - Expand variables using `${}` to concatenate strings.
- **Sourcing vs. Executing**:
    - Sourcing affects the current shell, while executing runs in a new shell.