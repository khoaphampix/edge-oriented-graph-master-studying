#!/bin/bash

# set variables
# REMOTE_HOST=65.109.75.59
source .env
REMOTE_HOST=$HOST_IP

REMOTE_USER="root"
REMOTE_PATH="/home/edge-oriented-graph-master-studying/results/vlsp-test-new"
LOCAL_PATH="/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/result_from_colab/FILTERED_1st_full_dataset_100_percent"

# create temporary file with timestamp
NOW=$(date +"%Y-%m-%d_%H-%M-%S")
TEMP_FILE="$REMOTE_PATH/temp_$NOW.zip"

# zip remote folder to temporary file
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && zip -r $TEMP_FILE *"

# download temporary file to local folder
scp $REMOTE_USER@$REMOTE_HOST:$TEMP_FILE $LOCAL_PATH


# rename local file with timestamp
mv $LOCAL_PATH/temp_$NOW.zip $LOCAL_PATH/temp_$NOW.zip
unzip $LOCAL_PATH/temp_$NOW.zip -d $LOCAL_PATH/temp_$NOW/
rm $LOCAL_PATH/temp_$NOW.zip


# remove temporary file on remote server
ssh $REMOTE_USER@$REMOTE_HOST "rm $TEMP_FILE"
