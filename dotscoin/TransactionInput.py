class TransactionInput:
    previous_tx = ""
    index = 0
    scriptSig = []
    verifying_key = []
    
    def to_json(self):
        data={
            "hash":self.previous_tx,
            "index":self.index,
            "script": self.scriptSig,
            "verifyingKey": self.verifying_key
        }
        return data