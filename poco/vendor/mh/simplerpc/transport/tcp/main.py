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
        self.s = Host(addr)
        # extend server's methods, not using multi-inheritance to prevent method name conflict
        self._s_handle_accept, self._s_close_client = self.s.handle_accept, self.s.close_client
        self.s.handle_accept, self.s.close_client = self._handle_accept, self._close_client
        self._connections = {}

    def start(self):
        init_loop()

    @property
    def connections(self):
        return self._connections

    def _handle_accept(self):
        client = self._s_handle_accept()
        conn = TcpConn(client)
        self._connections[client.cid] = conn
        self.on_client_connect(conn)

    def _close_client(self, client_id):
        client = self._s_close_client(client_id)
        conn = self._connections.pop(client.cid)
        self.on_client_close(conn)


class TcpClient(IClient):
    """docstring for TcpClient"""
    def __init__(self, addr):
        super(TcpClient, self).__init__()
        self.prot = SimpleProtocolFilter()
        self.c = Client(addr)
        # extends client's methods
        self._c_handle_connect, self._c_handle_close = self.c.handle_connect, self.c.handle_close
        self.c.handle_connect, self.c.handle_close = self._handle_connect, self._handle_close

    def connect(self):
        init_loop()

    def send(self, msg):
        msg_bytes = self.prot.pack(msg)
        self.c.say(msg_bytes)

    def recv(self):
        msg_bytes = self.c.read_message()
        return self.prot.input(msg_bytes)

    def _handle_connect(self):
        self._c_handle_connect()
        self.on_connect()

    def _handle_close(self):
        self._c_handle_close()
        self.on_close()
