import zmq
import json

context = zmq.Context()
print("Connecting to Server on port 5555")
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

transactions = [{"hash": "yutf86r86riy3yqo", "value":"123445"},{"hash": "yutf86r86riy3yqo", "value":"123445"},{"hash": "yutf86r86riy3yqo", "value":"123445"},{"hash": "yutf86r86riy3yqo", "value":"123445"},{"hash": "yutf86r86riy3yqo", "value":"123445"}]


print("Sending transactions")
socket.send_string(json.dumps(transactions))

#  Get the reply.
message = socket.recv()
print(message)