# coding=utf-8


from poco.sdk.AbstractDumper import AbstractDumper
from poco.sdk.exceptions import InvalidTargetException
from poco.drivers.windows.sdk.WindowsUINode import WindowsUINode
import uiautomation as UIAuto

__author__ = 'linzecong'


class WindowsUIDumper(AbstractDumper):

    def __init__(self, root):
        self.RootControl = root
        self.RootHeight = self.RootControl.BoundingRectangle[3] - self.RootControl.BoundingRectangle[1]
        self.RootWidth = self.RootControl.BoundingRectangle[2] - self.RootControl.BoundingRectangle[0]
        self.RootLeft = self.RootControl.BoundingRectangle[0]
        self.RootTop = self.RootControl.BoundingRectangle[1]

        if self.RootWidth == 0 or self.RootHeight == 0:
                raise InvalidTargetException(self, "You may have minimized your window or the window is too small!")

    def getRoot(self):
        return WindowsUINode(self.RootControl, self)
