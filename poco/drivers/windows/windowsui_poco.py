# -*- coding: utf-8 -*-

import threading
from poco.drivers.std import StdPoco
from poco.utils.device import VirtualDevice
from poco.drivers.std import DEFAULT_ADDR, DEFAULT_PORT
from poco.utils.simplerpc.utils import sync_wrapper
from poco.exceptions import InvalidOperationException


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
            options['action_interval'] = 0.1

        if addr[0] == "localhost" or addr[0] == "127.0.0.1":
            from poco.drivers.windows.sdk.WindowsUI import PocoSDKWindows
            self.sdk = PocoSDKWindows(addr)
            self.SDKProcess = threading.Thread(target=self.sdk.run)  # 创建线程
            self.SDKProcess.setDaemon(True)
            self.SDKProcess.start()

        dev = VirtualDevice(addr[0])
        super(WindowsPoco, self).__init__(addr[1], dev, False, **options)
        
        self.selector = selector
        self.connect_window(self.selector)

    @sync_wrapper
    def connect_window(self, selector):
        return self.agent.rpc.call("ConnectWindow", selector)

    @sync_wrapper
    def set_foreground(self):
        return self.agent.rpc.call("SetForeground")

    def scroll(self, direction='vertical', percent=1, duration=2.0):
        # 重写Win下的Scroll函数，percent代表滑动滚轮多少次，正数为向上滑，负数为向下滑，direction无用，只能上下滚
        if direction not in ('vertical', 'horizontal'):
            raise ValueError('Argument `direction` should be one of "vertical" or "horizontal". Got {}'.format(repr(direction)))
        if direction is 'horizontal':
            raise InvalidOperationException("Windows does not support horizontal scrolling currently")
            
        return self.agent.input.scroll(direction, percent, duration)

    def rclick(self, pos):
        return self.agent.input.rclick(pos[0], pos[1])

    def double_click(self, pos):
        return self.agent.input.double_click(pos[0], pos[1])

    def keyevent(self, keyname):
        return self.agent.input.keyevent(keyname)
