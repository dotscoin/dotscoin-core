import time
from dotscoin.Transaction import Transaction
import redis
import hashlib
from typing import List
import json
from collections import Set, Mapping, deque
import sys

class Block:
    previous_block_hash: str = ""
    height: int = 0
    size: int = 0
    timestamp = int(time.time())

    def __init__(self):
        self.hash: str = ""
        self.transactions: List[Transaction] = []
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.merkle_root: str = ""
        self.version: str = "0.0.1"
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
            'size': self.getsize(self.__dict__)
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
        return size
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
        print(message)

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

    def getsize(obj_0):
        """Recursively iterate to sum size of object & members."""
        _seen_ids = set()
        def inner(obj):
            obj_id = id(obj)
            if obj_id in _seen_ids:
                return 0
            _seen_ids.add(obj_id)
            size = sys.getsizeof(obj)
            if isinstance(obj, zero_depth_bases):
                pass # bypass remaining control flow and return
            elif isinstance(obj, (tuple, list, Set, deque)):
                size += sum(inner(i) for i in obj)
            elif isinstance(obj, Mapping) or hasattr(obj, iteritems):
                size += sum(inner(k) + inner(v) for k, v in getattr(obj, iteritems)())
            # Check for custom object instances - may subclass above too
            if hasattr(obj, '__dict__'):
                size += inner(vars(obj))
            if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
                size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
            self.size = size
        return 