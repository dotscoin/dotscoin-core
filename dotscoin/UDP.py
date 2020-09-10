from dotscoin.Transaction import Transaction
from dotscoin.Mempool import Mempool
import zmq
import json
import settings
class UdpHandler:

    def castvote(self,data):
       context = zmq.Context()
       z3socket = context.socket(zmq.REQ)
       z3socket.connect("tcp://127.0.0.1:%s" % settings.ELECTION_ZMQ_PORT)
       z3socket.send_string(json.dumps(data['body']))
       message = z3socket.recv()
       print("vote aaya")
       z3socket.close()
       context.destroy()
    
    def getchainlength(self,data):

        return

    def getblockbyheight(self,data):

        return

    def getmempoollength(self,data):

        return
    
    def gettxbymindex(self,data):

        return
    
    def sendtransaction (self,data):
        tx = Transaction.from_json(data['body'])
        mempool = Mempool()
        mempool.add_transaction(tx)
        
    def sendblock(self,data):
        context = zmq.Context()
        z3socket = context.socket(zmq.REQ)
        z3socket.connect("tcp://127.0.0.1:%s" % settings.ELECTION_ZMQ_PORT)
        z3socket.send_string(json.dumps(data['body']))
        message = z3socket.recv()
        z3socket.close()
        context.destroy()