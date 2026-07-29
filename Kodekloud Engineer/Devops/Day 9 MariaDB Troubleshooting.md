Day 9: MariaDB Troubleshooting


```
sudo systemctl status mariadb

sudo cat /var/log/mariadb/mariadb.log
```

```

sudo journalctl -u mariadb --since "2025-11-09 12:43:00" --until "2025-11-09 12:45:00"

sudo systemctl is-enabled mariadb
sudo systemctl start mariadb

sudo tail -30 /var/log/mariadb/mariadb.logs

ls -ld /run/mariadb

```


```
sudo chown mysql:mysql /run/mariadb  
  
# To check if the changes were applied.  
ls -ld /run/mariadb/  
drwxr-xr-x 2 mysql mysql 40 Nov 9 12:44 /run/mariadb/
```


```
sudo systemctl restart mariadb  
sudo systemctl status mariadb
```