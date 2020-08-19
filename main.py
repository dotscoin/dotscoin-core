from dotscoin.Address import Address
from dotscoin.Transaction import Transaction
from dotscoin.Mempool import Mempool

if __name__ == '__main__':
    address = Address()
    transaction = Transaction()
    mempool = Mempool()

    transaction.add_input("fhfhh")
    transaction.add_output("yhgyhgg")
    mempool.add_transaction(transaction)
    transaction.generate_signature(address.sk)
    print(transaction.signature)
    print(transaction.verify_signature(address.vk))
    print(mempool.get_transaction())
    print(mempool.get_size())
