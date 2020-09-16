import socket
from utils import get_own_ip, handle_network_error
import settings
import json
import urllib
from urllib.error import URLError
import redis

class Node:
    def __init__(self):
        self.dns_fetch()
        self.dns_push()

    def dns_push(self):
        headers = {'Content-Type': "application/json"}
        data = json.dumps({
                "ip_addr": get_own_ip(),
                "node_addr": "",
                "receiver_port": settings.UDP_RECEIVER_PORT,
                "rpc_port": settings.RPC_PORT,
                "storage_port": settings.FILE_RECV_PORT
            })

        for url in settings.DNS_SERVERS:
            req = urllib.request.Request(url + "/add_node", data.encode(), headers)
            try:
                response = urllib.request.urlopen(req)
            except URLError as e:
                handle_network_error(e)
            else:
                result = response.read()
                print(result)

    def dns_fetch(self):
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        pipe = redis_client.pipeline()
        for url in settings.DNS_SERVERS:
            try:
                response = urllib.request.urlopen(url + "/get_nodes")
            except URLError as e:
                handle_network_error(e)
            else:
                raw = response.read()
                result = json.loads(raw.decode("utf-8"))
                for value in result["nodes"]:
                    pipe.hset("nodes_map", value["ip_addr"], value["node_addr"])
        pipe.execute()
        redis_client.close()