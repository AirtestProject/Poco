# coding=utf-8

from poco.sdk.exceptions import UnableToSetAttributeException

__author__ = 'lxn3032'
__all__ = ['AbstractNode']


class AbstractNode(object):
    """
    AbstractNode is a wrapper class that provides ui hierarchy and node info in game engine.

    This class has node parent/children/attribute methods,
    """

    def getParent(self):
        """
        Return the parent node of this node. If no parent or this is the root node, return None.
        This method will be invoked by Selector or Dumper to get the UI Hierarchy

        :rettype: AbstractNode/None
        """

        return None

    def getChildren(self):
        """
        Return an iterator over all children node of this node.
        This method will be invoked by Selector or Dumper to get the UI Hierarchy

        :rettype: Iterable<AbstractNode>
        """

        raise NotImplementedError

    def getAttr(self, attrName):
        """
        Return the attributes of the node.
        All attributes in `cls.RequiredAttributes` are required to be implemented in this method.
        Other engine-specific attributes are optional, which will be used in poco query.

        Required attributes are defined as follows:
            "name": the name of the node, a unique and meaningful name for each node recommended.
            "type": the type name of the node, can be any string. e.g. "android.widget.Button" or as simple as "Button"
            "visible": whether the node is rendered on screen.
                       If the return value is False, all children nodes will be ignored in Poco selector
            "pos": position of the node in screen. Return value should be 2-elements-list represents the percents of
                    the coordinate(x, y) in the whole screen. e.g. if the node locates in the center of the screen,
                    this attribute will be [0.5f, 0.5f].
                    position can be negative which means the node is outside the screen
            "size": size of node's bounding box. similar to "pos", value is also a 2-elements-list of percents of the screen size,
                    e.g. the screen's size is always [1.0f, 1.0f].
                    if the node in left half side of the screen, its size will be [0.5f, 1.0f].
                    size should always be nonnegative.
            "scale": the scale factor applied to the node itself. leave it [1.0f, 1.0f] as default.
            "anchorPoint": the percentage of the key-point related to the bounding box of the node. leave it [0.5f, 0.5f] as default.
            "zOrders": the rendering order of this node. value is a dictionary like {"global": 0, "local": 0}.
                       the global zOrder is compared with all nodes in the hierarchy,
                       the local zOrder is compared with its parent and siblings.
                       topmost nodes have the largest value.

        :param attrName: attribute name, any of the `RequiredAttributes`
        :rettype: <any of JsonSerializable>
        :return: Attribute value. None if no such attribute.
        """

        attrs = {
            'name': '<Root>',
            'type': 'Root',
            'visible': True,
            'pos': [0.0, 0.0],
            'size': [0.0, 0.0],
            'scale': [1.0, 1.0],
            'anchorPoint': [0.5, 0.5],
            'zOrders': {'local': 0, 'global': 0},
        }

        return attrs.get(attrName)

    def setAttr(self, attrName, val):
        """
        Apply changes of the attribute value to this node.
        Only limited attributes may be modified, such as text.
        Some others are not recommended to modified, such as position/name, which may hard to understand for testers
        and results in unexpected exceptions.

        :param attrName: attribute name
        :param val: attribute value
        :retval: None
        """

        raise UnableToSetAttributeException(attrName, None)

    def getAvailableAttributeNames(self):
        """
        enumerate all available attributes' name of this node

        :rettype: Iterable<string>
        """

        return (
            "name",
            "type",
            "visible",
            "pos",
            "size",
            "scale",
            "anchorPoint",
            "zOrders",
        )

    def enumerateAttrs(self):
        """
        :rettype: Iterable<string, ValueType>
        """

        for attrName in self.getAvailableAttributeNames():
            yield attrName, self.getAttr(attrName)
