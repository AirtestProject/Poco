# encoding=utf-8
import json
import traceback

from poco.vendor.mh.simplerpc.transport.asynctcp.asynctcp import Client, init_loop
from poco.vendor.mh.simplerpc.transport.protocol import SimpleProtocolFilter
from poco.vendor.mh.simplerpc.transport.simpletcp.simpletcp import SafeSocket
from simplerpc import RpcAgent
from poco.vendor.mh.simplerpc.transport.interfaces import IClient


class SafeSocketConn(IClient):
    """docstring for SafeSocketConn"""
    def __init__(self, address):
        super(SafeSocketConn, self).__init__()
        self.s = SafeSocket(address=address)
        self.prot = SimpleProtocolFilter()

    def connect(self):
        self.s.connect()

    def send(self, msg):
        msg_bytes = self.prot.pack(msg)
        self.s.send(msg_bytes)

    def recv(self):
        msg_bytes = self.s.recv_nonblocking()
        return self.prot.input(msg_bytes)


class AsyncConn(IClient):
    """docstring for AsyncConn"""
    def __init__(self, address):
        super(AsyncConn, self).__init__()
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


class RpcClient(RpcAgent):
    """docstring for RpcClient"""
    def __init__(self, conn):
        super(RpcClient, self).__init__()
        self.conn = conn
        self.conn.connect()

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


if __name__ == '__main__':
    conn = SafeSocketConn(("localhost", 5001))
    # conn = AsyncConn(("localhost", 5001))
    # conn = AsyncConn(("10.254.46.45", 5001))
    c = RpcClient(conn)
    c.run(backend=True)
    # simply call rpc
    """
    print c.call("Add", 1, 2).wait()
    print(222)
    print c.call("Screen", 1, 2).wait()
    j, e = c.call("Dump", 1, 2).wait()
    print json.dumps(j)
    """
    from pprint import pprint
    c.call("foobar", foo="aaa", bar="bbb")
    # call rpc and wait for rpc result
    cb = c.call("foo", foo=1, bar=2)
    r = cb.wait()
    print("wait and got:", r)
    cb = c.call("make_error")
    r = cb.wait()
    print("wait and got:", r)
    # call rpc and register callback
    c.call("foobar", foo="aaa", bar="bbb").on_result(pprint)
    # call rpc and register callback, then wait for rpc result
    cb = c.call("foobar2", foo="aaa", bar="bbb")
    cb.on_error(pprint)
    print("after callback, wait and got error:", cb.wait())
    # call rpc and wait for delay rpc result
    cb = c.call("delayecho", 111, 222)
    cb.on_result(pprint)
    print("after callback, wait and got delayed result: ", cb.wait())

    cb = c.call("delayerror", 111, 222)
    cb.on_result(pprint)
    print("after callback, wait and got delayed result: ", cb.wait())
    # run python console
    # c.console_run({"c": c})

