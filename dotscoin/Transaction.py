from datetime import datetime
import hashlib
from ecdsa import VerifyingKey, BadSignatureError
from enum import Enum
from dotscoin.TransactionInput import TransactionInput
from dotscoin.TransactionOutput import TransactionOutput
from typing import List
import dotscoin.Address import Address
class TransactionStatus(str, Enum):
    UNCONFIRMED = "Unconfirmed"
    CONFIRMED = "Confirmed"

class Transaction:
    timestamp = datetime.now()
    version: str = "0.0.1"
    hash: str = ""
    inputs: List[TransactionInput] = []
    outputs: List[TransactionOutput] = []
    is_coinbase: bool = False
    status = TransactionStatus.UNCONFIRMED
    block = "Mempool"
    verifyingkey: str = ""
    def add_input(self, transaction):
        self.inputs.append(transaction)

    def add_output(self, address):
        self.outputs.append(address)

    def generate_hash(self):
        message = {
            'timestamp': datetime.timestamp(self.timestamp),
            'version': self.version,
            'input': str(self.inputs),
            'output': str(self.outputs)
        }

        self.hash = hashlib.sha256(str(message).encode()).hexdigest()

    def display(self):
        message = {
            'timestamp': datetime.timestamp(self.timestamp),
            'version': self.version,
            'input': str(self.inputs),
            'output': str(self.outputs)
        }

        return str(message)

    def generate_signature(self, sk):
        self.signature = sk.sign(self.display().encode("utf-8")).hex()

    def verify_signature(self, vk: VerifyingKey):
        try:
            vk.verify(bytes.fromhex(self.signature), self.display().encode("utf-8"))
            return True
        except BadSignatureError:
            return False

    def broadcast_transaction(self):
        message = {
            'timestamp': datetime.timestamp(self.timestamp),
            'version': self.version,
            'input': str(self.input),
            'output': str(self.output),
            'signature': self.signature,
            'hash': self.hash
        }
        return message

    def coinbase_transaction(self):
        if self.is_coinbase == True:
            self.input = []

    def check_transaction(self):
        if not isinstance(self.timestamp,datetime.datetime):
            return False
        if not isinstance(self.version, str):
            return False
        if not isinstance(self.hash , str):
            return False
        if not isinstance(self.input,List[TransactionInput]):
            return False
        if not isinstance(self.output,List[TransactionOutput]):
            return False
        if not isinstance(self.signature,str):
            return False
        if not isinstance(self.status,TransactionStatus):
            return False
        if not isinstance(self.fees,int):
            return False
        return True

    def verify_transaction(self):
        for i,input in enumerate(self.input):
            address=Address()
            if address.verify_signature(input['prev_out']['script'],self.verifyingkey):
                continue
            else: 
                return False
        return True
              