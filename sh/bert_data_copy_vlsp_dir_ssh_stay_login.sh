#!/bin/bash

source .env
remote_host=$HOST_IP

# remote_host=65.109.75.59
remote_user="root"
command_to_run=""

scp /Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/dataProcessingOfficialCleaned/dev_processed/split_sentence_underthesea/code/BERT_merge_file/data/PubMed-VLSP.txt.zip root@$HOST_IP:/home/edge-oriented-graph-master-studying/embeds/PubMed-VLSP.txt.zip



# Login to remote server and run command
# ssh -t "$remote_user"@"$remote_host" "cd /home/edge-oriented-graph-master-studying/data/VLSP/processed 
#                                         & cp processed/* .
#                                         & ll -ltlh
#                                         & /bin/bash -l"


ssh -t "$remote_user"@"$remote_host" "cd /home/edge-oriented-graph-master-studying/embeds/ && unzip PubMed-VLSP.txt.zip && ls -ltlh "
