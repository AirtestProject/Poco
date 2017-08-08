# coding=utf-8

from poco.interfaces.rpc import RpcInterface
from poco.vendor.local.Dumper import Dumper


__author__ = 'lxn3032'
__all__ = ['LocalRpcClient']


class LocalRpcClient(RpcInterface):
    def __init__(self, dumpable):
        dumper = Dumper(dumpable)
        super(LocalRpcClient, self).__init__(dumper)
