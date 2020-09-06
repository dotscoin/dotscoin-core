class TransactionOutput:
    value = 0
    address= ""
    n = 0
    def to_json(self):
        data={
            "value":self.value,
            "n":self.n,
            "address":self.address
        }
        return data