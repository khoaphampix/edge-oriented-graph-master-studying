#!/bin/bash
?????
print a
source ../.env
# remote_host=$HOST_IP
# Variables
# REMOTE_HOST=$HOST_IP
# REMOTE_USER=root
OLD_VALUE="ClientAliveInterval 60"
NEW_VALUE="ClientAliveInterval 120"

# SSH command to replace the old value with the new value
ssh ${REMOTE_USER}@${REMOTE_HOST} "sudo sed -i 's/${OLD_VALUE}/${NEW_VALUE}/g' /etc/ssh/sshd_config"

# Restart SSH daemon on remote server
ssh ${REMOTE_USER}@${REMOTE_HOST} "sudo systemctl restart sshd"
