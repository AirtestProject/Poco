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

    def getPortSize(self):
        """
        hierarchy中的尺寸，一般就取屏幕的物理分辨率

        :retval:  [width, height] in floats of pixels
        :rettype: list
        """

        raise NotImplementedError
