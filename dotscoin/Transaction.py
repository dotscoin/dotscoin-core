from datetime import datetime
import hashlib
from ecdsa import VerifyingKey, BadSignatureError

class Transaction:
    def __init__(self):
        self.timestamp = datetime.now()
        self.version: str = "0.0.1"
        self.hash: str = ""
        self.input = []
        self.output = []
        self.signature: str = ""
        self.is_coinbase: bool = False

    def add_input(self, transaction):
        self.input.append(transaction)

    def add_output(self, address):
        self.output.append(address)

    def generate_hash(self):
        message = {
            'timestamp': datetime.timestamp(self.timestamp),
            'version': self.version,
            'input': str(self.input),
            'output': str(self.output)
        }

        self.hash = hashlib.sha256(str(message).encode()).hexdigest()

    def display(self):
        message = {
            'timestamp': datetime.timestamp(self.timestamp),
            'version': self.version,
            'input': str(self.input),
            'output': str(self.output)
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


