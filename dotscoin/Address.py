import hashlib
import json
import redis
from typing import Any
from ecdsa import VerifyingKey, SigningKey, BadSignatureError

class Address:
    def __init__(self):
        self.sk = SigningKey.generate()
        self.vk = self.sk.verifying_key
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

    def load(self, sk, vk) -> None:
        """ Loads Signing Key and Verifying key from external source."""
        self.sk = SigningKey.from_pem(sk)
        self.vk = VerifyingKey.from_pem(vk)

    def sign_message(self, message) -> Any:
        """ Signs the message for user authentication """
        return self.sk.sign(message)

    def verify_signature(self, message, signature) -> bool:
        try:
            self.vk.verify(signature, message)
            return True
        except BadSignatureError:
            return False

    def display(self):
        print(self.vk.to_string().hex())

    def get_public_address(self) -> str:
        sha_hash_pk = hashlib.sha256(self.vk.to_string().hex().encode('utf-8')).hexdigest()
        h = hashlib.new('ripemd160')
        h.update(sha_hash_pk.encode('utf-8'))

        return h.hexdigest()

    def export(self) -> dict:
        return {
            'vk': self.vk.to_pem().decode("utf-8"),
            'sk': self.sk.to_pem().decode("utf-8")
        }

    def total_value(self, addr):
        i = 1
        total = 0
        while True:
            block = json.loads(self.redis_client.lindex('chain', i).decode('utf-8'))
            if block == None:
                return total
            for tx in block.txs:
                for input in tx.inputs:
                    if input.address == addr:
                        total = total + input.value
                for out in tx.outputs:
                    if out.address == addr:
                        total = total - out.value
            i = i + 1
        return total

    



