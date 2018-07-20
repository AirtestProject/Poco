# coding=utf-8

"""
This module provides bidirectional packet switching above the transport layer.
It is useful for target runtime which is not able to setup a server. The target runtime simple connect the repeater
(this module) to switch packets.

* Accepted tcp packet format: [4B as length][payload]
* Accepted websocket message format: [payload]
* Switching pattern: [payload] <--> [payload]
"""

import errno
import socket
import select
import time
import threading

from poco.utils.net.simple_wss import SimpleWebSocketServer, WebSocket
from poco.utils import six
from poco.utils.simplerpc.transport.tcp.protocol import SimpleProtocolFilter

if six.PY3:
    from queue import Queue, Empty
    from urllib.parse import urlparse
else:
    from Queue import Queue, Empty
    from urlparse import urlparse


def drain(q, to):
    total_tx = 0
    if isinstance(q, Queue):
        while True:
            try:
                d = q.get(False)
                to.send(d)
                total_tx += len(d)
            except Empty:
                break
    else:
        while q:
            d = q.pop(0)
            to.send(d)
            total_tx += len(d)
    return total_tx


class TcpSocket(object):
    def __init__(self, addr, rxsize=65536):
        super(TcpSocket, self).__init__()
        self.ip, self.port = addr
        if self.ip in ('', '*', '0'):
            self.ip = '0.0.0.0'
        self.s = socket.socket()
        self.s.bind((self.ip, self.port))
        self.s.listen(1)
        self.c = None
        self.rq = Queue()
        self.tq = Queue()
        self.RX_SIZE = rxsize
        self.p = SimpleProtocolFilter()
        print('server listens on ("{}", {}) transport socket'.format(self.ip, self.port))

    def update(self):
        rlist = [self.s]
        if self.c:
            rlist.append(self.c)
        r, _, _ = select.select(rlist, [], [], 0.005)
        for c in r:
            if c is self.s:
                self.c, addr = self.s.accept()
                print('accept from: {}'.format(addr))
                drain(self.tq, self)
            else:
                try:
                    rxdata = self.c.recv(self.RX_SIZE)
                except socket.error as e:
                    if e.errno in (errno.ECONNRESET, ):
                        rxdata = ''
                    else:
                        continue

                if not rxdata:
                    try:
                        self.c.close()
                    except socket.error:
                        pass
                    self.c = None
                else:
                    for packet in self.p.input(rxdata):
                        self.rq.put(packet)

        return self.recv()

    def recv(self):
        try:
            return self.rq.get(False)
        except Empty:
            return None

    def send(self, packet):
        if not self.c:
            self.tq.put(packet)
        else:
            data = self.p.pack(packet)
            self.c.sendall(data)


class WsSocket(object):
    def __init__(self, addr):
        super(WsSocket, self).__init__()
        self.ip, self.port = addr
        if self.ip in ('', '*', '0'):
            self.ip = '0.0.0.0'
        self.c = None
        self.rq = Queue()
        self.tq = Queue()

        class MyWsApp(WebSocket):
            def handleConnected(self2):
                self.c = self2
                drain(self.tq, self)
                print('server on accept. {}'.format(self.c))

            def handleMessage(self2):
                print('received_message from {}: {}'.format(self2.address, self2.data))
                self.rq.put(self2.data)

            def handleClose(self2):
                self.c = None
                print('client gone. {}'.format(self2.address))

        self.server = SimpleWebSocketServer(self.ip, self.port, MyWsApp)
        self.t = threading.Thread(target=self.server.serveforever)
        self.t.daemon = True
        self.t.start()
        print('server listens on ("{}", {}) transport websocket'.format(self.ip, self.port))

    def update(self):
        time.sleep(0.001)
        return self.recv()

    def recv(self):
        try:
            return self.rq.get(False)
        except Empty:
            return None

    def send(self, data):
        if not self.c:
            self.tq.put(data)
        else:
            self.c.sendMessage(data)


class Repeater(object):
    def __init__(self, *eps):
        super(Repeater, self).__init__()
        self.eps = [urlparse(ep) for ep in eps]
        self.transports = [self._make_transport(ep) for ep in self.eps]
        self.t = threading.Thread(target=self.loop)
        self.t.daemon = True
        self.t.start()

    def _make_transport(self, ep):
        if ep.scheme.startswith('ws'):
            transport = WsSocket((ep.hostname, ep.port))
        else:
            transport = TcpSocket((ep.hostname, ep.port))
        return transport

    def loop(self):
        print('Repeater on.')
        while True:
            for t in self.transports:
                data = t.update()
                if not data:
                    continue

                for t2 in self.transports:
                    if t2 is t:
                        continue
                    t2.send(data)


# raw tcp to tcp
def tcp2tcp(ep1, ep2):
    RX_SIZE = 65536

    ep1 = urlparse(ep1)
    ep2 = urlparse(ep2)

    s1 = socket.socket()
    s2 = socket.socket()
    s1.bind(('0.0.0.0', ep1.port))
    s2.bind(('0.0.0.0', ep2.port))
    s1.listen(1)
    s2.listen(1)

    c1 = None
    c2 = None
    q1 = []  # c1 -> q2
    q2 = []  # c2 -> q1

    print('proxy server started!')
    while True:
        rlist = [s1, s2]
        if c1 is not None:
            rlist.append(c1)
        if c2 is not None:
            rlist.append(c2)
        r, w, x = select.select(rlist, [], [])
        for c in r:
            if c is s1:
                c1, c1_addr = s1.accept()
                print('c1: accept from {}'.format(c1_addr))
                drain(q1, c1)
            elif c is s2:
                c2, c2_addr = s2.accept()
                print('c2: accept from {}'.format(c2_addr))
                drain(q2, c2)
            elif c is c1:
                rxdata = c.recv(RX_SIZE)
                if not rxdata:
                    try:
                        c1.close()
                    except socket.error:
                        pass
                    c1 = None
                    print('c1: disconnected')
                    continue

                if c2 is not None:
                    total_tx = drain(q2, c2)
                    c2.sendall(rxdata)
                    total_tx += len(rxdata)
                    print('c1 -> c2: send data {:06d} B'.format(total_tx))
                else:
                    q2.append(rxdata)
                    print('c1 -> c2: queue data {:06d} B'.format(len(rxdata)))
            elif c is c2:
                rxdata = c.recv(RX_SIZE)
                if not rxdata:
                    try:
                        c2.close()
                    except socket.error:
                        pass
                    c2 = None
                    print('c2: disconnected')
                    continue

                if c1 is not None:
                    total_tx = drain(q1, c1)
                    c1.sendall(rxdata)
                    total_tx += len(rxdata)
                    print('c2 -> c1: send data {:06d} B'.format(total_tx))
                else:
                    q1.append(rxdata)
                    print('c2 -> c1: queue data {:06d} B'.format(len(rxdata)))


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Not enough arguments. Please provide at least 2 endpoints.')
        print('e.g. ws://*:15003 tcp://*:15004')
        exit(-1)
    rpt = Repeater(sys.argv[1], sys.argv[2])

    while True:
        time.sleep(5)
