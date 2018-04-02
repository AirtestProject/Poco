# coding=utf-8

import base64
import time
import json

from poco.drivers.unity3d import UnityPoco
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
    print(t1 - t0)
    return h


def test_click():
    p = UnityPoco(('10.254.46.45', 5001))
    for star in p('star'):
        star.click()


def test_drag():
    p = UnityPoco(('10.254.46.45', 5001))
    shell = p('shell')
    for star in p('star'):
        star.drag_to(shell)


if __name__ == '__main__':
    # test_click()
    # test_drag()
    # time.sleep(2)

    from poco.drivers.cocosjs import CocosJsPoco
    poco = CocosJsPoco()
    for n in poco():
        print n.get_name()


