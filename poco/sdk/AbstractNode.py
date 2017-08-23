# coding=utf-8

__author__ = 'lxn3032'
__all__ = ['AbstractNode']


class AbstractNode(object):
    """
    AbstractNode class is a wrapper-like class which wrapped the real node object in target engine.
    
    This class provider standard node spec methods,  
    """

    RequiredAttributes = (
        "name",
        "type",
        "visible",
        "pos",
        "size",
        "scale",
        "anchorPoint",
        "zOrders",
    )

    def getParent(self):
        """
        Return the parent node of this node. If no parent or this is the root node, return None.
        This method will be invoked by Selector or Dumper to walk through the whole tree of the rendering nodes.
        
        :rettype: AbstractNode/None
        """

        raise NotImplementedError

    def getChildren(self):
        """
        Return an iterator over all children of this node.
        This method will be invoked by Selector or Dumper to walk through the whole tree of the rendering nodes.

        :rettype: Iterable<AbstractNode>
        """

        raise NotImplementedError

    def getAttr(self, attrName):
        """
        Retrieve the attributes of the node.
        This method should at least implement retrieving attributes in `RequiredAttributes`.
        
        Each attribute defines as following:
            "name": the name of the node, please name it yourself if engine dose not have a name for each node.
                    return a unique name is better than default value.
            "type": the type name of the node, can be any string. e.g. "android.widget.Button" or as simple as you 
                    like "Button"
            "visible": whether the node is arrange to render on screen. this is different from visibleToUser and 
                       transparency, if a node is transparent or its size is 0 is invisible to user, but it and its 
                       children will still be scheduled to render.
            "pos": position of the node no matter the size of the node. value should be 2-elements-list represents the
                   coordinate(x, y) percents of the whole screen. e.g. if the node locates in the center of the screen,
                   this attribute will be [0.5f, 0.5f].
            "size": size of node's square convex hull. similar to "pos", value is also a 2-elements-list of percents 
                    related to screen size, not parent. e.g. the screen's size is always [1.0f, 1.0f]. if the node in 
                    left half side of the screen, its size will be [0.5f, 1.0f]. position can be negative which means 
                    outside the screen but size should always be position or zero.
            "scale": the scale factor applied to the node itself. leave it [1.0f, 1.0f] as default value or if engine
                     does not have this attribute.
            "anchorPoint": the point related to the square convex hull of the node. leave it [0.5f, 0.5f] as default 
                           value or if engine does not have this attribute.
            "zOrders": the rendering orders of the node. value is a dict like {"global": 0, "local": 0}. the global
                       zOrder compares with all nodes in the tree, the local zOrder is only related to its parent and
                       compares with the siblings. the larger the value, more top in screen which is closer to user.
        
        Add any other attributes in order to get more details of a node.

        :param attrName: attribute name, any of the `RequiredAttributes`
        :rettype: <any of JsonSerializable>
        :return: Attribute value. None if no such attribute.
        """

        raise NotImplementedError

    def setAttr(self, attrName, val):
        """
        Apply changes of the attribute value of this node.
        Only several attributes can be modified, such as text.
        Some others are not recommended to modified, such as position/name, which may hard to understand for testers
        and results in unexpected exceptions.
        
        :param attrName: attribute name
        :param val: attribute value
        :retval: None
        """

        raise NotImplementedError

    def enumerateAttrs(self):
        """
        :rettype: Iterable<string, ValueType>
        """

        raise NotImplementedError
