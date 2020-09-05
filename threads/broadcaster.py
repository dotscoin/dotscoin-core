import sys
import time
from bottle import route, run, template
def broadcast_election():
    run(host='0.0.0.0', port=8080)


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

