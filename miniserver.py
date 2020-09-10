from threads.receiver import *  
from threads.rpc import rpc_receive
from threads.election import run_thread
from threads.broadcast import broadcaster
from dotscoin.Address import Address
import multiprocessing 
from server import node_start
import threading


def rpc_mining():
    rpc=threading.Thread(target=rpc_receive)
    mining=threading.Thread(target=run_thread)
    # mining.daemon=True
    # rpc.daemon=True
    rpc.start()
    mining.start()
def broadcast_receive():
    broadcast=threading.Thread(target=broadcaster)
    reciever=threading.Thread(target=broadcast_receive)
    # broadcast.daemon=True
    # reciever.daemon=True
    broadcast.start()
    reciever.start()


process1= multiprocessing.Process(target=rpc_mining)
process2= multiprocessing.Process(target=broadcast_receive)
process1.start()
process2.start()
node_start()