# coding=utf-8
from __future__ import absolute_import

from airtest.core.device import Device
from airtest.core.api import connect_device, device as current_device
from airtest.core.error import NoDeviceError


class VirtualDevice(Device):
    def __init__(self, ip):
        super(VirtualDevice, self).__init__()
        self.ip = ip

    @property
    def uuid(self):
        return 'virtual-device'

    def get_current_resolution(self):
        return [1920, 1080]

    def get_ip_address(self):
        return self.ip


def default_device():
    """
    Get default device, if no device connected, connect to first android device.

    :return:
    """
    try:
        return current_device()
    except NoDeviceError:
        return connect_device('Android:///')
