import redis
import json
from typing import List
from dotscoin.Block import Block
from dotscoin.Transaction import Transaction

class BlockChain:
    blocks: List[Block] = []

    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
    def add_block(self, blk: Block):
        self.redis_client.rpush('chain', json.dumps(blk.to_json()))

    def get_block(self, index: int) -> Block:
        return Block.from_json(json.loads(self.redis_client.lindex("chain", index).decode("utf-8")))


    def get_length(self) -> int:
        return self.redis_client.llen('chain')

    def flush_chain(self):
        self.redis_client.delete("chain")

    def get_all_txs_by_address(self, address: str) -> List[Transaction]:
        """ Function to get all transactions of an address """
        response: List[Transaction] = []
        chain_length = self.get_length()

        while chain_length > 0:
            block = self.get_block(chain_length - 1)
            print(block.to_json())
            print("--------------")
            for tx in block.transactions:
                if tx.inputs[0].address == address:
                    response.append(tx)
                    continue
                for output in tx.outputs:
                    if output.address == address:
                        response.append(tx)
                        break

            chain_length -= 1

        return response

    def close(self):
        self.redis_client.close()

    def __del__(self):
        self.close()
