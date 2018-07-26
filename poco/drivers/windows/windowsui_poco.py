# -*- coding: utf-8 -*-

from poco.drivers.std import StdPoco
from poco.utils.device import VirtualDevice
from poco.drivers.std import DEFAULT_ADDR,DEFAULT_PORT
from airtest.core.error import DeviceConnectionError
import win32api
import time
import os


class WindowsPoco(StdPoco):
    """
    Poco WindowsUI implementation.

    Args:
        selector (:py:obj:`dict`): find window by a selector, optional parameters: `name`,`handle`,`name_re`
        name: find windows by name
        handle: find windows by handle
        name_re: find windows by regular expression of name
        addr (:py:obj:`tuple`): where the WindowsUI running on, (localhost,15004) by default
        print_hierarchy (:py:obj:`bool`):  whether print the UI hierarchy in remote server,False by default
        options: see :py:class:`poco.pocofw.Poco`

    Examples:
        
            from poco.drivers.windows import WindowsPoco
            # poco = WindowsPoco({'name':'xxx'})
            # poco = WindowsPoco({'handle':123456})
            # poco = WindowsPoco({'name_re':'[a-z][a-z][a-z]'}) # match the first matched window

    """

    def __init__(self, selector={}, addr=DEFAULT_ADDR, print_hierarchy=False, **options):
        if 'action_interval' not in options:
            options['action_interval'] = 0.5

        if addr == DEFAULT_ADDR:
            win32api.ShellExecute(0, 'open',os.path.dirname(__file__) + "\\sdk\\WindowsUI.py", '', '', 1)

        dev = VirtualDevice(addr[0])
        super(WindowsPoco, self).__init__(addr[1], dev, False, **options)

        if not selector:
            raise DeviceConnectionError("Can't find any windows by the given parameter")

        if 'name' in selector:
            cb = self.agent.rpc.call("ConnectWindowsByName", selector['name'], print_hierarchy)
            ok = cb.wait(timeout=10)
            if not ok[0]:
                raise DeviceConnectionError("Can't find any windows by the given parameter")
            else:
                self.agent.rpc.call("SetForeground")

        if 'handle' in selector:
            cb = self.agent.rpc.call("ConnectWindowsByHandle", selector['handle'], print_hierarchy)
            ok = cb.wait(timeout=10)
            if not ok[0]:
                raise DeviceConnectionError("Can't find any windows by the given parameter")
            else:
                self.agent.rpc.call("SetForeground")

        if "name_re" in selector:
            cb = self.agent.rpc.call("ConnectWindowsByNameRe", selector['name_re'], print_hierarchy)
            ok = cb.wait(timeout=10)
            if not ok[0]:
                raise DeviceConnectionError("Can't find any windows by the given parameter")
            else:
                self.agent.rpc.call("SetForeground")   


        

