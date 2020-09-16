import os
from ecdsa import NIST384p, SigningKey
from ecdsa.util import randrange_from_seed__trytryagain
from mnemonic import Mnemonic

class Mnemonic:

    mnemo = Mnemonic("english")

    def gen_words(self):
        words = self.mnemo.generate(strength=128)
        return words

    def gen_seed(self, words, passphrase=""):
        seed = self.mnemo.to_seed(words, passphrase="")
        return seed
    
    def make_Skey(self, seed):
        secexp = randrange_from_seed__trytryagain(seed, NIST384p.order)
        return SigningKey.from_secret_exponent(secexp, curve=NIST384p)

    def make_Vkey(self, Skey):
        return Skey.verifying_key

# if __name__ == "__main__":
#     mn = Mnemonic()
#     words = mn.gen_words()
#     seed = mn.gen_seed(words)
#     sk = mn.make_Skey(seed)
#     vk = mn.make_Vkey(sk)
