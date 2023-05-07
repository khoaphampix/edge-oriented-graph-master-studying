#!/bin/bash
source .env
REMOTE_SERVER=$HOST_IP


REMOTE_FOLDER=/home/edge-oriented-graph-master-studying
# REMOTE_SERVER=65.109.75.59
remote_user="root"

# List of local folders to copy
LOCAL_FOLDERS=(
    "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/src" 
    "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/configs" 
    )

# Loop over the list of local folders and copy each one to the remote server
# for folder in "${LOCAL_FOLDERS[@]}"; do
#     scp -r --exclude="$folder/*.pyc"  "$folder" "root@$REMOTE_SERVER:$REMOTE_FOLDER"
# done


rsync -avz --exclude="*.pyc" --exclude="__pycache__" "${LOCAL_FOLDERS[@]}" "$remote_user"@"$REMOTE_SERVER":"$REMOTE_FOLDER"


#!/bin/bash

LOCAL_FOLDER_2=/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/data/VLSP/tunning
REMOTE_FOLDER_2=/home/edge-oriented-graph-master-studying/data/VLSP/tunning

rsync -avz --exclude="*.pyc" --exclude="__pycache__" "${LOCAL_FOLDER_2[@]}" "$remote_user"@"$REMOTE_SERVER":"$REMOTE_FOLDER_2"


ssh -t "$remote_user"@"$remote_host" "cd /home/edge-oriented-graph-master-studying/src && 
            cat /home/edge-oriented-graph-master-studying/configs/parameters_cdr.yaml
            echo -e '\n'
            echo -e '------------'
            cat /home/edge-oriented-graph-master-studying/src/run.sh
            echo -e '\n'
            echo -e '------------'
        "  