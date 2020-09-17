class TransactionOutput:

    def __init__(self):
        self.value = 0
        self.address= ""
        self.n = 0

    def to_json(self):
        return {
            "value":self.value,
            "n":self.n,
            "address":self.address
        }

    @staticmethod
    def from_json(data):
        tmp = TransactionOutput()
        tmp.n = data['n']
        tmp.address = data['address']
        tmp.value = data['value']
        return tmp