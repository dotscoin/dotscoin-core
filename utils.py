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

def decode_redis(src):
    if isinstance(src, list):
        rv = list()
        for key in src:
            rv.append(decode_redis(key))
        return rv
    elif isinstance(src, dict):
        rv = dict()
        for key in src:
            rv[key.decode()] = decode_redis(src[key])
        return rv
    elif isinstance(src, bytes):
        return src.decode()
    else:
        raise Exception("type not handled: " +type(src))