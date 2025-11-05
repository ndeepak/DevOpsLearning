C:\Program Files\Oracle\VirtualBox>cmdvboxmanage dhcpserver add --network=PentestNet --server-ip=172.30.1.1 --lower-ip=172.30.1.20 --upper-ip=172.30.1.50 --netmask=255.255.255.0 --enable

C:\Program Files\Oracle\VirtualBox>vboxmanage dhcpserver add --network=HiddenNet --server-ip=10.11.12.1 --lower-ip=10.11.12.20 --upper-ip=10.11.12.50 --netmask=255.255.255.0 --enable

C:\Program Files\Oracle\VirtualBox>vboxmanage dhcpserver add --network=RedTeamLab --server-ip=192.168.42.1 --lower-ip=192.168.42.20 --upper-ip=192.168.42.50 --netmask=255.255.255.0 --enable

C:\Program Files\Oracle\VirtualBox>


curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/docker-archive-keyring.gpg >/dev/nul


echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian buster stable' | sudo tee /etc/apt/sources.list.d/docker.list



sudo apt install -y docker-ce docker-ce-cli containerd.io

sudo docker pull bkimminich/juice-shop

sudo docker run --rm -p 3000:3000 bkimminich/juice-shop
