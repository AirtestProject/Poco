# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-11 14:34:46


import types
from functools import wraps
from . import RpcInterface, RpcRemoteException, RpcTimeoutException

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


@member_func_exception_transform(HRpcRemoteException, RpcRemoteException)
@member_func_exception_transform(HRpcTimeoutException, RpcTimeoutException)
class HunterRpc(RpcInterface):
    """hunter implementaion of rpc client"""
    def __init__(self, hunter):
        RpcInterface.__init__(self)
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
