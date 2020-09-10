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
from threads.broadcast import broadcaster
from dotscoin.Address import Address
def rpc_mining():
    rpc=threading.Thread(target=rpc_receive)
    mining=threading.Thread(target=run_thread)
    mining.daemon=True
    rpc.daemon=True
    rpc.start()
    mining.start()
    rpc.join()
    mining.join()
def broadcast_receive():
    broadcast=threading.Thread(target=broadcaster)
    reciever=threading.Thread(target=broadcast_receive)
    broadcast.daemon=True
    reciever.daemon=True
    broadcast.start()
    reciever.start()
    broadcast.join()
    reciever.join()
def add_my_node(my_node):
    body = json.dumps(my_node).encode('utf-8')
    url = "http://dns.dotscoin.com/add_node"
    headers = {'Content-Type':'application/json'}
    req = urllib.request.Request(url, body, headers) 
    try:
        response = urllib.request.urlopen(req).read()
        result = response
        print(result) 
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        print(json.loads(error.read()))  

def get_all_nodes():
    url = "http://dns.dotscoin.com/get_nodes"
    try:
        response = urllib.request.urlopen(url)
        result = response.read()
        print(result) 
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        print(json.loads(error.read()))
    return result

def store_nodes(all_nodes):
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    redis_client.rpush("nodes", json.dumps(all_nodes.decode('utf-8')))
    # print(redis_client.hgetall("nodes"))

def node_start():
    with open("this_node_data.json", 'r') as json_file:
        my_node = json.load(json_file)
    if my_node == {}:
        response = urllib.request.urlopen("https://checkip.amazonaws.com/").read()
        self_ip_addr = response.decode("utf-8").strip()
        add = Address()
        my_node = {
            "node_addr": add.get_public_address(),
            "ip_addr": self_ip_addr, 
            "receiver_port": settings.UDP_RECEIVER_PORT,
            "rpc_port": settings.RPC_PORT,
        }
        with open("this_node_data.json", 'w') as out_file:
            out_file.write(json.dumps(my_node))
    else:
        pass
    
    print(my_node)
    add_my_node(my_node)
    all_nodes = get_all_nodes()
    store_nodes(all_nodes)

    
node_start()
process1= multiprocessing.Process(target=rpc_mining)
process2= multiprocessing.Process(target=broadcast_receive)
process1.start()
process2.start()
