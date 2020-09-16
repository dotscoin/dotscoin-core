import socket
from urllib.error import URLError

def get_own_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def handle_network_error(e: URLError):
    if hasattr(e, 'reason'):
        print('Failed to reach DNS server.')
    elif hasattr(e, 'code'):
        print('The server couldn\'t fulfill the request.')