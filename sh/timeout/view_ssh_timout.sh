#!/bin/bash

source /Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying/sh/.env
remote_host=$HOST_IP
# Variables
REMOTE_HOST=$HOST_IP
REMOTE_USER=root

# ClientAliveInterval
# SSH command to replace the old value with the new value
ssh ${REMOTE_USER}@${REMOTE_HOST} "sudo cat /etc/ssh/sshd_config"
