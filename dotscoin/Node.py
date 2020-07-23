import socket


class Node:
    def __init__(self):
        self.ip_address: str = ""
        pass

    def load_own_node(self):
        hostname = socket.gethostname()
        self.ip_address = socket.gethostbyname(hostname)
