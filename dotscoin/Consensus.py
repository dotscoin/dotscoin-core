import socket

class Consensus:
    def broadcast_transaction(self, transaction: str) -> None:
        node_list = []
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            for node in node_list:
                s.connect((node.host, node.port))
                s.sendall(transaction.decode())
                data = s.recv(1024)
