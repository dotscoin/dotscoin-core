from typing import List
from dotscoin.Block import Block
import redis
import json

class BlockChain:
    def __init__(self):
        self.data = ""
        self.blocks: List[Block] = []
        self.block = {
            'hash': '16e8dab3a9185d5329fac9cfdc0a81c7817826f701e747cb3751878061e4dc8c', 
            'timestamp': 1599401715.846563,
            'transaction': {
                'timestamp': 1599401715.846347, 
                'version': '0.0.1', 
                'inputs': [
                    {
                        "sequence": 4294967293,
                        "witness": "",
                        "prev_out": {
                            "spent": "true",
                            "spending_outpoints": [
                            {}
                            ],
                            "tx_index": 0,
                            "type": 0,
                            "addr": "3AXBsYDtuwTSMr3xbZPhNk4A9mVJ6srDnr",
                            "value": 45,
                            "n": 29,
                            "script": "a91460dd46da88f6f98aa36ea2adf1e48d92b27be08887"
                    
                    },
      "script": "220020220bc102bbd1fc2bd1fcfbc12eeeee46b27f377647c23d1786785d69203e3756"
            }
                ],
                'outputs': [
                    {
                    'value': 5, 
                    'n': 0, 
                    'address': '1d3f347aada53547142da8edea5e0019e6ef31bb15'
                    }
                ], 
            'hash': 'eef9fda50a6bf6c11c5078d8772d94df4f60ce54573c009f145eb047426ad0fb',
            'block': 'testchain'
                        },
            'previous_block_hash': '', 
            'merkle_root': '78bc90dcc3fe2ae1eca8b9d4e09b63653cd18f0b583e002b2b4d43cc09fca9cd',
            'confirmation': 0, 'height': 0, 'miner': '1d3f347aada53547142da8edea5e0019e6ef31bb15', 
            'version': '0.0.1', 
            'size': 64,
            'block_reward': 50, 
            'fee': 0
        }
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
    def add_block(self):
        # print(json.dumps(self.block))
        self.redis_client.rpush('chain', json.dumps(self.block))

    def read_chain(self):
        return self.redis_client.lrange('chain', 0, -1)

    def clear_chain(self):
        self.redis_client.flushdb()
