import json
import socket

class TestUdp():

    def test_ping(self):
        host = '0.0.0.0'
        port = 4200
        udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udpsock.bind((host, port))
        udpsock.sendto(json.dumps({
                 "command": "ping",
                 "body": {}
             }).encode('utf-8'), ("34.68.253.117", 6500))
        udpsock.close()

if __name__ == '__main__':
    tup = TestUdp()
    tup.test_ping()