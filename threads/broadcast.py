import sys
import time
from datetime import datetime
import socket
import threading
import requests
import zmq
import json
host = '0.0.0.0'
port = 6500
INVALID_DATA=False



def get_nodes():
    base_url="http://dns.dotscoin.com/get_nodes/"
    nodes = requests.get(base_url)
    print(nodes)
    return nodes.json()['nodes']

udpsock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udpsock.bind((host,port))

def broadcast(data):
    # nodes= get_nodes()
    # print(nodes)
    # for node in nodes:
    #   add=node['addr'].split(":")
    #   udpsock.sendto(json.dumps(data).encode('utf-8'),(add[0],int(add[1])))
    #   print("broadcast")
    udpsock.sendto(json.dumps(data).encode('utf-8'),('127.0.0.1', 7000))


#reciever 
def reciever():
    context = zmq.Context()
    z1socket = context.socket(zmq.REP)
    z1socket.bind("tcp://127.0.0.1:5558")
    while True:
        data = json.loads(z1socket.recv_string())
        print("to broadcast")
        broadcast(data)
        z1socket.send_string("recieved")

# def vote_broadcast():
#     context = zmq.Context()
#     z2socket = context.socket(zmq.REP)
#     z2socket.bind("tcp://127.0.0.1:5008")
#     this_node_addr = "dgyuigy97ybvhvoi"
#     while True:
#         vote_to = z2socket.recv_string()
#         print(vote_to)
#         z2socket.send_string("vote recieved and broadcasting")