# Day 13: IPtables Installation And Configuration

SSHing
```bash
ssh tony@stapp01
|Ir0nM@n|

ssh steve@stapp02
|Am3ric@|


ssh banner@stapp03
|BigGr33n|

ssh loki@stlb01
|Mischi3f|

ssh thor@jump-host
|mjolnir123|

```


```
sudo dnf install -y iptables iptables-services
sudo systemctl enable --now iptables
sudo systemctl status iptables
```

```
sudo systemctl start iptables
```


```
sudo iptables -L -n --line-numbers
```

---


---


```bash
#!/bin/bash
# Safe iptables setup for CentOS Stream (remote-friendly)
# OS: CentOS Stream
# App server IP: <app-server-01>,<app-server-02>,<app-server-03>
# LBR IP: <LBR-ip>
# Apache listening on port <port-defined in question>
# Default INPUT policy: DROP

# --- Step 1: Determine your current SSH client IP ---
MY_IP=$(echo $SSH_CLIENT | awk '{print $1}')

# --- Step 2: Insert safe allow rules at the top ---
echo "Adding rules safely without flushing..."

# Allow SSH from current session first (top priority)
sudo iptables -C INPUT -p tcp -s $MY_IP --dport 22 -j ACCEPT 2>/dev/null || \
sudo iptables -I INPUT 1 -p tcp -s $MY_IP --dport 22 -j ACCEPT

# Allow LBR access to port 3001
sudo iptables -C INPUT -p tcp -s 10.244.244.181 --dport 3001 -j ACCEPT 2>/dev/null || \
sudo iptables -I INPUT 2 -p tcp -s 10.244.244.181 --dport 3001 -j ACCEPT

# Allow loopback traffic
sudo iptables -C INPUT -i lo -j ACCEPT 2>/dev/null || \
sudo iptables -I INPUT -j ACCEPT -i lo

# Allow established and related connections
sudo iptables -C INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT 2>/dev/null || \
sudo iptables -I INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# --- Step 3: Ensure default DROP policy for INPUT ---
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# --- Step 4: Add a final catch-all drop if not already present ---
sudo iptables -C INPUT -j DROP 2>/dev/null || \
sudo iptables -A INPUT -j DROP
```
---


```
iptables -A INPUT -p tcp --destination-port 5001 -s 10.244.97.165 -j ACCEPT
iptables -A INPUT -p tcp --destination-port 5001 -j DROP
```

```
iptables -L --line-numbers
iptables -R INPUT 5 -p icmp -j REJECT
```


```
service iptables save

sudo iptables-save | sudo tee /etc/sysconfig/iptables
```

```
sudo systemctl restart iptables && sudo systemctl status iptables

```



```
# SSH into the load balancer server.
thor@jumphost ~$ ssh loki@stlb01
[loki@stlb01 ~]$ curl http://<app-server-ip/name>:<port>
# You should be able to see the content.

10.244.244.180:3001


# SSH into any other server [You can try from the jumphost server too]. Your request will be timed out.
thor@jumphost ~$ curl http://<app-server-ip/name>:<port>
curl: (28) Failed to connect to stapp01 port <port>: Connection timed out
```