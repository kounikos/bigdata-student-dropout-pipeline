import subprocess
from subprocess import Popen


with Popen(["start-all.sh"], stdout=subprocess.PIPE, shell=True, universal_newlines=True) as p1:
    print(p1.communicate())

with Popen(["zookeepersrv"], stdout=subprocess.PIPE, shell=True, universal_newlines=True) as p2:
    print(p2.communicate())

with Popen(["kafkasrv"], stdout=subprocess.PIPE, shell=True, universal_newlines=True) as p3:
    print(p3.communicate())