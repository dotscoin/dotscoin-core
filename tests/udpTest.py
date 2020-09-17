import json
import socket
import settings
from dotscoin.UDPHandler import UDPHandler
from tests.addtransaction import addtransaction

class TestUdp():
    
    udp = UDPHandler()

    def test_getchainlength(self):
        print(self.udp.getchainlength())

    def test_getblockbyheight(self):
        print(self.udp.getblockbyheight({
            "height": 0
        }))

    def test_getmempoollength(self):
        print(self.udp.getmempoollength())

    def test_gettxbymindex(self):
        print(self.udp.gettxbymindex({
            "index": 0
        }))

    def test_sendtransaction(self):
        at = addtransaction()
        print(self.udp.sendtransaction({
            "tx": at.create_tx("tudfvdyivy89liqwhf37f7")
        }))

    def test_ping(self):
        # self.udp.ping(json.dumps({
        #         "command": "ping"
        #     }))
        host = '0.0.0.0'
        port = settings.UDP_BROADCAST_PORT
        udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udpsock.bind((host, port))
        udpsock.sendto(json.dumps({
                 "command": "ping"
             }).encode('utf-8'), ("127.0.0.1", settings.UDP_RECEIVER_PORT))
        udpsock.close()

if __name__ == '__main__':
    tup = TestUdp()
    tup.test_ping()