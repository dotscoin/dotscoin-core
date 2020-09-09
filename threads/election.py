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
import redis
import threading
import urllib.request
import settings

class Election:
    """
        This class holds the nodes election every 30 seconds. A miner is being chosen
        from a list of primary representative.
    """
    def __init__(self):
        self.primary_representatives = dict()
        self.blockchain = BlockChain()
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.fund_addr = "yikgyyf67rr68t887tfc"
        self.redis_client.hmset('fund '+self.fund_addr, {'total fund': 00})
        self.this_node_addr = "addr1"
        self.stakes = dict()
        self.votes = dict()
        self.verification =  Verification()

    def get_node_addr(self):
        response = urllib.request.urlopen("https://checkip.amazonaws.com/").read()
        self.this_node_addr = response.decode("utf-8").strip()


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
        chain_length = self.redis_client.llen('chain')
        i = 0
        while i < chain_length:
            raw = json.loads(self.redis_client.lindex('chain', i).decode('utf-8'))
            print(raw)
            block = Block.from_json(raw)
            if block == None:
                return 
            for tx in block.transactions:
                for out in tx.outputs:
                    if out.address == self.fund_addr:
                        sender_addr = tx.inputs[0].address
                        if self.redis_client.hget('fund '+self.fund_addr, sender_addr) == None:
                            self.redis_client.hmset('fund '+self.fund_addr, {sender_addr: out.value})
                        else:
                            self.redis_client.hmset('fund '+self.fund_addr, {sender_addr: self.redis_client.hincrby('fund '+self.fund_addr, sender_addr, out.value)})
            i = i + 1
        return 

    def get_stakes(self):
        self.election_fund()
        fetch_stakes_bytes = self.redis_client.hgetall('fund '+self.fund_addr)
        fetch_stakes = { y.decode('ascii'): fetch_stakes_bytes.get(y).decode('ascii') for y in fetch_stakes_bytes.keys() }
        # print(fetch_stakes)
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

def bestblock(merkle_roots=[]):
    key_value=dict()
    max=[]
    for i,merkle_root in enumerate(merkle_roots):
        if not merkle_root in key_value.keys():
            key_value[merkle_root]=1
        else:
            key_value[merkle_root] += 1
                        
    for key in key_value.keys():
        max.append(key_value[key])
        max.sort(reverse=True)
    for key in key_value.keys():
         if key_value[key] == max[0]:
           print(key)
           return key

def worker():
    elec = Election()
    elec.election_fund()
    elec.get_stakes()
    elec.vote_to()
    print("vote sent and waiting for other's votes")
    context = zmq.Context()
    zsocket = context.socket(zmq.REP)
    zsocket.bind("tcp://127.0.0.1:%s" % settings.ELECTION_ZMQ_PORT)
    zpoll = zmq.Poller()
    zpoll.register(zsocket)
    start_timestamp = time.time()
    while time.time() - start_timestamp < 25:
        events = dict(zpoll.poll(1))
        for key in events:
            vote = json.loads(key.recv_string())
            elec.add_vote(vote)
            zsocket.send_string("got some nodes vote")
    zpoll.unregister(zsocket)
    zsocket.close()
    context.destroy()

    return elec.delegates()

def mining():
    pass

def electionworker():
    elec = Election()
    elec.get_node_addr()
    dels = worker()
    print("yes")
    is_del = False
    for dele in dels:
        if dele == elec.this_node_addr:
            print("del")
            is_del = True
            if elec.redis_client.llen("mempool") == 0:
                print("ha ye to ")
                return
            blk = Block()
            for i in range(0, elec.redis_client.llen("mempool")):
                tx = elec.redis_client.lindex('mempool', i).decode('utf-8')
                if tx == None:
                    continue
                verify_verdict = elec.verification.verify_tx(tx)
                if verify_verdict == "verified":
                    #Sending data to block
                    blk.add_transaction(tx)
            
            #create block
            blk.compute_hash()
            blk.calculate_merkle_root()
            block = blk.to_json()
            
            #add block
            blkChain = BlockChain()
            blkChain.add_block(block)

            #full blockchain verify
            full_verify_message = elec.verification.full_chain_verify()
            if full_verify_message == "verified": 
                #braodcast the block you made
                context = zmq.Context()
                z4socket = context.socket(zmq.REQ)
                z4socket.connect("tcp://127.0.0.1:%s" % settings.BROADCAST_ZMQ_PORT)
                z4socket.send_string(json.dumps({'data':block, 'command':'addblock'}))
                message = z4socket.recv()
                z4socket.close()
            else:
                return
    if is_del == False :
        pass
        # full_verify_message = Election.verification.full_chain_verify()

def add_block_nondel():
    context = zmq.Context()
    zsocket = context.socket(zmq.REP)
    zsocket.bind("tcp://127.0.0.1:%s" % settings.ELECTION_ZMQ_PORT)
    zpoll = zmq.Poller()
    zpoll.register(zsocket)
    start_timestamp = time.time()
    all_blocks = []
    while time.time() - start_timestamp < 3:
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
    if len(all_blocks) > 0:
        print(all_blocks)
        mr = []
        for blk in all_blocks:
            mr.append(blk.merkle_root)
        #run full blockchain verif
        blkc = BlockChain()
        Mblock = bestblock(mr)
        blkc.add_block(Mblock)

def mining():
    vf = Verification()
    print(vf.full_chain_verify())

def run_thread():
    print("Starting Election/Mining rocess")
    t = threading.Thread(target=mining)
    # t = threading.Thread(target=electionworker)
    t.start()
    t.join()
    # t = threading.Thread(target=add_block_nondel)
    # t.start()
    # t.join()


