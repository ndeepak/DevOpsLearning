Url- https://chat.openai.com/chat

Url - https://bgp.he.net/

1.  whois -h whois.radb.net -- '-i origin AS6185' | grep -Eo "([0-9.]+){4}/[0-9]+" | uniq -u
whois is a command-line utility for querying WHOIS databases to retrieve information about IP addresses or domain names.
-h whois.radb.net specifies the WHOIS server to query.
-- '-i origin AS6185' is used to pass the query -i origin AS6185 to the WHOIS server. This query is specific to finding IP prefixes associated with Autonomous System Number (ASN) 6185.
grep -Eo "([0-9.]+){4}/[0-9]+" extracts IPv4 address prefixes (CIDR notation) from the WHOIS response.
uniq -u filters out duplicate entries and displays only unique IP prefixes.
GitHub Links:

whois: https://github.com/rfc1036/whois
grep: https://github.com/gvansickle/grep

2. cat ip.txt | mapcidr -si -silent -o ipscat ips.txt | hakrevdns -t 100 -d | anew domains.txt


This command appears to be a pipeline of several tools, performing the following tasks:

cat ip.txt reads the content of the file ip.txt.
mapcidr -si -silent -o ipscat ips.txt takes the IP addresses from ip.txt, aggregates them into CIDR notation, and outputs them to a file named ipscat.
hakrevdns -t 100 -d performs reverse DNS lookups on the IP addresses provided, with a timeout of 100 milliseconds.
anew domains.txt.txt appends the results of reverse DNS lookups to the file domains.txt.
GitHub Links:

mapcidr: https://github.com/keltia/mapcidr
hakrevdns: https://github.com/hakluke/hakrevdns
anew: https://github.com/tomnomnom/anew



GitHub Links:

hakrevdns: https://github.com/hakluke/hakrevdns
anew: https://github.com/tomnomnom/anew




