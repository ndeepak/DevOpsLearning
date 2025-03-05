# Host OS Vulnerabilities

The first item of the OWASP Docker Top 10 is:
"Host OS Vulnerabilities in the container host can be leveraged to gain access to containers."

An example of this type of attack is a vulnerability in the host OS kernel that could allow an attacker to escape from a container and gain access to the host system.

A well-known example is the "Dirty COW" vulnerability (CVE-2016-5195) which was a privilege escalation vulnerability in the Linux kernel.

An attacker could use this vulnerability to gain root access to the host system, even if the host was running in a container.

The exploitation of host operating system vulnerabilities can occur through various means, including known exploit kits, malware, and unauthorized access to the host operating system through misconfigured or weak access controls.

To mitigate the risk of host operating system vulnerabilities, organizations should implement regular patching and vulnerability management for the host operating system.

By implementing regular patching and vulnerability management, using security tools, and implementing strict access controls, organizations can effectively mitigate this risk.




