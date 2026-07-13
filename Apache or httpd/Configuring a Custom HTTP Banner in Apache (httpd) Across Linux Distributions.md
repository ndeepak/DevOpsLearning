# Configuring a Custom HTTP Banner in Apache (httpd) Across Linux Distributions

## Introduction

In web server administration and system security engineering, controlling the information a server exposes is an important aspect of hardening and compliance. One common requirement is the addition of a **custom banner**, which can either provide identification or deliberately obscure real service details.

A frequent point of confusion arises when administrators attempt to view such a banner using:
`telnet localhost 80  `

and expect an immediate response similar to services like SSH or FTP. This behavior is not supported by HTTP servers like Apache. Understanding why this is the case is essential before implementing the correct solution.

---

## Why Apache Does Not Display a Banner on Connection

Protocols such as SSH and FTP are designed to send a banner immediately after a TCP connection is established. HTTP, however, follows a **client-driven request-response model**.

When a connection is made to port 80:
`telnet localhost 80`

Apache performs the following:
- Accepts the TCP connection
- Waits for a valid HTTP request
- Sends no data until a request is received

This means that no banner or message will be displayed until the client sends a properly formatted HTTP request such as:
```
GET / HTTP/1.1
Host: localhost
```

Only after this request will Apache generate a response, including headers and content.

---

## Implementing a Custom Banner Using HTTP Headers
The correct and standard method of implementing a banner in Apache is by adding a custom **HTTP response header**. This approach integrates with the protocol rather than attempting to override it.

---

### Configuration on RHEL-Based Systems
(RHEL, CentOS, Rocky Linux, AlmaLinux)

#### Step 1: Verify that the headers module is enabled
`httpd -M | grep headers`
Expected output:
```
headers_module (shared)
```

#### Step 2: Create a configuration file
`sudo nano /etc/httpd/conf.d/banner.conf  ``
Add the following directive:
```Apache Config
Header always set X-Banner "Deepak Nagarkoti | System Security Engineer"  
```

#### Step 3: Restart the Apache service
`sudo systemctl restart httpd  ``
### Configuration on Debian-Based Systems
(Ubuntu, Debian)
#### Step 1: Enable the required module
`sudo a2enmod headers  ``
#### Step 2: Create a configuration file
`sudo nano /etc/apache2/conf-available/banner.conf  ``

Add:
`Header always set X-Banner "Deepak Nagarkoti | System Security Engineer"`

Enable the configuration:
`sudo a2enconf banner ``
#### Step 3: Restart the service
`sudo systemctl restart apache2`

## Testing the Configuration
### Using telnet
`telnet localhost 80`
Then manually issue a request:
```
GET / HTTP/1.1
Host: localhost
```

The response should include a header similar to:
```
X-Banner: Deepak Nagarkoti | System Security Engineer
```

---

### Using curl (recommended method)
`curl -I http://localhost`

Expected output:
```
HTTP/1.1 200 OK
X-Banner: Deepak Nagarkoti | System Security Engineer
```

Using `curl` is more reliable and efficient than telnet for HTTP testing.
## Adding a Banner in the Response Body
In addition to headers, a message can also be displayed in the web content itself.
Edit the default document root:
`/var/www/html/index.html`
Example:
`<h1>Deepak Nagarkoti | System Security Engineer</h1>`
This will display in a browser but is separate from HTTP headers and cannot be considered a service banner in the traditional sense.

---

## Security Hardening: Controlling Default Server Information

By default, Apache exposes version and platform details in the `Server` header. This information can aid attackers and should be minimized.

### Modify the Apache configuration

For RHEL-based systems:
`sudo nano /etc/httpd/conf/httpd.conf`

For Debian-based systems:
`sudo nano /etc/apache2/apache2.conf`

Add or modify the following directives:
```
ServerTokens Prod  

ServerSignature Off  
```

### Result
Before:
```
Server: Apache/2.4.57 (Red Hat)
```

After:
```
Server: Apache
```

---

## Advanced Banner Control Techniques

### Overriding the Server Header

Apache can be configured to present a different identity:
`Header set Server "nginx"`
### Removing the Server Header Completely
`Header unset Server`
### Implementing Warning or Compliance Messages
`Header always set X-Banner "Authorized Access Only - Activity Monitored"`
These techniques are often used in controlled environments such as penetration testing labs, honeypots, or compliance-driven systems.

---

## Alternative Approach: Non-HTTP Banner (For Demonstration Purposes)

If the requirement is to display a message immediately upon connection (without waiting for a request), Apache cannot fulfill this requirement.

A simple TCP listener can be used instead:
`while true; do echo "Custom Banner Message" | nc -l -p 80; done`

This approach:
- Stops Apache from using port 80
- Does not serve HTTP content
- Is suitable only for testing or simulation

---

## Summary
Apache does not support immediate banner display upon TCP connection because of the HTTP protocol design. The correct and standard approach is to include custom information in HTTP headers or content.

Key points:

- HTTP operates on a request-response model
- Custom banners should be implemented using headers
- Telnet testing requires a valid HTTP request
- Server information should be minimized for security
- Non-HTTP banners require alternative tools outside Apache

---

## Conclusion
Understanding protocol behavior is fundamental when configuring services. Attempting to force HTTP into behaving like other protocols leads to confusion and incorrect implementations.

By using Apache’s built-in capabilities such as `mod_headers`, administrators can properly implement banners in a way that aligns with standards while also improving system security and compliance posture.

This approach is widely applicable in enterprise environments, security testing scenarios, and production-grade deployments where control over service exposure is essential.