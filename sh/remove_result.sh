#!/bin/bash

source .env
remote_host=$HOST_IP

# remote_host=65.109.75.59
remote_user="root"
command_to_run=""

# Login to remote server and run command
# ssh -t "$remote_user"@"$remote_host" "cd /home/edge-oriented-graph-master-studying/data/VLSP/processed 
#                                         & cp processed/* .
#                                         & ll -ltlh
#                                         & /bin/bash -l"


# ssh -t "$remote_user"@"$remote_host" "cd /home/edge-oriented-graph-master-studying/results/vlsp-test/ && pwd &&  ls -ltlh && rm -r /home/edge-oriented-graph-master-studying/results/vlsp-test/* && ls"

#!/bin/bash

echo "view log downloaded to local ..."

read -p "delete train log? [y/N] " choice
if [[ "$choice" =~ ^[Yy]$ ]]; then
    ssh -t "$remote_user"@"$remote_host" "cd /home/edge-oriented-graph-master-studying/results/vlsp-test/ && pwd &&  ls -ltlh && rm -r /home/edge-oriented-graph-master-studying/results/vlsp-test/* && ls"

  echo "DETELE complete."
else
  echo "DETELE cancelled."
fi
