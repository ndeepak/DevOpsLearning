# SSH and all


# SSH: A Deep-Dive from Fundamentals to Advanced Port Forwarding

To understand SSH properly, it helps to build the concepts in layers:

1. Networking basics (IP, TCP)
2. What Telnet is
3. Why SSH was invented
4. How SSH works internally
5. Authentication (passwords, keys)
6. Public/private keys
7. Cryptography used in SSH
8. SSH tunnels and port forwarding
9. Real-world use cases
10. Security best practices

---

# 1. First: What is SSH?

SSH stands for:

**Secure Shell**
It is a protocol used to securely communicate with another computer over a network.

Before SSH existed, administrators used:
- Telnet
- rlogin
- rsh

The problem:
Everything was sent in plaintext.

Example:
```
Username: adminPassword: Secret123
```

Anyone sniffing the network could see the password.
### Core idea
SSH replaces insecure protocols (like Telnet) by providing:

- **Confidentiality** → encryption
- **Integrity** → data is not modified in transit
- **Authentication** → verify identities (client & server)

SSH solves this by:
- Encrypting communication
- Verifying identity
- Protecting integrity

SSH usually runs on:
```
TCP Port 22
```

---

# 2. Understanding TCP Before SSH
SSH runs on top of TCP.
### TCP (Transmission Control Protocol)

- A **transport layer protocol**
- Guarantees:
    - reliable delivery
    - ordered packets
    - error correction

SSH runs **on top of TCP**.

### How SSH uses TCP

- Default port: **22**
- SSH creates a **secure encrypted tunnel inside a TCP connection**

Think:
```scss
Application Layer
      SSH
       |
Transport Layer
      TCP
       |
Network Layer
      IP
```

When you run:

```
ssh user@10.10.10.5
```

SSH does not directly send packets.

Instead:

```scss
SSH
 ↓
TCP
 ↓
IP
 ↓
Ethernet
```

---

## What TCP Does

TCP provides:

### Reliable Delivery

If packet 3 is lost:

```scss
1
2
3 (lost)
4
5
```

TCP retransmits packet 3.

---

### Ordered Delivery

Data arrives in order:

```
HELLO
```

Not:

```
HLEOL
```

---

### Connection-Oriented

TCP first performs:

```
Three-way handshake
```

```scss
Client -> SYN
Server -> SYN-ACK
Client -> ACK
```

Connection established.

Only then SSH begins.

---

# 3. Telnet vs SSH

## Telnet

Default port:

```
23
```

Example:

```
telnet 192.168.1.10
```

Traffic:

```scss
username
password
commands
```

all plaintext.

Sniffer output:

```
adminPassword123
```

visible.

---

## SSH

Example:

```
ssh admin@192.168.1.10
```

Traffic:

```
Encrypted
```

Sniffer sees:

```
A7 F1 3B C9 29 ...
```

Unreadable.

---

## Comparison

| Feature             | Telnet               | SSH                |
| ------------------- | -------------------- | ------------------ |
| Encryption          | No                   | Yes                |
| Password Protection | No                   | Yes                |
| File Transfer       | No                   | Yes                |
| Tunneling           | No                   | Yes                |
| Integrity Check     | No                   | Yes                |
| Modern Use          | Rare                 | Standard           |
| Port                | 23                   | 22                 |
| Authentication      | Plaintext (Password) | Password/Key-based |
| Usage               | Mostly Outdated      | Modern Systems     |

---

# 4. What Happens During an SSH Connection?

Suppose:

```
ssh deep@server
```

Several steps occur.

---

## Step 1: TCP Connection

Client connects:

```
Client -> Server:22
```

TCP handshake completes.

---

## Step 2: Protocol Negotiation

Client:

```
SSH-2.0-OpenSSH_9.6
```

Server:

```
SSH-2.0-OpenSSH_8.9
```

They agree on:

- Encryption
- hashing algorithm
- Key exchange
- MAC algorithm

---

## Step 3: Key Exchange

Both sides generate a shared secret.

Usually:

```
Diffie-Hellman
```

or

```
ECDH
```

This shared secret becomes the session key.

---

## Step 4: Host Verification

Server proves:

```
"I am the real server."
```

using its host key.

Example:

```
/etc/ssh/ssh_host_rsa_key
```

Client stores fingerprint:

```
~/.ssh/known_hosts
```

---

## Step 5: Authentication

You prove your identity.

Using:

- Password
- Public Key
- Certificate

---

## Step 6: Encrypted Session

Commands:

```scss
ls
cat
pwd
```

travel through encrypted tunnel.

---

# 5. Symmetric vs Asymmetric Encryption

SSH uses both.

---

## Symmetric Encryption

Same key:

```scss
Encrypt
Decrypt
```

Example:

```scss
AES
ChaCha20
```

Fast.

Used for session traffic.

---

## Asymmetric Encryption

Two keys:

```scss
Private Key
Public Key
```

Used for:

- Authentication
- Key exchange

Examples:

```scss
RSA
ECDSA
Ed25519
```

---

# 6. Public and Private Keys

Imagine:

```scss
private key = master key
public key = lock
```

Anyone can have your lock.

Only you have the master key.

---

## Generate Keys

```
ssh-keygen
```

Creates:

```scss
~/.ssh/id_rsa
~/.ssh/id_rsa.pub
```

or

```
id_ed25519
id_ed25519.pub
```

---

## Private Key

```
id_ed25519
```

Keep secret.

Never share.

Example:

```
-----BEGIN OPENSSH PRIVATE KEY-----...
```

---

## Public Key

```
id_ed25519.pub
```

Safe to share.

Example:

```
ssh-ed25519 AAAAC3Nza...
```

---

# 7. How Public Key Authentication Works

Server contains:

```
~/.ssh/authorized_keys
```

with your public key.

---

Client:

```
ssh -i ~/.ssh/id_rsa user@server
```

---

Server:

```
Prove you own private key.
```

Sends challenge.

---

Client:

Signs challenge.

Using:

```
Private Key
```

---

Server:

Verifies signature.

Using:

```
Public Key
```

If valid:

```
Access Granted
```

---

# 8. SSH Host Keys

Different from user keys.

Many confuse these.

---

## User Key

Used to prove:

```
Who are you?
```

---

## Host Key

Used to prove:

```
Which server is this?
```

---

Server stores:

```
/etc/ssh/ssh_host_ed25519_key
```

Client stores fingerprint:

```
~/.ssh/known_hosts
```

---

First connection:

```
The authenticity of host can't be established.
```

Example:

```
ssh 10.10.10.5
```

Output:

```
Are you sure you want to continue connecting?
```

---

# 9. Hashes in SSH

Hash functions:

```
Input -> Fixed Length Output
```

Example:

```
hello
```

becomes:

```
2cf24dba...
```

using SHA256.

---

Properties:

- One-way
- Fast
- Deterministic

---

SSH uses hashes for:

### Integrity

Ensures packets weren't modified.

### Fingerprints

Example:

```
SHA256:aB7dX...
```

used for host verification.

---

# 10. Algorithms Used in SSH

Modern SSH may negotiate:

---

## Key Exchange

```scss
curve25519-sha256
ecdh-sha2-nistp256
diffie-hellman-group14-sha256
```

---

## Host Key Algorithms

```scss
ssh-ed25519
ecdsa-sha2-nistp256
rsa-sha2-512
```

---

## Encryption Algorithms

```scss
aes256-gcm
aes256-ctr
chacha20-poly1305
```

---

## Integrity Algorithms

```
hmac-sha2-256
hmac-sha2-512
```

---

See negotiated algorithms:

```
ssh -vvv user@server
```

---

# 11. SSH Agent

Without agent:

```
ssh server1
ssh server2
ssh server3
```

Passphrase every time.

---

Start:

```
eval $(ssh-agent)
```

Add key:

```
ssh-add ~/.ssh/id_ed25519
```

Now key remains in memory.

---

# 12. SSH Port Forwarding

One of SSH's most powerful features.
Port forwarding allows you to **tunnel traffic securely through SSH**.
SSH can tunnel TCP traffic.

Three major types:

1. Local Forwarding (-L)
2. Remote Forwarding (-R)
3. Dynamic Forwarding (-D)

---

# Local Port Forwarding (-L)

Syntax:

```bash
ssh -L local_port:remote_host:remote_port user@ssh_server
ssh -L [local_bind_address:]local_port:remote_host:remote_port user
```

Example:

```bash
ssh -L 1521:localhost:1521 oracle@10.10.10.5
```

```
Diagram:

```scss
Your PC
localhost:1521
      |
      |
      V
SSH Tunnel
      |
      |
Server
localhost:1521
```



---

## Oracle Example

Database only listens:

```
127.0.0.1:1521
```

Cannot access directly.

Create tunnel:

```
ssh -L 1521:localhost:1521 oracle@server
```

Now DBeaver connects to:

```
localhost:1521
```

and reaches remote Oracle.

---

Other example:

```
ssh -L 8080:localhost:80 user@server
```
### Meaning:
- Your machine listens on port 8080
- Traffic goes through SSH to `server`
- Then server connects to its own port 80

### Use case:
Access private web server safely
```
Browser → localhost:8080 → SSH tunnel → server:80
```



---

# Understanding Your Example

```
ssh -L [local_bind_address:]local_port:remote_host:remote_port user@ssh_server
```

Example:

```
ssh -L 8080:10.0.0.5:80 jumpbox
```

Meaning:

```scss
localhost:8080
      |
      V
jumpbox
      |
      V
10.0.0.5:80
```

Open:

```
http://localhost:8080
```

Actually reaches:

```
10.0.0.5:80
```

through jumpbox.

Very common in internal networks.

---

# Remote Port Forwarding (-R)
```
ssh -R remote_port:local_host:local_port user@ssh_server
```
Opposite direction.

```
ssh -R 8080:localhost:80 user@server
```

Server port:
```
8080
```

forwards to your machine.

Useful for:

```
Exposing local web server
```

behind NAT.

---

Diagram

```scss
Internet
    |
Server:8080
    |
SSH Tunnel
    |
Your PC:80
```

Example:
```
ssh -R 9000:localhost:3000 user  
```

Show more lines

Meaning:

- Server listens on port 9000
- Forwards back to your local 3000

---

# Dynamic Port Forwarding (-D)
Creates SOCKS proxy.
Use case:
- Route browser traffic through SSH

```
ssh -D 1080 user@server
```

Browser configured:

```
SOCKS5127.0.0.11080
```

Traffic:

```scss
Browser
    |
SOCKS
    |
SSH
    |
Server
    |
Internet
```

Often used in:

- Pentesting
- Bypassing network restrictions
- Internal pivoting

---

# 13. Jump Hosts (ProxyJump)

Suppose:

```scss
Your PC
    |
Jump Server
    |
Internal Server
```

Connect directly:

```
ssh -J jumpuser@jumphost internaluser@internalserver
```

Equivalent to:

```
SSH through jump host
```

---

# 14. SCP and SFTP

SSH also provides file transfer.

---

## SCP

```
scp file.txt user@server:/tmp
```

Copy file securely.

---

## SFTP

```
sftp user@server
```

Interactive file transfer.

---

# 15. Useful SSH Commands

Generate key:

```
ssh-keygen -t ed25519
```

Copy public key:

```
ssh-copy-id user@server
```

Verbose debugging:

```
ssh -vvv user@server
```

Execute command:

```
ssh user@server "hostname"
```

Open tunnel:

```
ssh -L 3306:localhost:3306 user@server
```

SOCKS proxy:

```
ssh -D 1080 user@server
```

---

### Git Authentication
```
git clone git@github.com:user/repo.git
```


# Real-World Examples You Will Encounter

## Oracle Database

```
ssh -L 1521:localhost:1521 oracle@dbserver
```

Then DBeaver:

```
Host: localhostPort: 1521
```

---

## Internal Web Application

```
ssh -L 8080:10.1.1.20:80 jumpbox
```

Access:

```
http://localhost:8080
```

---

## HTB / Pentesting Pivot

```
ssh -D 1080 user@pivot
```

Configure:

```scss
Proxychains
Burp Suite
Firefox SOCKS5
```

Now traffic routes through pivot host.

---

# Mental Model to Remember

SSH is fundamentally:

```
A secure encrypted TCP-based communication protocol
```

It provides:

```scss
1. Confidentiality (Encryption)
2. Authentication (Keys/Passwords)
3. Integrity (Hashes/MACs)
4. Tunneling (Port Forwarding)
```

When you type:

```
ssh user@server
```

the client:

```scss
1. Creates TCP connection
2. Negotiates algorithms
3. Exchanges keys
4. Verifies server identity
5. Authenticates user
6. Starts encrypted session
```

Everything else—SCP, SFTP, tunnels, jump hosts, database access, HTB pivots—is built on top of that secure encrypted channel.