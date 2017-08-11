# coding=utf-8

from functools import wraps

from hrpc.exceptions import RpcRemoteException as HRpcRemoteException
from poco.exceptions import PocoTargetRemovedException


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
