import unittest
from dotscoin.Transaction import Transaction
from dotscoin.Block import Block
from dotscoin.BlockChain import BlockChain
from dotscoin.TransactionInput import TransactionInput
from dotscoin.TransactionOutput import TransactionOutput

class TestTransaction(unittest.TestCase):

    def test_add_block(self):
        tx = Transaction()
        block = Block()
        tx.generate_hash()
        block.add_transaction(tx)

        blockchain = BlockChain()
        blockchain.flush_chain()
        blockchain.add_block(block)

        self.assertEqual(blockchain.get_length(), 1)
        blockchain.close()

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

        blockchain = BlockChain()
        blockchain.flush_chain()
        blockchain.add_block(block)
        txs = blockchain.get_all_txs_by_address("test_address")

        self.assertEqual(len(txs), 2)


if __name__ == '__main__':
    unittest.main()