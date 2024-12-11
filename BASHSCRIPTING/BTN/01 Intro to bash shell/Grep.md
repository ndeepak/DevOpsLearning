The `grep` command is a powerful text search tool in Linux that allows you to search for specific patterns within files. It supports regular expressions for complex searches and offers numerous options for advanced filtering and matching.

---
### **Command References**
1. **Manual and Help Options**
    - **Display the manual for `grep`:**
        `man grep`
        
    - **List all available options:**
        `grep --help`
---
### **Basic Usage**
1. **Search for a string in a file:**
    `grep ERROR books.txt`
    Finds lines containing the word `ERROR` in the file `books.txt`.
    
2. **Case-insensitive search:**
    `grep -i Alchemist books.txt`
    Matches `Alchemist`, `alchemist`, or any case variation.
    
3. **Inverse search (exclude matches):**
    - Exclude lines containing `Alchemist`:
        `grep -v Alchemist books.txt`
    - Exclude case-insensitively:    
        `grep -iv Alchemist books.txt`
        
4. **Search for multiple patterns:**
    `grep -e Alchemist -e Martin books.txt`
    Matches either `Alchemist` or `Martin`.
    
5. **Count matching lines:**
    `grep -c Alchemist books.txt`
    Displays the number of lines containing `Alchemist`.
    
6. **Display line numbers:**
    `grep -n alchemist books.txt`
    Shows the line numbers where matches occur.
    

---

### **Contextual Search**
1. **Print 2 lines below the match:**
    `grep -A 2 alchemist books.txt`
    
2. **Print 2 lines above the match:**
    `grep -B 2 alchemist books.txt`
    
3. **Print 2 lines before and after the match:**
    `grep -C 2 alchemist books.txt`

---
### **Regular Expressions**
#### **Basic Patterns**
1. **Search for `f.n` (matches `fan`, but not `faan`):**
    `grep "f.n" regex.txt`
    **Example Content:**
    ```
    fan 
    lan 
    tan 
    faan
    ```
    **Output:**
    `fan`
    
2. **Lines starting with `c`:**
    `grep "^c" regex.txt`
    
3. **Lines ending with `n`:**
    `grep "n$" regex.txt`

---
#### **Extended Regular Expressions (ERE)**
1. **Match `cat` with one or more occurrences of `t`:**
    `grep -E "cat+" regex.txt`
    Matches `cat`, `catt`, `cattt`.
    
2. **Match `cat` with zero or more occurrences of `t`:**
    `grep -E "cat*" regex.txt`
    
    Matches `cat`, `catt`, `cattt`, and `ca`.
    
3. **Match `cat` with zero or one occurrence of `t`:**
    `grep -E "cat?" regex.txt`
    Matches `cat` and `ca`.
    
4. **Match lines starting with uppercase letters:**
    `grep -E "^[A-Z]" regex.txt`
    
5. **Match lines containing digits:**
    `grep -E "[0-9]" regex.txt`
    
6. **Match lines ending with digits:** 
    `grep -E "[0-9]*$" regex.txt`
    
7. **Match either `accept` or `accent`:**
    `grep -E "acce[np]t" regex.txt`

---
### **Practical Examples**
**File Content:**
```
cat
fat
mat
fan
catt
cattt
123
222
344
color
colour
```
1. **Search for `cat+`:**
    `grep -E "cat+" regex.txt`
    **Output:**
    `cat catt cattt`
    
2. **Search for lines containing numbers:**
    `grep -E "[0-9]" regex.txt`
    **Output:**
    `123 222 344`
    
3. **Search for `accept` or `accent`:**
    `grep -E "acce[np]t" regex.txt`
    

---

### Summary Table

|**Command**|**Description**|
|---|---|
|`grep ERROR books.txt`|Search for `ERROR` in `books.txt`.|
|`grep -i Alchemist books.txt`|Case-insensitive search for `Alchemist`.|
|`grep -v Alchemist books.txt`|Exclude lines containing `Alchemist`.|
|`grep -c Alchemist books.txt`|Count lines containing `Alchemist`.|
|`grep -n alchemist books.txt`|Display line numbers of matches.|
|`grep -A 2 alchemist books.txt`|Print 2 lines below matches.|
|`grep -B 2 alchemist books.txt`|Print 2 lines above matches.|
|`grep -E "cat+" regex.txt`|Match `cat` with one or more `t`.|
|`grep -E "^[A-Z]" regex.txt`|Match lines starting with uppercase letters.|
|`grep -E "[0-9]" regex.txt`|Match lines containing numbers.|

These commands and their variations make `grep` an indispensable tool for text processing and pattern matching.