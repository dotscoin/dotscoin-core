from queue import LifoQueue
from dotscoin.Transaction import Transaction

class Mempool:
    """ This class stores all the transactions in a temporary cache memory for block generation. """
    def __init__(self):
        self.transactions = LifoQueue(maxsize=8000)

    def add_transaction(self, val: Transaction) -> bool:
        """
        This function add transaction to the mempool for further processing

        Parameters:
            val(Any): The transaction object to add to the mempool.

        Returns:
            boolean: A boolean result to show if the transaction is added successfully or not.
        """
        if self.transactions.full():
            return False
        self.transactions.put(val)
        return True

    def get_transaction(self) -> Transaction:
        return self.transactions.get()

    def get_size(self) -> int:
        return self.transactions.qsize()
