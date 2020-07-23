from dotscoin.Address import Address
from dotscoin.Transaction import Transaction

if __name__ == '__main__':
    address = Address()
    transaction = Transaction()

    transaction.add_input("{fhfhh")
    transaction.add_output("yhgyhgg")
    print(transaction.display())

    transaction.generate_signature(address.sk)

    print(transaction.signature)

    transaction.verify_signature(address.vk)

