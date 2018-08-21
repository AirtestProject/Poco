# -*- coding: utf-8 -*-

import threading
from poco.drivers.std import StdPoco
from poco.utils.device import VirtualDevice
from poco.drivers.std import DEFAULT_ADDR, DEFAULT_PORT
from poco.utils.simplerpc.utils import sync_wrapper
from poco.exceptions import InvalidOperationException


class OSXPoco(StdPoco):

    def __init__(self, selector=None, addr=DEFAULT_ADDR, **options):
        if 'action_interval' not in options:
            options['action_interval'] = 0.5

        if addr[0] == "localhost" or addr[0] == "127.0.0.1":
            from poco.drivers.osx.sdk.OSXUI import PocoSDKOSX
            sdk = PocoSDKOSX(addr)
            self.SDKProcess = threading.Thread(target=sdk.run)  # 创建线程
            self.SDKProcess.setDaemon(True)
            self.SDKProcess.start()

        dev = VirtualDevice(addr[0])
        super(OSXPoco, self).__init__(addr[1], dev, False, **options)
       
        self.selector = selector
        self.connect_window(self.selector)
        self.set_foreground()

    @sync_wrapper
    def connect_window(self, selector):
        return self.agent.rpc.call("ConnectWindow", selector)

    @sync_wrapper
    def set_foreground(self):
        return self.agent.rpc.call("SetForeground")

    @sync_wrapper
    def scroll(self, direction='vertical', percent=1, duration=2.0): 
        # 重写Mac下的Scroll函数，percent代表滑动滚轮多少次，正数为向上滑，负数为向下滑,只能上下滚,左右滚支持不太好
        if direction not in ('vertical', 'horizontal'):
            raise ValueError('Argument `direction` should be one of "vertical" or "horizontal". Got {}'.format(repr(direction)))
        if direction is 'horizontal':
            raise InvalidOperationException("MacOS does not support horizontal scrolling well")
        return self.agent.rpc.call("Scroll", direction, percent, duration)
