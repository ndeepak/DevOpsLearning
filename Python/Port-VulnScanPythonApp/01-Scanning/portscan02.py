#!/usr/bin/python

import  socket
# For adding color to print outs
from termcolor import colored

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.setdefaulttimeout(1)
host = input("[*] Enter the Host To Scan: "); 
# port = int(input("[*] Enter The Port To Scan: ")); 

def portScanner(port):
	if sock.connect_ex((host, port)):
		print (colored("[!!] Port %d is closed" % (port), 'red'))
	else:
		print (colored("[+] Port %d is open" % (port), 'green'))

# First 1000 port scan
for port in range(1,9000):
    portScanner(port)