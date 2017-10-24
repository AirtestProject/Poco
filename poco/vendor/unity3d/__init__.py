# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:47:51
from poco import Poco
from poco.agent import PocoAgent
from poco.freezeui.hierarchy import FreezedUIHierarchy, FreezedUIDumper
from poco.vendor.airtest.screen import AirtestScreen
from poco.vendor.airtest.input import AirtestInput
from poco.vendor.mh.mh_rpc import sync_wrapper
from poco.vendor.mh.simplerpc.rpcclient import RpcClient
from poco.vendor.mh.simplerpc.transport.tcp.main import TcpClient

DEFAULT_ADDR = ("localhost", 5001)


class UnityPocoAgent(PocoAgent):

    def __init__(self, addr=DEFAULT_ADDR):
        # init airtest env
        from airtest.core.main import set_serialno
        from airtest.cli.runner import device as current_device
        if not current_device():
            set_serialno()

        self.conn = TcpClient(addr)
        self.c = RpcClient(self.conn)
        self.c.DEBUG = False
        self.c.run(backend=True)

        hierarchy = FreezedUIHierarchy(Dumper(self.c))
        screen = AirtestScreen()
        input = AirtestInput()
        super(UnityPocoAgent, self).__init__(hierarchy, input, screen, None)


class Dumper(FreezedUIDumper):

    def __init__(self, rpcclient):
        super(Dumper, self).__init__()
        self.rpcclient = rpcclient

    @sync_wrapper
    def dumpHierarchy(self):
        return self.rpcclient.call("Dump")


class UnityPoco(Poco):

    def __init__(self, addr=DEFAULT_ADDR):
        agent = UnityPocoAgent(addr)
        super(UnityPoco, self).__init__(agent, action_interval=0.01)

    def on_pre_action(self, action, proxy, args):
        # airteset log用
        from airtest.core.main import snapshot
        snapshot(msg=unicode(proxy))


def dump():
    conn = TcpClient(DEFAULT_ADDR)
    c = RpcClient(conn)
    c.DEBUG = False
    c.run(backend=True)
    return Dumper(c).dumpHierarchy()
