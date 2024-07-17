### Setting Up SSL for GitLab with a Self-Signed Certificate
This guide provides step-by-step instructions for generating a self-signed SSL certificate and configuring GitLab to use it.
#### Step 1: Generate Root CA Key and Certificate
1. **Generate the Root CA Key:**
    `openssl genrsa -out ca.key 4096`
    
2. **Generate the Root CA Certificate:**
    `openssl req -x509 -new -nodes -key ca.key -sha256 -days 365 -out ca.crt -subj '/CN=ndeepak.gitlab.com'`
#### Step 2: Create Certificate Signing Request (CSR)
1. **Generate the CSR and Private Key:**
    `openssl req -new -nodes -out ndeepak.gitlab.com.csr -newkey rsa:4096 -keyout ndeepak.gitlab.com.key -subj '/CN=ndeepak.gitlab.com'`
#### Step 3: Create Certificate Configuration File
1. **Create the Configuration File:**
```
cat > run.extfile << EOF
basicConstraints=critical,CA:TRUE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = ndeepak.gitlab.com
EOF
```
#### Step 4: Generate GitLab Certificate
1. **Generate the Certificate:**
    `openssl x509 -req -in ndeepak.gitlab.com.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out ndeepak.gitlab.com.crt -days 365 -sha256 -extfile run.extfile`
#### Step 5: Configure GitLab with SSL
1. **Update GitLab Configuration:**    
```
echo "external_url 'https://ndeepak.gitlab.com'" >> /etc/gitlab/gitlab.rb
echo "nginx['redirect_http_to_https'] = true" >> /etc/gitlab/gitlab.rb
echo "letsencrypt['enable'] = false" >> /etc/gitlab/gitlab.rb
```

2. **Copy Certificates and Reconfigure GitLab:**
```
mkdir -p /etc/gitlab/ssl
chmod 755 /etc/gitlab/ssl
cp -f ndeepak.gitlab.com.{key,crt} /etc/gitlab/ssl/
gitlab-ctl reconfigure
```
#### Step 6: Verify SSL Configuration
1. **Use OpenSSL to Verify the Certificate Setup:**
    `openssl s_client -showcerts -verify 3 -connect ndeepak.gitlab.com:443`
### Summary
By following these steps, you will have created and configured a self-signed SSL certificate for your GitLab instance with the URL `https://ndeepak.gitlab.com`. This setup ensures secure communication between users and your GitLab server.