
from dotscoin.Block import Block
from dotscoin.Transaction import Transaction
from dotscoin.TransactionInput import TransactionInput
from dotscoin.TransactionOutput import TransactionOutput
import sys
output=TransactionOutput()
output.address="1d3f347aada53547142da8edea5e0019e6ef31bb15"
output.n=0
output.value=50
transaction = Transaction()
transaction.add_output(output)
transaction.is_coinbase = True
transaction.generate_hash()
print('1')
block = Block("")
block.add_transaction(transaction)
print([transaction.hash])
block.calculate_merkle_root([transaction.hash])
print('3')
Block.hash=Block.compute_hash()
block.miner="1d3f347aada53547142da8edea5e0019e6ef31bb15"
block.size=sys.getsizeof(block)
print('4')
message= {
    "hash":block.hash,
    "timestamp":block.timestamp,
    "transaction":block.transactions[0].broadcast_transaction(),
    "previous_block_hash":block.previous_block_hash,
    "merkle_root":block.merkle_root,
    "confirmation":block.confirmation,
    "height":block.height,
    "miner":block.miner,
    "version":block.version,
    "size":block.size,
    "block_reward":block.block_reward,
    "fee":block.fee
}
print(message)