
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
# pip install --target=$nb_path numpy==1.21.6              
pip install --target=$nb_path numpy==1.21.6              
pip install --target=$nb_path networkx
pip install --target=$nb_path yamlordereddictloader
pip install --target=$nb_path recordtype
pip install --target=$nb_path jupyter_beeper

# Command 3 - Changing directory
cd /home/edge-oriented-graph-master-studying/src

# Command 4 - Running script
# sh run.sh

echo -e '------------ init done ------------'
echo -e '>>> Please copy newest data 100% FILTERED to data/processed/VLSP'
echo -e 'vlsp_100_copy_to_server.sh'

