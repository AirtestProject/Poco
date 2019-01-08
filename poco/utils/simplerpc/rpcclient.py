# encoding=utf-8
from .simplerpc import RpcAgent, RpcConnectionError
from . import simplerpc
import warnings
import time


class RpcClient(RpcAgent):

    INIT, CONNECTING, CONNECTED, CLOSED = 0, 1, 2, 3

    """docstring for RpcClient"""
    def __init__(self, conn):
        super(RpcClient, self).__init__()
        self._status = self.INIT
        self.conn = conn
        self.conn.connect_cb = self.on_connect
        self.conn.close_cb = self.on_close

    def connect(self, timeout=10):
        self._status = self.CONNECTING
        self.conn.connect()
        self._wait_connected(timeout)

    def get_connection(self):
        return self.conn

    def wait_connected(self):
        warnings.warn(DeprecationWarning())
        return self.connect()

    def _wait_connected(self, timeout):
        for i in range(timeout):
            if self._status == self.CONNECTED:
                return True
            elif self._status == self.CONNECTING:
                print("[rpc]waiting for connection...%s" % i)
                time.sleep(0.5)
            else:
                raise RpcConnectionError("Rpc Connection Closed")
        raise RpcConnectionError("Connecting Timeout")

    def close(self):
        self.conn.close()
        self._status = self.CLOSED

    def on_connect(self):
        print("[rpc]connected")
        if self._status == self.CONNECTING:
            self._status = self.CONNECTED

    def on_close(self):
        print("[rpc]closed")
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

    @property
    def DEBUG(self):
        return simplerpc.DEBUG

    @DEBUG.setter
    def DEBUG(self, value):
        simplerpc.DEBUG = value
