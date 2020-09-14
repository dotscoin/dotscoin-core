import socket
import tqdm
import os
# device's IP address
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

# create the server socket
# TCP socket
s = socket.socket()

# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# accept connection if there is any
client_socket, address = s.accept() 
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")

# receive the file infos
# receive using client socket, not server socket
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove absolute path if there is
filename = os.path.basename(filename)
# convert to integer
filesize = int(filesize)

# start receiving the file from the socket
# and writing to the file stream
# progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        # write to the file the bytes we just received
        f.write(bytes_read)
        # update the progress bar
        # progress.update(len(bytes_read))

# close the client socket
client_socket.close()
# close the server socket
s.close()



# # Importing socket library 
# import socket

# # Now we can create socket object
# s = socket.socket()

# # Lets choose one port and start listening on that port
# PORT = 9898
# print("\n Server is listing on port :", PORT, "\n")

# # Now we need to bind to the above port at server side
# s.bind(('127.0.0.1', PORT))

# # Now we will put server into listenig  mode 
# s.listen(10)

# #Open one recv.txt file in write mode
# file = open("recv.mkv", "wb") 
# print("\n Copied file name will be recv.txt at server side\n")

# # Now we do not know when client will concatct server so server should be listening contineously  
# while True:
#     # Now we can establish connection with clien
#     conn, addr = s.accept()

#     # Send a hello message to client
#     msg = "\n\n|---------------------------------|\n Hi Client[IP address: "+ addr[0] + "], \n ֲֳ**Welcome to Server** \n -Server\n|---------------------------------|\n \n\n"    
#     conn.send(msg.encode())
    
#     # Receive any data from client side
#     RecvData = conn.recv(1024)
#     while RecvData:
#         file.write(RecvData)
#         RecvData = conn.recv(1024)

#     # Close the file opened at server side once copy is completed
#     file.close()
#     print("\n File has been copied successfully \n")

#     # Close connection with client
#     conn.close()
#     print("\n Server closed the connection \n")

#     # Come out from the infinite while loop as the file has been copied from client.
#     break