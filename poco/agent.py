# coding=utf-8

from poco.sdk.interfaces.hierarchy import HierarchyInterface
from poco.sdk.interfaces.input import InputInterface
from poco.sdk.interfaces.screen import ScreenInterface
from poco.sdk.interfaces.command import CommandInterface

__author__ = 'lxn3032'


class PocoAgent(object):
    def __init__(self, hierarchy, input, screen, command=None):
        self.hierarchy = hierarchy or HierarchyInterface()
        self.input = input or InputInterface()
        self.screen = screen or ScreenInterface()
        self.command = command or CommandInterface()
