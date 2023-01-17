import logging
from wsgiref.simple_server import make_server
from flask import Flask
from flask_cors import CORS
from spyne.application import Application
from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.complex import Iterable
from spyne.model.primitive import UnsignedInteger,String
from spyne.server.wsgi import WsgiApplication

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

appp = Flask(__name__)

class HelloWorldService(ServiceBase):
    @srpc(String, UnsignedInteger, _returns=Iterable(String))
    def say_hello(name, times):
        for i in range(times):
            yield 'Hello, %s' % name

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
