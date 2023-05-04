#!/bin/bash
source .env
REMOTE_SERVER=$HOST_IP


# REMOTE_SERVER=65.109.75.59
remote_user="root"

#!/bin/bash

LOCAL_FOLDER_2=/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/data/VLSP/processed
REMOTE_FOLDER_2=/home/edge-oriented-graph-master-studying/data/VLSP/processed

rsync -avz --exclude="*.pyc" --exclude="__pycache__" "${LOCAL_FOLDER_2[@]}" "$remote_user"@"$REMOTE_SERVER":"$REMOTE_FOLDER_2"
