# coding=utf-8
__author__ = 'lxn3032'


import copy
import time

from hunter_cli.rpc.exceptions import HunterRpcRemoteException, HunterRpcTimeoutException
from .utils.retry import retries_when


QueryAttributeNames = (
    'type', 'text', 'enable', 'visable', 'touchenable',
    'textNot', 'typeNot',
)


def build_query(name, **attrs):
    for attr_name in attrs.keys():
        if attr_name not in QueryAttributeNames:
            raise Exception('Unsupported Attribute name for query  !!!')
    query = []
    if name is not None:
        attrs['name'] = name
    for attr_name, attr_val in attrs.items():
        if attr_name in ('textNot', 'typeNot'):
            attr_name = attr_name[:-3]
            op = 'attr!='
        else:
            op = 'attr='
        query.append((op, (attr_name, attr_val)))
    return 'and', tuple(query)


class UIObjectProxy(object):
    def __init__(self, poco, name=None, **attrs):
        self.query = build_query(name, **attrs)
        self.poco = poco
        self._negtive = False

    def child(self, name=None, **attrs):
        """
        以当前ui对象为基准，选择直系ui对象。可通过节点名和其余节点属性共同选择
        选择器规则同PocoUI.__call__

        :param name:
        :param attrs:
        :return: ui对象

        :raises:
            HunterRpcRemoteException.NoSuchTargetException
            HunterRpcRemoteException.NoSuchAttributeException
        """
        sub_query = build_query(name, **attrs)
        query = ('/', (self.query, sub_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def offspring(self, name=None, **attrs):
        """
        以当前ui对象为基准，选择后代ui对象（所有后代）。可通过节点名和其余节点属性共同选择
        选择器规则同PocoUI.__call__

        :param name:
        :param attrs:
        :return: ui对象

        :raises:
            HunterRpcRemoteException.NoSuchTargetException
            HunterRpcRemoteException.NoSuchAttributeException
        """
        sub_query = build_query(name, **attrs)
        query = ('>', (self.query, sub_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def sibling(self, name=None, **attrs):
        """
        以当前ui对象为基准，选择兄弟ui对象。可通过节点名和其余节点属性共同选择
        选择器规则同PocoUI.__call__

        :param name:
        :param attrs:
        :return: ui对象

        :raises:
            HunterRpcRemoteException.NoSuchTargetException
            HunterRpcRemoteException.NoSuchAttributeException
        """
        sub_query = build_query(name, **attrs)
        query = ('-', (self.query, sub_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def __getitem__(self, item):
        """
        索引当前ui对象集合的第N个节点。在一个选择器的选择中可能会有多个满足条件的节点，例如物品栏的物品格子，使用数组索引可选出具体某一个

        :param item: <int> 数组索引
        :return: ui对象

        :raise: HunterRpcRemoteException.NoSuchTargetException
        """
        obj = UIObjectProxy(self.poco)
        obj.query = ('index', (self.query, item))
        return obj

    def __len__(self):
        """
        获取满足当前选择器的ui集合的节点个数

        :return: 当前ui集合的节点个数
        """
        return self.attr('length')

    def __neg__(self):
        ret = UIObjectProxy(self.poco)
        ret.query = self.query
        ret._negtive = True
        return ret

    def __iter__(self):
        """
        ui集合的节点迭代器，遍历所有节点对象

        :yield: 具体ui框架的节点对象代理(hunter_cli.rpc.proxy.RpcObjectProxy)
        :return:
        """
        nodes = self.poco.selector.select(self.query)
        for n in nodes:
            yield n

    @retries_when(HunterRpcTimeoutException)
    def click(self, click_anchor=True, sleep_interval=None):
        """
        点击当前ui对象，如果是ui对象集合则默认点击第一个

        :param click_anchor: True则点击对象的anchor，否则点击对象包围盒的中心。默认为True。
        :param sleep_interval: 点击后的静候时间，默认为poco的操作间隔
        :return: None
        """
        pos = self.attr('anchorPosition') if click_anchor else self.attr('screenPosition')
        self.poco.touch(pos)
        if sleep_interval:
            time.sleep(sleep_interval)
        else:
            self.poco.wait_stable()

    def swipe(self, dir, distance_percent=0.1, duration=0.5):
        """
        以当前对象的anchor为起点，swipe一段距离

        :param dir: 滑动方向，坐标系与屏幕坐标系相同。
        :param distance_percent: 滑动距离百分比，以屏幕宽为1
        :param duration: 滑动持续时间
        :return: None
        """
        origin_pos = self.attr('anchorPosition')
        if dir == 'up':
            dir_vec = [0, -1 * distance_percent]
        elif dir == 'down':
            dir_vec = [0, distance_percent]
        elif dir == 'left':
            dir_vec = [-1 * distance_percent, 0]
        elif dir == 'right':
            dir_vec = [distance_percent, 0]
        elif type(dir) in (list, tuple):
            dir_vec = [dir[0] * distance_percent, dir[1] * distance_percent]
        else:
            raise TypeError('Unsupported direction type {}. '
                            'Only "up/down/left/right" or 2 elements list/tuple available.'.format(type(dir)))
        self.poco.swipe(origin_pos, direction=dir_vec, duration=duration)

    def wait_for_appearance(self, timeout=120):
        """
        等待当前ui对象出现

        :param timeout: 最长等待时间
        :return: None

        :raise RuntimeError: 当超时时抛出该异常
        """
        start = time.time()
        while not self.exists():
            self.poco.sleep_for_polling_interval()
            if time.time() - start > timeout:
                raise RuntimeError('Timeout at waiting for {} to appear'.format(repr(self.query)))

    def wait_for_disappearance(self, timeout=120):
        """
        等待当前ui对象消失

        :param timeout: 最长等待时间
        :return: None

        :raise RuntimeError: 当超时时抛出该异常
        """
        start = time.time()
        while self.exists():
            self.poco.sleep_for_polling_interval()
            if time.time() - start > timeout:
                raise RuntimeError('Timeout at waiting for {} to disappear'.format(repr(self.query)))

    @retries_when(HunterRpcTimeoutException)
    def attr(self, name):
        """
        获取当前ui对象属性，如果为ui集合时，默认只取第一个ui对象的属性。
        坐标、向量、尺寸均为屏幕坐标系的下的值，字符串均为utf-8编码

        :param name: 属性名，只可能是下列之一
            visible: <bool>是否可见
            text: <str(utf-8)/NoneType> 节点文本值
            type: <str> 节点类型
            enable: <bool> 节点正常可用，通常是对于可操作的控件类
            touchenable: <bool> 是否可点击，目前没什么用
            screenPosition: <list[2]> 节点包围盒中心点在屏幕上的坐标
            anchorPosition: <list[2]> 节点anchor点在屏幕上的坐标
            size: <list[2]> 节点换算到屏幕上的尺寸，[width, height]
            name: <str> 节点名称
            direction_vector: <list[2]> 节点极轴在在屏幕坐标上的向量，单位向量
        :return: 以上属性值为空时返回None，否则返回对应属性值

        :raise HunterRpcRemoteException.NoSuchAttributeException: 当查询不是以上的属性名时抛出该异常
        """
        val = self.poco.selector.selectAndGetAttribute(self.query, name)
        if self._negtive:
            if type(val) is bool:
                return not val
            elif type(val) in (float, int, long):
                return -val
        return val

    def exists(self):
        """
        判断节点是否存在visible节点树中。只要在节点树中的可见节点均为exists，包括屏幕外的和被遮挡的

        :return: 节点是否存在， True/False
        """
        try:
            return self.attr('visible')
        except HunterRpcRemoteException:
            return False

    def visible(self):
        """
        判断节点是否可见。TODO：功能还没确定，不要用这个方法

        :return: True/False
        """
        return self.attr('visible')

    def enabled(self):
        """
        判断节点是否使能、可用

        :return: True/False
        """
        return self.attr('enable')

    def touchable(self):
        """
        判断节点是否可点击，不是所有类型节点都有这个属性

        :return: True/False

        :raise HunterRpcRemoteException.NoSuchAttributeException: 当查询不是以上的属性名时抛出该异常
        """
        return self.attr('touchenable')

    def get_text(self):
        """
        获取节点上的文本值，utf-8编码

        :return: 节点上的文本值，以utf-8编码
        """
        text = self.attr('text')
        if type(text) is unicode:
            text = text.encode('utf-8')
        return text

    def get_name(self):
        """
        获取节点名

        :return: 节点名
        """
        return self.attr('name')

    def get_size(self):
        """
        获取节点在屏幕上的尺寸

        :return: 格式为[width, height]的list
        """
        return self.attr('size')

    def __str__(self):
        return 'UIObjectProxy of "{}"'.format(self.query)
    __repr__ = __str__

    @property
    def nodes(self):
        return self.poco.selector.select(self.query)
