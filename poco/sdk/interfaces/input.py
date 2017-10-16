# coding=utf-8
__author__ = 'lxn3032'


class InputInterface(object):
    """
    This is one of the main communication interfaces. This interface ensure the ability of simulated input on target 
    device. There are only some simple and basic method defined as follows which is enough for simple features. To 
    fully support on mobile device, motion event will be introduced in the future.
    
    The coordinates are all in UniformCoordinate, see `UniformCoordinate` to get more details.
    """

    def click(self, x, y):
        """
        Perform click action as simulated input on target device.
        在目标设备上进行click操作

        :param y: y in range of 0~1 
        :param x: x in range of 0~1 
        :return: None
        """

        raise NotImplementedError

    def swipe(self, x1, y1, x2, y2, duration):
        """
        Perform swipe action as simulated input on target device from point A to B within given seconds.
        在目标设备上进行滑动操作

        :param x1, y1: 起始点，归一化坐标系
        :param x2, y2: 终止点，归一化坐标系
        :param duration: 整个滑动过程持续时间，单位秒
        :return: None 
        """

        raise NotImplementedError

    def longClick(self, x, y, duration):
        """
        Perform long click action as simulated input on target device within given seconds.
        在目标设备上长按

        :param x:  
        :param y: [x, y] in range of 0~1
        :param duration: 持续时间，单位秒
        :return: None
        """

        raise NotImplementedError

    def keyevent(self, keycode):
        """
        Send a key event to target device.
        模拟设备按键

        :param keycode: Ascii key code.
        :return: None.
        """

        raise NotImplementedError
