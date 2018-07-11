# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:47:51
import json

from poco.pocofw import Poco
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
DEFAULT_ADDR = ('localhost', 5003)


class CocosJsPocoAgent(PocoAgent):
    def __init__(self, port, device=None):
        self.device = device or current_device()
        if not self.device:
            self.device = connect_device("Android:///")

        if device_platform(self.device) == 'Android':
            local_port, _ = self.device.adb.setup_forward('tcp:{}'.format(port))
            ip = self.device.adb.host or 'localhost'
            port = local_port
        elif device_platform() == 'IOS':
            # Note: ios is now support for now.
            # ip = device.get_ip_address()
            # use iproxy first
            ip = 'localhost'
            local_port, _ = current_device().instruct_helper.setup_proxy(port)
            port = local_port
        else:
            import socket
            ip = socket.gethostbyname(socket.gethostname())

        # transport
        self.conn = WebSocketClient('ws://{}:{}'.format(ip, port))
        self.c = RpcClient(self.conn)
        self.c.connect()

        hierarchy = FrozenUIHierarchy(Dumper(self.c))
        screen = AirtestScreen()
        inputs = AirtestInput()
        super(CocosJsPocoAgent, self).__init__(hierarchy, inputs, screen, None)

    @property
    def rpc(self):
        return self.c


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
        if not isinstance(addr, (tuple, list, six.string_types)):
            raise TypeError('Argument "addr" should be `tuple[2]`, `list[2]` or `string` only. Got {}'
                            .format(type(addr)))

        try:
            if isinstance(addr, (list, tuple)):
                ip, port = addr
            else:
                port = int(addr.rsplit(":", 1)[-1])
        except ValueError:
            raise ValueError('Argument "addr" should be a tuple[2] or string format. e.g. '
                             '["localhost", 5003] or "ws://localhost:5003". Got {}'.format(repr(addr)))

        agent = CocosJsPocoAgent(port)
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
