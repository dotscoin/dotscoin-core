import time
import hashlib
from ecdsa import VerifyingKey, BadSignatureError
from enum import Enum
from dotscoin.TransactionInput import TransactionInput
from dotscoin.TransactionOutput import TransactionOutput
from typing import List
from dotscoin.Address import Address

class TransactionStatus(str, Enum):
    UNCONFIRMED = "Unconfirmed"
    CONFIRMED = "Confirmed"

class Transaction:
    timestamp = time.time()
    version: str = "0.0.1"
    hash: str = ""
    inputs: List[TransactionInput] = []
    outputs: List[TransactionOutput] = []
    is_coinbase: bool = False
    block = "Mempool"
    
    def add_input(self, transaction):
        self.inputs.append(transaction)

    def add_output(self, address):
        self.outputs.append(address)

    @staticmethod
    def from_json(data):
        tmp = Transaction()
        tmp.timestamp = data['timestamp']
        tmp.version = data['version']
        tmp.hash = data['hash']
        tmp.inputs = [TransactionInput.from_json(input) for input in data['inputs']]
        tmp.outputs = [TransactionOutput.from_json(output) for output in data['outputs']]
        tmp.is_coinbase = data['is_coinbase']
        tmp.block = data['block']

        return tmp

    def to_json(self):
        return {
            'timestamp': self.timestamp,
            'version': self.version,
            'hash': self.hash,
            'inputs': [TransactionInput.to_json(input) for input in self.inputs],
            'outputs': [TransactionOutput.to_json(output) for output in self.outputs],
            'is_coinbase': self.is_coinbase,
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
            vk.verify(bytes.fromhex(self.signature), self.display().encode("utf-8"))
            return True
        except BadSignatureError:
            return False

    def broadcast_transaction(self):
        input_tx = [ input.to_json() for input in self.inputs]
        output_tx= [ output.to_json() for output in self.outputs]
        message = self.to_json()
        return message

    def coinbase_transaction(self):
        if self.is_coinbase == True:
            self.input = []

    def verify_transaction(self):
        for i,input in enumerate(self.input):
            address=Address()
            if address.verify_signature(input['prev_out']['script'],self.verifyingkey):
                continue
            else: 
                return False
        return True
              