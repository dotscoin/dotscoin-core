import unittest
from dotscoin.Address import Address

class TestAddress(unittest.TestCase):

    def gen_words(self):
        add = Address()
        print(add.gen_words())


if __name__ == '__main__':
    unittest.main()