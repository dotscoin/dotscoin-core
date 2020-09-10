import redis
import json
from typing import List
from dotscoin.Block import Block

class BlockChain:
    data = ""

    def __init__(self):
        self.blocks: List[Block] = []
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
    def add_block(self, blk):
        self.redis_client.rpush('chain', json.dumps(blk))

    def read_chain(self, index: int):
        return self.redis_client.lrange('chain', 0, index)

    def clear_chain(self):
        self.redis_client.flushdb()
