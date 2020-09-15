from dotscoin.RPC import RPC
from dotscoin.Mempool import Mempool
from dotscoin.Transaction import Transaction
import time
import sys
import socket
import http.server
import selectors
import types
import json
import cgi
import socketserver
import threading
import zmq
import settings
from bottle import route, run, template, get, post, request, response
import bottle
import wsgiserver
host = '0.0.0.0'
port = settings.RPC_PORT


def response_handler(data):
    rpc = RPC()
    response = rpc.handlecommand(data)

    return response


@post('/')
def posting_handler():
    data = request.json
    if "command" not in data.keys():
        return {"status": "rejected"}
    if "data" not in data.keys():
        return {"status": "rejected"}
    response_handler(data)
    return {"status": "ok"}


def rpc_receive():
    print("Starting RPC Server at port %s" % settings.RPC_PORT)
    wsgiapp = bottle.default_app()
    httpd = wsgiserver.Server(wsgiapp)
    httpd.serve_forever()
