import json
import time
import hashlib
from ecdsa import VerifyingKey, BadSignatureError
from enum import Enum
from dotscoin.TransactionInput import TransactionInput
from dotscoin.TransactionOutput import TransactionOutput
from typing import List
from dotscoin.Address import Address
import redis


class TransactionStatus(str, Enum):
    UNCONFIRMED = "Unconfirmed"
    CONFIRMED = "Confirmed"


class Transaction:

    def __init__(self):
        self.timestamp = time.time()
        self.version: str = "0.0.1"
        self.hash: str = ""
        self.inputs: List[TransactionInput] = []
        self.outputs: List[TransactionOutput] = []
        self.block = "Mempool"

    def add_input(self, ti: TransactionInput):
        self.inputs.append(ti)

    def add_output(self, to: TransactionOutput):
        self.outputs.append(to)

    @staticmethod
    def from_json(data):
        tmp = Transaction()
        tmp.timestamp = data['timestamp']
        tmp.version = data['version']
        tmp.hash = data['hash']
        tmp.inputs = [TransactionInput.from_json(
            input) for input in data['inputs']]
        tmp.outputs = [TransactionOutput.from_json(
            output) for output in data['outputs']]
        tmp.block = data['block']

        return tmp

    def to_json(self):
        return {'timestamp': self.timestamp,
                'version': self.version,
                'hash': self.hash,
                'inputs': [TransactionInput.to_json(input) for input in self.inputs],
                'outputs': [TransactionOutput.to_json(output) for output in self.outputs],
                'block': self.block
                }

    def generate_hash(self):
        message = {
            'timestamp': self.timestamp,
            'version': self.version,
            'input': str(self.inputs),
            'output': str(self.outputs)
        }
        self.hash = hashlib.sha256(str(message).encode()).hexdigest()

    def generate_signature(self, sk):
        self.signature = sk.sign(self.display().encode("utf-8")).hex()

    def verify_signature(self, vk: VerifyingKey):
        try:
            vk.verify(bytes.fromhex(self.signature),
                      self.display().encode("utf-8"))
            return True
        except BadSignatureError:
            return False

    def coinbase_transaction(self):
        if self.is_coinbase == True:
            self.input = []

    def verify_transaction(self):
        for i, input in enumerate(self.input):
            address = Address()
            if address.verify_signature(input['prev_out']['script'], self.verifyingkey):
                continue
            else:
                return False
        return True

    def tx_by_hash(self, hash):
        i = 1
        while True:
            block = json.loads(self.redis_client.lindex(
                'chain', i).decode('utf-8'))
            if block == None:
                return None
            else:
                for tx in block.txs:
                    if tx.hash == hash:
                        return tx
            i = i + 1
        return None
