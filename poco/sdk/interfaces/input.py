# coding=utf-8
__author__ = 'lxn3032'


class InputInterface(object):
    """
    This is one of the main communication interfaces. This interface ensures the ability for simulated input on target
    device. So far, the interface supports only some basic methods definitions. The motion event will be added in future
    to provide full support for mobile devices.
    
    All coordinates are in NormalizedCoordinate system, see ``NormalizedCoordinate`` for more details.
    """

    def click(self, x, y):
        """
        Perform click action as simulated input on target device. Coordinates arguments are all in range of 0~1.

        Args:
            y (:obj:`float`): y-coordinate
            x (:obj:`float`): x-coordinate
        """

        raise NotImplementedError

    def swipe(self, x1, y1, x2, y2, duration):
        """
        Perform swipe action as simulated input on target device from point A to B within given time interval to
        perform the action. Coordinates  arguments are all in range of 0~1.

        Args:
            x1 (:obj:`float`): x-coordinate of the start point
            y1 (:obj:`float`): y-coordinate of the start point
            x2 (:obj:`float`): x-coordinate of the end point
            y2 (:obj:`float`): y-coordinate of the end point
            duration (:obj:`float`): time interval to perform the swipe action
        """

        raise NotImplementedError

    def longClick(self, x, y, duration):
        """
        Perform press action as simulated input on target device within given seconds. Coordinates arguments are
        all in range of 0~1.

        Args:
            x (:obj:`float`): x-coordinate
            y (:obj:`float`): y-coordinate
            duration (:obj:`float`): time interval to perform the action
        """

        raise NotImplementedError

    def keyevent(self, keycode):
        """
        Send a key event to target device.

        Args:
            keycode (:obj:`int` or :obj:`char`): Ascii key code
        """

        raise NotImplementedError
