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
    """
    UI Proxy class that represents UI element on target device.

    Any action performing on this instance is handled by poco. It is unnecessary to initialize this object manually.
    See ``QueryCondition`` to get more details about how to select UI elements.

    Args:
        poco: The poco instance.
        name: Query condition of attribute "name". This means you gonna select UI elements whose name is ``name``.
        attrs: The other query conditions except ``name``.

    See Also:
        :py:meth:`select UI element(s) by poco <poco.Poco.__call__>`
    """

    def __init__(self, poco, name=None, **attrs):
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
        Select direct child(ren) from this UI element(s) with given query conditions.
        See ``QueryCondition`` to get more details about selectors.

        Args:
            name: Query condition of attribute "name". This means you gonna select UI elements whose name is ``name``.
            attrs: The other query conditions except ``name``.

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: A new UI proxy object represents the child(ren) of \
             current UI elements.
        """

        sub_query = build_query(name, **attrs)
        query = ('/', (self.query, sub_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def children(self):
        """
        The same as :py:meth:`.child() <poco.proxy.UIObjectProxy.child>` but select all children from this UI 
        element(s).

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: A new UI proxy object.
        """

        return self.child()

    def offspring(self, name=None, **attrs):
        """
        Select any offsprings include direct child(ren) from this UI element(s) with given query conditions.
        See ``QueryCondition`` to get more details about selectors.

        Args:
            name: Query condition of attribute "name". This means you gonna select UI elements whose name is ``name``.
            attrs: The other query conditions except ``name``.

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: A new UI proxy object represents the child(ren) of \
             current UI elements.
        """

        sub_query = build_query(name, **attrs)
        query = ('>', (self.query, sub_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def sibling(self, name=None, **attrs):
        """
        Select sibling(s) from this UI element(s) with given query conditions.
        See ``QueryCondition`` to get more details about selectors.

        Args:
            name: Query condition of attribute "name". This means you gonna select UI elements whose name is ``name``.
            attrs: The other query conditions except ``name``.

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: A new UI proxy object represents the child(ren) of \
             current UI elements.
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
        the first one. See ``IterationOverUI`` to get more details.

        Warnings:
            This method may cause performance issue depending on implementation of PocoAgent.

        Args:
            item (:obj:`int`): the index.

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: A new UI proxy object represents the nth of current UI elements.
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

        Returns:
            :obj:`int`: Number of selected UI elements. 0 if none of the UI element matches the query condition of \
             this UI proxy.
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
        return len(nodes)

    def __iter__(self):
        """
        Similar to :py:meth:`.__getitem__() <poco.proxy.UIObjectProxy.__getitem__>` but this method helps to iterate 
        over all UI elements. The order rules of UI elements is the same as :py:meth:`.__getitem__() 
        <poco.proxy.UIObjectProxy.__getitem__>`. See ``IterationOverUI`` to get more details.

        Yields:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: A generator yielding new UI proxy represents the \
             specific UI element iterated over.

        Raises:
            PocoTargetRemovedException: When hierarchy structure changed and attempt to access to an 
             nonexistent UI element over the iteration.
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
        another point offset by the UI element by providing argument ``focus``.
        See ``CoordinateSystem`` to get more details.

        Args:
            focus (2-:obj:`tuple`/2-:obj:`list`/:obj:`str`): An offset point by the top left corner of the UI elements 
             as 2-list/2-tuple (x, y) whose component in range of 0~1. This argument can also be 'anchor' or 'center'. 
             'Center' means to click the center of bounding box of UI element. 
            sleep_interval: Seconds to wait after this action. If not provides, it will wait by default. The default 
             value can be configured by poco initialization. See configuration at poco 
             :py:class:`initialization <poco.Poco>`.

        Raises:
            PocoNoSuchNodeException: Raises when the UI element does not exist.
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
        Perform a swipe action by given direction from this UI element. Notices and limitations see  
        :py:meth:`.click() <poco.proxy.UIObjectProxy.click>`. 

        Args:
            dir (2-:obj:`tuple`/2-:obj:`list`/:obj:`str`): 2-list/2-tuple (x, y) coordinate in NormalizedCoordinate. Can 
             also be one of 'up', 'down', 'left', 'right', 'up' equivalent to [0, -0.1], 'down' equivalent to [0, 0.1], 
             'left' equivalent to [-0.1, 0], 'right' equivalent to [0, 0.1].
            focus (2-:obj:`tuple`/2-:obj:`list`/:obj:`str`): see :py:meth:`.click() <poco.proxy.UIObjectProxy.click>`. 
            duration: The time over the whole action.

        Raises:
            PocoNoSuchNodeException: Raises when the UI element does not exist.
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

        Args:
            target (:py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`): A UI proxy or 2-list/2-tuple (x, y) 
             coordinate in NormalizedCoordinate.
            duration: The time over the whole action.

        Raises:
            PocoNoSuchNodeException: Raises when the UI element does not exist.
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

        Args:
            f (2-:obj:`tuple`/2-:obj:`list`/:obj:`str`): The focus point. Can be 2-list/2-tuple (x, y) coordinate in 
             NormalizedCoordinate, 'center' or 'anchor'.

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: A new UI proxy copy.
        """

        ret = copy.copy(self)
        ret._focus = f
        return ret

    def get_position(self, focus=None):
        """
        Get the position of this UI elements.

        Args:
            focus: Focus point of UI proxy. See :py:meth:`.focus() <poco.proxy.UIObjectProxy.focus>`.

        Returns:
            2-list/2-tuple: coordinate (x, y) in NormalizedCoordinate.

        Raises:
            TypeError: If unsupported focus type given.
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

        Args:
            timeout: Maximum waiting time in seconds.

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: self.
        """

        start = time.time()
        while not self.exists():
            self.poco.sleep_for_polling_interval()
            if time.time() - start > timeout:
                break
        return self

    def wait_for_appearance(self, timeout=120):
        """
        Block and wait until this UI element **appears** within given timeout. Once timeout, 
        :py:class:`PocoTargetTimeout <poco.exceptions.PocoTargetTimeout>` will raise.

        Args:
            timeout: Maximum waiting time in seconds.

        Raises:
            PocoTargetTimeout: If timeout.
        """

        start = time.time()
        while not self.exists():
            self.poco.sleep_for_polling_interval()
            if time.time() - start > timeout:
                raise PocoTargetTimeout('appearance', self)

    def wait_for_disappearance(self, timeout=120):
        """
        Block and wait until this UI element **disappears** within given timeout. 

        Args:
            timeout: Maximum waiting time in seconds.

        Raises:
            PocoTargetTimeout: If timeout.
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
        Return None if attribute does not exist.
        If attribute type is :obj:`str`, it will be encoded to utf-8 as :obj:`str` in PY2.  

        Args:
            name: 
                Attribute name, can be one of the following or other customized related to sdk implementation.

                - visible: Whether or not it is visible to user. 
                - text: String value of the UI element. 
                - type: The type name of UI element from remote runtime. 
                - pos: The position of the UI element. 
                - size: The percentage size [width, height] in range of 0~1 according to the screen.
                - name: The name of UI element. 
                - ...: Other sdk implemented attributes. 

        Returns:
            None if no such attribute or it value is None/null/nil/etc. Otherwise its value will return. \
             The value type should be json serializable.

        Raises:
            PocoNoSuchNodeException: When the UI element does not exists.

        .. note:: :py:class:`NodeHasBeenRemovedException` will be caught automatically.
        
        See Also:
            :py:meth:`UI element's attributes in poco sdk definition <poco.sdk.AbstractNode.AbstractNode.getAttr>`.
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
        """
        Change the attribute value of UI element. Only a few attributes can be mutated such as text. If changes 
        an immutable attributes or attributes not exist, InvalidOperationException will raise. 

        Args:
            name: Attribute name.
            val: New attribute value to mutate.

        Raises:
            InvalidOperationException: When fail to set attribute on UI element.
        """

        nodes = self._do_query(multiple=False)
        try:
            self.poco.agent.hierarchy.setAttr(nodes, name, val)
        except UnableToSetAttributeException as e:
            raise InvalidOperationException('"{}" of "{}"'.format(e.message, self))

    def exists(self):
        """
        Test whether the UI element is in the hierarchy. The same as :py:meth:`.attr('visible') 
        <poco.proxy.UIObjectProxy.attr>`.

        Returns:
            bool: True if exists otherwise False.
        """

        try:
            return self.attr('visible')
        except (PocoTargetRemovedException, PocoNoSuchNodeException):
            return False

    def get_text(self):
        """
        Get the text attribute on UI element. Return None if no such attribute. The same as :py:meth:`.attr('text') 
        <poco.proxy.UIObjectProxy.attr>`.

        Returns:
            :obj:`str`: Text value with utf-8 encoded or None if does not have text attribute.
        """

        text = self.attr('text')
        if six.PY2 and type(text) is unicode:
            text = text.encode('utf-8')
        return text

    def set_text(self, text):
        """
        Get the text attribute on UI element. If this UI element does not support mutation, a exception will raise.

        Args:
            text: The text value to set.

        Raises:
            InvalidOperationException: If unable to mutate text value on UI element.
        """

        self.setattr('text', text)

    def get_name(self):
        """
        Get the UI element's name attribute.

        Returns:
            :obj:`str`: UI element's name attribute.
        """

        return self.attr('name')

    def get_size(self):
        """
        Get the UI element's size in ``NormalizedCoordinate``.

        Returns:
            2-:obj:`list`: [width, height] in range of 0 ~ 1.
        """

        return self.attr('size')

    def get_bounds(self):
        """
        Get the parameters of bounding box of the UI element.

        Returns:
            :obj:`list` <:obj:`float`>: 4-list (top, right, bottom, left) to the edge of screen in NormalizedCoordinate.
        """

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
        Readonly property accessing the UI element in remote runtime.
        """

        return self._do_query()

    def invalidate(self):
        """
        Clear the flag to indicate to re-query or re-select the UI element(s) from hierarchy.
        """

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
