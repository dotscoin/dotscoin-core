import urllib.request
import settings
from dotscoin.BlockChain import BlockChain
from dotscoin.Verification import Verification
from dotscoin.Transaction import Transaction
from dotscoin.Election import Election
from dotscoin.Block import Block
import json
from collections import defaultdict
import random
import zmq
import time
import redis
import threading
import urllib.request
import settings


def bestblock(merkle_roots=[]):
    key_value = dict()
    max = []
    for i, merkle_root in enumerate(merkle_roots):
        if not merkle_root in key_value.keys():
            key_value[merkle_root] = 1
        else:
            key_value[merkle_root] += 1

    for key in key_value.keys():
        max.append(key_value[key])
        max.sort(reverse=True)
    for key in key_value.keys():
        if key_value[key] == max[0]:
            print(key)
            return key


def worker():
    elec = Election()
    # elec.election_fund()
    elec.get_stakes()
    elec.vote_to()
    print("vote sent and waiting for other's votes")
    context = zmq.Context()
    zsocket = context.socket(zmq.REP)
    zsocket.bind("tcp://127.0.0.1:%s" % settings.ELECTION_ZMQ_PORT)
    zpoll = zmq.Poller()
    zpoll.register(zsocket)
    start_timestamp = time.time()
    while time.time() - start_timestamp < 25:
        events = dict(zpoll.poll(1))
        for key in events:
            vote = json.loads(key.recv_string())
            elec.add_vote(vote)
            zsocket.send_string("got some nodes vote")
    zpoll.unregister(zsocket)
    zsocket.close()
    context.destroy()

    return elec.delegates()


def mining():
    elec = Election()
    if elec.redis_client.llen("mempool") == 0:
        return
    blk = Block()
    for i in range(0, elec.redis_client.llen("mempool")):
        tx = elec.redis_client.lindex('mempool', i).decode('utf-8')
        if tx == None:
            continue
        verify_verdict = elec.verification.verify_tx(tx)
        if verify_verdict == "verified":
            # Sending data to block
            blk.add_transaction(tx)

    # create block
    blk.compute_hash()
    blk.calculate_merkle_root()
    block = blk.to_json()

    # add block
    blkChain = BlockChain()
    blkChain.add_block(block)

    # full blockchain verify
    full_verify_message = elec.verification.full_chain_verify()
    if full_verify_message == "verified":
        # braodcast the block you made
        context = zmq.Context()
        z4socket = context.socket(zmq.REQ)
        z4socket.connect("tcp://127.0.0.1:%s" %
                            settings.BROADCAST_ZMQ_PORT)
        z4socket.send_string(json.dumps(
            {'data': block, 'command': 'addblock'}))
        message = z4socket.recv()
        z4socket.close()
    else:
        return


def electionworker():
    elec = Election()
    elec.get_node_addr()
    dels = worker()
    print("yes")
    is_del = False
    if dels.count(elec.this_node_addr) > 0:
        is_del = True
        mining()
    if is_del == False:
        pass
        # full_verify_message = Election.verification.full_chain_verify()


def add_block_nondel():
    context = zmq.Context()
    zsocket = context.socket(zmq.REP)
    zsocket.bind("tcp://127.0.0.1:%s" % settings.ELECTION_ZMQ_PORT)
    zpoll = zmq.Poller()
    zpoll.register(zsocket)
    start_timestamp = time.time()
    all_blocks = []
    while time.time() - start_timestamp < 3:
        events = dict(zpoll.poll(1))
        for key in events:
            block = json.loads(key.recv_string())
            print(block)
            all_blocks.append(block)
            zsocket.send_string("got some block")
    zpoll.unregister(zsocket)
    zsocket.close()
    context.destroy()
    # get most common and add to chain
    if len(all_blocks) > 0:
        print(all_blocks)
        mr = []
        for blk in all_blocks:
            mr.append(blk.merkle_root)
        # run full blockchain verif
        blkc = BlockChain()
        Mblock = bestblock(mr)
        blkc.add_block(Mblock)


def mining():
    vf = Verification()
    print(vf.full_chain_verify())


def run_thread():
    print("Starting Election/Mining rocess")
    # t = threading.Thread(target=mining)
    t = threading.Thread(target=electionworker)
    t.start()
    t.join()
    t = threading.Thread(target=add_block_nondel)
    t.start()
    t.join()
