# -*- coding: utf-8 -*-

import threading
from poco.drivers.std import StdPoco
from poco.utils.device import VirtualDevice
from poco.drivers.std import DEFAULT_ADDR, DEFAULT_PORT
from poco.utils.simplerpc.utils import sync_wrapper


class WindowsPoco(StdPoco):
    """
    Poco WindowsUI implementation.

    Args:
        selector (:py:obj:`dict`): find window by a selector, optional parameters: ``title``, ``handle``, ``title_re``
         title: find windows by title

         handle: find windows by handle

         title_re: find windows by regular expression of title

        addr (:py:obj:`tuple`): where the WindowsUI running on, (localhost,15004) by default
        options: see :py:class:`poco.pocofw.Poco`

    Examples:
        If your programme is running, you could initialize poco instance by using following snippet::
            from poco.drivers.windows import WindowsPoco
            # poco = WindowsPoco({'title':'xxx'})
            # poco = WindowsPoco({'handle':123456})
            # poco = WindowsPoco({'title_re':'[a-z][a-z][a-z]'})

    """   
    
    def __init__(self, selector=None, addr=DEFAULT_ADDR, **options):
        if 'action_interval' not in options:
            options['action_interval'] = 0.5

        if addr[0] == "localhost" or addr[0] == "127.0.0.1":
            from poco.drivers.windows.sdk.WindowsUI import PocoSDKWindows
            sdk = PocoSDKWindows(addr)
            self.SDKProcess = threading.Thread(target=sdk.run)  # 创建线程
            self.SDKProcess.setDaemon(True)
            self.SDKProcess.start()

        dev = VirtualDevice(addr[0])
        super(WindowsPoco, self).__init__(addr[1], dev, False, **options)

        argunums = 0
        if 'handle' in selector:
            argunums += 1
        if 'title' in selector:
            argunums += 1
        if 'title_re' in selector:
            argunums += 1
        
        if argunums == 0:
            raise ValueError("Expect handle or title, got none")
        elif argunums != 1:
            raise ValueError("Too many arguments, only need handle or title or title_re")
        
        self.selector = selector
        self.connect_window(self.selector)
        self.set_foreground()

    @sync_wrapper
    def connect_window(self, selector):
        return self.agent.rpc.call("ConnectWindow", selector)

    @sync_wrapper
    def set_foreground(self):
        return self.agent.rpc.call("SetForeground")
