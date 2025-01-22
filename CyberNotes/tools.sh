#!/bin/bash

# Script to install various tools on Ubuntu
# Author: Deepak Nagarkoti
# This script installs essential security tools for system engineers.

set -e  # Exit on error

# Define colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RESET='\033[0m'

# Function to print status messages
print_status() {
  echo -e "${GREEN}[+] $1${RESET}"
}

# Function to check if a directory exists before cloning
install_git_tool() {
  tool_name=$1
  repo_url=$2
  install_path=$3

  if [ -d "$install_path" ]; then
    echo -e "${YELLOW}[!] $tool_name is already installed. Skipping...${RESET}"
  else
    print_status "Installing $tool_name..."
    git clone "$repo_url" "$install_path"
    cd "$install_path" || exit
    pip install -r requirements.txt || true  # Ignore missing requirements file
    cd ~ || exit
  fi
}

# Function to install Go-based tools
install_go_tool() {
  tool_name=$1
  go_url=$2

  if ! command -v "$(basename "$go_url" | cut -d '@' -f 1)" &>/dev/null; then
    print_status "Installing $tool_name..."
    go install -v "$go_url"
  else
    echo -e "${YELLOW}[!] $tool_name is already installed. Skipping...${RESET}"
  fi
}

# Update and install dependencies
print_status "Updating package lists and installing dependencies..."
sudo apt update && sudo apt install -y wget git curl python3 python3-pip snapd build-essential

# Install Go
print_status "Installing Go..."
if ! go version &>/dev/null; then
  wget https://go.dev/dl/go1.23.2.linux-amd64.tar.gz
  sudo tar -C /usr/local -xzf go1.23.2.linux-amd64.tar.gz
  rm go1.23.2.linux-amd64.tar.gz
  echo 'export GOROOT=/usr/local/go' >> ~/.bashrc
  echo 'export GOPATH=$HOME/go' >> ~/.bashrc
  echo 'export PATH=$GOPATH/bin:$GOROOT/bin:$PATH' >> ~/.bashrc
  source ~/.bashrc
else
  echo -e "${YELLOW}[!] Go is already installed. Skipping...${RESET}"
fi

# Verify Go installation
print_status "Verifying Go installation..."
go version

# Install various Go-based tools
install_go_tool "Subfinder" "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
install_go_tool "Amass" "github.com/owasp-amass/amass/v4/...@master"
install_go_tool "Assetfinder" "github.com/tomnomnom/assetfinder@latest"
install_go_tool "Waybackurls" "github.com/tomnomnom/waybackurls@latest"
install_go_tool "Httprobe" "github.com/tomnomnom/httprobe@latest"
install_go_tool "FFF" "github.com/tomnomnom/fff@latest"
install_go_tool "WappalyzerGo" "github.com/projectdiscovery/wappalyzergo/cmd/update-fingerprints@latest"
install_go_tool "Anew" "github.com/tomnomnom/anew@latest"
install_go_tool "Httpx" "github.com/projectdiscovery/httpx/cmd/httpx@latest"
install_go_tool "Gowitness" "github.com/sensepost/gowitness@latest"
install_go_tool "Gau" "github.com/lc/gau/v2/cmd/gau@latest"
install_go_tool "Gospider" "github.com/jaeles-project/gospider@latest"
install_go_tool "GF" "github.com/tomnomnom/gf@latest"
install_go_tool "Qsreplace" "github.com/tomnomnom/qsreplace@latest"

# Install tools via git clone and Python pip
install_git_tool "Subbrute" "https://github.com/TheRook/subbrute.git" "$HOME/tools/subbrute"
install_git_tool "Knockpy" "https://github.com/guelfoweb/knock.git" "$HOME/tools/knock"
install_git_tool "Censys Subdomain Finder" "https://github.com/christophetd/censys-subdomain-finder.git" "$HOME/tools/censys-subdomain-finder"
install_git_tool "crt.sh Tool" "https://github.com/az7rb/crt.sh" "$HOME/tools/crt.sh"
install_git_tool "4-ZERO-4" "https://github.com/Dheerajmadhukar/4-ZERO-3.git" "$HOME/tools/4-ZERO-3"
install_git_tool "ParamSpider" "https://github.com/devanshbatham/paramspider" "$HOME/tools/paramspider"

# Install additional Python tools
print_status "Installing Dnsgen..."
pip install dnsgen py-altdns==1.0.2

# Install Massdns
install_git_tool "Massdns" "https://github.com/blechschmidt/massdns.git" "$HOME/tools/massdns"
cd "$HOME/tools/massdns" || exit
make
sudo make install
cd ~

# Create a livetest.sh script
print_status "Creating livetest.sh script..."
cat <<EOF > ~/tools/livetest.sh
#!/bin/bash
while read -r line; do
  curl "\$line" &>/dev/null && echo "Alive Domain -- \$line"
done < subs.txt
EOF
chmod +x ~/tools/livetest.sh

# Final message
print_status "Installation complete! Restart your terminal or run 'source ~/.bashrc' to apply changes."
