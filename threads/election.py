import urllib.request
import settings
from dotscoin.BlockChain import BlockChain
from dotscoin.Verification import Verification
from dotscoin.Block import Block
import json
from collections import defaultdict
import random
import zmq
import time
import threading

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
        self.verification =  Verification()


    # @staticmethod
    # def load_all_nodes():
    #     """
    #         Loads all the primary representatives in the network.
    #     """
    #     nodes_list = urllib.request.urlopen("https://dns.dotscoin.com/nodes").read()

    def election_fund(self):
        # print(self.redis_client.hget('fund '+self.fund_addr, "test234"))
        # # print(self.redis_client.hmset('fund '+self.fund_addr, {"test2": self.redis_client.hget('fund '+self.fund_addr,"test2") + 2}))
        # if self.redis_client.hget('fund '+self.fund_addr, "test234") == None:
        #     self.redis_client.hmset('fund '+self.fund_addr, {"test234": 2})
        # else:
        #     self.redis_client.hmset('fund '+self.fund_addr, {"test234": self.redis_client.hincrby('fund '+self.fund_addr, "test234", 3463)})

        # print(self.redis_client.hget('fund '+self.fund_addr, "test23"))
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
            i = i + 1
        return 

    def get_stakes(self):
        # self.election_fund()
        fetch_stakes_bytes = self.redis_client.hgetall('fund '+self.fund_addr)
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
        select = arr[random.randint(0, total_stake-1)]
        while select == self.this_node_addr:
            select = arr[random.randint(0, total_stake - 1)]
        # add your vote to this node's this election's votes array
        self.votes.update({self.this_node_addr, select})
        # Broadcast the selected node to vote
        context = zmq.Context()
        z2socket = context.socket(zmq.REQ)
        z2socket.connect("tcp://127.0.0.1:5008")
        z2socket.send_string(json.dumps({"voter_addr":self.this_node_addr, "voted_addr":select}))
        message = z2socket.recv()
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

def worker():
    Election.election_fund()
    Election.get_stakes()
    Election.vote_to()
    context = zmq.Context()
    zsocket = context.socket(zmq.REP)
    zsocket.bind("tcp://127.0.0.1:5009")
    zpoll = zmq.Poller()
    zpoll.register(zsocket)
    start_timestamp = time.time()
    while time.time() - start_timestamp < 14:
        events = dict(zpoll.poll(1))
        for key in events:
            vote = json.loads(key.recv_string())
            print(vote)
            Election.add_vote(vote)
            zsocket.send_string("got some nodes vote")
    zpoll.unregister(zsocket)
    zsocket.close()
    context.destroy()
    return Election.delegates()

def mining():
    dels = worker()
    is_del = False
    for dele in dels:
        if dele == Election.this_node_addr:
            is_del = True
            blk = Block()
            for i in range(0,20):
                tx = Election.redis_client.lindex('mempool', i).decode('utf-8')
                if tx == None:
                    break
                verify_verdict = Election.verification.verify_tx(tx)
                if verify_verdict == "verified":
                    #Sending data to block
                    blk.add_transaction(tx)
                else:
                    i =  i - 1
                    continue
            #create block
            Block.compute_hash()
            Block.calculate_merkle_root()
            block = Block.to_json()
            
            #add block
            blkChain = BlockChain()
            blkChain.add_block(block)

            #full blockchain verify
            full_verify_message = Election.verification.full_chain_verify()
            if full_verify_message == "verified": 
                #braodcast the block you made
                context = zmq.Context()
                z4socket = context.socket(zmq.REQ)
                z4socket.connect("tcp://127.0.0.1:5007")
                z4socket.send_string(json.dumps(block))
                message = z4socket.recv()
                z4socket.close()
            else:
                return
    if is_del == False :
        full_verify_message = Election.verification.full_chain_verify()

def add_block_nondel():
    context = zmq.Context()
    zsocket = context.socket(zmq.REP)
    zsocket.bind("tcp://127.0.0.1:5119")
    zpoll = zmq.Poller()
    zpoll.register(zsocket)
    start_timestamp = time.time()
    all_blocks = []
    while time.time() - start_timestamp < 1:
        events = dict(zpoll.poll(1))
        for key in events:
            block = json.loads(key.recv_string())
            print(block)
            all_blocks.append(block)
            zsocket.send_string("got some block")
    zpoll.unregister(zsocket)
    zsocket.close()
    context.destroy()
    #get most common and add to chain
    
    #run full blockchain verif

def run_thread():
    t = threading.Thread(target=mining)
    t.start()
    t.join()
    t = threading.Thread(target=add_block_nondel)
    t.start()
    t.join()


