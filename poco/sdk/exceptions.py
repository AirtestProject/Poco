# coding=utf-8

"""
This module provides several exceptions for poco-sdk. These exceptions are raised only in sdk corresponding runtime.
"""


__author__ = 'lxn3032'
__all__ = ['NoSuchTargetException', 'NodeHasBeenRemovedException', 'UnableToSetAttributeException',
           'NoSuchComparatorException', 'NonuniqueSurfaceException', 'InvalidSurfaceException']


class NodeHasBeenRemovedException(Exception):
    """
    Raised when the node (UI element) is refreshed (updated, recycled or destroyed) while retrieving the attributes
    during traversing the hierarchy.

    In some engines implementations, the UI hierarchy is refreshed in a stand-alone thread while poco is performing
    the traverse process, so the engine error might be triggered when poco is trying to retrieve the attribute of
    the UI element but the attribute is being updated at the same time. In this situation, poco sdk catches the engine
    error and raises this exception.
    """

    def __init__(self, attrName, node):
        msg = 'Node was no longer alive when query attribute "{}". Please re-select.'.format(attrName)
        super(NodeHasBeenRemovedException, self).__init__(msg)


class UnableToSetAttributeException(Exception):
    """
    Raised when settings the attribute of the given UI element failed. In most cases, the reason why it failed is that
    the UI element does not support mutation. From the point of view of SDK implementation, this exception can be
    raised proactively to indicate that the modification of the attribute is not allowed.
    """

    def __init__(self, attrName, node):
        msg = 'Unable to set attribute "{}" of node "{}".'.format(attrName, node)
        super(UnableToSetAttributeException, self).__init__(msg)


class NoSuchTargetException(Exception):
    """
    Raised when the index is out of range for selecting the UI element by given index.
    
    .. TODO:: Maybe this is a little bit redundant to :py:class:`poco.exceptions.PocoNoSuchNodeException`. 
     Should be optimized.
    """

    pass


class NoSuchComparatorException(Exception):
    """
    Raised when the matcher does not support the given comparison method.
    """

    def __init__(self, matchingMethod, matcherName):
        super(NoSuchComparatorException, self).__init__()
        self.message = 'No such matching method "{}" of this Matcher ("{}")'.format(matchingMethod, matcherName)


class NonuniqueSurfaceException(Exception):
    """
    Raised when the device selector matches multiple devices surface
    """

    def __init__(self, selector):
        msg = 'The arguments ("{}") match multiple device surface. More precise conditions required.'.format(selector)
        super(NonuniqueSurfaceException, self).__init__(msg)


class InvalidSurfaceException(Exception):
    """
    Raised when the device surface is invalid
    """

    def __init__(self, target, msg="None"):
        msg = 'Target device surface invalid ("{}") . Detail message: "{}"'.format(target, msg)
        super(InvalidSurfaceException, self).__init__(msg)

