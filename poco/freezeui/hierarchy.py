# coding=utf-8

from poco.sdk.AbstractDumper import AbstractDumper
from poco.sdk.AbstractNode import AbstractNode
from poco.sdk.Attributor import Attributor
from poco.sdk.Selector import Selector
from poco.sdk.exceptions import UnableToSetAttributeException
from poco.sdk.interfaces.hierarchy import HierarchyInterface


__all__ = ['FrozenUIDumper', 'FrozenUIHierarchy']


class FrozenUIDumper(AbstractDumper):
    """
    Partially implementation of IDumper. This is only a helper that helps to make dumper work with local nodes just 
    like with remote nodes. The local nodes is an implementation of :py:class:`AbstractNode <poco.sdk.AbstractNode>` 
    locally with fixed hierarchy data in arbitrary data type. In a word, this class is not going to crawl hierarchy from 
    target app, but to perform like a ordinary dumper.
    """

    def dumpHierarchy(self, onlyVisibleNode=True):
        raise NotImplementedError

    def getRoot(self):
        """
        Dump a hierarchy immediately from target runtime and store into a Node (subclass of :py:class:`AbstractNode 
        <poco.sdk.AbstractNode>`) object.

        Returns:
            :py:class:`inherit from AbstractNode <Node>`: Each time a new node instance is created by latest hierarchy 
             data.
        """

        root = Node(self.dumpHierarchy())
        self._linkParent(root)
        return root

    def _linkParent(self, root):
        parent = root.getChildren()
        if parent:
            for child in parent:
                child.setParent(root)
                self._linkParent(child)



class FrozenUIHierarchy(HierarchyInterface):
    """
    Locally implementation of hierarchy interface with a given dumper and all other behaviours by default. As all 
    information can only be retrieve from a fixed UI hierarchy data created by dumper and all UI elements are immutable, 
    this class is called frozen hierarchy. With the help of this class, only very few of the methods are required to
    implement. See :py:class:`AbstractNode <poco.sdk.AbstractNode>` or poco-sdk integration guide to get more details 
    about this. 
     
    This class makes it much easier to integrate poco-sdk and optimizes performance in some situations, but it is not 
    sensitive enough to the changes of UI hierarchy in the app. For example, you should call ``select`` explicitly to 
    re-crawl a new UI hierarchy when some UI elements changed on screen. Otherwise you are using attributes that are 
    out of date.
    """

    def __init__(self, dumper, attributor=None):
        super(FrozenUIHierarchy, self).__init__()
        self.dumper = dumper
        self.selector = Selector(self.dumper)
        self.attributor = attributor or Attributor()

    def dump(self):
        return self.dumper.dumpHierarchy()

    def getAttr(self, nodes, name):
        """
        get node attribute
        """

        return self.attributor.getAttr(nodes, name)

    def setAttr(self, nodes, name, value):
        """
        set node attribute
        """

        return self.attributor.setAttr(nodes, name, value)

    def select(self, query, multiple=False):
        """
        select nodes by query
        """

        return self.selector.select(query, multiple)


class Node(AbstractNode):
    def __init__(self, node):
        super(Node, self).__init__()
        self.node = node

    def setParent(self, p):
        self.node['__parent__'] = p

    def getParent(self):
        return self.node.get('__parent__')

    def getChildren(self):
        for child in self.node.get('children') or []:
            yield Node(child)

    def getAttr(self, attrName):
        return self.node['payload'].get(attrName)

    def setAttr(self, attrName, val):
        # cannot set any attributes on local nodes
        raise UnableToSetAttributeException(attrName, self.node)

    def getAvailableAttributeNames(self):
        return self.node['payload'].keys()
