# Specify Ports, number of ports, host, threading library for faster
#!/usr/bin/python
from socket import *

# For help options 
import optparse
from ssl import Options 
from threading import *

from termcolor import colored

def connScan(tgtHost, tgtPort):
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((tgtHost, tgtPort))
        print(colored("[+] %d/tcp Open" % tgtPort), 'green')
    except:
        print(colored("[-] %d/tcp Closed " % tgtPort), 'red')
    finally:
        sock.close()

def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print("Unknown Host %s" %tgtHost)
    try:
        tgtName = gethostbyaddr(tgtIP)
        print("[+] Scan Results for: " + tgtName[0])
    except:
        print("[+] Scan Results for: " + tgtIP)

    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target= connScan, args=(tgtHost, int(tgtPort)))
        t.start()

def main():
    parser = optparse.OptionParser("Usage of Program: " + "-H <target host> -p <target ports>")
    parser.add_option('-H', dest= 'tgtHost', type='string', help='Specify Target Host')
    parser.add_option('-p', dest = 'tgtPort', type='string', help='Specify Target Ports separated by comma')
    (Options, args) = parser.parse_args()
    tgtHost = Options.tgtHost
    tgtPorts = str(Options.tgtPort).split(',')
    if(tgtHost == None) | (tgtPorts[0] == None):
        print(parser.usage)
        exit(0)
    portScan(tgtHost, tgtPorts)

if __name__ == '__main__' :
    main()
           