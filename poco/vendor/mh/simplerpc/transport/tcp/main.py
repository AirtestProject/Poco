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


class TcpServer(IServer, Host):  # 多重继承比较坑
    def __init__(self, addr=("0.0.0.0", 5001)):
        super(TcpServer, self).__init__()
        Host.__init__(self, addr)
        self._connections = {}

    def start(self):
        init_loop()

    @property
    def connections(self):
        return self._connections

    def handle_accept(self):
        client = super(TcpServer, self).handle_accept()
        conn = TcpConn(client)
        self._connections[client.cid] = conn
        self.on_client_connect(conn)

    def close_client(self, client_id):
        client = super(TcpServer, self).close_client(client_id)
        conn = self._connections.pop(client.cid)
        self.on_client_disconnect(conn)

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
