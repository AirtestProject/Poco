# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:47:51

from poco.drivers.std import StdPoco
from airtest.core.device import Device


__all__ = ['QtPoco']
DEFAULT_PORT = 9001
DEFAULT_ADDR = ("localhost", DEFAULT_PORT)


class QtPoco(StdPoco):
    """
    Poco Qt implementation.
    """

    def __init__(self, addr=DEFAULT_ADDR, **options):
        super(QtPoco, self).__init__(addr[1], Device(), **options)
