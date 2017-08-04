# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:48:10
from . import CocosJsPoco, SocketIORpc
from airtest.core.main import set_serialno
from pprint import pprint


if __name__ == '__main__':
    r = SocketIORpc()
    pprint(r.dump())
    # set_serialno()
    # p = CocosJsPoco()
    # # ret = p._rpc_client.dump()
    # # pprint(ret)
    # p("btnQuickStart").click()
