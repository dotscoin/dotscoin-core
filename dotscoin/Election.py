import urllib.request
import settings
from dotscoin.BlockChain import BlockChain
import json
from collections import defaultdict
import random
import zmq

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
        self.this_node_addr = "addr1"
        self.stakes = dict()
        self.votes = dict()

    # @staticmethod
    # def load_all_nodes():
    #     """
    #         Loads all the primary representatives in the network.
    #     """
    #     nodes_list = urllib.request.urlopen("https://dns.dotscoin.com/nodes").read()

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

    def get_stakes(self, fetched_stakes):
        self.stakes = fetched_stakes
        self.vote_to()

    def vote_to(self):
        total_stake = 0
        arr = []
        for key, val in self.stakes.items():
            total_stake += val
            for i in range(0, val):
                arr.append(key)
        select = arr[random.randint(0, total_stake-1)]
        while select == self.this_node_addr:
            select = arr[random.randint(0, total_stake - 1)]
        # add your vote to this node's this election's votes array
        self.votes.update({self.this_node_addr, select})
        # Broadcast the selected node
        context = zmq.Context()
        z2socket = context.socket(zmq.REQ)
        z2socket.connect("tcp://127.0.0.1:5008")
        z2socket.send_string(select)
        message = z2socket.recv()
        z2socket.close()
        return 

    # def get_vote(self):
    #     #recieve the vote of other nodes
    #     context = zmq.Context()
    #     z3socket = context.socket(zmq.REP)
    #     z3socket.bind("tcp://127.0.0.1:5009")
    #     while True:
    #         vote_data = json.loads(z3socket.recv_string())
    #         z3socket.send_string("got some nodes vote")

    #     for key, val in self.votes.items():
    #         if key == voter_addr:
    #             return
    #     self.votes.update({voter_addr, voted_addr})

    #     return

    def delegates(self):
        votes_count = defaultdict(int)
        for key, val in self.votes.items():
            votes_count[val] += 1
        votes_count = sorted(votes_count.items(), key=lambda kv:(kv[1], kv[0]))
        dels = []
        if len(votes_count) > 10 :
            dels = list(reversed(list(votes_count)))[0:10]
        else :
            dels = list(reversed(list(votes_count)))
        return dels






