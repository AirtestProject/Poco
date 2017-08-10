# coding=utf-8
__author__ = 'lxn3032'


class InputerInterface(object):
    def click(self, pos):
        """
        在目标设备上进行click操作

        :param pos: [x, y] in target device dimension 
        :return: None
        """

        raise NotImplementedError

    def swipe(self, p1, p2=None, direction=None, duration=1):
        """
        在目标设备上进行滑动操作

        :param p1: [x, y] 起始点，设备输入坐标系
        :param p2: 终止点，设备输入坐标系
        :param direction: 以起始点为原点的向量，归一化坐标系
        :param duration: 整个滑动过程持续时间，单位秒
        :return: None 
        """

        raise NotImplementedError

    def long_click(self, pos, duration=2):
        """
        在目标设备上长按

        :param pos:  [x, y] in target device dimension 
        :param duration: 持续时间，单位秒
        :return: None
        """

        raise NotImplementedError
