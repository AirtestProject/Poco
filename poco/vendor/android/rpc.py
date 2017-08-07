# coding=utf-8
from __future__ import unicode_literals

from poco.utils.exception_transform import member_func_exception_transform, transform_node_has_been_removed_exception
from poco.interfaces.rpc import RpcInterface, RpcRemoteException, RpcTimeoutException

from hrpc.exceptions import \
    RpcRemoteException as HRpcRemoteException, \
    RpcTimeoutException as HRpcTimeoutException

from hrpc.client import RpcClient
from hrpc.transport.http import HttpTransport


__author__ = 'lxn3032'
__all__ = ['AndroidRpcClient']


class Client(RpcClient):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        super(Client, self).__init__(HttpTransport)

    def initialize_transport(self):
        return HttpTransport(self.endpoint, self)


@member_func_exception_transform(HRpcRemoteException, RpcRemoteException)
@member_func_exception_transform(HRpcTimeoutException, RpcTimeoutException)
class AndroidRpcClient(RpcInterface):
    def __init__(self, endpoint, ime):
        RpcInterface.__init__(self)
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
        self.remote_poco.attributor.setAttr(nodes, name, val)
        if name == 'text':
            check_val = self.getattr(nodes, 'text')
            if check_val != val:
                raise Exception('调用android uiautomator setText失败，希望设置"{}"，但得到"{}"'.encode('utf-8').format(val, check_val))
            # self.ime.text(val)

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
