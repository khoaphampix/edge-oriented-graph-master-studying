#!/bin/bash

source .env
remote_host=$HOST_IP

# remote_host=65.109.75.59
remote_user="root"

command_to_run=""

# Login to remote server and run command
ssh -t "$remote_user"@"$remote_host" "cd /home/edge-oriented-graph-master-studying/src && 
            cat /home/edge-oriented-graph-master-studying/configs/parameters_cdr.yaml
            echo -e '\n'
            echo -e '------------'
            cat /home/edge-oriented-graph-master-studying/src/run.sh
            echo -e '\n'
            echo -e '------------'
        "  
