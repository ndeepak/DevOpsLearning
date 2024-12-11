## **1. Introduction to I/O Redirection**
I/O Redirection is the process of changing the input or output of a command to/from a file or another command.
### **Types of Streams**
- **Standard Input (`stdin`)**: File descriptor `0`, receives input from the keyboard by default.
- **Standard Output (`stdout`)**: File descriptor `1`, sends output to the terminal by default.
- **Standard Error (`stderr`)**: File descriptor `2`, sends error messages to the terminal by default.
---
## **2. I/O Redirection Operators**
### **Redirect Output (`>`)**
- Redirects the standard output (`stdout`) to a file. Overwrites the file if it exists.
    `echo "hello world" > hello.txt`
    - **Creates or overwrites** `hello.txt` with the text "hello world".

### **Append Output (`>>`)**
- Appends the standard output (`stdout`) to a file. Does not overwrite the file.
    `echo "new line" >> hello.txt`
    - Adds "new line" to `hello.txt`.

### **Redirect Errors (`2>`)**
- Redirects the standard error (`stderr`) to a file.
    `cala 2> error.txt`
    - Redirects the error message from the invalid `cala` command to `error.txt`.

### **Redirect Both Output and Errors (`2>&1`)**
- Redirects both `stdout` and `stderr` to the same file or location.
    `cala > output.txt 2>&1`
    - Combines the standard output and error into `output.txt`.

---

## **3. Practical Examples**
### **Standard Output (`stdout`)**
- **Print text to the terminal**:
    `echo "hello" `
    `echo "hello world"`
    **Output**:
    `hello `
    `hello world`
- **Redirect `stdout` to a file**:
    `echo "hello world" > hello.txt `
    `cat hello.txt`
    **Output**:
    `hello world`
- **Append to a file**:
    `echo "new line" >> hello.txt`
    `cat hello.txt`

    **Output**:    
    ```
    hello world 
    new line
	``` 
---
### **Standard Error (`stderr`)**
- **Redirect an error to a file**:    
    `cala 2> error.txt `
    `cat error.txt`
    **Output**:    
    `bash: cala: command not found`
    
- **Combine `stdout` and `stderr`**:
    `cala > all_output.txt 2>&1 `
    `cat all_output.txt`
    **Output**:    
    `bash: cala: command not found`
---
### **Combining Standard Input, Output, and Error**
- **Using `cal` to save output to a file**:
    `cal > calendar.txt `
    `cat calendar.txt`
    **Output**:
```
   December 2024
Su Mo Tu We Th Fr Sa
1  2  3  4  5  6  7
8  9 10 11 12 13 14
15 16 17 18 19 20 21
22 23 24 25 26 27 28
29 30 31
```
---
## **4. Python and I/O Redirection**
Python can also utilize I/O redirection via shell commands or within scripts.
### **Python Example**
```
# Save this script as io_example.py
print("This is standard output")
raise ValueError("This is an error")
```

### **Usage in Terminal**
- Redirect `stdout` to a file:
    `python io_example.py > output.txt`
- Redirect `stderr` to a file:
    `python io_example.py 2> error.txt`
- Combine `stdout` and `stderr`:
    `python io_example.py > all_output.txt 2>&1`

---
## **5. Summary of Commands**

|Command|Description|Example|Output|
|---|---|---|---|
|`>`|Redirects stdout to a file, overwriting existing content|`echo "data" > file.txt`|Writes "data" to `file.txt`|
|`>>`|Appends stdout to a file|`echo "data" >> file.txt`|Appends "data" to `file.txt`|
|`2>`|Redirects stderr to a file|`cala 2> error.txt`|Writes errors to `error.txt`|
|`2>&1`|Redirects stdout and stderr to the same file|`cala > all.txt 2>&1`|Combines output and errors into `all.txt`|

This comprehensive note covers all basics and practical use cases of I/O redirection, along with Python examples and their integration with redirection operations.