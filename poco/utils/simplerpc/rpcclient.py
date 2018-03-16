# encoding=utf-8
from .simplerpc import RpcAgent
from . import simplerpc
import time


class RpcClient(RpcAgent):

    CONNECTING, CONNECTED, CLOSED = 1, 2, 3

    """docstring for RpcClient"""
    def __init__(self, conn):
        super(RpcClient, self).__init__()
        self.conn = conn
        self.conn.connect_cb = self.on_connect
        self.conn.close_cb = self.on_close
        self._status = self.CONNECTING
        self.conn.connect()

    @property
    def DEBUG(self):
        return simplerpc.DEBUG

    @DEBUG.setter
    def DEBUG(self, value):
        simplerpc.DEBUG = value

    def on_connect(self):
        if self._status == self.CONNECTING:
            self._status = self.CONNECTED

    def on_close(self):
        self._status = self.CLOSED

    def call(self, func, *args, **kwargs):
        msg, cb = self.format_request(func, *args, **kwargs)
        self.conn.send(msg)
        return cb

    def update(self):
        if self._status != self.CONNECTED:
            return
        data = self.conn.recv()
        if not data:
            return
        for msg in data:
            self.handle_message(msg, self.conn)

    def wait_connected(self):
        for i in range(10):
            print("waiting for connection...%s" % i)
            if self._status == self.CONNECTED:
                return True
            elif self._status == self.CONNECTING:
                time.sleep(0.5)
            else:
                raise RuntimeError("Connection Closed")
        raise RuntimeError("connecting timeout")
