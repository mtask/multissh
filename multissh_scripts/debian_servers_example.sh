#!/bin/bash

# Example for Debian/Ubuntu servers in multissh.conf.

# Run updates
# Check disk space
# Check auth log for recent password changes
# Check uptime
# 

cd ..
./multissh.py -c "apt-get -y update > /dev/null && apt-get -y upgrade > /dev/null"
echo -e "\n"
./multissh.py -c "df -h"
echo -e "\n"
./multissh.py -c 'grep passwd /var/log/auth.log'
echo -e "\n" 
./multissh.py -c "uptime"

