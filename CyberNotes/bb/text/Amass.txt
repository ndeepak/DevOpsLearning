What is Amass?

Amass is a versatile and powerful subdomain enumeration tool that uses various data sources and techniques to discover subdomains associated with a target domain. It's known for its extensive feature set and flexibility.

Installation:

Before you begin, make sure you have Go (the programming language) installed. You can install Amass using the following commands:



bash code

go get -u https://github.com/owasp-amass/amass﻿

Basic Usage:

To effectively use Amass, follow these steps:

Open your terminal.

amass enum -d domain.com﻿

﻿

Basic Enumeration:

amass enum -d domain.com﻿

This command performs a basic subdomain enumeration against the target domain using default data sources.

﻿

Specifying an Output File:

amass enum -d domain.com -o output.txt

﻿

Active Scanning:



amass enum -d domain.com -active

﻿

Recursive Enumeration:



bashCopy code

amass enum -d domain.com -recursive

﻿

Customizing Data Sources:



amass enum -d domain.com -src <data_source_name>





How to get better and more effective results from Amass?

A lot of you are not aware of API keys. There are many companies that provide monitoring services or more. Like Securitytrails, Project Discovery, and all. You need to set up those. I will share the link in the Description for a few.

﻿

Companies- AlienVault, BinaryEdge, BufferOver, BuiltWith, C99, Censys, Chaos, CIRCL, DNSDB, DNSTable, FacebookCT, GitHub, HackerOne, HackerTarget, NetworksDB, PassiveTotal, RapidDNS, Riddler, SecurityTrails, Shodan, SiteDossier, Twitter, Umbrella, URLScan, VirusTotal, WhoisXML, ZETAlytics, Cloudflare

﻿

For setting up in Amass - https://github.com/owasp-amass/amass/blob/master/examples/datasources.yaml﻿

﻿

Here is a good Article to learn more about the usage - https://hakluke.medium.com/haklukes-guide-to-amass-how-to-use-amass-more-effectively-for-bug-bounties-7c37570b83f7﻿


Shodan: https://developer.shodan.io/

VirusTotal:https://developers.virustotal.com/v3.0/reference#overview

HackerTarget:https://hackertarget.com/

Censys:https://search.censys.io/register

GitHub: https://docs.github.com/en/rest

Website: https://builtwith.com/api

PassiveTotal API:https://www.riskiq.com/products/passivetotal/api-documentation/

CIRCL API:https://www.circl.lu/doc/misp/automation/index.html

Farsight DNSDB API:https://www.farsightsecurity.com/solutions/dnsdb/

SecurityTrails:https://securitytrails.com/corp/api

BinaryEdge:https://app.binaryedge.io/account/signup

ProjectDiscovery API: https://pdiscovery.io/
