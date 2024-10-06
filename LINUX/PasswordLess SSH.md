# Setting Up SSH Key-Pair to Connect to a Server

### Setting Up a PasswordLess SSH Connection!
**Introduction:** SSH (Secure Shell) is an application layer networking protocol used to establish a secure connection between two systems. Using a password to establish a secure connection defeats the purpose of secure communication. Passwords can be tricky; they are often reused across multiple accounts, too easy to guess, or so complicated that they are easily forgotten. Relying solely on a password to secure data transfer leaves it vulnerable. This guide explores a better way to establish a secure connection.
### Config Files:
On a Linux system, OpenSSH is the most common tool for remote logins using the SSH protocol. Like other packages, the config files for OpenSSH are located in the `/etc` directory. By default, the OpenSSH server runs on port 22, but you can configure it to use any other open port.

There are two files of interest in the `/etc/ssh` directory:

- **sshd_config:** This config file is specific to the OpenSSH server and controls how remote clients can log in to the machine.
- **ssh_config:** This is the OpenSSH client-specific configuration file, which controls how users on this machine can connect to remote servers as clients.

### Generating SSH Keys:
A secure alternative to using passwords for SSH connections is to use a key-pair consisting of a private key and a public key.

- The **private key** stays on the client machine (the machine where the key is generated).
- The **public key** must be copied to a specific location on the server.

With encryption keys available on both ends, OpenSSH uses these keys instead of passwords for authentication.

To enhance security, you can add a **passphrase** to your private key, providing an extra layer of authentication:

- **Step 1:** Enter the passphrase to access the private key on the client host.
- **Step 2:** Regular key verification on the server-side checks if the client key is included in the `authorized_keys` list.

### Client-Side:
To generate a public-private key pair, the `ssh-keygen` command is the go-to option. It supports key creation for use by SSH version 2.

#### Key Type:
There are four types supported by the `ssh-keygen` command. The `-t` option allows you to specify the key type:

- **DSA:** An old Digital Signature Algorithm. Typically used with a key size of 1024. No longer recommended.
- **ECDSA:** An algorithm based on Elliptic curves, standardized by the US Government. Supports specific key sizes and is generally well-supported.
- **ED25519:** A recent addition to OpenSSH. Support for this algorithm is not universal yet; hence, it is not recommended for general-purpose applications.
- **RSA:** One of the oldest and most widely used public-key cryptosystems. While it has been effective, its security may diminish with advancements in factoring. Increasing the key size is advisable.

#### Key Size:
Each key type has a default key size value. However, this option is ignored for the ED25519 key type:

- **ECDSA:** Key size options are 256, 384, or 521.
- **ED25519:** Fixed key length.
- **RSA:** Minimum and default key size is 1024; 4096 is recommended.
- **DSA:** The key size must be exactly 1024 bits.

Here’s an example of the key generation process:
```
$ ssh-keygen -t rsa -b 4096
Generating public/private rsa key pair.
Enter file in which to save the key (/home/deepak/.ssh/id_rsa): /home/deepak/.ssh/id_deepak
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/deepak/.ssh/id_deepak.
Your public key has been saved in /home/deepak/.ssh/id_deepak.pub.
The key fingerprint is:
SHA256:X7sJY+eXGEQ1x48pQVbb+3rAJucww16yViyb8Z1nkwg deepak@myvm
```

The public and private keys are now in the desired location on the client machine. The public key must be placed on the server to enable SSH access with the generated key pair. It is recommended to generate the private key on the client machine and not transfer it from one host to another for security reasons.

### Server-Side:
The public key generated on the client side must be added to the server. Follow these steps:

1. Create a directory `.ssh` in the user's home directory.
2. Create a file called `authorized_keys` with permissions set to 600.
3. Copy the public key into the file.
```
$ ssh deepak@myserver.com
# on the server
$ mkdir -p /home/deepak/.ssh
# create authorized_keys file with read and write permissions only for the owner
$ install -m 600 /dev/null .ssh/authorized_keys
# copy and paste the public key from the client to the authorized_keys file on the server.
```

To simplify the process, you can use this one-liner:
`cat .ssh/id_deepak.pub | ssh deepak@myserver.com "cat >> .ssh/authorized_keys"`
You'll be prompted for the password.
Alternatively, you can use the official command to copy the public key to the server:
`ssh-copy-id -i /home/deepak/.ssh/id_deepak.pub deepak@myserver.com`

After adding the public key to `authorized_keys`, you can now log in to the server without a password:
`ssh deepak@myserver.com # Welcome screen on the server`

If you have multiple keys on the client, specify which key to use with the `-i` option:
`ssh -i /home/deepak/.ssh/id_deepak myserver.com`

### Passing Custom SSH Options During File Transfer:
**SCP** and **Rsync** are commonly used tools for file transfer between systems, utilizing SSH for secure connections. You can pass custom SSH options to both SCP and Rsync with the following parameters:
- Specify a different port or the path to the key:
```
# Copying a file from the server to the client
scp -i /home/deepak/test_key -P 2001 deepak@myserver.com:/home/deepak/backup.tar .
rsync -avz -e "ssh -i $HOME/.ssh/id_deepak -p 2001" deepak@myserver.com:/from/dir/ /to/dir/
```

### Final Words:
This guide demonstrates how to use a public-private key pair to establish a secure connection with SSH, transitioning to a password-less SSH experience. I hope you found this article informative!

---

