import redis
import urllib.request
import json
import random
import zmq
import settings
from dotscoin.Verification import Verification
from dotscoin.Transaction import Transaction
from dotscoin.Block import Block
from collections import defaultdict
from dotscoin.UDPHandler import UDPHandler
from dotscoin.BlockChain import BlockChain
from dotscoin.TransactionOutput import TransactionOutput
from utils import decode_redis, get_own_ip


class Election:
    """
        This class holds the nodes election every 30 seconds. A miner is being chosen
        from a list of primary representative.
    """

    def __init__(self):
        self.primary_representatives = dict()
        self.blockchain = BlockChain()
        self.fund_addr = ""
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.redis_client.hmset('fund '+self.fund_addr, {'total fund': 00})
        self.this_node_addr = get_own_ip()
        self.stakes_map = dict()
        self.votes_map = dict()
        self.verification = Verification()
        self.load_election_fund_details()

    def load_election_fund_details(self):
        f = open('electionfund.json', 'r')
        data = json.load(f)
        self.fund_addr = data["address"]

    def scan_election_fund(self):
        txs = blockchain.get_txs_by_addr(self.fund_addr)
        pipe = self.redis_client.pipeline()
        for tx in txs:
            for output in tx.outputs:
                if output.address == self.fund_addr:
                    if tx.inputs > 0:
                        pipe.hincrbyfloat(
                            "stakes_map", tx.inputs[0].address, output.value)
        pipe.execute()

    def get_stakes(self):
        self.stakes_map = decode_redis(redis_client.hgetall("stakes_map"))

    def elect_delegate(self):
        total_stake = 0
        arr = []
        for key, val in self.stakes_map.items():
            total_stake += int(val)
            for i in range(0, int(val)):
                arr.append(key)
        if total_stake == 0:
            return
        select = arr[random.randint(0, total_stake-1)]
        self.votes_map[self.this_node_addr] = select
        UDPHandler.castvote(json.dumps(
            {"node_addr": self.this_node_addr, "representative": select}))

    def vote_to(self):
        # Broadcast the selected node to vote
        # UDPHandler.broadcastmessage(json.dumps(
        #     {'data': {"voter_addr": self.this_node_addr, "voted_addr": select}, 'command': 'voteto'}))
        # context = zmq.Context()
        # z2socket = context.socket(zmq.REQ)
        # z2socket.connect("tcp://127.0.0.1:%s" % settings.BROADCAST_ZMQ_PORT)
        # z2socket.send_string(json.dumps({'data':{"voter_addr":self.this_node_addr, "voted_addr":select},'command': 'voteto'}))
        # message = z2socket.recv()
        # print(message)
        # z2socket.close()
        return

    def add_vote(self, vote):
        self.votes.update(vote)

    def delegates(self):
        votes_count = defaultdict(int)
        for key, val in self.votes.items():
            votes_count[val] += 1
        votes_count = sorted(votes_count.items(),
                             key=lambda kv: (kv[1], kv[0]))
        dels = []
        if len(votes_count) > 10:
            dels = list(reversed(list(votes_count)))[0:10]
        else:
            dels = list(reversed(list(votes_count)))
        return dels
