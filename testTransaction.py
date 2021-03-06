
import json
from dotscoin.Transaction import Transaction
from dotscoin.Block import Block
from dotscoin.BlockChain import BlockChain
from dotscoin.TransactionInput import TransactionInput
from dotscoin.TransactionOutput import TransactionOutput

class TestBlockChain():

    # def test_add_block(self):
    #     tx = Transaction()
    #     block = Block()
    #     tx.generate_hash()
    #     block.add_transaction(tx)

    #     blockchain = BlockChain()
    #     blockchain.flush_chain()
    #     blockchain.add_block(block)

    #     self.assertEqual(blockchain.get_length(), 1)
    #     blockchain.close()

    def test_txs_by_address(self):
        blockchain = BlockChain()
        blockchain.flush_chain()
        block = Block()
        tx = Transaction()
        input1 = TransactionInput()
        input1.address = "test_address"
        tx.add_input(input1)
        tx.generate_hash()
        block.add_transaction(tx)

        tx1 = Transaction()
        output = TransactionOutput()
        output.address = "fake_address"
        output1 = TransactionOutput()
        output1.address = "test_address"
        tx1.add_output(output)
        tx1.add_output(output1)
        tx1.generate_hash()
        block.add_transaction(tx1)

        tx2 = Transaction()
        output2 = TransactionOutput()
        output2.address = "fake_address"
        tx2.add_output(output2)
        tx2.generate_hash()
        
        block.add_transaction(tx2)
        block.compute_hash()

        blockchain.add_block(block)
        txs = blockchain.get_txs_by_addr("test_address")
        getb = blockchain.get_block(-1)
        print(getb.to_json())
        for tx in txs:
            print(tx.hash, end='\n')

        # self.assertEqual(len(txs), 2)
        print(len(txs))
        blockchain.close()


if __name__ == '__main__':
    tb = TestBlockChain()
    tb.test_txs_by_address()