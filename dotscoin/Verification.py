from dotscoin.BlockChain import BlockChain
from dotscoin.Block import Block
import redis
import json

class Verification:
    def __init__(self):
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
                flag = 0
                block = json.loads(self.redis_client.lindex('chain', -1-i).decode('utf-8'))
                if block == None:
                    tx_verdict = "verified"
                    return tx_verdict
                for tx in block.txs:
                    if tx.hash == input.previous_tx:
                        flag = 1
                        continue
                    for inp in tx.inputs:
                        if input.previous_tx == inp.previous_tx and input.index == inp.index :
                            tx_verdict = "rejected"
                            return tx_verdict
                if flag == 1:
                    break
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
        verify_message = "unverified"
        for i in range(0, self.chain_length):
            block = json.loads(self.redis_client.lindex('chain', i).decode('utf-8'))
            v_merkl_root = self.block.calculate_merkle_root(block.txs)
            if v_merkl_root != block.merkle_root: 
                verify_message = "failed"
                self.del_from_faultblock(i)
        verify_message = "verified"
        return verify_message
    
    def del_from_faultblock(self, fault_index):
        self.redis_client.ltrim(fault_index, self.chain_length)
        self.sync_chain()

    def sync_chain(self):
        pass









    





    





