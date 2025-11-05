
```
sudo adduser superadmin
sudo usermod -aG sudo superadmin
echo "superadmin ALL=(ALL) NOPASSWD:ALL" | sudo tee -a /etc/sudoers
```


```
sudo adduser superadmin
sudo usermod -aG wheel superadmin
echo "superadmin ALL=(ALL) NOPASSWD:ALL" | sudo tee -a /etc/sudoers
```