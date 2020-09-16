import redis
import json
from dotscoin.BlockChain import BlockChain
from dotscoin.Block import Block
from dotscoin.StorageTx import StorageTx

class Verification:
    def __init__(self):
        blockchain = BlockChain()
        self.block = Block()
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.chain_length = self.redis_client.llen('chain')

    def verify_tx(self, transaction):
        inputs = transaction.inputs
        tx_verdict = "pending"

        if transaction.idf == "storage": 
            temp = []
            stx = StorageTx()
            temp.append(transaction.inputs[0].file_hash)
            for out in transaction.outputs:
                #check (out.part_filename, storage_addr)
                #ask for part file and verify part hash
                temp.append(out.part_hash)
            stx.gen_tx_hash(temp)
            chash = stx.hash

            if chash == transaction.hash:
                return "transaction verified"
            else:
                return "transaction unverified"
            
        else: 
            for input in inputs:
                i = 0
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

    def full_chain_verify(self):
        verify_message = "unverified"
        for i in range(0, self.chain_length):
            raw = json.loads(self.redis_client.lindex('chain', i).decode('utf-8'))
            block = Block.from_json(raw)
            block.calculate_merkle_root()
            v_merkl_root = block.merkle_root
            if v_merkl_root != raw["merkle_root"]: 
                verify_message = "failed"
        verify_message = "verified"
        return verify_message
    
    def del_from_faultblock(self, fault_index):
        self.redis_client.ltrim(fault_index, self.chain_length)
        self.sync_chain()









    





    





