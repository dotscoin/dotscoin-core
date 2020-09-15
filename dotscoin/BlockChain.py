# all imports
import redis
import json
from typing import List
from dotscoin.Block import Block

class BlockChain:
    """ Object Initialization """

    data = ""

    def __init__(self):
        """ Initialization """

        self.blocks: List[Block] = []
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
    def add_block(self, blk):
        """ Adding Block to blockchain """

        self.redis_client.rpush('chain', json.dumps(blk))

    def read_chain(self, index: int):
        """ Reading the blockchain """

        return self.redis_client.lrange('chain', 0, index)

    def clear_chain(self):
        """ Clearing the blockchain """
        
        self.redis_client.flushdb()
