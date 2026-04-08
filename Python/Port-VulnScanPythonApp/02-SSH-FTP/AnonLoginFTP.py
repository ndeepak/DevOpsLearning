#!/usr/bin/python
import ftplib

def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'anonymous')
        print("[*] " + hostname + "FTP Anonymous Logon Succeeded.")
        ftp.quit()
        return True
    except Exception as e:
        print("[-] " + hostname + "FTP Anonynous Logon Failed.")
# host = input("Enter the IP address of the Machine: ")
host = '192.168.1.75'
anonLogin(host)
