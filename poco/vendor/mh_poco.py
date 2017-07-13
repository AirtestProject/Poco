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
        super(MhPoco, self).__init__(self._rpc_client)

    def click(self, pos):
        self._rpc_client.click(pos)


if __name__ == '__main__':
    p = MhPoco()
    p(name=u"超级神虎").click((0,0))
    p(text=u"超级神虎").sibling(type="Button").click()
