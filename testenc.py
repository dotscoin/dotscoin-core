from dotscoin.FileHandler import FileHash

file = FileHash("genesisblock.json",10)
file.get_hash()
print(file.hash)
print(file.merkle_root)