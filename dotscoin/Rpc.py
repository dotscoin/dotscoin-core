import json
import redis
from dotscoin.Mempool import Mempool
from dotscoin.Transaction import Transaction
from dotscoin.Address import Address
from threads.broadcast import broadcast

class Rpc:
    
    def __init__(self):
        super().__init__()
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def addTransaction(self,data):
        tx = Transaction.from_json(data['data'])
        mempool = Mempool()
        mempool.add_transaction(tx)
        broadcast(tx)
        return 
    
    def getlastblock(self,data):
        return self.redis_client.lindex('chain', -1)

    def getaddressbalance(self,data):
        addr = Address()
        return addr.total_value(data["data"])
    
    def getblockbyheight(self,data):
        return self.redis_client.lindex('chain', data["data"])
    
    def gettxsbyaddress(self,data):
        tran = Transaction()
        return tran.txs_by_addr(data["data"])
    
    def getnodeinfo(self,data):
        with open("this_node_data.json", 'r') as json_file:
            my_node = json.load(json_file)
        return my_node

    def getstakes(self,data):
        fetch_stakes_bytes = self.redis_client.hgetall('fund '+self.fund_addr)
        fetch_stakes = { y.decode('ascii'): fetch_stakes_bytes.get(y).decode('ascii') for y in fetch_stakes_bytes.keys() }
        self.stakes = fetch_stakes
        return fetch_stakes

    def gettxbyhash(self,data):
        tran = Transaction()
        return tran.tx_by_hash(data["data"])
        