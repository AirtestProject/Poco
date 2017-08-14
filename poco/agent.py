# coding=utf-8

from poco.sdk.interfaces.command import CommandInterface

__author__ = 'lxn3032'


class PocoAgent(object):
    def __init__(self, hierarchy, input, screen, command=None):
        self.hierarchy = hierarchy
        self.input = input
        self.screen = screen
        self.command = command or CommandInterface()
