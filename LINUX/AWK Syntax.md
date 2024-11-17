### **AWK Syntax**
The basic syntax of the `awk` command in Linux is as follows:
`awk 'pattern { action }' input-file`
- **pattern**: Defines the condition or filter to apply to each record (row).
- **action**: Specifies what to do if the pattern matches (e.g., print, calculate).
- **input-file**: The file to be processed by AWK.

If no **pattern** is provided, AWK will execute the **action** for every record in the file.

### **Detailed Syntax Breakdown**:
1. **Field Manipulation**:
    - `$n` refers to the nth field (column) in the input record (row).
    - `NR` is the built-in variable for the current record number (row).
    - `NF` is the built-in variable for the number of fields (columns) in the current record.
2. **Typical Example**:
    `awk '{print $1, $3}' input-file.txt`
	`awk '{print} file.txt'` to print as it is.
    - Prints the first and third columns of every row in the file.
3. **With a Pattern**:    
    `awk '$3 > 100 {print $1, $2}' input-file.txt`
    - Prints the first and second columns of rows where the third column is greater than 100.
4. **Performing Arithmetic**:
    `awk '{sum = $2 + $3; print sum}' input-file.txt`
    - Adds the second and third columns and prints the sum for each row.
5. **Pattern Matching**:
    `awk '/error/ {print $0}' log-file.txt`
    - Prints lines containing the word "error".
6. **Using Field Separator**:
    `awk -F "," '{print $1, $2}' file.csv`
    - The `-F` option sets the field separator to a comma for CSV files.
7. **BEGIN and END Blocks**:
    - **BEGIN** block: Actions performed before reading the input.
    - **END** block: Actions performed after processing all records.
    Example:
    `awk 'BEGIN {print "Processing..."} {print $1} END {print "Done."}' input-file.txt`
    - Prints "Processing..." before processing records, prints the first field of each row, and "Done." after processing all rows.

### **Full Example**:
`awk 'BEGIN { FS=","; OFS=" | " } $3 > 50 { print $1, $2, $3 } END { print "Completed." }' data.csv`
- **FS=","**: Sets the field separator to a comma.
- **OFS=" | "**: Sets the output field separator to `|`.
- **$3 > 50**: Processes records where the third column is greater than 50.
- **{ print $1, $2, $3 }**: Prints the first, second, and third fields.
- **BEGIN** and **END** blocks are used to initialize and finalize actions.