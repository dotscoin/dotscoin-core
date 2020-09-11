import json
import redis
from dotscoin.Mempool import Mempool
from dotscoin.Transaction import Transaction
from dotscoin.Address import Address

class RPC:
    #check for type of data sent
    def __init__(self):
        super().__init__()
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.command_mapping = {
            'addtransaction': self.addtransaction,
            'getlastblock': self.getlastblock,
            'getaddressbalance': self.getaddressbalance,
            'getblockbyheight': self.getblockbyheight,
            'gettxbyhash': self.gettxbyhash,
            'getnodeinfo': self.getnodeinfo,
            'getstakes': self.getstakes,
            'gettxsbyaddress': self.gettxsbyaddress
        }

    def handlecommand(self, data):
        pass

    def addtransaction(self, data):
        tx = Transaction.from_json(data['body'])
        mempool = Mempool()
        mempool.add_transaction(tx)
        return json.dumps({
            "status": "ok"
        })
    
    def getlastblock(self, data=None):
        return self.redis_client.lindex('chain', -1).decode("utf-8")

    def getaddressbalance(self, data=None):
        addr = Address()
        return addr.total_value(data["parameters"])
    
    def getblockbyheight(self, data=None):
        return self.redis_client.lindex('chain', data["parameters"]).decode("utf-8")
    
    def gettxsbyaddress(self, data=None):
        tran = Transaction()
        return tran.txs_by_addr(data["parameters"])
    
    def getnodeinfo(self, data=None):
        with open("this_node_data.json", 'r') as json_file:
            my_node = json.load(json_file)
        return json.dumps(my_node)

    def getstakes(self, data=None):
        fetch_stakes_bytes = self.redis_client.hgetall('fund '+self.fund_addr)
        fetch_stakes = { y.decode('ascii'): fetch_stakes_bytes.get(y).decode('ascii') for y in fetch_stakes_bytes.keys() }
        self.stakes = fetch_stakes
        return fetch_stakes

    def gettxbyhash(self, data=None):
        tran = Transaction()
        return tran.tx_by_hash(data["parameters"])

    def gettxsbyaddress(self, data=None):
        txs = Address.get_transactions_by_address(data["parameters"])

        return json.dumps({
            "txs": txs
        })
        