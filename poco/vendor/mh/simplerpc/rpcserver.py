# encoding=utf-8
from .simplerpc import RpcAgent


class RpcServer(RpcAgent):
    """docstring for RpcServer"""
    def __init__(self, server):
        super(RpcServer, self).__init__()
        self.server = server
        self.server.client_connect_cb = self.on_client_connect
        self.server.client_close_cb = self.on_client_close
        self.server.start()

    def on_client_connect(self, conn):
        print("on_client_connect", conn)

    def on_client_close(self, conn):
        print("on_client_close", conn)

    def update(self):
        for conn in self.server.connections.values():
            messages = conn.recv()
            for msg in messages:
                self.handle_message(msg, conn)

    def call(self, conn, func, *args, **kwargs):
        req, cb = self.format_request(func, *args, **kwargs)
        conn.send(req)
        return cb
