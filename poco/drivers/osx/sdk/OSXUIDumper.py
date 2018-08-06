# coding=utf-8


from poco.sdk.AbstractDumper import AbstractDumper
from poco.drivers.osx.sdk.OSXUINode import OSXUINode
from poco.sdk.exceptions import InvalidSurfaceException


class OSXUIDumper(AbstractDumper):

    def __init__(self, root):
        self.RootControl = root
        self.RootHeight = self.RootControl.AXSize[1]
        self.RootWidth = self.RootControl.AXSize[0]
        self.RootLeft = self.RootControl.AXPosition[0]
        self.RootTop = self.RootControl.AXPosition[1]
        if self.RootWidth == 0 or self.RootHeight == 0:
            raise InvalidSurfaceException(self, "You may have minimized your window or the window is too small!")

    def getRoot(self):
        return OSXUINode(self.RootControl, self)
