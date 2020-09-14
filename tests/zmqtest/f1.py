import time
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5555")

while True:
    #  Wait for next request from client
    txs = json.loads(socket.recv_string())
    print("Received txs")
    print(txs)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send_string("recieved your transactions")