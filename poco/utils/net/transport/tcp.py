# coding=utf-8

import errno
import socket
import select
import uuid

from poco.sdk.std.transport import Transport
from poco.sdk.std.protocol import SimpleProtocolFilter
from poco.utils import six

if six.PY3:
    from queue import Queue, Empty
else:
    from Queue import Queue, Empty


class ConnectionReset(Exception):
    pass


class Connection(object):
    def __init__(self, cid, sock, endpoint, RX_SIZE=65536):
        super(Connection, self).__init__()
        self.cid = cid
        self.sock = sock
        self.endpoint = endpoint
        self.p = SimpleProtocolFilter()
        self.RX_SIZE = RX_SIZE

    def send(self, packet):
        data = self.p.pack(packet)
        self.sock.sendall(data)

    def recv(self):
        rxdata = ''
        try:
            rxdata = self.sock.recv(self.RX_SIZE)
        except socket.error as e:
            if e.errno in (errno.ECONNRESET, ):
                raise ConnectionReset

        if not rxdata:
            self.close()
            raise ConnectionReset
        else:
            for packet in self.p.input(rxdata):
                yield packet

    def close(self):
        try:
            self.sock.close()
        except socket.error:
            pass

    def get_socket_object(self):
        return self.sock


class TcpSocket(Transport):
    def __init__(self, RX_SIZE=65536):
        super(TcpSocket, self).__init__()
        # active socket object
        self.s = None
        self.connections = {}  # sock -> Connection
        self.connections_endpoints = {}  # endpoint -> Connection

        self.rq = Queue()
        self.RX_SIZE = RX_SIZE

    def connect(self, endpoint):
        if endpoint in self.connections_endpoints:
            raise RuntimeError("Already connected to {}".format(endpoint))

        c = socket.socket()
        c.connect(endpoint)
        cid = six.text_type(uuid.uuid4())
        conn = Connection(cid, c, endpoint, self.RX_SIZE)
        self.connections[c] = conn
        self.connections_endpoints[endpoint] = conn

    def disconnect(self, endpoint=None):
        if endpoint is not None:
            conn = self.connections_endpoints.pop(endpoint, None)
            if conn:
                self.connections.pop(conn.get_socket_object(), None)
                conn.close()
        else:
            for _, conn in self.connections_endpoints.items():
                conn.close()
            self.connections_endpoints = {}
            self.connections = {}

    def bind(self, endpoint):
        if self.s is not None:
            raise RuntimeError("Already bound at {}".format(self.s.getsockname()))

        ip, port = endpoint
        if ip in ('', '*', '0'):
            ip = '0.0.0.0'
        self.s = socket.socket()
        self.s.bind((ip, port))
        self.s.listen(10)
        print('server listens on ("{}", {}) transport socket'.format(ip, port))

    def update(self, timeout=0.002):
        rlist = []
        if self.s is not None:
            rlist.append(self.s)
        rlist.extend(self.connections.keys())
        r, _, _ = select.select(rlist, [], [], timeout)
        for c in r:
            if c is self.s:
                client_sock, endpoint = self.s.accept()
                print('accept from: {}'.format(endpoint))
                cid = six.text_type(uuid.uuid4())
                conn = Connection(cid, client_sock, endpoint, self.RX_SIZE)
                self.connections[client_sock] = conn
                self.connections_endpoints[endpoint] = conn
            else:
                conn = self.connections.get(c)
                if not conn:
                    continue

                try:
                    for packet in conn.recv():
                        self.rq.put((conn.cid, packet))
                except ConnectionReset:
                    self.connections.pop(c)

        return self.recv()

    def recv(self):
        try:
            return self.rq.get(False)
        except Empty:
            return None, None

    def send(self, cid, packet):
        if cid is None:
            # broadcast
            for _, conn in self.connections.items():
                conn.send(packet)
        else:
            conn = self.get_connection(cid)
            if conn:
                conn.send(packet)

    def get_connection(self, cid):
        for sock, conn in self.connections.items():
            if conn.cid == cid:
                return conn
        return None

    def __str__(self):
        return 'Tcp connection(s) at {}'.format(self.connections_endpoints.keys())

    __repr__ = __str__
