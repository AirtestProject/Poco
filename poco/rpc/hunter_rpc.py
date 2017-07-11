# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-11 14:34:46


from . import RpcCient
from hunter_cli.rpc.client import HunterRpcClient


class HunterRpc(RpcCient):
    """hunter implementaion of rpc client"""
    def __init__(self, hunter):
        super(HunterRpc, self).__init__()
        self.rpc_client = HunterRpcClient(hunter)
        self.remote_poco = self.rpc_client.remote('poco-uiautomation-framework')
        self.selector = self.remote_poco.selector
        self.attributor = self.remote_poco.attributor

    def get_screen_size(self):
        return self.remote_poco.get_screen_size()

    def getattr(self, nodes, name):
        return self.attributor.getattr(nodes, name)

    def setattr(self, nodes, name, value):
        return self.attributor.setattr(nodes, name, value)

    def make_selection(self, node):
        return self.selector.make_selection(node)

    def select(self, query, multiple=True):
        return self.selector.select(query, multiple)
