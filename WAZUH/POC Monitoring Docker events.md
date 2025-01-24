Prerequisites: 
1. Install Python and pip:
	sudo apt install python3 python3-pip
2. Upgrade pip:   
    pip3 install --upgrade pip

Python 3.8–3.10
```
curl -sSL https://get.docker.com/ | sh
sudo pip3 install docker==7.1.0 urllib3==1.26.20 requests==2.32.2
```

Python 3.11–3.12
```
curl -sSL https://get.docker.com/ | sh
sudo pip3 install docker==7.1.0 urllib3==1.26.20 requests==2.32.2 --break-system-packages
```

Edit the Wazuh agent configuration file `/var/ossec/etc/ossec.conf` and add this block to enable the `docker-listener` module:
```
<ossec_config>
  <wodle name="docker-listener">
    <interval>10m</interval>
    <attempts>5</attempts>
    <run_on_start>yes</run_on_start>
    <disabled>no</disabled>
  </wodle>
</ossec_config>
```

`sudo systemctl restart wazuh-agent`

## Test the configuration
1. Pull an image, such as the NGINX image, and run a container:
    ```
	sudo docker pull nginx
    sudo docker run -d -P --name nginx_container nginx
    sudo docker exec -it nginx_container cat /etc/passwd
    sudo docker exec -it nginx_container /bin/bash
    exit
	```
1. Stop and remove the container:
    `sudo docker stop nginx_container`

Other info:
https://documentation.wazuh.com/current/user-manual/capabilities/container-security/monitoring-docker.html
