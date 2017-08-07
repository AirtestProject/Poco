# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-11 14:34:46
from __future__ import unicode_literals


from poco.utils.exception_transform import member_func_exception_transform, transform_node_has_been_removed_exception
from poco.interfaces.rpc import RpcInterface, RpcRemoteException, RpcTimeoutException

from hrpc.exceptions import \
    RpcRemoteException as HRpcRemoteException, \
    RpcTimeoutException as HRpcTimeoutException
from hunter_cli.rpc.client import HunterRpcClient


@member_func_exception_transform(HRpcRemoteException, RpcRemoteException)
@member_func_exception_transform(HRpcTimeoutException, RpcTimeoutException)
class HunterRpc(RpcInterface):
    def __init__(self, hunter):
        RpcInterface.__init__(self)
        self.rpc_client = HunterRpcClient(hunter)
        self.rpc_client.set_timeout(25)  # 把timeout设置长一点，避免有些游戏切场景时耗时太久，来不及响应rpc请求
        self.remote_poco = self.rpc_client.remote('poco-uiautomation-framework-2')
        self.selector = self.remote_poco.selector
        self.attributor = self.remote_poco.attributor

    # screen interface
    def get_screen_size(self):
        return self.remote_poco.screen.getPortSize()

    # node/hierarchy interface
    @transform_node_has_been_removed_exception
    def getattr(self, nodes, name):
        return self.attributor.getAttr(nodes, name)

    @transform_node_has_been_removed_exception
    def setattr(self, nodes, name, value):
        return self.attributor.setAttr(nodes, name, value)

    @transform_node_has_been_removed_exception
    def select(self, query, multiple=True):
        return self.selector.select(query, multiple)

    def dump(self):
        return self.remote_poco.dumper.dumpHierarchy()

    def evaluate(self, obj_proxy):
        return self.rpc_client.evaluate(obj_proxy)
