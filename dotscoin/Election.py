from dotscoin.BlockChain import BlockChain
from dotscoin.Verification import Verification
from dotscoin.Transaction import Transaction
from dotscoin.Block import Block
import redis
import urllib.request
import json
import random
import zmq
import settings
from collections import defaultdict

class Election:
    """
        This class holds the nodes election every 30 seconds. A miner is being chosen
        from a list of primary representative.
    """
    def __init__(self):
        self.primary_representatives = dict()
        self.blockchain = BlockChain()
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.fund_addr = ""
        self.redis_client.hmset('fund '+self.fund_addr, {'total fund': 00})
        self.this_node_addr = "addr1"
        self.stakes = dict()
        self.votes = dict()
        self.verification =  Verification()
        self.load_election_fund_details()

    def load_election_fund_details(self):
        f = open('electionfund.json',) 
        data = json.load(f)
        self.fund_addr = data["address"]

    def get_node_addr(self):
        response = urllib.request.urlopen("https://checkip.amazonaws.com/").read()
        self.this_node_addr = response.decode("utf-8").strip()


    # @staticmethod
    # def load_all_nodes():
    #     """
    #         Loads all the primary representatives in the network.
    #     """
    #     nodes_list = urllib.request.urlopen("https://dns.dotscoin.com/nodes").read()

    def election_fund_initial(self):
        # print(self.redis_client.hget('fund '+self.fund_addr, "test234"))
        # # print(self.redis_client.hmset('fund '+self.fund_addr, {"test2": self.redis_client.hget('fund '+self.fund_addr,"test2") + 2}))
        # if self.redis_client.hget('fund '+self.fund_addr, "test234") == None:
        #     self.redis_client.hmset('fund '+self.fund_addr, {"test234": 2})
        # else:
        #     self.redis_client.hmset('fund '+self.fund_addr, {"test234": self.redis_client.hincrby('fund '+self.fund_addr, "test234", 3463)})

        # print(self.redis_client.hget('fund '+self.fund_addr, "test23"))

        #chain scan 
        chain_length = self.redis_client.llen('chain')
        i = 0
        while i < chain_length:
            raw = json.loads(self.redis_client.lindex('chain', i).decode('utf-8'))
            print(raw)
            block = Block.from_json(raw)
            if block == None:
                return 
            for tx in block.transactions:
                print(Transaction.to_json(tx))
                for out in tx.outputs:
                    if out.address == self.fund_addr:
                        sender_addr = tx.inputs[0].address
                        # print(sender_addr)
                        if self.redis_client.hget('fund '+self.fund_addr, sender_addr) == None:
                            self.redis_client.hmset('fund '+self.fund_addr, {sender_addr: out.value})
                        else:
                            self.redis_client.hmset('fund '+self.fund_addr, {sender_addr: self.redis_client.hincrby('fund '+self.fund_addr, sender_addr, out.value)})
            i = i + 1
        return 

    def get_stakes(self):
        self.election_fund_initial()
        fetch_stakes_bytes = self.redis_client.hgetall('fund '+self.fund_addr)
        print(fetch_stakes_bytes)
        fetch_stakes = { y.decode('ascii'): fetch_stakes_bytes.get(y).decode('ascii') for y in fetch_stakes_bytes.keys() }
        print(fetch_stakes)
        self.stakes = fetch_stakes

    def vote_to(self):
        total_stake = 0
        arr = []
        for key, val in self.stakes.items():
            total_stake += int(val)
            for i in range(0, int(val)):
                arr.append(key)
        self.redis_client.hmset('fund '+self.fund_addr, {"total fund": total_stake})
        if total_stake == 0:
            return
        select = arr[random.randint(0, total_stake-1)]
        while select == self.this_node_addr:
            select = arr[random.randint(0, total_stake - 1)]
        # add your vote to this node's this election's votes array
        self.votes[self.this_node_addr] = select
        # Broadcast the selected node to vote
        context = zmq.Context()
        z2socket = context.socket(zmq.REQ)
        z2socket.connect("tcp://127.0.0.1:%s" % settings.BROADCAST_ZMQ_PORT)
        z2socket.send_string(json.dumps({'data':{"voter_addr":self.this_node_addr, "voted_addr":select},'command': 'voteto'}))
        message = z2socket.recv()
        print(message)
        z2socket.close()
        return 

    def add_vote(self, vote):
        self.votes.update(vote)

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

    # def run_election(self):
    #     self.get_stakes()
    #     self.vote_to()
    #     self.get_vote()
    #     dels = self.delegates()

    #     for dele in dels:
    #         if dele == self.this_node_addr:
    #             blk = Block()
    #             for i in range(0,20):
    #                 tx = self.redis_client.lindex('mempool', i).decode('utf-8')
    #                 if tx == None:
    #                     break
    #                 verify_verdict = self.verification.verify_tx(tx)
    #                 if verify_verdict == "verified":
    #                     #map to blk/create block
    #                     blk.add_transaction(tx)
    #                 else:
    #                     i =  i - 1
    #                     continue
    #             #add block
    #             blkChain = blockchain()
    #             blkChain.add_block(blk)

    #             #full blockchain verify
    #             full_verify_message = self.verification.full_chain_verify()
    #             if full_verify_message == "verified": 
    #                 pass
    #             else:
    #                 return