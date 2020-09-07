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
from bottle import route, run, template,get,post ,request,response
import bottle
import wsgiserver
host = '0.0.0.0'
port = 7000
def response_handler(data):
    context = zmq.Context()
    zsocket = context.socket(zmq.REQ)
    zsocket.connect("tcp://127.0.0.1:5558")
    zsocket.send_string(json.dumps(data))
    message = zsocket.recv()
    zsocket.close()
@get('/')
def listening_handler():
    '''Handles name creation'''
    # return 200 Success
    data= {"hello":"world"}
    return data
          
@post('/')
def posting_handler():
    data=request.json
    if "command" not in data.keys():
        return {"status":"rejected"}
    if "data" not in data.keys():
        return {"status":"rejected"}
    response_handler(data)
    return {"status":"ok"}
    
def rpc_receive():
    wsgiapp = bottle.default_app()
    httpd = wsgiserver.Server(wsgiapp)
    httpd.serve_forever()

