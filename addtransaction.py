import redis
import json
import time
from dotscoin.Block import Block
from dotscoin.Transaction import Transaction
from dotscoin.TransactionInput import TransactionInput
from dotscoin.TransactionOutput import TransactionOutput
from dotscoin.Address import Address
import nodecreate
    
def create_tx(addr):
    add_data = {
        "address": "1d3f347aada53547142da8edea5e0019e6ef31bb15",
        "vk": "-----BEGIN PUBLIC KEY-----\nMEkwEwYHKoZIzj0CAQYIKoZIzj0DAQEDMgAEHxzkpgh/lqgd1/rb7d+D+srhlhzG\ncOAveBQafVnHkffNR2aCiFHVQZKzhyO7iC/p\n-----END PUBLIC KEY-----\n",
        "sk": "-----BEGIN EC PRIVATE KEY-----\nMF8CAQEEGKtkXJ8xlejSSOl4mzNTYiXmb70wRByW1aAKBggqhkjOPQMBAaE0AzIA\nBB8c5KYIf5aoHdf62+3fg/rK4ZYcxnDgL3gUGn1Zx5H3zUdmgohR1UGSs4cju4gv\n6Q==\n-----END EC PRIVATE KEY-----\n"
    }
    tx = Transaction()
    add = Address()
    add.load(add_data["sk"], add_data["vk"])
    # print(addr)
    tx.inputs = []
    tx.inputs.append(TransactionInput.from_json({
        'previous_tx': "16e8dab3a9185d5329fac9cfdc0a81c7817826f701e747cb3751878061e4dc8c",
        'index': 0,
        'scriptSig': [add.sign_message(json.dumps({
            'previous_tx': "16e8dab3a9185d5329fac9cfdc0a81c7817826f701e747cb3751878061e4dc8c",
            'index': 0
        }).encode("utf-8")).hex()],
        'address': addr,
        'verifying_key': [add_data["vk"]]
    }))
    tx.outputs.append(TransactionOutput.from_json({
        'address': "yikgyyf67rr68t887tfc",
        'value': 25,
        'n': 0
    }))
    tx.generate_hash()
    txf = tx.to_json()
    # print(txf['inputs'][0]['address'])
    return txf

def create_txs(n):
    nodes = nodecreate.get_dns(n)
    txs = []
    for key, value in nodes.items():
        # print(value)
        tx = create_tx(value)
        txs.append(tx)
    
    return txs

if __name__ == '__main__':
    create_txs(15)
    pass
    # print(create_txs(15))