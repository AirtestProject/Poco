# encoding=utf-8
import sys
sys.path.append("../../..")
from simplerpc.rpcserver import RpcServer
from simplerpc.simplerpc import dispatcher, AsyncResponse
import time


@dispatcher.add_method
def foobar(**kwargs):
    return kwargs["foo"] + kwargs["bar"]


@dispatcher.add_method
def make_error(*args):
    raise


@dispatcher.add_method
def delayecho(*args):
    r = AsyncResponse()
    from threading import Thread

    def func(r):
        time.sleep(5)
        r.result(args)

    Thread(target=func, args=(r,)).start()
    return r


@dispatcher.add_method
def delayerror(*args):
    r = AsyncResponse()
    from threading import Thread

    def func(r):
        time.sleep(5)
        r.error(RuntimeError("something wrong here"))

    Thread(target=func, args=(r,)).start()
    return r


def test_with_tcp():
    from simplerpc.transport.tcp import TcpServer
    s = RpcServer(TcpServer())
    s.run()
    # s.console_run({"s": s})


def test_with_sszmq():
    from simplerpc.transport.sszmq import SSZmqServer
    s = RpcServer(SSZmqServer())
    s.run()


if __name__ == '__main__':
    # test_with_tcp()
    test_with_sszmq()
