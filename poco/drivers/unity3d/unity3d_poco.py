# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:47:51
from poco import Poco
from poco.agent import PocoAgent
from poco.freezeui.hierarchy import FreezedUIHierarchy, FreezedUIDumper
from poco.sdk.Attributor import Attributor
from poco.sdk.interfaces.screen import ScreenInterface
from poco.sdk.exceptions import UnableToSetAttributeException
from poco.utils.airtest import AirtestInput, AirtestScreen
from poco.utils.simplerpc.rpcclient import RpcClient
from poco.utils.simplerpc.transport.tcp.main import TcpClient
from poco.utils.simplerpc.utils import sync_wrapper

__all__ = ['UnityPoco']
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
        # if not unity_editor:
        # init airtest env
        try:
            # new version
            from airtest.core.api import connect_device, device as current_device
            from airtest.core.helper import device_platform
            if not current_device():
                if unity_editor:
                    connect_device("Windows:///?title_re=Unity.*")
                    game_window = current_device().app.top_window().child_window(title="UnityEditor.GameView")
                    current_device()._top_window = game_window.wrapper_object()
                    current_device().focus_rect = (0, 40, 0, 0)
                else:
                    connect_device("Android:///")
            if device_platform() == "Android":
                # unity games poco sdk listens on Android localhost:5001
                current_device().adb.forward("tcp:%s" % addr[1], "tcp:5001", False)
        except ImportError:
            # old version
            from airtest.cli.runner import device as current_device
            from airtest.core.main import set_serialno
            if not current_device():
                set_serialno()
            # unity games poco sdk listens on Android localhost:5001
            current_device().adb.forward("tcp:%s" % addr[1], "tcp:5001", False)

        self.conn = TcpClient(addr)
        self.c = RpcClient(self.conn)
        self.c.DEBUG = False
        # self.c.run(backend=True)
        self.c.wait_connected()

        hierarchy = FreezedUIHierarchy(Dumper(self.c), UnityAttributor(self.c))
        if unity_editor:
            screen = UnityScreen(self.c)
        else:
            screen = AirtestScreen()
        input = AirtestInput()
        super(UnityPocoAgent, self).__init__(hierarchy, input, screen, None)

    @sync_wrapper
    def get_debug_profiling_data(self):
        return self.c.call("GetDebugProfilingData")


class UnityAttributor(Attributor):
    def __init__(self, client):
        super(UnityAttributor, self).__init__()
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


class Dumper(FreezedUIDumper):
    def __init__(self, rpcclient):
        super(Dumper, self).__init__()
        self.rpcclient = rpcclient

    @sync_wrapper
    def dumpHierarchy(self):
        return self.rpcclient.call("Dump")


class UnityPoco(Poco):
    """
    Poco Unity3D implementation.

    Args:
        addr (:py:obj:`tuple`): the endpoint of your Unity3D game, default to ``("localhost", 5001)``
        unity_editor (:py:obj:`bool`): whether your Unity3D game is running in UnityEditor or not. default to ``False``
        options: see :py:class:`poco.pocofw.Poco`
    
    Examples:
        If your game is running on Android, you could initialize poco instance by using following snippet::
            
            from poco.drivers.unity3d import UnityPoco
            
            # your phone and your PC/mac should be inside the same sub-net.
            ip = '<ip address of your phone>'
            poco = UnityPoco((ip, 5001))
            poco('button').click()
            ...

    """

    def __init__(self, addr=DEFAULT_ADDR, unity_editor=False, **options):
        agent = UnityPocoAgent(addr, unity_editor)
        if 'action_interval' not in options:
            options['action_interval'] = 0.1
        super(UnityPoco, self).__init__(agent, **options)

    def on_pre_action(self, action, proxy, args):
        try:
            from airtest.core.api import snapshot
        except ImportError:
            # 兼容旧airtest
            from airtest.core.main import snapshot
            snapshot(msg=unicode(proxy))
