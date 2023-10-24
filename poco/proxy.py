# coding=utf-8
from __future__ import unicode_literals, division

import math
import copy
import poco.utils.six as six
import time
from functools import wraps

from poco.gesture import PendingGestureAction
from poco.exceptions import PocoTargetTimeout, InvalidOperationException, PocoNoSuchNodeException, PocoTargetRemovedException
from poco.sdk.exceptions import UnableToSetAttributeException
from poco.utils.query_util import query_expr, build_query
from poco.utils.multitouch_gesture import make_pinching

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


class ReevaluationContext(object):
    """
    volatile attributes的重运算同一批次内只执行一次，无需多次执行
    """

    def __init__(self, proxy):
        self.target = proxy
        self.with_this_batch = hasattr(self.target, '__reevaluation_context__')

    def __enter__(self):
        if not self.with_this_batch:
            setattr(self.target, '__reevaluation_context__', True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.with_this_batch:
            delattr(self.target, '__reevaluation_context__')


def volatile_attribute(func):
    @wraps(func)
    def wrapped(proxy, *args, **kwargs):
        with ReevaluationContext(proxy) as rc:
            if not rc.with_this_batch and proxy.poco._reevaluate_volatile_attributes:
                proxy._evaluated = False
            return func(proxy, *args, **kwargs)

    return wrapped


class UIObjectProxy(object):
    """
    UI Proxy class that represents the UI element on target device.

    Any action performing on this instance is handled by Poco. It is not necessary to initialize this object manually.
    See ``QueryCondition`` for more details about how to select the UI elements.

    Args:
        poco: the poco instance
        name: query condition of "name" attribute, i.e. the UI element(s) with ``name`` name will be selected
        attrs: other query expressions except for the ``name``

    See Also:
        :py:meth:`select UI element(s) by poco <poco.pocofw.Poco.__call__>`
    """

    def __init__(self, poco, name=None, **attrs):
        # query object in tuple
        self.query = build_query(name, **attrs)
        self.poco = poco

        # this flag is introduced to improve the performance, it is set if multiple UI elements are selected and
        # it does not affect the selection result
        # 上一次选择是否是多选，如果不是多选但需要访问所有UI elements时会进行重新选择。
        self._query_multiple = False

        # true or false whether the corresponding UI elements of this UI proxy (self) have been selected
        # 此UI proxy是否已经查找到对应的UI elements了
        self._evaluated = False

        # the proxy object of UI elements, migh be `node` or `[nodes]`, the proxy type is specified by
        # `self._nodes_proxy_is_list`
        # 可能是远程node代理，也可能是远程[node]代理, 由`self._nodes_proxy_is_list`指定是何种proxy类型
        self._nodes = None
        self._nodes_proxy_is_list = True

        # use only for caching some proxies of sorted nodes in `self.__getitem__`
        # 仅用于__getitem__时保存好已排序的child代理对象
        self._sorted_children = None

        # focus point of the UI element, see `CoordinateSystem` for more details
        # 相对于包围盒的focus point定义，用于touch/swipe/drag操作的局部相对定位
        self._focus = None

    def child(self, name=None, **attrs):
        """
        Select the direct child(ren) from the UI element(s) given by the query expression, see ``QueryCondition`` for
        more details about the selectors.

        Args:
            name: query expression of attribute "name", i.e. the UI elements with ``name`` name will be selected
            attrs: other query expression except for the ``name``

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: a new UI proxy object representing the child(ren) of
            current UI element(s)
        """

        sub_query = build_query(name, **attrs)
        query = ('/', (self.query, sub_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def children(self):
        """
        The same as :py:meth:`.child() <poco.proxy.UIObjectProxy.child>` but it selects all children from the UI
        element(s).

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: a new UI proxy object
        """

        return self.child()

    def offspring(self, name=None, **attrs):
        """
        Select the offsprings including the direct child(ren) from the UI element(s) given by the query expression,
        see ``QueryCondition`` for more details about selectors.

        Args:
            name: query expression of attribute "name", i.e. the UI elements with ``name`` name will be selected
            attrs: other query expression except for the ``name``

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: a new UI proxy object representing the child(ren) of
            current UI element(s)
        """

        sub_query = build_query(name, **attrs)
        query = ('>', (self.query, sub_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def sibling(self, name=None, **attrs):
        """
        Select the sibling(s) from the UI element(s) given by the query expression, see ``QueryCondition`` for more
        details about the selectors.

        Args:
            name: query expression of attribute "name", i.e. the UI elements with ``name`` name will be selected
            attrs: other query expression except for the ``name``

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: a new UI proxy object representing the child(ren) of
            current UI element(s)
        """

        sub_query = build_query(name, **attrs)
        query = ('-', (self.query, sub_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def parent(self):
        """
        Select the direct parent from the UI element(s) given by the query expression, see ``QueryCondition`` for
        more details about the selectors.

        Warnings:
            Experimental method, may not be available for all drivers.

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: a new UI proxy object representing the direct parent
            of the first UI element.
        """

        sub_query = build_query(None)  # as placeholder
        query = ('^', (self.query, sub_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def __getitem__(self, item):
        """
        Select the specific UI element by index. If this UI proxy represents a set of UI elements, then use this method
        to access the specific UI element. The new UI element will be wrapped by UIObjectProxy instance and therefore
        the returned value is also the UI proxy object.

        The order of UI elements are determined by their position on the screen and not by the selection sequence. This
        rule is called  "L2R U2D" (one by one from left to right, line by line from up to down), i.e. the most top left
        UI element is always the first one. See ``IterationOverUI`` for more details.

        Warnings:
            This method may cause some performance issues depending on implementation of PocoAgent.

        Args:
            item (:obj:`int`): the index.

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: a new UI proxy object representing the n-th of the
            current UI elements.
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

        self._sorted_children.sort(key=lambda v: (v[1][1], v[1][0]))
        return self._sorted_children[item][0]

    def __len__(self):
        """
        Return the number of selected UI elements.

        Returns:
            :obj:`int`: returns 0 if none of the UI element matches the query expression otherwise returns the number
            of selected UI elements
        """

        if not self._nodes_proxy_is_list:
            return 1

        # 获取长度时总是multiple的
        if not self._query_multiple:
            try:
                nodes = self._do_query(multiple=True, refresh=True)
            except PocoNoSuchNodeException:
                nodes = []
        else:
            nodes = self._nodes
        return len(nodes) if nodes else 0

    def __iter__(self):
        """
        Similar method to :py:meth:`.__getitem__() <poco.proxy.UIObjectProxy.__getitem__>` with the difference that this
        method iterates over all UI elements. The order rules of UI elements is same as for :py:meth:`.__getitem__()
        <poco.proxy.UIObjectProxy.__getitem__>`. See ``IterationOverUI`` for more details.

        Yields:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: a generator yielding new UI proxy represents the
            specific UI element iterated over

        Raises:
            PocoTargetRemovedException: when hierarchy structure has changed and it is attempted to access to the
             nonexistent UI element over the iteration
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
        sorted_nodes.sort(key=lambda v: (v[1][1], v[1][0]))

        for obj, _ in sorted_nodes:
            yield obj

    @wait
    def click(self, focus=None, sleep_interval=None):
        """
        Perform the click action on the UI element(s) represented by the UI proxy. If this UI proxy represents a set of
        UI elements, the first one in the set is clicked and the anchor point of the UI element is used as the default
        one. It is also possible to click another point offset by providing ``focus`` argument.

        See ``CoordinateSystem`` for more details.

        Args:
            focus (2-:obj:`tuple`/2-:obj:`list`/:obj:`str`): an offset point (x, y) from the top left corner of the UI
             element(s), values must be in range of 0~1. This argument can be also specified by 'anchor' or 'center'.
             'Center' means to click the center of bounding box of UI element. 
            sleep_interval: number of seconds to wait after this action. Default is None which is the default sleep
             interval. This value can be configured by Poco initialization. See configuration at poco
             :py:class:`initialization <poco.pocofw.Poco>` for more details.

        Raises:
            PocoNoSuchNodeException: raised when the UI element does not exist
        """

        focus = focus or self._focus or 'center'
        pos_in_percentage = self.get_position(focus)
        self.poco.pre_action('click', self, pos_in_percentage)
        ret = self.poco.click(pos_in_percentage)
        if sleep_interval:
            time.sleep(sleep_interval)
        else:
            self.poco.wait_stable()
        self.poco.post_action('click', self, pos_in_percentage)
        return ret

    @wait
    def rclick(self, focus=None, sleep_interval=None):
        """
        Perform the right click action on the UI element(s) represented by the UI proxy. If this UI proxy represents a set of
        UI elements, the first one in the set is clicked and the anchor point of the UI element is used as the default
        one. It is also possible to click another point offset by providing ``focus`` argument.

        See ``CoordinateSystem`` for more details.

        Args:
            focus (2-:obj:`tuple`/2-:obj:`list`/:obj:`str`): an offset point (x, y) from the top left corner of the UI
             element(s), values must be in range of 0~1. This argument can be also specified by 'anchor' or 'center'.
             'Center' means to click the center of bounding box of UI element. 
            sleep_interval: number of seconds to wait after this action. Default is None which is the default sleep
             interval. This value can be configured by Poco initialization. See configuration at poco
             :py:class:`initialization <poco.pocofw.Poco>` for more details.

        Raises:
            PocoNoSuchNodeException: raised when the UI element does not exist
        """

        focus = focus or self._focus or 'center'
        pos_in_percentage = self.get_position(focus)
        self.poco.pre_action('rclick', self, pos_in_percentage)
        ret = self.poco.rclick(pos_in_percentage)
        if sleep_interval:
            time.sleep(sleep_interval)
        else:
            self.poco.wait_stable()
        self.poco.post_action('rclick', self, pos_in_percentage)
        return ret

    @wait
    def double_click(self, focus=None, sleep_interval=None):
        """
        Perform the double click action on the UI element(s) represented by the UI proxy. If this UI proxy represents a set of
        UI elements, the first one in the set is clicked and the anchor point of the UI element is used as the default
        one. It is also possible to click another point offset by providing ``focus`` argument.

        See ``CoordinateSystem`` for more details.

        Args:
            focus (2-:obj:`tuple`/2-:obj:`list`/:obj:`str`): an offset point (x, y) from the top left corner of the UI
             element(s), values must be in range of 0~1. This argument can be also specified by 'anchor' or 'center'.
             'Center' means to double click the center of bounding box of UI element. 
            sleep_interval: number of seconds to wait after this action. Default is None which is the default sleep
             interval. This value can be configured by Poco initialization. See configuration at poco
             :py:class:`initialization <poco.pocofw.Poco>` for more details.

        Raises:
            PocoNoSuchNodeException: raised when the UI element does not exist
        """

        focus = focus or self._focus or 'center'
        pos_in_percentage = self.get_position(focus)
        self.poco.pre_action('double_click', self, pos_in_percentage)
        ret = self.poco.double_click(pos_in_percentage)
        if sleep_interval:
            time.sleep(sleep_interval)
        else:
            self.poco.wait_stable()
        self.poco.post_action('double_click', self, pos_in_percentage)
        return ret

    @wait
    def long_click(self, duration=2.0):
        """
        Perform the long click action on the UI element(s) represented by the UI proxy. If this UI proxy represents a 
        set of UI elements, the first one in the set is clicked and the anchor point of the UI element is used as the 
        default one. Similar to click but press the screen for the given time interval and then release.
    
        Args:
            duration (:py:obj:`float`): whole action duration.
        
        Return:
            the same as :py:meth:`poco.pocofw.Poco.long_click`, depending on poco agent implementation.
        """

        try:
            duration = float(duration)
        except ValueError:
            raise ValueError('Argument `duration` should be <float>. Got {}'.format(repr(duration)))

        pos_in_percentage = self.get_position(self._focus or 'center')
        self.poco.pre_action('long_click', self, pos_in_percentage)
        ret = self.poco.long_click(pos_in_percentage, duration)
        self.poco.post_action('long_click', self, pos_in_percentage)
        return ret

    @wait
    def swipe(self, direction, focus=None, duration=0.5):
        """
        Perform a swipe action given by the direction from this UI element. For notices and limitations see
        :py:meth:`.click() <poco.proxy.UIObjectProxy.click>`. 

        Args:
            direction (2-:obj:`tuple`/2-:obj:`list`/:obj:`str`):  coordinates (x, y) in NormalizedCoordinate system, it
             can be also specified as  'up', 'down', 'left', 'right'. Swipe 'up' is equivalent to [0, -0.1], swipe
             'down' is equivalent to [0, 0.1], swipe 'left' is equivalent to [-0.1, 0] and swipe 'right' is equivalent
             to [0.1, 0]
            focus (2-:obj:`tuple`/2-:obj:`list`/:obj:`str`): see :py:meth:`.click() <poco.proxy.UIObjectProxy.click>`
             for more details
            duration (:py:obj:`float`): time interval in which the action is performed

        Raises:
            PocoNoSuchNodeException: raised when the UI element does not exist
        """

        try:
            duration = float(duration)
        except ValueError:
            raise ValueError('Argument `duration` should be <float>. Got {}'.format(repr(duration)))

        focus = focus or self._focus or 'center'
        dir_vec = self._direction_vector_of(direction)
        origin = self.get_position(focus)
        self.poco.pre_action('swipe', self, (origin, dir_vec))
        ret = self.poco.swipe(origin, direction=dir_vec, duration=duration)
        self.poco.post_action('swipe', self, (origin, dir_vec))
        return ret

    def drag_to(self, target, duration=2.0):
        """
        Similar to swipe action, but the end point is provide by a UI proxy or by fixed coordinates.

        Args:
            target (:py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`): a UI proxy or 2-list/2-tuple coordinates
             (x, y) in NormalizedCoordinate system
            duration (:py:obj:`float`): time interval in which the action is performed

        Raises:
            PocoNoSuchNodeException: raised when the UI element does not exist
        """

        try:
            duration = float(duration)
        except ValueError:
            raise ValueError('Argument `duration` should be <float>. Got {}'.format(repr(duration)))

        if type(target) in (list, tuple):
            target_pos = target
        else:
            target_pos = target.get_position()
        origin_pos = self.get_position()
        dir_ = [target_pos[0] - origin_pos[0], target_pos[1] - origin_pos[1]]
        return self.swipe(dir_, duration=duration)

    def scroll(self, direction='vertical', percent=0.6, duration=2.0):
        """
        Simply touch down from point A and move to point B then release up finally. This action is performed within
        specific motion range and duration.

        Args:
            direction (:py:obj:`str`): scrolling direction. "vertical" or "horizontal"
            percent (:py:obj:`float`): scrolling distance percentage of selected UI height or width according to
             direction
            duration (:py:obj:`float`): time interval in which the action is performed

        Raises:
            PocoNoSuchNodeException: raised when the UI element does not exist
        """

        if direction not in ('vertical', 'horizontal'):
            raise ValueError('Argument `direction` should be one of "vertical" or "horizontal". Got {}'
                             .format(repr(direction)))

        focus1 = self._focus or [0.5, 0.5]
        focus2 = list(focus1)
        half_distance = percent / 2
        if direction == 'vertical':
            focus1[1] += half_distance
            focus2[1] -= half_distance
        else:
            focus1[0] += half_distance
            focus2[0] -= half_distance

        return self.focus(focus1).drag_to(self.focus(focus2), duration=duration)

    def pinch(self, direction='in', percent=0.6, duration=2.0, dead_zone=0.1):
        """
        Squeezing or expanding 2 fingers on this UI with given motion range and duration.

        Args:
            direction (:py:obj:`str`): pinching direction, only "in" or "out". "in" for squeezing, "out" for expanding
            percent (:py:obj:`float`): squeezing range from or expanding range to of the bounds of the UI
            duration (:py:obj:`float`): time interval in which the action is performed
            dead_zone (:py:obj:`float`): pinching inner circle radius. should not be greater than ``percent``

        Raises:
            PocoNoSuchNodeException: raised when the UI element does not exist
        """

        if direction not in ('in', 'out'):
            raise ValueError('Argument `direction` should be one of "in" or "out". Got {}'.format(repr(direction)))
        if dead_zone >= percent:
            raise ValueError('Argument `dead_zone` should not be greater than `percent`. dead_zoon={}, percent={}'
                             .format(repr(dead_zone), repr(percent)))

        w, h = self.get_size()
        x, y = self.get_position()
        # focus = self._focus or [0.5, 0.5]
        tracks = make_pinching(direction, [x, y], [w, h], percent, dead_zone, duration)
        speed = math.sqrt(w * h) * (percent - dead_zone) / 2 / duration

        # 速度慢的时候，精度适当要提高，这样有助于控制准确
        ret = self.poco.apply_motion_tracks(tracks, accuracy=speed * 0.03)
        return ret

    def pan(self, direction, duration=2.0):
        raise NotImplementedError

    def start_gesture(self):
        """
        Start a gesture action. This method will return a :py:class:`PendingGestureAction
        <poco.gesture.PendingGestureAction>` object which is able to generate decomposed gesture steps. You can invoke
        ``.to`` and ``.hold`` any times in a chain. See the following example.

        Examples:
            ::

                poco = Poco(...)
                ui1 = poco('xxx')
                ui2 = poco('yyy')

                # touch down on ui1 and hold for 1s
                # then drag to ui2 and hold for 1s
                # finally release(touch up)
                ui1.start_gesture().hold(1).to(ui2).hold(1).up()

        .. note:: always starts touching down at the position of current UI object.

        Returns:
            :py:class:`PendingGestureAction <poco.gesture.PendingGestureAction>`: an object for building serialized
            gesture action.
        """

        return PendingGestureAction(self.poco, self)

    def focus(self, f):
        """
        Get a new UI proxy copy with the given focus. Return a new UI proxy object as the UI proxy is immutable.

        Args:
            f (2-:obj:`tuple`/2-:obj:`list`/:obj:`str`): the focus point, it can be specified as 2-list/2-tuple
             coordinates (x, y) in NormalizedCoordinate system or as 'center' or 'anchor'.

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: a new UI proxy object (copy)
        """
        ret = copy.copy(self)
        ret._focus = f
        return ret

    @volatile_attribute
    def get_position(self, focus=None):
        """
        Get the position of the UI elements.

        Args:
            focus: focus point of UI proxy,  see :py:meth:`.focus() <poco.proxy.UIObjectProxy.focus>` for more details

        Returns:
            2-list/2-tuple: coordinates (x, y) in NormalizedCoordinate system

        Raises:
            TypeError: raised when unsupported focus type is specified
        """
        focus = focus or self._focus or 'center'
        if focus == 'anchor':
            pos = list(map(float, self.attr('pos')))
        elif focus == 'center':
            x, y = map(float, self.attr('pos'))
            w, h = self.get_size()
            ap_x, ap_y = map(float, self.attr("anchorPoint"))
            fx, fy = 0.5, 0.5
            pos = [x + w * (fx - ap_x), y + h * (fy - ap_y)]
        elif type(focus) in (list, tuple):
            x, y = map(float, self.attr('pos'))
            w, h = self.get_size()
            ap_x, ap_y = map(float, self.attr("anchorPoint"))
            fx, fy = focus
            pos = [x + w * (fx - ap_x), y + h * (fy - ap_y)]
        else:
            raise TypeError('Unsupported focus type {}. '
                            'Only "anchor/center" or 2-list/2-tuple available.'.format(type(focus)))
        return pos

    def _direction_vector_of(self, dir_):
        if dir_ == 'up':
            dir_vec = [0, -0.1]
        elif dir_ == 'down':
            dir_vec = [0, 0.1]
        elif dir_ == 'left':
            dir_vec = [-0.1, 0]
        elif dir_ == 'right':
            dir_vec = [0.1, 0]
        elif type(dir_) in (list, tuple):
            dir_vec = dir_
        else:
            raise TypeError('Unsupported direction type {}. '
                            'Only "up/down/left/right" or 2-list/2-tuple available.'.format(type(dir_)))
        return dir_vec

    def wait(self, timeout=3):
        """
        Block and wait for max given time before the UI element appears.

        Args:
            timeout: maximum waiting time in seconds

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: self
        """

        start = time.time()
        while not self.exists():
            self.poco.sleep_for_polling_interval()
            if time.time() - start > timeout:
                break
        return self

    def wait_for_appearance(self, timeout=120):
        """
        Block and wait until the UI element **appears** within the given timeout. When timeout, the
        :py:class:`PocoTargetTimeout <poco.exceptions.PocoTargetTimeout>` is raised.

        Args:
            timeout: maximum waiting time in seconds

        Raises:
            PocoTargetTimeout: when timeout
        """

        start = time.time()
        while not self.exists():
            self.poco.sleep_for_polling_interval()
            if time.time() - start > timeout:
                raise PocoTargetTimeout('appearance', self)

    def wait_for_disappearance(self, timeout=120):
        """
        Block and wait until the UI element **disappears** within the given timeout.

        Args:
            timeout: maximum waiting time in seconds

        Raises:
            PocoTargetTimeout: when timeout
        """

        start = time.time()
        while self.exists():
            self.poco.sleep_for_polling_interval()
            if time.time() - start > timeout:
                raise PocoTargetTimeout('disappearance', self)
            # 强制重新获取节点状态，避免节点已经存在、又消失后，这里不会刷新节点信息导致exists()永远为True的bug
            self.invalidate()

    @refresh_when(PocoTargetRemovedException)
    def attr(self, name):
        """
        Retrieve the attribute of UI element by given attribute name. Return None if attribute does not exist.
        If attribute type is :obj:`str`, it is encoded to utf-8 as :obj:`str` in Python2.7.

        Args:
            name: 
                attribute name, it can be one of the following or any other customized type implemented by SDK

                - visible: whether or not it is visible to user
                - text: string value of the UI element
                - type: the type name of UI element from remote runtime
                - pos: the position of the UI element
                - size: the percentage size [width, height] in range of 0~1 according to the screen
                - name: the name of UI element
                - ...: other sdk implemented attributes

        Returns:
            None if no such attribute or its value is None/null/nil/etc. Otherwise the attribute value is returned. The
            returned value type is json serializable. In both py2 and py3, if the attribute value in remote is a
            text-like object, the return value type will be :obj:`str`.

        Raises:
            PocoNoSuchNodeException: when the UI element does not exists

        .. note:: Exception :py:class:`NodeHasBeenRemovedException` is caught automatically.
        
        See Also:
            :py:meth:`UI element attributes in poco sdk definition <poco.sdk.AbstractNode.AbstractNode.getAttr>`.
        """

        # to optimize performance speed, retrieve only the first matched element.
        # 优化速度，只选择第一个匹配到的节点
        nodes = self._do_query(multiple=False)
        val = self.poco.agent.hierarchy.getAttr(nodes, name)
        if six.PY2 and isinstance(val, six.text_type):
            # 文本类型的属性值，只在python2里encode成utf-8的str，python3保持str类型
            # 这是为了在写代码的时候，无论py2/3始终可以像下面这样写
            # node.attr('text') == '节点属性值'
            val = val.encode('utf-8')
        return val

    @refresh_when(PocoTargetRemovedException)
    def setattr(self, name, val):
        """
        Change the attribute value of the UI element. Not all attributes can be casted to text. If changing the
        immutable attributes or attributes which do not exist, the InvalidOperationException exception is raised.

        Args:
            name: attribute name
            val: new attribute value to cast

        Raises:
            InvalidOperationException: when it fails to set the attribute on UI element
        """

        nodes = self._do_query(multiple=False)
        try:
            return self.poco.agent.hierarchy.setAttr(nodes, name, val)
        except UnableToSetAttributeException as e:
            raise InvalidOperationException('"{}" of "{}"'.format(str(e), self))

    @volatile_attribute
    def exists(self):
        """
        Test whether the UI element is in the hierarchy. Similar to :py:meth:`.attr('visible')
        <poco.proxy.UIObjectProxy.attr>`.

        Returns:
            bool: True if exists otherwise False
        """

        try:
            return self.attr('visible')
        except (PocoTargetRemovedException, PocoNoSuchNodeException):
            return False

    def get_text(self):
        """
        Get the text attribute of the UI element. Return None if no such attribute. Similar to :py:meth:`.attr('text')
        <poco.proxy.UIObjectProxy.attr>`.

        Returns:
            :obj:`str`: None if the UI element does not have the text element, otherwise the utf-8 encoded text value.
            In both py2 and py3, the return value type will be :obj:`str`.
        """

        text = self.attr('text')
        return text

    def set_text(self, text):
        """
        Set the text attribute of the UI element. If the UI element does not support mutation, an exception is raised

        Args:
            text: the text value to be set

        Raises:
            InvalidOperationException: when unable to mutate text value of the UI element
        """

        return self.setattr('text', text)

    def get_name(self):
        """
        Get the UI element name attribute

        Returns:
            :obj:`str`: UI element name attribute
        """

        return self.attr('name')

    @volatile_attribute
    def get_size(self):
        """
        Get the UI element size in ``NormalizedCoordinate`` system.

        Returns:
            2-:obj:`list`: size [width, height] in range of 0 ~ 1.
        """

        return self.attr('size')

    @volatile_attribute
    def get_bounds(self):
        """
        Get the parameters of bounding box of the UI element.

        Returns:
            :obj:`list` <:obj:`float`>: 4-list (top, right, bottom, left) coordinates related to the edge of screen in
            NormalizedCoordinate system
        """

        size = self.get_size()
        top_left = self.get_position([0, 0])

        # t, r, b, l
        bounds = [top_left[1], top_left[0] + size[0], top_left[1] + size[1], top_left[0]]
        return bounds

    def __str__(self):
        if six.PY2:
            return 'UIObjectProxy of "{}"'.format(query_expr(self.query)).encode("utf-8")
        else:
            return 'UIObjectProxy of "{}"'.format(query_expr(self.query))

    if six.PY2:
        def __unicode__(self):
            return 'UIObjectProxy of "{}"'.format(query_expr(self.query))

    __repr__ = __str__

    @property
    def nodes(self):
        """
        Readonly property accessing the UI element(s) in the remote runtime.
        """

        return self._do_query()

    def invalidate(self):
        """
        Clear the flag to indicate to re-query or re-select the UI element(s) from hierarchy.

        alias is refresh()

        Example:
            >>> a = poco(text="settings")
            >>> print(a.exists())
            >>> a.refresh()
            >>> print(a.exists())
        """

        self._evaluated = False
        self._nodes = None

    # refresh is alias of invalidate
    # use poco(xxx).refresh() to force the UI element(s) to re-query
    refresh = invalidate

    def _do_query(self, multiple=True, refresh=False):
        if not self._evaluated or refresh:
            self._nodes = self.poco.agent.hierarchy.select(self.query, multiple)
            if not self._nodes or len(self._nodes) == 0:
                # 找不到节点时，将当前节点状态重置，强制下一次访问时重新查询一次节点信息
                self.invalidate()
                raise PocoNoSuchNodeException(self)
            self._evaluated = True
            self._query_multiple = multiple
        return self._nodes
