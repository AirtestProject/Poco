# coding=utf-8


from poco.sdk.AbstractDumper import AbstractDumper
from uiautomation import uiautomation as UIAuto
from WindowsUINode import WindowsUINode

__author__ = 'linzecong'

class WindowsUIDumper(AbstractDumper):

    def __init__(self, root):
        self.RootControl=root
        self.RootHeight = self.RootControl.BoundingRectangle[3] - self.RootControl.BoundingRectangle[1]
        self.RootWidth = self.RootControl.BoundingRectangle[2] - self.RootControl.BoundingRectangle[0]
        self.RootLeft = self.RootControl.BoundingRectangle[0]
        self.RootTop = self.RootControl.BoundingRectangle[1]
        
    def getRoot(self):
        
        return WindowsUINode(self.RootControl, self)
