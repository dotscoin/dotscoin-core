
from dotscoin.Block import Block
from dotscoin.Transaction import Transaction
from dotscoin.TransactionInput import TransactionInput
from dotscoin.TransactionOutput import TransactionOutput
import time
import sys
from utils import getsize,getbytes
output=TransactionOutput()
output.address="1d3f347aada53547142da8edea5e0019e6ef31bb15"
output.n=0
output.value=50
transaction = Transaction()
transaction.add_output(output)
transaction.is_coinbase = True
transaction.hash="eef9fda50a6bf6c11c5078d8772d94jk"
block = Block()
block.add_transaction(transaction)
block.calculate_merkle_root()
block.compute_hash()
block.miner="1d3f347aada53547142da8edea5e0019e6ef31bb15jk"
block.size=getbytes(block)
print(block.__dict__)
message= {
    "hash":block.hash,
    "timestamp":block.timestamp,
    "transaction":block.transactions[0].broadcast_transaction(),
    "previous_block_hash":block.previous_block_hash,
    "merkle_root":block.merkle_root,
    "height":block.height,
    "miner":block.miner,
    "version":block.version,
    "size":block.size
}
size=0
for key in message.keys():
    size +=sys.getsizeof(message[key])

print(size)
print(message)