import json
import logging
from wsgiref.simple_server import make_server
from flask import Flask, request
import requests
from spyne.application import Application
from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.complex import Iterable
from spyne.model.primitive import UnsignedInteger,String, Integer
from spyne.server.wsgi import WsgiApplication

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

appp = Flask(__name__)

docker = True
if docker:
    domain = "http://localhost:8888"
else:
    domain = "http://127.0.0.1:5000"

class HelloWorldService(ServiceBase):
    @srpc(String, UnsignedInteger, _returns=Iterable(String))
    def say_hello(name, times):
        for i in range(times):
            yield 'Hello, %s' % name
    @srpc(_returns=Iterable(String))
    def get_all_trains():
        response = requests.get(domain+'/trains')
        trains = response.json()
        yield str(trains)
    @srpc(Integer, String, Integer, _returns=Iterable(String))
    def reserve_outbound(train_id,classe,places):
        data = {
            "classe": classe,
            "nb_ticket": places
        }
        response = requests.put(domain+'/revervation/train/'+str(train_id),json=data)
        result = response.json()

        yield str(result)


app = Application([HelloWorldService], 'spyne.examples.hello.http',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11(),
    )
wsgi_app = WsgiApplication(app)

server = make_server('127.0.0.1', 7789, wsgi_app)

print ("listening to http://127.0.0.1:7789")
print ("wsdl is at: http://localhost:7789/?wsdl")

server.serve_forever()

if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)    

server = make_server('127.0.0.1', 7789, app)
server.serve_forever()
