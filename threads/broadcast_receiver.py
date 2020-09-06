import sys
import time
from datetime import datetime
import socket
import threading
import requests
host = '0.0.0.0'
port = 6040
def get_nodes():
    base_url="http://dns.dotscoin.com/get_nodes/"
    nodes = requests.get(base_url)
    print(nodes)
    print(nodes.json()['nodes'])

get_nodes()

class UDPBroadcastReceiveServer():
    def __init__(self, host, port):

        self.host = host    # Host address
        self.port = port    # Host port
        self.sock = None    # Socket
    def printwt(self, msg):

        ''' Print message with current date and time '''
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{current_date_time}] {msg}')
    def configure_server(self):
        self.printwt('Creating socket...')
        self.printwt('Socket created')
        # bind server to the address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host,port))
        self.printwt(f'Binding server to {self.host}:{self.port}...')
        self.printwt(f' Broadcasting and Receiving Server binded to {self.host}:{self.port}')
    def get_phone_no(self, name):

        ''' Get phone no for a given name '''
        phonebook = {'Alex': '1234567890', 'Bob': '1234512345'}
        if name in phonebook.keys():
            return f"{name}'s phone number is {phonebook[name]}"


        else:
            return f"No records found for {name}"
    def handle_request(self, data, client_address):

        ''' Handle the client '''
        # handle request

        name = data.decode('utf-8')
        self.printwt(f'[ REQUEST from {client_address} ]')
        print('\n', name, '\n')
        # send response to the client
        resp = self.get_phone_no(name)

        time.sleep(3)
        self.printwt(f'[ RESPONSE to {client_address} ]')
        self.sock.sendto(resp.encode('utf-8'), client_address)
        print('\n', resp, '\n')
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

    def __init__(self, host, port):
        super().__init__(host, port)
        self.socket_lock = threading.Lock()
    
    def handle_request(self, data, client_address):
        # handle request
        name = data.decode('utf-8')
        resp = self.get_phone_no(name)
        self.printwt(f'[ REQUEST from {client_address} ]')
        print('\n', name, '\n')

        # send response to the client
        self.printwt(f'[ RESPONSE to {client_address} ]')
        with self.socket_lock:
            self.sock.sendto(resp.encode('utf-8'), client_address)
        print('\n', resp, '\n')

    def wait_for_client(self):
        ''' Wait for clients and handle their requests '''

        try:
            while True: # keep alive

                try: # receive request from client
                    data, client_address = self.sock.recvfrom(1024)

                    c_thread = threading.Thread(target = self.handle_request,
                                            args = (data, client_address))
                    c_thread.daemon = True
                    c_thread.start()

                except OSError as err:
                    self.printwt(err)

        except KeyboardInterrupt:
            self.shutdown_server()

def broadcast_receive():
    udp = UDPServerMultiClient(host,port)
    udp.configure_server()
    udp.wait_for_client()