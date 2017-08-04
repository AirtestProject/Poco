# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:48:10
from . import CocosJsPoco, SocketIORpc
from airtest.core.main import set_serialno
from pprint import pprint
import json


def quick_game(p):
    p("btnQuickStart").click('center')

    for i in range(4):
        p("btnChip%d" % i).click('center')

    p("btnBet").click('center')
    p("btnBack").click('center')


if __name__ == '__main__':
    # r = SocketIORpc()
    # d = (r.dump())
    # with open("test.log", "w") as f:
    #     f.write(json.dumps(d, indent=4))
    set_serialno()
    p = CocosJsPoco()
    # ret = p._rpc_client.dump()
    # pprint(ret)
    for i in range(3):
        quick_game(p)
