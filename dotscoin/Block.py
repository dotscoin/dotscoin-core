from datetime import datetime
from Transaction import Transaction
import hashlib
from typing import List


class Block:
    def __init__(self, prev_block_hash: str):
        self.timestamp = datetime.now()
        self.transactions: List[Transaction] = []
        self.previous_block_hash = prev_block_hash
        self.merkle_root: str = ""

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def calculate_merkle_root(self):
        h = hashlib.sha256()
        for transaction in self.transactions:
            h.update(transaction.hash)

        self.merkle_root = h.digest().decode("utf-8")

