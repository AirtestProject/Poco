# encoding=utf-8
import json

from .transport.asynctcp.asynctcp import Host, init_loop
from .transport.protocol import SimpleProtocolFilter
from .transport.interfaces import IServer, IConnection
from .simplerpc import RpcAgent


class TcpConn(IConnection):
    """docstring for AsyncConn"""
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
        self.host = Host(addr)

    def start(self):
        init_loop()

    def connections(self):
        return {cid: TcpConn(client) for (cid, client) in self.host.remote_clients.items()}


class RpcServer(RpcAgent):
    """docstring for RpcServer"""
    def __init__(self, server):
        super(RpcServer, self).__init__()
        self.server = server
        self.server.start()

    def update(self):
        for conn in self.server.connections().values():
            messages = conn.recv()
            for msg in messages:
                self.handle_message(msg, conn)

    def call(self, cid, func, *args, **kwargs):
        req, cb = self.format_request(func, *args, **kwargs)
        client = self.server.connections[cid]
        client.send(req)
        return cb


if __name__ == '__main__':
    s = RpcServer(TcpServer())
    s.run()
    # s.console_run({"s": s})
