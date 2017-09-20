# encoding=utf-8

from simplerpc import RpcAgent


class RpcClient(RpcAgent):
    """docstring for RpcClient"""
    def __init__(self, conn):
        super(RpcClient, self).__init__()
        self.conn = conn
        self.conn.connect_cb = self.on_connected
        self.conn.close_cb = self.on_closed
        self.conn.connect()

    def on_connected(self):
        pass

    def on_closed(self):
        pass

    def call(self, func, *args, **kwargs):
        msg, cb = self.format_request(func, *args, **kwargs)
        self.conn.send(msg)
        return cb

    def update(self):
        data = self.conn.recv()
        if not data:
            return
        for msg in data:
            self.handle_message(msg, self.conn)
