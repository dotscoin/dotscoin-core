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
            "timestamp": datetime.timestamp(self.timestamp),
            "transactions": self.transactions,
            "previous_block_hash":self.previous_block_hash,
            "height":self.height,
            "version":self.version,
            "merkle_root":self.merkle_root
        }
    
        self.hash= hashlib.sha256(str(message).encode()).hexdigest()

    def calculate_merkle_root(self, transactions=[]):
        new_tran = []
        if len(transactions) == 0: 
            transactions = [tx.hash for tx in self.transactions]
        if len(transactions) > 1:
            if transactions[-1] == transactions[-2]:
                return ""
        for i in range(0,len(transactions),2):
            h = hashlib.sha256()
            if i+1 == len(transactions):
                h.update(((transactions[i]) + (transactions[i])).encode("UTF-8"))
                new_tran.append(h.hexdigest())
            else:
                h.update(((transactions[i]) + (transactions[i+1])).encode("UTF-8"))
                new_tran.append(h.hexdigest())

        if len(new_tran) == 1 :
            self.merkle_root = new_tran[0]
            return
        else:
            self.calculate_merkle_root(new_tran)
        
    