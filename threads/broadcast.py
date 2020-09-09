import sys
import time
from datetime import datetime
import socket
import threading
import requests
import zmq
import json
import urllib.request
import settings

host = '0.0.0.0'
port = settings.UDP_BROADCAST_PORT
INVALID_DATA=False

def get_nodes():
    response = urllib.request.urlopen("http://dns.dotscoin.com/get_nodes").read()
    return json.loads(response)['nodes']

udpsock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udpsock.bind((host,port))

def broadcast(data):
    # nodes= get_nodes()
    # print(nodes)
    # for node in nodes:
    #   add=node['addr'].split(":")
    #   udpsock.sendto(json.dumps(data).encode('utf-8'),(add[0],int(add[1])))
    #   print("broadcast")
    udpsock.sendto(json.dumps(data).encode('utf-8'),('34.122.30.88', settings.UDP_RECEIVER_PORT))


#reciever 
def reciever():
    print("Starting Broadcast Process")
    context = zmq.Context()
    z1socket = context.socket(zmq.REP)
    z1socket.bind("tcp://127.0.0.1:%s" % settings.BROADCAST_ZMQ_PORT)
    while True:
        data = json.loads(z1socket.recv_string())
        broadcast(data)
        z1socket.send_string("recieved")