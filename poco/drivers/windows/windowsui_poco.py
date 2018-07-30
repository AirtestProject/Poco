# -*- coding: utf-8 -*-

from poco.drivers.std import StdPoco
from poco.utils.device import VirtualDevice
from poco.drivers.std import DEFAULT_ADDR, DEFAULT_PORT
from airtest.core.error import DeviceConnectionError

import threading
import time
import os
import atexit


class WindowsPoco(StdPoco):
    """
    Poco WindowsUI implementation.

    Args:
        selector (:py:obj:`dict`): find window by a selector, optional parameters: `title`,`handle`,`title_re`
        title: find windows by title
        handle: find windows by handle
        title_re: find windows by regular expression of title
        addr (:py:obj:`tuple`): where the WindowsUI running on, (localhost,15004) by default
        options: see :py:class:`poco.pocofw.Poco`

    Examples:
        ::
            from poco.drivers.windows import WindowsPoco
            # poco = WindowsPoco({'title':'xxx'})
            # poco = WindowsPoco({'handle':123456})
            # poco = WindowsPoco({'title_re':'[a-z][a-z][a-z]'}) # match the first matched window

    """   

    def __init__(self, selector=None, addr=DEFAULT_ADDR, **options):
        if 'action_interval' not in options:
            options['action_interval'] = 0.5

        if addr[0] == "localhost":
            from .sdk.WindowsUI import PocoSDKWindows
            sdk = PocoSDKWindows(addr)
            self.SDKProcess = threading.Thread(target=sdk.run)  # 创建线程
            self.SDKProcess.setDaemon(True)
            self.SDKProcess.start()
           
            # atexit.register(self.KillSDKProcess)
            # self.SDKProcess = subprocess.Popen("python " + os.path.dirname(__file__) + "\\sdk\\WindowsUI.py")

        dev = VirtualDevice(addr[0])
        super(WindowsPoco, self).__init__(addr[1], dev, False, **options)

        cb = self.agent.rpc.call("ConnectWindow", selector)
        ok = cb.wait(timeout=30)
        if not ok[0]:
            raise DeviceConnectionError("Can't find any windows by the given parameter")
        else:
            self.agent.rpc.call("SetForeground")
