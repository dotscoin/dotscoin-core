import socket
from utils import get_own_ip, handle_network_error
import settings
import json
import urllib
from urllib.error import URLError
import redis
from dotscoin.Address import Address
from os import path


class Node:
    def __init__(self):
        self.dns_fetch()
        self.dns_push()

    def dns_push(self):
        my_node_info = self.load_node_json()
        headers = {'Content-Type': "application/json"}
        data = json.dumps({
            "ip_addr": get_own_ip(),
            "node_addr": my_node_info["address"],
            "receiver_port": settings.UDP_RECEIVER_PORT,
            "rpc_port": settings.RPC_PORT,
            "storage_port": settings.FILE_RECV_PORT
        })

        for url in settings.DNS_SERVERS:
            req = urllib.request.Request(
                url + "/add_node", data.encode(), headers)
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
                    pipe.hset(
                        "nodes_map", value["ip_addr"], value["node_addr"])
        pipe.execute()
        redis_client.close()

    def load_node_json(self):
        if not path.exists("node_data.json"):
            create_file = open("node_data.json", "x")
            create_file.close()
        read_file = open("node_data.json", "r")
        raw = read_file.read()
        if len(raw) == 0:
            addr = Address()
            add_data = addr.export()
            my_node = {
                **add_data,
                'address': addr.get_public_address()
            }
            write_file = open("node_data.json", 'w')
            write_file.write(json.dumps(my_node))
            write_file.close()

            return my_node
        else:
            try:
                my_node = json.loads(raw)
                return my_node
            except ValueError:
                print('Error: The json is malformed in node_data.json. Please fix the file or delete it.\n(Note: Deleting this file will cause your node main wallet signing key to be lost.)')
                exit()
            read_file.close()
