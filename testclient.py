import socket
import json
sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0',7002))
data =json.dumps({"hello":"there"})
sock.sendto(data.encode('utf-8'),("15.207.11.83",6040)) 