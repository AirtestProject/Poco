import sys
sys.path.append("../..")
from simplerpc.rpcserver import RpcServer



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
    test_with_tcp()
    # test_with_sszmq()
