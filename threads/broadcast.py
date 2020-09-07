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
    print(nodes.json()['nodes'])

udpsock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udpsock.bind((host,port))

def broadcast(data,host,port):
    udpsock.sendto(data.encode('utf-8'),(host,port))

#reciever 
def reciever():
    context = zmq.Context()
    z1socket = context.socket(zmq.REP)
    z1socket.bind("tcp://127.0.0.1:5558")
    while True:
        # print("r")
        data = json.loads(z1socket.recv_string())
        print(data)
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