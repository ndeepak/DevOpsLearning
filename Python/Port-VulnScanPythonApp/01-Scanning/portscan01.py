#!/usr/bin/python

import  socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.setdefaulttimeout(2)
host = input("[*] Enter the Host To Scan: "); 
port = int(input("[*] Enter The Port To Scan: ")); 

def portScanner(port):
	if sock.connect_ex((host, port)):
		print ("Port %d is closed" % (port))
	else:
		print ("Port %d is open" % (port))

portScanner(port)