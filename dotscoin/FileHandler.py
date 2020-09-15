import hashlib
import os, random, struct
from Crypto.Cipher import AES
from Crypto import Random
import sys
import math
class FileHash:
    
    def __init__(self,path,parts):
        self.filepath=path
        self.block_size= 0
        self.parts=parts
        self.hash = []
        self.merkle_root:str = ""

    def get_hash(self):
       file_size= os.stat(self.filepath)
       self.block_size =math.ceil(file_size.st_size/self.parts)
       with open(self.filepath,"rb") as file:
           chunk = file.read(self.block_size)
           while chunk:
               hash= hashlib.sha256()
               hash.update(chunk)
               self.hash.append(hash.hexdigest())
               chunk = file.read(self.block_size)
       self.calculate_merkle_root(self.hash)

    def encrypt_file(self,key, out_filename=None, chunksize=64*1024):

        if not out_filename:
            out_filename = self.filepath + '.enc'

        iv = Random.new().read( AES.block_size )
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        filesize = os.path.getsize(self.filepath)

        with open(self.filepath, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += (' ' * (16 - len(chunk) % 16)).encode()

                    outfile.write(encryptor.encrypt(chunk))
        
    def decrypt_file(self,key, in_filename, out_filename=None, chunksize=64*1024):
 
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]
           # decrypted=out_filename[0]
        with open(in_filename, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(origsize)
        
    def calculate_merkle_root(self, transactions=[]):
        new_tran = []
        if len(transactions) > 1:
            if transactions[-1] == transactions[-2]:
                return ""
        for i in range(0, len(transactions), 2):
            h = hashlib.sha256()
            if i+1 == len(transactions):
                h.update(
                    ((transactions[i]) + (transactions[i])).encode("UTF-8"))
                new_tran.append(h.hexdigest())
            else:
                h.update(
                    ((transactions[i]) + (transactions[i+1])).encode("UTF-8"))
                new_tran.append(h.hexdigest())

        if len(new_tran) == 1:
            self.merkle_root = new_tran[0]
            return
        else:
            self.calculate_merkle_root(new_tran)