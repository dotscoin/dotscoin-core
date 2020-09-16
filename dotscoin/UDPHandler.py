from dotscoin.Transaction import Transaction
from dotscoin.Mempool import Mempool
import zmq
import json
import settings
import socket
import redis
import time
from dotscoin.TimeServer import TimeServer

class UDPHandler:
    def __init__(self):
        command_mapping = {
            "castvote": self.castvote,
            "getchainlength": self.getchainlength,
            "getblockbyheight": self.getblockbyheight,
            "getmempoollength": self.getmempoollength,
            "gettxbymindex": self.gettxbymindex,
            "sendtransaction": self.sendtransaction,
            "sendblock": self.sendblock,
            "getallmtxhash": self.getallmtxhash,
            "gettxbyhash": self.gettxbyhash,
            "synctime": self.synctime,
            "gettime": self.gettime
        }

    @staticmethod
    def sendmessage(message, sender_ip, sender_port):
        host = '0.0.0.0'
        port = settings.UDP_BROADCAST_PORT
        udpsock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        udpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udpsock.bind((host,port))
        udpsock.sendto(message.encode('utf-8'),(sender_ip, sender_port))
        udpsock.close()

    @staticmethod
    def broadcastmessage(message):
        host = '0.0.0.0'
        port = settings.UDP_BROADCAST_PORT
        udpsock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        udpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udpsock.bind((host,port))
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        for ip_addr, raw_data in redis_client.hgetall("nodes_map"):
            data = json.loads(raw_data)
            print(data)
            udpsock.sendto(message.encode('utf-8'),(ip_addr, data["receiver_port"]))
        udpsock.close()
    
    def castvote(self,data):
       pass
    
    def getchainlength(self,data):
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        return redis_client.llen("chain")

    def getblockbyheight(self,data):
        return

    def getmempoollength(self,data):
        return
    
    def gettxbymindex(self,data):
        return
    
    def sendtransaction (self,data):
        tx = Transaction.from_json(data['body'])
        UDPHandler.broadcastmessage(json.dumps(tx.to_json()))

    def getallmtxhash(self, response=None):
        if response is None:
            UDPHandler.broadcastmessage(json.dumps({
                "command": "getallmtxhash"
            }))
        else:
            redis_client = redis.Redis(host='localhost', port=6379, db=0)
            local_tx_hashes: set = set()
            remote_tx_hashes: set = set()

            for tx in redis_client.lrange("mempool", 0, -1):
                local_tx_hashes.add(Transaction.from_json(tx.decode("utf-8")).hash)
            
            response_data = json.loads(response)
            for tx in response_data["hashes"]:
                remote_tx_hashes.add(tx)
            
            remote_tx_hashes.difference_update(local_tx_hashes)

            receiver_port = settings.UDP_RECEIVER_PORT
            for raw in redis_client.lrange("nodes", 0, -1):
                info = json.loads(raw.decode("utf-8"))
                if info["ip_addr"] == response_data["ip_addr"]:
                    receiver_port = info["receiver_port"]
            
            for tx_hash in remote_tx_hashes:
                self.gettxbyhash({
                    "hash": tx_hash,
                    "ip_addr": response_data["ip_addr"],
                    "receiver_port": receiver_port
                })


    def gettxbyhash(self, request=None, response=None):
        if request is not None:
            UDPHandler.sendmessage(json.dumps({
                "hash": request["hash"]
            }), request["ip_addr"], request["receiver_port"])
        elif response is not None:
            mempool = Mempool()
            mempool.add_transaction(Transaction.from_json(json.loads(response)["tx"]))

    def synctime(self, request=None, response=None):
        if response is None:
            UDPHandler.sendmessage(json.dumps({
                "command": "synctime",
                "timestamp": time.time()
            }), request["ip_addr"], request["receiver_port"])
        else:
            raw = json.loads(response)
            redis_client = redis.Redis(host='localhost', port=6379, db=0)
            current_timestamp = time.time()
            redis_client.set("delay_time", (current_timestamp - int(raw["timestamp"])) / 2)

    def gettime(self, request=None, response=None):
        ts = TimeServer()
        if response is not None:
            raw = json.loads(response)
            redis_client = redis.Redis(host='localhost', port=6379, db=0)
            ts.set_time(int(raw["timestamp"]) + int(redis_client.get("delay_time")))
