# coding=utf-8

from .exceptions import UnableToSetAttributeException

__author__ = 'lxn3032'
__all__ = ['AbstractNode']


class AbstractNode(object):
    """
    AbstractNode is a wrapper class that provides UI hierarchy and node info in game engine.

    This class uniformly specifies node-related methods such as retrieving the attributes or accessing the parent nodes
    or their children.
    """

    def getParent(self):
        """
        Return the parent node of this node. Return None if there is no parent or parent is not accessible or this is
        the root node. This method is invoked by ``Selector`` or ``Dumper`` when traversing UI hierarchy.

        Returns:
            :py:class:`AbstractNode or NoneType <poco.sdk.AbstractNode>`: parent node of this node or None.
        """

        return None

    def getChildren(self):
        """
        Return an iterator over all children nodes of this node. This method is invoked by ``Selector`` or ``Dumper``
        to retrieve the UI hierarchy.

        Returns:
            Iterable <:py:class:`AbstractNode <poco.sdk.AbstractNode>`>
        """

        raise NotImplementedError

    def getAttr(self, attrName):
        """
        Return the attributes of the node. The list below shows the most used basic attributes used during while writing
        test code. The implementation class should return the corresponding value as soon as it retrieves its value. If
        the value cannot be determined, the default value is obtained from super class invocation and returned.  See the
        example below for more detailed information. More attributes can be added in order to enhance the selection
        and displaying in ``Inspector``.

        The most used basic attributes are listed as follows:

        - ``name``: name of the node, use the unique and meaningful name for each node is recommended
        - ``type``: type of the name of the node, it can be either any string, e.g. "android.widget.Button" or just
          simple as "Button"
        - ``visible``: True or False whether the node is rendered on screen. In case the return value is False, all
          children nodes are ignored in Poco selector
        - ``pos``: position of the node in screen, return value should be 2-list coordinates (x, y) representing
          the percentage of the screen. e.g. if the node lies in the center of the screen, the attribute will be
          ``[0.5f, 0.5f]``. If the returned value for position is negative, it means the node lies out of the screen
        - ``size``: size of the node bounding box, similar to ``pos``, value is also a 2-list of the percentage of
          the screen size, e.g. the screen size is always ``[1.0f, 1.0f]``,
          if the node lies in left half side of the screen, its size will be ``[0.5f, 1.0f]``, the returned value of
          size should be always positive value
        - ``scale``: scale factor applied to the node itself, leave it ``[1.0f, 1.0f]`` by default
        - ``anchorPoint``: 2-list coordinates (x, y) of the anchor expressed in the percentage related to the bounding
          box of the node, leave it ``[0.5f, 0.5f]`` by default.
        - ``zOrders``: rendering order of this node, its value is a dictionary such as ``{"global": 0, "local": 0}``,
          global zOrder value is compared with all nodes in the hierarchy, local zOrder value is compared with its
          parent and siblings. The most top nodes have the largest values.

        Examples:
            The following sample code demonstrates some ideas about the implementation of this method::
                
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
        Apply changes of the attribute value to this node. Not all attributes can be modified. The most common
        attribute to be modified is the `text`. It is not recommended to modify attributes such as position, name,
        their modifications can lead to unexpected and false-positive errors.

        Args:
            attrName (:obj:`str`): attribute name
            val: attribute value

        Returns:
            True if success else False or raise.

        See Also:
            :py:meth:`setAttr <poco.sdk.interfaces.hierarchy.HierarchyInterface.setAttr>` in
            ``poco.sdk.interfaces.hierarchy``
        """

        raise UnableToSetAttributeException(attrName, None)

    def getAvailableAttributeNames(self):
        """
        Enumerate all available attribute names of this node. This method in base class returns the basic
        attribute name by default. It is possible to add other customized or engine-specific attributes.
        See the example below.

        .. note:: It is recommended to always call the super method and return should contain the part from super method.

        Examples:
            This code demonstrates how to implement this method::

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
        Enumerate all available attributes and yield the 2-tuple (name, value).

        Yields:
            Iterable<:obj:`str`, :obj:`ValueType`>
        """

        for attrName in self.getAvailableAttributeNames():
            yield attrName, self.getAttr(attrName)
