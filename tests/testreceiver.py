import socket

sock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(('0.0.0.0',6500))
sock.sendto("hello".encode('utf-8'),('34.122.30.88', 9000))