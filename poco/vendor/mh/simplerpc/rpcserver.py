# encoding=utf-8
from poco.vendor.mh.simplerpc.transport.tcp.main import TcpServer
from .simplerpc import RpcAgent


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
