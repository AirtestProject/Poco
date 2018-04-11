# coding=utf-8

from poco import Poco
from poco.agent import PocoAgent
from poco.sdk.Attributor import Attributor
from poco.sdk.interfaces.screen import ScreenInterface
from poco.sdk.exceptions import UnableToSetAttributeException
from poco.freezeui.hierarchy import FrozenUIHierarchy, FrozenUIDumper
from poco.utils.airtest import AirtestInput, AirtestScreen
from poco.utils.simplerpc.rpcclient import RpcClient
from poco.utils.simplerpc.transport.tcp.main import TcpClient
from poco.utils.simplerpc.utils import sync_wrapper

from airtest.core.api import device as current_device

__all__ = ['StdPoco']
DEFAULT_PORT = 15004
DEFAULT_ADDR = ('localhost', DEFAULT_PORT)


class Dumper(FrozenUIDumper):
    def __init__(self, rpcclient):
        super(Dumper, self).__init__()
        self.rpcclient = rpcclient

    @sync_wrapper
    def dumpHierarchy(self):
        return self.rpcclient.call("Dump")


class StdAttributor(Attributor):
    def __init__(self, client):
        super(StdAttributor, self).__init__()
        self.client = client

    def setAttr(self, node, attrName, attrVal):
        if attrName == 'text':
            if type(node) in (list, tuple):
                node = node[0]
            instance_id = node.getAttr('_instanceId')
            if instance_id:
                success = self.client.call('SetText', instance_id, attrVal)
                if success:
                    return
        raise UnableToSetAttributeException(attrName, node)


class StdScreen(ScreenInterface):
    def __init__(self, client):
        super(StdScreen, self).__init__()
        self.client = client

    @sync_wrapper
    def getScreen(self, width):
        return self.client.call("Screenshot", width)

    @sync_wrapper
    def getPortSize(self):
        return self.client.call("GetScreenSize")


class StdPocoAgent(PocoAgent):
    def __init__(self, addr=DEFAULT_ADDR):
        # init airtest env

        self.conn = TcpClient(addr)
        self.c = RpcClient(self.conn)
        self.c.DEBUG = False
        self.c.wait_connected()

        hierarchy = FrozenUIHierarchy(Dumper(self.c), StdAttributor(self.c))
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
    def __init__(self, device=None, port=DEFAULT_PORT, **kwargs):
        device = device or current_device()
        if not device:
            raise RuntimeError('Please call `connect_device` first. see airtest.core.api.connect_device to get '
                               'more infomation')
        ip = device.get_ip_address()
        agent = StdPocoAgent((ip, port))
        super(StdPoco, self).__init__(agent, **kwargs)
