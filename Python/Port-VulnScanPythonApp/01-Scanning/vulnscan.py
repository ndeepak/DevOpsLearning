#!/usr/bin/python

from asyncore import read
import socket
import os
import sys

def retBanner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip,port))
        banner = s.recv(1024)
        return banner
    except:
        return

def checkVulns(banner, filename):
    f = open(filename, "r")
    for line in f.readlines():
        if line.strip("\n") in str(banner):
            print("[+] Server is Vulnerable:"  + str(banner))


def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print("[-] File Doesn't Exist!!! ")
            exit(0)
        if not os.access(filename, os.R_OK):
            print("[-] Access Denied!!!") 
            exit(0)   
    else:
        print("[-] Usage: " + str(sys.argv[0]) + " <vuln filename>")
        exit(0)
    portlist = [21,22,25,80,110,443,445]

    # to all hosts in network
    for x in range(74, 77):
        ip = "192.168.1." + str(x)
        for port in portlist:
            banner = retBanner(ip,port)
            if banner:
                print("[+] " + ip + "/" + str(port) + ":" + str(banner))
                checkVulns(banner, filename)


main()
    