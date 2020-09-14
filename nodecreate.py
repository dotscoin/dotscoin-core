import random
from dotscoin.Address import Address

def random_ip(num):
    ips = []
    for i in range(0, num):
        ip = str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255))
        ips.append(ip)
    return ips
    
def get_dns(n=15):
    nodes = dict()
    ips = random_ip(n)
    for i in range(0,n):
        getadd = Address()
        nodes[str(ips[i])] = str(getadd.get_public_address())
    return nodes


if __name__ == '__main__':
    nodes = []
    n = 15
    ips = random_ip(n)
    
    for i in range(0,n):
        getadd = Address()
        nodes.append({ips[i]: getadd.get_public_address()})
    print(nodes)