# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:47:51

from poco.pocofw import Poco
from poco.agent import PocoAgent
from poco.freezeui.hierarchy import FrozenUIHierarchy, FrozenUIDumper
from poco.utils.simplerpc.utils import sync_wrapper
from poco.utils.airtest import AirtestInput, AirtestScreen
from poco.utils.simplerpc.rpcclient import RpcClient
from poco.utils.simplerpc.transport.ws import WebSocketClient
from poco.utils import six
if six.PY3:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse

from airtest.core.api import connect_device, device as current_device
from poco.utils.device import default_device
from airtest.core.helper import device_platform


__all__ = ['CocosJsPoco']
DEFAULT_PORT = 5003
DEFAULT_ADDR = ('localhost', DEFAULT_PORT)


class CocosJsPocoAgent(PocoAgent):
    def __init__(self, port, device=None, ip=None):
        if ip is None or ip == "localhost":
            self.device = device or default_device()

            platform_name = device_platform(self.device)
            if platform_name == 'Android':
                local_port, _ = self.device.adb.setup_forward('tcp:{}'.format(port))
                ip = self.device.adb.host or 'localhost'
                port = local_port
            elif platform_name == 'IOS':
                port, _ = self.device.setup_forward(port)
                if self.device.is_local_device:
                    ip = 'localhost'
                else:
                    ip = self.device.ip
            else:
                ip = self.device.get_ip_address()

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

    def get_sdk_version(self):
        return self.rpc.call("getSDKVersion")


class Dumper(FrozenUIDumper):
    def __init__(self, rpcclient):
        super(Dumper, self).__init__()
        self.rpcclient = rpcclient

    @sync_wrapper
    def dumpHierarchy(self, onlyVisibleNode=True):
        # NOTE: cocosjs 的driver里，这个rpc方法名首字母是小写，特别注意！
        return self.rpcclient.call("dump", onlyVisibleNode)


class CocosJsPoco(Poco):
    """docstring for CocosJsPoco"""

    def __init__(self, addr=DEFAULT_ADDR, device=None, **options):
        if not isinstance(addr, (tuple, list, six.string_types)):
            raise TypeError('Argument "addr" should be `tuple[2]`, `list[2]` or `string` only. Got {}'
                            .format(type(addr)))

        try:
            if isinstance(addr, (list, tuple)):
                ip, port = addr
            else:
                port = urlparse(addr).port
                if not port:
                    raise ValueError
                ip = urlparse(addr).hostname
        except ValueError:
            raise ValueError('Argument "addr" should be a tuple[2] or string format. e.g. '
                             '["localhost", 5003] or "ws://localhost:5003". Got {}'.format(repr(addr)))

        agent = CocosJsPocoAgent(port, device, ip=ip)
        if 'action_interval' not in options:
            options['action_interval'] = 0.5
        super(CocosJsPoco, self).__init__(agent, **options)
