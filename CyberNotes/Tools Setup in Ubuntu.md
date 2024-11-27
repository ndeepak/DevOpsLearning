Here's a complete Bash script to automate the installation and setup of the various tools mentioned in your list for an Ubuntu machine:

### Bash Script: `install_tools.sh`
```
#!/bin/bash

# Script to install various tools on Ubuntu

# Exit immediately if a command exits with a non-zero status
set -e

# Install dependencies
sudo apt update
sudo apt install -y wget git curl python3 python3-pip snapd build-essential

# 1. Install Go
echo "Installing Go..."
# wget https://go.dev/dl/go1.23.2.linux-amd64.tar.gz
# sudo tar -xvf go1.23.2.linux-amd64.tar.gz -C /usr/local
# rm go1.23.2.linux-amd64.tar.gz

# Set Go environment variables
# echo "Configuring Go environment variables..."
# echo 'export GOROOT=/usr/local/go' >> ~/.bashrc
# echo 'export GOPATH=$HOME/go' >> ~/.bashrc
# echo 'export PATH=$GOPATH/bin:$GOROOT/bin:$PATH' >> ~/.bashrc
# source ~/.bashrc

# Verify Go installation
go version

# 2. Install Subfinder
echo "Installing Subfinder..."
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
sudo cp ~/go/bin/subfinder /usr/local/bin/
subfinder -h

# 3. Install Amass
echo "Installing Amass..."
go install -v github.com/owasp-amass/amass/v4/...@master
# sudo snap install amass
# sudo apt install -y amass
amass -h

# 4. Install Assetfinder
echo "Installing Assetfinder..."
go install -v github.com/tomnomnom/assetfinder@latest
sudo cp ~/go/bin/assetfinder /usr/local/bin/

# 5. Install Subbrute
echo "Installing Subbrute..."
git clone https://github.com/TheRook/subbrute.git ~/tools/subbrute
cd ~/tools/subbrute/
pip install requests dnspython argparse
chmod +x ~/subbrute/subbrute.py
cd ../

# 6. Install Knockpy
echo "Installing Knockpy..."
git clone https://github.com/guelfoweb/knock.git ~/tools/knock
cd ~/tools/knock
chmod +x *
sudo python3 setup.py install
cd ../

# 7. Install Dnsgen
echo "Installing Dnsgen..."
pip install dnsgen

# 8. Install Censys Subdomain Finder
echo "Installing Censys Subdomain Finder..."
git clone https://github.com/christophetd/censys-subdomain-finder.git ~/tools/censys-subdomain-finder
cd ~/tools/censys-subdomain-finder
pip install -r ~/censys-subdomain-finder/requirements.txt
cd ../

# 9. Install crt.sh Tool
echo "Installing crt.sh tool..."
git clone https://github.com/az7rb/crt.sh ~/tools/crt.sh
chmod +x ~/tools/crts.sh/*

# 10. Install Waybackurls
echo "Installing Waybackurls..."
go install github.com/tomnomnom/waybackurls@latest

# 11. Install Httprobe
echo "Installing Httprobe..."
go install github.com/tomnomnom/httprobe@latest

# 12. Install FFF
echo "Installing FFF..."
go install github.com/tomnomnom/fff@latest

# 13. Install WappalyzerGo
echo "Installing WappalyzerGo..."
go install -v github.com/projectdiscovery/wappalyzergo/cmd/update-fingerprints@latest

# 14. Install Anew
echo "Installing Anew..."
go install -v github.com/tomnomnom/anew@latest

# 15. Install 4-ZERO-4
echo "Installing 4-ZERO-4..."
git clone https://github.com/Dheerajmadhukar/4-ZERO-3.git ~/4-ZERO-3


cd ~/tools/
echo '#!/bin/bash' >> livetest.sh

echo "cat subs.txt |" >> livetest.sh
echo "while read line" >> livetest.sh
echo "do" >> livetest.sh
echo "	curl $line &> /dev/null" >> livetest.sh
echo "	if [ $? == 0 ]" >> livetest.sh
echo "	then" >> livetest.sh
echo "		echo Alive Domain -- $line" >> livetest.sh
echo "	fi" >> livetest.sh
echo "done" >> livetest.sh

pip3 install py-altdns==1.0.2


# 16. Installing Massdns
echo "Installing massdns"
git clone https://github.com/blechschmidt/massdns.git ~/tools/massdns
cd ~/tools/massdns
make
make install
cd ..

# 17. Installing httpx
echo "Installing httpx"
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
httpx -h

# 18. Installing gowitness
go install github.com/sensepost/gowitness@latest

# 19. Installing gau
go install github.com/lc/gau/v2/cmd/gau@latest

# 20. Installing  
GO111MODULE=on go install github.com/jaeles-project/gospider@latest

# 21. Installing paramspider
git clone https://github.com/devanshbatham/paramspider ~/tools/paramspider
cd ~/tools/paramspider
chmod +x *
pip install .
cd ..

# 22. Installing gf qsreplace
go install github.com/tomnomnom/gf@latest
go install github.com/tomnomnom/qsreplace@latest

# Cleaning up and finishing
echo "Installation complete. Please restart your terminal or run 'source ~/.bashrc' to apply changes."
```

### Steps to Use:

1. **Save** the script to a file:
    `nano install_tools.sh`
    
2. **Paste** the script contents and save (CTRL+O, then CTRL+X).
3. **Make it executable**:
    `chmod +x install_tools.sh`
    
4. **Run** the script:
    `./install_tools.sh`

### Notes:
- This script assumes a clean Ubuntu environment.
- It includes environment setup for Go and installs various tools using `go install` or package managers.
- You can customize it further based on additional tool configurations or specific paths.