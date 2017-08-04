# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:48:10
from . import CocosJsPoco, SocketIORpc


if __name__ == '__main__':
    # r = SocketIORpc()
    # print r.dump()
    p = CocosJsPoco()
    print p._rpc_client.dump()
