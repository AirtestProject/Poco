# coding=utf-8
from ..interfaces import IConnection, IServer, IClient
from .asynctcp import Host, Client, init_loop
from .protocol import SimpleProtocolFilter


class TcpConn(IConnection):
    """docstring for TcpConn"""
    def __init__(self, client):
        super(TcpConn, self).__init__()
        self.client = client
        self.prot = SimpleProtocolFilter()

    def send(self, msg):
        msg_bytes = self.prot.pack(msg)
        self.client.say(msg_bytes)

    def recv(self):
        msg_bytes = self.client.read_message()
        return self.prot.input(msg_bytes)


class TcpServer(IServer):
    def __init__(self, addr=("0.0.0.0", 5001)):
        super(TcpServer, self).__init__()
        self.host = Host(addr)

    def start(self):
        init_loop()

    def connections(self):
        """每次重新构造有点不好, to be fixed"""
        return {cid: TcpConn(client) for (cid, client) in self.host.remote_clients.items()}


class TcpClient(IClient):
    """docstring for TcpClient"""
    def __init__(self, address):
        super(TcpClient, self).__init__()
        self.s = Client(address)
        self.prot = SimpleProtocolFilter()

    def connect(self):
        init_loop()

    def send(self, msg):
        msg_bytes = self.prot.pack(msg)
        self.s.say(msg_bytes)

    def recv(self):
        msg_bytes = self.s.read_message()
        return self.prot.input(msg_bytes)
