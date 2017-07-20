# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-13 20:29:56
from poco import Poco
from .mh_rpc import MhRpc


class MhPoco(Poco):
    """docstring for MhPoco"""
    def __init__(self):
        rpc_client = MhRpc()
        rpc_client.c.DEBUG = False
        super(MhPoco, self).__init__(rpc_client, action_interval=0.01)

    def click(self, pos):
        self.rpc.click(pos)
