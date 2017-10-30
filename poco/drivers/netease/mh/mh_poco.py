# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-13 20:29:56
from poco import Poco
from poco.agent import PocoAgent
from poco.drivers.netease.mh.mh_rpc import MhHierarchy, MhScreen, MhInput
from poco.utils.simplerpc.rpcclient import RpcClient
from poco.utils.simplerpc.transport.tcp.main import TcpClient


class MhPocoAgent(PocoAgent):
    def __init__(self, addr=("localhost", 5001)):
        conn = TcpClient(addr)
        self.c = RpcClient(conn)
        self.c.DEBUG = False
        self.c.run(backend=True)

        hierarchy = MhHierarchy(self.c)
        screen = MhScreen(self.c)
        input = MhInput(self.c)
        super(MhPocoAgent, self).__init__(hierarchy, input, screen, None)


class MhPoco(Poco):
    """docstring for MhPoco"""
    def __init__(self, addr=("localhost", 5001)):
        agent = MhPocoAgent(addr)
        super(MhPoco, self).__init__(agent, action_interval=0.2)
