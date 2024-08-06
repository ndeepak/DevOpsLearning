explore the `cut`, `diff`, and `tee` commands with explanations, codes, and examples.

### 1. `cut` Command

The `cut` command is used to extract specific sections from each line of a file or input data. It can be used to cut parts of a line by specifying a delimiter or fixed width.

#### Basic Syntax
`cut [OPTIONS] [FILE]`

#### Common Options

- `-d` : Specifies the delimiter (default is tab).
- `-f` : Specifies the fields to extract.
- `-c` : Specifies the character positions to extract.

#### Examples

**Example 1: Extracting Fields by Delimiter
```
# File: data.csv
Name,Age,Location
Alice,30,New York
Bob,25,Los Angeles
Charlie,28,Chicago

# Extract the first and second fields (Name and Age) from the CSV file
cut -d',' -f1,2 data.csv

# Output
Name,Age
Alice,30
Bob,25
Charlie,28

```

**Example 2: Extracting Characters
```
# File: data.txt
123-456-789
987-654-321

# Extract the first three characters from each line
cut -c1-3 data.txt

# Output
123
987

```

### 2. `diff` Command

The `diff` command compares two files line by line and displays the differences between them. It's commonly used for version control, configuration management, and more.

#### Basic Syntax
`diff [OPTIONS] file1 file2`

#### Common Options

- `-u` : Shows unified diff format.
- `-c` : Shows context diff format.
- `-i` : Ignores case differences in file contents.

#### Examples

**Example 1: Basic File Comparison
```
# File: file1.txt
Hello World
This is a file.

# File: file2.txt
Hello World
This is another file.

# Compare file1.txt and file2.txt
diff file1.txt file2.txt

# Output
2c2
< This is a file.
---
> This is another file.

```

**Example 2: Unified Diff Format
```
diff -u file1.txt file2.txt

# Output
--- file1.txt
+++ file2.txt
@@ -1,2 +1,2 @@
 Hello World
-This is a file.
+This is another file.

```

### 3. `tee` Command

The `tee` command reads from the standard input and writes to the standard output and one or more files. It's often used to capture the output of a command while still displaying it on the terminal.

#### Basic Syntax

`command | tee [OPTIONS] [FILE]`

#### Common Options

- `-a` : Appends the output to the file instead of overwriting it.

#### Examples

**Example 1: Basic Usage
```
# Capture the output of `ls` and write it to both the terminal and a file
ls | tee output.txt

# Output (displayed on terminal and written to output.txt)
file1.txt
file2.txt
file3.txt

```

**Example 2: Appending to a File
```
# Append the output of `date` to a file
date | tee -a output.txt

# Output (appended to output.txt)
Mon Aug  7 00:00:00 UTC 2024
```

These commands are powerful tools for text processing and data manipulation in Unix-like systems. They can be combined with other commands in pipelines to perform complex tasks efficiently.