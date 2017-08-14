# coding=utf-8

import types

from poco.sdk.interfaces.hierarchy import HierarchyInterface
from poco.sdk.interfaces.input import InputInterface
from poco.sdk.interfaces.screen import ScreenInterface
from poco.sdk.interfaces.command import CommandInterface

__author__ = 'lxn3032'


def _assign(val, default_val):
    if isinstance(val, types.NoneType):
        return default_val
    else:
        return val


class PocoAgent(object):
    def __init__(self, hierarchy, input, screen, command=None):
        self.hierarchy = _assign(hierarchy, HierarchyInterface())
        self.input = _assign(input, InputInterface())
        self.screen = _assign(screen, ScreenInterface())
        self.command = _assign(command, CommandInterface())
