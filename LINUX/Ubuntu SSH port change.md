# Ubuntu SSH port change
Update the SSH configuration file (/etc/ssh/sshd_config) and set the Port directive to 2222 or something you like.

```bash
sudo systemctl restart ssh

# check the ports for ssh
sudo ss -tuln | grep ssh

# Check the ssh configuration syntax
sudo sshd -t

# Allow the firewall
sudo ufw allow 2222/tcp

# Check the start, start or enable it
sudo systemctl status ssh

# Check the logs if needed
tail -f /var/log/auth.log
tail -f /var/log/secure
```

You might need to update the `ListenStream` config in `/etc/systemd/system/sockets.target.wants/ssh.socket`.

Change it from:

```
[Socket]
ListenStream=22
Accept=no
```

To:
```
[Socket]
ListenStream=2222
Accept=no
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl restart ssh
```