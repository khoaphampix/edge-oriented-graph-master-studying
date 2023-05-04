from __future__ import absolute_import

from fabric import task
from fabric import Connection
from fabric.operations import local
from fabric.contrib.project import rsync_project
host = '65.109.75.59'
user = 'root'

@task
def deploy(c):
    # Define variables
    local_path = "/Users/n2t2k/Documents/Studying/Master/Thesis/InProgress/Coding/ORIGIN_RUN_ALL_edge-oriented-graph-master-studying"
    remote_path = "/home/edge-oriented-graph-master-studying"
    excluded_dirs = ["cache", "logs"]
    compressed_filename = "edge-oriented-graph-master-studying.tgz"

    # Compress local folder
    local("""tar czf {0}
        --exclude='*.pyc' --exclude='*.log' --exclude='env'--exclude='__pycache__' --exclude='.git' 
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
          {1}""".format(compressed_filename, local_path))

    # Upload compressed folder to remote server
    conn = Connection(host=host, user=user)
    rsync_project(local_dir='./' + compressed_filename, remote_dir=remote_path, delete=True, exclude=excluded_dirs, connection=conn)

    # Unzip folder on remote server
    with conn.cd(remote_path):
        conn.run("tar xf {0}".format(compressed_filename))

    # Remove compressed folder from local machine
    local("rm -f {0}".format(compressed_filename))
