How to effectively use knock.py
knockpy domain.com thats how everyone uses it.
knockpy domain.com --dns 8.8.8.8 

This is what we will be talking about. How to benefit from this.
The command knockpy domain.com --dns 8.8.8.8 is using the knockpy tool to perform subdomain enumeration on the target domain "domain.com" while specifying a custom DNS server, in this case, "8.8.8.8." Let's break down what this command is doing and its benefits in detail:
1. Subdomain Enumeration:
knockpy domain.com: This part of the command tells knockpy to perform subdomain enumeration on the target domain "domain.com." Subdomain enumeration involves finding subdomains associated with the main domain.

2. Using Custom DNS Server:
--dns 8.8.8.8: This part of the command specifies a custom DNS server to be used for the enumeration process. In this case, "8.8.8.8" is Google's public DNS server.



Setup

git clone https://github.com/guelfoweb/knock.git
cd knock
python3 setup.py install

Usage
 knockpy domain.com


knockpy domain.com --dns 8.8.8.8 



Chatgtp prompt for More Private DNS

are there more dns like google 8.8.8.8 we can use for recon on tools like knockpy

