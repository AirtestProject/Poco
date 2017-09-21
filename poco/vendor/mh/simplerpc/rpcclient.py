# encoding=utf-8
from simplerpc import RpcAgent
import time


class RpcClient(RpcAgent):
    """docstring for RpcClient"""
    def __init__(self, conn):
        super(RpcClient, self).__init__()
        self.conn = conn
        self.conn.connect_cb = self.on_connect
        self.conn.close_cb = self.on_close
        self.conn.connect()
        self._connected = False

    def on_connect(self):
        print("on_connect")
        self._connected = True

    def on_close(self):
        print("on_close")
        self._connected = False

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

    def wait_connected(self):
        for i in range(10):
            print("waiting for connection")
            if self._connected:
                return True
            time.sleep(0.5)
        raise RuntimeError("connecting timeout")
