# coding=utf-8

import time
import json

from poco.drivers.unity3d.unity3d_poco import DEFAULT_ADDR, Dumper
from poco.utils.simplerpc.rpcclient import RpcClient
from poco.utils.simplerpc.transport.tcp import TcpClient


def dump():
    conn = TcpClient(DEFAULT_ADDR)
    c = RpcClient(conn)
    c.DEBUG = False
    c.run(backend=True)
    time.sleep(2)
    t0 = time.time()
    d = Dumper(c)
    h = d.dumpHierarchy()
    t1 = time.time()
    print t1 - t0
    return h


if __name__ == '__main__':
    # p = UnityPoco(("10.254.46.45", 5001))
    # p("Player").offspring("Mesh").click()
    time.sleep(2)
    h = dump()
    print json.dumps(h)
