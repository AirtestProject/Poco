# coding=utf-8

from poco.pocofw import Poco
from poco.agent import PocoAgent
from poco.drivers.std.attributor import StdAttributor
from poco.drivers.std.dumper import StdDumper
from poco.drivers.std.screen import StdScreen
from poco.drivers.std.inputs import StdInput
from poco.freezeui.hierarchy import FrozenUIHierarchy
from poco.utils.airtest import AirtestInput
from poco.utils.simplerpc.rpcclient import RpcClient
from poco.utils.simplerpc.transport.tcp.main import TcpClient
from poco.utils.simplerpc.utils import sync_wrapper

from airtest.core.api import connect_device, device as current_device
from airtest.core.helper import device_platform
import socket


__all__ = ['StdPoco', 'StdPocoAgent']
DEFAULT_PORT = 15004
DEFAULT_ADDR = ('localhost', DEFAULT_PORT)


class StdPocoAgent(PocoAgent):
    def __init__(self, addr=DEFAULT_ADDR, use_airtest_input=True):
        self.conn = TcpClient(addr)
        self.c = RpcClient(self.conn)
        self.c.connect()

        hierarchy = FrozenUIHierarchy(StdDumper(self.c), StdAttributor(self.c))
        screen = StdScreen(self.c)
        if use_airtest_input:
            inputs = AirtestInput()
        else:
            inputs = StdInput(self.c)
        super(StdPocoAgent, self).__init__(hierarchy, inputs, screen, None)

    @property
    def rpc(self):
        return self.c

    @sync_wrapper
    def get_debug_profiling_data(self):
        return self.c.call("GetDebugProfilingData")

    @sync_wrapper
    def get_sdk_version(self):
        return self.c.call('GetSDKVersion')

    def on_bind_driver(self, driver):
        super(StdPocoAgent, self).on_bind_driver(driver)
        if isinstance(self.input, AirtestInput):
            self.input.add_preaction_cb(driver)


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

    def __init__(self, port=DEFAULT_PORT, device=None, use_airtest_input=True, **kwargs):
        self.device = device or current_device()
        if not self.device:
            self.device = connect_device("Android:///")

        platform_name = device_platform(self.device)
        if platform_name == 'Android':
            # always forward for android device to avoid network unreachable
            local_port, _ = self.device.adb.setup_forward('tcp:{}'.format(port))
            ip = self.device.adb.host or 'localhost'
            port = local_port
        elif platform_name == 'IOS':
            # ip = device.get_ip_address()
            # use iproxy first
            ip = 'localhost'
            local_port, _ = self.device.instruct_helper.setup_proxy(port)
            port = local_port
        else:
            try:
                ip = self.device.get_ip_address()
            except AttributeError:
                try:
                    ip = socket.gethostbyname(socket.gethostname())
                except socket.gaierror:
                    # 某些特殊情况下会出现这个error，无法正确获取本机ip地址
                    ip = 'localhost'

        agent = StdPocoAgent((ip, port), use_airtest_input)
        kwargs['reevaluate_volatile_attributes'] = True
        super(StdPoco, self).__init__(agent, **kwargs)
