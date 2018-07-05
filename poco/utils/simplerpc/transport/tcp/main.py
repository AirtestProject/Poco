# coding=utf-8

from ..interfaces import IClient
# from .asynctcp import Client, init_loop
from .safetcp import Client
from .protocol import SimpleProtocolFilter


DEFAULT_ADDR = ("0.0.0.0", 5001)


class TcpClient(IClient):
    """docstring for TcpClient"""
    def __init__(self, addr=DEFAULT_ADDR):
        super(TcpClient, self).__init__()
        self.addr = addr
        self.prot = SimpleProtocolFilter()
        self.c = None

    def connect(self):
        if not self.c:
            self.c = Client(self.addr,
                            on_connect=self.on_connect,
                            on_close=self.on_close)
            # init_loop()
        # self.c.connect_server()
        self.c.connect()

    def send(self, msg):
        msg_bytes = self.prot.pack(msg)
        self.c.send(msg_bytes)

    def recv(self):
        # msg_bytes = self.c.read_message()
        msg_bytes = self.c.recv()
        return self.prot.input(msg_bytes)

    def close(self):
        # self.c.close_connection()
        self.c.close()
        self.c = None
