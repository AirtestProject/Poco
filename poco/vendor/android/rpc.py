# coding=utf-8
__author__ = 'lxn3032'


from poco.rpc import RpcInterface

from hrpc.client import RpcClient
from hrpc.transport.http import HttpTransport


__all__ = ['AndroidRpcClient']


class Client(RpcClient):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        super(Client, self).__init__(HttpTransport)

    def initialize_transport(self):
        return HttpTransport(self.endpoint, self)


class AndroidRpcClient(RpcInterface):
    def __init__(self, endpoint):
        super(AndroidRpcClient, self).__init__()
        self.endpoint = endpoint
        self.client = Client(endpoint)
        self.remote_poco = self.client.remote('poco-uiautomation-framework')

    def get_screen_size(self):
        """get screen size"""
        return self.remote_poco.get_screen_size()

    def getattr(self, nodes, name):
        """get node attribute"""
        return self.remote_poco.attributor.getAttr(nodes, name)

    def setattr(self, nodes, name, val):
        """set node attribute"""
        self.remote_poco.attributor.setAttr(nodes, name, val)

    def make_selection(self, node):
        """get remote list of nodes by node proxy"""
        return self.remote_poco.selector.make_selection(node)

    def select(self, query, multiple=False):
        """select nodes by query"""
        return self.remote_poco.selector.select(query, multiple)
