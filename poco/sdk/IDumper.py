# coding=utf-8
from poco.sdk.Dumpable import Dumpable


__author__ = 'lxn3032'


class IDumper(Dumpable):

    def getRoot(self):
        """
        Return the root node of the UI Hierarchy

        :rettype: support.poco.sdk.AbstractNode
        """

        raise NotImplementedError

    def dumpHierarchy(self):
        """
        :rettype: dict or NoneType
        """

        raise NotImplementedError
