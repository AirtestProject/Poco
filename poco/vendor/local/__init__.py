# coding=utf-8

__author__ = 'lxn3032'


from poco import Poco

from poco.vendor.local.rpc import LocalRpcClient


class LocalPoco(Poco):
    def __init__(self, dumper):
        rpc_client = LocalRpcClient(dumper)
        super(LocalPoco, self).__init__(rpc_client)

