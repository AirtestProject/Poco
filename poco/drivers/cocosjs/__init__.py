# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:47:51
import json

from poco import Poco
from poco.agent import PocoAgent
from poco.utils.simplerpc.utils import sync_wrapper
from poco.freezeui.hierarchy import FrozenUIHierarchy, FrozenUIDumper
from poco.utils.airtest import AirtestInput, AirtestScreen
from poco.utils.simplerpc.rpcclient import RpcClient
from poco.utils.simplerpc.transport.ws import WebSocketClient
from poco.utils import six

from airtest.core.api import connect_device, device as current_device
from airtest.core.helper import device_platform


__all__ = ['CocosJsPoco']
DEFAULT_ADDR = "ws://localhost:5003"


class CocosJsPocoAgent(PocoAgent):
    def __init__(self, addr=DEFAULT_ADDR):
        try:
            port = int(addr.rsplit(":", 1)[-1])
        except ValueError:
            raise ValueError('Argument `addr` should be a string-like format. e.g. "ws://192.168.1.2:5003". Got {}'
                             .format(repr(addr)))

        if not current_device():
            connect_device("Android:///")
        if device_platform() == 'Android':
            local_port, _ = current_device().adb.setup_forward('tcp:{}'.format(port))
            ip = 'localhost'
            port = local_port
        else:
            import socket
            ip = socket.gethostbyname(socket.gethostname())
            # Note: ios is not support for now.

        self.conn = WebSocketClient('ws://{}:{}'.format(ip, port))
        self.c = RpcClient(self.conn)
        self.c.DEBUG = False
        # self.c.run(backend=True)
        self.c.wait_connected()

        hierarchy = FrozenUIHierarchy(Dumper(self.c))
        screen = AirtestScreen()
        input = AirtestInput()
        super(CocosJsPocoAgent, self).__init__(hierarchy, input, screen, None)


class Dumper(FrozenUIDumper):
    def __init__(self, rpcclient):
        super(Dumper, self).__init__()
        self.rpcclient = rpcclient

    @sync_wrapper
    def dumpHierarchy(self, onlyVisibleNode=True):
        return self.rpcclient.call("dump", onlyVisibleNode)


class CocosJsPoco(Poco):
    """docstring for CocosJsPoco"""

    def __init__(self, addr=DEFAULT_ADDR, **options):
        agent = CocosJsPocoAgent(addr)
        if 'action_interval' not in options:
            options['action_interval'] = 0.5
        super(CocosJsPoco, self).__init__(agent, **options)


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
