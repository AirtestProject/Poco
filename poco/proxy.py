# coding=utf-8
from __future__ import unicode_literals

import copy
import six
import time
from functools import wraps

from .exceptions import PocoTargetTimeout, InvalidOperationException, PocoNoSuchNodeException, PocoTargetRemovedException
from .sdk.exceptions import UnableToSetAttributeException
from .utils.query_util import query_expr, build_query

__author__ = 'lxn3032'
__all__ = ['UIObjectProxy']


def wait(func):
    @wraps(func)
    def wrapped(proxy, *args, **kwargs):
        try:
            return func(proxy, *args, **kwargs)
        except PocoNoSuchNodeException as e:
            try:
                proxy.wait_for_appearance(timeout=proxy.poco._pre_action_wait_for_appearance)
                return func(proxy, *args, **kwargs)
            except PocoTargetTimeout:
                raise e

    return wrapped


def refresh_when(err_type):
    def wrapper(func):
        @wraps(func)
        def wrapped(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except err_type:
                self._do_query(multiple=False, refresh=True)
                return func(self, *args, **kwargs)
        return wrapped
    return wrapper


class UIObjectProxy(object):
    def __init__(self, poco, name=None, **attrs):
        """
        UI proxy class implementation. This class instance is only a proxy that represents UI element on target device. 
        Any action performing on this instance is handled by poco. 
        It is unnecessary to initialize this object manually.
        See `QueryCondition` to get more details about how to select UI elements.

        :param poco: The poco instance.
        :param name: Query condition of attribute "name". This means you gonna select UI elements whose name is `name`.
        :param attrs: The other query conditions except `name`.
        """

        # query object in tuple
        self.query = build_query(name, **attrs)
        self.poco = poco

        # Whether multiple UI elements are selected. This will is only a result flag. It would not effect the selection
        # results. In order to make the selection faster, this flag is introduced.
        # 上一次选择是否是多选，如果不是多选但需要访问所有UI elements时会进行重新选择。
        self._query_multiple = False

        # Whether the corresponding UI elements of this UI proxy (self) has been selected.
        # 此UI proxy是否已经查找到对应的UI elements了
        self._evaluated = False

        # Proxy object of UI elements. May be proxy of `node` or proxy of `[node]`. `self._nodes_proxy_is_list` tells
        # the proxy type.
        # 可能是远程node代理，也可能是远程[node]代理, 由`self._nodes_proxy_is_list`指定是何种peoxy类型
        self._nodes = None
        self._nodes_proxy_is_list = True

        # Only use for caching some proxies of sorted node in `self.__getitem__`
        # 仅用于__getitem__时保存好已排序的child代理对象
        self._sorted_children = None

        # The focus point of this UI element. See `CoordinateSystem` to get more details.
        # 相对于包围盒的focus point定义，用于touch/swipe/drag操作的局部相对定位
        self._focus = None

    def child(self, name=None, **attrs):
        """
        Select straight child(ren) from this UI element(s) with given query conditions.
        See `QueryCondition` to get more details about selectors.

        以当前ui对象为基准，选择直系ui对象。可通过节点名和其余节点属性共同选择
        选择器规则同PocoUI.__call__

        :param name: Query condition of attribute "name". This means you gonna select UI elements whose name is `name`.
        :param attrs: The other query conditions except `name`.
        :return: A new UI proxy object represents the child(ren) of current UI elements.
        """

        sub_query = build_query(name, **attrs)
        query = ('/', (self.query, sub_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def children(self):
        """
        The same as `child` but select all children from this UI element(s).
        获取当前节点的所有孩子节点

        :return: A new UI proxy object.
        """

        return self.child()

    def offspring(self, name=None, **attrs):
        """
        Select any offsprings include straight child(ren) from this UI element(s) with given query conditions.
        See `QueryCondition` to get more details about selectors.

        以当前ui对象为基准，选择后代ui对象（所有后代）。可通过节点名和其余节点属性共同选择
        选择器规则同PocoUI.__call__

        :param name: <same as `.child()'>
        :param attrs: <same as `.child()'>
        :return: A new UI proxy object represents the offspring(s) of current UI elements.
        """

        sub_query = build_query(name, **attrs)
        query = ('>', (self.query, sub_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def sibling(self, name=None, **attrs):
        """
        Select sibling(s) from this UI element(s) with given query conditions.
        See `QueryCondition` to get more details about selectors.

        以当前ui对象为基准，选择兄弟ui对象。可通过节点名和其余节点属性共同选择
        选择器规则同PocoUI.__call__

        :param name: <same as `.child()'>
        :param attrs: <same as `.child()'>
        :return: A new UI proxy object represents the sibling(s) of current UI elements.
        """

        sub_query = build_query(name, **attrs)
        query = ('-', (self.query, sub_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def __getitem__(self, item):
        """
        Select specific UI element by index. If this UI proxy represents a set of UI elements, you could use this method
         to access specific UI element. The new UI element will be wrapped by UIObjectProxy instance. So the return
        value is also a UI proxy object.
        The order of UI elements are determined by its position on screen not the selection sequence. We call this rule 
        "L2R U2D" (left to right one by one, up to down line by line) which means the most top left UI element is always 
         the first one.
        See `IterationOverUI` to get more details.

        索引当前ui对象集合的第N个节点。在一个选择器的选择中可能会有多个满足条件的节点，例如物品栏的物品格子，使用数组索引可选出具体某一个。
        该函数默认按照空间排序（从左到右从上到下）后才进行选择

        WARNING: This method may cause performance issue depending on implementation of PocoAgent.
        警告：此方法有极大延迟，请勿频繁调用此方法。

        :param item: An integer of the index.
        :return: A new UI proxy object represents the nth of current UI elements.
        """

        if not self._query_multiple:
            nodes = self._do_query(multiple=True, refresh=True)
        else:
            nodes = self._nodes
        length = len(nodes)
        if not self._sorted_children:
            self._sorted_children = []
            for i in range(length):
                uiobj = UIObjectProxy(self.poco)
                uiobj.query = ('index', (self.query, i))
                uiobj._evaluated = True
                uiobj._query_multiple = True
                uiobj._nodes = nodes[i]
                uiobj._nodes_proxy_is_list = False
                pos = uiobj.get_position()
                self._sorted_children.append((uiobj, pos))
        self._sorted_children.sort(lambda a, b: cmp(list(reversed(a)), list(reversed(b))), key=lambda v: v[1])
        return self._sorted_children[item][0]

    def __len__(self):
        """
        Count how many UI elements selected.
        获取满足当前选择器的ui集合的节点个数

        :return: Number of selected UI elements.
        :raise PocoNoSuchNodeException: Raises when none of the UI element matches the query condition.
        """

        if not self._nodes_proxy_is_list:
            return 1

        # 获取长度时总是multiple的
        if not self._query_multiple:
            nodes = self._do_query(multiple=True, refresh=True)
        else:
            nodes = self._nodes
        return len(nodes)

    def __iter__(self):
        """
        Similar to `__getitem__` but this method helps to iterate over all UI elements.
        The order rules of UI elements is the same as `__getitem__`.
        See `IterationOverUI` to get more details.

        ui集合的节点迭代器，遍历所有满足选择条件的ui对象。
        遍历会默认按照从左到右从上到下的顺序，进行按顺序遍历。
        遍历过程中，还未遍历到的节点如果从画面中移除了则会抛出异常，已遍历的节点即使移除也不受影响。
        遍历顺序在遍历开始前已经确定，遍历过程中界面上的节点进行了重排则仍然按照之前的顺序进行遍历。

        :return: A generator yielding new UI proxy represents the specific UI element iterated over.

        :raise PocoTargetRemovedException: Raises when hierarchy structure changed and attempt to access to an 
            non-exists UI element over the iteration.
        """

        # 节点数量太多时，就不按照控件顺序排序了
        if not self._query_multiple:
            nodes = self._do_query(multiple=True, refresh=True)
        else:
            nodes = self._nodes
        length = len(nodes)
        sorted_nodes = []
        for i in range(length):
            uiobj = UIObjectProxy(self.poco)
            uiobj.query = ('index', (self.query, i))
            uiobj._evaluated = True
            uiobj._query_multiple = True
            uiobj._nodes = nodes[i]
            uiobj._nodes_proxy_is_list = False
            pos = uiobj.get_position()
            sorted_nodes.append((uiobj, pos))
        sorted_nodes.sort(lambda a, b: cmp(list(reversed(a)), list(reversed(b))), key=lambda v: v[1])

        for obj, _ in sorted_nodes:
            yield obj

    @wait
    def click(self, focus=None, sleep_interval=None):
        """
        Perform a click action on the UI element this UI proxy represents. If this UI proxy represent a set of UI 
        elements, click the first one. Will click the anchor point of the UI element by default. It is able to click
        another point offset by the UI element by providing argument `focus`.
        See `CoordinateSystem` to get more details.
        点击当前ui对象，如果是ui对象集合则默认点击第一个

        :param focus: An offset point by the top left corner of the UI elements as 2-list/2-tuple (x, y) whose component 
             in range of 0~1. This argument can also be 'anchor' or 'center'. 'Center' means to click the center of 
             bounding box of UI element. 
        :param sleep_interval: Seconds to wait after this action. If not provides, it will wait by default. The default 
            value can be configured by poco initialization. See `PocoConfiguration`.
        :return: None

        :raise PocoNoSuchNodeException: Raises when the UI element does not exists.
        """

        focus = focus or self._focus or 'anchor'
        pos_in_percentage = self.get_position(focus)
        self.poco.pre_action('click', self, pos_in_percentage)
        self.poco.click(pos_in_percentage)
        if sleep_interval:
            time.sleep(sleep_interval)
        else:
            self.poco.wait_stable()
        self.poco.post_action('click', self, pos_in_percentage)

    @wait
    def swipe(self, dir, focus=None, duration=0.5):
        """
        Perform a swipe action by given direction from this UI element. Notices and limitations see `.click()`. 
        以当前对象的anchor为起点，swipe一段距离

        :param dir: 2-list/2-tuple (x, y) coordinate in UniformCoordinate. Can also be one of 'up', 'down', 'left',
            'right', 'up' equivalent to [0, -0.1], 'down' equivalent to [0, 0.1], 'left' equivalent to [-0.1, 0],
            'right' equivalent to [0, 0.1]
        :param focus: see `.click()`
        :param duration: The time over the whole action.
        :return: None

        :raise PocoNoSuchNodeException:
        """

        focus = focus or self._focus or 'anchor'
        dir_vec = self._direction_vector_of(dir)
        origin = self.get_position(focus)
        self.poco.pre_action('swipe', self, (origin, dir_vec))
        self.poco.swipe(origin, direction=dir_vec, duration=duration)
        self.poco.post_action('swipe', self, (origin, dir_vec))

    def drag_to(self, target, duration=2):
        """
        Similar to swipe, but the end point is provide by a UI proxy or a fixed coordinate.
        以当前对象节点anchor为起点，拖动到目标对象节点anchor

        :param target: A UI proxy or 2-list/2-tuple (x, y) coordinate in UniformCoordinate.
        :param duration: The time over the whole action.
        :return: None

        :raise PocoNoSuchNodeException:
        """

        if type(target) in (list, tuple):
            target_pos = target
        else:
            target_pos = target.get_position()
        origin_pos = self.get_position()
        dir = [target_pos[0] - origin_pos[0], target_pos[1] - origin_pos[1]]
        self.swipe(dir, duration=duration)

    def focus(self, f):
        """
        Get a new UI proxy copy from this with given focus. As UI proxy is immutable, a new UI proxy is always returned.
        设置对象的操作定位点，相对于对象包围盒。Immutable操作，返回一个新的对象代理，原对象不受影响

        :param f: The focus point. Can be 2-list/2-tuple (x, y) coordinate in UniformCoordinate, 'center' or 'anchor'.
        :return: A new UI proxy copy.
        """

        ret = copy.copy(self)
        ret._focus = f
        return ret

    def get_position(self, focus=None):
        """
        Get the position of this UI elements.

        :param focus: 
        :return: 2-list/2-tuple (x, y) coordinate in UniformCoordinate.
        """

        focus = focus or self._focus or 'anchor'
        if focus == 'anchor':
            pos = self.attr('pos')
        elif focus == 'center':
            x, y = self.attr('pos')
            w, h = self.get_size()
            ap_x, ap_y = self.attr("anchorPoint")
            fx, fy = 0.5, 0.5
            pos = [x + w * (fx - ap_x), y + h * (fy - ap_y)]
        elif type(focus) in (list, tuple):
            x, y = self.attr('pos')
            w, h = self.get_size()
            ap_x, ap_y = self.attr("anchorPoint")
            fx, fy = focus
            pos = [x + w * (fx - ap_x), y + h * (fy - ap_y)]
        else:
            raise TypeError('Unsupported focus type {}. '
                            'Only "anchor/center" or 2-list/2-tuple available.'.format(type(focus)))
        return pos

    def _direction_vector_of(self, dir):
        if dir == 'up':
            dir_vec = [0, -0.1]
        elif dir == 'down':
            dir_vec = [0, 0.1]
        elif dir == 'left':
            dir_vec = [-0.1, 0]
        elif dir == 'right':
            dir_vec = [0.1, 0]
        elif type(dir) in (list, tuple):
            dir_vec = dir
        else:
            raise TypeError('Unsupported direction type {}. '
                            'Only "up/down/left/right" or 2-list/2-tuple available.'.format(type(dir)))
        return dir_vec

    def wait(self, timeout=3):
        """
        Block and wait at most given time before this UI element appears.
        等待当前ui对象出现，总是返回自身，如果目标出现即时返回，否则超时后返回

        :param timeout: Maximum waiting time in seconds.
        :return: self
        """

        start = time.time()
        while not self.exists():
            self.poco.sleep_for_polling_interval()
            if time.time() - start > timeout:
                break
        return self

    def wait_for_appearance(self, timeout=120):
        """
        Block and wait until this UI element appears within given timeout. Once timeout, `PocoTargetTimeout` will raise.
        等待当前ui对象出现

        :param timeout: Maximum waiting time in seconds.
        :return: None

        :raise PocoTargetTimeout: Raises if timeout.
        """

        start = time.time()
        while not self.exists():
            self.poco.sleep_for_polling_interval()
            if time.time() - start > timeout:
                raise PocoTargetTimeout('appearance', self)

    def wait_for_disappearance(self, timeout=120):
        """
        Block and wait until this UI element disappears within given timeout. Once timeout, `PocoTargetTimeout` will 
        raise.
        等待当前ui对象消失

        :param timeout: Maximum waiting time in seconds.
        :return: None

        :raise PocoTargetTimeout: Raises if timeout.
        """

        start = time.time()
        while self.exists():
            self.poco.sleep_for_polling_interval()
            if time.time() - start > timeout:
                raise PocoTargetTimeout('disappearance', self)

    @refresh_when(PocoTargetRemovedException)
    def attr(self, name):
        """
        Retrieve attribute of UI element by attribute name.
        If attribute value is a string, it will be encode to utf-8 as <type str> in PY2.  

        获取当前ui对象属性，如果为ui集合时，默认只取第一个ui对象的属性。
        坐标、向量、尺寸均为屏幕坐标系的下的值，并非归一化值，字符串均为utf-8编码

        :param name: Attribute name, can be one of the following. 属性名，只可能是下列之一
            visible: <bool> Whether or not it is visible to user. 是否可见
            text: <str(utf-8)/NoneType> String value of the UI element. 节点文本值
            type: <str> The type name of UI element from remote runtime. 节点类型
            pos: <list[2]> The position of the UI element. 节点包围盒中心点在屏幕上的坐标
            size: <list[2]> The percentage size [width, height] in range of 0~1 according to the screen.
            name: <str> The name of UI element. 节点名称
        :return: None if no such attribute or it value is None/null/nil/etc. Otherwise its value will return.
            The value type should be json serializable.
            以上属性值为空时返回None，否则返回对应属性值

        :raise PocoNoSuchNodeException: Raises when the UI element does not exists.

        :note: 自动捕获NodeHasBeenRemovedException
               远程节点对象可能已经从渲染树中移除，这样需要重新选择这个节点了
        """

        # to optimize speed, retrieve only the first matched element.
        # 优化速度，只选择第一个匹配到的节点
        nodes = self._do_query(multiple=False)
        val = self.poco.agent.hierarchy.getAttr(nodes, name)
        if six.PY2 and isinstance(val, unicode):
            val = val.encode('utf-8')
        return val

    @refresh_when(PocoTargetRemovedException)
    def setattr(self, name, val):
        nodes = self._do_query(multiple=False)
        try:
            self.poco.agent.hierarchy.setAttr(nodes, name, val)
        except UnableToSetAttributeException as e:
            raise InvalidOperationException('"{}" of "{}"'.format(e.message, self))

    def exists(self):
        """
        判断节点是否存在visible节点树中。只要在节点树中的可见节点均为exists，包括屏幕外的和被遮挡的

        :return: 节点是否存在， True/False
        """

        try:
            return self.attr('visible')
        except (PocoTargetRemovedException, PocoNoSuchNodeException):
            return False

    def get_text(self):
        """
        获取节点上的文本值，utf-8编码

        :return: 节点上的文本值，以utf-8编码
        """

        text = self.attr('text')
        if six.PY2 and type(text) is unicode:
            text = text.encode('utf-8')
        return text

    def set_text(self, text):
        """
        给TextField节点设置text值

        :param text: 要设置的text值
        :return: None

        :raise InvalidOperationException: 在一个不可设置文本值的节点上设置节点时会抛出该异常
        """

        self.setattr('text', text)

    def get_name(self):
        """
        获取节点名

        :return: 节点名
        """

        return self.attr('name')

    def get_size(self):
        """
        获取节点在屏幕上的归一化尺寸

        :return: 格式为[width, height]的list, width,height ∈ [0, 1]
        """

        return self.attr('size')

    def get_bounds(self):
        size = self.get_size()
        top_left = self.get_position([0, 0])

        # t, r, b, l
        bounds = [top_left[1], top_left[0] + size[0], top_left[1] + size[1], top_left[0]]
        return bounds

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return 'UIObjectProxy of "{}"'.format(query_expr(self.query))

    __repr__ = __str__

    @property
    def nodes(self):
        """
        访问所选择对象的远程节点对象

        :return: RpcRemoteObjectProxy. Rpc远程对象代理
        """
        return self._do_query()

    def invalidate(self):
        self._evaluated = False
        self._nodes = None

    def _do_query(self, multiple=True, refresh=False):
        if not self._evaluated or refresh:
            self._nodes = self.poco.agent.hierarchy.select(self.query, multiple)
            if len(self._nodes) == 0:
                raise PocoNoSuchNodeException(self)
            self._evaluated = True
            self._query_multiple = multiple
        return self._nodes
