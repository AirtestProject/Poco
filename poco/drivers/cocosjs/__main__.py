# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:48:10
from poco.drivers.cocosjs import CocosJsPoco, CocosJsPocoAgent
from pprint import pprint
import json
import time


def quick_game(p):
    p("btnQuickStart").click('center')

    for i in range(4):
        p("btnChip%d" % i).click('center')

    p("btnBet").click('center')
    p("btnBack").click('center')


if __name__ == '__main__':
    rpc = CocosJsPocoAgent()
    t0 = time.time()
    rpc.hierarchy.dump()
    t1 = time.time()
    print t1 - t0
    # print(dump())

    '''adb reverse tcp:5002 tcp:5002'''
    # addr = ('', 5002)
    # r = SocketIORpc(addr)
    # d = (r.dump())
    # pprint(d)

    # 默认的就是5001
    '''adb reverse tcp:5001 tcp:5001'''
    # r = SocketIORpc(addr)
    # d = (r.dump())
    # with open("test.log", "w") as f:
    #     f.write(json.dumps(d, indent=4))
    p = CocosJsPoco()
    # ret = p._rpc_client.dump()
    # pprint(ret)
    for i in range(300):
        print(i * 100000000000)
        quick_game(p)
