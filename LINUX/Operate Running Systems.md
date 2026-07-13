# Operate Running Systems


```
sudo systemctl reboot
sudo systemctl poweroff

sudo shutdown 02:00		# 00:00 to 23:59
sudo shutdown +15
sudo shutdown -r 02:00
sudo shutdown -r +15
```


## Boot or change system into different operating modes
```
systemctl get-default
systemctl set-default multi-user.target
systemctl reboot

# to login in graphical login
systemctl isolate graphical.target

# emergency target
systemctl isolate emergency.target # few programs as possible

# rescue target
systemctl isolate rescue.target # few programs as root shell


systemctl set-default graphical.target
```


##  Interrupt the boot process in order to gain access to a system
Restart the machine, and hit down, when something appears, then press `e` to edit.
go to linux line, then press, ctrl + e
```bash

```



