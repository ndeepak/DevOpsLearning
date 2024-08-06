### **Introduction to `awk` and `sed` Commands**

Both `awk` and `sed` are powerful command-line utilities in Unix/Linux systems used for text processing and manipulation. They allow you to search, filter, and transform text data efficiently.

### **`awk` Command**

`awk` is a versatile programming language primarily used for pattern scanning and processing. It processes each line of a file, breaks it into fields, and allows various actions to be performed on these fields.

#### **Basic Syntax**

`awk 'pattern { action }' filename`

#### **Examples**

1. **Print All Lines
    `awk '{ print }' file.txt`
    
    This prints every line in the file.
    
2. **Print Specific Columns
    `awk '{ print $1, $3 }' file.txt`
    
    This prints the first and third columns of each line.
    
3. **Print Lines Matching a Pattern
    `awk '/pattern/ { print }' file.txt`
    
    This prints lines containing the specified pattern.
    
4. **Compute and Print Column Sums
    `awk '{ sum += $1 } END { print sum }' numbers.txt`
    
    This calculates and prints the sum of all numbers in the first column.
    
5. **Field Separator
    `awk -F: '{ print $1 }' /etc/passwd`
    
    This prints the first field (username) of each line in `/etc/passwd`, using `:` as the field separator.
    

#### **Use Case**

- **Log Analysis:** Extract specific fields from server logs for monitoring and analysis.

### **`sed` Command**

`sed` (stream editor) is a command-line utility that parses and transforms text using a simple, compact programming language. It can perform basic text transformations on an input stream (a file or input from a pipeline).

#### **Basic Syntax
`sed 's/pattern/replacement/' filename`

#### **Examples**

1. **Substitute Text**
    `sed 's/old/new/' file.txt`
    
    This replaces the first occurrence of "old" with "new" in each line.
    
2. **Global Substitution**
    `sed 's/old/new/g' file.txt`
    
    This replaces all occurrences of "old" with "new" in each line.
    
3. **Delete Lines Matching a Pattern
    `sed '/pattern/d' file.txt`
    
    This deletes lines containing the specified pattern.
    
4. **Print Lines
    `sed -n '2,5p' file.txt`
    
    This prints lines from the second to the fifth line.
    
5. **Insert Text Before a Line
    `sed '2i\Insert this line before line 2' file.txt`
    
    This inserts the specified text before the second line.
    

#### **Use Case**

- **Text Substitution:** Automating the replacement of text patterns in configuration files or scripts.

### **Combining `awk` and `sed`**

You can use `awk` and `sed` together in a pipeline to perform complex text processing tasks. For example, you can use `awk` to filter specific lines and `sed` to modify the content of those lines:
`awk '/pattern/' file.txt | sed 's/old/new/g'`

This command first filters lines containing "pattern" using `awk` and then replaces "old" with "new" in those lines using `sed`.