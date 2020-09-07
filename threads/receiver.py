
import sys
import time
from datetime import datetime
import socket
import threading
import requests
import json
host = '0.0.0.0'
port = 7000
sock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((host,port))
INVALID_DATA=False
def response_handler(data):
    keys=['index','data','command']

    for key in keys:
        if not key in data.keys():
            INVALID_DATA =True       
    if INVALID_DATA:
        response = {
        "error":"invaid type of data"
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
   
    def handle_request(self, data, client_address):

        ''' Handle the client '''
        # handle request

        data= data.decode('utf-8')
        self.printwt(f'[ REQUEST from {client_address} ]')
        print('\n', data, '\n')
        
        response = response_handler(data)

        time.sleep(3)
        self.printwt(f'[ RESPONSE to {client_address} ]')
        self.sock.sendto(response.encode('utf-8'), client_address)
        print('\n', response, '\n')
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
        data= data.decode('utf-8')
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
    udp = UDPServerMultiClient()
    udp.configure_server()
    udp.wait_for_client()


