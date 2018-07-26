# coding=utf-8

import time
import threading
import uuid

from poco.sdk.std.transport import Transport
from poco.utils import six
from poco.utils.net.transport.simple_wss import SimpleWebSocketServer, WebSocket

if six.PY3:
    from queue import Queue, Empty
else:
    from Queue import Queue, Empty


class WsSocket(Transport):
    def __init__(self):
        super(WsSocket, self).__init__()
        self.s = None
        self.connections = {}  # websocket client object -> cid
        self.connections_endpoints = {}  # endpoint -> websocket client object
        self.rq = Queue()

    def connect(self, endpoint):
        raise NotImplementedError

    def disconnect(self, endpoint=None):
        raise NotImplementedError

    def bind(self, endpoint):
        if self.s is not None:
            raise RuntimeError("Already bound at {}".format((self.s.serversocket.getsockname())))

        ip, port = endpoint
        if ip in ('', '*', '0'):
            ip = '0.0.0.0'

        class MyWsApp(WebSocket):
            def handleConnected(self2):
                self.connections[self2] = six.text_type(uuid.uuid4())
                self.connections_endpoints[self2.address] = self2
                print('server on accept. {}'.format(self2))

            def handleMessage(self2):
                print('received_message from {}: {}'.format(self2.address, self2.data))
                cid = self.connections.get(self2)
                if cid:
                    self.rq.put((cid, self2.data))

            def handleClose(self2):
                self.connections.pop(self2, None)
                self.connections_endpoints.pop(self2.address, None)
                print('client gone. {}'.format(self2.address))

        self.s = SimpleWebSocketServer(ip, port, MyWsApp)
        t = threading.Thread(target=self.s.serveforever)
        t.daemon = True
        t.start()
        print('server listens on ("{}", {}) transport websocket'.format(ip, port))

    def update(self, timeout=0.001):
        time.sleep(timeout)
        return self.recv()

    def recv(self):
        try:
            return self.rq.get(False)
        except Empty:
            return None, None

    def send(self, cid, data):
        if cid is None:
            # broadcast
            for conn, _ in self.connections.items():
                conn.sendMessage(data)
        else:
            conn = self.get_connection(cid)
            if conn:
                conn.sendMessage(data)

    def get_connection(self, cid_):
        for conn, cid in self.connections.items():
            if cid == cid_:
                return conn
        return None

    def __str__(self):
        return 'Websocket connection(s) at {}'.format(self.connections_endpoints.keys())

    __repr__ = __str__
