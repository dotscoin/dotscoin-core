from datetime import datetime
from dotscoin.Transaction import Transaction
import hashlib
from typing import List


class Block:
    def __init__(self, prev_block_hash: str):
        self.hash:str = ""
        self.timestamp = datetime.now()
        self.transactions: List[Transaction] = []
        self.previous_block_hash = prev_block_hash
        self.merkle_root: str = ""
        self.confirmation = 0
        self.height =0
        self.miner: str = ""
        self.version:str = "0.0.1"
        self.size = 0
        self.block_reward = 50
        self.fee = 0

    
    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def compute_hash(self):
        message={
            "timestamp":self.timestamp,
            "transactions": self.transactions,
            "previous_block_hash":self.previous_block_hash,
            "height":self.height,
            "version":self.version,
            "merkle_root":self.merkle_root
        }
        self.hash= hashlib.sha256(str(message).encode()).hexdigest()

    def calculate_merkle_root(self, txs=None):
        new_tran = []

        if txs is None:
            new_tran= [tx.hash for tx in self.transactions]
        else:
            new_tran = txs
        if len(new_tran) > 1:
            if new_tran[-1] == new_tran[-2]:
                return ""
        for i in range(0,len(new_tran),2):
            h = hashlib.sha256()
            if i+1 == len(new_tran):
                h.update(((new_tran[i]) + (new_tran[i])).encode("UTF-8"))
                new_tran.append(h.hexdigest())
            else:
                h.update(((new_tran[i]) + (new_tran[i+1])).encode("UTF-8"))
                new_tran.append(h.hexdigest())
        self.merkle_root = new_tran[0] if (len(new_tran) == 1) else self.calculate_merkle_root(new_tran)

    