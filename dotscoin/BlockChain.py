# all imports
import redis
import json
from typing import List, Tuple
from dotscoin.Block import Block
from dotscoin.Transaction import Transaction

class BlockChain:
    """ Object Initialization """

    def __init__(self):
        """ Initialization """

        self.data = ""
        self.blocks: List[Block] = []
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
    def add_block(self, blk: Block):
        self.redis_client.rpush('chain', json.dumps(blk.to_json()))

    def get_block(self, index: int) -> Block:
        raw = self.redis_client.lindex("chain", index)
        if raw is not None:
            return Block.from_json(json.loads(raw.decode("utf-8")))
        else:
            return

    def get_length(self) -> int:
        return self.redis_client.llen("chain")

    def flush_chain(self):
        self.redis_client.delete("chain")

    def final_addr_balance(self, addr):
        """ This function scans the complete blockchain and returns
        the total balance of an Address """
        chain_length = self.redis_client.llen('chain')
        total = 0
        used_transactions = set()
        while chain_length > 0:
            block = Block.from_json(json.loads(self.redis_client.lindex('chain', chain_length - 1).decode('utf-8')))
            for tx in block.transactions:
                for inp in tx.inputs:
                    if inp.address == addr:
                        used_transactions.add((inp.previous_tx, inp.index))
                for out_index, out in enumerate(tx.outputs):
                    if tx.hash not in used_transactions:
                        if out.address == addr:
                            total = total + out.value
                    else:
                        if out.address == addr and (tx.hash, out_index) not in used_transactions:
                            total = total + out.value
            chain_length -= 1

        return total

    def get_txs_by_addr(self, addr) -> List[Transaction]:
        txs = []
        chain_length = self.redis_client.llen('chain')
        while chain_length > 0:
            block = Block.from_json(json.loads(self.redis_client.lindex('chain', chain_length - 1).decode('utf-8')))
            print(len(block.transactions))
            for tx in block.transactions:
                inp_adresses = [inp.address for inp in tx.inputs]
                if addr in inp_adresses:
                    txs.append(tx)
                    continue
                out_adresses = [out.address for out in tx.outputs]
                if addr in out_adresses:
                    txs.append(tx)
                    continue
            chain_length -= 1

        return txs

    def get_utxos_by_addr(self, addr) -> List[Tuple[str, int, float]]:
        utxos = []
        chain_length = self.redis_client.llen('chain')
        used_transactions = set()
        while chain_length > 0:
            block = Block.from_json(json.loads(self.redis_client.lindex('chain', chain_length - 1).decode('utf-8')))
            for tx in block.transactions:
                for inp in tx.inputs:
                    if inp.address == addr:
                        used_transactions.add((inp.previous_tx, inp.index))
                for out_index, out in enumerate(tx.outputs):
                    if tx.hash not in used_transactions:
                        if out.address == addr:
                            utxos.append((tx.hash, out_index, out.value))
                    else:
                        if out.address == addr and (tx.hash, out_index) not in used_transactions:
                            utxos.append((tx.hash, out_index, out.value))
            chain_length -= 1

        return utxos

    def get_tx_by_hash(self, hash: str):
        chain_length = self.redis_client.llen('chain')
        while chain_length > 0:
            block = Block.from_json(json.loads(self.redis_client.lindex('chain', chain_length - 1).decode('utf-8')))
            for tx in block.transactions:
                if tx.hash == hash:
                    return tx
            chain_length -= 1

        return

    def close(self):
        self.redis_client.close()

    def __del__(self):
        self.close()
