# coding=utf-8

from ..interfaces import IClient
from .safetcp import Client, socket
from .protocol import SimpleProtocolFilter


DEFAULT_ADDR = ("0.0.0.0", 5001)


class TcpClient(IClient):
    """docstring for TcpClient"""
    def __init__(self, addr=DEFAULT_ADDR):
        super(TcpClient, self).__init__()
        self.addr = addr
        self.prot = SimpleProtocolFilter()
        self.c = None

    def __str__(self):
        return 'tcp://{}:{}'.format(*self.addr)
    __repr__ = __str__

    def connect(self):
        if not self.c:
            self.c = Client(self.addr,
                            on_connect=self.on_connect,
                            on_close=self.on_close)
        self.c.connect()

    def send(self, msg):
        msg_bytes = self.prot.pack(msg)
        self.c.send(msg_bytes)

    def recv(self):
        try:
            msg_bytes = self.c.recv()
        except socket.timeout:
            # print("socket recv timeout")
            msg_bytes = b""
        return self.prot.input(msg_bytes)

    def close(self):
        self.c.close()
        self.c = None
