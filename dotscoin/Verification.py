from dotscoin.BlockChain import BlockChain
from dotscoin.Block import Block
import redis
import json

class Verification:
    def __init__(self, pending_block: any):
        self.pblock = pending_block
        blockchain = BlockChain()
        self.block = Block()
        self.redis_client = blockchain.redis_client
        self.chain_length = self.redis_client.llen('chain')

    def verify_tx(self, transaction):
        inputs = transaction.inputs
        tx_verdict = "pending"

        for input in inputs:
            i = 0
            # block = json.loads(self.redis_client.lindex('chain', -1).decode('utf-8'))
            while True:
                block = json.loads(self.redis_client.lindex('chain', -1-i).decode('utf-8'))
                if block == None:
                    tx_verdict = "verified"
                    return tx_verdict
                for tx in block.txs:
                    for out in tx.outs:
                        if out.tx_index == input.prev_out.tx_index and out.hash == input.prev_out.hash :
                            tx_verdict = "transaction rejected"
                            return tx_verdict
                i = i + 1
        
        tx_verdict = "verified"
        return tx_verdict

        # index = -1
        # while True:
        #     block = json.loads(self.redis_client.lindex('chain', -1).decode('utf-8'))
        #     for tx in block.txs:
        #         if tx.hash == transaction.hash:
        #             return False
        #         for input in tx.inputs:
        #             if input.prev_out.hash == transaction.input.prev_out.hash and input.prev_out.tx_index == transaction.input.prev_out.tx_index:



    def full_chain_verify(self):
        for i in range(0,self.chain_length):
            block = json.loads(self.redis_client.lindex('chain', i).decode('utf-8'))
            v_merkl_root = self.block.calculate_merkle_root(block.txs)
            if v_merkl_root != block.merkle_root: 
                return i
    
    def del_from_faultblock(self, fault_index):
        self.redis_client.ltrim(0, fault_index-1)

    def sync_chain(self):
        #sync from a node
        return self









    





    





