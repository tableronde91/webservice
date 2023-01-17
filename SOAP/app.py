from flask import Flask
from spyne import Application, srpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class HelloWorldService(ServiceBase):
    @srpc(Unicode, Integer, _returns=Unicode)
    def say_hello(name, times):
        result = ""
        for i in range(times):
            result += "Hello, %s! " % name
        return result

app = Flask(__name__)

@app.route("/soap", methods=['POST'])
def soap():
    application = Application([HelloWorldService], "spyne.examples.hello.soap",
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11()
    )
    wsgi_app = WsgiApplication(application)
    return wsgi_app

if __name__ == "__main__":
    app.run(port=8060)

