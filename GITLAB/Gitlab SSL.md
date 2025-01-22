# Securing GitLab with Custom SSL Certificates
When deploying a GitLab server in a production environment, enabling secure HTTPS communication is essential to protect sensitive data. This step-by-step guide will walk you through generating SSL certificates, configuring GitLab for HTTPS, and verifying the setup.

### Prerequisites
- A Linux-based server running GitLab
- OpenSSL installed for certificate generation
- sudo privileges for configuration changes

---

## Step 1: Generate an SSL Certificate Key Pair
We start by creating a custom SSL certificate for the fully qualified domain name (FQDN) of our GitLab server.

### Create a Directory for SSL Files
```
gitadmin@ndeepak:~$ mkdir ssl  
gitadmin@ndeepak:~$ cd ssl/  
```

### Create an SSL Configuration File
Name the configuration file `sslcert.conf` with the following content:
```
[req]  
distinguished_name = req_distinguished_name  
x509_extensions = v3_req  
prompt = no  

[req_distinguished_name]  
C = NP  
ST = Bagmati  
L = Kathmandu  
O = Ndeepak Corp  
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

### Generate the SSL Certificate and Key
Run the following command to create the `.crt` and `.key` files:
```
gitadmin@ndeepak:~/ssl$ openssl req -x509 -nodes -days 730 -newkey rsa:2048 -keyout ndeepak.gitlab.com.key -out ndeepak.gitlab.com.crt -config sslcert.conf -extensions 'v3_req'
```
The generated files will appear in the `ssl` directory.

---

## Step 2: Update the GitLab Configuration
We need to configure GitLab to use HTTPS by updating the `gitlab.rb` file.

### Modify `gitlab.rb`
Open the configuration file and set the external URL to HTTPS:
`gitadmin@ndeepak:~$ sudo nano /etc/gitlab/gitlab.rb`  

Locate and update:
`external_url 'https://ndeepak.gitlab.com'`  

---

## Step 3: Copy SSL Files to the GitLab Directory
GitLab expects SSL certificates in `/etc/gitlab/ssl`.
```
gitadmin@ndeepak:~/ssl$ sudo mkdir -p /etc/gitlab/ssl  
gitadmin@ndeepak:~/ssl$ sudo chmod 755 /etc/gitlab/ssl  
gitadmin@ndeepak:~/ssl$ sudo cp ndeepak.gitlab.com.key ndeepak.gitlab.com.crt /etc/gitlab/ssl/  
```

---

## Step 4: Reconfigure GitLab
Apply the changes with the reconfigure command:
`gitadmin@ndeepak:~$ sudo gitlab-ctl reconfigure`  

---

## Step 5: Validate the SSL Setup
Check if the GitLab server is accessible over HTTPS using `openssl`:
`gitadmin@ndeepak:~$ openssl s_client -connect ndeepak.gitlab.com:443`  

The output should display certificate details, confirming the setup.

---

### Access the GitLab Web Interface
Open a browser and navigate to:  
[https://ndeepak.gitlab.com/users/sign_in](https://ndeepak.gitlab.com/users/sign_in)

---

**Conclusion**  
Setting up a custom SSL certificate enhances the security of your GitLab server, ensuring encrypted communication and protecting sensitive data. Following these steps, you can confidently deploy GitLab in a secure, production-ready configuration.

Happy coding and secure hosting!