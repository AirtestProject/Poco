import sys
sys.path.append("../..")
from simplerpc.rpcclient import RpcClient
from pprint import pprint
from simplerpc.ssrpc.plugin import PluginRepo, Plugin, SSRpcClient
from simplerpc.simplerpc import dispatcher
import time


def test_with_tcp():
    from simplerpc.transport.tcp import TcpClient

    client = TcpClient()
    c = RpcClient(client)
    c.run(backend=True)
    test_client(c)


def test_with_sszmq():
    from simplerpc.transport.sszmq import SSZmqClient

    client = SSZmqClient()
    c = RpcClient(client)
    c.run(backend=True)
    c.wait_connected()
    test_client(c)


def test_client(c):
    """
    print c.call("Add", 1, 2).wait()
    print(222)
    print c.call("Screen", 1, 2).wait()
    j, e = c.call("Dump", 1, 2).wait()
    print json.dumps(j)
    """

    # simply call rpc
    c.call("foobar", foo="aaa", bar="bbb")
    # call rpc and wait for rpc result
    cb = c.call("foo", foo=1, bar=2)
    r = cb.wait()
    print("wait and got:", r)
    return
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


class AAAPlugin(Plugin):
    UUID = "AAAAAAA"

    def add_AAA(self, a, b):
        print(self)
        return a + b


@dispatcher.add_method
def add(a, b):
    print("aaa")
    return a + b


def test_ssrpc():
    from simplerpc.transport.tcp import TcpClient

    PluginRepo.register(AAAPlugin())

    client = TcpClient()
    c = SSRpcClient(client)
    c.run(backend=True)
    test_client(c)


if __name__ == '__main__':
    # test_with_tcp()
    # test_with_sszmq()
    test_ssrpc()
