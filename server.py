import socket
import selectors
import types
import os
import multiprocessing 
import time
from threads.receiver import *  
from threads.rpc import rpc_receive
from threads.election import run_thread
from threads.broadcast import reciever
host = '0.0.0.0'
port = 8080

cpucount = os.cpu_count()
print("total cpu cores in the system=",cpucount)
if cpucount < 4:
    print("this version of software can't run on your system")
    exit()

time.sleep(5)
rpc=multiprocessing.Process(target=rpc_receive)
rpc.start()
receiver=multiprocessing.Process(target=broadcast_receive)
receiver.start()
broadcast_process=multiprocessing.Process(target=reciever)
broadcast_process.start()
election_process = multiprocessing.Process(target=run_thread)
election_process.start()
