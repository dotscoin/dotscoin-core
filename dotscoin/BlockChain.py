from typing import List
from Block import Block


class BlockChain:
    def __init__(self):
        self.data = ""
        self.blocks: List[Block] = []

    def load(self):
        file = open("chain.txt", "r")
        print(file.read())
        self.data = file.read()
        file.close()

    def save(self):
        file = open("chain.txt", "w")
        file.write(self.data)
        file.close()
