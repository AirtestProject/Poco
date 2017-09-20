# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:47:51
import json
import time


from poco import Poco
from poco.agent import PocoAgent
from poco.vendor.airtest.input import AirtestInput
from poco.vendor.airtest.screen import AirtestScreen
from poco.vendor.localui.hierarchy import LocalUIHierarchy, LocalUIDumper
from poco.vendor.mh.mh_rpc import sync_wrapper
from poco.vendor.mh.simplerpc.rpcclient import RpcClient
from poco.vendor.mh.simplerpc.transport.ws import WebSocketClient

DEFAULT_ADDR = "ws://localhost:5003"


class CocosJsPocoAgent(PocoAgent):
    def __init__(self, addr=DEFAULT_ADDR):
        # init airtest env
        from airtest.core.main import connect_device
        from airtest.cli.runner import device as current_device
        if not current_device():
            connect_device("Android:///")
        current_device().adb.forward("tcp:5003", "tcp:5003", False)

        self.conn = WebSocketClient(addr)
        self.c = RpcClient(self.conn)
        self.c.DEBUG = False
        self.c.run(backend=True)

        hierarchy = LocalUIHierarchy(Dumper(self.c))
        screen = AirtestScreen()
        input = AirtestInput()
        super(CocosJsPocoAgent, self).__init__(hierarchy, input, screen, None)


class Dumper(LocalUIDumper):

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


# test code
def dump():
    from websocket import create_connection
    ws = create_connection(DEFAULT_ADDR, timeout=2)
    ws.send('{"jsonrpc": "2.0", "params": {}, "method": "dump", "id": 0}')
    print("Sent")
    print("Receiving...")
    result = ws.recv()
    print("Received '%s'" % result)
    ws.close()
    data = json.loads(result)
    return data["result"]
