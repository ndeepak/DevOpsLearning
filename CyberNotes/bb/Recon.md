So How to actually look for vulnerability or what to look after Recon?


Checking Live Subdomains (you can use HTTPX)
 We will check technology (we can do that manually or automation)



Tip- If you have a good system you can test open ports on the IP address you gathered and then run your automation.


Manual Testing
Open each website one by one to check functionality or what that web page does.
Follow the Checklist to avoid confusion.

Tip- Look for 3rd Party Technology used and their vulnerability.


How to Find a Good Checklist?




Bounty Target List- https://github.com/amanmahendra00/bugbounty/blob/cf3121fd1004cd9544b78caf1855bdd51819998ec/bug_bounty_list.json





Harsh Bothra 365 Day Checklist- https://github.com/harsh-bothra/learn365/blob/main/README.md





Bugcrowd Taxanomy - https://bugcrowd.com/vulnerability-rating-taxonomy



Few Gitbook and Checklist
https://0xn3va.gitbook.io
https://pentestbook.six2dez.com
https://github.com/punishell/bbtips
https://github.com/imran-parray/Web-Sec-CheatSheet


Website for finding Exploit- https://sploitus.com/?




Vulnerabilities List

SQL injection aka SQLi
Cross-site scriptting aka XSS
Subdomain takeover
Relative path overwrite / Path-relative style sheet import
Cross-site request forgery aka CSRF
Clickjacking
Cross-origin resource sharing aka CORS
Cookies

SSL cookie without secure flag set
Cookie scoped to parent domain
Duplicate cookies set
Cookie without HttpOnly fla1g set
Cookie manipulation (DOM-based)
Cookie manipulation (reflected DOM-based)
Cookie manipulation (stored DOM-based)
Headers manipulation

HTTP response header injection aka CRLF
Referer-dependent response
X-Forwarded-For dependent response
User agent-dependent response

Ajax request header manipulation (DOM-based)
Ajax request header manipulation (reflected DOM-based)
Ajax request header manipulation (stored DOM-based)

Cacheable HTTPS response
Multiple content types specified
Content type incorrectly stated
Content type is not specified
Code injection

PHP code injection
Serialized object in HTTP message
Server-side JavaScript code injection
Perl code injection
Ruby code injection
Python code injection
Expression Language injection
Unidentified code injection
Server-side template injection
SSI injection
Client-side template injection
JavaScript injection (DOM-based)
JavaScript injection (reflected DOM-based)
JavaScript injection (stored DOM-based)

Client-side JSON injection (DOM-based)
Client-side JSON injection (reflected DOM-based)
Client-side JSON injection (stored DOM-based)
XML manipulation

XML injection
XML external entity injection
XPath injection
Client-side XPath injection (DOM-based)
Client-side XPath injection (reflected DOM-based)
Client-side XPath injection (stored DOM-based)
XML entity expansion
HTTP method

HTTP PUT method is enabled
HTTP TRACE method is enabled
HTML5

HTML5 web message manipulation (DOM-based)
HTML5 web message manipulation (reflected DOM-based)
HTML5 web message manipulation (stored DOM-based)
HTML5 storage manipulation (DOM-based)
HTML5 storage manipulation (reflected DOM-based)
HTML5 storage manipulation (stored DOM-based)
Information exposure

ASP.NET tracing enabled
ASP.NET debugging enabled
ASP.NET ViewState without MAC enabled
Email addresses disclosed
Private IP addresses disclosed
Private key disclosed
Database connection string disclosed
Source code disclosure
Directory listing
File path manipulation

File path traversal
File path manipulation
Local file path manipulation (DOM-based)
Local file path manipulation (reflected DOM-based)
Local file path manipulation (stored DOM-based)
Password related

Cleartext submission of password
Password returned in later response
Password submitted using GET method
Password returned in URL query string
Password field with autocomplete enabled
Password value set in cookie
DDOS

Denial of service (DOM-based)
Denial of service (reflected DOM-based)
Denial of service (stored DOM-based)
Others

Out-of-band resource load (HTTP)
WebSocket hijacking (DOM-based)
WebSocket hijacking (reflected DOM-based)
WebSocket hijacking (stored DOM-based)
LDAP injection
SMTP header injection
Os command injection

Flash cross-domain policy
Silverlight cross-domain policy

External service interaction (DNS)
External service interaction (HTTP)
External service interaction (SMTP)

Cross-domain POST
Input returned in response (stored)
Input returned in response (reflected)
Suspicious input transformation (reflected)
Suspicious input transformation (stored)
Cross-domain Referer leakage
Cross-domain script include
Session token in URL

File upload functionality

Long redirection response
Open redirection
Open redirection (DOM-based)
Open redirection (reflected DOM-based)
Open redirection (stored DOM-based)

Link manipulation (DOM-based)
Link manipulation (reflected DOM-based)
Link manipulation (stored DOM-based)
Document domain manipulation (DOM-based)
Document domain manipulation (reflected DOM-based)
Document domain manipulation (stored DOM-based)
DOM data manipulation (DOM-based)
DOM data manipulation (reflected DOM-based)
DOM data manipulation (stored DOM-based)

HTML does not specify charset
HTML uses unrecognized charset

SSL certificate
Unencrypted communications
Strict transport security not enforced
Mixed content