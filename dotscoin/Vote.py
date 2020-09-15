from dotscoin.Address import Address
import json
import urllib.request

class Vote:
    ip_address: str = ""
    verifying_key: str = ""
    script_sig: str = ""
    representative: str = ""

    def __init__(self):
      response = urllib.request.urlopen("https://checkip.amazonaws.com/").read()
      self.ip_address = response.decode("utf-8").strip()
          
    def sign_vote(self, sk, vk):
        add = Address()
        add.load(sk, vk)
        self.script_sig = add.sign_message(json.dumps({
            "ip_address": self.ip_address,
            "representative": self.representative
        }))
        self.vk=vk

         
    
