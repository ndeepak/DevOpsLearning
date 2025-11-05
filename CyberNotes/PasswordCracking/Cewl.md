### **CeWL (Custom Word List Generator)**

CeWL is a Ruby-based tool used to generate custom wordlists by spidering a target website. It’s often used for password cracking or conducting dictionary attacks using a list of words derived from the content of a website. It is especially useful for penetration testers and cybersecurity professionals.

---
## ✅ **Installation of CeWL**
CeWL is pre-installed on Kali Linux. However, on other Linux distributions, you can install it using:
`sudo apt update sudo apt install cewl`
To verify the installation:
`cewl --help`

---
## ✅ **Basic Syntax of CeWL**
`cewl [options] <URL>`
- `<URL>`: Target website to crawl.
- `[options]`: Various flags to customize the behavior.
---
## ✅ **Common Options in CeWL**

| Option                | Description                               | Example                         |
| --------------------- | ----------------------------------------- | ------------------------------- |
| `-d`                  | Depth to crawl.                           | `-d 3` (3 levels deep)          |
| `-m`                  | Minimum word length to include.           | `-m 5` (Minimum 5 characters)   |
| `-w <filename>`       | Save output to a file.                    | `-w words.txt`                  |
| `-u <user-agent>`     | Use a custom User-Agent string.           | `-u "Mozilla/5.0"`              |
| `-c`                  | Include email addresses in output.        | `-c`                            |
| `-v`                  | Enable verbose mode.                      | `-v`                            |
| `-e`                  | Include words from metadata of files.     | `-e`                            |
| `-o <filename>`       | Save the extracted metadata to a file.    | `-o metadata.txt`               |
| `--auth <user:pass>`  | Perform Basic Authentication if required. | `--auth admin:password`         |
| `--proxy <host:port>` | Use a proxy for requests.                 | `--proxy http://127.0.0.1:8080` |

---
## ✅ **Examples of Using CeWL**
### 📌 **1. Generate a Wordlist from a Website**
`cewl http://example.com -w example_wordlist.txt`
- Crawls `http://example.com` and saves the wordlist to `example_wordlist.txt`.
---
### 📌 **2. Set a Specific Depth for Crawling**
`cewl http://example.com -d 2 -w wordlist.txt`
- Crawls 2 levels deep into the website.
---
### 📌 **3. Generate Words of a Specific Length**
`cewl http://example.com -m 8 -w wordlist.txt`
- Extracts words with a minimum of 8 characters.  
---
### 📌 **4. Extract Email Addresses**
`cewl http://example.com -c -w emails.txt`
- Extracts emails and saves them to `emails.txt`.
---
### 📌 **5. Extract Metadata from Documents**
`cewl http://example.com -e -o metadata.txt`
- Collects words from metadata in documents and saves them to `metadata.txt`.
---
### 📌 **6. Use Custom User-Agent**
`cewl http://example.com -u "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -w wordlist.txt`
- Spoofs the User-Agent as a common browser to avoid detection.

---
### 📌 **7. Perform Basic Authentication**
`cewl http://example.com --auth user:password -w wordlist.txt`
- Uses authentication credentials to access protected content.
---
### 📌 **8. Use Proxy for Crawling**
`cewl http://example.com --proxy http://127.0.0.1:8080 -w wordlist.txt`
- Uses a proxy (e.g., Burp Suite) for traffic monitoring.
---
## ✅ **Use Case Scenario**
### 🔎 **Scenario: Password Cracking**
1. Generate a wordlist using CeWL:    
    `cewl http://targetsite.com -w target_wordlist.txt`
2. Use a password cracking tool like **John the Ripper** or **Hashcat** with the generated wordlist:   
    `john --wordlist=target_wordlist.txt hashfile`
---
## ✅ **Additional Tips**
- Combine CeWL-generated wordlists with other tools like `crunch` to enhance the attack surface.
- Always test the generated wordlist against multiple targets to improve results.
- Use verbose mode (`-v`) to troubleshoot or monitor progress.
---
## ✅ **Legal and Ethical Considerations**
- Only use CeWL for authorized testing or ethical hacking purposes.    
- Always obtain permission before scanning a website.    
- Avoid generating unnecessary load on the target server.