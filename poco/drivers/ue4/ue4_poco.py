# -*- coding: utf-8 -*-

from poco.drivers.std import StdPoco
from poco.drivers.ue4.device import UE4EditorWindow
from airtest.core.api import connect_device, device as current_device

__all__ = ['UE4Poco', 'DEFAULT_PORT', 'DEFAULT_ADDR']
DEFAULT_PORT = 5001
DEFAULT_ADDR = ('localhost', DEFAULT_PORT)


class UE4Poco(StdPoco):

    def __init__(self, addr=DEFAULT_ADDR, ue4_editor=False, connect_default_device=True, device=None, **options):
        if 'action_interval' not in options:
            options['action_interval'] = 0.5

        if ue4_editor:
            dev = UE4EditorWindow()
        else:
            dev = device or current_device()

        if dev is None and connect_default_device and not current_device():
            dev = connect_device("Android:///")

        super(UE4Poco, self).__init__(addr[1], dev, ip=addr[0], **options)
