# coding=utf-8

from poco.sdk.AbstractDumper import AbstractDumper
from poco.vendor.local.Node import Node


class Dumper(AbstractDumper):
    def __init__(self, dumpable):
        self.dumpable = dumpable

    def _build_tree(self, root):
        for child in root.getChildren():
            child.setParent(root)
            self._build_tree(child)

    def getRoot(self):
        # 每次获取root时，就给一个新的root
        root = Node(self.dumpable.dumpHierarchy())
        for child in root.getChildren():
            child.setParent(root)
        return root

    def getPortSize(self):
        return 1.0, 1.0
