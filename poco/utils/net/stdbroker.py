# coding=utf-8

import json
import threading

from poco.utils.net.transport.ws import WsSocket
from poco.utils.net.transport.tcp import TcpSocket
from poco.utils import six

if six.PY3:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse


class StdBroker(object):
    def __init__(self, ep1, ep2):
        super(StdBroker, self).__init__()

        # always ep2  --request---> ep1
        #        ep2 <--response--  ep1
        self.ep1 = self._make_transport(ep1)
        self.ep2 = self._make_transport(ep2)
        self.requests_map = {}  # reqid -> requester cid

        self.t = threading.Thread(target=self.loop)
        self.t.daemon = True
        self.t.start()

    def _make_transport(self, ep):
        ep = urlparse(ep)
        if ep.scheme.startswith('ws'):
            transport = WsSocket()
        else:
            transport = TcpSocket()
        transport.bind((ep.hostname, ep.port))
        return transport

    def deserialize(self, data):
        if six.PY3 and not isinstance(data, six.text_type):
            data = data.decode('utf-8')
        return json.loads(data)

    def serialize(self, packet):
        return json.dumps(packet)

    def handle_request(self):
        cid, data = self.ep2.update()
        if data:
            packet = self.deserialize(data)
            reqid = packet['id']
            self.requests_map[reqid] = cid
            self.ep1.send(None, data)

    def handle_response(self):
        _, data = self.ep1.update()
        if data:
            packet = self.deserialize(data)
            reqid = packet['id']
            cid = self.requests_map.pop(reqid, None)
            if cid:
                self.ep2.send(cid, data)

    def loop(self):
        print('StdBroker on.')
        while True:
            self.handle_request()
            self.handle_response()


if __name__ == '__main__':
    import sys
    import time

    if len(sys.argv) < 3:
        print('Not enough arguments. Please provide at least 2 endpoints.')
        print('e.g. ws://*:15003 tcp://*:15004')
        exit(-1)
    rpt = StdBroker(sys.argv[1], sys.argv[2])

    while True:
        time.sleep(5)
