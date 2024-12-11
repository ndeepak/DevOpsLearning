* bash is a unix shell and command language written by brian fox for the GNU project as a free software replacement for the bourne shell
* a shell program is typically an executable binary that takes commands that we type
* typically runs in a text window where user can interpret commands to carry out various actions
* most modern linux and unix distributions provide a bash shell by default.


## terminal
* a piece of equipment through which you could interact with a computer 
* today's terminals are software representations of the old physical terminals, often running on a GUI
* mainly helps in transmission of commands


## shell
* command interpreter whose main purpose is to run other programs 
* converts the command into a kernel-understandable form and passes it to the kernel
* terminal passes the typed commands to shell, which understands them and tells the kernel what to do.


## features of bash
* bash is sh-compatible. it is incorporated with the best and useful features of the Korn and C shell like directory manipulation, job control, aliases, etc.
* bash can be invoked by single character command line options (-a, -b, -c, -i, -l, -r, etc.) as well as by multi-character command line options also like --debugger, --help, --login, etc.
* bash start-up files are the scripts that bash reads and executes when it starts. each file has its specific use, and the collection of the these files is used to help create an environment
* bash consists of key bindings by which one can set up customized editing key sequences
* bash contains one-dimensional arrays using which you can easily reference and manipulate the lists of data.
* bash compromised of control structrues like the select construct that specially used for menu generation
* directory stack in bash specifies the history of recently-visited directories within a list. example: pushd builtin is used to add the directory to the stack, popd is to remove directory from the stack and dirs builtin is to display content of the directory stack.
* bash also comprised of restricted mode for the environment security. a shell gets restricted if bash starts with name rbash, or the bash --restricted, or bash -r option passed at invocation.


bash scripting environment setup
download git-bash from git-scm.com
or download and install ubuntu


what is prompt, which specifies the user,
explain this "user@ubuntu:~$"


## commands lines basics
* hostname 
* pwd - print working directory.
* echo $HOME, echo $SHELL
* startup files, bashrc, .profile or .bash_profile and cat to read these.
*  whatis "command"
* tldr
* man "command"
* echo $PATH
* tilde ~ , cd ~
* ls -a, ls -la, ls 
* mkdir sample1 sample2 sample3
* creating file: touch, echo, cat >, nano, vi, vim, etc. touch file{1...100}.txt
* rm, rmdir, rm -rf 
* whereis, whereis python, whereis bash
* cal
* date, date +%D, date +%d, date +%A, date +%H, date +%d/%m/%Y
* time
* timedatectl
* timedatectl set-timezone "Asia/Kathmandu"
* history , !!,  !123
* cp  for file and folders
* mv for file and folders
* df, df -h
* lsblk
* free -h
* who and w, who -H, who -a
* backgrounding the process, sleep 100&
* jobs
* fg
* ps a, ps e, ps -e, ps -ef, ps -aux, ps -U username
* kill, kill -l, kill -9
* find, find / -f -user username -name -type
* locate
* apt, apt install, apt remove, apt autoremove, apt search, apt autoclean
* su, su -
* sudo -i


## grep
