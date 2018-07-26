# coding=utf-8

import time
import threading

from poco.sdk.std.rpc.controller import StdRpcEndpointController
from poco.sdk.std.rpc.reactor import StdRpcReactor
from poco.utils.net.transport.tcp import TcpSocket
from poco.utils.net.stdbroker import StdBroker


def Dump(arg):
    return 'this is Dump ' + arg


if __name__ == '__main__':
    # broker = StdBroker('tcp://*:15003', 'tcp://*:15004')

    reactor = StdRpcReactor()
    reactor.register('Dump', Dump)

    responser = TcpSocket()
    responser.connect(('localhost', 15003))

    rpc_responser = StdRpcEndpointController(responser, reactor)
    t = threading.Thread(target=rpc_responser.serve_forever)
    t.daemon = True
    t.start()

    requester = TcpSocket()
    requester.connect(('localhost', 15004))
    rpc_requester = StdRpcEndpointController(requester, StdRpcReactor())
    t = threading.Thread(target=rpc_requester.serve_forever)
    t.daemon = True
    t.start()

    requester = TcpSocket()
    requester.connect(('localhost', 15004))
    rpc_requester2 = StdRpcEndpointController(requester, StdRpcReactor())
    t = threading.Thread(target=rpc_requester2.serve_forever)
    t.daemon = True
    t.start()


    print(1111, rpc_requester.call('Dump', '111111'))
    print(2222, rpc_requester2.call('Dump', '222222'))

    while True:
        time.sleep(1)
