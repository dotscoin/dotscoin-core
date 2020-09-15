import redis
import json
from typing import List
from dotscoin.Block import Block

class BlockChain:
    blocks: List[Block] = []

    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
    def add_block(self, blk):
        self.redis_client.rpush('chain', json.dumps(blk))

    def get_length(self) -> int:
        return self.redis_client.llen('chain')

    def clear_chain(self):
        self.redis_client.delete("chain")

    def close(self):
        self.redis_client.close()
