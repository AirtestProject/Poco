# coding=utf-8

import uiautomation as UIAuto
from poco.sdk.exceptions import UnableToSetAttributeException
from poco.sdk.AbstractNode import AbstractNode


class WindowsUINode(AbstractNode):

    def __init__(self, control, dumper):
        self.Control = control
        self.Children = []
        self.dumper = dumper

    def getParent(self):
        return WindowsUINode(self.Control.GetParentControl(), self.dumper)

    def getChildren(self):
        if len(self.Children):  # 防止多次获取children，提高性能
            for node in self.Children:
                yield WindowsUINode(node, self.dumper)
        else:
            self.Children = self.Control.GetChildren()
            for node in self.Children:
                yield WindowsUINode(node, self.dumper)

    def getAttr(self, attrName):

        if attrName == 'name':
            strr = self.Control.Name
            if strr != "":
                return strr
            return self.Control.ControlTypeName.replace("Control", "")
            
        if attrName == 'originType':
            return self.Control.ControlTypeName

        if attrName == 'type':
            return self.Control.ControlTypeName.replace("Control", "")

        if attrName == 'pos':
            rect = self.Control.BoundingRectangle
            # 计算比例
            pos1 = float(rect[0] + (rect[2] - rect[0]) / 2.0 - self.dumper.RootLeft) / float(self.dumper.RootWidth)
            pos2 = float(rect[1] + (rect[3] - rect[1]) / 2.0 - self.dumper.RootTop) / float(self.dumper.RootHeight)
            return [pos1, pos2]

        if attrName == 'size':
            rect = self.Control.BoundingRectangle
            pos1 = float(rect[2] - rect[0]) / float(self.dumper.RootWidth)
            pos2 = float(rect[3] - rect[1]) / float(self.dumper.RootHeight)
            return [pos1, pos2]

        if attrName == 'text':
            # 先判断控件是否有text属性
            if ((isinstance(self.Control, UIAuto.ValuePattern) and self.Control.IsValuePatternAvailable())):
                return self.Control.CurrentValue()
            else:
                return None

        if attrName == '_instanceId':
            return self.Control.Handle
            
        return super(WindowsUINode, self).getAttr(attrName)

    def setAttr(self, attrName, val):
        if attrName != 'text':
            raise UnableToSetAttributeException(attrName, self)
        else:
            if ((isinstance(self.Control, UIAuto.ValuePattern) and self.Control.IsValuePatternAvailable())):
                self.Control.SetValue(val)
                return True
            else:
                raise UnableToSetAttributeException(attrName, self)

    def getAvailableAttributeNames(self):
        if ((isinstance(self.Control, UIAuto.ValuePattern) and self.Control.IsValuePatternAvailable())):
            return super(WindowsUINode, self).getAvailableAttributeNames() + ('text', '_instanceId', 'originType')
        else:
            return super(WindowsUINode, self).getAvailableAttributeNames() + ('_instanceId', 'originType')
