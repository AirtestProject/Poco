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
    """
    This is a aggregation class of 4 major interfaces for poco to communicate with target device. PocoAgent is
    introduced to handle scattered control units and provider a uniform entry to assess target device.

    There are 4 major parts at the moment.
        - ``HierarchyInterface``: Defines some hierarchy accessibility methods such as dump(crawl the whole UI tree), 
          getAttr(retrieve attribute value by name).
        - ``InputInterface``: Defines simulated input methods to make it possible to inject simulated input on target 
          device.
        - ``ScreenInterface``: Defines methods to access the screen surface.
        - ``CommandInterface``: Defines methods to communicate with target device in arbitrary way. This is optional.
    """

    def __init__(self, hierarchy, input, screen, command=None):
        self.hierarchy = _assign(hierarchy, HierarchyInterface())
        self.input = _assign(input, InputInterface())
        self.screen = _assign(screen, ScreenInterface())
        self.command = _assign(command, CommandInterface())
