# coding=utf-8
from __future__ import unicode_literals

import types
from functools import wraps

from hrpc.exceptions import \
    RpcRemoteException as HRpcRemoteException, \
    RpcTimeoutException as HRpcTimeoutException

from poco.exceptions import PocoTargetRemovedException

__author__ = 'lxn3032'


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
