import socket
import os
import json
import hashlib

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024

# the ip address or hostname of the server, the receiver
host = "34.74.0.126"
# the port, let's use 5001
port = 5001
# the name of file we want to send, make sure it exists
filename = "tests/test.mp4"
# get the file size
filesize = os.path.getsize(filename)

# create the client socket
s = socket.socket()

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

# json object
info = {
    "filename" : filename,
    "filesize" : filesize,
    "filetype" : "temp",
    "filehash" : "fxsrysyws55ws57e",
    "fileaddr" : "104.196.106.117",
 }

# send the filename and filesize
s.sendall(pickle.dumps(info))
# s.sendall(f"{filename}{SEPARATOR}{filesize}{SEPARATOR}{'temp'}{SEPARATOR}{'fxsrysyws55ws57e'}{SEPARATOR}{'104.196.106.117'}".encode('utf-32'))

# start sending the file
# progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in 
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        # progress.update(len(bytes_read))
# close the socket
s.close()

# # Importing libraries
# import socket
# import sys

# # Lets catch the 1st argument as server ip
# if (len(sys.argv) > 1):
#     ServerIp = sys.argv[1]
# else:
#     print("\n\n Run like \n python3 client.py < serverip address > \n\n")
#     exit(1)


# # Now we can create socket object
# s = socket.socket()

# # Lets choose one port and connect to that port
# PORT = 9898

# # Lets connect to that port where server may be running
# s.connect((ServerIp, PORT))

# # We can send file sample.txt
# file = open("/home/rishav4101/12345.mkv", "rb")
# SendData = file.read(1024)


# while SendData:
#     # Now we can receive data from server
#     print("\n\n################## Below message is received from server ################## \n\n ", s.recv(1024).decode("utf-8"))
#     #Now send the content of sample.txt to server
#     s.send(SendData)
#     SendData = file.read(1024)      

# # Close the connection from client side
# s.close()

def file_split(filename, n):
    file_list = []
    filesize = os.path.getsize(filename)
    SPLIT_SIZE = filesize / n
    with open(filename, "rb") as f:
        i = 0
        while True:
            bytes_read = f.read(SPLIT_SIZE)
            if not bytes_read:
                break
            hash = hashlib.sha256(json.dumps(bytes_read).encode("utf-8")).hexdigest()
            file_list.append({"index": i, "key" : hash, "value": bytes_read})
            i = i + 1
    
    for i in range(0,n):
        filename = "output" + i + ".mkv"
        with open(filename, "wb") as f:
            f.write(file_list[i].value)

def file_join(file_list):
    filename = "output.txt"
    for file in file_list.items():
        with open(filename, "wb") as f:
            while True:
                bytes_read = file.value
                if not bytes_read:    
                    break
                f.write(bytes_read)
    
