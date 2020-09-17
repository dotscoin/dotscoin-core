import os
import json
import time
import redis
import hashlib

class StorageTx:

    def __init__(self):
        self.hash: str = ""
        self.block = "Mempool" 
        self.timestamp = time.time()
        self.inputs = []
        self.outputs = []
        self.temp = []
        self.temp.append(timestamp)
        self.idf = "storage"
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def add_input(self, Hash, addr):
        self.temp.append(Hash)
        inp = {
            "file_hash" : Hash,
            "sender_addr" : addr,
        }
        self.inputs.append(inp)
        return
    
    def add_output(self, Hash, addr, part_filename):
        print(Hash)
        print(part_filename)
        self.temp.append(Hash)
        out = {
            "part_hash" : Hash,
            "part_filename": part_filename,
            "storage_addr" : addr,
        }
        self.outputs.append(out)
        return

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
            "outputs": self.outputs,
            "idf": self.idf
        }

    #FILE RETRIEVAL CODE
    def get_file(self, filehash):
        i = 0
        while True:
            block = json.loads(self.redis_client.lindex('chain', -1-i).decode('utf-8'))
            if block == None:
                return "file not found"
            for tx in block.txs:
                if tx.idf == "storage":
                    if tx.hash == filehash:
                        #function to retrieve file
                        self.retrieve_file(tx)
                        #send file
                        return "found"
            i = i + 1
        return "some error occured"

    def retrieve_file(self, tx):
        file_list = []
        for out in tx.outputs:
            #recv and store files
            file_list.append()
        self.file_merge(file_list)
        return

    def file_merge(self, file_list):
        filename = "compiled/retreived.format"
        fbl = []
        for file in file_list:
            filesize = os.path.getsize(file)
            # SPLIT_SIZE = math.ceil(filesize)
            with open(file, "rb") as f:
                bytes_read = f.read(filesize)
                fbl.append(bytes_read)

        with open(filename, "wb") as fs:
            for byt in fbl:
                fs.write(byt)
