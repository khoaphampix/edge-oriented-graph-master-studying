
#!/bin/bash

cd /home

sudo apt-get update 
sudo apt install python3-pip -y
sudo apt-get install zip -y


git clone https://github.com/khoaphampix/edge-oriented-graph-master-studying.git
cd /home/edge-oriented-graph-master-studying
git checkout dev-low-memory


# Command 2 - Installing dependencies
pip3 install -r /home/edge-oriented-graph-master-studying/requirements.txt


# Command 3 - Changing directory
cd /home/edge-oriented-graph-master-studying/src

# Command 4 - Running script
sh run.sh
