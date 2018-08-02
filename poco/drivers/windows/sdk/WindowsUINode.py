# coding=utf-8

from poco.sdk.exceptions import UnableToSetAttributeException
from poco.sdk.AbstractNode import AbstractNode
import uiautomation as UIAuto

__author__ = 'linzecong'


class WindowsUINode(AbstractNode):

    NameTime = {}

    def __init__(self, control, dumper):
        self.Control = control
        self.Children = []
        self.dumper = dumper

    def getParent(self):
        return WindowsUINode(self.Control.GetParentControl(), self.dumper)

    def getChildren(self):
        if len(self.Children):
            for node in self.Children:
                yield WindowsUINode(node, self.dumper)
        else:
            self.Children = self.Control.GetChildren()
            for node in self.Children:
                yield WindowsUINode(node, self.dumper)

    def getAttr(self, attrName):
        # default value
        attrs = {
            'name': '<Root>',
            'originType': 'Unknow',
            'type': 'Root',
            'visible': True,
            'pos': [0.0, 0.0],
            'size': [0.0, 0.0],
            'scale': [1.0, 1.0],
            'anchorPoint': [0.5, 0.5],
            'zOrders': {'local': 0, 'global': 0},
            'text': 'Empty',
        }

        if attrName == 'name':
            newname = "Uname"
            strr = self.Control.Name
            if strr != "":
                newname = strr
            if newname in WindowsUINode.NameTime:
                WindowsUINode.NameTime[newname] += 1
            else:
                WindowsUINode.NameTime[newname] = 0
            if WindowsUINode.NameTime[newname] != 0:
                newname = newname + str(WindowsUINode.NameTime[newname])
            return newname

        if attrName == 'originType':
            return self.Control.ControlTypeName

        if attrName == 'type':
            return self.Control.ControlTypeName.replace("Control", "")

        if attrName == 'pos':
            rect = self.Control.BoundingRectangle
            return [float(rect[0] + (rect[2] - rect[0]) / 2.0 - self.dumper.RootLeft) / float(self.dumper.RootWidth), float(rect[1] + (rect[3] - rect[1]) / 2.0 - self.dumper.RootTop) / float(self.dumper.RootHeight)]

        if attrName == 'size':
            rect = self.Control.BoundingRectangle
            return [float(rect[2] - rect[0]) / float(self.dumper.RootWidth), float(rect[3] - rect[1]) / float(self.dumper.RootHeight)]

        if attrName == 'text':
            if ((isinstance(self.Control, UIAuto.ValuePattern) and self.Control.IsValuePatternAvailable())):
                return self.Control.CurrentValue()
            else:
                return 'Empty'

        if attrName == '_instanceId':
            return self.Control.Handle
        return attrs.get(attrName)

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
        return super(WindowsUINode, self).getAvailableAttributeNames() + ('text', '_instanceId', 'originType')
