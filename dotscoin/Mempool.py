import redis
import json
from dotscoin.Transaction import Transaction

class Mempool:
    """ This class stores all the transactions in a temporary cache memory for block generation. """
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def add_transaction(self, val: Transaction) -> bool:
        """
        This function add transaction to the mempool for further processing

        Parameters:
            val(Any): The transaction object to add to the mempool.

        Returns:
            boolean: A boolean result to show if the transaction is added successfully or not.
        """
        self.redis_client.rpush("mempool", json.dumps(val.to_json()))
        return True
    
    def get_len(self):
        return self.redis_client.llen("mempool")

    def get_tx_by_mindex(self, i):
        return Transaction.from_json(self.redis_client.lindex("mempool", i).decode("utf-8"))

    def get_transaction(self) -> Transaction:
        return Transaction.from_json(json.loads(self.redis_client.rpop("mempool").decode("utf-8")))

    def get_size(self) -> int:
        return self.redis_client.llen("mempool")

    def remove_transaction(self, hash):
        length = self.redis_client.llen('mempool')
        while length > 0:
            raw = self.redis_client.lindex('mempool', length-1).decode('utf-8')
            tx = json.loads(raw)
            if tx == None:
                return
            if tx["hash"] == hash:
                self.redis_client.lrem('mempool', length, raw)
            length -= 1
    
    def flush_mempool(self):
        self.redis_client.delete("mempool")

    def close(self): 
        self.redis_client.close()

    def __del__(self):
        self.close()
