from dotscoin.Address import Address
from dotscoin.Transaction import Transaction
from dotscoin.Mempool import Mempool

if __name__ == '__main__':
    address = Address()
    
    print(address.export())
    print(address.get_public_address())

