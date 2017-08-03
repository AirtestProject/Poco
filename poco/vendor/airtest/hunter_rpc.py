# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-11 14:34:46
from __future__ import unicode_literals

import types
from functools import wraps

from poco.interfaces.rpc import RpcInterface, RpcRemoteException, RpcTimeoutException
from poco.exceptions import PocoTargetRemovedException

from hrpc.exceptions import RpcRemoteException as HRpcRemoteException, RpcTimeoutException as HRpcTimeoutException
from hunter_cli.rpc.client import HunterRpcClient


def exception_transform(Origin, Target):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Origin as e:
                raise Target(e)
        return wrapped
    return wrapper


def member_func_exception_transform(Origin, Target):
    def wrapper(Cls):
        class WrapperCls(Cls):
            def __getattribute__(self, item):
                func = super(WrapperCls, self).__getattribute__(item)
                if isinstance(func, types.FunctionType) and not item.startswith('_'):
                    @wraps(func)
                    def wrapped(*args, **kwargs):
                        try:
                            return func(*args, **kwargs)
                        except Origin as e:
                            raise Target(e)
                    return wrapped
                else:

                    return func

        WrapperCls.__name__ = Cls.__name__
        return WrapperCls
    return wrapper


def transform_node_has_been_removed_exception(func):
    """
    将HRpcRemoteException.NodeHasBeenRemovedException转换成PocoTargetRemovedException

    :param func: 仅限getattr和setattr两个接口方法
    :return: 
    """

    @wraps(func)
    def wrapped(self, nodes, name, *args, **kwargs):
        try:
            return func(self, nodes, name, *args, **kwargs)
        except HRpcRemoteException as e:
            if e.error_type == 'NodeHasBeenRemovedException':
                raise PocoTargetRemovedException('{}: {}'.format(func.__name__, name), repr(nodes).decode('utf-8'))
            else:
                raise
    return wrapped


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

    def select(self, query, multiple=True):
        return self.selector.select(query, multiple)

    def evaluate(self, obj_proxy):
        return self.rpc_client.evaluate(obj_proxy)
