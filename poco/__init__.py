# coding=utf-8
from __future__ import unicode_literals

import time
import traceback
import warnings

from .acceleration import PocoAccelerationMixin
from .assertions import PocoAssertionMixin
from .exceptions import PocoTargetTimeout, InvalidOperationException
from .proxy import UIObjectProxy
from .agent import PocoAgent
from .freezeui.utils import create_immutable_hierarchy

__author__ = 'lxn3032'


class Poco(PocoAssertionMixin, PocoAccelerationMixin):
    """
    Poco standard initializer.

    Args:
        agent (:py:class:`PocoAgent <poco.agent.PocoAgent>`): An agent object for poco to communication with 
         target device. See :py:class:`PocoAgent <poco.agent.PocoAgent>`'s definition.
        options:
            - action_interval: The time after an action(like touch/swipe) performed on device to wait for the UI becoming stable. default 
              0.8s.
            - poll_interval: The minimal time between each poll event. Such as waiting for some UI to appear and it will 
              be polling periodically.
            - pre_action_wait_for_appearance: Before actions like click or swipe, it will wait for at most this time to 
              wait for appearance. If the target does not show up after that, raise :py:class:`PocoNoSuchNodeException  
              <poco.exceptions.PocoNoSuchNodeException>` will raise.
    """

    def __init__(self, agent, **options):
        super(Poco, self).__init__()
        self._agent = agent

        # options
        self._pre_action_wait_for_appearance = options.get('pre_action_wait_for_appearance', 6)
        self._post_action_interval = options.get('action_interval', 0.8)
        self._poll_interval = options.get('poll_interval', 1.44)

        self._pre_action_callbacks = [self.on_pre_action.__func__]
        self._post_action_callbacks = [self.on_post_action.__func__]

    def __call__(self, name=None, **kw):
        """
        Simply call poco instance to select UI element by query conditions. You can specify the name or other 
        attributes together in query condition. Invisible UI element will be skipped even "visible=False" is given.  

        Selection is not executed instantly. The query string will be store in the UI proxy. Selection can be executed 
        exactly when UI elements' info is needed (like position to click, or attribute to retrieve).

        Examples:
            This example shows selecting a Button whose name is 'close'::

                poco = Poco(...)
                close_btn = poco('close', type='Button')

        Args:
            name (:obj:`str`): Select UI element(s) by name.

        Keyword Args:
            xx: Arbitrary key value pairs stands for selecting by ``UI.xx``'s value matching.
            xxMatches (:obj:`str`): Arbitrary key value pairs stands for selecting by ``UI.xx``'s value matching the 
             regular pattern

        In keyword args, xx is the attribute name and should be unique that is to choose only one matching way. ::

            # select UI element(s) whose text attribute matches the pattern '^close.*$'
            poco = Poco(...)
            arb_close_btn = poco(textMatches='^close.*$')

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: UI proxy object representing the UI element matches \
             given query condition.
        """

        if not name and len(kw) == 0:
            warnings.warn("Wildcard selector may cause performance trouble. Please give at least one condition to "
                          "shrink range of results")
        return UIObjectProxy(self, name, **kw)

    def wait_for_any(self, objects, timeout=120):
        """
        Wait until any of given UI proxies show up before timeout and return the first appeared UI proxy.
        All UI proxies will be polled periodically. See option :py:class:`poll_interval <poco.Poco>` in 
        ``Poco``'s initialization.

        Args:
            objects (Iterable<:py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`>): Iterable of the given UI proxies.
            timeout (:obj:`float`): timeout in seconds. 120s by default.

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: the first appeared UI proxy.

        Raises:
            PocoTargetTimeout: When none of UI proxies appeared before timeout.
        """

        start = time.time()
        while True:
            for obj in objects:
                if obj.exists():
                    return obj
            if time.time() - start > timeout:
                raise PocoTargetTimeout('any to appear', repr(objects).decode('utf-8'))
            self.sleep_for_polling_interval()

    def wait_for_all(self, objects, timeout=120):
        """
        Wait until all of given UI proxies show up before timeout.
        All UI proxies will be polled periodically. See option :py:class:`poll_interval <poco.Poco>` in 
        ``Poco``'s initialization.

        Args:
            objects (Iterable<:py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`>): Iterable of the given UI proxies.
            timeout (:obj:`float`): timeout in seconds. 120s by default.

        Raises:
            PocoTargetTimeout: When not all of UI proxies appeared before timeout.
        """

        start = time.time()
        while True:
            all_exist = True
            for obj in objects:
                if not obj.exists():
                    all_exist = False
                    break
            if all_exist:
                return
            if time.time() - start > timeout:
                raise PocoTargetTimeout('all to appear', repr(objects).decode('utf-8'))
            self.sleep_for_polling_interval()

    def freeze(this):
        """
        Snapshot current hierarchy and cache it into a new poco instance. This new poco instance is a copy from current 
        poco instance (``self``). The hierarchy of the new poco instance is fixed and immutable. It will return directly
        when invoking ``dump``.

        Returns:
            :py:class:`Poco <poco.Poco>`: A new poco instance copy from current poco instance (``self``).
        """

        class FreezedPoco(Poco):
            def __init__(self):
                hierarchy_dict = this.agent.hierarchy.dump()
                hierarchy = create_immutable_hierarchy(hierarchy_dict)
                agent_ = PocoAgent(hierarchy, this.agent.input, this.agent.screen)
                super(FreezedPoco, self).__init__(agent_, action_interval=0.01, pre_action_wait_for_appearance=0)
                self._pre_action_callbacks = this._pre_action_callbacks
                self._post_action_callbacks = this._post_action_callbacks

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

        return FreezedPoco()

    def wait_stable(self):
        """
        Sleep fixed seconds in order to wait for the UI becoming stable.
        There is no need to call this method manually. It's automatically invoked in cases.  
        """

        time.sleep(self._post_action_interval)

    def sleep_for_polling_interval(self):
        """
        Sleep fixed seconds after each polling.
        There is no need to call this method manually. It's automatically invoked in cases.  
        """

        time.sleep(self._poll_interval)

    @property
    def agent(self):
        """
        Readonly property to access poco agent instance. See :py:class:`poco.agent.PocoAgent` to get more details.

        Returns:
            :py:class:`poco.agent.PocoAgent`: poco agent instance.
        """

        return self._agent

    def click(self, pos):
        """
        Perform click(touch, tap, etc.) action on target device at given coordinate. 

        The coordinate is a 2-list or
        2-tuple (x, y). The coordinate value x, y should be in range of 0 ~ 1 that indicates the percentage range of 
        the screen. For example, ``[0.5, 0.5]`` is the center of the screen, ``[0, 0]`` represents the top left corner. 
        See ``CoordinateSystem`` to get more details about coordinate system.

        Examples:
            Click a point of ``(100, 100)`` of screen whose resolution is ``(1920, 1080)``, the statement as follows::

                poco.click([100.0 / 1920, 100.0 / 1080])

        Args:
            pos (:obj:`list(float, float)` / :obj:`tuple(float, float)`): coordinate (x, y) in range of 0 to 1.

        Raises:
            InvalidOperationException: When click outside screen.
        """

        if not (0 <= pos[0] <= 1) or not (0 <= pos[1] <= 1):
            raise InvalidOperationException('Click position out of screen. {}'.format(repr(pos).decode('utf-8')))
        self.agent.input.click(pos[0], pos[1])

    def swipe(self, p1, p2=None, direction=None, duration=2.0):
        """
        Perform swipe action on target device from given start to end point, or a 2-list/2-tuple value as direction
        vector.

        The coordinate definition of points is the same as ``click``. The components of direction vector (x, y)
        is also represents the range of the screen from 0 to 1.
        See ``CoordinateSystem`` to get more details about coordinate system.
        Should provide at least one of the end point or direction.

        Examples:
            Here is a screen with resolution 1920x1080. Swipe from (100, 100) to (100, 200) could be a statement as
            follows::

                poco.swipe([100.0 / 1920, 100.0 / 1080], [100.0 / 1920, 200.0 / 1080])

            Or give a specific direction instead of end point::

                poco.swipe([100.0 / 1920, 100.0 / 1080], direction=[0, 100.0 / 1080])

        Args:
            p1 (:obj:`2-list/2-tuple`): start point.
            p2: end point.
            direction: swipe direction.
            duration (:obj:`float`): The time over the whole action.

        Raises:
            InvalidOperationException: When swipe start point outside the screen.
        """

        if not (0 <= p1[0] <= 1) or not (0 <= p1[1] <= 1):
            raise InvalidOperationException('Swipe origin out of screen. {}'.format(repr(p1).decode('utf-8')))
        if direction is not None:
            p2 = [p1[0] + direction[0], p1[1] + direction[1]]
        elif p2 is not None:
            p2 = p2
        else:
            raise TypeError('Swipe end not set.')
        self.agent.input.swipe(p1[0], p1[1], p2[0], p2[1], duration)

    def long_click(self, pos, duration=2.0):
        """
        Similar to click, but hold for a given duration and then release.

        Args:
            pos (:obj:`2-list/2-tuple`): coordinate (x, y) in range of 0 to 1.
            duration: The time over the whole action.
        """

        if not (0 <= pos[0] <= 1) or not (0 <= pos[1] <= 1):
            raise InvalidOperationException('Click position out of screen. {}'.format(repr(pos).decode('utf-8')))
        self.agent.input.longClick(pos[0], pos[1], duration)

    def snapshot(self, width=720):
        """
        Take a screenshot from the target device. The format (png, jpg, etc.) depends on the agent implementation.

        Args:
            width (:obj:`int`): Expected width of the screen shot. The real size is depending on agent implementation.
             It may not be able to get a expected width of the screen shot.

        Returns:
            2-tuple:
                - screen_shot (:obj:`str/bytes`): Screen shot data with base64 encoded.
                - format (:obj:`str`): 'png', 'jpg', etc.
        """

        return self.agent.screen.getScreen(width)

    def get_screen_size(self):
        """
        Get real physical resolution of the screen of target device.

        Returns:
            tuple: screen physical resolution in pixels in floats.
        """

        return self.agent.screen.getPortSize()

    def command(self, cmd, type=None):
        return self.agent.command.command(cmd, type)

    def on_pre_action(self, action, proxy, args):
        pass

    def on_post_action(self, action, proxy, args):
        pass

    def add_pre_action_callback(self, cb):
        """
        Register a callback function to be invoked before each action(like touch/swipe).

        The callback function's arguments defines as follows:

        - action (:obj:`str`): The action's name or tag.
        - proxy (:py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>` or :obj:`NoneType`): The related UI proxy that
          involves in the action.
        - args (:obj:`tuple`): All arguments of the specific action function.

        Args:
            cb: the callback function
        """

        self._pre_action_callbacks.append(cb)

    def add_post_action_callback(self, cb):
        """
        Register a callback function to be invoked after each action(like touch/swipe).

        3 arguments that passes to callback functions is identical to the callback function in
        :py:meth:`add_pre_action_callback <poco.Poco.add_pre_action_callback>`.

        Args:
            cb: the callback function
        """

        self._post_action_callbacks.append(cb)

    def pre_action(self, action, proxy, args):
        for cb in self._pre_action_callbacks:
            try:
                cb(self, action, proxy, args)
            except:
                warnings.warn("Error occurred at pre action stage.\n{}".format(traceback.format_exc()))

    def post_action(self, action, proxy, args):
        for cb in self._post_action_callbacks:
            try:
                cb(self, action, proxy, args)
            except:
                warnings.warn("Error occurred at post action stage.\n{}".format(traceback.format_exc()))
