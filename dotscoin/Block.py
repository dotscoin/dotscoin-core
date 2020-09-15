import time
import redis
import hashlib
import json
import sys
from typing import List
from dotscoin.Transaction import Transaction
from collections import Set, Mapping, deque

class Block:
    hash: str = ""
    timestamp = int(time.time())
    transactions: List[Transaction] = []
    previous_block_hash: str = ""
    merkle_root: str = ""
    height: int = 0
    version: str = "0.0.1"
    size: int = 0

    def __init__(self): 
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.add_previous_block()

    def add_previous_block(self):
        raw = self.redis_client.lindex('chain', -1)
        if raw is not None and json.loads(raw.decode('utf-8')) is not None:
            self.previous_block_hash = json.loads(raw.decode("utf-8"))["hash"]
            self.height = int(json.loads(raw.decode("utf-8"))["height"])+ 1 

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def to_json(self):
        return {
            'hash': self.hash,
            'timestamp': self.timestamp,
            'transactions': [tx.to_json() for tx in self.transactions],
            'previous_block_hash': self.previous_block_hash,
            'merkle_root': self.merkle_root,
            'height': self.height,
            'version': self.version,
            'size': self.size
        }
    def calcalute_block_size(self):
        size = 0
        message={
            'hash': self.hash,
            'timestamp': self.timestamp,
            'transactions': [tx.to_json() for tx in self.transactions],
            'previous_block_hash': self.previous_block_hash,
            'merkle_root': self.merkle_root,
            'height': self.height,
            'version': self.version,
            'size': self.size
        }
        for key in message.keys():
            size += sys.getsizeof(message[key]) 
        self.size = size

    @staticmethod
    def from_json(data):
        tmp = Block()
        tmp.hash = data['hash']
        tmp.timestamp = data['timestamp']
        tmp.transactions = [Transaction.from_json(
            tx) for tx in data['transactions']]
        tmp.previous_block_hash = data['previous_block_hash']
        tmp.merkle_root = data['merkle_root']
        tmp.height = data['height']
        tmp.version = data['version']
        tmp.size = data['size']
        return tmp

    def compute_hash(self):
        message = {
            "timestamp": self.timestamp,
            "transactions": [tx.to_json() for tx in self.transactions],
            "previous_block_hash": self.previous_block_hash,
            "merkle_root": self.merkle_root,
            "height": self.height,
            "version": self.version,
            "size": self.size
        }

        self.hash = hashlib.sha256(json.dumps(message).encode("utf-8")).hexdigest()
        

    def calculate_merkle_root(self, transactions=[]):
        new_tran = []
        if len(transactions) == 0:
            transactions = [tx.hash for tx in self.transactions]
        if len(transactions) > 1:
            if transactions[-1] == transactions[-2]:
                return ""
        for i in range(0, len(transactions), 2):
            h = hashlib.sha256()
            if i+1 == len(transactions):
                h.update(
                    ((transactions[i]) + (transactions[i])).encode("UTF-8"))
                new_tran.append(h.hexdigest())
            else:
                h.update(
                    ((transactions[i]) + (transactions[i+1])).encode("UTF-8"))
                new_tran.append(h.hexdigest())

        if len(new_tran) == 1:
            self.merkle_root = new_tran[0]
            return
        else:
            self.calculate_merkle_root(new_tran)