# all imports
import hashlib
import json
import redis
from typing import Any
# ECDSA algo for key generation
from ecdsa import VerifyingKey, SigningKey, BadSignatureError

class Address:
    """Address class to generate the public addresses. Eg: address of this node"""
    
    def __init__(self):
        """ Initializations, generation of signing key and verifying key,
        and connecting to the Redis database where everything is stored """
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
        """ Returns True if the signature is verified else False """
        try:
            self.vk.verify(signature, message)
            return True
        except BadSignatureError:
            return False

    def display(self):
        """ Function to display the verifying key """
        print(self.vk.to_string().hex())

    def get_public_address(self) -> str:
        """ Final generation of public address by making us of
        --> SHA256, ripemd160. Encoding method -> utf-8 """
        sha_hash_pk = hashlib.sha256(self.vk.to_string().hex().encode('utf-8')).hexdigest()
        h = hashlib.new('ripemd160')
        h.update(sha_hash_pk.encode('utf-8'))

        return h.hexdigest()

    def export(self) -> dict:
        """ Exports the signing key and verifying key """
        return {
            'vk': self.vk.to_pem().decode("utf-8"),
            'sk': self.sk.to_pem().decode("utf-8")
        }

    def total_value(self, addr):
        """ This function scans the complete blockchain and returns
        the total balance of an Address """
        i = 1
        total = 0
        while True:
            block = json.loads(self.redis_client.lindex('chain', i).decode('utf-8'))
            if block == None:
                return total
            for tx in block.txs:
                for input in tx.inputs:
                    if input.address == addr:
                        # adding up inputs
                        total = total + input.value
                for out in tx.outputs:
                    if out.address == addr:
                        # subtracting outputs
                        total = total - out.value
            i = i + 1
        return total

    



