from queue import LifoQueue
from dotscoin.Transaction import Transaction
import redis


class Mempool:
    """ This class stores all the transactions in a temporary cache memory for block generation. """
    def __init__(self):
        # self.transactions = LifoQueue(maxsize=8000)
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def add_transaction(self, val: Transaction) -> bool:
        """
        This function add transaction to the mempool for further processing

        Parameters:
            val(Any): The transaction object to add to the mempool.

        Returns:
            boolean: A boolean result to show if the transaction is added successfully or not.
        """
        self.redis_client.rpush("mempool", val.display())
        return True

    def get_transaction(self) -> Transaction:
        return self.redis_client.rpop("mempool").decode("utf-8")

    def get_size(self) -> int:
        return self.redis_client.llen("mempool")
