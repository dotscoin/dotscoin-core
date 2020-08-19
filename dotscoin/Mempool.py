from queue import LifoQueue
from dotscoin.Transaction import Transaction
import redis


class Mempool:
    """ This class stores all the transactions in a temporary cache memory for block generation. """
    def __init__(self):
        # self.transactions = LifoQueue(maxsize=8000)
        self.redis_client = redis.Redis(host='redis-15273.c92.us-east-1-3.ec2.cloud.redislabs.com', port=15273, db=0, password="8561sara")

    def add_transaction(self, val: Transaction) -> bool:
        """
        This function add transaction to the mempool for further processing

        Parameters:
            val(Any): The transaction object to add to the mempool.

        Returns:
            boolean: A boolean result to show if the transaction is added successfully or not.
        """
        # if self.transactions.full():
        #     return False
        # self.transactions.put(val)
        self.redis_client.rpush("mempool", val.display())
        return True

    def get_transaction(self) -> Transaction:
        # return self.transactions.get()
        return self.redis_client.rpop("mempool").decode("utf-8")

    def get_size(self) -> int:
        # return self.transactions.qsize()
        return self.redis_client.llen("mempool")
