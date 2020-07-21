import urllib.request
import settings


class Election:
    """
        This class holds the nodes election every 30 seconds. A miner is being chosen
        from a list of primary representative.
    """
    def __init__(self):
        self.primary_representatives = dict()

    @staticmethod
    def load_all_nodes():
        """
            Loads all the primary representatives in the network.
        """
        nodes_list = urllib.request.urlopen("https://dns.dotscoin.com/nodes").read()


