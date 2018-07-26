# coding=utf-8

import json
import time

from poco.utils import six


class RpcRemoteException(Exception):
    pass


class StdRpcEndpointController(object):
    def __init__(self, transport, reactor):
        super(StdRpcEndpointController, self).__init__()
        self.transport = transport
        self.reactor = reactor

    def deserialize(self, data):
        if six.PY3 and not isinstance(data, six.text_type):
            data = data.decode('utf-8')
        return json.loads(data)

    def serialize(self, packet):
        return json.dumps(packet)

    def serve_forever(self):
        while True:
            cid, data = self.transport.update()
            if data:
                packet = self.deserialize(data)
                if 'method' in packet:
                    result = self.reactor.handle_request(packet)
                    sres = self.serialize(result)
                    self.transport.send(cid, sres)
                else:
                    self.reactor.handle_response(packet)

    def call(self, method, *args, **kwargs):
        req = self.reactor.build_request(method, *args, **kwargs)
        rid = req['id']
        sreq = self.serialize(req)
        self.transport.send(None, sreq)
        while True:
            time.sleep(0.004)
            res = self.reactor.get_result(rid)
            if res is not None:
                if 'result' in res:
                    return res['result']

                if 'error' in res:
                    raise RpcRemoteException(res['error']['message'])

                raise RuntimeError('Invalid response from {}. Got {}'.format(self.transport, res))