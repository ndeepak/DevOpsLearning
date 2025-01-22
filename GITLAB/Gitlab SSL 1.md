# Complete Guide to Securing GitLab with Custom SSL Certificates

In today’s connected world, security is paramount, especially when dealing with sensitive code repositories. Using HTTPS for your GitLab server ensures encrypted communication between your browser (or Git client) and the server, preventing data interception. This guide explains how to configure GitLab with a custom SSL certificate, including a detailed breakdown of _what_ we are doing and _why_ each step matters.

---

## **Why HTTPS and SSL?**

**HTTP** (HyperText Transfer Protocol) is the standard protocol for web communication. However, it is insecure, transmitting data in plain text. **HTTPS** (HTTP Secure) uses **SSL/TLS** (Secure Sockets Layer / Transport Layer Security) to encrypt data, making it unreadable to eavesdroppers. This is critical for repositories containing sensitive code or credentials.

---

### **Step 1: Generate an SSL Certificate and Key**

### **What We Are Doing**

We’re creating a custom SSL certificate, which is a digital file that authenticates our server’s identity and enables encrypted communication. SSL certificates consist of a **private key** and a **public certificate**. The private key encrypts data, and the public certificate allows users to decrypt it.

### **Why This Step Is Important**

Without an SSL certificate, any data sent between your GitLab server and clients could be intercepted by attackers. A custom certificate allows us to avoid security warnings typically seen with self-signed certificates.

#### **1.1 Create a Directory for SSL Files**
`mkdir ssl  && cd ssl/`  

We’re creating a dedicated folder to keep SSL-related files organized.

#### **1.2 Create an SSL Configuration File**

We’ll use a configuration file to automate the certificate generation process with **OpenSSL**.

**Configuration: `sslcert.conf`**
```
[req]  
distinguished_name = req_distinguished_name  
x509_extensions = v3_req  
prompt = no  

[req_distinguished_name]  
C = NP  
ST = Bagmati  
L = Kathmandu  
O = DevOps Solutions  
OU = Engineering  
CN = ndeepak.gitlab.com  

[v3_req]  
keyUsage = keyEncipherment, dataEncipherment  
extendedKeyUsage = serverAuth, clientAuth  
subjectAltName = @alt_names  

[alt_names]  
DNS.1 = ndeepak.gitlab.com  
DNS.2 = runner.gitlab.com  
```

#### **Explanation**

- **req** and **req_distinguished_name**: These are sections required for generating certificates.
- **CN (Common Name)**: The domain name for the server (`ndeepak.gitlab.com`).
- **subjectAltName**: Specifies additional DNS names. This allows the certificate to be valid for multiple domains.
- **keyUsage and extendedKeyUsage**: Define how the certificate can be used (e.g., for server authentication).

---

#### **1.3 Generate the SSL Certificate and Key**

We use `openssl` to create a self-signed certificate:
`openssl req -x509 -nodes -days 730 -newkey rsa:2048 -keyout ndeepak.gitlab.com.key -out ndeepak.gitlab.com.crt -config sslcert.conf -extensions 'v3_req'`  

**Explanation of Options**:

- `-x509`: Creates a self-signed certificate.
- `-nodes`: Prevents encryption of the private key (for simplicity).
- `-days 730`: Sets the validity of the certificate to 2 years.
- `-newkey rsa:2048`: Generates a new 2048-bit RSA key pair.
- `-keyout` and `-out`: Specify the output filenames for the key and certificate.
- `-config sslcert.conf`: Uses the custom configuration file for input.

---

### **Step 2: Configure GitLab to Use HTTPS**

#### **What We Are Doing**

We’ll modify the GitLab configuration file (`gitlab.rb`) to enable HTTPS, specifying our custom domain.

#### **Why This Step Is Important**

Without this configuration, GitLab will continue using HTTP, leaving your communication vulnerable.
`sudo nano /etc/gitlab/gitlab.rb`  

Update the `external_url` line to:
`external_url 'https://ndeepak.gitlab.com'`  

**Explanation**:  
The `external_url` setting tells GitLab how to construct URLs for links and redirects. Changing it to HTTPS ensures that all traffic to your GitLab server is encrypted.

---

### **Step 3: Place SSL Files in the Correct Directory**

#### **What We Are Doing**

GitLab expects SSL files in `/etc/gitlab/ssl`. We’ll create this directory and copy our certificate and key into it.

#### **Why This Step Is Important**

Storing SSL files in the correct location allows GitLab to access them when serving HTTPS traffic.
```
sudo mkdir -p /etc/gitlab/ssl  
sudo chmod 755 /etc/gitlab/ssl  
sudo cp ndeepak.gitlab.com.key ndeepak.gitlab.com.crt /etc/gitlab/ssl/  
```

**Explanation of Commands**:

- `mkdir -p`: Creates the directory and any necessary parent directories.
- `chmod 755`: Sets permissions so that GitLab can read the files.
- `cp`: Copies the SSL files to the appropriate location.

---

### **Step 4: Reconfigure GitLab**

#### **What We Are Doing**

We’ll apply our configuration changes with the `gitlab-ctl reconfigure` command.

#### **Why This Step Is Important**

This step regenerates GitLab’s configuration files and restarts necessary services to apply our changes.
`sudo gitlab-ctl reconfigure`  

---

### **Step 5: Verify the SSL Configuration**

#### **What We Are Doing**

We’ll check the SSL connection using `openssl`.
`openssl s_client -connect ndeepak.gitlab.com:443`  

#### **Why This Step Is Important**

This command tests the SSL handshake and displays certificate details, confirming that HTTPS is working as expected.

---

### **Step 6: Access GitLab Over HTTPS**
Open a web browser and navigate to:  
[https://ndeepak.gitlab.com/users/sign_in](https://ndeepak.gitlab.com/users/sign_in)

---

## **Conclusion**

Securing your GitLab server with a custom SSL certificate is a crucial step in protecting sensitive data. By following these steps, you ensure encrypted communication, providing safety and trust for your development environment.

This guide not only helps configure SSL but also explains the _why_ behind each step, empowering you to make informed security decisions in your DevOps practices.