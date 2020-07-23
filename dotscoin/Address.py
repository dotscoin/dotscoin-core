from typing import Any
from ecdsa import VerifyingKey, SigningKey, BadSignatureError
import hashlib

class Address:
    def __init__(self):
        self.sk = SigningKey.generate()
        self.vk = self.sk.verifying_key

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
