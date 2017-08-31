# coding=utf-8

__author__ = 'lxn3032'
__all__ = ['NoSuchTargetException', 'NodeHasBeenRemovedException', 'UnableToSetAttributeException',
           'NoSuchComparatorException', 'NoSuchAttributeException']


class NodeHasBeenRemovedException(Exception):
    def __init__(self, attrName, node):
        msg = 'Node was no longer alive when query attribute "{}". Please re-select.'.format(attrName)
        super(NodeHasBeenRemovedException, self).__init__(msg)


class UnableToSetAttributeException(Exception):
    def __init__(self, attrName, node):
        msg = 'Unable to set attribute "{}" of node "{}".'.format(attrName, node)
        super(UnableToSetAttributeException, self).__init__(msg)


class NoSuchTargetException(Exception):
    pass


class NoSuchComparatorException(Exception):
    def __init__(self, matchingMethod, matcherName):
        super(NoSuchComparatorException, self).__init__()
        self.message = 'No such matching method "{}" of this Matcher ("{}")'.format(matchingMethod, matcherName)
