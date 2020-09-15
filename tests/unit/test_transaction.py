import unittest
from dotscoin.Transaction import Transaction
from dotscoin.Block import Block
from dotscoin.TransactionInput import TransactionInput
from dotscoin.TransactionOutput import TransactionOutput

class TestTransaction(unittest.TestCase):

    def test_txs_by_address(self):
        block = Block()
        tx = Transaction()
        input = TransactionInput()
        input.address = "test_address"
        tx.add_input(input)
        tx.generate_hash()
        block.add_transaction(tx)

        tx1 = Transaction()
        output = TransactionOutput()
        output.address = "fake_address"
        tx1.add_output(output)
        output1 = TransactionOutput()
        output1.address = "test_address"
        tx1.add_output(output1)
        block.add_transaction(tx1)

        
