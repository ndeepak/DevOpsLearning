## 1. [[find]] Command
The `find` command searches for files and directories within a specified directory hierarchy, offering numerous options to filter results.
### Syntax:
`find [path] [expression]`
### Common Options:

| **Option** | **Description**                                                                 |
| ---------- | ------------------------------------------------------------------------------- |
| `-name`    | Searches for files with a specific name (case-sensitive).                       |
| `-iname`   | Searches for files with a specific name (case-insensitive).                     |
| `-type`    | Specifies the type of file (e.g., `f` for files, `d` for directories).          |
| `-size`    | Searches for files of a specific size (e.g., `+1M` for files larger than 1 MB). |
| `-user`    | Searches for files owned by a specific user.                                    |
| `-exec`    | Executes a command on matching files.                                           |
| `-mtime`   | Finds files modified within a specific number of days.                          |
### Examples:
1. **Find files by name:**
    `find /home -name "example.txt"`
    Searches for `example.txt` in the `/home` directory.
    
2. **Find directories only:**
    `find /var -type d -name "logs"`
    
3. **Find files larger than 100 MB:**
    `find / -type f -size +100M`
    
4. **Find files and execute a command:**
    `find . -type f -name "*.log" -exec rm {} \;`
    
    Deletes all `.log` files in the current directory and subdirectories.

---
## 2. [[locate]] Command
The `locate` command is faster than `find` because it uses a pre-built database of file paths. The database is updated periodically with the `updatedb` command.
### Syntax:
`locate [options] [pattern]`
### Common Options:

| **Option** | **Description**                                                           |
| ---------- | ------------------------------------------------------------------------- |
| `-i`       | Makes the search case-insensitive.                                        |
| `-c`       | Displays the count of matching entries instead of the matches themselves. |
| `-n`       | Limits the number of results displayed.                                   |
### Examples:
1. **Locate a file by name:**
    `locate example.txt`
    Quickly finds all paths containing `example.txt`.
    
2. **Case-insensitive search:** 
    `locate -i example`
    
3. **Limit results to 5 entries:**
    `locate -n 5 example`
    
4. **Update the database manually:**
    `sudo updatedb`
    
---
## 3. [[grep]] Command
The `grep` command searches for specific patterns in files and displays matching lines. It is ideal for searching file contents rather than filenames.
### Syntax:
`grep [options] [pattern] [file]`
### Common Options:

| **Option**   | **Description**                                         |
| ------------ | ------------------------------------------------------- |
| `-i`         | Makes the search case-insensitive.                      |
| `-r` or `-R` | Searches recursively in directories.                    |
| `-v`         | Inverts the search, displaying lines that do not match. |
| `-n`         | Displays line numbers of matching lines.                |
| `-l`         | Displays only the filenames containing the match.       |
| `-c`         | Displays the count of matching lines in a file.         |
| -A 'num'     | After the line of matching lines in a file.             |
| -B 'num'     | Before the line of matching lines in a file.            |
| -C 'num'     | Between the line of matching lines in a file.           |
### Examples:
1. **Search for a word in a file:**
    `grep "error" logfile.txt`
    
2. **Case-insensitive search:**
    `grep -i "error" logfile.txt`
    
3. **Search recursively in a directory:**
    `grep -r "error" /var/log`
    
4. **Display line numbers:**
    `grep -n "error" logfile.txt`
    
5. **Count matches:**
    `grep -c "error" logfile.txt`
    
6. **Find lines not matching a pattern:**
    `grep -v "error" logfile.txt`

---
## When to Use Each Command:

| **Command** | **Use Case**                                                                                      |
| ----------- | ------------------------------------------------------------------------------------------------- |
| `find`      | When searching for files and directories based on attributes like name, size, type, or ownership. |
| `locate`    | For fast searches of files and directories when you know their name or partial name.              |
| `grep`      | To search for specific content or patterns inside files.                                          |

By combining these commands (`find` + `grep` or `locate` + `grep`), you can create powerful search workflows!