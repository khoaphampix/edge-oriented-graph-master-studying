from fabric.api import *

# from fabric.operations import *
# from fabric.transfer import *
# from fabric import task
# from fabric.context_managers import lcd



# the user to use for the remote commands
# the servers where the commands are executed
# env.use_ssh_config = True
hosts = ['65.109.75.59']
user = 'root'
# env.path = '/home/edge-oriented-graph-master-studying'
path = \
"/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying"
import time
import os

def pack():
    """pack the . from local dir"""
    # create local tar archive
    local(
        """tar -zcf edge-oriented-graph-master-studying.tgz --exclude='*.pyc' --exclude='*.log' --exclude='env'--exclude='__pycache__' --exclude='.git' 
         --exclude='data'
         --exclude='embeds'
         --exclude='data_processing'
         --exclude='dataProcessingOfficialCleaned'
         --exclude='evaluation'
         --exclude='PhoBERT_base_fairseq'
         --exclude='results'
         --exclude='statistic_result'
         --exclude='results'
        --exclude='LICENSE'
        --exclude='network.svg'
        --exclude='README_preprocess_data.md'
        --exclude='README.md'
        --exclude='ScriptRun.ipynb'
        --exclude='.gitignore' 
        edge-oriented-graph-master-studying""" % env)


def upload():
    put('edge-oriented-graph-master-studying.tgz', '/tmp/edge-oriented-graph-master-studying.tgz')


# def change_mode():
#     run('sudo chmod 777 /home/edge-oriented-graph-master-studying/edge-oriented-graph-master-studying/debug.log*')


def unpack():
    run('tar -xzf /tmp/edge-oriented-graph-master-studying.tgz -C /home/edge-oriented-graph-master-studying')


@task
def deploy(environment='65.109.75.59'):
    with lcd(path):
        host = [environment]
        pack()
        """scp the archive and unpack"""
        execute(upload, hosts=host)
        execute(unpack, hosts=host)
        
        # #execute(start_redis_queue, hosts=host)
        execute(cleanup, hosts=host)
        local_cleanup()


def local_cleanup():
    local('rm edge-oriented-graph-master-studying.tgz' % env)


def cleanup():
    run('rm /tmp/edge-oriented-graph-master-studying.tgz' % env)
