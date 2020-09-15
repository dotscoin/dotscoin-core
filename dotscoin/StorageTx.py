import json
import time
import hashlib

class StorageTx:
    hash: str = ""
    block = "Mempool" 
    timestamp = time.time()
    inputs = []
    outputs = []
    temp = []

    def add_input(self, hash, addr):
        temp.append(hash)
        inp = {
            "file_hash" : hash,
            "sender_addr" : addr,
        }
        inputs.append(inp)
        return
    
    def add_output(self, hash, addr, part_filename):
        temp.append(hash)
        out = {
            "part_hash" : hash,
            "part_filename" part_filename,
            "storage_addr" : addr,
        }

    def gen_tx_hash(self, tmp = []):
        new_tran = []
        if len(tmp) == 0:
            tmp = [hsh for hsh in self.temp]
        if len(tmp) > 1:
            if tmp[-1] == tmp[-2]:
                return ""
        for i in range(0, len(tmp), 2):
            h = hashlib.sha256()
            if i+1 == len(tmp):
                h.update(
                    ((tmp[i]) + (tmp[i])).encode("UTF-8"))
                new_tran.append(h.hexdigest())
            else:
                h.update(
                    ((tmp[i]) + (tmp[i+1])).encode("UTF-8"))
                new_tran.append(h.hexdigest())

        if len(new_tran) == 1:
            self.hash = new_tran[0]
            return
        else:
            self.gen_tx_hash(new_tran)

    def to_json(self):
        return {
            "hash": self.hash,
            "block": self.block,
            "timestamp":self.timestamp,
            "inputs": self.inputs,
            "outputs": self.outputs
        }