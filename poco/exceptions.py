# coding=utf-8
from __future__ import unicode_literals

import six


__author__ = 'lxn3032'


class PocoException(Exception):
    """
    Base class for errors and exceptions of Poco. It is Python3 compatible.
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


class InvalidOperationException(PocoException):
    """
    Raised when the operation performing on target device is foreseen, e.g. instruction to click outside the screen is
    definitely meaningless, then the ``InvalidOperationException`` is raised.
    """

    pass


class PocoTargetTimeout(PocoException):
    """
    Raised when the timeout expired while waiting for some condition to be fulfilled, e.g. waiting for the specific
    UI element but it has not appeared on the screen.
    """

    def __init__(self, action, poco_obj_proxy):
        super(PocoTargetTimeout, self).__init__()
        self.message = 'Waiting timeout for {} of "{}"'.format(action, poco_obj_proxy)


class PocoNoSuchNodeException(PocoException):
    """
    Raised when the UI element specified by query expression cannot be found.
    """

    def __init__(self, objproxy):
        super(PocoNoSuchNodeException, self).__init__()
        self.message = 'Cannot find any visible node by query {}'.format(objproxy)


class PocoTargetRemovedException(PocoException):
    """
    Raised when the hierarchy structure changed over the selection or when accessing the UI element that is already
    recycled.

    In most cases, there is no need to handle this exception manually. If this exception occurs, it usually means it
    is a bug in your code rather than application itself. Check your code first. The most of misuses comes from as
    follows.
    
    Examples:
        ::

            button1 = poco('button1')
            time.sleep(10)   # waiting for long enough before the UI hierarchy changing
            button1.click()  # PocoTargetRemovedException will raise at this line. Because the 'button1' is not on the screen.
    """

    def __init__(self, action, objproxy):
        super(PocoTargetRemovedException, self).__init__()
        self.message = 'Remote ui object "{}" has been removed from hierarchy during {}.'.format(objproxy, action)
