# [[Cracking ZIP]] Passwords with John the Ripper and fcrackzip
This guide provides detailed steps and examples for cracking password-protected ZIP files using **John the Ripper** and **fcrackzip**, two popular tools for password recovery.

---
## 1. Using John the Ripper
### Step 1: Extract the ZIP Hash
Before using John the Ripper, you must extract the hash from the ZIP file.
#### Example ZIP File
File: `example.zip`

#### Extracting the Hash
1. Use `zip2john` to generate the hash:
    ```
    zip2john example.zip > example_hash.txt
    ```
2. View the extracted hash:
    ```
    cat example_hash.txt
    ```
    Example output:
    ```
    example.zip:$pkzip$2*1*1*0*8*24*...*$/pkzip$::example.zip
    ```
    The hash will vary based on the ZIP file.
### Step 2: Crack the Hash
Use a wordlist to attempt cracking the password.
#### Example with rockyou.txt
1. Run John the Ripper with a wordlist:
    ```
    john --wordlist=rockyou.txt example_hash.txt
    ```
2. To check progress or see if the password is found:
    ```
    john --show example_hash.txt
    ```
### Common Issues and Solutions
- **No password hashes loaded:** Ensure the hash is properly formatted. Use `tr -cd '[:print:]'` to clean up non-printable characters:
    ```
    cat example_hash.txt | tr -cd '[:print:]' > cleaned_hash.txt
    john --wordlist=rockyou.txt cleaned_hash.txt
    ```
---
## 2. Using fcrackzip
### Step 1: Running fcrackzip
fcrackzip is a command-line tool designed specifically for ZIP files.
#### Example Command
1. Basic usage with a wordlist (e.g., `rockyou.txt`):
    ```
    fcrackzip -D -p rockyou.txt -u example.zip
    ```
    Explanation:
    - `-D`: Use a dictionary-based attack.
    - `-p rockyou.txt`: Specify the path to the wordlist.
    - `-u`: Test each file in the archive to validate the password.
#### Output Example
```
PASSWORD FOUND!!!!: pw == mysecretpassword
```
### Step 2: Brute Force (Optional)
If a wordlist attack fails, you can try brute force.
#### Example Brute Force Attack
1. Use `fcrackzip` with brute force mode:
    ```
    fcrackzip -b -c a -l 1-8 example.zip
    ```
    Explanation:
    - `-b`: Brute force mode.
    - `-c a`: Use lowercase letters.        
    - `-l 1-8`: Limit the password length from 1 to 8 characters.

---
## Additional Tips
### Cleaning the ZIP Hash for John the Ripper
To avoid unnecessary file-level hashes when extracting from ZIP files with multiple contents:
- Filter the `zip2john` output to only get the main hash:
    ```
    grep 'example.zip:' hash_output.txt > main_hash.txt
    ```
### Using Alternative Tools
- **7z2hashcat**: Use if you prefer cracking ZIP passwords with `hashcat`.
### Important Considerations
- **Complex passwords**: May require advanced dictionaries or hybrid attacks.
- **Wordlists**: Use comprehensive lists like `rockyou.txt` or custom ones based on password patterns.
    

---

## Creating Password-Protected ZIP Files
### Using `zip`
```
zip -e protected.zip file1.txt file2.txt
```
- The `-e` option enables encryption.
- You will be prompted to enter a password.
### Using `7z`
```
7z a -pPasswordHere -mhe=on protected.7z file1.txt file2.txt
```
- `-pPasswordHere`: Sets the password.
- `-mhe=on`: Encrypts file headers for additional security.

---
## Verifying ZIP File Contents
```
unzip -l protected.zip
```
To test without extracting:
`unzip -t protected.zip`