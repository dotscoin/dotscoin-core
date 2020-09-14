from dotscoin.FileHandler import FileHash
import hashlib

password = 'kitty'
key = hashlib.sha256(password.encode()).digest()

file = FileHash("tests/test.zip",10)
file.get_hash()
print(file.hash)
print(file.merkle_root)
file.encrypt_file(key)