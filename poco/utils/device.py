# coding=utf-8
from __future__ import absolute_import

from airtest.core.device import Device


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
