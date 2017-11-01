# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:47:51
import json

from poco import Poco
from poco.agent import PocoAgent
from poco.utils.simplerpc.utils import sync_wrapper
from poco.freezeui.hierarchy import FreezedUIHierarchy, FreezedUIDumper
from poco.utils.airtest import AirtestInput, AirtestScreen, connect_device, airtest_device
from poco.utils.simplerpc.rpcclient import RpcClient
from poco.utils.simplerpc.transport.ws import WebSocketClient

DEFAULT_ADDR = "ws://localhost:5003"


class CocosJsPocoAgent(PocoAgent):
    def __init__(self, addr=DEFAULT_ADDR):
        # init airtest env
        if not airtest_device():
            connect_device("Android:///")
        # cocos games poco sdk listens on Android localhost:5003
        localport = addr.split(":")[-1]
        airtest_device().adb.forward("tcp:%s" % localport, "tcp:5003", False)

        self.conn = WebSocketClient(addr)
        self.c = RpcClient(self.conn)
        self.c.DEBUG = False
        self.c.run(backend=True)
        self.c.wait_connected()

        hierarchy = FreezedUIHierarchy(Dumper(self.c))
        screen = AirtestScreen()
        input = AirtestInput()
        super(CocosJsPocoAgent, self).__init__(hierarchy, input, screen, None)


class Dumper(FreezedUIDumper):

    def __init__(self, rpcclient):
        super(Dumper, self).__init__()
        self.rpcclient = rpcclient

    @sync_wrapper
    def dumpHierarchy(self):
        return self.rpcclient.call("dump")


class CocosJsPoco(Poco):
    """docstring for CocosJsPoco"""

    def __init__(self, addr=DEFAULT_ADDR):
        agent = CocosJsPocoAgent(addr)
        super(CocosJsPoco, self).__init__(agent, action_interval=0.01)

    def on_pre_action(self, action, proxy, args):
        # airteset log用
        from airtest.core.main import snapshot
        snapshot(msg=unicode(proxy))


# test code
def dump():
    from websocket import create_connection
    ws = create_connection(DEFAULT_ADDR, timeout=2)
    ws.send('{"jsonrpc": "2.0", "params": {}, "method": "dump", "id": 0}')
    # print("Sent")
    # print("Receiving...")
    result = ws.recv()
    # print("Received '%s'" % result)
    ws.close()
    data = json.loads(result)
    return data["result"]
