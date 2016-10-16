#!/bin/bash

# Add domain to every websites hosts file
#./add_to_hosts.sh 1.2.3.4 example.com

if [[ $# != 2 ]]; then
    exit 1
fi


cd ..

./multissh.py -S -c "echo $1	$2 >> /etc/hosts" 
