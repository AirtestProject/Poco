# coding=utf-8
__author__ = 'lxn3032'


class InputInterface(object):
    def click(self, x, y):
        """
        在目标设备上进行click操作

        :param y: y in range of 0~1 
        :param x: x in range of 0~1 
        :return: None
        """

        raise NotImplementedError

    def swipe(self, x1, y1, x2, y2, duration):
        """
        在目标设备上进行滑动操作

        :param x1, y1: 起始点，归一化坐标系
        :param x2, y2: 终止点，归一化坐标系
        :param duration: 整个滑动过程持续时间，单位秒
        :return: None 
        """

        raise NotImplementedError

    def longClick(self, x, y, duration):
        """
        在目标设备上长按

        :param x:  
        :param y: [x, y] in range of 0~1
        :param duration: 持续时间，单位秒
        :return: None
        """

        raise NotImplementedError

    def keyevent(self, keycode):
        """
        模拟设备按键

        :param keycode: 
        :return: 
        """

        raise NotImplementedError
