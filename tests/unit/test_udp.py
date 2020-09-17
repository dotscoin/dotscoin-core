import unittest
import json
from dotscoin.UDPHandler import UDPHandler
from tests.addtransaction import addtransaction

class TestUdp(unittest.TestCase):
    
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
        self.udp.ping(json.dumps({
                "command": "ping"
            }))

if __name__ == '__main__':
    unittest.main()