### **SED (Stream Editor) in Linux**
#### **Introduction**:
`sed` (Stream Editor) is a powerful, non-interactive text processing tool in Linux used for manipulating and transforming text from input streams (files or pipelines). It processes text on a line-by-line basis and is commonly used for searching, replacing, inserting, and deleting text. Unlike editors like `vi` or `nano`, `sed` is designed to execute operations automatically from a script or command line without user interaction.

---

### **Basic Syntax**:
`sed [options] 'command' file(s)`
- **options**: Additional flags that modify `sed` behavior (e.g., `-i` for in-place editing).
- **command**: The operation to be performed (like substitute, delete, insert, etc.).
- **file(s)**: The file(s) on which `sed` will operate.

---

### **Common SED Commands**:
1. **Substitute (s)**: The most commonly used `sed` command is `s`, which substitutes a pattern with a replacement.
    `sed 's/pattern/replacement/' file.txt`
    Example:    
    `sed 's/Linux/Unix/' file.txt`
    This will substitute the first occurrence of "Linux" with "Unix" on each line.
    - **Global Replacement**: By default, `sed` replaces only the first occurrence of the pattern on each line. To replace **all** occurrences, use the `g` flag:
        `sed 's/Linux/Unix/g' file.txt`
    - **Case-Insensitive Replacement**: To perform case-insensitive replacements, use the `I` flag:
        `sed 's/linux/Unix/I' file.txt`
        
2. **Delete (d)**: The `d` command deletes lines that match a pattern.
    `sed '/pattern/d' file.txt`
    Example:    
    `sed '/^$/d' file.txt`
    This deletes all empty lines (lines that start with `^` and end with `$`).
    
3. **Insert (i)**: The `i` command inserts a line of text before the matched line.
    `sed '/pattern/i\text to insert' file.txt`
    Example:
    `sed '/Linux/i\This line is added before Linux' file.txt`
    This will insert the text "This line is added before Linux" before every line that contains the word "Linux."
    
4. **Append (a)**: The `a` command appends a line after the matched line.
    `sed '/pattern/a\text to append' file.txt`
    Example:    
    `sed '/Linux/a\This line is added after Linux' file.txt`
    
5. **Change (c)**: The `c` command changes (replaces) the entire line with new text if the pattern matches.
    `sed '/pattern/c\new text' file.txt`
    Example:
    `sed '/Linux/c\This line has been replaced' file.txt`
    
6. **Print (p)**: The `p` command prints lines that match the pattern.
    `sed -n '/pattern/p' file.txt`    
    Example:
    `sed -n '/Linux/p' file.txt`
    This prints only the lines that contain "Linux." The `-n` option suppresses the default printing of each line, and `p` is used to print only matching lines.
    
7. **Line Addressing**: You can specify lines or ranges of lines to apply commands on:
    
```
sed '2d' file.txt       # Delete the 2nd line
sed '2,5d' file.txt     # Delete lines from 2 to 5
sed '1,/pattern/d' file.txt  # Delete from the 1st line to the line matching "pattern"
```
    

---

### **Useful Options**:

1. **In-place Editing (-i)**: By default, `sed` does not modify files directly. It prints the output to standard output (the terminal). The `-i` option allows you to edit files in place.
    `sed -i 's/old/new/g' file.txt`    
    - **Backup with `-i`**: You can create a backup of the original file before editing:
        `sed -i.bak 's/old/new/g' file.txt`
        This will create a backup file `file.txt.bak`.
2. **Quiet Mode (-n)**: Suppresses automatic line printing. Used with the `p` command to print only the matched lines.    
    `sed -n 'p' file.txt`
---

### **Examples of SED Operations**:
1. **Replacing Text Globally**:
    `sed 's/Linux/Unix/g' file.txt`    
    - This replaces all instances of "Linux" with "Unix" in each line.
2. **Deleting Lines Containing a Pattern**:    
    `sed '/error/d' log.txt`
    - Deletes all lines that contain the word "error."
3. **Replacing with Special Characters**: When using special characters like `/`, you can escape them with a backslash (`\`), or you can use a different delimiter, like `|`:
    `sed 's|/usr/local|/opt/local|g' file.txt`
    
4. **Multiple Commands**: Use the `-e` option to execute multiple commands in one `sed` invocation:
    `sed -e 's/Linux/Unix/' -e 's/Ubuntu/Debian/' file.txt`
    
5. **Range of Lines**: Replace a pattern within a specific range of lines:
    `sed '2,4s/Linux/Unix/' file.txt`
    
    - This replaces "Linux" with "Unix" only in lines 2 to 4.
6. **Replacing Only on a Specific Line**:
    `sed '3s/Linux/Unix/' file.txt`
    
    - This replaces "Linux" with "Unix" only on the 3rd line.
---

### **Advanced SED Features**:

1. **Pattern Buffers (Hold and Pattern Space)**:
    - `sed` uses a pattern space (a working area where it manipulates text) and a hold space (a secondary buffer to store intermediate data).
    - You can swap, append, or retrieve text from these spaces for more complex processing.
2. **Transform Command (y)**: The `y` command translates characters like `tr`:
    `sed 'y/abc/xyz/' file.txt`    
    - Replaces all occurrences of `a` with `x`, `b` with `y`, and `c` with `z`.
3. **Using Shell Variables in SED**: Shell variables can be used in `sed` with double quotes:
    `sed "s/$old/$new/g" file.txt`
    
4. **Using Regular Expressions**: You can leverage the power of **regular expressions** to match complex patterns:    
    `sed 's/[0-9]\{3\}-[0-9]\{2\}-[0-9]\{4\}/XXX-XX-XXXX/g' ssn.txt`
    - This replaces Social Security numbers (SSN format) with `XXX-XX-XXXX`.

---
### **Advantages of SED**:
1. **Efficient for Large Files**: `sed` processes text line-by-line, making it extremely efficient for large files.
    
2. **Non-Interactive**: All operations are scripted, making `sed` ideal for automating tasks or including in shell scripts.
    
3. **Stream Processing**: Since `sed` reads from the input stream, it can process piped data or files on the fly without the need for manual file editing.
---

### **Use Cases**:
- **Log file processing**: `sed` can filter, search, and modify log files on the fly.
- **Batch text replacements**: Quickly replace or transform text across multiple files.
- **Text formatting**: Extract, rearrange, and format text from input files for reports.
- **Automated scripting**: Include `sed` in shell scripts for system automation tasks.

---

### **Conclusion**:
`sed` is a versatile tool for text processing in Linux. Its ability to handle complex text manipulation tasks like search and replace, pattern matching, and text insertion/deletion makes it a valuable tool for system administrators, developers, and anyone dealing with text data.