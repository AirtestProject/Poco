# coding=utf-8
from __future__ import unicode_literals

import six


__author__ = 'lxn3032'


class PocoException(Exception):
    """
    Base class of exceptions of poco. PY3 compatible.
    """

    def __str__(self):
        if six.PY2:
            if isinstance(self.message, unicode):
                return self.message.encode("utf-8")
            else:
                return self.message
        else:
            if isinstance(self.message, bytes):
                return self.message.decode('utf-8')
            else:
                return self.message

    __repr__ = __str__


class PocoAssertionError(PocoException):
    """
    Warning:
        Deprecated, do not use.
    """

    pass


class InvalidOperationException(PocoException):
    """
    When an operation performing on target device is foreseen, this exceptions will raise.
    For example, click outside the screen is definitely meaningless, an ``InvalidOperationException`` raised.

    操作无效
    通常超出屏幕之外的点击或者滑动会判定为操作无效
    """

    pass


class PocoTargetTimeout(PocoException):
    """
    Timeout when waiting for some condition to be matched. Such as waiting some UI element but it never appeared.
    """

    def __init__(self, action, poco_obj_proxy):
        super(PocoTargetTimeout, self).__init__()
        self.message = 'Timeout when waiting for {} of "{}"'.format(action, poco_obj_proxy)


class PocoNoSuchNodeException(PocoException):
    """
    Cannot find any UI element of given query condition.
    """

    def __init__(self, objproxy):
        super(PocoNoSuchNodeException, self).__init__()
        self.message = 'Cannot find any visible node by query {}'.format(objproxy)


class PocoTargetRemovedException(PocoException):
    """
    This exception raises when hierarchy structure changed over the selection or access a UI element that is already
    recycled. In many cases there is no need to handle this exception by hand. Once this exception occurred, please
    check your code carefully. Most of misuses as follows.
    
    e.g.
    ```py
    button1 = poco('button1')
    time.sleep(10)   # waiting for long enough before the UI hierarchy changing
    button1.click()  # PocoTargetRemovedException will raise at this line. Because the 'button1' is not on the screen.
    ```
    """

    def __init__(self, action, objproxy):
        super(PocoTargetRemovedException, self).__init__()
        self.message = 'Remote ui object "{}" has been removed from hierarchy during {}.'.format(objproxy, action)
