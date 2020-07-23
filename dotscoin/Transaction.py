from datetime import datetime
import hashlib

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
            'timestamp': self.timestamp,
            'version': self.version,
            'input': str(self.input),
            'output': str(self.output)
        }

        return hashlib.sha256(str(message).encode())

