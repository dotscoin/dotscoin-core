import math
import os
import json
import hashlib

def file_split(filename, n):
    file_list = []
    filesize = os.path.getsize(filename)
    SPLIT_SIZE = math.ceil(filesize / n)
    with open(filename, "rb") as f:
        i = 0
        while True:
            bytes_read = f.read(SPLIT_SIZE)
            if not bytes_read:
                break
            # hash = hashlib.sha256(json.dumps(bytes_read).encode("utf-8")).hexdigest()
            file_list.append(bytes_read)
            i = i + 1
    
    for i in range(0,n):
        filename = "output" + str(i) + ".mkv"
        with open(filename, "wb") as f:
            f.write(file_list[i])

def file_merge(file_list):
    filename = "compiled.mkv"
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



if __name__ == "__main__":
    # file_split("/home/rishav4101/12345.mkv", 5)
    file_list = ["/home/rishav4101/dotscoin-core/output0.mkv", "/home/rishav4101/dotscoin-core/output1.mkv", "/home/rishav4101/dotscoin-core/output2.mkv", "/home/rishav4101/dotscoin-core/output3.mkv", "/home/rishav4101/dotscoin-core/output4.mkv"]
    file_merge(file_list)

