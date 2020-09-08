class TransactionInput:
    previous_tx = ""
    index = 0
    address = ""
    scriptSig = []
    verifying_key = []
    
    def to_json(self):
        return {
            "previous_tx":self.previous_tx,
            "index":self.index,
            "scriptSig": self.scriptSig,
            "verifying_key": self.verifying_key,
            "address": self.address
        }

    @staticmethod
    def from_json(data):
        tmp = TransactionInput()
        tmp.previous_tx = data['previous_tx']
        tmp.index = data['index']
        tmp.scriptSig = data['scriptSig']
        tmp.verifying_key = data['verifying_key']
        tmp.address = data['address']

        return tmp