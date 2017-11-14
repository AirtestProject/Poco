# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:47:51
from poco import Poco
from poco.agent import PocoAgent
from poco.freezeui.hierarchy import FreezedUIHierarchy, FreezedUIDumper
from poco.sdk.interfaces.screen import ScreenInterface
from poco.utils.airtest import AirtestInput, AirtestScreen
from poco.utils.simplerpc.rpcclient import RpcClient
from poco.utils.simplerpc.transport.tcp.main import TcpClient
from poco.utils.simplerpc.utils import sync_wrapper

DEFAULT_ADDR = ("localhost", 5001)


class UnityScreen(ScreenInterface):
    def __init__(self, client):
        super(UnityScreen, self).__init__()
        self.client = client

    @sync_wrapper
    def getScreen(self, width):
        return self.client.call("Screenshot", width)

    @sync_wrapper
    def getPortSize(self):
        return self.client.call("GetScreenSize")


class UnityPocoAgent(PocoAgent):
    def __init__(self, addr=DEFAULT_ADDR, unity_editor=False):
        if not unity_editor:
            # init airtest env
            try:
                from airtest.core.api import connect_device, airtest_device as current_device
                if not current_device():
                    connect_device("Android:///")
            except ImportError:
                from airtest.cli.runner import device as current_device
                if not current_device():
                    raise RuntimeError("You are using old version of airtest, "
                                       "please initialize airtest device instance first.")
            # unity games poco sdk listens on Android localhost:5001
            current_device().adb.forward("tcp:%s" % addr[1], "tcp:5001", False)

        self.conn = TcpClient(addr)
        self.c = RpcClient(self.conn)
        self.c.DEBUG = False
        self.c.run(backend=True)
        self.c.wait_connected()

        hierarchy = FreezedUIHierarchy(Dumper(self.c))
        if unity_editor:
            screen = UnityScreen(self.c)
        else:
            screen = AirtestScreen()
        input = AirtestInput()
        super(UnityPocoAgent, self).__init__(hierarchy, input, screen, None)

    @sync_wrapper
    def get_debug_profiling_data(self):
        return self.c.call("GetDebugProfilingData")


class Dumper(FreezedUIDumper):
    def __init__(self, rpcclient):
        super(Dumper, self).__init__()
        self.rpcclient = rpcclient

    @sync_wrapper
    def dumpHierarchy(self):
        return self.rpcclient.call("Dump")


class UnityPoco(Poco):
    def __init__(self, addr=DEFAULT_ADDR, unity_editor=False):
        agent = UnityPocoAgent(addr, unity_editor)
        super(UnityPoco, self).__init__(agent, action_interval=0.1)

    def on_pre_action(self, action, proxy, args):
        # airteset log用
        try:
            from airtest.core.api import snapshot
        except ImportError:
            # 兼容旧版本
            from airtest.core.main import snapshot
        snapshot('img.png', msg=unicode(proxy))


