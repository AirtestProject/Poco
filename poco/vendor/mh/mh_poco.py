# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-13 20:29:56
from poco import Poco
from poco.rpc.mh_rpc import MhRpc


class MhPoco(Poco):
    """docstring for MhPoco"""
    def __init__(self):
        self._rpc_client = MhRpc()
        self._rpc_client.c.DEBUG = False
        super(MhPoco, self).__init__(self._rpc_client, action_interval=0.01)

    def click(self, pos, op):
        self._rpc_client.click(pos, op)
