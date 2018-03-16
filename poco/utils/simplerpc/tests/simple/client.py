import sys
sys.path.append("../../..")
from simplerpc.rpcclient import RpcClient
from time import sleep

from pprint import pprint


def test_with_tcp():
    from simplerpc.transport.tcp import TcpClient

    client = TcpClient()
    c = RpcClient(client)
    # c.run()
    c.wait_connected()
    test_client(c)


def test_client(c):
    """
    # unity rpc test
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


if __name__ == '__main__':
    test_with_tcp()
