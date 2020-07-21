from datetime import datetime


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
