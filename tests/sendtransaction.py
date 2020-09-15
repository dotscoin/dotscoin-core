import requests
import json
import time

if __name__ == '__main__':
    tx = {
        'timestamp': time.time(),
        'version': '0.0.2',
        'inputs': [
            {
                "previous_tx": "oihrsgiohsioj9ih05i0yu9u59y8o4yu54h",
                "index": 3,
                "scriptSig": ["segbikldrih95euy9u4509uyh90e9p4ujy"],
                "verifying_key": ["jlbuigfuiga89y89egyg8w4oig8gw"]
            }
        ],
        'outputs': [
            {
                'value': 5,
                'n': 0,
                'address': '1d3f347aada53547142da8edea5e0019e6ef31bb15'
            }
        ],
        'hash': 'eef9fda50a6bf6c11c5078d8772d94df4f60ce54573c009f145eb047426ad0fb',
        'block': 'testchain',
        'is_coinbase': False
    }

    url = "http://localhost:8000/"
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTk4Mjk4ODIyLCJqdGkiOiJkNDQ1MDZkNmJjOGY0NjQxYWJlNmQyMzI2NzI5OTI5MCIsInVzZXJfaWQiOjF9.zk3CUn8XXvhZE0WsARUzr2IogPfB3XPzAp68zgJ7Kus',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps({
        'command': 'addtransaction',
        'body': tx
    }))
