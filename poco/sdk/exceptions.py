# coding=utf-8

"""
This module provides several exceptions for poco sdk. These exceptions are only raised in sdk corresponding runtime.
"""


__author__ = 'lxn3032'
__all__ = ['NoSuchTargetException', 'NodeHasBeenRemovedException', 'UnableToSetAttributeException',
           'NoSuchComparatorException']


class NodeHasBeenRemovedException(Exception):
    """
    Raises if node (UI element) refreshed (updated, recycled or destroyed) when retrieving attributes at traversing. 
    For some engines, the UI hierarchy is refreshing in another thread when poco is traversing. At the moment poco is 
    retrieving attribute on the UI element that is refreshed, this may trigger an engine error. Poco sdk catches 
    this engine error and transform into this exception.
    """

    def __init__(self, attrName, node):
        msg = 'Node was no longer alive when query attribute "{}". Please re-select.'.format(attrName)
        super(NodeHasBeenRemovedException, self).__init__(msg)


class UnableToSetAttributeException(Exception):
    """
    Raises when fail to set attributes on UI element. Mostly, the reason may be the UI element is not support to mutate 
    attribute. At the view of sdk implementation, you can throw this exception proactively to indicate that modification 
    is not allowed.
    """

    def __init__(self, attrName, node):
        msg = 'Unable to set attribute "{}" of node "{}".'.format(attrName, node)
        super(UnableToSetAttributeException, self).__init__(msg)


class NoSuchTargetException(Exception):
    """
    Raises when index out of range on selecting UI element by given index. 
    
    .. TODO:: Maybe this is a little bit redundant to :py:class:`poco.exceptions.PocoNoSuchNodeException`. 
     Should be optimized.
    """

    pass


class NoSuchComparatorException(Exception):
    """
    When the matcher does not support the given comparison method, this will be raised.
    """

    def __init__(self, matchingMethod, matcherName):
        super(NoSuchComparatorException, self).__init__()
        self.message = 'No such matching method "{}" of this Matcher ("{}")'.format(matchingMethod, matcherName)
