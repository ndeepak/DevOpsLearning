# Day 5: SElinux Installation and Configuration

```bash
# First identify the base OS:  
cat /etc/os-release  
  
# This will install SELinux and all it's dependencies in a system that manages Debian-based package management.  
sudo apt install policycoreutils selinux-basics selinux-utils -y  
  
# This will install SELinux and all it's dependencies in a system that manages CentOS-based package management.  
sudo yum install selinux-policy selinux-policy-targeted  
  
# Open this file and change the SELINUX to Disabled.  
sudo vi /etc/selinux/config
```