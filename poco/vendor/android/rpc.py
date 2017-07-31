# coding=utf-8
from __future__ import unicode_literals

from functools import wraps

from poco.interfaces.rpc import RpcInterface
from poco.exceptions import PocoTargetRemovedException

from hrpc.exceptions import RpcRemoteException
from hrpc.client import RpcClient
from hrpc.transport.http import HttpTransport


__author__ = 'lxn3032'
__all__ = ['AndroidRpcClient']


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
        except RpcRemoteException as e:
            if e.error_type == 'NodeHasBeenRemovedException':
                raise PocoTargetRemovedException('{}: {}'.format(func.__name__, name), repr(nodes).decode('utf-8'))
            else:
                raise
    return wrapped


class Client(RpcClient):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        super(Client, self).__init__(HttpTransport)

    def initialize_transport(self):
        return HttpTransport(self.endpoint, self)


class AndroidRpcClient(RpcInterface):
    def __init__(self, endpoint, ime):
        super(AndroidRpcClient, self).__init__()
        self.endpoint = endpoint
        self.client = Client(endpoint)
        self.remote_poco = self.client.remote('poco-uiautomation-framework')
        self.inputer = self.remote_poco.inputer
        self.ime = ime

    # screen interface
    def get_screen_size(self):
        return self.remote_poco.screen.getPortSize()

    def get_screen(self, width):
        assert type(width) is int
        return self.remote_poco.screen.getScreen(width)

    # node/hierarchy interface
    @transform_node_has_been_removed_exception
    def getattr(self, nodes, name):
        return self.remote_poco.attributor.getAttr(nodes, name)

    @transform_node_has_been_removed_exception
    def setattr(self, nodes, name, val):
        if name == 'text':
            self.ime.text(val)
        else:
            self.remote_poco.attributor.setAttr(nodes, name, val)

    def select(self, query, multiple=False):
        return self.remote_poco.selector.select(query, multiple)

    def dump(self):
        return self.remote_poco.dumper.dumpHierarchy()

    # input interface
    def click(self, x, y):
        return self.inputer.click(x, y)

    def long_click(self, x, y, duration=3.0):
        return self.inputer.longClick(x, y, duration)

    def swipe(self, x1, y1, x2, y2, duration=2.0):
        return self.inputer.swipe(x1, y1, x2, y2, duration)
