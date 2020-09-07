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

context = zmq.Context()
socke = context.socket(zmq.REQ)
socke.connect("tcp://127.0.0.2:5555")

@get('/')
def listening_handler():
    '''Handles name creation'''
    # return 200 Success
    data= {"hello":"world"}
    return data
          
@post('/')
def posting_handler():
    body=request.json
    socke.send_string(json.dumps(body))
    return {"status":"ok"}
    
def rpc_receive():
    wsgiapp = bottle.default_app()
    httpd = wsgiserver.Server(wsgiapp)
    httpd.serve_forever()  

