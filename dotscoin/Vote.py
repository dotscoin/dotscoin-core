from dotscoin.Address import Address
import json
import urllib.request

class Vote:

    def __init__(self):
      response = urllib.request.urlopen("https://checkip.amazonaws.com/").read()
      self.ip_address = response.decode("utf-8").strip()
      self.verifying_key: str = ""
      self.script_sig: str = ""
      self.representative: str = ""
          
    def sign_vote(self, sk, vk):
        add = Address()
        add.load(sk, vk)
        self.script_sig = add.sign_message(json.dumps({
            "ip_address": self.ip_address,
            "representative": self.representative
        }))
        self.vk=vk

         
    
