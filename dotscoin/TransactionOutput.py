class TransactionOutput:

    value = 0
    address= ""
    n = 0

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