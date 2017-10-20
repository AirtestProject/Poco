# coding=utf-8

from poco.sdk.exceptions import UnableToSetAttributeException

__author__ = 'lxn3032'
__all__ = ['AbstractNode']


class AbstractNode(object):
    """
    AbstractNode is a wrapper class that provides ui hierarchy and node info in game engine.

    This class uniformly specifies node-related methods such as retrieving attribute or accessing up to parent or down 
    to children.
    """

    def getParent(self):
        """
        Return the parent node of this node. Return None if no parent or parent is not accessible or this is the root 
        node. This method will be invoked by ``Selector`` or ``Dumper`` when traversing UI hierarchy.

        Returns:
            :py:class:`AbstractNode or NoneType <poco.sdk.AbstractNode>`: Parent node of this node or None.
        """

        return None

    def getChildren(self):
        """
        Return an iterator over all children nodes of this node. Will be invoked by ``Selector`` or ``Dumper`` to get 
        the UI hierarchy.

        Returns:
            Iterable<:py:class:`AbstractNode <poco.sdk.AbstractNode>`>
        """

        raise NotImplementedError

    def getAttr(self, attrName):
        """
        Return the attributes of the node. The following list shows the most basic attributes that will be used during 
        the test run. The implementation class should return correct value as possible as it can. If cannot determine 
        the value, return the invocation from super class to use default value. See the example below. More attributes 
        can be added in order to enhance the selection and displaying in ``Inspector``.

        Most basic attributes defines as follows:

        - ``name``: The name of the node, a unique and meaningful name for each node recommended.
        - ``type``: The type name of the node, can be any string. e.g. "android.widget.Button" or as simple as 
          "Button"
        - ``visible``: Whether the node is rendered on screen. If the return value is False, all children nodes 
          will be ignored in Poco selector
        - ``pos``: Position of the node in screen. Return value should be 2-list represents the percents of
          the coordinate(x, y) in the whole screen. e.g. if the node locates in the center of the screen,
          this attribute will be ``[0.5f, 0.5f]``.
          position can be negative which means the node is outside the screen
        - ``size``: Size of node's bounding box. similar to ``pos``, value is also a 2-list of percents of 
          the screen size, e.g. the screen's size is always ``[1.0f, 1.0f]``.
          if the node in left half side of the screen, its size will be ``[0.5f, 1.0f]``.
          size should always be nonnegative.
        - ``scale``: The scale factor applied to the node itself. leave it ``[1.0f, 1.0f]`` by default.
        - ``anchorPoint``: The percentage of the key-point related to the bounding box of the node. leave it 
          ``[0.5f, 0.5f]`` by default.
        - ``zOrders``: The rendering order of this node. value is a dictionary like ``{"global": 0, "local": 0}``.
          Global zOrder is compared with all nodes in the hierarchy, Local zOrder is compared with its parent and 
          siblings. Topmost nodes have the largest value.

        Examples:
            The following code gives some idea about implementing this method::
                
                def getAttr(self, attrName):
                    # basic attributes
                    if attrName == 'name':
                        return self.node.get_name() or '<no name>'

                    elif attrName == 'pos':
                        return self.node.get_position()

                    # ...

                    # extra engine-specific attributes
                    elif attrName == 'rotation':
                        return self.node.get_rotation()

                    # call the super method by default
                    else:
                        return super().getAttr(attrName)

        Args:
            attrName (:obj:`str`): attribute name

        Returns:
            JsonSerializable attribute value or None if no such attribute.
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
        Only limited attributes can be modified, such as text.
        Some others are not recommended to modified, such as position/name, which may hard to understand for testers
        and results in unexpected exceptions.

        Args:
            attrName (:obj:`str`): attribute name
            val: attribute value

        See Also:
            :py:meth:`setAttr <poco.sdk.interfaces.hierarchy.HierarchyInterface.setAttr>` in \
             ``poco.sdk.interfaces.hierarchy``
        """

        raise UnableToSetAttributeException(attrName, None)

    def getAvailableAttributeNames(self):
        """
        Enumerate all available attributes' name of this node. This method in base class returns the most basic 
        attribute name by default. You can add other customized or engine-specific attributes. See the example above.

        .. note:: Please always call super method and return should contain the part from super method.

        Examples:
            This code shows a way about implementing this method::

                def getAvailableAttributeNames(self):
                    return super().getAvailableAttributeNames() + (
                        # add other engine-specific attribute names here if need.
                        'rotation',
                    )

        Returns:
            Iterable<:obj:`str`>
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
        Enumerate all available attributes and yielding in 2-tuple (name, value).

        Returns:
            Iterable<:obj:`str`, :obj:`ValueType`>
        """

        for attrName in self.getAvailableAttributeNames():
            yield attrName, self.getAttr(attrName)
