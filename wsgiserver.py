
from wsgiref.simple_server import make_server, WSGIServer
import socketserver
import settings
host='0.0.0.0'
port=settings.RPC_PORT
class ThreadingWSGIServer(socketserver.ThreadingMixIn, WSGIServer):
    daemon_threads = True

class Server:
    def __init__(self, wsgi_app, listen=host,port=port):
        self.wsgi_app = wsgi_app
        self.listen = listen
        self.port = port
        self.server = make_server(self.listen, self.port, self.wsgi_app,
                                  ThreadingWSGIServer)
   
    def serve_forever(self):
        print("rpc server  started on:",host,port)
        self.server.serve_forever()