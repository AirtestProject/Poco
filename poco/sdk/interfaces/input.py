# coding=utf-8
__author__ = 'lxn3032'


class InputInterface(object):
    """
    This is one of the main communication interfaces. This interface ensure the ability of simulated input on target 
    device. There are only some simple and basic method defined as follows which is enough for simple features. To 
    fully support on mobile device, motion event will be introduced in the future.
    
    The coordinates are all in UniformCoordinate, see ``UniformCoordinate`` for more details.
    """

    def click(self, x, y):
        """
        Perform click action as simulated input on target device. Coordinates arguments are all in range of 0~1.

        Args:
            y (:obj:`float`): y
            x (:obj:`float`): x
        """

        raise NotImplementedError

    def swipe(self, x1, y1, x2, y2, duration):
        """
        Perform swipe action as simulated input on target device from point A to B within given seconds. Coordinates 
        arguments are all in range of 0~1.

        Args:
            x1 (:obj:`float`): start point x
            y1 (:obj:`float`): start point y
            x2 (:obj:`float`): end point x
            y2 (:obj:`float`): end point y
            duration (:obj:`float`): Time over the whole action.
        """

        raise NotImplementedError

    def longClick(self, x, y, duration):
        """
        Perform long click action as simulated input on target device within given seconds. Coordinates arguments are 
        all in range of 0~1.

        Args:
            y (:obj:`float`): y
            x (:obj:`float`): x
            duration (:obj:`float`): Time over the whole action.
        """

        raise NotImplementedError

    def keyevent(self, keycode):
        """
        Send a key event to target device.

        Args:
            keycode (:obj:`int` or :obj:`char`): Ascii key code.
        """

        raise NotImplementedError
