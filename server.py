# all imports
import socket
import selectors
import types
import os
import redis
import urllib
import urllib.request
import settings
import json
import ast
import multiprocessing 
import time
from threads.receiver import *  
from threads.rpc import rpc_receive
from threads.election import run_thread
from dotscoin.Address import Address
from threads.storage import start
from dotscoin.Node import Node

# Defining host and port to run the main server on
host = '0.0.0.0'
port = 8080

def cpu_count():
    """ Returns CPU count and software compatibility """
    cpucount = os.cpu_count()
    print("total cpu cores in the system=",cpucount)
    if cpucount < 2:
        print("this version of software can't run on your system")
        exit()

def run_threads():
    rpc=multiprocessing.Process(target=rpc_receive)
    rpc.start()
    # receiver=multiprocessing.Process(target=broadcast_receive)
    # receiver.start()
    election_process = multiprocessing.Process(target=run_thread)
    election_process.start()
    storage_process = multiprocessing.Process(target=start)
    storage_process.start()

# def add_my_node(my_node):
#     body = json.dumps(my_node).encode('utf-8')
#     url = "http://dns.dotscoin.com/add_node"
#     headers = {'Content-Type':'application/json'}
#     req = urllib.request.Request(url, body, headers) 
#     try:
#         response = urllib.request.urlopen(req).read()
#         result = response
#         print(result) 
#     except urllib.error.HTTPError as error:
#         print("The request failed with status code: " + str(error.code))
#         print(error.info())
#         print(json.loads(error.read()))  

# def get_all_nodes():
#     url = "http://dns.dotscoin.com/get_nodes"
#     try:
#         response = urllib.request.urlopen(url)
#         result = response.read()
#         print(result) 
#     except urllib.error.HTTPError as error:
#         print("The request failed with status code: " + str(error.code))
#         print(error.info())
#         print(json.loads(error.read()))
#     return result

# def store_nodes(all_nodes):
#     redis_client = redis.Redis(host='localhost', port=6379, db=0)
#     redis_client.rpush("nodes", json.dumps(all_nodes.decode('utf-8')))
#     # print(redis_client.hgetall("nodes"))

def node_start():
    node = Node()
    cpu_count()
    run_threads()
    
if __name__ == '__main__':
    node_start()

        


