Setting up a **Certificate Authority (CA)** involves generating a root certificate, signing certificates for clients or servers, and managing trust. Here’s a step-by-step guide to setting up your own **CA** using OpenSSL.

---
## **1️⃣ Generate a Root Certificate Authority (CA)**
### Step 1: Create a Private Key for the CA
`openssl genrsa -aes256 -out rootCA.key 4096`
🔹 This creates a 4096-bit encrypted private key for your CA.

### Step 2: Generate a Root Certificate
`openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 3650 -out rootCA.crt`
🔹 This generates a **self-signed root certificate** valid for **10 years**.

---
## **2️⃣ Create & Sign a Server Certificate with the CA**
### Step 3: Generate a Private Key for the Server
`openssl genrsa -out server.key 2048`
### Step 4: Create a Certificate Signing Request (CSR)
`openssl req -new -key server.key -out server.csr`
### Step 5: Sign the CSR with the Root CA
`openssl x509 -req -in server.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out server.crt -days 365 -sha256`
🔹 This signs the server certificate using the CA.

---
## **3️⃣ Install & Trust the CA Certificate**
For Linux:
`cp rootCA.crt /etc/pki/ca-trust/source/anchors/ 
`update-ca-trust`
For Windows:  
🔹 Import `rootCA.crt` into **Trusted Root Certificate Authorities**.
For macOS:  
🔹 Use **Keychain Access** to trust `rootCA.crt`.

---
## **4️⃣ Verify the Certificate**
`openssl x509 -in server.crt -text -noout`
🔹 This displays certificate details.
`openssl verify -CAfile rootCA.crt server.crt`
🔹 This verifies that the certificate is signed by your CA.

---
