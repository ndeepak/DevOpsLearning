### Tool Documentation: **[[crunch]]**
**Overview:**
**Crunch** is a versatile wordlist generator tool that allows you to generate custom wordlists for use in penetration testing, password cracking, or any scenario requiring a list of potential combinations of characters. You can specify the minimum and maximum lengths of words, and customize the character sets used to generate the wordlist. Crunch works by combining and permuting a specified set of characters to create the list.

---
### **Installation on Ubuntu:**
To install **Crunch** on Ubuntu, follow these steps:
`sudo apt update && sudo apt install crunch`
**Installed Size:** 83 KB

---
### **Crunch Usage Example:**
**Goal**: Generate a dictionary file containing words of exactly 6 characters long using the given characters (0123456789abcdef), and save the output to a file called `6chars.txt`.
**Command**:
`root@kali:~# crunch 6 6 0123456789abcdef -o 6chars.txt`

#### Breakdown of the command:
- `6`: Minimum length of the word to be generated.
- `6`: Maximum length of the word to be generated.
- `0123456789abcdef`: The set of characters to be used to generate the words (in this case, hexadecimal characters).
- `-o 6chars.txt`: Specifies the output file where the generated wordlist will be saved.

---
### **Crunch Output:**
When the command is run, the following output will be generated:
```
crunch version 3.6

Crunch can create a wordlist based on criteria you specify.  The output from crunch can be sent to the screen, file, or to another program.

Usage: crunch <min> <max> [options]
where min and max are numbers

Please refer to the man page for instructions and examples on how to use crunch.
```
- **Data Generated**: 117,440,512 bytes (~112 MB).
- **Lines Generated**: 16,777,216 possible combinations of 6 characters.

---
### **Key Options and Parameters for Crunch**:
Here’s a list of important options you can use with **crunch**:
- `-o <filename>`: Specifies the output file to save the generated wordlist.
- `-h`: Displays the help information for **crunch**.
- `<min> <max>`: The minimum and maximum length of the words to generate.
- `-t <pattern>`: Use a specific pattern for the wordlist. For example, `-t @@@%` would generate words where `@` represents a lowercase letter and `%` represents a number.
- `-p`: Permutes the words in the wordlist (useful for rearranging already created wordlists).
- `-i`: Use an input file containing a list of characters to generate words.
#### Example: Generate a wordlist with a custom pattern
`root@kali:~# crunch 5 5 -o custom_pattern.txt -t @@%%%`
This generates words of exactly 5 characters using two lowercase letters (`@`) followed by three numbers (`%`).

---
### **Use Cases for Crunch:**
Crunch is useful in a variety of scenarios, including:
1. **Password Cracking**:    
    - Generating wordlists based on custom character sets for use in brute-force attacks against password hashes.
    - For example, creating wordlists for possible combinations of lowercase letters, uppercase letters, numbers, and symbols.
2. **Penetration Testing**:    
    - Generating wordlists to test the security of various services like SSH, HTTP basic authentication, or any service that relies on user credentials.
3. **Testing Systems**:    
    - Creating wordlists to simulate possible credentials for testing the robustness of authentication systems in a safe, controlled environment.
4. **Custom Wordlists**:    
    - When default wordlists (like RockYou) are insufficient or too large, **crunch** allows you to create smaller, more targeted wordlists.

---

### **Crunch Help Command**:
If you're ever unsure about how to use **crunch**, you can access the built-in help command:
`root@kali:~# crunch -h`
Output:
```
crunch version 3.6

Crunch can create a wordlist based on criteria you specify.  The output from crunch can be sent to the screen, file, or to another program.

Usage: crunch <min> <max> [options]
where min and max are numbers

Please refer to the man page for instructions and examples on how to use crunch.
```

This will show you the full usage options and provide more detailed instructions.

---
### **Crunch Example Use Cases**:
1. **Generate a wordlist of length 6 containing only lowercase letters**:
`root@kali:~# crunch 6 6 abcdefghijklmnopqrstuvwxyz -o lowercase_6chars.txt`
2. **Generate a wordlist of length 8-10 using a mix of uppercase letters and numbers**:
`root@kali:~# crunch 8 10 A1B2C3D4 -o mixed_8_10chars.txt`
3. **Generate a wordlist using a pattern of letters followed by digits**:
`root@kali:~# crunch 6 6 -t @@%% -o letter_digit_patterns.txt`
This command will generate words with 2 letters (`@`) followed by 2 digits (`%`), such as `ab01`, `zz99`, etc.

---
### **Dependencies:**
- **crunch** requires no additional dependencies for its basic functionality. However, depending on the usage context (e.g., using the generated wordlist in a password-cracking tool), you may need additional tools (like **hashcat** or **John the Ripper**) to perform cracking operations.

---
### **Conclusion:**
**Crunch** is a powerful and flexible tool for generating wordlists based on custom patterns and character sets. Whether you're preparing wordlists for penetration testing or generating potential password combinations for security assessments, **crunch** provides the necessary functionality with ease and efficiency.