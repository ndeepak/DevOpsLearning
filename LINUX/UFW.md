## What is UFW?

**UFW (Uncomplicated Firewall)** is a frontend for managing firewall rules on Linux systems, primarily those that use **iptables** (or the newer **nftables** backend). Its main purpose is to simplify firewall configuration while still allowing powerful control over network traffic.

UFW is commonly pre-installed on Ubuntu and is also available on Debian and other distributions.

---

## Core Concepts

Before using UFW, you need to understand some key networking concepts:

### 1. Ports

- Services listen on ports (e.g., HTTP = 80, HTTPS = 443, SSH = 22).
- Firewalls control whether traffic to these ports is allowed.

### 2. Protocols

- TCP – reliable (web, SSH)
- UDP – faster but less reliable (DNS, streaming)

### 3. Direction of Traffic

- **Incoming**: traffic entering your system
- **Outgoing**: traffic leaving your system

---

## Installation

On Ubuntu (usually preinstalled). To install manually:
sudo apt update  
sudo apt install ufw  



---

## Basic Commands

### Check Status
sudo ufw status  


If inactive:
sudo ufw enable  

Disable:
sudo ufw disable  


---

## Default Policies

UFW uses default rules for incoming and outgoing traffic.

Set defaults:
sudo ufw default deny incoming  
sudo ufw default allow outgoing  


Explanation:
- Deny incoming → blocks unsolicited connections
- Allow outgoing → lets your system access internet

This is a secure standard configuration.

---

## Allowing and Blocking Traffic

### Allow a Port
sudo ufw allow 22  

Allow specific protocol:
sudo ufw allow 80/tcp  
sudo ufw allow 53/udp  

### Deny a Port
sudo ufw deny 23  

### Reject Instead of Deny
sudo ufw reject 23  


- **deny**: silently drops packets
- **reject**: sends a response back (more visible to attacker)

---

## Using Service Names
UFW recognizes services defined in `/etc/services`.
sudo ufw allow ssh  
sudo ufw allow http  
sudo ufw allow https  

---

## Allow Specific IP Addresses
Allow only a specific IP to access:
sudo ufw allow from 192.168.1.100  

Allow a specific IP to a specific port:
sudo ufw allow from 192.168.1.100 to any port 22  

---

## Blocking IP Addresses
sudo ufw deny from 192.168.1.100  

---

## Allow from Subnet
sudo ufw allow from 192.168.1.0/24  

CIDR notation:
- `/24` means range 192.168.1.1 – 192.168.1.254

---

## Outgoing Rules

By default outgoing is allowed, but you can control it:
sudo ufw deny out 25  

Example:
- Block SMTP to prevent spam bots.

---

## Deleting Rules

List rules with numbers:
sudo ufw status numbered  

Delete rule:
sudo ufw delete 3  


Or delete by command:
sudo ufw delete allow 22  


---

## Logging
Enable logging:
sudo ufw logging on  


Levels:
sudo ufw logging low  
sudo ufw logging medium  
sudo ufw logging high  

Logs are stored in:
```
/var/log/ufw.log
```

---

## Advanced Features

### 1. Limiting Connections (Protection Against Brute Force)
sudo ufw limit ssh  

This:
- Allows connections
- Blocks repeated rapid attempts

---

### 2. Allow Port Ranges
sudo ufw allow 1000:2000/tcp  

---

### 3. IPv6 Support
Configure in:
```
/etc/default/ufw
```

Enable IPv6:
```
IPV6=yes
```

---

### 4. Application Profiles

UFW supports predefined profiles in:

```
/etc/ufw/applications.d/
```

List profiles:
sudo ufw app list  

Example:
sudo ufw allow "Nginx Full"  

Details:
sudo ufw app info "Nginx Full"  


---

### 5. Reset UFW
sudo ufw reset  

This clears all rules and disables UFW.

---

### 6. Before and After Rules

Advanced rules can be edited manually in:
- `/etc/ufw/before.rules`
- `/etc/ufw/after.rules`

These are processed:
1. Before user-defined rules
2. After user-defined rules

Used for:
- NAT
- port forwarding
- advanced filtering

---

## Practical Example Setup
Secure a server with SSH + web:
sudo ufw default deny incoming  
sudo ufw default allow outgoing  

  

sudo ufw allow ssh  
sudo ufw allow http  
sudo ufw allow https  

  
sudo ufw enable  


---

## Common Mistake to Avoid

### Locking Yourself Out (SSH)

If you're using a remote server:
Always allow SSH before enabling firewall:
sudo ufw allow ssh  
sudo ufw enable  


---

## How UFW Works Internally
- UFW is not a firewall itself
- It is a wrapper around:
    - **iptables** (older systems)
    - **nftables** (modern systems)

It translates simple commands like:
ufw allow 22  

into complex backend rules.

---

## When to Use UFW vs iptables

|Feature|UFW|iptables|
|---|---|---|
|Ease of use|Very easy|Complex|
|Flexibility|Moderate|Very high|
|Best for|Beginners and admins|Advanced networking|

---

## Summary
- UFW is a simple tool to manage Linux firewall rules.
- It controls traffic based on ports, IPs, and protocols.
- Default secure setup: deny incoming, allow outgoing.
- Supports advanced features like rate limiting and subnet filtering.
- Acts as a user-friendly layer over iptables/nftables.

---