import sys
import time
from datetime import datetime
import socket
import threading
import requests
import json
import zmq
import settings
from dotscoin.Transaction import Transaction
from dotscoin.Mempool import Mempool
from dotscoin.Block import Block
from dotscoin.UDP import UdpHandler

host = '0.0.0.0'
port = settings.UDP_RECEIVER_PORT
sock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
INVALID_DATA=False

def response_handler(data):
    keys=['body','command']
    INVALID_DATA =False

    for key in keys:
        if not key in data.keys():
            INVALID_DATA =True       
    if INVALID_DATA:
        response = {
        "error":"invaid type of data"
        }
        return json.dumps(response)
    else:
        print(data)
        if data['command'] == "sendtransaction":
            udp_handler=UdpHandler()
            udp_handler.sendtransaction(data)
        elif data['command'] == "castvote":
            udp_handler=UdpHandler()
            udp_handler.castvote(data)
        elif data['command'] == "sendblock":
            udp_handler=UdpHandler()
            udp_handler.sendblock(data)
        elif data['command'] == "getblockbyheight":
            udp_handler=UdpHandler()
            udp_handler.getblockbyheight(data)
        elif data['command'] == "getmempoollength":
            udp_handler=UdpHandler()
            udp_handler.getmempoollength(data)
        elif data['command'] == "gettxbymindex":
            udp_handler=UdpHandler()
            udp_handler.gettxbymindex(data)
        elif data['command'] == "getchainlength":
            udp_handler=UdpHandler()
            udp_handler.getchainlength(data)   
        response = {
        "message":"ok"
        }
        return json.dumps(response)
    
class UDPBroadcastReceiveServer():
    sock=sock    # Socket
    def printwt(self, msg):

        ''' Print message with current date and time '''
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{current_date_time}] {msg}')
    def configure_server(self):
        self.printwt('Creating socket...')
        self.printwt('Socket created')
        self.printwt(f'Binding server to {host}:{port}...')
        self.printwt(f' Broadcasting and Receiving Server binded to {host}:{port}')
   
        
    def wait_for_client(self):
        ''' Wait for a client '''
        try:
            # receive message from a client
            data, client_address = self.sock.recvfrom(1024)
            # handle client's request

            self.handle_request(data, client_address)
        except OSError as err:
            self.printwt(err)
    def shutdown_server(self):


        ''' Shutdown the UDP server '''
        self.printwt('Shutting down server...')
        self.sock.close()

class UDPServerMultiClient(UDPBroadcastReceiveServer):
    ''' A simple UDP Server for handling multiple clients '''

    def __init__(self):
        self.socket_lock = threading.Lock()
    
    def handle_request(self, data, client_address):
        # handle request
        data = data.decode('utf-8')
        self.printwt(f'[ REQUEST from {client_address} ]')
        print('\n', data, '\n')
        response = response_handler(json.loads(data))

        # send response to the client
        self.printwt(f'[ RESPONSE to {client_address} ]')
        with self.socket_lock:
            self.sock.sendto(response.encode('utf-8'), client_address)
        print('\n', response, '\n')

    def wait_for_client(self):
        ''' Wait for clients and handle their requests '''
        try:
            while True: # keep alive
                try: # receive request from client
                    data, client_address = self.sock.recvfrom(4096)
                    c_thread = threading.Thread(target = self.handle_request,
                                            args = (data, client_address))
                    c_thread.daemon = True
                    c_thread.start()

                except OSError as err:
                    self.printwt(err)

        except KeyboardInterrupt:
            self.shutdown_server()

def broadcast_receive():
    print("Starting Receiver Process")
    udp = UDPServerMultiClient()
    udp.configure_server()
    udp.wait_for_client()


