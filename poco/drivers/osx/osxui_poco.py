# -*- coding: utf-8 -*-

from poco.drivers.std import StdPoco
from poco.utils.device import VirtualDevice
from poco.drivers.std import DEFAULT_ADDR, DEFAULT_PORT
from poco.utils.simplerpc.utils import sync_wrapper
from airtest.core.error import DeviceConnectionError
import threading


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

        argusnum = int('bundleid' in selector) + int('title' in selector) + int('title_re' in selector)
        if argusnum == 0:
            raise DeviceConnectionError("need bundleid or title to connect device")
        elif argusnum != 1:
            raise DeviceConnectionError("too many arguments, only need bundleid or title or title_re")
        
        self.selector = selector
        ok = self.connect_window(self.selector)
        if not ok:
            raise DeviceConnectionError("Can't find any windows by the given parameter")
        else:
            self.set_foreground()

    @sync_wrapper
    def connect_window(self, selector):
        return self.agent.rpc.call("ConnectWindow", selector)

    @sync_wrapper
    def set_foreground(self):
        return self.agent.rpc.call("SetForeground")
