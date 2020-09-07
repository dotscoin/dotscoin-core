import urllib.request
import settings
from dotscoin.BlockChain import BlockChain
import json

class Election:
    """
        This class holds the nodes election every 30 seconds. A miner is being chosen
        from a list of primary representative.
    """
    def __init__(self):
        self.primary_representatives = dict()
        self.blockchain = BlockChain()
        self.redis_client = self.blockchain.redis_client
        self.fund_addr = "yikgyyf67rr68t887tfc"
        self.redis_client.hmset('fund '+self.fund_addr, {'total fund': 00})

    @staticmethod
    def load_all_nodes():
        """
            Loads all the primary representatives in the network.
        """
        nodes_list = urllib.request.urlopen("https://dns.dotscoin.com/nodes").read()

    def election_fund(self):
        # print(self.redis_client.hget('fund '+self.fund_addr, "total fun"))
        # print(self.redis_client.hmset('fund '+self.fund_addr, {"test2": self.redis_client.hget('fund '+self.fund_addr,"test2") + 2}))
        # if self.redis_client.hget('fund '+self.fund_addr, "test23") == None:
        #     self.redis_client.hmset('fund '+self.fund_addr, {"test23": 2})
        # else:
        #     self.redis_client.hmset('fund '+self.fund_addr, {"test23": self.redis_client.hincrby('fund '+self.fund_addr, "test23", 3463)})

        print(self.redis_client.hget('fund '+self.fund_addr, "test23"))
        i = 1
        while True:
            block = json.loads(self.redis_client.lindex('chain', i).decode('utf-8'))
            if block == None:
                return 
            for tx in block.txs:
                for out in tx.outputs:
                    if out.addr == self.fund_addr:
                        sender_addr = tx.inputs[0].addr
                        if self.redis_client.hget('fund '+self.fund_addr, sender_addr) == None:
                            self.redis_client.hmset('fund '+self.fund_addr, {sender_addr: out.value})
                        else:
                            self.redis_client.hmset('fund '+self.fund_addr, {sender_addr: self.redis_client.hincrby('fund '+self.fund_addr, sender_addr, out.value)})
            i = i+1
        return






