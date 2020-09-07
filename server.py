import socket
import selectors
import types
import os
import multiprocessing
from threads.broadcast import *  
from threads.receiver import *  
from threads.rpc import rpc_receive
host = '0.0.0.0'
port = 8080

cpucount = os.cpu_count()
print("total cpu cores in the system=",cpucount)
if cpucount < 4:
    print("this version of software can't run on your system")
    exit()
rpc=multiprocessing.Process(target=rpc_receive)
rpc.start()
receiver=multiprocessing.Process(target=broadcast_receive)
receiver.start()
