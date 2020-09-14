import socket
import os
import settings 
import hashlib
import math
from StorageTx import StorageTx
from Mempool import Mempool

SERVER_HOST = settings.NODE_IP
SERVER_PORT = settings.FILE_RECV_PORT

BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

def start():
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    while True:
        client_socket, address = s.accept() 
        print(f"[+] {address} is connected.")
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize, filetype, filehash, fileaddr = received.split(SEPARATOR)
        if filetype == "temp":
            filename = os.path.basename(settings.TEMP_STORAGE_PATH + filename)
        else:
            filename = os.path.basename(settings.STORAGE_PATH + filename)
        filesize = int(filesize)

        with open(filename, "wb") as f:
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:    
                    break
                f.write(bytes_read)

        # client_socket.close()

        if filetype == "temp":
            #split and broadcast
            file_split(filename,4)
            file_send(4, filehash, fileaddr)
            #create transaction
            #store to Mempool
            #broadcast transaction
            client_socket.close()
            
        else:
            with open(filename,"rb") as f:
                bytes = f.read() # read entire file as bytes
                readable_hash = hashlib.sha256(bytes).hexdigest()
                print(readable_hash)
            client_socket.send(readable_hash.encode('utf-8'))
            #calulate CID and send
            client_socket.close()
            

# def store(filename):
#     file = os.path.basename(settings.STORAGE_PATH + filename)
#     with open(file,"rb") as f:
#         bytes = f.read() # read entire file as bytes
#         readable_hash = hashlib.sha256(bytes).hexdigest()
#         print(readable_hash)

def file_split(filename, n):
    file_list = []
    filesize = os.path.getsize(filename)
    SPLIT_SIZE = math.ceil(filesize / n)
    with open(filename, "rb") as f:
        i = 0
        while True:
            bytes_read = f.read(SPLIT_SIZE)
            if not bytes_read:
                break
            # hash = hashlib.sha256(json.dumps(bytes_read).encode("utf-8")).hexdigest()
            file_list.append(bytes_read)
            i = i + 1
    
    for i in range(0,n):
        filename = settings.TEMP_STORAGE_PATH + "output" + str(i) + ".format"
        with open(filename, "wb") as f:
            f.write(file_list[i])

def file_send(n, filehash, fileaddr):
    stx = StorageTx()
    mem = Mempool()
    stx.add_input(filehash,fileaddr)
    for i in range(0,n):
        host = "rcv host"
        port = "rcv port"

        filename = settings.TEMP_STORAGE_PATH + "output" + str(i) + ".format"
        filesize = math.ceil(os.path.getsize(filename))
        filetype = "non-temp"
        
        send = socket.socket()
        print(f"[+] Connecting to {host}:{port}")
        send.connect((host, port))
        print("[+] Connected.")
        
        send.send(f"{filename}{SEPARATOR}{filesize}{SEPARATOR}{filetype}".encode())
        with open(filename, "rb") as f:
            bytes = f.read() # read entire file as bytes
            genhash = hashlib.sha256(bytes).hexdigest()
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                send.sendall(bytes_read)
        filehash = send.recv(BUFFER_SIZE).decode('utf-8')
        if genhash == filehash:
            stx.add_output(filehash, host)
        else:
            return "tx error"
        send.close()
        
    stx.gen_tx_hash()
    mem.add_transaction(stx.to_json())
    #stx.broadcast


        
            