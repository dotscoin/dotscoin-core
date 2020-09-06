
from dotscoin.Block import Block
from dotscoin.Transaction import Transaction
from dotscoin.TransactionInput import TransactionInput
from dotscoin.TransactionOutput import TransactionOutput

output=TransactionOutput()
output.address="1d3f347aada53547142da8edea5e0019e6ef31bb15"
output.n=0
output.value=50
transaction = Transaction()
transaction.add_output(output)
transaction.is_coinbase = True
transaction.generate_hash()
block = Block('')
block.add_transaction(transaction)
block.calculate_merkle_root([transaction.hash])
block.miner="1d3f347aada53547142da8edea5e0019e6ef31bb15"
block
Block.merkle_root=Block.calculate_merkle_root()
Block.hash=Block.compute_hash()
