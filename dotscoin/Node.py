import socket

class Node:

    ip_address: str = ""

    def load_own_node(self):
        hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(hostname)
