# coding=utf-8
from __future__ import unicode_literals

from functools import wraps

from hrpc.exceptions import RpcRemoteException
from hrpc.object_proxy import safe_repr
from poco.exceptions import PocoTargetRemovedException


def transform_node_has_been_removed_exception(func):
    """
    将HRpcRemoteException.NodeHasBeenRemovedException转换成PocoTargetRemovedException

    :param func: 仅限getattr和setattr两个接口方法
    :return: 
    """

    @wraps(func)
    def wrapped(self, nodes, name, *args, **kwargs):
        """

        :param self:
        :param nodes: UI object proxy
        :param name: attribute name
        :param args:
        :param kwargs:
        :return:
        """

        tolerance_exc_types = (
            'NodeHasBeenRemovedException',
            'RemoteObjectNotFoundException',
        )
        try:
            return func(self, nodes, name, *args, **kwargs)
        except RpcRemoteException as e:
            for t in tolerance_exc_types:
                if e.error_type == t or e.error_type.endswith('.' + t):
                    raise PocoTargetRemovedException('{}: {}'.format(func.__name__, name), safe_repr(nodes))
            else:
                raise
    return wrapped
