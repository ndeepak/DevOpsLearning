Day 12: Linux Network Services

```bash
# 
curl http://stapp01:3004
```



- [ ] Define the problem clearly and make a list of the symptoms and the possible causes for the symptoms and also gather the evidences.  
- [ ] Check if the Apache process is running.  
- [ ] Check if Apache is listening on the correct port.  
- [ ] Check firewall rules.  
- [ ] Test connectivity from the jump host.  
- [ ] Check logs.  
- [ ] Fix the issue and verify the fix.


```
sudo systemctl status httpd

stapp01.stratos.xfusioncorp.com httpd[544]: (98)Address already in use: A  
H00072: make_sock: could not bind to address 0.0.0.0:3004
```

```
sudo ss -tulnp | grep 3004
```