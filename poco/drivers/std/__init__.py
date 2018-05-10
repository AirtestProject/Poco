# coding=utf-8

from poco import Poco
from poco.agent import PocoAgent
from poco.drivers.std.attributor import StdAttributor
from poco.drivers.std.dumper import StdDumper
from poco.drivers.std.screen import StdScreen
from poco.freezeui.hierarchy import FrozenUIHierarchy
from poco.utils.airtest import AirtestInput
from poco.utils.simplerpc.rpcclient import RpcClient
from poco.utils.simplerpc.transport.tcp.main import TcpClient
from poco.utils.simplerpc.utils import sync_wrapper

from airtest.core.api import device as current_device
from airtest.core.helper import device_platform

__all__ = ['StdPoco', 'StdPocoAgent']
DEFAULT_PORT = 15004
DEFAULT_ADDR = ('localhost', DEFAULT_PORT)


class StdPocoAgent(PocoAgent):
    def __init__(self, addr=DEFAULT_ADDR):
        self.conn = TcpClient(addr)
        self.c = RpcClient(self.conn)
        self.c.DEBUG = False
        self.c.wait_connected()

        hierarchy = FrozenUIHierarchy(StdDumper(self.c), StdAttributor(self.c))
        screen = StdScreen(self.c)
        input = AirtestInput()
        super(StdPocoAgent, self).__init__(hierarchy, input, screen, None)

    @sync_wrapper
    def get_debug_profiling_data(self):
        return self.c.call("GetDebugProfilingData")

    @sync_wrapper
    def get_sdk_version(self):
        return self.c.call('GetSDKVersion')


class StdPoco(Poco):
    """
    Poco standard implementation for PocoSDK protocol.

    Args:
        port (:py:obj:`int`): the port number of the server that listens on the target device. default to 15004.
        device (:py:obj:`Device`): :py:obj:`airtest.core.device.Device` instance provided by ``airtest``. leave the
         parameter default and the default device will be chosen. more details refer to ``airtest doc``
        options: see :py:class:`poco.pocofw.Poco`

    Examples:
        The simplest way to connect to a cocos2dx-lua game::

            from poco.drivers.std import StdPoco
            from airtest.core.api import connect_device

            # connect a device first, then initialize poco object
            device = connect_device('Android:///')
            poco = StdPoco(10054, device)

            # now you can play with poco
            ui = poco('...')
            ui.click()
            ...

    """

    def __init__(self, port=DEFAULT_PORT, device=None, **kwargs):
        device = device or current_device()
        if not device:
            raise RuntimeError('Please call `connect_device` first. see airtest.core.api.connect_device to get '
                               'more infomation')

        # always forward for android device to avoid network unreachable
        if device_platform() == 'Android':
            local_port, _ = device.adb.setup_forward('tcp:{}'.format(port))
            ip = 'localhost'
            port = local_port
        elif device_platform() == 'IOS':
            # ip = device.get_ip_address()
            # use iproxy first
            ip = 'localhost'
        else:
            import socket
            ip = socket.gethostbyname(socket.gethostname())
            # Note: ios is not support for now.

        agent = StdPocoAgent((ip, port))
        super(StdPoco, self).__init__(agent, **kwargs)
