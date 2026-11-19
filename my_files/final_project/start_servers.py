import subprocess
from subprocess import Popen
import os


def start_servers():
    # Start the servers
    print("Starting servers...")

    with Popen(["start-all.sh"], stdout=subprocess.PIPE, shell=True, universal_newlines=True) as p1:
        print(p1.communicate())

    with Popen(["cd /home/nikos && docker-compose up -d"], stdout=subprocess.PIPE, shell=True, universal_newlines=True) as p2:
        print(p2.communicate())

    with Popen(["gnome-terminal"], stdout=subprocess.PIPE, shell=True, universal_newlines=True) as p3:
        print(p3.communicate())
