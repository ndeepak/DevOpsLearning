#!/bin/bash

# Define colors
RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'
RESET='\033[0m'

# Display MOTD with colors
echo -e "
${RED}#######################################################################${RESET}
${RED}#${RESET}           ${YELLOW}UNAUTHORIZED ACCESS WARNING${RESET}           ${RED}#${RESET}
${RED}#${RESET}
${RED}#${RESET}    ${WHITE}Access to this device is strictly prohibited.${RESET}
${RED}#${RESET}    ${WHITE}You must have explicit, authorized permission${RESET}
${RED}#${RESET}    ${WHITE}to access or configure this device.${RESET}
${RED}#${RESET}
${RED}#${RESET}    ${WHITE}Unauthorized attempts and actions to access or${RESET}
${RED}#${RESET}    ${WHITE}use this system may result in civil and/or${RESET}
${RED}#${RESET}    ${WHITE}criminal penalties.${RESET}
${RED}#${RESET}
${RED}#${RESET}    ${WHITE}All activities performed on this device are${RESET}
${RED}#${RESET}    ${WHITE}logged and monitored.${RESET}
${RED}#${RESET}
${RED}#${RESET}    ${GREEN}Deepak Nagarkoti - System Engineer (CAS Total Solutions)${RESET}
${RED}#${RESET}    ${GREEN}WELCOME TO THIS MACHINE, PLEASE WORK EFFICIENTLY${RESET}
${RED}#${RESET}    ${GREEN}AND VERY CAREFULLY, SENSITIVE RESOURCE${RESET}
${RED}#${RESET}                    ${CYAN}$(hostname)${RESET}
${RED}#${RESET}    ${BLUE}This system is running $(lsb_release -d | cut -f2)${RESET}
${RED}#${RESET}    ${BLUE}Kernel is $(uname -r)${RESET}
${RED}#${RESET}    ${BLUE}You are logged in as $(whoami)${RESET}
${RED}#${RESET}
${RED}#######################################################################${RESET}
"
