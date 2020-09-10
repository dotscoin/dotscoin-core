import sys
import time
from datetime import datetime
import socket
import threading
import requests
import zmq
import json
import redis
import urllib.request
import settings


INVALID_DATA=False

def get_nodes():
    response = urllib.request.urlopen("http://dns.dotscoin.com/get_nodes").read()
    return json.loads(response)['nodes']

def broadcast(data):
    host = '0.0.0.0'
    port = settings.UDP_BROADCAST_PORT
    udpsock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udpsock.bind((host,port))
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    i = 0
    while True:
        node = redis_client.lindex('nodes', i).decode('utf-8')
        if node == None:
            return
        udpsock.sendto(json.dumps(data).encode('utf-8'),(node.ip_addr, node.receiver_port))
        i = i + 1
    udpsock.close()


# #reciever 
# def broadcaster():
#     print("Starting Broadcast Process")
#     context = zmq.Context()
#     z1socket = context.socket(zmq.REP)
#     z1socket.bind("tcp://127.0.0.1:%s" % settings.BROADCAST_ZMQ_PORT)
#     while True:
#         data = json.loads(z1socket.recv_string())
#         print(data)
#         broadcast(data)
#         z1socket.send_string("recieved")