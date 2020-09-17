import redis
import json
import time
import random
from dotscoin.Block import Block
from dotscoin.Transaction import Transaction
from dotscoin.TransactionInput import TransactionInput
from dotscoin.TransactionOutput import TransactionOutput
from dotscoin.Address import Address

global_addresses = []
add_data = {
    "address": "1d3f347aada53547142da8edea5e0019e6ef31bb15",
    "vk": "-----BEGIN PUBLIC KEY-----\nMEkwEwYHKoZIzj0CAQYIKoZIzj0DAQEDMgAEHxzkpgh/lqgd1/rb7d+D+srhlhzG\ncOAveBQafVnHkffNR2aCiFHVQZKzhyO7iC/p\n-----END PUBLIC KEY-----\n",
    "sk": "-----BEGIN EC PRIVATE KEY-----\nMF8CAQEEGKtkXJ8xlejSSOl4mzNTYiXmb70wRByW1aAKBggqhkjOPQMBAaE0AzIA\nBB8c5KYIf5aoHdf62+3fg/rK4ZYcxnDgL3gUGn1Zx5H3zUdmgohR1UGSs4cju4gv\n6Q==\n-----END EC PRIVATE KEY-----\n"
}


def create_fake_transaction(address: Address):
    tmp_tx = Transaction()
    add = Address()
    add.load(add_data["sk"], add_data["vk"])

    tmp_tx.inputs.append(TransactionInput.from_json({
        'previous_tx': "16e8dab3a9185d5329fac9cfdc0a81c7817826f701e747cb3751878061e4dc8c",
        'index': 0,
        'scriptSig': [add.sign_message(json.dumps({
            'previous_tx': "16e8dab3a9185d5329fac9cfdc0a81c7817826f701e747cb3751878061e4dc8c",
            'index': 0
        }).encode("utf-8")).hex()],
        'address': add_data["address"],
        'verifying_key': [add_data["vk"]]
    }))
    tmp_tx.outputs.append(TransactionOutput.from_json({
        'address': "yikgyyf67rr68t887tfc",
        'value': 25,
        'n': 0
    }))
    tmp_tx.generate_hash()

    return tmp_tx


if __name__ == "__main__":
    # Push 10 random addresses
    for i in range(10):
        tmp_addr = Address()
        global_addresses.append(tmp_addr)

    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    # Clean the whole database
    redis_client.flushall()

    # Add genesis block
    redis_client.rpush("chain", json.dumps({
        "hash": "16e8dab3a9185d5329fac9cfdc0a81c7817826f701e747cb3751878061e4dc8c",
        "timestamp": 1599401715.846563,
        "transactions": [{
            "timestamp": 1599401715.846347,
            "version": "0.0.1",
            "inputs": [],
            "outputs": [
                {
                    "value": 50,
                    "n": 0,
                    "address": "1d3f347aada53547142da8edea5e0019e6ef31bb15"
                }
            ],
            "hash": "eef9fda50a6bf6c11c5078d8772d94df4f60ce54573c009f145eb047426ad0fb",
            "block": "16e8dab3a9185d5329fac9cfdc0a81c7817826f701e747cb3751878061e4dc8c"
        }],
        "previous_block_hash": "",
        "merkle_root": "78bc90dcc3fe2ae1eca8b9d4e09b63653cd18f0b583e002b2b4d43cc09fca9cd",
        "height": 0,
        "version": "0.0.1",
        "size": 1949
    }))

    for i in range(5):
        block = Block()
        block.add_transaction(create_fake_transaction(
            global_addresses[random.randint(0, 9)]))
        block.calculate_merkle_root()
        block.compute_hash()
        block.calcalute_block_size()
   
        redis_client.rpush("chain", json.dumps(block.to_json()))